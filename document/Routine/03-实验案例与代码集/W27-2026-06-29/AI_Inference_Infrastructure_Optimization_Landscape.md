# AI Inference Infrastructure Optimization Landscape

**Research Date:** 2026-07-02  
**Researcher:** Deep Research Specialist (Sub-agent)  
**Sources:** arXiv papers, official documentation, GitHub repositories, technical blogs, peer-reviewed conference proceedings (NeurIPS, ICML, MLSys, ACL, SOSP).  
**Confidence:** Primary sources cited where possible; uncertain claims flagged explicitly.

---

# Table of Contents

1. [Executive Summary](#executive-summary)
2. [Attention Optimizations](#1-attention-optimizations)
3. [Quantization](#2-quantization)
4. [Scheduling & Memory Management](#3-scheduling--memory-management)
5. [Speculative Decoding](#4-speculative-decoding)
6. [Hardware-Level Trends](#5-hardware-level-trends)
7. [Communication & Disaggregated Serving](#6-communication--disaggregated-serving)
8. [Model-Specific Optimizations](#7-model-specific-optimizations)
9. [Comparative Notes & Benchmarks](#8-comparative-notes--benchmarks)
10. [References](#9-references)

---

# Executive Summary

The AI inference infrastructure landscape has evolved dramatically over the past 2 years. The dominant themes are:  
**(a) Memory hierarchy exploitation** (FlashAttention, Paged KV Cache),  
**(b) Asynchronous execution on modern hardware** (H100/H200 TMA, WGMMA, FP8),  
**(c) Disaggregation of serving phases** (prefill vs. decode separation, KV transfer),  
**(d) Speculative execution** (draft-then-verify paradigms), and  
**(e) Model-specific kernel co-design** (MoE routing, SSM scans, multi-modal token pruning).  

A unifying insight: **the bottleneck has shifted from compute to memory bandwidth**, and modern optimizations are overwhelmingly about reducing HBM traffic and hiding latency via overlap.

---

# 评估指标详解

> 本文档涉及大量性能指标与对比维度。以下统一解释每个指标的**定义、计算方式、直观含义与局限性**，便于初学者快速定位关键信息。

- **TFLOPS (Tera Floating-point Operations Per Second)**: GPU每秒能执行多少万亿次浮点运算
  - 定义：$\text{TFLOPS} = \frac{\text{总浮点运算次数 (FLOPs)}}{\text{执行时间 (秒)} \times 10^{12}}$
  - 示例：H100 理论峰值 ~989 TFLOPS (FP16 dense)。FlashAttention-3 实测 740 TFLOPS 意味着利用了约 75% 的理论峰值
  - 为什么用：衡量**计算吞吐量**，是算法效率的核心指标
  - 局限性：只看 TFLOPS 会忽略内存带宽瓶颈。一个算法 TFLOPS 高，但如果数据搬运开销大，实际端到端延迟未必最优

- **Utilization (利用率)**: 实际达到的 TFLOPS 占 GPU 理论峰值 TFLOPS 的百分比
  - 定义：$\text{Utilization} = \frac{\text{Achieved TFLOPS}}{\text{Peak TFLOPS}} \times 100\%$
  - 示例：FlashAttention-2 在 H100 上 ~35% 利用率，FA-3 提升到 75%。这意味着 FA-3 更好地「喂饱」了 Tensor Core
  - 为什么用：不同 GPU 峰值不同，利用率是**跨硬件可比**的效率指标
  - 局限性：峰值 TFLOPS 通常是理论值（dense、无内存限制），实际可持续利用率很少超过 80%

- **Speedup (加速比)**: 优化后版本相对于基线版本的性能提升倍数
  - 定义：$\text{Speedup} = \frac{T_{\text{baseline}}}{T_{\text{optimized}}}$（时间比）或 $\frac{\text{Throughput}_{\text{optimized}}}{\text{Throughput}_{\text{baseline}}}$（吞吐比）
  - 示例：Speculative Decoding 报告 2.2x speedup 表示同样任务只需原时间的 1/2.2 ≈ 45%
  - 为什么用：直观反映优化收益，便于横向对比不同方法
  - 局限性：加速比高度依赖**基线选择**和**工作负载**。对短序列的加速比不能直接推广到长序列

- **Throughput (吞吐量)**: 单位时间内处理的请求数或生成的 token 数
  - 定义：$\text{Throughput} = \frac{\text{总请求数 (或 token 数)}}{\text{总时间 (秒)}}$，常用单位 req/s 或 tok/s
  - 示例：vLLM 的 Continuous Batching 将吞吐量从 10 req/s 提升到 30 req/s（3x 提升）
  - 为什么用：服务端最关心的指标，直接决定**单卡能服务多少用户**
  - 局限性：高吞吐往往以牺牲**首 token 延迟 (TTFT)** 或**单请求延迟**为代价，需与延迟指标联合看

- **Latency / TTFT (Time To First Token)**: 从收到请求到输出第一个 token 的延迟
  - 定义：$\text{TTFT} = t_{\text{first\_token\_out}} - t_{\text{request\_in}}$
  - 示例：Mooncake 通过 RDMA KV 传输将 TTFT 降低 25%，从 200ms 降到 150ms
  - 为什么用：用户**感知到的「响应速度」**，是交互体验的核心
  - 局限性：TTFT 只测第一个 token。对于长输出，**Inter-Token Latency (ITL)** 同样影响体验

- **ITL (Inter-Token Latency)**: 相邻两个生成 token 之间的间隔时间
  - 定义：$\text{ITL} = t_{\text{token}_i} - t_{\text{token}_{i-1}}$
  - 示例：ITL 从 50ms 降到 20ms，用户会感觉到输出「更流畅」
  - 为什么用：衡量**流式生成体验**。ITL 不稳定（jitter）会导致输出「卡顿感」
  - 局限性：ITL 与 batch size 强相关。batch 越大，ITL 通常越高

- **Memory Bandwidth (内存带宽)**: GPU 显存 (HBM) 与计算单元之间的数据传输速率
  - 定义：单位时间内可从 HBM 读取/写入的数据量，单位 GB/s 或 TB/s
  - 示例：H100 HBM3 带宽 3.35 TB/s；H200 提升到 4.8 TB/s。这意味着 H200 在纯内存受限场景下快 ~43%
  - 为什么用：现代 LLM inference 绝大多数场景是**内存带宽受限**（decode 阶段），带宽直接决定上限
  - 局限性：带宽利用率受限于访问模式（随机访问 vs 顺序访问）。理论带宽 ≠ 实际可达带宽

- **FLOP/B (Floating-point Operations per Byte)**: 每读取 1 字节数据需要进行多少次浮点运算
  - 定义：$\text{FLOP/B} = \frac{\text{总 FLOPs}}{\text{总数据搬运量 (Bytes)}}$
  - 示例：Transformer decode 的 FLOP/B ≈ 200 (A100)。这意味着每读 1 字节只做 200 次运算——远低于 GPU 计算峰值，所以是内存带宽瓶颈
  - 为什么用：判断 workload 是**计算受限**还是**内存带宽受限**的关键指标
  - 局限性：FLOP/B 是静态分析值，实际还受缓存命中率、并行效率影响

- **Quality Retention (质量保持率)**: 量化/压缩后模型相对于原始 FP16 模型的质量保留比例
  - 定义：通常用**困惑度 (Perplexity)** 或**下游任务准确率**的比值衡量
  - 示例：AWQ W4A16 量化后 MMLU 得分从 FP16 的 65% 降到 63.5%，质量保持率 ≈ 97.7%
  - 为什么用：量化不是免费的——质量保持率告诉你「省了多少内存」vs「丢了多少精度」
  - 局限性：不同任务对量化敏感度不同。MMLU 保持 98% 不代表代码生成任务也保持 98%

- **Acceptance Rate (接受率)**: Speculative Decoding 中，draft model 生成的 token 被 target model 验证通过的比例
  - 定义：$\text{Acceptance Rate} = \frac{\text{被接受的 draft tokens 数}}{\text{总 draft tokens 数}}$
  - 示例：EAGLE 的接受率 ~75%，Medusa ~65%。接受率越高，speculative decoding 收益越大
  - 为什么用：直接决定 speculative decoding 的**实际加速比**。理论上限 = $1 / (1 - \alpha)$，其中 $\alpha$ 为接受率
  - 局限性：高接受率不一定高 speedup——如果 draft model 本身很慢，验证开销可能抵消收益

---

---

# 1. Attention Optimizations

## 1.1 FlashAttention Family (v1 -> v2 -> v3 -> v4)

### FlashAttention v1 (2022)
- **What it is:** IO-aware exact attention algorithm that avoids materializing the N*N attention matrix in HBM by using tiling + softmax rescaling + recomputation. All operations (QK^T, softmax, PV) fused into a single kernel.
- **Project:** `Dao-AILab/flash-attention` (Stanford / Together AI)
- **Performance impact:** 2-4x faster attention, up to 10x lower memory vs. standard PyTorch attention.
- **Key insight:** The attention operation is memory-bound, not compute-bound. By keeping tiles in SRAM (fast on-chip cache) and avoiding HBM round-trips, the algorithm becomes IO-bound rather than memory-capacity-bound.
  - **初学者注**：SRAM 是 GPU 芯片上的高速缓存（速度 ~19 TB/s），HBM 是片外显存（速度 ~3 TB/s）。FA 的核心 trick 是「能不算的就不算，能不搬的就不搬」——通过分块 (tiling) 和在线重算 (recomputation) 避免把 $N \times N$ 的注意力矩阵写出到 HBM。
- **Source:** Dao et al., NeurIPS 2022.
- **Source:** Dao et al., NeurIPS 2022.

### FlashAttention v2 (2023)
- **What it is:** Algorithmic improvements on parallelism and work partitioning: better warp-level scheduling, reduced non-matmul FLOPs, and improved causal mask handling.
- **Project:** Same repo
- **Performance impact:** ~2x faster than FA-1, especially on long sequences. Achieved ~70% Tensor Core utilization on A100.
- **Key insight:** Reduces the number of synchronizations and better partitions work across warps/threads. The core math remains exact (no approximation).
- **Source:** Dao et al., 2023.

### FlashAttention v3 (2024)
- **What it is:** Deep algorithm-hardware co-design specifically for NVIDIA Hopper (H100) architecture. Introduces:
  - **Warp specialization**: Producer-consumer warp groups where some warps async-load data via TMA (Tensor Memory Accelerator) while others compute via WGMMA (Warpgroup Matrix Multiply-Accumulate).
  - **Tensor Memory Accelerator (TMA)**: Async data movement between HBM and SRAM without SM (Streaming Multiprocessor) involvement.
  - **Register Dynamic Reallocation**: Dynamic register allocation between producer and consumer warps.
  - **Ping-pong scheduling**: Interleaves matmul (GEMM) and softmax operations so Tensor Cores and SFUs (Special Function Units for exp) operate in parallel.
  - **FP8 support with incoherent processing**: Hadamard transform to reduce FP8 quantization error.
- **Project:** `Dao-AILab/flash-attention`
- **Performance impact:** 1.5-2.0x faster than FA-2 in FP16/BF16; up to **740 TFLOPS** (75% utilization) on H100. With FP8, reaches **~1.2 PFLOPS** with 2.6x smaller numerical error than baseline FP8 attention.
- **Key insight:** On H100, FA-2 only achieved ~35% utilization because it did not leverage Hopper's async execution capabilities. FA-3 fully exploits asynchrony to overlap data movement and compute at the micro-architectural level.
  - **初学者注**：H100 的 Tensor Core 理论峰值 ~989 TFLOPS，FA-2 只用到 35%（~346 TFLOPS），大量计算单元在「等数据」。FA-3 通过 **Warp Specialization**（一部分 warp 专门搬数据，一部分专门计算）和 **TMA 异步传输**（不占用 SM 计算资源的数据搬运）把利用率翻倍。这是典型的「算法-硬件协同设计」——不是算法本身变了，而是**调度方式**变了。
- **Note:** FA-3 also has custom adaptations for AMD MI300X (via Composable Kernel) with XCD-aware scheduling and LDS layout optimizations, achieving ~2x speedup over Triton baselines on MI300X.
- **Note:** FA-3 also has custom adaptations for AMD MI300X (via Composable Kernel) with XCD-aware scheduling and LDS layout optimizations, achieving ~2x speedup over Triton baselines on MI300X.
- **Source:** Shah et al., arXiv:2407.08608 (also PyTorch blog, Jul 2024).

### FlashAttention v4 (2026)
- **What it is:** Targets Hopper and Blackwell (B200). Written in CuTeDSL. Key features: fully asynchronous MMA, larger tiles, software-emulated exponentials, conditional softmax rescaling, tensor memory, and 2-CTA MMA.
- **Project:** `flash-attn-4`
- **Performance impact:** Up to 1.3x faster than cuDNN 9.13, up to 2.7x faster than Triton; **1613 TFLOPS** (71% utilization) on B200 BF16 benchmarks.
- **Key insight:** On Blackwell, Tensor Cores scaled much faster than shared memory bandwidth and SFUs. The bottleneck shifted, requiring larger tiles and software-emulated exponentials to keep Tensor Cores fed.
  - **初学者注**：B200 的 Tensor Core 算力增长到 2.25 PFLOPS，但共享内存带宽和 SFU（计算 exp 的专用单元）没有同比例增长。这意味着 softmax 里的 `exp` 成了新瓶颈——FA-4 用**软件模拟的指数函数**替代硬件 SFU，虽然单条指令慢了，但可以通过更大的 tile 和更好的并行掩盖延迟。这体现了「瓶颈转移」的普遍规律：优化一个瓶颈后，次优瓶颈会浮出水面。
- **Source:** BentoML / LLM Inference Handbook, 2025.
- **Source:** BentoML / LLM Inference Handbook, 2025.

---

# 2. Quantization

## 2.1 GPTQ (General-purpose Post-Training Quantization)
- **What it is:** Layer-wise post-training quantization using calibration data and approximate second-order information (OBS-style weight updates). Typically 4-bit weights with FP16/FP8 activations.
- **Project:** `AutoGPTQ`, `GPTQ-for-LLaMA`, `ExLlama`, `ExLlamaV2`
- **Performance impact:** 4-bit models retain ~94-96% of FP16 quality (perplexity). ~3x memory reduction. Inference speed fast with optimized kernels (e.g., Marlin).
- **Key insight:** Quantization-aware weight updates minimize the error introduced by rounding; the method is one-shot and requires ~128-256 calibration samples.
  - **初学者注**：GPTQ 的核心思想来自经典的最优脑外科 (Optimal Brain Surgeon, OBS)——量化一个权重后，不是简单四舍五入，而是**调整其他未量化权重来补偿误差**。这相当于「拆东墙补西墙」，用剩余权重的自由度来最小化层输出误差。校准数据只需 128-256 条，因为只关心权重的统计分布，不重新训练。
- **Trade-offs:** Calibration time 1-4 hours for 7B on A100. Quality degradation at 2-3-bit.
- **Trade-offs:** Calibration time 1-4 hours for 7B on A100. Quality degradation at 2-3-bit.
- **Source:** Frantar et al., ICLR 2023.

## 2.2 AWQ (Activation-aware Weight Quantization)
- **What it is:** Identifies and protects "salient" weights (those with large activation magnitudes) during quantization. Quantizes the rest aggressively.
- **Project:** `mit-han-lab/llm-awq` (MLSys 2024 Best Paper)
- **Performance impact:** W4A16 quantization retains ~96-98% of FP16 quality; 1-3% better than GPTQ at same bit-width. MMLU scores 0.5-1.5% higher than GPTQ.
- **Key insight:** Not all weights are equally important; protecting those with high activation impact preserves model quality per bit better than uniform quantization.
  - **初学者注**：AWQ 的发现是——**激活值大的权重对输出影响更大**。直观理解：如果某个权重 $w$ 总是乘以很小的激活 $a$，那量化误差 $|w - \hat{w}| \cdot a$ 也很小；反之，如果 $a$ 很大，同样的量化误差会被放大。AWQ 通过保护「高激活权重」（通常只占 1%），实现了比 GPTQ 更好的「每比特质量」。
- **Deployment:** vLLM, TGI both have optimized AWQ kernels. Marlin kernel backend is recommended for production.
- **Deployment:** vLLM, TGI both have optimized AWQ kernels. Marlin kernel backend is recommended for production.
- **Source:** Lin et al., MLSys 2024.

## 2.3 Marlin Kernel
- **What it is:** Optimized inference kernel for 4-bit quantized models (GPTQ/AWQ). Achieves near-FP16 latency on modern GPUs by using INT4 tensor core instructions and specialized memory layouts.
- **Project:** `IST-DASLab/marlin`
- **Performance impact:** Near-FP16 throughput for W4A16 models; the fastest 4-bit inference kernel on NVIDIA GPUs as of 2024-2025.
- **Key insight:** Memory bandwidth reduction from 4-bit weights dominates at batch=1; at higher batch sizes, compute throughput matters, and Marlin's tensor core utilization is critical.
  - **初学者注**：这是一个**batch size 决定瓶颈**的经典案例。batch=1 时，每次 forward 都要从 HBM 读一遍全部权重，4-bit 权重意味着带宽需求降为 1/4，所以**内存带宽是瓶颈**。batch 增大后，权重可以被复用（一次读取服务多个样本），此时矩阵乘法的计算量成为瓶颈，Marlin 的 Tensor Core 优化才显现价值。
- **Source:** Frantar et al., 2024.
- **Source:** Frantar et al., 2024.

## 2.4 FP8 / FP4 (TensorRT-LLM, NVIDIA Hopper/Blackwell)
- **What it is:** Native 8-bit or 4-bit floating point formats on H100 and B200. TensorRT-LLM automatically converts weights and activations to FP8 with minimal accuracy loss.
- **Project:** NVIDIA TensorRT-LLM
- **Performance impact:** FP8 doubles performance and halves memory vs. FP16/BF16 with minimal accuracy loss. FP4 on B200 further reduces memory.
- **Key insight:** FP8 uses E4M3/E5M2 formats with per-tensor or per-channel scaling. The hardware-native support on Hopper/Blackwell avoids the overhead of INT8/INT4 emulation.
  - **初学者注**：FP8 不是简单把 FP16 砍半。E4M3（4 位指数 3 位尾数）用于前向，E5M2（5 位指数 2 位尾数）用于反向——因为反向梯度需要更大动态范围。per-channel scaling 意味着每个通道有自己的缩放因子 $s$，实际值 = $s \times \text{FP8\_value}$，这比 per-tensor（整个矩阵一个 $s$）精度更高，但硬件支持更复杂。H100/B200 的 Tensor Core 原生支持 FP8，不需要像 INT4 那样用整数运算「模拟」浮点。
- **Comparative note:** TensorRT-LLM's FP8 path is more mature than vLLM's FP8 support; vLLM relies on Triton kernels which may not yet achieve the same Tensor Core utilization.
- **Comparative note:** TensorRT-LLM's FP8 path is more mature than vLLM's FP8 support; vLLM relies on Triton kernels which may not yet achieve the same Tensor Core utilization.
- **Source:** NVIDIA TensorRT-LLM docs, 2024.

## 2.5 GGUF (llama.cpp ecosystem)
- **What it is:** Universal quantization format for CPU+GPU+Apple Silicon inference. Supports various bit-widths (Q4_K_M, Q5_K_M, Q8_0) and mixed quantization strategies.
- **Project:** `ggerganov/llama.cpp`
- **Performance impact:** Q4_K_M offers ~95-98% quality retention; works on CPU with acceptable speed for small models. On GPU, Metal (Apple Silicon) and CUDA backends are available.
- **Key insight:** CPU inference is viable for small models (7B-13B) thanks to ARM NEON and AVX2 optimizations. The ecosystem (Ollama, LM Studio, Jan) is the widest.
  - **初学者注**：GGUF 的「K-quant」系列（如 Q4_K_M）不是均匀量化，而是把权重矩阵按列分组，对每组分别找最优的量化参数（scale + min）。这类似于「局部自适应量化」，比全局量化精度更高。Q4_K_M 的 "K" 代表 Kaiser 窗优化（一种减少量化误差的数学技巧），"M" 代表 medium（中等压缩率）。
- **Trade-off:** CPU inference is orders of magnitude slower than GPU for large batches or long contexts.
- **Trade-off:** CPU inference is orders of magnitude slower than GPU for large batches or long contexts.
- **Source:** localaimaster.com, 2026; llama.cpp project docs.

---

# 3. Scheduling & Memory Management

## 3.1 Continuous / In-Flight Batching
- **What it is:** Instead of static batching (waiting for all sequences to finish), the scheduler dynamically adds/removes sequences from the GPU batch at every iteration. New requests can join mid-generation.
- **Projects:** vLLM (continuous batching), TensorRT-LLM (in-flight batching), TGI, DeepSpeed-MII, SGLang
- **Performance impact:** Dramatically improves GPU utilization and throughput (2-5x over static batching) by eliminating idle time waiting for slow sequences to finish.
- **Key insight:** The critical parameter is the **arrival window**: widening the window improves throughput but increases tail latency. Production deployments must tune this based on SLO traces.
  - **初学者注**：Continuous Batching 的直观类比是**公交车的「滚动发车」**——传统 batching 等所有乘客（请求）到齐才发车，如果有人迟到，整车人都等着。Continuous Batching 允许「车开了还有人上」——新请求可以在任意 iteration 加入正在运行的 batch。代价是：如果窗口设得太宽（等太久），早到的请求会多等，TTFT 变长；设得太窄，batch 利用率低。这是一个**吞吐 vs 延迟的权衡**。
- **Comparative note:** TensorRT-LLM's in-flight batching is equivalent to vLLM's continuous batching but with tighter engine integration. SGLang adds RadixAttention for prefix caching on top.
- **Comparative note:** TensorRT-LLM's in-flight batching is equivalent to vLLM's continuous batching but with tighter engine integration. SGLang adds RadixAttention for prefix caching on top.
- **Source:** vLLM docs; Skywork.ai blog, 2025; quant67.com, 2026.

## 3.2 PagedAttention / Paged KV Cache
- **What it is:** Manages KV cache as fixed-size blocks (pages), similar to OS virtual memory. Avoids memory fragmentation and enables dynamic memory allocation and prefix sharing.
- **Projects:** vLLM (original), TensorRT-LLM, SGLang (RadixAttention), TGI v3, LMDeploy
- **Performance impact:** 2-4x higher throughput in multi-turn conversations; enables serving 2-4x more concurrent requests on the same GPU memory budget.
- **Key insight:** The KV cache is the dominant memory consumer in LLM serving. Paging eliminates pre-allocation overhead and allows memory sharing across requests with common prefixes (e.g., system prompts).
  - **初学者注**：PagedAttention 的灵感直接来自**操作系统虚拟内存**。传统实现会为每个请求预分配最大可能长度的 KV cache（如 4096 tokens × 层数 × 头数 × 维度），即使请求只生成 10 个 token，也占满 4096 的空间——这是巨大的浪费。PagedAttention 把 KV cache 切成固定大小的 block（如 16 tokens/block），按需分配，用完回收。内存碎片从 $O(N)$ 降到 $O(\text{block\_size})$，且支持**同前缀共享**（多个请求的系统 prompt 只存一份 KV）。
- **Page size tuning:** Typical page sizes are 16-32 KB. Larger pages reduce metadata overhead but increase internal fragmentation; smaller pages improve sharing granularity.
- **Page size tuning:** Typical page sizes are 16-32 KB. Larger pages reduce metadata overhead but increase internal fragmentation; smaller pages improve sharing granularity.
- **Source:** Kwon et al., SOSP 2023.

## 3.3 Prefix Caching & RadixAttention (SGLang)
- **What it is:** SGLang's RadixAttention uses a radix tree to cache and reuse KV states across requests with matching prefixes. This is particularly effective for multi-turn conversations, RAG, and agent workflows where system prompts and context are reused.
- **Project:** `lm-sys/SGLang`
- **Performance impact:** Up to 10x latency reduction for requests with high prefix overlap (e.g., shared system prompts, repeated queries).
- **Key insight:** Unlike vLLM's automatic prefix caching, RadixAttention finds the longest matching prefix and can handle partial matches. This is critical for agent/tool-call workflows where conversation prefixes diverge and then reconverge.
  - **初学者注**：RadixAttention 的核心数据结构是**基数树 (Radix Tree)**——一种压缩前缀树。想象多个对话共享同一个系统 prompt，但在第 10 轮后分道扬镳，第 20 轮又合并回同一个话题。普通前缀缓存只能匹配「从头到尾完全一致」的前缀；RadixAttention 能匹配「最长公共子序列」，把树的分叉和合并都利用起来。这在 Agent 场景（工具调用后上下文经常分叉）特别有效。
- **Source:** Zheng et al., 2024; quant67.com, 2026.
- **Source:** Zheng et al., 2024; quant67.com, 2026.

---

# 4. Speculative Decoding

## 4.1 Classic Speculative Decoding (Leviathan et al. 2022, Chen et al. 2023)
- **What it is:** A small "draft" model generates K candidate tokens; the large "target" model verifies them in parallel in one forward pass. Accepted tokens are emitted; rejected tokens trigger a single target-model forward pass.
- **Projects:** Implemented in TensorRT-LLM, vLLM, TGI, and various standalone frameworks.
- **Performance impact:** Theoretically up to 2-3x speedup. In practice, NVIDIA reports up to **3.6x** with well-chosen draft models. Speedup depends heavily on draft-target agreement rate.
- **Key insight:** The speedup is limited by the draft model's quality and the overhead of running it. If the draft model is too small, acceptance rate drops; if too large, overhead dominates.
  - **初学者注**：Speculative Decoding 的核心数学是——假设 draft model 一次生成 $K$ 个 token，接受率为 $\alpha$，则期望接受的 token 数为 $\alpha K$。加速比的上限约为 $\frac{1}{1-\alpha}$（当 draft 开销可忽略时）。如果 $\alpha = 0.5$，理论上限 2x；$\alpha = 0.75$，上限 4x。实际中 draft 模型本身也要跑，所以**最优的 draft 模型不是最小的**——需要在「接受率」和「单次 draft 成本」之间找平衡。
- **Source:** Leviathan et al., ICML 2022; Chen et al., 2023; NVIDIA TensorRT-LLM docs, 2025.
- **Source:** Leviathan et al., ICML 2022; Chen et al., 2023; NVIDIA TensorRT-LLM docs, 2025.

## 4.2 Medusa (Multiple Decoding Heads)
- **What it is:** Adds extra decoding heads on top of the target model's final hidden states. These heads predict multiple future tokens in parallel. No separate draft model needed.
- **Project:** `FasterDecoding/Medusa` (arXiv:2401.10774)
- **Performance impact:** Medusa-1 (frozen backbone + fine-tuned heads): **2.2x speedup** lossless. Medusa-2 (joint fine-tuning): **2.3-3.6x speedup**.
- **Key insight:** Avoids the draft model overhead entirely. Uses tree-based attention to verify multiple candidate continuations simultaneously. Training is self-distillation from the target model's own outputs.
  - **初学者注**：Medusa 的巧妙之处在于**「自举」**——不依赖外部 draft 模型，而是在目标模型的最后一层 hidden state 上接几个额外的「预测头」，每个头预测未来 1 个 token、2 个 token、...、K 个 token。这些头通过**自蒸馏**训练：用目标模型自己的输出作为标签，不需要额外数据。验证时使用**树注意力 (Tree Attention)**——把所有候选序列组织成树，共享公共前缀的计算，一次 forward 验证多个分支。
- **Trade-off:** Requires fine-tuning the heads; not zero-shot compatible with any model without training.
- **Trade-off:** Requires fine-tuning the heads; not zero-shot compatible with any model without training.
- **Source:** Cai et al., arXiv:2401.10774; CSDN blog, 2024.

## 4.3 EAGLE (Extrapolative Speculative Sampling)
- **What it is:** Uses a lightweight autoregressive head on the target model's hidden states (feature-level drafting). Builds an instance-adaptive tree of candidates and verifies them in one batched forward pass.
- **Project:** `EAGLE-ml` (ICML 2024)
- **Performance impact:** Generally higher acceptance rates than Medusa because it drafts at the feature level rather than the token level. Benchmarks on Spec-Bench show it consistently outperforms Medusa and classic speculative decoding on Vicuna-7B.
- **Key insight:** Feature-level drafting captures the target model's internal state better than token-level heads, leading to higher-quality speculation and better tree verification efficiency.
  - **初学者注**：EAGLE 与 Medusa 的关键区别是**「在哪 draft」**。Medusa 在 token 层面 draft（从 hidden state 直接预测 token）；EAGLE 在 feature 层面 draft（先预测下一层的 hidden state，再从 hidden state 解码 token）。feature 的语义空间比 token 更平滑、更连续，所以更容易预测。类比：预测「明天的天气」比预测「明天报纸上的每一个字」更容易——feature 是「天气」，token 是「字」。
- **Source:** Li et al., ICML 2024; Spec-Bench leaderboard, 2024.
- **Source:** Li et al., ICML 2024; Spec-Bench leaderboard, 2024.

## 4.4 Lookahead Decoding
- **What it is:** Training-free speculative decoding using N-gram matching from the prompt and generated text. Uses Jacobi iteration to generate multiple candidate tokens.
- **Project:** `hao-ai-lab/lookahead-decoding`
- **Performance impact:** Speedup depends on N-gram repetition in the text. Good for repetitive or structured outputs (code, JSON). Less effective for free-form creative writing.
- **Key insight:** No model training required. Works out-of-the-box on any autoregressive model. Best for tasks with high lexical overlap or template-based generation.
  - **初学者注**：Lookahead Decoding 的核心是**Jacobi 迭代**——一种解非线性方程组的数值方法。在自回归生成中，通常 $x_t = f(x_{<t})$，Jacobi 迭代同时猜测 $x_t, x_{t+1}, ..., x_{t+K}$，然后用并行 forward 验证这些猜测，保留正确的、修正错误的。N-gram 匹配提供「好的初始猜测」——如果文本中有重复模式（如代码里的缩进、JSON 的括号），猜测命中率很高。这完全**免训练**，但效果高度依赖输入数据的重复性。
- **Source:** Fu et al., ICML 2024; TechRxiv survey, 2025.
- **Source:** Fu et al., ICML 2024; TechRxiv survey, 2025.

## 4.5 REST (Retrieval-Based Speculative Decoding)
- **What it is:** Retrieves draft tokens from a datastore (e.g., prefix matching against past generations or a document corpus). Uses a DraftRetriever module.
- **Project:** `FasterDecoding/REST` (NAACL 2024)
- **Performance impact:** Highly variable; can be very effective for RAG and code-completion where the draft can be retrieved from a large context. Spec-Bench integration shows it is competitive with other methods.
- **Key insight:** Shifts the drafting burden from a model to a retrieval system. Excellent for long-document QA and code completion where the answer often appears verbatim in the context.
  - **初学者注**：REST 把 Speculative Decoding 的「生成」问题转化为「检索」问题。在 RAG 或代码补全场景中，答案往往已经在上下文里出现过——REST 用一个轻量级的检索模块（如 BM25 或向量匹配）从文档/代码库中找出最可能的后续 token 序列。这避免了 draft 模型的训练和推理开销，但**依赖数据存储的质量和覆盖率**。如果检索库中没有相关内容，接受率会骤降。
- **Source:** He et al., NAACL 2024; Spec-Bench docs.
- **Source:** He et al., NAACL 2024; Spec-Bench docs.

## 4.6 Spec-Bench Unified Benchmark
- **What it is:** A comprehensive benchmark and evaluation platform for speculative decoding methods. Evaluates EAGLE, Hydra, Medusa, Speculative Sampling, Prompt Lookup Decoding, REST, Lookahead Decoding, and SPACE on the same device and environment.
- **Project:** `hemingkx/Spec-Bench` (ACL 2024 Findings)
- **Key insight:** Standardized evaluation is critical because speedup is highly dependent on model, task, and hardware. Spec-Bench provides fair comparisons under controlled conditions.
  - **初学者注**：Spec-Bench 的重要性在于解决了**「苹果 vs 橘子」**问题。不同论文报告的 speedup 往往基于不同的模型（7B vs 70B）、不同的硬件（A100 vs H100）、不同的任务（代码 vs 创意写作）。Spec-Bench 固定了所有变量，在同一台机器、同一套模型、同一批任务上跑所有方法，让比较有意义。这是评估加速方法的「黄金标准」。
- **Source:** Xu et al., ACL 2024 Findings; https://github.com/hemingkx/Spec-Bench
- **Source:** Xu et al., ACL 2024 Findings; https://github.com/hemingkx/Spec-Bench

---

# 5. Hardware-Level Trends

## 5.1 NVIDIA H100 / H200 / B200 Architecture Evolution
- **H100 (Hopper, 2023):** Fourth-gen Tensor Cores, TMA (Tensor Memory Accelerator), WGMMA instructions, FP8 support. HBM3 bandwidth: 3.35 TB/s (SXM). 80GB HBM3.
- **H200 (2024):** Same compute as H100 but with **141GB HBM3e** and **4.8 TB/s** bandwidth. Specifically designed for inference workloads where KV cache size and memory bandwidth are the bottleneck.
- **B200 (Blackwell, 2024):** Fifth-gen Tensor Cores. FP4 support. 2.25 PFLOPS FP16 (dense). 8 TB/s HBM3e bandwidth. Asymmetric scaling: Tensor Cores scaled much faster than shared memory bandwidth and SFUs. This shifts the bottleneck to non-matmul operations (softmax, elementwise).
- **Key insight:** For **memory-bandwidth-bound** workloads (long-context Transformers, large batch decode), H200's bandwidth premium is worth the price. For **compute-bound** workloads (SSMs like Mamba, small-batch prefill), H100's price-to-performance ratio is better because the extra bandwidth goes unused.
  - **初学者注**：这是**「瓶颈决定性价比」**的经典案例。H200 比 H100 贵很多，但如果你的 workload 是 decode（内存带宽瓶颈），H200 的 4.8 TB/s vs H100 的 3.35 TB/s 直接转化为 ~43% 的吞吐提升，这笔钱花得值。但如果你的 workload 是 Mamba（计算瓶颈），H200 多出来的带宽「用不上」，H100 更划算。选择 GPU 前，先用 Roofline 模型判断瓶颈类型。
- **Source:** NVIDIA H100 Datasheet; NanoFlow (arXiv:2408.12757); Spheron blog, 2026.
- **Source:** NVIDIA H100 Datasheet; NanoFlow (arXiv:2408.12757); Spheron blog, 2026.

## 5.2 AMD MI300X
- **What it is:** AMD's flagship AI accelerator. 8 XCD chiplets, 304 CUs, 192GB HBM3, 5.3 TB/s HBM bandwidth, 896 GB/s Infinity Fabric.
- **Key specs:** 2.4x HBM capacity vs. H100 (80GB). 1.6x HBM bandwidth vs. H100. Memory bandwidth to compute ratio is favorable for memory-bound workloads.
- **Performance impact:** On FlashAttention-style kernels, MI300X achieves competitive performance with H100 when kernels are optimized for its multi-chiplet NUMA architecture (e.g., XCD-aware scheduling, explicit VMEM/MFMA interleaving). However, the lack of TMA and warp-specialized async execution means some Hopper-specific optimizations cannot be directly ported.
- **Key insight:** MI300X's multi-chiplet design exposes NUMA effects to software. The L2 cache is per-die, not unified. Swizzled Head-first Mapping and other NUMA-aware scheduling strategies are essential for high L2 hit rates (80-97% reported).
  - **初学者注**：MI300X 有 8 个 XCD（类似 8 个小 GPU 拼在一起），每个 XCD 有自己的 L2 缓存。如果数据分布不均匀，一个 XCD 要频繁访问另一个 XCD 的 L2（甚至 HBM），就会产生 NUMA 延迟。**Swizzled Head-first Mapping** 是一种数据重排策略：把 attention head 维度优先映射到 XCD，确保同一个 head 的计算尽量在同一个 XCD 内完成，减少跨 XCD 通信。这类似于 MPI 编程中的「数据亲和性」优化。
- **Source:** AMD MI300X specs; arXiv:2511.02132 (NUMA-aware scheduling); 与非网, 2024.
- **Source:** AMD MI300X specs; arXiv:2511.02132 (NUMA-aware scheduling); 与非网, 2024.

## 5.3 Memory Bandwidth vs. Compute Bottlenecks
- **Transformer decode:** Memory-bandwidth-bound. Each iteration loads all model weights and KV cache. The FLOP/B ratio is low (~200 FLOP/B for A100, ~295 for H100).
- **Transformer prefill:** Compute-bound. The large matmuls in the prompt processing phase saturate Tensor Cores.
- **SSM (Mamba) decode:** More compute-bound than Transformers because the state update is a fixed-size matrix multiplication (state size is constant, independent of sequence length). The bottleneck shifts from memory bandwidth to FLOP throughput at long context.
- **Roofline model insight:** For decode, the achievable throughput is `MemBW / (model_size_bytes + KV_cache_bytes_per_token)`. This is why quantization (reducing weight size) and KV cache compression (e.g., KV cache quantization, paging) are so effective for decode throughput.
  - **初学者注**：Roofline 模型是分析**「算力天花板 vs 带宽天花板」**的利器。对于 decode 阶段，每个 token 都要把全部模型权重和对应的 KV cache 从 HBM 读一遍，所以吞吐上限 = 带宽 / 每 token 数据量。量化把 `model_size_bytes` 降为 1/4（4-bit），直接让上限提升 4x；KV cache paging 减少碎片和冗余存储，降低 `KV_cache_bytes_per_token`。这就是为什么「内存优化」对 decode 如此重要——它直接抬高了 Roofline 的「带宽墙」。
- **Source:** NanoFlow (arXiv:2408.12757); Table 1 in NanoFlow paper.
- **Source:** NanoFlow (arXiv:2408.12757); Table 1 in NanoFlow paper.

---

# 6. Communication & Disaggregated Serving

## 6.1 NCCL and Custom Collectives
- **NCCL (NVIDIA Collective Communications Library):** Standard for multi-GPU all-reduce, all-gather, reduce-scatter, all-to-all. Used by all major frameworks (vLLM, TensorRT-LLM, DeepSpeed, SGLang).
- **All-to-all in MoE:** Expert parallelism requires token shuffling between GPUs via all-to-all. This is the dominant communication cost in MoE inference. The cost scales with `batch_size * hidden_dim * num_experts_activated`.
- **Optimization:** Overlapping communication with compute (e.g., via NCCL's point-to-point or custom RDMA) is critical. FlowKV and others optimize the KV cache structure to reduce the number of NCCL calls.
  - **初学者注**：All-to-all 通信的本质是**「数据重排」**：每个 GPU 只负责一部分 expert，但每个 token 需要路由到正确的 expert，所以要把 token 的 hidden state 从「按 token 分布」重排为「按 expert 分布」。这类似于深度学习中的 `torch.distributed.all_to_all`。优化关键是**「隐藏通信延迟」**——在等数据到达时做其他计算（如 attention），或在数据搬运时重叠下一个层的计算。NCCL 的 point-to-point 允许更细粒度的重叠控制。
- **Source:** vLLM MoE docs; Sem-MoE paper, 2026.
- **Source:** vLLM MoE docs; Sem-MoE paper, 2026.

## 6.2 Disaggregated Serving (Prefill-Decode Separation)
- **What it is:** Separates the prefill phase (prompt processing, compute-bound) from the decode phase (token generation, memory-bandwidth-bound) onto different GPU pools. The KV cache is transferred from prefill nodes to decode nodes via high-speed interconnect (RDMA, NVLink, or custom transfer engines).
- **Projects:** Mooncake (Kimi / Moonshot AI), DistServe (UCSD), Splitwise (Microsoft), FlowKV, vLLM disaggregated serving, TensorRT-LLM (Beta)
- **Performance impact:**
  - DistServe: 4-8x throughput improvement at same SLO.
  - Sarathi-Serve: 2.6-5.6x improvement in throughput-latency tradeoffs over vLLM.
  - FlowKV: Optimizes KV cache structure to reduce NCCL communication overhead; eliminates transfer time relative to total request latency.
- **Key insight:** Prefill and decode have opposite resource preferences. Prefill likes large batches and high compute; decode likes small, consistent steps and high memory bandwidth. Mixing them causes interference: a large prefill job stalls decode jobs, causing inter-token latency (ITL) jitter.
  - **初学者注**：这是一个**「资源偏好冲突」**问题。Prefill 是大矩阵乘法（计算密集），decode 是逐 token 读取权重（带宽密集）。如果把它们混在同一个 GPU 上，一个长 prefill 会占用大量 SM（Streaming Multiprocessor），导致 decode 的 token 被「插队」，ITL 忽高忽低（jitter）。分离后，prefill 节点可以大胆用大 batch，decode 节点保持稳定的低延迟——类似于餐厅把「点菜」（prefill）和「上菜」（decode）分成两个窗口。
- **KV Transfer mechanisms:**
- **KV Transfer mechanisms:**
  - **RDMA (Mooncake):** Uses GPUDirect RDMA for zero-copy transfer. ~25% lower TTFT than TCP-based transports.
  - **NCCL-based (Splitwise, vLLM):** Good protocol compatibility (RoCE, IB, Socket) but frequent NCCL transfers can limit effectiveness.
  - **NIXLConnector:** NVIDIA's Inference Xfer Library; supports UCX, libfabric, EFA.
- **Comparative note:** TensorRT-LLM's disaggregated serving is in beta. vLLM v1 has native `--kv-transfer-config` support. Mooncake (Kimi's production system) is the most mature open-source disaggregated serving platform, with a KV-centric scheduler that routes by KV affinity rather than request affinity.
- **Source:** quant67.com, 2026; Ray Serve docs; vLLM PR #10502; Mooncake GitHub docs.

## 6.3 Mooncake (Kimi Serving Platform)
- **What it is:** Production serving platform for Kimi. Core innovations: KVCache Store (CPU memory pool for KV cache), RDMA/GDS transfer, KV-centric scheduling.
- **Project:** `kvcache-ai/mooncake`
- **Performance impact:** Enables xPyD (any prefill, any decode) disaggregation. Supports vLLM and SGLang integration. Mean TTFT up to 25% lower than traditional TCP-based transports.
- **Key insight:** Treats KV cache as a first-class distributed object. The scheduler makes decisions based on KV cache locality, not just request queue length. This is critical for multi-turn conversations where the KV cache is large and re-computation is expensive.
  - **初学者注**：Mooncake 的 KV-centric scheduling 把 KV cache 从「附属品」提升为「一等公民」。传统调度器只看「哪个队列最长」，Mooncake 还看「哪个节点已经有这个对话的 KV cache」。在多轮对话中，第 N 轮的 KV cache 就是第 N-1 轮的结果——如果能把请求路由到「上一轮处理过的节点」，就省去了 KV 传输开销。这类似于 CDN 的「边缘缓存」策略：把内容（KV）放在离用户（请求）最近的地方。
- **Source:** Mooncake GitHub README; Qin et al., 2024.
- **Source:** Mooncake GitHub README; Qin et al., 2024.

---

# 7. Model-Specific Optimizations

## 7.1 Mixtral / MoE (Mixture of Experts) Inference
- **What it is:** MoE models use sparse activation: only a subset of "expert" FFNs fire per token. This reduces active compute but increases memory footprint (all experts must be resident) and communication overhead (all-to-all routing).
- **Key projects:** vLLM, SGLang, TensorRT-LLM, DeepSpeed-MoE, Sem-MoE, SP-MoE, MoE-Infinity
- **Parallelism strategies:**
  - **Expert Parallelism (EP):** Distributes experts across GPUs. Each GPU owns a subset of experts. Tokens are routed via all-to-all. Best for 2-8 GPUs with high-bandwidth NVLink.
  - **Tensor Parallelism (TP):** Shards each expert across GPUs. Better when individual experts exceed single-GPU VRAM or for prefill latency reduction.
  - **Pipeline Parallelism (PP):** Splits layers across GPUs. Only used when EP/TP are insufficient; introduces pipeline bubbles.
  - **Mixed strategies:** vLLM supports combinations (e.g., EP + TP). The formula is `EP_SIZE = TP_SIZE * DP_SIZE`.
- **Performance impact:** DeepSeek-R1 (256 routed experts, 8 activated) requires careful EP tuning. With FP8 quantization on 8x H100, production deployments achieve good throughput-latency tradeoffs.
- **Key insight:** MoE inference is dominated by (a) all-to-all communication latency, and (b) load balancing across experts. Expert hotness can cause some GPUs to be overloaded. Solutions like Lina (non-uniform expert replicas) and EPS-MoE (dynamic GroupGemm/DenseGemm backend selection) address this.
  - **初学者注**：MoE 的「稀疏激活」是双刃剑——计算量少了，但**所有 expert 的权重都要驻留显存**（因为不知道哪个会用到）。这导致 MoE 的显存占用是 dense 模型的 4-8x。all-to-all 通信是另一个隐形杀手：每个 token 只激活 2-8 个 expert，但要把 token 的 hidden state 发到这些 expert 所在的 GPU，通信量 = `batch_size × hidden_dim × num_activated`。当 batch 大时，这会成为瓶颈。Lina 的 trick 是给热门 expert 多配几个副本（类似负载均衡中的「加权轮询」），分散压力。
- **Comparative note:** vLLM's `--enable-expert-parallel` is the go-to for 2-8 GPU setups. TensorRT-LLM has optimized MoE kernels but requires engine build. SGLang also supports EP with good performance.
- **Comparative note:** vLLM's `--enable-expert-parallel` is the go-to for 2-8 GPU setups. TensorRT-LLM has optimized MoE kernels but requires engine build. SGLang also supports EP with good performance.
- **Source:** vLLM MoE docs; AMD ROCm blog, 2025; Spheron blog, 2026; Sem-MoE paper (arXiv:2503.04398).

## 7.2 Mamba / State Space Models (SSM)
- **What it is:** Linear-complexity sequence models that replace quadratic attention with a state space recurrence. The state is a fixed-size matrix, so memory per token is constant (unlike KV cache which grows with sequence length).
- **Projects:** `state-spaces/mamba`, `mamba-minimal`, `vLLM` (increasing SSM support), `COREY` (entropy-guided chunk scheduling)
- **Performance impact:**
  - Mamba-1: 3x faster than Transformer on A100 for long sequences, thanks to hardware-aware parallel scan (Triton/CUDA).
  - Mamba-2: 2-8x faster training than Mamba-1 via structured state-space duality.
  - Mamba-3: Designed for inference, not just training. MIMO SSM design. Beats Mamba-2 and Llama-3.2-1B on prefill+decode latency at 1.5B scale. Kernels built with Triton, TileLang, and CuTe DSL.
- **Key insight:** For long context, SSMs shift from memory-bandwidth-bound (Transformers) to compute-bound. This changes GPU economics: H100's compute advantage matters more than H200's bandwidth advantage for SSM workloads. The state update is a matrix multiplication over a fixed-size state, which Tensor Cores handle well.
  - **初学者注**：SSM 的核心优势是**「状态大小恒定」**。Transformer 的 KV cache 随序列长度线性增长（$O(L)$），所以长序列时内存带宽是瓶颈；SSM 的状态是一个固定大小的矩阵（如 $N \times D$，与序列长度无关），所以无论多长的序列，每步的计算量都一样。这使得 SSM 在长序列时从「带宽受限」转为「计算受限」——H100 的高算力比 H200 的高带宽更有价值。但 SSM 的并行扫描 (parallel scan) 比 attention 的矩阵乘法更难优化，kernel 成熟度是当前的短板。
- **Kernel optimization:** COREY (entropy-guided runtime chunk scheduling) dynamically selects chunk sizes for selective scan kernels based on activation entropy, improving throughput by adapting to the input's local complexity.
- **Kernel optimization:** COREY (entropy-guided runtime chunk scheduling) dynamically selects chunk sizes for selective scan kernels based on activation entropy, improving throughput by adapting to the input's local complexity.
- **Comparative note:** SSMs are still less mature than Transformers for general-purpose serving. vLLM and TensorRT-LLM are adding SSM support, but the ecosystem is smaller. The 1.5B-3B SSM models show promise, but scaling to 70B+ with quality competitive to Transformers is an open research question.
- **Source:** Gu & Dao, 2023; Dao & Gu, 2024; Together AI blog (Mamba-3), 2026; arXiv:2604.10597 (COREY); arXiv:2604.07935 (edge efficiency analysis).

## 7.3 Multi-Modal (Vision-Language) Inference Scheduling
- **What it is:** VLMs (e.g., LLaVA, InternVL, Qwen-VL) encode images into hundreds or thousands of visual tokens that are fed into the LLM. The prefill phase is dominated by vision encoding (often a ViT) and the LLM prefill of visual tokens.
- **Key optimizations:**
  - **Vision token compression:** Reducing visual tokens via pruning, merging, or dropping less important tokens. Methods: FasterVLM, VisionZip, PyramidDrop, SparseVLM, FastV.
  - **Modality-aware scheduling:** MMInference uses modality-aware permutation sparse attention to accelerate prefill for long-context VLMs.
  - **Disaggregated multi-modal serving:** EPD (Encoding-Prefill-Decode) separates vision encoding, LLM prefill, and LLM decode into different stages. This allows encoding multiple video frames in parallel and pipelining the stages.
- **Performance impact:** Vision tokens can dominate the sequence length (e.g., 2880 tokens for a 672x672 image). Compression can reduce this by 2-10x with minimal accuracy loss. EPD disaggregation can reduce head-of-line blocking for long video inputs.
- **Key insight:** The bottleneck in VLM inference is often the vision encoder (for single images) or the LLM prefill (for long videos). Unlike text-only LLMs, the workload is bimodal: image encoding is compute-heavy and parallelizable, while LLM decode is memory-bandwidth-bound. This makes disaggregated serving even more beneficial for VLMs.
  - **初学者注**：VLM 的「双峰」特性意味着**单一优化策略不够**。对于单图输入，ViT 编码是瓶颈（要把 224×224 像素的图转成 576 个 visual token，涉及大量卷积/注意力计算）；对于长视频，LLM prefill 成为瓶颈（ thousands of visual tokens 要一次性处理）。EPD（Encoding-Prefill-Decode）分离把这三个阶段分到不同 GPU：编码节点用高算力 GPU（如 H100），decode 节点用高带宽 GPU（如 H200），实现「各尽其用」。
- **Comparative note:** Standard LLM serving systems (vLLM, TGI) can serve VLMs but do not optimize for the vision-specific bottlenecks. Dedicated systems like HeteroServe and EPD are emerging to address modality-level partitioning and cross-tier GPU heterogeneity.
- **Comparative note:** Standard LLM serving systems (vLLM, TGI) can serve VLMs but do not optimize for the vision-specific bottlenecks. Dedicated systems like HeteroServe and EPD are emerging to address modality-level partitioning and cross-tier GPU heterogeneity.
- **Source:** arXiv:2603.12707 (HeteroServe); arXiv:2501.05460 (EPD); OpenReview papers on MMInference, 2025.

---

# 8. Comparative Notes & Benchmarks

## 8.1 Engine Comparison Matrix

| Workload | Best Engine | Why |
|----------|-------------|-----|
| Short prompt + short output | vLLM | Continuous batching is mature and stable |
| Long system prompt + repeated queries | SGLang | RadixAttention prefix caching dominates |
| Agent / multi-turn / tool call | SGLang | Radix + structured output support |
| Ultra-long context (128K+) | SGLang / vLLM v1 | Hierarchical KV management |
| Max QPS / stable traffic | TensorRT-LLM | Hand-optimized CUDA kernels, FP8, best raw throughput |
| AMD / MI300X | ROCm-vLLM / SGLang | Native composable kernel support |
| Multi-LoRA serving | vLLM v1 / LMDeploy | Native multi-LoRA adapter support |
| Heavy FP8/INT4 quantization | LMDeploy / TensorRT-LLM | Mature quantization kernels |
| Consumer GPU (1x RTX 4090) | ExLlamaV2 / llama.cpp | GGUF/EXL2 format, low VRAM footprint |

## 8.2 FlashAttention vs. Standard Attention

| Metric | PyTorch SDP | FlashAttention-2 | FlashAttention-3 (H100) |
|--------|-------------|------------------|------------------------|
| H100 FP16 Utilization | ~30% | ~35% | **75%** |
| FP8 Support | No | Limited | **Yes (~1.2 PFLOPS)** |
| Memory Traffic | O(N^2) | O(N) | O(N) (async) |
| Sequence Length | 8K-32K typical | 128K+ | 128K+ |
| Hardware Lock-in | None | Ampere+ | **Hopper+** |

## 8.3 Quantization Quality Comparison (4-bit)

| Format | Quality Retention | Speed | Ecosystem |
|--------|-------------------|-------|-----------|
| AWQ | **96-98%** | Fast (Marlin) | vLLM, TGI |
| GPTQ | 94-96% | Fast (Marlin) | Widest (HuggingFace) |
| GGUF Q4_K_M | 95-98% | Medium (CPU/GPU) | llama.cpp, Ollama |
| FP8 | 99%+ | **Fastest** | TensorRT-LLM (H100+) |

## 8.4 Disaggregated Serving Solutions

| System | Transfer Mechanism | Key Innovation | Maturity |
|--------|-------------------|--------------|----------|
| Mooncake | RDMA/GDS | KV-centric scheduling, CPU KV Store | Production (Kimi) |
| DistServe | RDMA/NVLink | First academic PD separation | Research |
| Splitwise | NCCL | Cost-optimal GPU type selection | Azure (production) |
| vLLM + NIXL | NIXLConnector | Multiple backends (UCX, EFA) | v1 (beta) |
| FlowKV | Optimized NCCL | KV structure optimization, Load-aware | Research |

## 8.5 Speculative Decoding Speedup Summary (Vicuna-7B, Spec-Bench)

| Method | Approx. Speedup | Draft Source | Training-Free |
|--------|----------------|-------------|--------------|
| Classic Speculative | 1.5-2.5x | Separate small model | No (needs draft model) |
| Medusa-1 | 2.2x | Extra heads on target | Yes (heads trained) |
| Medusa-2 | 2.3-3.6x | Extra heads on target | Yes (joint training) |
| EAGLE | 2.5-3.5x | Feature-level head | Yes (head trained) |
| Lookahead | 1.2-2.0x | N-gram matching | **Yes** |
| REST | 1.3-2.5x | Retrieval datastore | **Yes** (after datastore build) |

*Note: Exact speedup depends on model, task, and hardware. Spec-Bench is the recommended reference for fair comparisons.*

---

## 8.6 配置矩阵：初学者选型指南

> 以下矩阵按「场景 → 推荐配置」组织，帮助初学者根据实际需求快速定位技术栈。

### 场景1：个人开发者 / 本地部署（单卡消费级 GPU）

| 维度 | 推荐选择 | 理由 |
|------|----------|------|
| 量化格式 | GGUF Q4_K_M (llama.cpp) | 单卡显存有限（24GB），4-bit 量化让 70B 模型可运行 |
| 推理框架 | llama.cpp / Ollama / LM Studio | 生态最完善，一键运行，支持 CPU fallback |
| Attention | FlashAttention-2 (若支持) | 长上下文时降低显存占用 |
| 不推荐 | TensorRT-LLM / vLLM | 消费卡不支持 FP8，且这些框架为服务器设计，本地使用过重 |

### 场景2：中小规模 API 服务（1-8 张 A100/H100）

| 维度 | 推荐选择 | 理由 |
|------|----------|------|
| 推理框架 | vLLM | Continuous Batching + PagedAttention 成熟稳定，社区活跃 |
| 量化 | AWQ W4A16 + Marlin kernel | 质量保持 96-98%，速度接近 FP16 |
| Attention | FlashAttention-2 (A100) / FA-3 (H100) | 根据 GPU 代际选择，H100 务必用 FA-3 发挥 async 优势 |
| 长上下文 | SGLang (RadixAttention) | 多轮对话/Agent 场景下前缀缓存收益巨大 |
| 部署模式 | 统一部署（prefill+decode 同机） | 1-8 卡规模下，PD 分离的通信开销可能抵消收益 |

### 场景3：大规模生产服务（8+ 张 H100/H200）

| 维度 | 推荐选择 | 理由 |
|------|----------|------|
| 推理框架 | vLLM v1 + Mooncake / 自研 PD 分离 | 大规模下 PD 分离是必选项，Mooncake 的 KV-centric 调度成熟 |
| 量化 | FP8 (TensorRT-LLM) | H100/H200 原生支持，吞吐最高，质量损失 <1% |
| Attention | FlashAttention-3 (H100) / FA-4 (B200) | 硬件专用优化，利用率可达 70-75% |
| MoE 模型 | EP + TP 混合并行 | vLLM `--enable-expert-parallel`，注意 all-to-all 通信优化 |
| 长上下文 | 分层 KV 管理 / KV cache 量化 | 128K+ 上下文必须压缩 KV，否则显存爆炸 |

### 场景4：边缘/移动端部署

| 维度 | 推荐选择 | 理由 |
|------|----------|------|
| 模型大小 | 1.5B-3B SSM (Mamba-3) | 状态恒定，长序列时比 Transformer 更省显存/内存 |
| 量化 | INT4 / INT8 (GGUF) | 极限压缩，配合 ARM NEON/AVX2 指令集优化 |
| 框架 | llama.cpp (Metal/CUDA backend) | 跨平台支持最好，Apple Silicon 可用 Metal |
| 注意 | 避免大 batch | 边缘设备内存极小，batch=1 是常态 |

### 快速决策树

```
1. 你有几张 GPU？
   ├─ 1 张 4090/3090 → llama.cpp + GGUF Q4_K_M
   ├─ 1-4 张 A100 → vLLM + AWQ + FlashAttention-2
   └─ 8+ 张 H100 → vLLM/Mooncake + FP8 + FlashAttention-3 + PD 分离

2. 你的主要场景？
   ├─ 多轮对话/Agent → SGLang (RadixAttention)
   ├─ 长文档 RAG → 长上下文模型 + KV cache 压缩
   └─ 代码生成/结构化输出 → Speculative Decoding (EAGLE/Medusa)

3. 你的瓶颈是什么？
   ├─ 显存不够 → 量化 (AWQ/GPTQ/FP8)
   ├─ 吞吐不够 → Continuous Batching + PD 分离
   └─ 延迟太高 → FlashAttention + 小 batch + KV cache 优化
```

---

# 9. References

1. **FlashAttention v1/v2:** Dao et al. (2022, 2023). *Fast and Memory-Efficient Exact Attention.* NeurIPS. https://github.com/Dao-AILab/flash-attention
2. **FlashAttention v3:** Shah et al. (2024). *FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision.* https://pytorch.org/blog/flashattention-3/ (also arXiv:2407.08608)
3. **FlashAttention v4:** (2026). *FlashAttention-4: Asynchronous MMA and Blackwell Optimization.* BentoML LLM Inference Handbook, 2025. https://bentoml.com/llm/kernel-optimization/flashattention
4. **TensorRT-LLM:** NVIDIA. https://nvidia.github.io/TensorRT-LLM/overview.html
5. **DeepSpeed Inference:** Microsoft. https://www.deepspeed.ai/ — Holmes et al. (2024). DeepSpeed-MII.
6. **TGI:** HuggingFace. https://github.com/huggingface/text-generation-inference
7. **AWQ:** Lin et al. (2024). *AWQ: Activation-aware Weight Quantization.* MLSys 2024 Best Paper. https://github.com/mit-han-lab/llm-awq
8. **GPTQ:** Frantar et al. (2023). *GPTQ: Accurate Post-Training Quantization.* ICLR 2023. https://github.com/IST-DASLab/gptq
9. **Marlin:** Frantar et al. (2024). *Marlin: Fast 4-bit Inference.* https://github.com/IST-DASLab/marlin
10. **vLLM:** Kwon et al. (2023). *Efficient Memory Management for LLM Serving.* SOSP. https://github.com/vllm-project/vllm
11. **SGLang:** Zheng et al. (2024). *SGLang: Efficient Structured Generation.* https://github.com/lm-sys/SGLang
12. **Medusa:** Cai et al. (2024). *Medusa: Simple LLM Inference Acceleration with Multiple Decoding Heads.* arXiv:2401.10774. https://github.com/FasterDecoding/Medusa
13. **EAGLE:** Li et al. (2024). *EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty.* ICML 2024. https://github.com/SafeAILab/EAGLE
14. **Lookahead Decoding:** Fu et al. (2024). *Lookahead: Break the Sequential Dependency.* ICML 2024. https://github.com/hao-ai-lab/lookahead-decoding
15. **REST:** He et al. (2024). *REST: Retrieval-Based Speculative Decoding.* NAACL 2024. https://github.com/FasterDecoding/REST
16. **Spec-Bench:** Xu et al. (2024). *Spec-Bench: A Comprehensive Benchmark for Speculative Decoding.* ACL 2024 Findings. https://github.com/hemingkx/Spec-Bench
17. **Mooncake:** Qin et al. (2024). *Mooncake: Kimi's Serving Platform.* https://github.com/kvcache-ai/mooncake
18. **DistServe:** Zhong et al. (2024). *Disaggregating Prefill and Decode for LLM Serving.*
19. **Splitwise:** Patel et al. (2024). *Splitwise: Splitwise Disaggregated Serving.*
20. **FlowKV:** (2025). *FlowKV: Disaggregated Inference with Low-Latency KV Transfer.* arXiv:2504.03775
21. **Mamba:** Gu & Dao (2023). *Mamba: Linear-Time Sequence Modeling.* https://github.com/state-spaces/mamba
22. **Mamba-2:** Dao & Gu (2024). *Transformers are SSMs.* arXiv:2405.04560
23. **Mamba-3:** (2026). *Mamba-3: Inference-First SSM Design.* Together AI blog, 2026. https://www.together.ai/blog/mamba-3
24. **COREY:** (2026). *Entropy-Guided Runtime Chunk Scheduling for Selective Scan.* arXiv:2604.10597
25. **NanoFlow:** Jin et al. (2024). *NanoFlow: Towards Optimal LLM Serving Throughput.* arXiv:2408.12757
26. **AMD MI300X:** AMD (2023). https://www.amd.com/en/products/accelerators/instinct/mi300
27. **NUMA-aware Scheduling for MI300X:** Choudhary & Sangaiah (2025). *Swizzled Head-first Mapping for Disaggregated GPUs.* arXiv:2511.02132
28. **Sem-MoE:** (2026). *Semantic Parallelism for MoE Inference.* arXiv:2503.04398
29. **Expert Parallelism in vLLM:** AMD & vLLM teams (2025). https://rocm.blogs.amd.com/software-tools-optimization/vllm-moe-guide/
30. **MMInference / EPD:** (2025). *Efficiently Serving Large Multimodal Models via EPD.* arXiv:2501.05460
31. **SP-MoE:** (2025). *Speculative Decoding and Prefetching for MoE.* arXiv:2510.10302
32. **HeteroServe:** (2026). *Cost-Efficient Multimodal LLM Inference via Cross-Tier GPU Heterogeneity.* arXiv:2603.12707
33. **FlatAttention:** (2024). *Dataflow and Fabric Collectives Co-Optimization for MHA.* arXiv:2505.18824
34. **ULTRA-HSTU:** (2025). *Bending the Scaling Law Curve in Large-Scale Recommendation Systems.* arXiv:2602.16986
35. **Triton Attention Kernel:** (2025). *The Anatomy of a Triton Attention Kernel.* arXiv:2511.11581

---

**End of Report.**
