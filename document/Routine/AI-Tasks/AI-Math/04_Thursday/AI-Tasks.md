---
tags: [routine/AI-tasks, topic/AI-Math, day/Thursday]
aliases: []
---

# Thursday：AI 任务清单 — AI数学基础 工程化与工具链

> **人类目标**：复现代码 + 工具开发
> **AI 任务**：提供脚手架、解释障碍、生成问题。

---

### 任务 1：代码复现

**AI 输出**：从头实现Scaled Dot-Product Attention + Multi-Head Attention + Transformer Block（含LayerNorm、FFN、残差连接）

### 任务 2：调试

**AI 输出**：维度不匹配（Q/K/V的head_dim不一致）、Softmax数值溢出（大值导致NaN，用max trick）、LayerNorm位置（Pre-Norm vs Post-Norm）

### 任务 3：工具

**AI 输出**：Attention模式可视化工具：输入句子 → 生成注意力热力图（每个头的注意力权重）

### 任务 4：性能

**AI 输出**：自实现vs PyTorch F.scaled_dot_product_attention（可能调用FlashAttention）的速度对比

---

## 完成检查清单

- [ ] 代码复现 已执行
- [ ] 调试 已执行
- [ ] 工具 已执行
- [ ] 性能 已执行
- [ ] 笔记已整理

---

*AI 执行时间：约 10 分钟*
*人类执行时间：约 2-3 小时*
