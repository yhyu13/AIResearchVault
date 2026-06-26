---
tags: [routine/AI-tasks, topic/AI-Optimization, day/Tuesday]
aliases: []
---

# Tuesday：AI 任务清单 — AI系统优化 专项技能突破

> **人类目标**：算法推导 + 数学基础
> **AI 任务**：提供脚手架、解释障碍、生成问题。

---

### 任务 1：算法推导

**AI 输出**：PagedAttention的内存分配：块大小（如16 tokens/块）、块表（逻辑块→物理块映射）、引用计数（copy-on-write）。内存节省计算：传统 $B×S×H$ vs PagedAttention按需分配

### 任务 2：数学补漏

**AI 输出**：Transformer推理的KV Cache计算（内存=2×batch×seq_len×num_layers×hidden_dim×sizeof(dtype)）、吞吐量=requests/time、时延分布（P50/P99）

### 任务 3：代码骨架

**AI 输出**：简化KV Cache管理器：BlockAllocator类 → allocate_blocks → free_blocks → 物理块池，模拟PagedAttention分配策略

### 任务 4：测试用例

**AI 输出**：模拟：不同请求长度（短/长/混合）的内存利用率、碎片化率、吞吐量对比（静态分配 vs 分页分配）

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
