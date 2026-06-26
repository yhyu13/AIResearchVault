---
tags: [routine/AI-tasks, topic/AI-Optimization, day/Sunday]
aliases: []
---

# Sunday：AI 任务清单 — AI系统优化 项目收尾

> **人类目标**：集成测试 + 复盘
> **AI 任务**：提供脚手架、解释障碍、生成问题。

---

### 任务 1：测试

**AI 输出**：测试：不同序列长度（256/512/2048/4096）的内存占用、并发请求稳定性（1小时压力测试）、API兼容性（OpenAI client）

### 任务 2：文档

**AI 输出**：README：安装(vLLM)、模型下载、启动命令、API使用、性能调参（GPU利用率/max_num_seqs）

### 任务 3：复盘

**AI 输出**：成就：部署vLLM并理解PagedAttention；问题：长序列OOM；改进：调低max_num_seqs或启用swap；下周：Speculative Decoding

---

## 完成检查清单

- [ ] 测试 已执行
- [ ] 文档 已执行
- [ ] 复盘 已执行
- [ ] 笔记已整理

---

*AI 执行时间：约 10 分钟*
*人类执行时间：约 2-3 小时*
