# 04-性能优化备忘录

> **用途**：训练/推理优化技巧、部署经验、性能基准
> **输入**：实验中的性能瓶颈、社区经验、论文方法
> **输出**：优化方案、基准数据、最佳实践

---

## 优化案例格式

```markdown
---
tags: [optimization, <topic>]
aliases: [<optimization-name>]
---

# 优化场景

- **问题**：...
- **主题**：[[LLM]] / [[RL]] / ...

## 优化前

- 指标：...
- 瓶颈：...

## 优化方法

## 优化后

- 指标：...
- 提升：...

## 经验教训

## 参考
```

---

## 分类索引

### 训练优化
| 技术 | 适用场景 | 效果 | 参考 |
|------|----------|------|------|
| | | | |

### 推理优化
| 技术 | 适用场景 | 效果 | 参考 |
|------|----------|------|------|
| Speculative Decoding（modified rejection sampling） | LLM decode 内存带宽瓶颈；低 QPS 服务、本地单卡 | 低 QPS 1.5–2.8x；期望加速 (1−α^(γ+1))/((1−α)(γc+1))；高 QPS 反减速 1.4–1.8x | [[Speculative-Decoding-蒙特卡洛框架分析]] |
| PagedAttention / Continuous Batching / 量化 / FlashAttention 全景 | 推理引擎选型（llama.cpp → vLLM） | 吞吐 up to 24x；PagedAttention 显存浪费 60-80% → <4% | [[AI-Infra-性能优化全景]] |

### 部署优化
| 技术 | 适用场景 | 效果 | 参考 |
|------|----------|------|------|
| Agent 记忆外部化（Mem0 类：extraction + update + 向量检索） | 长上下文多轮 Agent 的 token/延迟成本 | token ↓>90%（26K→1.7K）、p95 17s→1.44s；代价 LOCOMO J −6pt | [[Agent-Memory-System-性能优化]] |
| Sleep-time 离线整合（LightMem 思路） | 写入/整合路径的在线开销 | 纯在线 token ↓最高 106×/117×；总成本口径仅 ↓38×/20.9×（转移非消除） | [[Agent-Memory-System-性能优化]] |

---

## 常见瓶颈诊断

| 症状 | 可能原因 | 检查方法 | 解决方案 |
|------|----------|----------|----------|
| GPU 利用率低 | CPU 瓶颈、数据加载慢 | nvidia-smi, profiler | DataLoader 优化、缓存 |
| OOM | 模型太大、Batch 太大 | 内存监控 | 梯度累积、模型并行、检查点 |
| 训练慢 | 学习率、数据、模型 | 基准测试 | 混合精度、分布式、编译优化 |
| 推理慢 | 模型大小、框架开销 | 延迟测试 | 量化、KV-Cache、批处理 |

