---
tags: [routine/AI-tasks, topic/AI-Training-Technique, day/Thursday]
aliases: []
---

# Thursday：AI 任务清单 — AI训练技术 工程化与工具链

> **人类目标**：复现代码 + 工具开发
> **AI 任务**：提供脚手架、解释障碍、生成问题。

---

### 任务 1：代码复现

**AI 输出**：PEFT库实现LoRA微调：加载预训练模型 → 配置LoraConfig → 训练（只优化LoRA参数）→ 保存/合并权重

### 任务 2：调试

**AI 输出**：LoRA权重未加载（target_modules正则匹配错误）、显存仍高（未使用梯度检查点）、合并后推理慢（未调用merge_and_unload）

### 任务 3：工具

**AI 输出**：LoRA参数统计工具：计算可训练参数量、对比全量微调内存、自动选择target_modules（q_proj/v_proj/k_proj/o_proj）

### 任务 4：性能

**AI 输出**：微调时间对比（LoRA vs 全量）、显存占用（GPU内存）、最终效果（LoRA r=8 vs r=64 vs 全量）

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
