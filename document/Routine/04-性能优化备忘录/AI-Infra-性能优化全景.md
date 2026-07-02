---
tags: [optimization, AI-Inference, LLM, vLLM, llama.cpp, quantization, FlashAttention, PagedAttention, speculative-decoding]
aliases: [AI-Infra-Performance-Evolution]
---

# AI-Infra 性能优化备忘录：从 llama.cpp 到 vLLM 的技术迭代全景

> **研究日期**: 2026-07-02  
> **聚焦项目**: llama.cpp, vLLM, FlashAttention, TensorRT-LLM, SGLang  
> **核心问题**: 现代 AI 推理引擎如何通过技术迭代实现极致性能？

---

## 优化场景

- **问题**: LLM 推理的瓶颈已从**计算 (FLOPS)** 转移到**内存带宽 (HBM BW)** 与**调度开销**。如何在单机消费级硬件到数据中心 GPU 集群的全谱系上压榨极限性能？
- **主题**: [[LLM]] / [[Inference]] / [[System Optimization]]

## 优化前：原始的瓶颈画像

| 阶段 | 指标 | 瓶颈 | 表现 |
|------|------|------|------|
| **Prompt Processing (Prefill)** | 计算密集 | 无并行 attention, 无内存复用 | 长 prompt 等待数秒至数分钟 |
| **Token Generation (Decode)** | 内存带宽密集 | 每次加载全量权重 + KV Cache | 大模型 decode 速度 < 5 t/s |
| **Serving 多并发** | 吞吐极低 | 静态 batching, KV Cache 碎片 | GPU 利用率 30-40%, 显存浪费 60-80% |
| **部署门槛** | 显存/内存不足 | FP16 全精度 | 7B 模型需 13GB+，70B 模型需 140GB+ |

---

## 优化方法：技术迭代全景

### 一、核心范式转移：从「计算优先」到「内存-调度优先」

> ** Roofline Insight**: 对于 Transformer decode， achievable throughput = `MemBW / (model_size_bytes + KV_cache_bytes_per_token)`。因此，**减少内存占用**和**提升内存复用率**比增加 FLOPS 更有效。

这一定律驱动了过去三年的所有重大优化。

---

### 二、llama.cpp 的优化哲学：「先跑起来，再跑得快」

llama.cpp 代表了**消费级/边缘端**的优化路径，核心思想是：先让大模型在 CPU/笔记本上运行，再逐步压榨每一层硬件。

#### 2.1 量化革命：从 4-bit 到 Importance-Aware

| 阶段 | 技术 | 时间 | 效果 | 关键洞察 |
|------|------|------|------|----------|
| **原始** | Q4_0 / Q5_0 / Q8_0 | 2023-03 | 7B 模型从 13GB → 3.5-6.7GB | 让 LLaMA-7B 在 M1 MacBook 上跑到 ~15 t/s，引爆本地 LLM 运动 |
| **K-Quants** | Q2_K - Q6_K (super-block) | 2023-06 | Q4_K_M: ~3.8GB, +0.053 PPL | 社区标准。将 metadata 开销压缩到 super-block，省下的位给 weights |
| **IQ-Quants** | IQ2_XXS ... IQ4_NL | 2024 | 2.06-4.50 bpw, 非线性码本 | **Importance-aware bit allocation**：给敏感权重更多精度，实现 sub-3-bit 可用 |
| **imatrix** | 重要性矩阵校准 | 2024 | Q2_K_S 从 +9.06 PPL 降到可用水平 | 通过校准数据识别敏感 tensor，指导量化参数。让 2-bit 成为现实 |
| **GGUF** | 自包含二进制格式 | 2023-08 | 支持 mmap（瞬载）、无外部 tokenizer | 格式稳定性 + 内存映射使模型大于 RAM 也能加载 |

**关键结论**：llama.cpp 将量化视为**一等公民**，而非后处理插件。`quantize` 是核心二进制，新量化方案立即在所有后端（Metal/CUDA/Vulkan/SYCL）落地。

#### 2.2 后端版图：从 CPU SIMD 到全平台 GPU

| 后端 | 引入时间 | 目标硬件 | 关键优化 |
|------|----------|----------|----------|
| **ARM NEON** | 2023-03 | Apple Silicon / ARM64 | 本地运行的基石 |
| **AVX/AVX2/AVX512** | 2023-03+ | x86 CPU | 量化反量化 2-8x 加速 |
| **Metal** | 2023-03 | Apple GPU | 2-3x 于 CPU 的 token generation |
| **CUDA / cuBLAS** | 2023-04 | NVIDIA GPU | 自定义量化 matmul kernel (MMVQ/DMMV)，`-ngl` 分层卸载 |
| **Vulkan** | 2024-01 | AMD/Intel GPU | Linux/Windows 跨平台，RDNA3+ coopmat |
| **SYCL** | 2024-01 | Intel Arc / Data Center GPU | 2025 年 Q4_0 优化 +21-87%，FlashAttention 2025-03 加入 |
| **HIP/ROCm** | 2023 | AMD GPU | Linux 原生 AMD 支持 |

**架构转折点**：2023 年底 `ggml-backend` 抽象层重构，将计算图与硬件后端解耦，实现**跨 CPU/GPU/多设备的自动调度**。

#### 2.3 内存管理：KV Cache 的每一 byte 都要省

| 技术 | 时间 | 效果 |
|------|------|------|
| **KV Cache 量化** | 2024-2025 | Q8_0 省一半，Q4_0 省四分之三 |
| **FlashAttention (`-fa`)** | 2024 | 4K+ 上下文提速 30-50%，KV 内存减 ~50% |
| **Defragmentation** | 2023-2024 | 长期服务防止碎片化内存泄漏 |
| **Persistent Prefix Caching** | 2024-2025 | 复用系统 prompt，降低 TTFT |
| **mmap / mlock** | 2023-03 | 瞬载 + 防页错误卡顿 |

#### 2.4 推测解码：用「草稿」换带宽

| 技术 | 时间 | 机制 | 加速 |
|------|------|------|------|
| **Draft Model** | 2023-2024 | 小模型草稿 → 大模型并行验证 | 1.5-3x |
| **MTP (Multi-Token Prediction)** | 2025-2026 | 模型自带多 token 头（如 Qwen3.6） | RTX 3090: 38 → 65 t/s (1.71x) |
| **N-gram Cache** | 2024 | 从上下文/跨请求复用 n-gram | 无额外模型，对重复文本高效 |
| **EAGLE-3 / DFlash** | 2025 | 从目标模型 hidden states 提取特征做草稿 | 更高接受率 |

**核心洞察**：decode 阶段是内存带宽瓶颈，推测解码通过「一次前向验证多个 token」将内存受限转为计算受限，从而获得净收益。

---

### 三、vLLM 的优化哲学：「从单卡到数据中心，吞吐率至上」

vLLM 代表了**生产级服务**的优化路径，核心思想是：在 GPU 集群上服务成千上万并发请求，最大化吞吐而非单流延迟。

#### 3.1 PagedAttention：LLM 推理的「虚拟内存」

> **SOSP 2023** | v0.1 | `Kwon et al.`

- **机制**：将 KV Cache 拆分为固定大小的 **block**（默认 16 tokens），通过 **block table** 映射逻辑位置到物理内存。按需分配，copy-on-write 共享。
- **效果**：传统连续预分配浪费 **60-80%** 显存；PagedAttention 将浪费降至 **<4%**。高并发下吞吐比 HF Transformers 高 **up to 24x**。
- **代价**：batch=1 时比 FasterTransformer 慢 20-26%（block table 查找开销）。但吞吐场景的收益完全覆盖此代价。
- **衍生**：block 共享天然支持 **Prefix Caching** —— 相同前缀的 KV block 直接复用。

#### 3.2 连续调度体系：让 GPU 永不空闲

| 技术 | 版本 | 机制 | 效果 |
|------|------|------|------|
| **Continuous Batching** | v0.1 | 迭代级调度：每步结束后踢出完成请求、补入新请求 | GPU 利用率 30-40% → **75-90%**；吞吐 +2-3x |
| **Chunked Prefill** | v0.4+ | 将长 prefill 切小块，与 decode 请求同批执行 | TTFT p95 降 50-70%，避免单条长 prompt 阻塞所有 decode |
| **Multi-Step Scheduling + Async Output** | v0.6.0 | 一次准备输入，连续跑 n 步；CPU 后处理与 GPU 前向重叠 | Llama 8B 吞吐 **2.7x**，TPOT **5x** 降低 |
| **Prefix-Aware Scheduling** | v0.9.0+ | 调度器优先准入 cache-hit 请求，将高命中请求路由到同一实例 | 将 volatile token 移到 prompt 尾部可使 hit rate 从 0.3% → 87% |

#### 3.3 Attention 内核：FlashAttention 的渐进式集成

| 后端 | 支持版本 | 目标硬件 | H100 Llama 3.1 70B 32K 延迟 |
|------|----------|----------|---------------------------|
| Vanilla PyTorch | - | 通用 | 1820 ms (OOM at 32K) |
| xFormers | 早期 | 旧 GPU (V100/T4) | 480 ms / 18 GB |
| FlashAttention-2 | v0.3-v0.4 | Ampere+ | 220 ms / 14 GB |
| **FlashAttention-3** | v0.5-v0.6 | **Hopper (H100)** | **130 ms BF16 / 65 ms FP8** |

**vLLM 的自动选择链**：Hopper → FA-3 → FA-2 → FlashInfer → xFormers → SDPA。用户无需手动配置。

#### 3.4 Prefix Caching：消灭重复计算

- **机制**：per-block hash table + LRU 驱逐。请求前缀匹配 cached block 时，跳过这些 token 的 prefill。
- **效果**：1,847 token 共享前缀 + 94% hit rate → TTFT p50 从 **480 ms → 110 ms**，p95 从 **1.4 s → 280 ms**。
- **安全 caveat**：存在 timing side-channel 攻击 (GHSA-4qjh-9fv9-r85r)，攻击者可通过 TTFT 差异推断前缀是否命中。

#### 3.5 推测解码：vLLM 的多策略实现

| 方法 | 适用场景 | 训练成本 | 典型加速 |
|------|----------|----------|----------|
| N-gram | 摘要、prompt-heavy Q&A | 无 | up to 2.8x (低 QPS) |
| Draft Model | 通用 | 需小模型 | 1.5x |
| EAGLE-3 | 通用 chat, 大模型 | 需训练 draft head | 1.57-1.60x (70B) |
| MTP | 自带 MTP 的模型 | 模型已支持 | 1.5-1.7x |
| **Dynamic Speculative** | 全负载 | 动态调整 | 消除高 QPS 时的 slowdown |

**关键限制**：高 QPS 下推测解码可能导致 **1.4-1.8x slowdown**（额外草稿计算成为开销）。Dynamic speculative decoding 是 2025-2026 的关键方向。

#### 3.6 分布式与分离式架构

| 技术 | 版本 | 机制 | 效果 |
|------|------|------|------|
| **Tensor Parallelism (TP)** | v0.1 | 每 transformer 层跨 GPU 切分，NCCL all-reduce | 2xH100 下 KV cache 预算 +13.9x, 吞吐 +3.9x (超线性，因为显存释放允许更大 batch) |
| **Pipeline Parallelism (PP)** | v0.18 | 按深度切层，micro-batch 填 pipeline bubble | 适合 PCIe 工作站，多节点 405B+ 模型 |
| **Disaggregated Serving (PD分离)** | v0.7.3+ | prefill 节点与 decode 节点物理分离，KV 通过 RDMA/NCCL/NIXL 传输 | DistServe: 4-8x 吞吐；避免长 prefill 阻塞 decode ITL |

**PD 分离的 KV 传输生态**：
- **Mooncake (Kimi)**：RDMA/GPUDirect, CPU memory KV Store, KV-centric 调度。生产级最成熟。
- **DistServe**：学术研究先驱，RDMA/NVLink。
- **Splitwise (Azure)**：成本最优 GPU 选型，NCCL 传输。
- **vLLM NIXL**：UCX/libfabric/EFA 多后端。

---

### 四、跨生态共性技术：FlashAttention、量化与硬件协同设计

#### 4.1 FlashAttention 的硬件渐进

| 版本 | 时间 | 核心创新 | 性能 |
|------|------|----------|------|
| **FA-1** | 2022 | IO-aware tiling，SRAM 内完成 softmax，避免 HBM 写 N×N attention 矩阵 | 2-4x 加速，10x 省内存 |
| **FA-2** | 2023 | Warp-level 调度优化，非 matmul FLOP 减少，causal mask 优化 | ~2x 于 FA-1，A100 上 ~70% Tensor Core util |
| **FA-3** | 2024 | **Hopper 专用**：Warp specialization (TMA 异步加载 + WGMMA 计算)，ping-pong 调度，FP8 + incoherent processing | H100 75% util, **740 TFLOPS**; FP8 达 **1.2 PFLOPS** |
| **FA-4** | 2026 | Blackwell (B200) 专用：CuTeDSL，2-CTA MMA，software-emulated exp，conditional softmax rescaling | **1613 TFLOPS** on B200, 2.7x 于 Triton |

**关键洞察**：每一代 FlashAttention 都不是纯算法改进，而是**深度硬件协同设计**。FA-3 专为 Hopper 的 async execution 能力重写；FA-4 针对 Blackwell 的 Tensor Core 增速远超 SRAM/SFU 的瓶颈重新平衡。

#### 4.2 量化：从「压缩权重」到「全链路低精度」

| 技术 | 场景 | 精度 | 质量保留 | 速度 |
|------|------|------|----------|------|
| **GPTQ** | 通用后训练 | W4A16 | 94-96% | 快 (Marlin) |
| **AWQ** | 保护敏感权重 | W4A16 | **96-98%** | 快 (Marlin) |
| **Marlin** | 4-bit 推理 kernel | W4A16 | 依赖上游 | **Near-FP16** 吞吐 on Ampere+ |
| **FP8** | Hopper/Blackwell 原生 | W8A8 + KV FP8 | **99%+** | **最快** (2x 于 BF16, 硬件原生) |
| **SmoothQuant** | Pre-Hopper W8A8 | W8A8 | 高 | 中等 (解决 INT8 activation outlier) |

**FP8 正在取代 INT8 成为 H100+ 的默认选择**：因为 floating-point exponent 天然处理 activation outlier，无需 SmoothQuant 的复杂 scaling。

#### 4.3 硬件拓扑与 NUMA 效应

- **H100 (Hopper)**: 3.35 TB/s HBM3, 80GB。Prefill 瓶颈是 compute，decode 瓶颈是 memory BW。
- **H200 (2024)**: 同算力，**141GB HBM3e + 4.8 TB/s**。专为长上下文推理（KV cache 大）优化。
- **B200 (Blackwell, 2024)**: 2.25 PFLOPS FP16, 8 TB/s HBM3e。FP4 支持。Tensor Core 增速 > SRAM/SFU 增速 → **非 matmul 操作 (softmax, elementwise) 成为新瓶颈**。
- **AMD MI300X**: 192GB HBM3, 5.3 TB/s。多 chiplet (8 XCD) 暴露 NUMA 效应。需 XCD-aware scheduling + explicit VMEM/MFMA interleaving 才能达到 80-97% L2 hit rate。

---

### 五、前沿方向：2025-2026 及以后

| 方向 | 代表技术 | 核心思想 | 成熟度 |
|------|----------|----------|--------|
| **Disaggregated Serving** | Mooncake, DistServe, vLLM PD | Prefill/decode 物理分离，KV 作为一等分布式对象 | 生产中 (Kimi/Azure) |
| **MoE 稀疏路由优化** | Expert Parallelism (EP), SP-MoE | 仅激活部分 expert，all-to-all 通信重叠 | vLLM EP 已支持 |
| **SSM 替代 Attention** | Mamba-3, COREY | Linear-time sequence modeling，固定状态大小 | 研究中，1.5B-3B 有竞争力 |
| **多模态推理调度** | EPD, VisionZip, FasterVLM | Vision encoding / LLM prefill / LLM decode 三阶段分离 | 新兴 |
| **自适应推测解码** | Dynamic Speculative, Hydra | 根据负载动态调整草稿长度 | 活跃研究 |

---

## 优化后：现代引擎的基准画像

| 场景 | 引擎 | 配置 | 指标 | 对比基线 |
|------|------|------|------|----------|
| **本地单卡 7B** | llama.cpp | Q4_K_M, Metal/CUDA | 30-100+ t/s | 2023 年初 CPU FP32: ~1 t/s |
| **本地 70B** | llama.cpp | Q4_K_M + IQ2, 单卡 24GB | 可运行 | 2023 年不可行 |
| **服务 8B 高吞吐** | vLLM v1 | H100, FP8, TP=1, continuous batch | 数千 req/s | HF Transformers: 数十 req/s |
| **服务 70B 高吞吐** | vLLM v1 | 2xH100, FP8, TP=2, chunked prefill + prefix cache | TTFT 110ms, 3.9x 吞吐 | 基线: TTFT 480ms |
| **长上下文 32K** | vLLM + FA-3 | H100, FlashAttention-3 | 130ms prefill | FA-2: 220ms; PyTorch: OOM |
| **推测解码低 QPS** | vLLM | EAGLE-3 on 70B | 1.57-1.60x speedup | 无推测: 1.0x |

---

## 经验教训

### 1. 瓶颈识别是第一优化

> 不要假设瓶颈在哪里。用 `nvidia-smi`, profiler, roofline model 测量。  
> Transformer decode 的 FLOP/B ratio 仅 ~200 (A100) / ~295 (H100)。**内存带宽是天花板**。

### 2. 量化不是后处理，是架构决策

llama.cpp 将量化嵌入到生态的每一层（格式、kernel、后端）。vLLM 的 FP8 路径在 H100 上成为默认。量化已从「压缩模型」进化为「释放 batch size 和上下文长度」的核心手段。

### 3. 调度比内核更重要（在高并发时）

FlashAttention-3 可将单请求 prefill 加速 2x，但 **continuous batching + PagedAttention** 可将系统吞吐提升 24x。单点优化 vs. 系统级优化的收益差距巨大。

### 4. 硬件协同设计是指数级收益

FlashAttention-3 对 Hopper 的 warp specialization 不是通用优化，而是**针对 TMA/WGMMA 的指数级收益**。同样，FP8 在 Hopper 上 2x 加速，在旧 GPU 上不可用。选择优化方向时必须知道目标硬件的代际。

### 5. 推测解码的「普适性陷阱」

推测解码在 batch=1 时可加速 1.5-3x，但在高 QPS 下会变慢。Dynamic speculative decoding 和 PD 分离（让 prefill 节点做草稿）是解决方向。

### 6. 上下文长度是新的显存杀手

32K 上下文的 KV cache 可超过模型权重本身。KV cache quantization (INT8/FP8) + PagedAttention + Prefix Caching 是长上下文的三件套。未来 H200 的 141GB 显存和 4.8 TB/s 带宽正是为此而生。

### 7. 生态选择矩阵

| 需求 | 推荐引擎 | 理由 |
|------|----------|------|
| 本地/边缘/消费级 GPU | llama.cpp / Ollama | 最宽硬件支持，GGUF 生态 |
| 生产高吞吐、短 prompt | vLLM | Continuous batching + PagedAttention 成熟 |
| 生产多轮对话、RAG、Agent | SGLang | RadixAttention prefix caching 最强 |
| 极致 QPS / 稳定流量 | TensorRT-LLM | 手写 CUDA kernel + FP8，原始吞吐最高 |
| AMD MI300X | ROCm-vLLM / SGLang | 原生 composable kernel |
| 多 LoRA 服务 | vLLM v1 / LMDeploy | 原生 multi-LoRA adapter 支持 |
| 消费级单卡 70B+ | ExLlamaV2 / llama.cpp | EXL2/GGUF, 低 VRAM footprint |

---

## 参考

### 论文与核心文献

1. **Dao et al. (2022, 2023)**. FlashAttention v1/v2. NeurIPS. https://github.com/Dao-AILab/flash-attention
2. **Shah et al. (2024)**. FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision. arXiv:2407.08608
3. **Kwon et al. (2023)**. Efficient Memory Management for LLM Serving with PagedAttention. SOSP. https://github.com/vllm-project/vllm
4. **Frantar et al. (2023)**. GPTQ: Accurate Post-Training Quantization. ICLR.
5. **Lin et al. (2024)**. AWQ: Activation-aware Weight Quantization. MLSys 2024 Best Paper.
6. **Frantar et al. (2024)**. Marlin: Fast 4-bit Inference. https://github.com/IST-DASLab/marlin
7. **Cai et al. (2024)**. Medusa: Simple LLM Inference Acceleration with Multiple Decoding Heads. arXiv:2401.10774
8. **Li et al. (2024)**. EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty. ICML.
9. **Zheng et al. (2024)**. SGLang: Efficient Structured Generation.
10. **Qin et al. (2024)**. Mooncake: Kimi's Serving Platform. https://github.com/kvcache-ai/mooncake
11. **Zhong et al. (2024)**. DistServe: Disaggregating Prefill and Decode for LLM Serving.
12. **Gu & Dao (2023)**. Mamba: Linear-Time Sequence Modeling.

### 项目与仓库

- **llama.cpp**: https://github.com/ggml-org/llama.cpp
- **vLLM**: https://github.com/vllm-project/vllm
- **SGLang**: https://github.com/lm-sys/SGLang
- **TensorRT-LLM**: https://nvidia.github.io/TensorRT-LLM/
- **Spec-Bench**: https://github.com/hemingkx/Spec-Bench
- **Mooncake**: https://github.com/kvcache-ai/mooncake

---

> **编制说明**：本文档整合 llama.cpp (边缘端优化)、vLLM (服务端优化) 与跨生态共性技术 (FlashAttention, 量化, 硬件协同设计) 的演进脉络，以「瓶颈转移」为主线，展示现代 AI 推理引擎从「能运行」到「极致性能」的技术迭代路径。建议配合具体实验复现与 profiler 数据深化理解。
