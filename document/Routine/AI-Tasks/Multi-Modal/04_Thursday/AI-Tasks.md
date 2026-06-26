---
tags: [routine/AI-tasks, topic/Multi-Modal, day/Thursday]
aliases: []
---

# Thursday：AI 任务清单 — 多模态学习 工程化与工具链

> **人类目标**：复现代码 + 工具开发
> **AI 任务**：提供脚手架、解释障碍、生成问题。

---

### 任务 1：代码复现

**AI 输出**：Hugging Face transformers加载openai/clip-vit-base-patch32，实现零样本分类器

### 任务 2：调试

**AI 输出**：图像预处理（归一化参数clip-specific）、文本tokenization（BPE vs WordPiece）、embedding维度不匹配

### 任务 3：工具

**AI 输出**：零样本分类器类：接收类别列表+图像 → 输出top-k预测，支持批量处理

### 任务 4：性能

**AI 输出**：延迟：单图推理 vs 批量推理；准确率：CIFAR-10/100 vs ImageNet vs 自定义数据集

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
