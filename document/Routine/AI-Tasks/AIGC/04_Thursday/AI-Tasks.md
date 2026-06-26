---
tags: [routine/AI-tasks, topic/AIGC, day/Thursday]
aliases: []
---

# Thursday：AI 任务清单 — AI生成内容 工程化与工具链

> **人类目标**：复现代码 + 工具开发
> **AI 任务**：提供脚手架、解释障碍、生成问题。

---

### 任务 1：代码复现

**AI 输出**：diffusers库加载stable-diffusion-v1-5，实现文本到图像生成（不同prompt、不同guidance_scale对比）

### 任务 2：调试

**AI 输出**：CUDA OOM（降低分辨率或使用float16）、提示词理解偏差（负面提示词）、生成结果不一致（seed固定）

### 任务 3：工具

**AI 输出**：批量生成+评估工具：生成N张图 → CLIP分数评估 → 人工筛选Top-K

### 任务 4：性能

**AI 输出**：生成512×512单图时间、batch生成效率、不同采样器（DDPM vs Euler a vs DPM++）速度对比

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
