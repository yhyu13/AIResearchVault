---
tags: [routine/AI-tasks, topic/AI-Training-Technique, day/Tuesday]
aliases: []
---

# Tuesday：AI 任务清单 — AI训练技术 专项技能突破

> **人类目标**：算法推导 + 数学基础
> **AI 任务**：提供脚手架、解释障碍、生成问题。

---

### 任务 1：算法推导

**AI 输出**：LoRA参数更新：$h = W_0x + BAx$，$rac{\partial L}{\partial B}$和$rac{\partial L}{\partial A}$的推导。梯度等价于在原始梯度上投影到低秩子空间。最优秩$r$的权衡：表达能力vs参数量

### 任务 2：数学补漏

**AI 输出**：矩阵低秩分解（SVD）、秩的性质、梯度流在低秩约束下的行为、初始化策略（B=0, A随机高斯）

### 任务 3：代码骨架

**AI 输出**：PyTorch实现LoRA层：LoRALinear(nn.Module) → forward (x @ W_0.T + x @ A.T @ B.T) → 可合并到原始权重

### 任务 4：测试用例

**AI 输出**：验证：LoRA层输出与原始层相同（alpha=0时）、参数量对比（LoRA vs 全量）、梯度正确性检查

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
