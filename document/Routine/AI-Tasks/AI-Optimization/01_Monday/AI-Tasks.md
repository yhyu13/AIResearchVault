---
tags: [routine/AI-tasks, topic/AI-Optimization, day/Monday]
aliases: []
---

# Monday：AI 任务清单 — AI系统优化 前沿技术输入

> **人类目标**：精读论文 + 追踪前沿进展
> **AI 任务**：提供脚手架、解释障碍、生成问题。

---

### 任务 1：论文预读

**AI 输出**：vLLM论文：KV Cache的内存问题（静态分配导致80%+浪费）→ PagedAttention（类似OS虚拟内存，按块分配）→ 连续批处理（Continuous Batching）→ 实验（吞吐量比TGI高2-4x）

### 任务 2：概念解释

**AI 输出**：PagedAttention直觉：传统LLM推理像酒店给每个客人预留一个楼层（无论用多少房间），PagedAttention像按需分配房间。每个请求按需分配KV Cache块，用完释放，可复用

### 任务 3：文献地图

**AI 输出**：FasterTransformer (NVIDIA) → Orca (Yu 2022, iteration-level scheduling) → vLLM (2023, PagedAttention) → TensorRT-LLM → TGI (HuggingFace) → llama.cpp (边缘) → DeepSpeed Inference

---

## 完成检查清单

- [ ] 论文预读 已执行
- [ ] 概念解释 已执行
- [ ] 文献地图 已执行
- [ ] 笔记已整理

---

*AI 执行时间：约 10 分钟*
*人类执行时间：约 2-3 小时*
