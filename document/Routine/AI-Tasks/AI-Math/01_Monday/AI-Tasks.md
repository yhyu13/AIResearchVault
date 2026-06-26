---
tags: [routine/AI-tasks, topic/AI-Math, day/Monday]
aliases: []
---

# Monday：AI 任务清单 — AI数学基础 前沿技术输入

> **人类目标**：精读论文 + 追踪前沿进展
> **AI 任务**：提供脚手架、解释障碍、生成问题。

---

### 任务 1：论文预读

**AI 输出**：Transformer论文数学部分：Self-Attention = 软选择（Softmax+QK^T+V），Scaled Dot-Product（除以$\sqrt{d_k}$防止梯度消失），Multi-Head = 子空间并行

### 任务 2：概念解释

**AI 输出**：Attention直觉：$Q$是'查询'（我想找什么），$K$是'键'（你有什么），$V$是'值'（内容是什么）。$QK^T$是相似度矩阵，Softmax是归一化，乘$V$是加权求和。就像图书馆：查询主题→匹配书名→取出内容

### 任务 3：文献地图

**AI 输出**：RNN Encoder-Decoder (2014) → Attention (Bahdanau 2015) → Self-Attention (Cheng 2016) → Transformer (2017) → Linformer (2020, O(n)) → Performer (2021, FAVOR+) → FlashAttention (2022, IO-aware)

---

## 完成检查清单

- [ ] 论文预读 已执行
- [ ] 概念解释 已执行
- [ ] 文献地图 已执行
- [ ] 笔记已整理

---

*AI 执行时间：约 10 分钟*
*人类执行时间：约 2-3 小时*
