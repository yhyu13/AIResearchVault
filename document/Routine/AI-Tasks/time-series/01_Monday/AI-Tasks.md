---
tags: [routine/AI-tasks, topic/time-series, day/Monday]
aliases: []
---

# Monday：AI 任务清单 — 时间序列 前沿技术输入

> **人类目标**：精读论文 + 追踪前沿进展
> **AI 任务**：提供脚手架、解释障碍、生成问题。

---

### 任务 1：论文预读

**AI 输出**：Informer论文：动机（长序列预测需要O(n²)注意力，不可扩展）→ ProbSparse Attention（查询稀疏性：只保留'主导'查询）→ 自注意力蒸馏（下采样层减少序列长度）→ 生成式解码（一次性预测多步）

### 任务 2：概念解释

**AI 输出**：ProbSparse直觉：不是所有查询都值得关注。就像开会：重要的发言人（高信息量）才需要回应，其他人可以忽略。通过KL散度度量每个查询的'重要性'，只保留Top-U个

### 任务 3：文献地图

**AI 输出**：ARIMA (经典) → LSTM/GRU (2014) → Transformer (2019时间序列) → LogTrans (2020, Log稀疏注意力) → Informer (2021) → Autoformer (2021, 分解) → FEDformer (2022, 频域) → PatchTST (2023, Patch) → TimeGPT (2023, 基础模型) → Chronos/Moirai (2024, 时序大模型)

---

## 完成检查清单

- [ ] 论文预读 已执行
- [ ] 概念解释 已执行
- [ ] 文献地图 已执行
- [ ] 笔记已整理

---

*AI 执行时间：约 10 分钟*
*人类执行时间：约 2-3 小时*
