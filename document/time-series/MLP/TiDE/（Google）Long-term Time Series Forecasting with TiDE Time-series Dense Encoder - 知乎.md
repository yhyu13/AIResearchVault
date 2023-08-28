## 论文链接：

Google最近在Arxiv上放了一个基于MLP的预测模型TiDE，效果和SOTA差不多的情况下，有着很高的时间和空间效率。时间序列预测领域，自从DLinear出来之后，X-Former之类的文章越来越少了，基于MLP的文章越来越多了，感兴趣的可以看一下我整理的这个库：

里面按照网络架构的分类（Transformer、MLP、RNN、TCN等），持续更新一些最新的时间序列预测论文。

由于此论文还没有开源代码，我简要写了这个模型的代码供参考，注释很详细，在文中不过多介绍。

## Key Points

### TiDE整体架构

![](https://pic1.zhimg.com/v2-082a1616973b0539cda4e63e08893840_b.jpg)

TiDE模型整体架构如上图。**首先，它也是和PatchTST一样，假设通道独立的**。也就是说将多变量预测转变为多个单变量预测，模型参数共享。通道独立的详细介绍可见：

其次，和PatchTST以及一些基于MLP的预测模型相比，**它不仅利用了过去的序列值（LookBack），而且利用了一些协变量信息，比如静态协变量（Attributes）和在任何时刻均已知的动态协变量（Dynamic Covariates）**。协变量的详细介绍可见：

**模型中的最基本模块如上图右侧所示，叫做Residual Block，其实就是加了Dropout、ReLU非线性、残差连接、LayerNorm的MLP**。模型的编码器和解码器都是用多个Residual Block堆叠而成的。最左侧有个全局的残差连接，只用了一个线性层，实际上就是DLinear做的事情，这种全局残差连接可以使得TiDE理论上最差也和DLinear差不多。下面结合我写的代码介绍编码和解码过程。

导入的库：

```
import torch
import torch.nn as nn
import torch.nn.functional as F
from einops import rearrange
```

一些变量的介绍：

```
# B: Batchsize
# L: Lookback
# H: Horizon
# N: the number of series
# r: the number of covariates for each series
# r_hat: temporalWidth in the paper, i.e., \hat{r} << r
# p: decoderOutputDim in the paper
# hidden_dim: hiddenSize in the paper
```

### Residual Block

![](https://pic4.zhimg.com/v2-16164709a559f84c429f9725d7f47483_b.jpg)

```
class ResidualBlock(nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim, dropout_rate=0.2):
        super(ResidualBlock, self).__init__()
        self.linear_1 = nn.Linear(in_dim, hidden_dim)
        self.linear_2 = nn.Linear(hidden_dim, out_dim)
        self.linear_res = nn.Linear(in_dim, out_dim)
        self.dropout = nn.Dropout(dropout_rate)
        self.layernorm = nn.LayerNorm(out_dim)

    def forward(self, x):
        # x: [B,L,in_dim] or [B,in_dim]
        h = F.relu(self.linear_1(x))  # [B,L,in_dim] -> [B,L,hidden_dim] or [B,in_dim] -> [B,hidden_dim]
        h = self.dropout(self.linear_2(h))  # [B,L,hidden_dim] -> [B,L,out_dim] or [B,hidden_dim] -> [B,out_dim]
        res = self.linear_res(x)  # [B,L,in_dim] -> [B,L,out_dim] or [B,in_dim] -> [B,out_dim]
        out = self.layernorm(h+res)  # [B,L,out_dim] or [B,out_dim] 

        # out: [B,L,out_dim] or [B,out_dim]
        return out
```

### 编码

![](https://pic1.zhimg.com/v2-c5a617edfe003291ff8a22ec8d791e1c_b.jpg)

编码的过程很简单，首先把过去和未来的动态协变量经过一个Residual Block（Feature Projection）再展平，和过去的序列值以及静态协变量拼接起来，一起输入到多个Residual Block堆叠而成的编码器中。

```
class Encoder(nn.Module):
    def __init__(self, layer_num, hidden_dim, r, r_hat, L, H, featureProjectionHidden):
        super(Encoder, self).__init__()
        self.encoder_layer_num = layer_num
        self.horizon = H
        self.feature_projection = ResidualBlock(r, featureProjectionHidden, r_hat)
        self.first_encoder_layer = ResidualBlock(L + 1 + (L + H) * r_hat, hidden_dim, hidden_dim)
        self.other_encoder_layers = nn.ModuleList([
            ResidualBlock(hidden_dim, hidden_dim, hidden_dim) for _ in range(layer_num-1)
            ])

    def forward(self, x, covariates, attributes):
        # x: [B*N,L], covariates: [B*N,1], attributes: [B*N,L+H,r]

        # Feature Projection
        covariates = self.feature_projection(covariates)  # [B*N,L+H,r] -> [B*N,L+H,r_hat]
        covariates_future = covariates[:, -self.horizon:, :]  # [B*N,H,r_hat]

        # Flatten
        covariates_flat = rearrange(covariates, 'b l r -> b (l r)')  # [B*N,L+H,r_hat] -> [B*N,(L+H)*r_hat]

        # Concat
        e = torch.cat([x, attributes, covariates_flat], dim=1)  # [B*N,L+1+(L+H)*r_hat]

        # Dense Encoder
        e = self.first_encoder_layer(e)  # [B*N,L+1+(L+H)*r_hat] -> [B*N,hidden_dim]
        for i in range(self.encoder_layer_num-1):
            e = self.other_encoder_layers[i](e)  # [B*N,hidden_dim] -> [B*N,hidden_dim]

        # e: [B*N,hidden_dim], covariates_future: [B*N,H,r_hat]
        return e, covariates_future
```

### 解码

![](https://pic3.zhimg.com/v2-76dfb2853bd29f12cdf0c1f931e82232_b.jpg)

解码的过程也很简单，首先把编码器的输入送到多个Residual Block堆叠而成的解码器中，然后将解码器输出的结果reshape，并和未来的动态协变量拼接。拼接后的结果再送入一个Residual Block（Temporal Decoder）中即可。

```
class Decoder(nn.Module):
    def __init__(self, layer_num, hidden_dim, r_hat, H, p, temporalDecoderHidden):
        super(Decoder, self).__init__()
        self.decoder_layer_num = layer_num
        self.horizon = H
        self.last_decoder_layer = ResidualBlock(hidden_dim, hidden_dim, p * H)
        self.other_decoder_layers = nn.ModuleList([
                ResidualBlock(hidden_dim, hidden_dim, hidden_dim) for _ in range(layer_num-1)
            ])
        self.temporaldecoder = ResidualBlock(p + r_hat, temporalDecoderHidden, 1)

    def forward(self, e, covariates_future):
        # e: [B*N,hidden_dim], covariates_future: [B*N,H,r_hat]

        # Dense Decoder
        for i in range(self.decoder_layer_num-1):
            e = self.other_decoder_layers[i](e)  # [B*N,hidden_dim] -> [B*N,hidden_dim]
        g = self.last_decoder_layer(e)  # [B*N,hidden_dim] -> [B*N,p*H]

        # Unflatten
        matrixD = rearrange(g, 'b (h p) -> b h p', h=self.horizon)  # [B*N,p*H] -> [B*N,H,p]

        # Stack
        out = torch.cat([matrixD, covariates_future], dim=-1)  # [B*N,H,p+r_hat]

        # Temporal Decoder
        out = self.temporaldecoder(out)  # [B*N,H,p+r_hat] -> [B*N,H,1]
        
        # out: [B*N,H,1]
        return out
```

### TiDE

有了前面的编码器和解码器，加上一个global的残差连接，TiDE模型就很好写了。注意一下代码里面的Channel Independence: Convert Multivariate series to Univariate series的操作即可。

```
class TiDE(nn.Module):
    def __init__(
            self,
            L,
            H,
            r,
            r_hat,
            p,
            hidden_dim,
            encoder_layer_num,
            decoder_layer_num,
            featureProjectionHidden,
            temporalDecoderHidden,
        ):
        super(TiDE, self).__init__()
        self.encoder = Encoder(encoder_layer_num, hidden_dim, r, r_hat, L, H, featureProjectionHidden)
        self.decoder = Decoder(decoder_layer_num, hidden_dim, r_hat, H, p, temporalDecoderHidden)
        self.residual = nn.Linear(L, H)

    def forward(self, x, covariates, attributes):
        # x: [B,L,N], covariates: [B,L+H,N,r], attributes: [B,N,1]
        batch_size = x.size(0)
        
        # Channel Independence: Convert Multivariate series to Univariate series
        x = rearrange(x, 'b l n -> (b n) l')  # [B,L,N] -> [B*N,L]
        covariates = rearrange(covariates, 'b l n r -> (b n) l r')  # [B,L+H,N,r] -> [B*N,L+H,r]
        attributes = rearrange(attributes, 'b n 1 -> (b n) 1')  # [B,N,1] -> [B*N,1]
        
        # Encoder
        e, covariates_future = self.encoder(x, covariates, attributes)

        # Decoder
        out = self.decoder(e, covariates_future)  # out: [B*N,H,1]

        # Global Residual
        prediction = out.squeeze(-1) + self.residual(x)  # prediction: [B*N,H]

        # Reshape
        prediction = rearrange(prediction, '(b n) h -> b h n', b=batch_size)  # [B*N,H] -> [B,H,N]

        # prediction: [B,H,N]
        return prediction
```

## 实验

主要实验如下表，可以看到和PatchTST的性能差不多：

![](https://pic1.zhimg.com/v2-e84e134f34eb2ffbcc31778154a4abe8_b.jpg)

但是，TiDE的时空效率非常高，要远远高于X-Former之类的模型。如下图，无论是推理时间还是训练时间都非常快，而且空间复杂度也很低，能够处理非常长的序列而不爆显存。

![](https://pic1.zhimg.com/v2-da6f79128ef8cd9b4a2bef120ba8ae2c_b.jpg)

## Comments

TiDE应该是最近的基于MLP的预测模型中效果最能打的了，相比于其他MLP的模型，也考虑到了对于预测任务比较重要的协变量信息（时变的协变量信息或静态的协变量信息）。而且整体思路也很简单，实现起来也很简单。整体代码如下：

```
import torch
import torch.nn as nn
import torch.nn.functional as F
from einops import rearrange


# B: Batchsize
# L: Lookback
# H: Horizon
# N: the number of series
# r: the number of covariates for each series
# r_hat: temporalWidth in the paper, i.e., \hat{r} << r
# p: decoderOutputDim in the paper
# hidden_dim: hiddenSize in the paper


class ResidualBlock(nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim, dropout_rate=0.2):
        super(ResidualBlock, self).__init__()
        self.linear_1 = nn.Linear(in_dim, hidden_dim)
        self.linear_2 = nn.Linear(hidden_dim, out_dim)
        self.linear_res = nn.Linear(in_dim, out_dim)
        self.dropout = nn.Dropout(dropout_rate)
        self.layernorm = nn.LayerNorm(out_dim)

    def forward(self, x):
        # x: [B,L,in_dim] or [B,in_dim]
        h = F.relu(self.linear_1(x))  # [B,L,in_dim] -> [B,L,hidden_dim] or [B,in_dim] -> [B,hidden_dim]
        h = self.dropout(self.linear_2(h))  # [B,L,hidden_dim] -> [B,L,out_dim] or [B,hidden_dim] -> [B,out_dim]
        res = self.linear_res(x)  # [B,L,in_dim] -> [B,L,out_dim] or [B,in_dim] -> [B,out_dim]
        out = self.layernorm(h+res)  # [B,L,out_dim] or [B,out_dim] 

        # out: [B,L,out_dim] or [B,out_dim]
        return out


class Encoder(nn.Module):
    def __init__(self, layer_num, hidden_dim, r, r_hat, L, H, featureProjectionHidden):
        super(Encoder, self).__init__()
        self.encoder_layer_num = layer_num
        self.horizon = H
        self.feature_projection = ResidualBlock(r, featureProjectionHidden, r_hat)
        self.first_encoder_layer = ResidualBlock(L + 1 + (L + H) * r_hat, hidden_dim, hidden_dim)
        self.other_encoder_layers = nn.ModuleList([
            ResidualBlock(hidden_dim, hidden_dim, hidden_dim) for _ in range(layer_num-1)
            ])

    def forward(self, x, covariates, attributes):
        # x: [B*N,L], covariates: [B*N,1], attributes: [B*N,L+H,r]

        # Feature Projection
        covariates = self.feature_projection(covariates)  # [B*N,L+H,r] -> [B*N,L+H,r_hat]
        covariates_future = covariates[:, -self.horizon:, :]  # [B*N,H,r_hat]

        # Flatten
        covariates_flat = rearrange(covariates, 'b l r -> b (l r)')  # [B*N,L+H,r_hat] -> [B*N,(L+H)*r_hat]

        # Concat
        e = torch.cat([x, attributes, covariates_flat], dim=1)  # [B*N,L+1+(L+H)*r_hat]

        # Dense Encoder
        e = self.first_encoder_layer(e)  # [B*N,L+1+(L+H)*r_hat] -> [B*N,hidden_dim]
        for i in range(self.encoder_layer_num-1):
            e = self.other_encoder_layers[i](e)  # [B*N,hidden_dim] -> [B*N,hidden_dim]

        # e: [B*N,hidden_dim], covariates_future: [B*N,H,r_hat]
        return e, covariates_future


class Decoder(nn.Module):
    def __init__(self, layer_num, hidden_dim, r_hat, H, p, temporalDecoderHidden):
        super(Decoder, self).__init__()
        self.decoder_layer_num = layer_num
        self.horizon = H
        self.last_decoder_layer = ResidualBlock(hidden_dim, hidden_dim, p * H)
        self.other_decoder_layers = nn.ModuleList([
                ResidualBlock(hidden_dim, hidden_dim, hidden_dim) for _ in range(layer_num-1)
            ])
        self.temporaldecoder = ResidualBlock(p + r_hat, temporalDecoderHidden, 1)

    def forward(self, e, covariates_future):
        # e: [B*N,hidden_dim], covariates_future: [B*N,H,r_hat]

        # Dense Decoder
        for i in range(self.decoder_layer_num-1):
            e = self.other_decoder_layers[i](e)  # [B*N,hidden_dim] -> [B*N,hidden_dim]
        g = self.last_decoder_layer(e)  # [B*N,hidden_dim] -> [B*N,p*H]

        # Unflatten
        matrixD = rearrange(g, 'b (h p) -> b h p', h=self.horizon)  # [B*N,p*H] -> [B*N,H,p]

        # Stack
        out = torch.cat([matrixD, covariates_future], dim=-1)  # [B*N,H,p+r_hat]

        # Temporal Decoder
        out = self.temporaldecoder(out)  # [B*N,H,p+r_hat] -> [B*N,H,1]
        
        # out: [B*N,H,1]
        return out


class TiDE(nn.Module):
    def __init__(
            self,
            L,
            H,
            r,
            r_hat,
            p,
            hidden_dim,
            encoder_layer_num,
            decoder_layer_num,
            featureProjectionHidden,
            temporalDecoderHidden,
        ):
        super(TiDE, self).__init__()
        self.encoder = Encoder(encoder_layer_num, hidden_dim, r, r_hat, L, H, featureProjectionHidden)
        self.decoder = Decoder(decoder_layer_num, hidden_dim, r_hat, H, p, temporalDecoderHidden)
        self.residual = nn.Linear(L, H)

    def forward(self, x, covariates, attributes):
        # x: [B,L,N], covariates: [B,L+H,N,r], attributes: [B,N,1]
        batch_size = x.size(0)
        
        # Channel Independence: Convert Multivariate series to Univariate series
        x = rearrange(x, 'b l n -> (b n) l')  # [B,L,N] -> [B*N,L]
        covariates = rearrange(covariates, 'b l n r -> (b n) l r')  # [B,L+H,N,r] -> [B*N,L+H,r]
        attributes = rearrange(attributes, 'b n 1 -> (b n) 1')  # [B,N,1] -> [B*N,1]
        
        # Encoder
        e, covariates_future = self.encoder(x, covariates, attributes)

        # Decoder
        out = self.decoder(e, covariates_future)  # out: [B*N,H,1]

        # Global Residual
        prediction = out.squeeze(-1) + self.residual(x)  # prediction: [B*N,H]

        # Reshape
        prediction = rearrange(prediction, '(b n) h -> b h n', b=batch_size)  # [B*N,H] -> [B,H,N]

        # prediction: [B,H,N]
        return prediction
```