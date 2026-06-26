---
tags: [routine/AI-tasks, topic/time-series, day/Tuesday]
aliases: []
---

# Tuesday：AI 任务清单 — 时间序列 专项技能突破

> **人类目标**：算法推导 + 数学基础
> **AI 任务**：提供脚手架、解释障碍、生成问题。

---

### 任务 1：算法推导

**AI 输出**：ProbSparse Attention的KL散度推导：$M(q_i,K) = \max_j rac{q_i k_j^T}{\sqrt{d}} - rac{1}{L}\sum_j rac{q_i k_j^T}{\sqrt{d}}$，只保留$M$大的查询（'主导'查询）。自注意力蒸馏：Conv1D(核=3) + MaxPool(步=2)逐层减半序列长度

### 任务 2：数学补漏

**AI 输出**：KL散度（相对熵）、稀疏性度量、1D卷积下采样、生成式解码（用Start token + 占位符一次性解码多步）

### 任务 3：代码骨架

**AI 输出**：PyTorch实现ProbSparse Attention：计算查询重要性M → Top-U选择 → 只计算U个查询的完整注意力 → 其余用均匀分布近似

### 任务 4：测试用例

**AI 输出**：验证：M值计算正确、Top-U选择正确（U=L*log L）、注意力复杂度O(L log L) vs O(L²)的实测对比

---

## 完成检查清单

- [ ] 算法推导 已执行
- [ ] 数学补漏 已执行
- [ ] 代码骨架 已执行
- [ ] 测试用例 已执行
- [ ] 笔记已整理

---

*AI 执行时间：约 10 分钟*
*人类执行时间：约 2-3 小时*
