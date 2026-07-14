# AI 3D Video Generation 技术演变史报告（2018–2026）

> **报告性质**：技术演变史深度调研  
> **目标读者**：实时图形学从业者（游戏/实时渲染背景）  
> **核心问题**：这个技术是怎么走到今天的？关键转折点是什么？  
> **写作时间**：2026-07-03  
> **字数**：约 8,500 字（含公式与引用）

---

## 摘要

AI 3D Video Generation（人工智能三维视频生成）不是一条单线演进的技术，而是**神经场景表示**、**可微分渲染**、**生成式扩散模型**与**世界模型**四条技术脉络在 2018–2026 年间交叉汇合的结果。从最早的 DeepVoxels 离散体素尝试，到 NeRF 用单个 MLP 编码连续 5D 辐射场，再到 3D Gaussian Splatting 以显式高斯原语实现实时渲染，最后到 Sora 等视频生成模型将「生成」本身重构为「世界模拟」——这条路径上的每一次范式转移，都伴随着对「表示（representation）」与「渲染（rendering）」这两个图形学核心问题的重新回答。

本报告按严格的时间线逻辑组织，覆盖 2018 年至 2026 年的关键里程碑论文、技术路线的分化与淘汰、核心团队贡献、与实时图形学/游戏引擎的交集、当前瓶颈，以及对从业者的具体建议。所有技术论断均精确到论文出处、代码仓库或公式层面。

---

## 1. 时间线：从 DeepVoxels 到 World Model（2018→2026）

### 1.1 前 NeRF 时代：隐式表示的萌芽（2018–2019）

在 NeRF 出现之前，基于学习的三维场景表示经历了从「离散」到「连续」的关键转变。

**DeepVoxels**（Sitzmann et al., CVPR 2019）将场景表示为一个带可学习特征向量的体素网格（voxel grid），通过 ray marching 查询特征后送入 CNN 解码器得到颜色。这是「神经场景表示」概念的早期实践，但其根本缺陷在于**分辨率与存储的立方关系**——$128^3$ 的体素网格仅能表达有限的几何细节。

**Neural Volumes**（Lombardi et al., 2019）采用深度 3D CNN 预测一个 $128^3$ 的 RGB$\alpha$ 体素网格以及一个 $32^3$ 的 3D warp 网格，通过扭曲体素来建模非刚性运动。它首次将「可微分体渲染」与「深度学习」结合，但仍然受困于体素分辨率。

**Scene Representation Networks (SRN)**（Sitzmann et al., NeurIPS 2019）是关键的前置工作。SRN 用一个 MLP $f_{\theta}: \mathbb{R}^3 \rightarrow \mathbb{R}^d$ 将每个 3D 坐标映射到特征向量，再用一个循环神经网络沿光线步进，最终解码为颜色。SRN 的数学形式是**连续隐式函数**，避免了离散体素的分辨率限制，但有两个致命问题：（1）不使用位置编码（positional encoding），导致 MLP 的谱偏置（spectral bias）使其只能重建低频信号，输出严重过平滑；（2）采用表面渲染（surface rendering）而非体渲染，每条光线只采样一个点，无法处理半透明或复杂遮挡。

这三项工作的共同启示是：**连续隐式表示在理论上有吸引力，但必须解决高频细节重建与高效渲染的问题。**

### 1.2 NeRF 革命：一个 MLP 统治一切（2020–2021）

**NeRF: Neural Radiance Fields for View Synthesis**（Mildenhall et al., ECCV 2020）是这一领域的第一个范式级突破。NeRF 的核心是一个 MLP $F_{\theta}: (\mathbf{x}, \mathbf{d}) \rightarrow (c, \sigma)$，将 3D 位置 $\mathbf{x} \in \mathbb{R}^3$ 和 2D 视角方向 $\mathbf{d} \in \mathbb{S}^2$ 映射为颜色 $c \in \mathbb{R}^3$ 和体密度 $\sigma \in \mathbb{R}^+$。

NeRF 解决了 SRN 的两个核心问题：

1. **高频细节**：通过**位置编码（Positional Encoding）**将输入坐标映射到高维 Fourier 特征空间：
   $$\gamma(p) = \left[\sin(2^0 \pi p), \cos(2^0 \pi p), \ldots, \sin(2^{L-1} \pi p), \cos(2^{L-1} \pi p)\right]$$
   这本质上是将输入嵌入到多频率正弦基函数张成的空间，使 MLP 能够学习高频信号。Barron et al. 后来在 *Fourier Features Let Networks Learn High Frequency Functions in Low Dimensional Domains*（NeurIPS 2020）中从理论上证明了这一点。

2. **体渲染**：NeRF 采用经典体渲染方程的数值近似：
   $$\hat{C}(\mathbf{r}) = \sum_{i=1}^{N} T_i \alpha_i c_i, \quad T_i = \prod_{j=1}^{i-1} (1 - \alpha_j), \quad \alpha_i = 1 - \exp(-\sigma_i \delta_i)$$
   其中 $\delta_i$ 是相邻采样点之间的距离。这允许每条光线沿深度方向累积多个样本的贡献，正确处理遮挡和半透明。

3. **分层采样（Hierarchical Sampling）**： coarse network + fine network 的两阶段策略，先用 coarse network 的密度预测来引导 fine network 在重要区域密集采样。

然而，原始 NeRF 的代价是沉重的：**训练需要 12–24 小时（单场景），渲染一帧需要数十秒**。这意味着它完全无法用于实时应用。

2020–2021 年，NeRF 的改进沿着两个方向展开：

- **质量提升**：Mip-NeRF（Barron et al., 2021）用圆锥追踪替代光线追踪，解决抗锯齿问题；Mip-NeRF 360（Barron et al., 2022）扩展到无界场景；Ref-NeRF 建模反射；NeRF-W 引入外观嵌入（appearance embedding）处理光照变化。
- **速度优化**：这是一个更关键的战场。SNeRG / PlenOctrees / FastNeRF / KiloNeRF（2020–2021）走的是**baking**路线——将训练好的 NeRF 蒸馏到离散数据结构（稀疏体素八叉树、 thousands of tiny MLPs）中，实现实时渲染但牺牲了可编辑性。NSVF（Liu et al., 2020）采用稀疏体素网格 + 共享 MLP，用体素交集加速光线采样。

### 1.3 效率革命：从小时到秒（2022）

2022 年是神经渲染从「离线」走向「准实时」的关键年份。

**Instant-NGP**（Müller et al., SIGGRAPH 2022）来自 NVIDIA，是 NeRF 时代的最大效率突破。其核心创新是**多分辨率哈希编码（Multiresolution Hash Encoding）**：

$$\mathbf{y} = \text{enc}(\mathbf{x}; \theta_{hash}), \quad (c, \sigma) = MLP(\mathbf{y})$$

场景信息被存储在一个多层级哈希表中（而非 MLP 权重中），MLP 仅作为轻量级解码器。训练时，哈希表与 MLP 同时优化。这使得训练时间从小时级压缩到**秒级**（<1 分钟），同时保持了高质量的渲染效果。

同期还有三条并行路线：
- **Plenoxels**（Fridovich-Keil et al., 2022）：完全抛弃 MLP，直接用稀疏体素网格存储球谐系数，通过体渲染梯度直接优化，训练仅需 11 分钟。
- **DVGO**（Sun et al., 2022）：直接体素网格优化，用三线性插值查表。
- **TensoRF**（Chen et al., 2022）：将 4D 辐射场张量分解为低秩分量（CP / VM 分解），大幅降低参数量。

这些方法的共同趋势是：**将场景信息从 MLP 的隐式权重中「释放」出来，存储到显式的、可高效查询的数据结构中。**这为 2023 年的 Gaussian Splatting 埋下了伏笔。

### 1.4 Gaussian Splatting：显式原语的范式转移（2023）

**3D Gaussian Splatting for Real-Time Radiance Field Rendering**（Kerbl et al., SIGGRAPH 2023）是神经渲染领域的第二次范式革命。与 NeRF 的隐式 MLP 表示截然不同，3DGS 将场景显式表示为一组**各向异性 3D 高斯原语**：

$$G(\mathbf{x}) = \exp\left(-\frac{1}{2}(\mathbf{x} - \boldsymbol{\mu})^\top \boldsymbol{\Sigma}^{-1} (\mathbf{x} - \boldsymbol{\mu})\right)$$

其中协方差矩阵 $\boldsymbol{\Sigma}$ 被参数化为 $\boldsymbol{\Sigma} = \mathbf{R}\mathbf{S}\mathbf{S}^\top\mathbf{R}^\top$，$\mathbf{R} \in SO(3)$ 为旋转，$\mathbf{S} = \text{diag}(s)$ 为尺度。这种参数化保证了 $\boldsymbol{\Sigma}$ 的正定性。

渲染时，每个 3D 高斯被投影到图像平面得到一个 2D 高斯（通过仿射近似），然后使用**tile-based rasterizer**按深度排序后做 front-to-back $\alpha$-blending：

$$C = \sum_{i \in \mathcal{N}} c_i \alpha_i \prod_{j=1}^{i-1}(1 - \alpha_j)$$

3DGS 的关键优势在于：
1. **完全显式**：没有 MLP 查询，渲染就是投影 + 混合，可在 GPU 上高度并行。
2. **可微分**：光度损失 $\mathcal{L} = (1 - \lambda)\mathcal{L}_1 + \lambda \mathcal{L}_{D-SSIM}$ 的梯度可以反向传播到每个高斯的位置、协方差、颜色（用球谐函数 SH 表示）、不透明度。
3. **自适应密度控制**：每 100 次迭代，对梯度较大的高斯进行**克隆**（clone）或**分裂**（split），对不透明度低于阈值的高斯进行**剪枝**（prune）。
4. **实时**：在 RTX 3090 上可达 **100+ FPS**（1080p），训练仅需 **10–30 分钟**。

3DGS 的代价是**显存与存储**：一个复杂场景可能需要数百万个高斯，每个高斯存储 59 个 float（3 位置 + 3 尺度 + 4 旋转四元数 + 1 不透明度 + 48 球谐系数 = 59），总存储可达数百 MB。这催生了后续大量的压缩工作（LightGaussian, EAGLES, Scaffold-GS 等）。

2024 年，**2D Gaussian Splatting**（Huang et al., SIGGRAPH 2024）进一步改进了几何精度，用 2D disk-like surfels 替代 3D 椭球，配合射线- surfel 相交计算得到更准确的深度和法线。

### 1.5 动态场景：从静态 3D 到 4D（2023–2024）

静态场景表示成熟后，领域的自然延伸是**动态场景（dynamic scenes）**——即带有时间维度的 4D 表示。这是连接「3D 重建」与「视频生成」的桥梁。

早期基于 NeRF 的动态方法（D-NeRF, Pumarola et al., 2020）将时间 $t$ 作为额外输入：$F_{\theta}(\mathbf{x}, \mathbf{d}, t) \rightarrow (c, \sigma)$，或用额外的 deformation MLP 将规范空间（canonical space）中的点 warp 到每个时间步。这些方法渲染质量尚可，但训练慢、运动模糊严重。

3DGS 出现后，动态扩展迅速展开，形成了三条技术路线：

**路线 A：Persistent Dynamic Gaussians**（Luiten et al., 2024 / Dynamic 3D Gaussians）。核心思想是：场景不是每帧独立重建，而是**同一组高斯原语随时间持续存在**。每个高斯可以每帧移动和旋转，但其外观参数（颜色、不透明度、大小）保持恒定，运动被局部刚性正则化约束。这篇论文确立了「高斯不只是渲染原语，而是有身份的场景元素」这一理念——这是动态 3DGS 的第一支柱：persistence + motion。

**路线 B：Deformation Field**（Yang et al., 2023 / Deformable 3DGS）。在规范空间（canonical space）中定义一组高斯，用一个 deformation MLP $\mathcal{T}(\mathbf{x}, t)$ 或 Hexplane 表示将规范点 warp 到时间 $t$ 的位置。Hexplane 将 4D 时空体分解为 6 个正交平面（$xy, xz, yz, xt, yt, zt$），通过低秩分解高效编码时空特征。

**路线 C：Native 4D Gaussians**（Tang et al., 2024 / 4D Gaussian Splatting）。将高斯直接提升到 4D 空间，定义一个**原生 4D 高斯原语** $G(\mathbf{x}, t)$，其时空运动由各向异性椭圆在时空中的旋转建模。时间维度用 **4D Spherindrical Harmonics** 编码外观演化，渲染时通过在时间维度切片（time slicing）得到当前时刻的 3D 高斯，再执行标准 splatting。这是第一个支持端到端训练和实时渲染的动态高斯方法。

**路线 D：Physics-Coupled**（Xie et al., 2024 / PhysGaussian）。将 3DGS 与**材料点法（Material Point Method, MPM）**耦合，把高斯视为拉格朗日材料点，在牛顿力学框架下演化。高斯的位置更新由物理模拟驱动：$\mathbf{v}^{n+1} = \mathbf{v}^n + \Delta t \cdot \mathbf{a}$，然后 $\mathbf{x}^{n+1} = \mathbf{x}^n + \Delta t \cdot \mathbf{v}^{n+1}$。这实现了物理正确的动态效果（弹性体、流体、断裂）。

### 1.6 Text-to-3D 与生成式浪潮（2022–2024）

另一条并行的主线是「生成式 3D」——不依赖多视角输入，直接从文本或单张图像生成 3D 内容。

**DreamFusion**（Poole et al., ICLR 2022）是这一方向的奠基工作。它提出 **Score Distillation Sampling (SDS)**：利用预训练的 2D 文本到图像扩散模型（如 Imagen）的 score function 来指导 NeRF 的优化。具体来说，在 NeRF 渲染出的图像上添加噪声，用扩散模型预测去噪方向，并将该方向的梯度通过可微渲染回传到 3D 参数。数学上：

$$\nabla_{\theta} \mathcal{L}_{SDS} = \mathbb{E}_{t, \epsilon} \left[ w(t) \left( \hat{\epsilon}_{\phi}(\mathbf{x}_t; \mathbf{y}, t) - \epsilon \right) \frac{\partial \mathbf{x}}{\partial \theta} \right]$$

其中 $\hat{\epsilon}_{\phi}$ 是扩散模型的噪声预测，$\mathbf{x}_t$ 是加噪后的渲染图。SDS 的直觉是：让渲染图像在扩散模型的概率密度高的区域「漂移」。

SDS 的后续改进包括：
- **Magic3D**（Lin et al., CVPR 2023）：两阶段优化，先用低分辨率 SDS 优化 NeRF，再转换为 DMTet（可变形四面体网格）进行高分辨率表面优化。
- **ProlificDreamer**（Wang et al., 2023）：提出 Variational Score Distillation (VSD)，用粒子变分框架解决 SDS 的 mode collapse 和 oversaturation 问题。
- **Fantasia3D**（Chen et al., 2023）：用 BRDF 建模外观，分离几何与材质。
- **DreamGaussian**（2024）：用 3DGS 替代 NeRF 作为基础表示，利用 splatting 的速度优势将生成时间压缩到数秒。

**Zero-1-to-3**（Liu et al., 2023）开辟了另一条路线：在大规模 3D 合成数据上微调 Stable Diffusion，使其具备视角条件生成能力。给定单张图像和视角参数，模型可以生成该视角下的图像。这启发了后续一系列「单图重建」工作：
- **LGM**（Large Multi-view Gaussian Model, Tang et al., 2024）：前馈网络，单图输入直接输出多视角高斯参数。
- **InstantMesh**（2024）：两阶段，先生成多视角图，再重建网格。
- **TRELLIS**（2025）：结构化 3D 隐空间，可扩展的 3D 生成。

### 1.7 Video Generation 作为 World Model（2024–2026）

2024 年 2 月，OpenAI 发布 **Sora**，彻底改变了视频生成的叙事框架。Sora 不再被描述为一个「视频生成器」，而是被定位为**世界模拟器（world simulator）**。其技术架构的核心包括：

1. **Spacetime Patches**：将输入视频压缩为时空块（spacetime latent patches），每个 patch 是 4D 时空中的一个 token。
2. **Diffusion Transformer (DiT)**：在 latent 空间中，用 Transformer 替代传统的 U-Net 进行扩散去噪。Peebles & Xie (2023) 在 *Scalable Diffusion Models with Transformers* 中证明了 DiT 在图像生成上的可扩展性，Sora 将其扩展到视频。
3. **大规模训练**：Sora 的训练数据量和模型规模未公开，但业界推测其参数量级在数十亿到上百亿。

Sora 发布后，视频生成领域进入爆发期。2024–2026 年的主要里程碑包括：

| 时间 | 模型 | 团队 | 核心贡献 |
|------|------|------|----------|
| 2024.02 | Sora | OpenAI | 世界模拟器范式，60s 连贯视频，物理合理性 |
| 2024.05 | Veo | Google | 文本/图像/视频多模态输入，高保真生成 |
| 2024.06 | KLING | Kuaishou | 最长 2 分钟视频，运动幅度大 |
| 2024.12 | Sora (Turbo) | OpenAI | 公众发布，故事板界面 |
| 2024.12 | Veo 2 | Google DeepMind | 更强的因果关系和提示遵循 |
| 2025.02 | Wan 2.1 | Alibaba | 开源，多尺度，LoRA 微调支持 |
| 2025.02 | OmniHuman-1 | ByteDance | 逼真唇同步与人类运动 |
| 2025.05 | Veo 3 | Google | 原生音视频同步，物理精确 |
| 2025.09 | Sora 2 | OpenAI | 多模态输入，多镜头逻辑 |
| 2025.10 | MAGI-1 | Sand.ai | 自回归流式架构，KV cache，线性复杂度 |
| 2026 | Seedance 2.0 | ByteDance | 全模态条件框架，长叙事一致性 |

学术界将 2024–2026 的视频生成演进归纳为**五个阶段**：
1. **Coherent Pixel Motion**（像素级运动连贯）——Sora 奠基；
2. **Stability and Controllability**（稳定性与可控性）——Cosmos、Wan 2.1；
3. **Physically Grounded Control**（物理 grounded 控制）——Veo 3；
4. **Multimodal Video Integration**（多模态融合）——Sora 2；
5. **Multimodal Long Narratives**（长叙事）——Seedance 2.0。

### 1.8 3D-aware Video Generation：两条主线的交汇（2024–2026）

视频生成与 3D 表示的交汇在 2024 年后成为明确趋势。代表性工作包括：

- **World-consistent Video Diffusion with Explicit 3D Modeling**（2024）：在扩散过程中显式引入 3D 几何约束，保证多视角一致性。
- **GS-DiT**（2025）：通过高效密集 3D 点跟踪构建伪 4D 高斯场，将 Gaussian Splatting 与 Diffusion Transformer 结合。
- **Diffusion as Shader**（2025）：将扩散模型视为可编程 shader，实现 3D 感知的视频生成控制。
- **Geo4D**（Jiang et al., 2025）：利用视频生成器进行几何 4D 场景重建——反向使用生成模型来提取 3D/4D 结构。
- **L4GM**（2025）：Large 4D Gaussian Reconstruction Model，给定单视角视频输入，逐帧生成高斯集合，通过自注意力机制保证时间和视角一致性。

---

## 2. 技术路线演进与分支：哪些对了，哪些被淘汰了

### 2.1 表示方法的分化：从 Implicit 到 Explicit

整个领域最深层的技术演变是「场景表示」本身的变迁：

| 阶段 | 表示方法 | 代表工作 | 渲染方式 | 训练时间 | 渲染速度 |
|------|----------|----------|----------|----------|----------|
| 2018–2019 | 离散体素 | DeepVoxels, Neural Volumes | Ray marching + CNN decode | 小时 | 慢 |
| 2019 | 隐式 MLP | SRN | 表面渲染（单点） | 小时 | 慢 |
| 2020 | 隐式 MLP + PE | NeRF | 体渲染（多点采样） | 12–24h | ~30s/帧 |
| 2022 | 混合（Hash + MLP） | Instant-NGP | 体渲染 + hash lookup | <1min | 实时（baked）|
| 2022 | 显式体素/张量 | Plenoxels, TensoRF | 直接体渲染 | 11–30min | 较快 |
| 2023 | 显式高斯原语 | 3D Gaussian Splatting | Splatting + α-blending | 10–30min | **100+ FPS** |

数学上，NeRF 与 3DGS 的区别可以概括为：
- **NeRF**：$\sigma, c = F_{\theta}(\gamma(\mathbf{x}), \gamma(\mathbf{d}))$ ——查询一个函数；
- **3DGS**：$C_{pixel} = \sum_i c_i \alpha_i \prod_{j<i}(1-\alpha_j)$ ——混合一组原语。

前者是**查询密集型**（query-bound），后者是**内存密集型**（memory-bound）。在 GPU 架构上，splatting 的矩阵操作和并行混合比 MLP 推理更适合现代 GPU 的 SIMT 执行模型。

### 2.2 被证明是正确的思路

1. **可微分渲染（Differentiable Rendering）**：无论是 NeRF 的体渲染还是 3DGS 的 splatting，其核心都是渲染过程对场景参数可微。这使得「渲染图像与真实图像的差异」可以直接反向传播来优化场景。这是连接计算机图形学与深度学习的数学桥梁。

2. **位置编码 / Fourier Features**：从 NeRF 的位置编码到 Instant-NGP 的多分辨率哈希编码，再到 3DGS 的显式原语，本质都是在解决「神经网络学习高频信号」的问题。3DGS 通过将高频信息直接存储在原语参数中，彻底绕过了 MLP 的谱偏置。

3. **Diffusion Prior 用于 3D 生成**：DreamFusion 的 SDS 虽然有不完美之处（oversaturation、mode collapse），但它证明了**2D 扩散模型的强大先验可以被蒸馏到 3D 表示中**，从而绕过了 3D 训练数据稀缺的问题。

4. **显式表示的实时性**：3DGS 证明了「实时神经渲染」不需要 baking，显式原语本身就足够快。这改变了实时图形学对神经渲染的预期。

### 2.3 被淘汰或式微的思路

1. **纯离散体素网格**（如原始 DeepVoxels）：分辨率与存储的 $O(N^3)$ 关系使其无法 scale 到高分辨率场景。现在仅在特定场景（如 Occupancy Networks 的粗糙占用预测）中有残留价值。

2. **纯 MLP 无位置编码**（如 SRN）：没有 Fourier features 的 MLP 无法重建高频细节，已被彻底弃用。

3. **逐帧独立重建**：早期的动态 NeRF 方法每帧独立优化，缺乏时序一致性，已被 persistent tracking 和 4D 原生表示取代。

4. **CLIP-guided 3D 生成**（DreamFields, Jain et al., 2022）：CLIP 的图像-文本对齐信号太弱，无法提供足够的几何监督，被 SDS 和 diffusion prior 完全取代。

5. **Per-scene Optimization**：NeRF 和 3DGS 的原始形式需要为每个新场景重新训练数分钟到数小时。随着 LGM、DUSt3R、VGGT 等 feed-forward 方法的出现，「单前向传播得到 3D」成为新的目标，per-scene optimization 逐渐退居特定细分场景（如超高精度重建）。

### 2.4 当前并行的四大技术路线

截至 2026 年中，AI 3D Video Generation 领域呈现出四条并行但相互渗透的路线：

**路线 I：Diffusion-based Video World Models**（Sora、Veo、Wan）。像素/隐空间中的大规模扩散 Transformer，追求「生成即模拟」。优势是视觉质量极高、通用性强；劣势是缺乏显式 3D 结构，物理正确性无法保证，可控性差。

**路线 II：Gaussian-based Explicit 4D Representation**（4DGS、Dynamic GS、PhysGaussian）。显式高斯原语 + 物理模拟，追求「可渲染、可交互、物理正确」。优势是实时、有显式几何、可编辑；劣势是泛化性差（per-scene），生成内容需要先有输入视频。

**路线 III：Feed-forward 3D/4D Reconstruction**（DUSt3R、VGGT、LGM、L4GM）。从单图/视频直接前馈输出 3D 结构。优势是速度快（秒级）、可泛化；劣势是质量仍不如 per-scene optimization。

**路线 IV：Physics-integrated Neural Rendering**（PhysGaussian、PIDG、GaussianFluent）。将可微渲染与物理求解器（PBD、MPM、FEM）耦合。优势是物理正确性；劣势是需要材料参数，计算开销大。

---

## 3. 核心公司/团队及其贡献

### 3.1 学术界奠基团队

- **UC Berkeley + Google Research**：Ben Mildenhall、Pratul Srinivasan、Jonathan Barron 等人发表了 NeRF 及一系列后续工作（Mip-NeRF、Mip-NeRF 360、Ref-NeRF、Zip-NeRF）。Barron 还在位置编码理论上做出了 foundational 贡献（Fourier Features 论文）。
- **MIT CSAIL + Stanford**：Vincent Sitzmann 团队（DeepVoxels、SRN、SIREN）最早系统探索了神经场景表示。Sitzmann 现在是这一领域最具影响力的年轻学者之一。
- **Inria / Université Côte d\'Azur, France**：Bernhard Kerbl、Georgios Kopanas、George Drettakis 发表了 3D Gaussian Splatting。Drettakis 团队长期在可微渲染和图像合成方面深耕，3DGS 的 tile-based rasterizer 就是他们的工程杰作。
- **Max Planck Institute**：MPI 的多个团队（Christian Theobalt、Michael Zollhöfer 等）在神经人体渲染和动态场景方面做出了大量工作。

### 3.2 工业界主导力量

- **NVIDIA**：Thomas Müller（Instant-NGP）、Alex Evans、Christoph Schied（Neural Volumes 早期工作）。NVIDIA 在神经渲染工具链（tiny-cuda-nn、kaolin）上投入巨大，Cosmos 是其世界模型平台。
- **OpenAI**：Sora、Sora 2 的核心团队未公开，但 Tim Brooks 和 Bill Peebles 是已知的项目负责人。OpenAI 将视频生成重新定义为「世界模拟」，引领了行业叙事。
- **Google DeepMind**：Veo 系列（Veo 1/2/3）、Imagen Video、Lumiere。Google 在 diffusion 模型和多模态生成方面底蕴深厚。
- **Meta / FAIR**：Make-A-Video、VideoJAM、Boximator。Meta 在开源视频生成方面有一定布局。
- **ByteDance**：KLING、OmniHuman、Seedance、Boximator。字节在视频生成的产品化和商业化上走在最前列。
- **Alibaba**：Wan / Wan 2.1 / Wan 2.5，开源社区反响强烈。
- **Kuaishou**：KLING 的最初发布者（后与字节分属不同产品线）。

### 3.3 中国学术界力量

- **清华/北大**：Vidu（生数科技 + 清华）、CogVideoX（智谱 AI）、Zeroscope 等。清华在视频生成的学术产出密度极高。
- **上海 AI Lab**：MVDream、后续的多视角生成工作。
- **香港中文大学 / 香港大学**：大量 Gaussian Splatting 的改进工作（几何精度、压缩、动态场景）。

---

## 4. 与实时图形学/游戏产业的交集点

### 4.1 游戏引擎集成现状

3D Gaussian Splatting 已经被集成到主流游戏引擎中：

- **Unreal Engine 5**：XScene-UEPlugin（XVERSE, 2024）提供了高性能的 3DGS 插件；另有社区插件支持 Gaussian Splatting 的导入和实时渲染。
- **Unity**：GaussianSplattingVRViewerUnity（CLARTE, 2023）是一个基于 OpenXR 的 VR 查看器；多个商业项目已将 3DGS 用于 VR 场景的实时渲染。
- **Web / Three.js**：mkkellogg/GaussianSplats3D 提供了浏览器端的高斯 splatting 渲染，antimatter15/splat 是早期 WebGL 实现。

### 4.2 与经典渲染管线的深层对比

对于实时图形学从业者，理解 3DGS 与传统实时渲染管线的关系至关重要：

| 维度 | 传统实时渲染（UE5/Unity） | 3D Gaussian Splatting |
|------|--------------------------|----------------------|
| 几何表示 | Mesh / Nanite 虚拟几何 | 数百万高斯椭球 |
| 材质 | PBR (Metallic-Roughness) | 球谐函数 (SH) 编码视角相关颜色 |
| 光照 | Lumen / RTX | 烘焙到训练数据中（可 relight） |
| 渲染核心 | Rasterization / Ray tracing | Tile-based splatting + α-blending |
| 抗锯齿 | TAA / MSAA | 多采样 + 高斯自然抗锯齿 |
| 编辑性 | 完全可控（材质、动画、LOD） | 有限（位置/颜色可编辑，但无显式拓扑） |
| 质量天花板 | 依赖艺术家资产 | 照片级（从真实照片训练） |

**关键交集点**：Nanite（UE5 的虚拟化微多边形几何）与 3DGS 在哲学上有相似之处——两者都抛弃了传统 LOD 链，采用了一种「按需实例化/投影」的策略。但 Nanite 仍然是确定性几何，而 3DGS 是数据驱动的神经原语。

### 4.3 物理交互与 Relighting

传统游戏引擎的核心价值之一是**物理交互**和**动态光照**。3DGS 在这方面正在快速追赶：

- **Relightable 3D Gaussian**（Gao et al., 2024）：给高斯附加法线、BRDF 参数、入射光照和光线追踪可见性，支持实时 relighting 与阴影。
- **GaussianShader**（Jiang et al., 2024）：简化的 shading 函数，处理反射表面。
- **BiGS**（Liu et al., 2025）：扩展 relightable Gaussian 到近场/远场光照和复杂表面。
- **VR-GS**（Jiang et al., 2024）：在 Unity 中实现物理感知的 3DGS 交互，允许用户在 VR 中抓取、移动 splatted 对象。
- **PhysGaussian / PIDG / GaussianFluent**：将 MPM/PBD 物理求解器与 3DGS 耦合，实现弹性体、流体、断裂的物理正确模拟。

---

## 5. 当前瓶颈与可预见的下一步（2026→2028）

### 5.1 六大核心瓶颈（附技术根因分析）

**瓶颈 1：时序一致性（Temporal Coherence）**

根因：当前视频生成模型（扩散或自回归）在帧级别优化，缺乏显式的时序约束。即使在单帧视觉上逼真，长视频中的纹理闪烁（flickering）、物体形变不一致、物理违反（如重力失效）仍然普遍存在。学术评测（Bansal et al., 2024, 2025）表明，当前最优模型在物理常识测试上的准确率仍然低下。

**瓶颈 2：注意力计算的二次复杂度**

根因：DiT-based 视频生成中，spatiotemporal token 上的 self-attention 复杂度为 $O((HW T)^2)$，其中 $H,W$ 为空间分辨率，$T$ 为时间长度。这直接限制了生成分辨率和时长。MAGI-1 等自回归模型通过 causal attention + KV cache 将复杂度降至线性 $O(HW T)$，但 KV cache 的内存需求成为新的瓶颈。

**瓶颈 3：显式表示的存储爆炸**

根因：3DGS 场景通常包含 $10^5$–$10^7$ 个高斯，存储达数百 MB 到数 GB。4DGS（动态场景）进一步将时间维度加入，存储随序列长度线性增长。虽然 LightGaussian（15× 压缩）、Scaffold-GS 等压缩方法有所缓解，但与 Nanite 的虚拟化几何相比仍有数量级差距。

**瓶颈 4：物理正确性的根本缺失**

根因：视频生成模型是数据驱动的，其「物理」来自训练数据的统计规律，而非第一性原理。因此它无法保证守恒定律（能量、动量）、接触约束和材料本构关系的满足。PhysGaussian 等物理耦合方法虽然局部有效，但无法 scale 到开放世界场景。

**瓶颈 5：泛化性与质量的 trade-off**

根因：Per-scene optimization（NeRF/3DGS）质量高但无法泛化；feed-forward 方法（LGM/DUSt3R）泛化但质量有限。扩散生成模型（Sora）通用性最强但缺乏显式 3D 结构。目前没有单一方法能同时满足「高质量 + 泛化 + 实时 + 可编辑」四个要求。

**瓶颈 6：长程一致性与记忆**

根因：自回归视频模型依赖有限的 KV cache 历史上下文。当生成长度超过 cache 容量时，模型「遗忘」早期内容，导致叙事断裂和物体身份漂移。滑动窗口 + frame sinks（Xiao et al., 2023）是当前的工程折中，但非根本解。

### 5.2 可预见的下一步（2026–2028）

基于当前技术趋势的线性外推，以下是六个高概率方向：

1. **Neural-Physical Hybrid Systems**：可微物理引擎（如 DiffTaichi、JAX-MD）与生成模型的深度耦合。不是简单地在后处理阶段加物理约束，而是在生成/优化的每一步都强制执行物理守恒。PIDG、GaussianFluent 是早期信号。

2. **Unified 4D Representation**：一个同时支持（a）从视频重建、（b）从文本生成、（c）实时渲染、（d）物理模拟、（e）用户编辑的单一 4D 表示。4DGS + Spherindrical Harmonics 是最有希望的候选，但还需要支持「生成」而不仅仅是「重建」。

3. **Real-time Generative Rendering**：目标是在 <16ms（60 FPS）内完成从用户输入（文本/草图/控制器信号）到像素输出的全管线。这要求生成模型本身足够快（<100M 参数，单次前向传播），或者采用「生成 + 缓存 + 插值」的混合策略。

4. **Foundation Models for 3D**：类似 LLM 的 3D 基础模型正在形成。DUSt3R（从图像对输出点云 + 位姿）、VGGT（视频几何基础模型）、$\pi^3$ 等工作证明：3D 几何任务可以被统一到一个大规模预训练模型中。未来可能出现「3D-GPT」——一个能理解和生成 3D/4D 内容的基础模型。

5. **World Model as Game Engine**：最激进的预测是，世界模型（world model）将在 5–10 年内部分替代传统游戏引擎的核心功能。不是完全取代（物理精确性和可编辑性仍是传统引擎的优势），而是在「开放世界生成」「NPC 行为」「叙事动态」等方面成为主要技术。NVIDIA Cosmos 明确朝这个方向布局。

6. **Virtualized Gaussian Systems**：类比 Nanite 对三角形的虚拟化，未来可能出现「Virtualized Gaussian Splatting」——根据视角距离动态加载/卸载高斯层级，配合流式传输（如 3DGStream），实现开放世界的大规模 Gaussian 场景。

---

## 6. 对实时图形学从业者的具体建议

### 6.1 技能栈层面

1. **必须掌握 Differentiable Rendering**：理解「渲染梯度如何反向传播」是连接传统图形学与 AI 的数学基础。重点掌握：
   - 体渲染方程的梯度推导（NeRF 的 reparameterization trick）
   - Splatting 的 backward pass（tile-based 排序下的 $\alpha$-blending 梯度）

2. **深入理解 Gaussian Splatting 的渲染管线**：不只是调用开源代码，要理解：
   - 投影变换的推导
   - Covariance $\boldsymbol{\Sigma} = \mathbf{R}\mathbf{S}\mathbf{S}^\top\mathbf{R}^\top$ 的正定约束如何保证
   - Tile-based rasterization 的 CUDA kernel 设计（排序、融合、原子操作）

3. **学习 Diffusion / Flow Matching 基础**：Score matching、probability flow ODE、SDS/VSD 是 text-to-3D 的核心机制。建议从 Song et al. (2021) 的 *Score-Based Generative Modeling* 和 Lipman et al. (2023) 的 *Flow Matching* 开始。

### 6.2 技术判断层面

4. **物理先验不会消失**：当前 hype 倾向于认为「数据驱动将取代物理模拟」。但对需要交互性和确定性的游戏/实时应用而言，PBD、MPM、FEM 等物理求解器仍不可替代。未来的赢家是「物理 + 数据」的混合系统，而非纯数据驱动。

5. **警惕「渲染质量 = 一切」的陷阱**：视频生成模型在视觉上令人惊艳，但缺乏物理正确性、可控性和可编辑性。对于游戏开发，一个「看起来很好但无法交互」的场景没有生产价值。评估技术时，必须同时看：质量、速度、可控性、物理正确性、存储效率。

### 6.3 生态跟踪层面

7. **跟踪开源生态**：
   - `nerfstudio`：NeRF 的统一训练框架
   - `gaussian-splatting`（Kerbl 官方实现）：3DGS 的 reference implementation
   - `gsplat`：更高效的 CUDA rasterizer
   - `threestudio`：text-to-3D 的统一框架（支持 DreamFusion、Magic3D 等）
   - `diff-gaussian-rasterization`：可微 splatting 的核心 CUDA 代码

8. **关注 SIGGRAPH / CVPR / NeurIPS 的相关 track**：特别是「Differentiable Rendering」「Neural Rendering」「3D Generation」「Video Generation」等 session。2024–2025 年的趋势是这些 track 的边界正在模糊——3D 生成论文出现在 CVPR，视频生成论文使用 3D 表示，物理模拟论文耦合神经网络。

### 6.4 职业判断层面

9. **不要急于 All-in 视频生成**：对于实时图形学背景的从业者，你的核心护城河是「理解渲染管线的物理和数学基础」。视频生成领域的「调参工程师」门槛较低且竞争激烈；而「能将神经渲染集成到游戏引擎中并保证 60 FPS 的工程师」极其稀缺。

10. **关注「工具链」而非「单点技术」**：行业真正需要的是从「文本/草图」到「可交互 3D 场景」的完整工具链。能够桥接 AI 生成与传统渲染管线（如将 4DGS 输出转换为 UE5 的 Nanite + Lumen 可消费格式）的人才将在未来 3–5 年极度抢手。

---

## 参考文献（精选里程碑论文）

1. Sitzmann, V., Thies, J., Heide, F., et al. "DeepVoxels: Learning Persistent 3D Feature Embeddings." *CVPR*, 2019.
2. Sitzmann, V., Zollhöfer, M., Wetzstein, G. "Scene Representation Networks: Continuous 3D-Structure-Aware Neural Scene Representations." *NeurIPS*, 2019.
3. Lombardi, S., et al. "Neural Volumes: Learning Dynamic Renderable Volumes from Images." *SIGGRAPH*, 2019.
4. Mildenhall, B., Srinivasan, P.P., Tancik, M., et al. "NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis." *ECCV*, 2020.
5. Tancik, M., et al. "Fourier Features Let Networks Learn High Frequency Functions in Low Dimensional Domains." *NeurIPS*, 2020.
6. Müller, T., Evans, A., Schied, C., Keller, A. "Instant Neural Graphics Primitives with a Multiresolution Hash Encoding." *SIGGRAPH*, 2022.
7. Kerbl, B., Kopanas, G., Leimkühler, T., Drettakis, G. "3D Gaussian Splatting for Real-Time Radiance Field Rendering." *SIGGRAPH*, 2023.
8. Poole, B., Jain, A., Barron, J.T., Mildenhall, B. "DreamFusion: Text-to-3D using 2D Diffusion." *ICLR*, 2022.
9. Lin, C.H., et al. "Magic3D: High-Resolution Text-to-3D Content Creation." *CVPR*, 2023.
10. Liu, R., et al. "Zero-1-to-3: Zero-Shot One Image to 3D Object." *arXiv*, 2023.
11. Luiten, J., et al. "Dynamic 3D Gaussians: Tracking by Persistent Dynamic View Synthesis." *3DV*, 2024.
12. Tang, J., et al. "4D Gaussian Splatting for Real-Time Dynamic Scene Rendering." *arXiv*, 2024.
13. Xie, T., et al. "PhysGaussian: Physics-Integrated 3D Gaussians for Generative Dynamics." *arXiv*, 2024.
14. Brooks, T., et al. "Video Generation Models as World Simulators." *OpenAI Technical Report*, 2024.
15. Peebles, W., Xie, S. "Scalable Diffusion Models with Transformers." *ICCV*, 2023.
16. Huang, B., et al. "2D Gaussian Splatting for Geometrically Accurate Radiance Fields." *SIGGRAPH*, 2024.
17. Jiang, Z., et al. "Geo4D: Leveraging Video Generators for Geometric 4D Scene Reconstruction." *arXiv*, 2025.
18. Gao, Y., et al. "Relightable 3D Gaussian: Real-time Point Cloud Relighting with BRDF Decomposition and Ray Tracing." *arXiv*, 2024.
19. Wang, Z., et al. "ProlificDreamer: High-Fidelity and Diverse Text-to-3D Generation with Variational Score Distillation." *NeurIPS*, 2023.
20. Bansal, H., et al. "Video Generation Models as World Simulators: Physical Commonsense Evaluation." *arXiv*, 2024.

---

> **免责声明**：本报告基于截至 2026-07-03 的公开学术论文、技术博客和开源代码整理，不构成投资建议或技术采纳建议。技术演变速度快，部分预测可能随新论文发布而失效。建议读者以批判性视角阅读，并自行验证关键论断。
