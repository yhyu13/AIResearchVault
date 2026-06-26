---
tags: [routine/AI-tasks, topic/NeRF, day/Tuesday]
aliases: []
---

# Tuesday：AI 任务清单 — 神经辐射场 专项技能突破

> **人类目标**：算法推导 + 数学基础
> **AI 任务**：提供脚手架、解释障碍、生成问题。

---

### 任务 1：算法推导

**AI 输出**：体渲染积分：$C(r) = \int T(t)\sigma(r(t))c(r(t),d)dt$，离散化：$\hat{C}(r) = \sum T_i(1-\exp(-\sigma_i\delta_i))c_i$，其中$T_i = \exp(-\sum_{j<i}\sigma_j\delta_j)$。位置编码：$\gamma(p) = [\sin(2^k p), \cos(2^k p)]_{k=0}^{L-1}$

### 任务 2：数学补漏

**AI 输出**：体渲染（Volume Rendering）、光在参与介质中的传播（Beer-Lambert定律）、高频函数的低频表示问题（谱偏置）、傅里叶特征映射

### 任务 3：代码骨架

**AI 输出**：PyTorch实现简化NeRF：位置编码(γ) → MLP(density head + color head) → 体渲染(沿光线采样 → 积分) → 与真实像素对比Loss

### 任务 4：测试用例

**AI 输出**：简单场景（单球体）：验证光线穿过球体时密度峰值、球体后方颜色被遮挡、背景颜色正确

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
