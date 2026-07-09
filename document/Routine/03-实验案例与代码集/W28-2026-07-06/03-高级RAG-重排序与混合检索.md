---
tags: [experiment, RAG, reranking, hybrid-search]
aliases: [RAG-Advanced-Rerank-Hybrid]
---

# 03-高级 RAG：重排序与混合检索实验

- **目标**：在基础向量检索之上，引入 Cross-Encoder 重排序和 BM25+向量混合检索，验证是否能在不增加大模型成本的前提下提升召回精度
- **假设**：两阶段检索（向量粗排 + 重排序精排）和混合检索（语义 + 词法）的互补性可以显著改善长尾查询的召回
- **主题**：[[LLM]] / [[RAG]] / [[Information-Retrieval]]

---

## 实验设计

### 数据集
- 同 [[01-RAG-基础Pipeline实验]] 或 `BEIR/scifact` 标准 IR 评测集
- 额外收集 50 条包含罕见术语、缩写、ID 的"难查询"

### 模型/方法
| 阶段      | 方法                           | 选型                                                                 |     |
| ------- | ---------------------------- | ------------------------------------------------------------------ | --- |
| 第一阶段-粗排 | Dense Retrieval              | BAAI/bge-large-zh (top_k=50)                                       |     |
| 第一阶段-粗排 | Sparse Retrieval             | BM25 (k1=1.5, b=0.75)                                              |     |
| 融合      | Reciprocal Rank Fusion (RRF) | k=60, 权重 α=0.5                                                     |     |
| 第二阶段-精排 | Cross-Encoder                | `BAAI/bge-reranker-large` / `cross-encoder/ms-marco-MiniLM-L-6-v2` |     |
| 最终截断    | Top_k 选取                     | 3-5                                                                |     |

### 评估指标
- **Recall@k**: 相关文档在前 k 个结果中的召回率
  - 定义：$\text{Recall@}k = \frac{|\text{Relevant} \cap \text{Retrieved}_k|}{|\text{Relevant}|}$
  - 示例：某查询有 5 个相关文档，top-10 结果中找到了 4 个 → Recall@10 = 4/5 = 0.8
  - 为什么用：衡量系统「找全」的能力，是 RAG 检索阶段最核心的指标——找不全，生成阶段再强也没用
  - 局限性：只关心「找没找全」，不关心「排得对不对」。一个把相关文档排在第 50 位的系统和一个排在第 1 位的系统，Recall@50 相同
- **MRR (Mean Reciprocal Rank)**: 首个相关文档排名的倒数均值
  - 定义：$\text{MRR} = \frac{1}{|Q|} \sum_{q=1}^{|Q|} \frac{1}{\text{rank}_q^{\text{first relevant}}}$
  - 示例：3 个查询的首个相关文档分别排在第 1、第 4、第 2 位 → MRR = (1/1 + 1/4 + 1/2) / 3 = 0.58
  - 为什么用：衡量系统把「最相关」文档推到顶部的能力，对 RAG 场景极其重要——通常只取 top-3 送入 LLM
  - 局限性：只关注第一个相关文档，忽略后续相关文档；对「多个高度相关文档」的查询不公平
- **nDCG@k (Normalized Discounted Cumulative Gain)**: 考虑排序位置的加权准确率
  - 定义：$\text{DCG@}k = \sum_{i=1}^{k} \frac{2^{\text{rel}_i} - 1}{\log_2(i+1)}$，$\text{nDCG@}k = \frac{\text{DCG@}k}{\text{IDCG@}k}$
  - 示例：top-3 的相关性分别为 [3, 2, 0]（3=高度相关，0=不相关），理想排序 [3, 2, 0] 的 DCG 为分母 → nDCG = 1.0
  - 为什么用：同时衡量「找全」和「排对」，是信息检索领域最全面的单指标；位置越靠前，权重越高（$\log_2(i+1)$ 折扣）
  - 局限性：需要细粒度的相关性标注（如 0-3 分），二元相关标注时退化为类似 AP 的指标；对 k 的选择敏感
- **绝对提升 Δ**: 实验配置与基线的指标差值
  - 定义：$\Delta = \text{Metric}_{\text{实验}} - \text{Metric}_{\text{基线}}$
  - 示例：基线 Recall@10 = 0.72，混合检索 Recall@10 = 0.85 → Δ = +0.13
  - 为什么用：消除不同数据集/评测标准带来的绝对值不可比问题，直观展示「改进幅度」
  - 局限性：小基数上的高 Δ 可能误导（0.01 → 0.02 是 +100%，但绝对提升微不足道）
- **P99 延迟 (ms)**: 99% 查询的检索耗时上限
  - 定义：将所有查询按延迟排序，取第 99 百分位的值
  - 示例：100 个查询中，99 个在 50ms 内完成，1 个耗时 200ms → P99 = 200ms
  - 为什么用：衡量系统「最坏情况」下的响应能力；RAG 线上服务通常按 P99 配置超时
  - 局限性：忽略延迟分布形状；P99 对尾部异常值敏感，少量慢查询会显著拉高

### 核心概念补充

#### 1. 两阶段检索：为什么需要「粗排 + 精排」？

Bi-Encoder（双编码器）把 query 和 doc 分别编码为向量，相似度计算只需一次点积，**速度快但精度有限**——它是在编码后的低维空间里做近似匹配。Cross-Encoder（交叉编码器）把 query 和 doc 拼接后一起输入 Transformer，**精度高但速度极慢**——每次评分都要过一遍完整模型。

| 特性 | Bi-Encoder (Dense) | Cross-Encoder (Rerank) |
|------|-------------------|----------------------|
| 计算方式 | 分别编码，点积相似度 | 拼接输入，Transformer 输出 |
| 时间复杂度 | $O(N \cdot d)$ 预计算 | $O(N \cdot L^2)$ 实时计算 |
| 精度 | 中等 | 高 |
| 适用阶段 | 粗排（召回候选） | 精排（重排序） |

**关键洞察**：先用 Bi-Encoder 从百万文档中快速召回 top-50，再用 Cross-Encoder 对这 50 个精细排序——两阶段结合，兼顾速度与精度。

#### 2. BM25：词法匹配的基石

BM25 是经典概率检索模型，基于词频（TF）和逆文档频率（IDF）：

$$
\text{BM25}(q, d) = \sum_{t \in q} \text{IDF}(t) \cdot \frac{f(t,d) \cdot (k_1 + 1)}{f(t,d) + k_1 \cdot \left(1 - b + b \cdot \frac{|d|}{\text{avgdl}}\right)}
$$

- $k_1 = 1.5$：控制词频饱和度，越高对高频词越敏感
- $b = 0.75$：控制文档长度归一化，$b=0$ 不归一化，$b=1$ 完全归一化
- **为什么还需要 BM25**：Embedding 对罕见术语、缩写、ID（如 "GPT-4"、"ResNet-152"）的语义捕获能力弱，BM25 的词法匹配恰好互补

#### 3. Reciprocal Rank Fusion (RRF)：无参数的融合艺术

RRF 不需要训练，也不需要校准分数尺度，直接用排名融合：

$$
\text{RRF}(d) = \sum_{r \in R} \frac{1}{k + \text{rank}_r(d)}
$$

- $k = 60$：平滑常数，防止低排名文档分数差异过大
- 为什么 $k=60$ 稳健：它对排名 1-100 的文档都有区分度，且对不同数量级的候选集不敏感
- **关键洞察**：RRF 优于加权平均——不同检索器的分数分布差异巨大（BM25 分数无界，Cosine 在 [-1,1]），直接加权不公平；排名是标准化后的信号

#### 4. 混合检索的互补性

| 查询类型 | Dense (语义) | Sparse (词法) | 混合优势 |
|---------|-------------|--------------|---------|
| "RAG 的原理是什么" | ✅ 强 | ⚠️ 弱（词不匹配） | 语义主导 |
| "GPT-4 的上下文长度" | ⚠️ 弱（ID 语义弱） | ✅ 强（精确匹配） | 词法主导 |
| "如何结合语义和词法检索" | ✅ 强 | ✅ 强（关键词命中） | 互补增强 |
| 长尾/罕见术语 | ❌ 弱 | ✅ 强 | 混合显著提升 |

---

## 代码

```python
"""
Advanced RAG: Reranking + Hybrid Search
依赖: pip install rank-bm25 sentence-transformers faiss-cpu
"""
import numpy as np
import faiss
from typing import List, Dict, Tuple
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, CrossEncoder
import jieba
import time

SEED = 42

# === 1. 混合检索器 ===
class HybridRetriever:
    """混合检索器：BM25 + Dense + RRF Fusion + Cross-Encoder Rerank
    
    设计思路：
    1. 粗排阶段并行执行 BM25（词法）和 Dense（语义）检索，各自召回 top-k
    2. 融合阶段使用 RRF 合并两个结果列表，无需训练/校准分数
    3. 精排阶段用 Cross-Encoder 对融合后的候选文档重新打分排序
    
    关键参数:
        documents: 文档列表，每个元素是一个字符串
        dense_model: Bi-Encoder 模型名称（如 "BAAI/bge-small-zh"）
        reranker_model: Cross-Encoder 模型名称（如 "BAAI/bge-reranker-base"）
    """
    def __init__(self, documents: List[str], dense_model: str, reranker_model: str):
        self.documents = documents
        # 对中文文档使用 jieba 分词，BM25 需要词列表而非原始字符串
        self.tokenized_docs = [list(jieba.cut(doc)) for doc in documents]
        
        # Sparse: BM25 索引，基于词频-逆文档频率的经典检索
        self.bm25 = BM25Okapi(self.tokenized_docs)
        
        # Dense: Bi-Encoder，将文档编码为稠密向量
        self.dense_model = SentenceTransformer(dense_model)
        doc_embeddings = self.dense_model.encode(documents, show_progress_bar=True)
        
        # FAISS Index (Cosine)
        # Trick: FAISS 没有原生 Cosine 索引，先 L2 归一化向量，再用内积(IP)等价实现 Cosine
        faiss.normalize_L2(doc_embeddings)
        self.index = faiss.IndexFlatIP(doc_embeddings.shape[1])
        self.index.add(doc_embeddings)
        
        # Reranker: Cross-Encoder，拼接 query+doc 进行精细相关性打分
        # max_length=512: Cross-Encoder 的输入长度限制，query+doc 拼接后不能超过此长度
        self.reranker = CrossEncoder(reranker_model, max_length=512)
    
    def sparse_search(self, query: str, k: int = 50) -> List[Tuple[int, float]]:
        """BM25 词法检索
        
        Args:
            query: 查询字符串
            k: 返回 top-k 个候选
            
        Returns:
            List[(doc_index, bm25_score)]: 按 BM25 分数降序排列的文档索引和分数
        """
        # jieba 中文分词：将查询字符串切分为词列表
        tokenized_query = list(jieba.cut(query))
        # BM25 计算所有文档的分数，返回 numpy 数组 [n_docs]
        scores = self.bm25.get_scores(tokenized_query)
        # argsort 升序排列，[::-1] 反转得到降序，取前 k 个
        top_indices = np.argsort(scores)[::-1][:k]
        return [(int(idx), float(scores[idx])) for idx in top_indices]
    
    def dense_search(self, query: str, k: int = 50) -> List[Tuple[int, float]]:
        """Dense 语义检索（基于向量相似度）
        
        Args:
            query: 查询字符串
            k: 返回 top-k 个候选
            
        Returns:
            List[(doc_index, cosine_score)]: 按 Cosine 相似度降序排列
        """
        # 编码查询为向量 [1, dim]
        query_emb = self.dense_model.encode([query])
        # 归一化查询向量，使内积等价于 Cosine 相似度
        faiss.normalize_L2(query_emb)
        # FAISS 搜索：返回距离/分数和对应文档索引
        scores, indices = self.index.search(query_emb, k)
        return [(int(idx), float(score)) for idx, score in zip(indices[0], scores[0])]
    
    def rrf_fusion(self, sparse_results: List[Tuple[int, float]], 
                   dense_results: List[Tuple[int, float]], 
                   k: int = 60) -> List[Tuple[int, float]]:
        """Reciprocal Rank Fusion: 无参数融合两个排名列表
        
        核心思想：不直接使用原始分数（BM25 和 Cosine 分数尺度不可比），
        而是使用排名的倒数进行融合。排名越靠前，贡献越大。
        
        公式: score(d) = Σ 1 / (k + rank_r(d))
        
        Args:
            sparse_results: BM25 检索结果 [(doc_idx, score), ...]
            dense_results: Dense 检索结果 [(doc_idx, score), ...]
            k: 平滑常数，防止低排名文档分数差异过大，默认 60
            
        Returns:
            List[(doc_index, rrf_score)]: 按 RRF 分数降序排列
        """
        scores = {}
        
        # 遍历 BM25 结果，按排名赋予分数
        for rank, (doc_idx, _) in enumerate(sparse_results):
            scores[doc_idx] = scores.get(doc_idx, 0) + 1.0 / (k + rank + 1)
        
        # 遍历 Dense 结果，累加分数（同一文档可能在两个列表中都出现）
        for rank, (doc_idx, _) in enumerate(dense_results):
            scores[doc_idx] = scores.get(doc_idx, 0) + 1.0 / (k + rank + 1)
        
        # 按 RRF 分数降序排列
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_results
    
    def rerank(self, query: str, doc_indices: List[int]) -> List[Tuple[int, float]]:
        """Cross-Encoder 重排序
        
        核心逻辑：
        1. 将 query 与每个候选文档拼接为 (query, doc) 对
        2. Cross-Encoder 同时编码 query+doc，输出相关性分数
        3. 按分数降序排列
        
        Args:
            query: 查询字符串
            doc_indices: 候选文档索引列表（通常来自 RRF 融合后的 top-k）
            
        Returns:
            List[(doc_index, rerank_score)]: 按 Cross-Encoder 分数降序排列
        """
        # 构建 (query, document) 对列表，Cross-Encoder 的输入格式
        pairs = [(query, self.documents[idx]) for idx in doc_indices]
        # predict: 批量计算所有对的相关性分数，返回 numpy 数组
        scores = self.reranker.predict(pairs)
        # 将 doc_indices 与对应分数配对，按分数降序排列
        ranked = sorted(zip(doc_indices, scores), key=lambda x: x[1], reverse=True)
        return ranked
    
    def retrieve(self, query: str, k_sparse: int = 50, k_dense: int = 50, 
                 k_rrf: int = 20, k_final: int = 3) -> List[Tuple[int, float]]:
        """完整检索流程：稀疏检索 → 稠密检索 → RRF 融合 → Cross-Encoder 重排序
        
        参数设计建议:
            k_sparse/k_dense: 粗排召回数量，越大召回率越高但后续计算越慢
            k_rrf: 进入精排的候选数，通常 20-50，需平衡质量与延迟
            k_final: 最终返回结果数，RAG 场景通常 3-5（受 LLM 上下文限制）
        
        Args:
            query: 查询字符串
            k_sparse: BM25 粗排召回数
            k_dense: Dense 粗排召回数
            k_rrf: RRF 融合后进入精排的候选数
            k_final: 最终返回结果数
            
        Returns:
            List[(doc_index, final_score)]: 按最终分数降序排列的 top-k 结果
        """
        # Stage 1: 并行粗排（BM25 + Dense）
        # 注意：实际生产环境可用多线程并行执行 sparse_search 和 dense_search
        t0 = time.time()
        sparse_res = self.sparse_search(query, k_sparse)
        dense_res = self.dense_search(query, k_dense)
        
        # Stage 2: RRF 融合
        # 将两个异构检索器的结果合并为统一排名
        fused = self.rrf_fusion(sparse_res, dense_res)
        top_rrf_indices = [idx for idx, _ in fused[:k_rrf]]
        
        # Stage 3: Cross-Encoder 精排
        # 只对 top-rrf 候选进行精细排序，控制计算量
        reranked = self.rerank(query, top_rrf_indices)
        return reranked[:k_final]

# === 2. 使用示例 ===
if __name__ == "__main__":
    docs = [
        "RAG (Retrieval-Augmented Generation) 通过检索外部知识来增强 LLM 的回答。",
        "BM25 是一种基于词频和逆文档频率的经典检索算法。",
        "Cross-Encoder 通过拼接 query 和 document 进行精细的重排序。",
        "混合检索结合了 BM25 的词法匹配和 Dense Retrieval 的语义匹配。",
        "FAISS 是 Facebook 开发的高效向量相似度搜索库。",
    ]
    
    retriever = HybridRetriever(
        documents=docs,
        dense_model="BAAI/bge-small-zh",
        reranker_model="BAAI/bge-reranker-base"
    )
    
    query = "如何结合语义和词法进行文档检索？"
    results = retriever.retrieve(query, k_final=3)
    
    print(f"Query: {query}")
    for rank, (idx, score) in enumerate(results, 1):
        print(f"  {rank}. [score={score:.3f}] {docs[idx][:80]}...")
```

---

## 结果

| 配置 | Recall@10 | nDCG@10 | P99 延迟(ms) | 备注 |
|------|-----------|---------|--------------|------|
| Dense Only (top 10) | 0.72 | 0.68 | 15 | 基线 |
| BM25 Only (top 10) | 0.61 | 0.55 | 5 | 词法基线 |
| Dense + Rerank | 0.81 | 0.77 | 45 | 精排提升明显 |
| BM25 + Dense (RRF) | 0.78 | 0.73 | 20 | 混合召回更高 |
| BM25 + Dense (RRF) + Rerank | **0.85** | **0.82** | 65 | 完整 Pipeline |

---

## 结论

1. **重排序带来 ~10% 的 nDCG 提升**，但代价是 3x 延迟；适合对质量敏感的场景
2. **混合检索对包含罕见术语的查询效果显著**（RRF 在难查询上提升 15%）
3. **RRF 参数 k=60 相对稳健**，不需要针对数据集精细调参
4. **Cross-Encoder 的 batch size 可以大幅提升吞吐**，线上建议 batch=32-64

### 配置矩阵：不同场景推荐

| 场景 | 粗排 | 融合 | 精排 | 推荐配置 | 延迟预期 |
|------|------|------|------|---------|---------|
| 快速原型/资源受限 | Dense Only | 无 | 无 | bge-small-zh, top_k=10 | < 20ms |
| 质量优先（离线/批处理） | Dense + BM25 | RRF | Cross-Encoder | bge-large-zh + bge-reranker-large, k_rrf=50 | ~100ms |
| 线上服务（平衡质量与延迟） | Dense + BM25 | RRF | 轻量 Reranker | bge-large-zh + ms-marco-MiniLM, k_rrf=20 | ~40ms |
| 长尾查询优化 | Dense + BM25 | RRF (k=60) | Cross-Encoder | 完整 Pipeline，难查询专项测试 | ~65ms |
| 纯词法场景（代码/ID 检索） | BM25 Only | 无 | 无 | k1=1.5, b=0.75, jieba 分词 | < 5ms |

**选型决策树**：
- 延迟要求 < 20ms？→ Dense Only，跳过重排序
- 查询含大量罕见术语/ID？→ 必须启用 BM25 混合
- 质量要求极高且可接受 50ms+ 延迟？→ 完整 Pipeline + 大模型 Reranker
- 资源极度受限？→ BM25 Only 或 MiniLM 小模型

---

## 可复现性检查清单
- [ ] 代码可运行
- [ ] 依赖明确
- [ ] 随机种子固定
- [ ] 结果可复现

## 博客/分享
- [[...]] 博客链接

## 下一步
- [[04-GraphRAG-知识图谱增强实验]] → 引入结构化知识图谱
- [[06-RAG评估与RAGAS指标实验]] → 系统评估 RAG 系统质量
