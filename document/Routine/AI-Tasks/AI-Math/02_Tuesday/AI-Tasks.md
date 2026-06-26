---
tags: [routine/AI-tasks, topic/AI-Math, day/Tuesday]
aliases: []
---

# Tuesday：AI 任务清单 — AI数学基础 专项技能突破

> **人类目标**：算法推导 + 数学基础
> **AI 任务**：提供脚手架、解释障碍、生成问题。

---

### 任务 1：算法推导

**AI 输出**：Attention梯度流：$rac{\partial 	ext{Attention}(Q,K,V)}{\partial Q}$的推导（3D张量导数），Scaled Dot-Product的$\sqrt{d_k}$为什么是必要的（Softmax温度与方差），多头Attention的并行分解

### 任务 2：数学补漏

**AI 输出**：张量导数（链式法则）、Softmax的Jacobian矩阵、正交投影（子空间分解）、核方法（Kernel Methods）与Attention的联系（$\exp(QK^T/\sqrt{d})$是RBF核）

### 任务 3：代码骨架

**AI 输出**：纯NumPy实现Attention（无PyTorch）：矩阵乘法 → Scaled → Softmax → 乘V，验证与PyTorch F.scaled_dot_product_attention结果一致

### 任务 4：测试用例

**AI 输出**：验证：$Q=K=V=I$时输出、$d_k$很大时Softmax尖锐化、多头拼接后维度恢复、梯度数值检查（finite differences）

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
