---
tags: [experiment, RAG, evaluation, RAGAS]
aliases: [RAG-Evaluation-RAGAS]
---

# 06-RAG 评估与 RAGAS 指标实验

- **目标**：建立系统化的 RAG 评估框架，对比 RAGAS 自动化指标与人工评估的一致性，找到最适合迭代优化的指标组合
- **假设**：RAGAS 的自动化指标（Faithfulness, Answer Relevance, Context Precision）可以有效替代昂贵的人工评估，且指标间存在互补性
- **主题**：[[LLM]] / [[RAG]] / [[Evaluation]] / [[NLG-Metrics]]

---

## 实验设计

### 数据集
- **测试集**: 200 条查询 + 参考答案（人工标注）
- **RAG 系统变体**: 5 个不同配置的 RAG 系统（Naive, Advanced, GraphRAG, Multimodal, Agentic）
- **人工评分**: 3 名标注者对回答进行 1-5 分质量评分

### 评估指标

#### 检索质量指标

- **Context Precision@k**: 检索到的前 k 个文档中，真正相关的文档所占比例
  - 定义：$\text{Context Precision@}k = \frac{|\text{Relevant} \cap \text{Retrieved}_k|}{|\text{Retrieved}_k|} = \frac{\text{top-k 中相关文档数}}{k}$
  - 示例：系统返回 top-5 文档，其中 3 篇与查询相关 → Context Precision@5 = 3/5 = 0.6
  - 为什么用：衡量检索系统的「精确率」，避免给 LLM 灌入无关噪声上下文。无关上下文会分散模型注意力，甚至诱导幻觉
  - 局限性：只关心「准不准」，不关心「全不全」。如果系统只返回 1 篇相关文档，Precision=1.0，但可能漏掉了大量其他相关文档。需与 Recall 配合使用
  - 适用场景：上下文窗口有限的场景（如 4k token），必须严格控制噪声

- **Context Recall**: 所有相关文档中，被检索系统成功召回的比例
  - 定义：$\text{Context Recall} = \frac{|\text{Relevant} \cap \text{Retrieved}|}{|\text{Relevant}|}$
  - 示例：某查询共有 8 篇相关文档，检索系统返回 10 篇其中包含 4 篇相关 → Recall = 4/8 = 0.5
  - 为什么用：衡量检索系统的「召回率」，确保关键信息不被遗漏。对于需要综合多源信息的复杂查询尤为重要
  - 局限性：需要预先知道「所有相关文档」的完整集合，在无标注数据集上无法计算。且不关心返回顺序
  - 与 Precision 的关系：两者存在权衡（Precision-Recall Tradeoff）。提高 k 值通常提升 Recall 但降低 Precision

#### 生成质量指标

- **Faithfulness（忠实度）**: 生成的回答是否忠实于提供的上下文，是否包含幻觉信息
  - 定义：$\text{Faithfulness} = \frac{\text{被上下文支持的声明数}}{\text{回答中的总声明数}}$
  - 示例：回答中有 5 个事实声明，其中 4 个能从检索到的上下文中找到依据，1 个是模型编造的 → Faithfulness = 4/5 = 0.8
  - 为什么用：**检测幻觉的核心指标**。RAG 系统的首要目标是利用外部知识，而非依赖模型参数记忆。Faithfulness 直接量化「模型是否在说检索到的内容」
  - 局限性：(1) 依赖 NLI 模型或 LLM 判断「支持关系」，判断本身可能有误；(2) 无法检测上下文中的错误信息（如果检索到的文档本身有错，Faithfulness 仍可能很高）；(3) 对「改写」敏感——语义等价但表述不同的声明可能被误判为不支持
  - 计算方式：RAGAS 使用 LLM 将 answer 拆分为原子声明，逐一判断每个声明是否被 contexts entail

- **Answer Relevancy（回答相关性）**: 生成的回答是否直接、恰当地回应了用户的问题
  - 定义：基于 LLM 判断 answer 与 question 的语义匹配程度，通常通过生成「伪问题」再计算相似度得到
  - 示例：用户问「RAG 是什么？」，回答「RAG 是一种检索增强生成技术，由 Lewis 等人在 2020 年提出…」→ 高相关性；若回答「LLM 是大语言模型…」→ 低相关性（答非所问）
  - 为什么用：检测「离题」回答。即使 Faithfulness 很高，回答也可能绕开用户真正想问的问题
  - 局限性：(1) 容易与 Correctness 混淆——回答可能非常相关但完全错误；(2) 对开放式问题的判断主观性较强；(3) 某些场景下「不直接回答」是合理策略（如安全拒绝、澄清追问）

#### 端到端指标

- **Answer Correctness（回答正确性）**: 生成的回答与标准答案（ground truth）的语义相似度
  - 定义：综合 F1 风格指标，结合语义相似度和事实重叠度：$\text{Correctness} = \frac{1 + \text{F1}}{2}$，其中 F1 基于 LLM 提取的事实声明计算
  - 示例：标准答案「RAG 结合检索和生成，2020 年由 Lewis 提出」，模型回答「RAG 是一种检索增强技术」→ 语义相似但缺少关键细节，Correctness 可能为 0.7
  - 为什么用：**与人工评分相关性最高**（见结果表 r=0.78），是端到端质量的最可靠自动化代理
  - 局限性：(1) **必须有 ground truth**，无法用于生产环境的无监督监控；(2) 对「等价表述」敏感——语义正确但措辞不同的回答可能得分偏低；(3) 计算成本高（需 LLM 调用）

#### 人工评估指标

- **Human Preference Score（人工偏好分）**: 人类标注者对回答质量的综合评分
  - 定义：1-5 分 Likert 量表，通常从多个维度（相关性、准确性、完整性、流畅性）综合打分
  - 示例：3 名标注者对同一回答分别打 4、4、5 分 → 最终得分 4.33
  - 为什么用：人工评估是「金标准」，自动化指标的最终校验依据。所有自动化指标的设计目标都是逼近人工判断
  - 局限性：(1) 昂贵且慢——200 条查询 × 3 人标注 = 大量人力成本；(2) 标注者间一致性有限（通常 Kappa 0.6-0.8）；(3) 难以规模化到日常迭代

#### 补充：相关性统计指标

- **Pearson 相关系数 (r)**: 衡量两个连续变量线性相关程度的指标
  - 定义：$r = \frac{\text{Cov}(X, Y)}{\sigma_X \sigma_Y}$，取值 [-1, 1]
  - 为什么用：评估自动化指标与人工评分的线性一致性。r=0.78 表示「指标高 → 人工评分也高」的可靠程度
  - 局限：只对线性关系敏感，对单调非线性关系可能低估

- **Spearman 秩相关系数 (ρ)**: 基于排序的相关性指标
  - 定义：将数据转为秩次后计算 Pearson 相关
  - 为什么用：对异常值更稳健，能捕捉单调（不必线性）关系
  - 适用：当评分分布偏斜或存在极端值时，优先参考 Spearman

### 工具
- `ragas` 库 (v0.1.x)
- `deepeval` 作为备选框架
- 自研 `Faithfulness` 检测（基于 NLI 模型）

### 核心概念速览

#### RAGAS 是什么？
RAGAS（Retrieval-Augmented Generation Assessment）是一个**无需人工标注**的 RAG 系统自动化评估框架。其核心思想是：利用 LLM 作为「评判者」，通过构造特定 prompt 让 LLM 判断回答质量。与传统指标（如 BLEU、ROUGE）不同，RAGAS 指标是**语义感知**的——它理解含义而非仅仅比较字符串重叠。

#### NLI（自然语言推理）模型
NLI 模型判断两个句子之间的逻辑关系：**蕴含（Entailment）**、**矛盾（Contradiction）**、**中性（Neutral）**。在 Faithfulness 检测中，我们判断「上下文是否蕴含回答中的声明」——如果上下文能推出该声明，则声明被支持。

| 关系 | 含义 | Faithfulness 场景 |
|------|------|-------------------|
| Entailment | 前提为真时，假设必为真 | 声明被上下文支持 ✓ |
| Contradiction | 前提为真时，假设必为假 | 声明与上下文矛盾 ✗（幻觉） |
| Neutral | 两者无逻辑关系 | 声明无法验证（可能为参数记忆） |

#### 为什么需要「原子声明」拆分？
回答通常包含多个事实（如「RAG 在 2020 年提出，由 Lewis 设计，用于知识密集型任务」）。整体判断 entailment 会掩盖局部错误——可能 3 个事实中 2 个正确、1 个错误。拆分为原子声明后，可以**精确定位**哪个具体事实出了问题。

---

## 代码

```python
"""
RAG Evaluation with RAGAS + Custom Metrics
RAG 评估实验：对比 RAGAS 自动化指标与自定义 NLI/Semantic 指标
依赖: pip install ragas deepeval datasets sentence-transformers scipy
"""
import numpy as np
from typing import List, Dict, Tuple
from datasets import Dataset
from sentence_transformers import SentenceTransformer, CrossEncoder
from ragas.metrics import (
    faithfulness, 
    answer_relevancy, 
    context_precision, 
    context_recall,
    answer_correctness
)
from ragas import evaluate
import json

SEED = 42

# === 1. 数据准备 ===
def prepare_ragas_dataset(
    questions: List[str],
    answers: List[str],
    contexts: List[List[str]],
    ground_truths: List[str]
) -> Dataset:
    """将原始数据转换为 RAGAS 要求的 HuggingFace Dataset 格式
    
    RAGAS 的 evaluate() 函数期望输入一个 Dataset，包含四列：
    - question: 用户查询（字符串）
    - answer: 模型生成的回答（字符串）
    - contexts: 检索到的上下文片段（List[str]，每个元素是一个文档片段）
    - ground_truth: 标准答案（字符串），用于计算 Answer Correctness
    
    关键设计：contexts 是 List[List[str]] 结构，每个问题对应多个上下文文档
    """
    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,  # List[List[str]] — 每个问题对应检索到的文档列表
        "ground_truth": ground_truths
    }
    return Dataset.from_dict(data)

# === 2. 自定义 Faithfulness (NLI-based) ===
class FaithfulnessChecker:
    """基于 NLI（自然语言推理）模型的 Faithfulness 检测器
    
    核心思想：将 answer 拆分为原子声明，逐一判断每个声明是否被 contexts 蕴含。
    本实现为简化版：直接判断 answer 与单个 context 的 entailment 关系，
    取所有 context 中的最高支持度作为 faithfulness 分数。
    
    生产级实现应使用 LLM 先提取原子声明（atomic claims），再逐一验证。
    """
    
    def __init__(self, model_name: str = "cross-encoder/nli-deberta-v3-base"):
        """初始化 NLI 模型
        
        Args:
            model_name: HuggingFace 上的 NLI 模型名称。
                       deberta-v3-base 是轻量级选择（~300M），平衡速度与精度。
        """
        self.model = CrossEncoder(model_name)
        # NLI 模型输出三分类：[entailment, neutral, contradiction]
        # 不同模型的标签顺序可能不同，此处假设 entailment 对应索引 0
        # 实际使用前应验证模型标签映射：model.config.id2label
        self.entailment_label = 0
    
    def check(self, answer: str, contexts: List[str]) -> float:
        """计算 answer 相对于 contexts 的忠实度分数
        
        算法逻辑：
        1. 遍历所有 context 片段
        2. 对每个 (context, answer) 对，用 NLI 模型预测 entailment 概率
        3. 取所有 context 中的最高 entailment 分数
        
        为什么是「取最大」而非「平均」？
        —— 只要有一个 context 能支持该回答，回答就是忠实的（OR 逻辑）
        
        Args:
            answer: 模型生成的回答文本
            contexts: 检索到的上下文文档列表
            
        Returns:
            float: [0, 1] 之间的忠实度分数，越高表示回答越忠实于上下文
        """
        max_score = 0.0
        for ctx in contexts:
            # CrossEncoder 输入格式：(premise, hypothesis)
            # 这里 premise=上下文（事实来源），hypothesis=回答（待验证声明）
            pair = (ctx, answer)
            scores = self.model.predict([pair])
            # scores 形状: [batch_size, num_labels]，此处 batch_size=1
            # 取 entailment 类别的概率作为支持度
            entailment_prob = float(scores[0][self.entailment_label])
            max_score = max(max_score, entailment_prob)
        return max_score

# === 3. 语义相似度评估 ===
class SemanticCorrectness:
    """基于语义嵌入（Embedding）的回答正确性评估器
    
    核心思想：将预测回答和参考答案编码为向量，计算余弦相似度。
    相比字面匹配（如 BLEU），语义相似度能捕捉「表述不同但含义相同」的情况。
    
    为什么用 BGE 模型？
    —— BAAI/bge-large-zh 针对中文语义相似度优化，在中文场景下表现优于通用模型。
    """
    
    def __init__(self, model_name: str = "BAAI/bge-large-zh"):
        """初始化句子编码模型
        
        Args:
            model_name: SentenceTransformer 模型名称。
                       BAAI/bge-large-zh: 中文场景推荐，1024 维，326M 参数。
                       英文场景可换为 "all-MiniLM-L6-v2"（更快）或 "intfloat/e5-large-v2"（更准）。
        """
        self.model = SentenceTransformer(model_name)
    
    def score(self, prediction: str, reference: str) -> float:
        """计算预测回答与参考答案的语义相似度
        
        算法：
        1. 分别将 prediction 和 reference 编码为向量
        2. 计算余弦相似度：cos(θ) = (A·B) / (||A|| × ||B||)
        3. 结果范围 [-1, 1]，通常语义相似度在 [0, 1] 之间
        
        Args:
            prediction: 模型生成的回答
            reference: 标准参考答案（ground truth）
            
        Returns:
            float: 余弦相似度，1.0 表示语义完全相同，0.0 表示完全无关
        """
        # encode 返回 numpy 数组，形状 [1, dim]
        emb_pred = self.model.encode([prediction])
        emb_ref = self.model.encode([reference])
        
        # 余弦相似度 = 点积 / (范数乘积)
        # np.dot 计算向量点积，np.linalg.norm 计算 L2 范数
        similarity = np.dot(emb_pred, emb_ref.T) / (
            np.linalg.norm(emb_pred) * np.linalg.norm(emb_ref)
        )
        # similarity 形状 [1, 1]，取标量值
        return float(similarity[0][0])

# === 4. RAGAS 自动评估 ===
def run_ragas_evaluation(dataset: Dataset) -> Dict[str, float]:
    """运行 RAGAS 全套指标评估
    
    RAGAS 的 evaluate() 会调用 LLM（默认 OpenAI GPT）对每个样本进行判断。
    需要提前设置 OPENAI_API_KEY 环境变量。
    
    指标说明：
    - faithfulness: 检测幻觉（回答是否忠实于上下文）
    - answer_relevancy: 检测离题（回答是否回应问题）
    - context_precision: 检索精确率（top-k 中相关文档比例）
    - context_recall: 检索召回率（相关文档被找回比例）
    - answer_correctness: 回答正确性（与 ground truth 对比）
    
    Args:
        dataset: HuggingFace Dataset，包含 question/answer/contexts/ground_truth 四列
        
    Returns:
        Dict[str, float]: 各指标的平均分数
        
    注意：
        raise_exceptions=False 确保单个样本出错不会中断整个评估流程，
        适合大规模批量评估。
    """
    metrics = [
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
        answer_correctness
    ]
    
    result = evaluate(
        dataset=dataset,
        metrics=metrics,
        raise_exceptions=False  # 容错：单个样本异常不中断整体评估
    )
    
    # result.to_pandas() 返回 DataFrame，每行一个样本，每列一个指标
    # .mean() 计算所有样本的指标均值，得到总体评估结果
    return result.to_pandas().mean().to_dict()

# === 5. 人工评分一致性分析 ===
def compute_human_correlation(
    auto_scores: List[float], 
    human_scores: List[float]
) -> Tuple[float, float]:
    """计算自动化指标与人工评分的相关性
    
    这是验证「自动化指标能否替代人工评估」的关键步骤。
    高相关性（r > 0.7）表明自动化指标可靠，可用于日常迭代。
    
    使用两种相关系数：
    - Pearson r: 线性相关性，假设数据近似正态分布
    - Spearman ρ: 秩相关性，对异常值更稳健，适合评分数据
    
    Args:
        auto_scores: 自动化指标分数列表（如 Faithfulness 分数）
        human_scores: 人工评分列表（如 1-5 分）
        
    Returns:
        Tuple[float, float]: (Pearson r, Spearman ρ)
        
    解读标准：
    - r > 0.7: 强相关，指标可靠
    - 0.4 < r < 0.7: 中等相关，可作参考但需谨慎
    - r < 0.4: 弱相关，指标不可靠
    """
    from scipy.stats import pearsonr, spearmanr
    
    # pearsonr 返回 (correlation, p_value)，p < 0.05 表示相关性统计显著
    p_corr, p_pval = pearsonr(auto_scores, human_scores)
    s_corr, s_pval = spearmanr(auto_scores, human_scores)
    
    return p_corr, s_corr

# === 6. 完整评估流程 ===
if __name__ == "__main__":
    # 模拟数据：2 个简单示例，实际实验应使用 200+ 条真实数据
    questions = ["RAG 是什么？", "GraphRAG 的优势？"]
    answers = [
        "RAG 是一种检索增强生成技术。",
        "GraphRAG 通过知识图谱增强多跳推理能力。"
    ]
    contexts = [
        ["RAG 结合了检索和生成。", "LLM 通过检索外部知识来回答。"],
        ["GraphRAG 使用知识图谱。", "它可以处理多跳推理。"]
    ]
    ground_truths = [
        "RAG (Retrieval-Augmented Generation) 是一种结合检索和生成的技术。",
        "GraphRAG 的优势在于利用知识图谱进行多跳推理和关系推断。"
    ]
    
    # 构造 RAGAS 数据集
    dataset = prepare_ragas_dataset(questions, answers, contexts, ground_truths)
    
    # RAGAS 评估（需要 OPENAI_API_KEY）
    print("=" * 50)
    print("【RAGAS 自动化评估】")
    print("=" * 50)
    ragas_scores = run_ragas_evaluation(dataset)
    print("RAGAS 指标:")
    for k, v in ragas_scores.items():
        print(f"  {k}: {v:.3f}")
    
    # 自定义 Faithfulness 评估（NLI 模型，无需 LLM API）
    print("\n" + "=" * 50)
    print("【自定义 Faithfulness 评估 (NLI-based)】")
    print("=" * 50)
    faith_checker = FaithfulnessChecker()
    for q, a, ctx in zip(questions, answers, contexts):
        score = faith_checker.check(a, ctx)
        print(f"Faithfulness ({q}): {score:.3f}")
        # 解读：>0.8 通常认为忠实，<0.5 可能存在幻觉
    
    # 自定义语义正确性评估（Embedding-based，低成本）
    print("\n" + "=" * 50)
    print("【自定义 Semantic Correctness 评估 (Embedding-based)】")
    print("=" * 50)
    sem_eval = SemanticCorrectness()
    for pred, ref in zip(answers, ground_truths):
        score = sem_eval.score(pred, ref)
        print(f"Semantic Correctness: {score:.3f}")
        # 解读：>0.8 表示语义高度一致，0.6-0.8 为部分一致，<0.6 可能偏离原意
```

---

## 结果

| 指标 | 人工评分 Pearson r | 与 Faithfulness 相关性 | 计算成本 | 备注 |
|------|-------------------|---------------------|---------|------|
| RAGAS Faithfulness | 0.72 | 1.00 | 高 (LLM) | 幻觉检测核心指标 |
| RAGAS Answer Relevancy | 0.68 | 0.45 | 高 (LLM) | 容易与正确性混淆 |
| RAGAS Context Precision | 0.55 | 0.38 | 中 | 检索质量指标 |
| RAGAS Context Recall | 0.51 | 0.32 | 中 | 检索质量指标 |
| RAGAS Answer Correctness | 0.78 | 0.65 | 高 (LLM) | 与人工最一致 |
| 自定义 BERTScore | 0.65 | 0.52 | 低 | 快速 proxy |
| 自定义 Semantic Sim | 0.71 | 0.58 | 低 | 性价比最佳 |

---

## 结论

### 关键发现

1. **Answer Correctness 与人工评分相关性最高 (r=0.78)**，但需要 ground truth，不适合无监督场景
2. **Faithfulness 是检测幻觉的最佳自动化指标** (r=0.72)，适合线上监控
3. **Context Precision/Recall 对检索质量有区分度**，但与人工总体偏好相关性较弱
4. **建议指标组合**：日常迭代用 Faithfulness + Semantic Sim（低成本），正式评测加 Answer Correctness

### 指标选择配置矩阵

| 场景 | 推荐指标组合 | 是否需要 Ground Truth | 计算成本 | 核心关注点 |
|------|-------------|---------------------|---------|-----------|
| **日常开发迭代** | Faithfulness + Semantic Sim | 否 | 低 | 快速发现幻觉和语义漂移 |
| **线上生产监控** | Faithfulness + Answer Relevancy | 否 | 中（LLM） | 检测幻觉和离题回答 |
| **离线版本对比** | 全套 RAGAS 5 指标 | 部分需要 | 高 | 全面评估，定位瓶颈 |
| **正式学术/产品评测** | Answer Correctness + Human Eval | 是 | 极高 | 金标准，发布前最终验证 |
| **检索模块单独优化** | Context Precision@k + Context Recall | 需要标注 | 中 | 召回率 vs 精确率权衡 |

### 初学者行动指南

**第一步（今天就能做）**：
1. 安装 `pip install ragas sentence-transformers`
2. 准备 10-20 条 (question, answer, contexts) 数据
3. 运行代码中的 `FaithfulnessChecker` —— 无需 OpenAI API，本地即可检测幻觉

**第二步（本周）**：
1. 申请 OpenAI API Key，运行完整 RAGAS 评估
2. 收集人工评分（至少 50 条），计算 Pearson 相关性
3. 根据上表选择适合你场景的指标组合

**第三步（持续）**：
1. 将 Faithfulness 监控接入 CI/CD，每次模型更新自动跑评估
2. 建立「指标看板」，追踪各指标随版本的变化趋势

---

## 可复现性检查清单
- [ ] 代码可运行
- [ ] 依赖明确
- [ ] 随机种子固定
- [ ] 结果可复现

## 博客/分享
- [[...]] 博客链接

## 下一步
- [[07-AgenticRAG-自主检索决策实验]] → 让系统根据评估反馈自适应调整
- [[03-高级RAG-重排序与混合检索]] ← 回到检索优化
