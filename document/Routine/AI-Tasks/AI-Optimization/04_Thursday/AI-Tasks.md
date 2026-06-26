---
tags: [routine/AI-tasks, topic/AI-Optimization, day/Thursday]
aliases: []
---

# Thursday：AI 任务清单 — AI系统优化 工程化与工具链

> **人类目标**：复现代码 + 工具开发
> **AI 任务**：提供脚手架、解释障碍、生成问题。

---

### 任务 1：代码复现

**AI 输出**：安装vLLM，部署LLaMA-2-7B，实现API服务（兼容OpenAI格式），测试不同max_num_seqs配置

### 任务 2：调试

**AI 输出**：GPU OOM（GPU Memory Utilization调优）、CUDA graph编译失败（GPU兼容性）、请求排队（throughput vs latency trade-off）

### 任务 3：工具

**AI 输出**：推理性能基准工具：发送不同长度请求 → 记录吞吐量(requests/sec)、延迟(ms/token)、GPU利用率、内存占用

### 任务 4：性能

**AI 输出**：单GPU vs 多GPU(Tensor Parallelism)、不同量化级别（FP16/AWQ/GPTQ）的速度对比、与HuggingFace naive推理的对比

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
