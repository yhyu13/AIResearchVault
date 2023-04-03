## Paper:4




1. Title: Text and Code Embeddings by Contrastive Pre-Training (对比预训练下的文本和代码嵌入)
                 
2. Authors: Arvind Neelakantan, Tao Xu, Raul Puri, Alec Radford, Jesse Michael Han, Jerry Tworek, Qiming Yuan, Nikolas Tezak, Jong Wook Kim, Chris Hallacy, Johannes Heidecke, Pranav Shyam, Boris Power, Tyna Eloundou Nekoul, Girish Sastry, Gretchen Krueger, David Schnurr, Felipe Petroski Such, Kenny Hsu, Madeleine Thompson, Tabarak Khan, Toki Sherbakov, Joanne Jang, Peter Welinder, Lilian Weng.
                 
3. Affiliation: OpenAI (OpenAI)
                 
4. Keywords: Reinforcement Learning, Natural Language Processing, Contrastive Pre-Training, Text Embeddings, Code Embeddings. (强化学习，自然语言处理，对比预训练，文本嵌入，代码嵌入)

5. Urls: Paper: https://arxiv.org/abs/2201.10005, Github: None
                 
6. Summary:
                    - (1): 本文研究文本和代码嵌入的有效方法。
 
                    - (2): 过去的方法都是为了不同的用例而训练定制模型，数据集，训练目标和模型架构各不相同。本文提出的方法是利用大规模无监督数据的对比预训练，从而生成高质量的文本和代码向量表示。 在线性探测分类中，最佳的无监督模型相比以前的无监督和监督文本嵌入模型分别获得了4％和1.8％的相对改进。相对于以前在MSMARCO，Natural Questions和TriviaQA基准上最好的无监督方法，本文方法在大规模语义搜索中达到了23.4％，14.7％和10.6％的相对改进。对于代码嵌入，本文方法相对于之前最好的工作在代码搜索方面获得了20.8％的相对改进。
 
                    - (3): 本文方法是利用大规模的对比预训练无监督数据，通过学习文本和代码向量表示生成高质量向量。 
 
                    - (4):本文方法在文本分类和语义搜索任务方面获得了很好的性能表现，该表现支持本文方法的目标。
7. Methods: 

- (1): 本文利用对比预训练的方法，对大量文本和代码无监督数据进行训练，生成高质量的文本和代码向量表示，以解决过去方法在不同用例下需要训练不同模型、数据集、训练目标和模型架构等问题。

- (2): 对于训练数据，采用成对的样本集合{(xi, yi)}Ni=1作为输入，其中(xi, yi)表示一对正样本，即xi和yi在语义或上下文方面具有相似性或相关性。

- (3): 对于模型，本文采用Transformer（Vaswani et al., 2017）编码器E来分别处理训练对(x, y)。编码器将输入映射到密集的向量表示或嵌入（图2）。在输入序列的开头和结尾处插入两个特殊标记分隔符[SOS]和[EOS]。对应于特殊标记[EOS]的最后一层的隐藏状态被视为输入序列的嵌入。

- (4): 在线性探测分类中，本文方法相比以往的无监督和监督文本嵌入模型分别获得了4％和1.8％的相对改进，在大规模语义搜索中分别相对于之前最好的无监督方法在MSMARCO、Natural Questions和TriviaQA基准上获得了23.4％，14.7％和10.6％的相对改进。对于代码嵌入，本文方法相对于之前最好的工作在代码搜索方面获得了20.8％的相对改进。





8. Conclusion:

- (1): 本文提出的对比预训练下的文本和代码嵌入方法在强化学习和自然语言处理领域具有重要意义，能够生成高质量的向量表示，提升线性探测分类、语义搜索和代码搜索任务的性能。

- (2): 创新点：本文提出了利用对比预训练方法生成文本和代码向量表示的方法；性能：本文方法在文本分类、语义搜索和代码搜索任务方面获得了较大的相对改进，但在句子相似度任务方面表现有限；工作量：本文利用大量的无监督数据进行训练，需要较大的计算资源和时间。




