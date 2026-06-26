---
tags: [routine/AI-tasks, topic/AI-Theory, day/Thursday]
aliases: []
---

# Thursday：AI 任务清单 — AI基础理论 工程化与工具链

> **人类目标**：复现代码 + 工具开发
> **AI 任务**：提供脚手架、解释障碍、生成问题。

---

### 任务 1：代码复现

**AI 输出**：使用公开训练曲线数据（如GPT-3论文Figure 3、LLaMA训练日志），拟合Scaling Law参数

### 任务 2：调试

**AI 输出**：拟合数据点不足（需要至少3-4个不同规模的数据）、对数空间异常值、不同架构（Dense vs MoE）的Scaling差异

### 任务 3：工具

**AI 输出**：Scaling Law可视化工具：绘制Loss vs Params、Loss vs FLOPs、IsoFLOP曲线，支持预测目标Loss所需配置

### 任务 4：性能

**AI 输出**：拟合耗时（<1秒）、预测精度（与真实Loss的误差）、外推稳定性（10x外推是否准确）

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
