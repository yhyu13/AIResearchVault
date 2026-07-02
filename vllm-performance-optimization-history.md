# vLLM Performance Optimization History: A Technical Survey

> **Research Date:** 2026-07-20  
> **Scope:** Major performance optimization techniques introduced by the vLLM project, with version/date attribution, performance benchmarks, and technical significance.  
> **Sources:** vLLM SOSP 2023 paper, official GitHub releases, vLLM blog, arXiv papers, and community benchmarking studies.

---

## Table of Contents

1. [Attention & Memory](#1-attention--memory)
   - 1.1 PagedAttention
   - 1.2 Attention Kernel Optimizations (FlashAttention, xFormers, Custom CUDA)
   - 1.3 Prefix Caching
2. [Batching & Scheduling](#2-batching--scheduling)
   - 2.1 Continuous Batching (Iteration-Level Scheduling)
   - 2.2 Chunked Prefill
   - 2.3 Multi-Step Scheduling & Async Output Processing
   - 2.4 Prefix-Aware Scheduling
3. [Decoding](#3-decoding)
   - 3.1 Speculative Decoding
   - 3.2 Dynamic Speculative Decoding
4. [Parallelism & Distributed Serving](#4-parallelism--distributed-serving)
   - 4.1 Tensor Parallelism
   - 4.2 Pipeline Parallelism
   - 4.3 Disaggregated Serving (Prefill/Decode Separation)
5. [Quantization](#5-quantization)
   - 5.1 Weight-Only Quantization (AWQ, GPTQ)
   - 5.2 Weight + Activation Quantization (FP8, INT8, SmoothQuant)
   - 5.3 KV Cache Quantization
6. [Summary: Impact Timeline](#6-summary-impact-timeline)

---

## 1. Attention & Memory

### 1.1 PagedAttention

| Attribute | Detail |
|-----------|--------|
| **What it is** | A virtual-memory-inspired KV cache manager that splits the KV cache into fixed-size **blocks** (default: 16 tokens) mapped through per-request **block tables**. Logical blocks are filled left-to-right; physical blocks are allocated on-demand from a GPU DRAM pool. |
| **When introduced** | **SOSP 2023** (paper: *Efficient Memory Management for Large Language Model Serving with PagedAttention*); shipped in vLLM **v0.1** (mid-2023). |
| **Performance impact** | - **Memory waste:** Traditional contiguous pre-allocation wastes **60-80%** of KV memory on padding/reserved-but-unused slots; PagedAttention reduces this to **<4%**.  <br>- **Throughput:** Up to **24x higher throughput** vs. HuggingFace Transformers on high-concurrency workloads (SOSP 2023 paper).  <br>- **Concurrent requests:** Enables **2-4x** more concurrent requests in the same VRAM budget.  <br>- **Overhead:** PagedAttention kernels are **20-26% slower** than non-paged FasterTransformer kernels at batch-size 1 due to block-table lookup and extra branches; they also add **7-13% more instructions** versus non-paged FlashAttention-2/FlashInfer kernels. The win comes from memory efficiency enabling larger batches, not raw single-stream latency. |
| **Why it matters** | Eliminated the single biggest bottleneck in LLM serving - KV cache fragmentation. Made vLLM the throughput leader and became the de-facto standard (adopted by TGI, TensorRT-LLM, SGLang, etc.). Copy-on-write block sharing also enables prefix caching. |

**Key Technical Details:**
- Block size is configurable via `--block-size` (default 16, sweet spot for most models; 32-64 can be better for >32K contexts, though larger blocks hurt L1 cache efficiency on decode).
- The block table is maintained in CPU memory; each entry records the physical block index and number of filled positions.
- Custom CUDA kernels: (1) fused reshape + block write, (2) fused block read + attention (adapted from FasterTransformer), (3) fused batched block copy for copy-on-write.

---

### 1.2 Attention Kernel Optimizations (FlashAttention, xFormers, Custom CUDA)

| Attribute | Detail |
|-----------|--------|
| **What it is** | vLLM integrates multiple attention backends and automatically selects the best one based on GPU architecture, model features, and data types. |
| **When introduced** | FlashAttention-2 backend matured in **v0.3.x-v0.4.x** (2023-2024); FlashAttention-3 support added for Hopper (H100) in **v0.5.x-v0.6.x** (2024). xFormers has been the fallback for older GPUs (Volta/Turing) since early versions. |
| **Performance impact** | On Llama 3.1 70B, 32K context, batch=1, H100: <br>- Vanilla PyTorch: **1820 ms** (OOMs at 32K) <br>- xFormers: **480 ms** / 18 GB <br>- FlashAttention-2 BF16: **220 ms** / 14 GB <br>- **FlashAttention-3 BF16: 130 ms** / 14 GB <br>- **FlashAttention-3 FP8: 65 ms** / 12 GB <br><br>vLLM auto-detects FA-3 on Hopper; can force FA-2 via `VLLM_ATTENTION_BACKEND=FLASH_ATTN`. |
| **Why it matters** | FlashAttention's IO-aware tiling keeps intermediate values in SRAM, reducing HBM traffic. FA-3 leverages Hopper-specific instructions (TMA, WGMMA) and FP8 tensor cores. For older GPUs (V100, T4), xFormers provides a functional fallback since FlashAttention-2/3 do not support SM < 80. |

**Backend Selection Logic (simplified):**
1. Hardware detection (CUDA / ROCm / XPU / CPU)
2. Model features (sliding window, head_dim, GQA/MLA, block-sparse)
3. Data type (`dtype`, `kv_cache_dtype`)
4. Fallback chain: FlashAttention-3 (Hopper) -> FlashAttention-2 -> FlashInfer -> xFormers -> SDPA

---

### 1.3 Prefix Caching

| Attribute | Detail |
|-----------|--------|
| **What it is** | Automatic reuse of KV cache blocks for identical prompt prefixes across requests. Implemented via **per-block hash tables** with LRU eviction. When a request's prefix matches cached blocks, the prefill phase skips those tokens entirely. |
| **When introduced** | Experimental in **v0.4.x**; stabilized in **v0.5.1** (mid-2024). v0.6.0 enabled **chunked prefill + prefix caching together** (PR #7753, Sep 2024). Enabled by default in modern versions. |
| **Performance impact** | - **TTFT reduction:** A 1,847-token fixed prefix with 94% hit rate saw TTFT p50 drop from **480 ms -> 110 ms** and p95 from **1.4 s -> 280 ms** (community benchmark, Qwen2.5-32B).  <br>- On a 10K-token prompt, second-request TTFT dropped from **4.3 s -> 0.6 s** (Qwen3-32B).  <br>- GPU prefill compute dropped by **38%** in high-hit-rate scenarios.  <br>- **Overhead:** Negligible in production; hash-table maintenance is CPU-side and block-granular. |
| **Why it matters** | Prefix caching is transformative for multi-turn chat, agent loops, RAG, and few-shot prompting where system prompts or retrieved contexts are repeated. It directly attacks the O(n^2) prefill cost of long shared prefixes. |

**Key Caveats:**
- Caching is **block-granular**: one differing token in the first block invalidates the entire suffix. Workloads with volatile fields early in the prompt (timestamps, UUIDs) can see near-0% hit rates unless those fields are moved to the prompt tail.
- Early implementations (BlockSpaceManagerV2) had regressions where prefix caching increased TTFT; V1 and later V2 fixes resolved this.
- Security: timing side-channel attacks have been demonstrated (GHSA-4qjh-9fv9-r85r) where an attacker measures TTFT differences to infer whether a prefix is cached.

---

## 2. Batching & Scheduling

### 2.1 Continuous Batching (Iteration-Level Scheduling)

| Attribute | Detail |
|-----------|--------|
| **What it is** | Also known as **in-flight batching**. The scheduler operates at **token-level granularity** rather than request-level. After every decode step, finished requests are removed and new requests are immediately admitted. This is vLLM's default scheduling mode. |
| **When introduced** | Present from **v0.1** (2023), building on ideas from Orca (iteration-level scheduling). |
| **Performance impact** | - GPU utilization: naive static batching achieves **30-40%**; continuous batching achieves **75-90%**.  <br>- **Throughput: +2-3x** vs. static batching on mixed workloads; up to **5-20x** over naive PyTorch loops at high QPS.  <br>- Tail latency tightens because short requests no longer wait for long ones in the same batch. |
| **Why it matters** | LLM output lengths vary wildly (5 tokens vs. 500 tokens). Static batching forces all requests to wait for the slowest, leaving GPU slots idle. Continuous batching keeps the GPU saturated by backfilling slots immediately. |

**Key Mechanisms:**
- Three queues: **Waiting**, **Running**, **Swapped** (preempted sequences evicted to CPU RAM).
- Preemption modes: `--preemption-mode recompute` (default, drops KV blocks and reruns prefill on restore) vs. `swap` (serializes blocks to CPU DRAM over PCIe).
- Scheduler flags: `--max-num-seqs` (default 1024), `--max-num-batched-tokens`.

---

### 2.2 Chunked Prefill

| Attribute | Detail |
|-----------|--------|
| **What it is** | Splits long **prefill** computations into smaller chunks that can be **batched alongside decode requests** in the same forward pass. This avoids head-of-line blocking where a single long prompt monopolizes the GPU and stalls all decoding. |
| **When introduced** | Introduced in **v0.4.x-v0.5.x** (2024); enabled by default in **vLLM V1** (v0.9.0+ / Jan 2025). In V1, it is the default scheduling policy whenever possible. |
| **Performance impact** | - **TTFT p95 reduction: 50-70%** on mixed workloads (Spheron benchmark, v0.18.0, Llama 3.3 70B FP8 on H100).  <br>- Better GPU utilization by co-locating compute-bound prefills with memory-bound decodes.  <br>- In V1, the scheduler prioritizes decode requests and automatically chunks prefills that exceed the `max_num_batched_tokens` budget. |
| **Why it matters** | Without chunking, a 10K-token prefill would block all decode requests for hundreds of milliseconds. Chunked prefill interleaves work so that decode latency (ITL) stays bounded while still making progress on long prompts. |

**Tuning Parameters:**
- `--max-num-batched-tokens`: smaller (e.g., 2048) favors ITL; larger (e.g., 16384-32768) favors TTFT and throughput.
- If disabled, `max_num_batched_tokens` must be > `max_model_len`.

---

### 2.3 Multi-Step Scheduling & Async Output Processing

| Attribute | Detail |
|-----------|--------|
| **What it is** | **Multi-step scheduling:** The scheduler prepares inputs once and runs the model for `n` consecutive steps (e.g., `--num-scheduler-steps 8`), reducing CPU scheduling overhead.  <br>**Async output processing:** Overlaps CPU-side output processing (stopping criteria, detokenization, string matching) with the next GPU forward pass. |
| **When introduced** | **v0.6.0** (Sep 2024). |
| **Performance impact** | - **v0.6.0 overall:** 2.7x higher throughput and 5x lower TPOT vs. earlier versions on Llama 8B.  <br>- Multi-step alone: **+28% throughput** on Llama 70B @ 4xH100.  <br>- Async output processing: **+12% throughput**, **-8.7% TPOT** on Llama 70B @ 4xH100. |
| **Why it matters** | As GPUs get faster (H100, B100), CPU overhead becomes the bottleneck. On Llama-8B/H100, GPU execution is only ~5 ms; CPU scheduling and output processing can dominate. These techniques amortize CPU work across multiple GPU steps. |

---

### 2.4 Prefix-Aware Scheduling

| Attribute | Detail |
|-----------|--------|
| **What it is** | Routing and scheduling decisions that account for prefix cache hit rates. For example, requests with high prefix overlap may be co-located on the same instance to maximize cache reuse, or the scheduler may preferentially admit cache-hit requests to reduce TTFT. |
| **When introduced** | **Production stack / v0.9.0+ era** (2024-2025), particularly in vLLM's Kubernetes production stack and prefix-aware routing layer. |
| **Performance impact** | Community reports show that moving volatile tokens to the end of prompts can increase hit rates from **0.3% -> 87%**, with corresponding TTFT p50 drops from **510 ms -> 145 ms**. |
| **Why it matters** | Prefix caching is only as good as the scheduling that exploits it. Prefix-aware routing turns cache locality into a cluster-level optimization, not just a single-node one. |

---

## 3. Decoding

### 3.1 Speculative Decoding

| Attribute | Detail |
|-----------|--------|
| **What it is** | Drafts multiple future tokens cheaply, then verifies them in parallel with the target model. If the draft is accepted, the model advances multiple tokens per forward pass. vLLM supports multiple speculation strategies: **draft model** (small LM), **EAGLE / EAGLE-3** (learned draft heads), **MTP** (multi-token prediction), **n-gram matching** (prompt lookup), **suffix decoding**, **PARD** (parallel draft), **MLP speculator**, and **hidden-state extraction**. |
| **When introduced** | Early speculative decoding (draft model) shipped in **v0.3.0** (2023). N-gram / prompt lookup decoding added in **v0.4.x** (2024). EAGLE and expanded methods landed in **v0.5.x-v0.6.x** (2024). Dynamic speculative decoding is an active research direction. |
| **Performance impact** | **Low QPS (latency-focused):**  <br>- Draft model (Llama3-70B, ShareGPT, QPS=1): **1.5x speedup**  <br>- N-gram (CNN/DailyMail summarization, QPS=1): **up to 2.8x speedup**  <br>- EAGLE-3 (Llama 3.3 70B, code/agentic tasks): **1.57-1.60x speedup**  <br>- Suffix decoding (SWE-Bench, repetitive code): **1.33-1.45x speedup**  <br><br>**High QPS (throughput-focused):** Can cause **1.4-1.8x slowdown** because extra draft compute becomes overhead when the system is already compute-bound. |
| **Why it matters** | Speculative decoding is one of the few techniques that directly reduces **time-to-output** without approximating the model. It is especially effective for memory-bound decode phases on large models and repetitive workloads (code, RAG). |

**Method Selection Guidance:**

| Method | Best For | Training-Free? |
|--------|----------|----------------|
| N-gram | Summarization, prompt-heavy Q&A | Yes |
| Suffix Decoding | Code generation, repetitive agentic loops | Yes |
| Draft Model | General use, when a small compatible model exists | No (needs separate model) |
| EAGLE / EAGLE-3 | General chat, large models (8B-70B+) | No (needs draft head training) |
| MTP | Models with native MTP support (e.g., some Qwen, DeepSeek) | Yes (if model already has it) |
| MLP Speculator | When compatible speculators are available | No |

---

### 3.2 Dynamic Speculative Decoding

| Attribute | Detail |
|-----------|--------|
| **What it is** | Automatically adjusts the number of speculative tokens based on system load and draft model acceptance rate. Shortens draft length when QPS is high to avoid compute overhead; lengthens it when QPS is low to maximize latency reduction. |
| **When introduced** | On the roadmap as of v0.5.x-v0.6.x (2024); references in vLLM docs and blog posts indicate active development. |
| **Performance impact** | Designed to eliminate the high-QPS slowdown of fixed speculative decoding, making it a net win across all load levels. |
| **Why it matters** | Static speculative decoding is a liability at high QPS. Dynamic adaptation makes it safe to leave speculative decoding enabled unconditionally. |

---

## 4. Parallelism & Distributed Serving

### 4.1 Tensor Parallelism (TP)

| Attribute | Detail |
|-----------|--------|
| **What it is** | Splits each transformer layer **across GPUs** within a node. Each GPU holds a shard of the weight matrices and performs a partial matmul/attention; results are synchronized via NCCL all-reduce after each layer. |
| **When introduced** | Present from **v0.1** (2023); uses NCCL for communication. |
| **Performance impact** | - Fits models larger than single-GPU memory (e.g., Llama 70B FP16 needs ~140 GB; requires 2xA100 80 GB with TP=2).  <br>- **Super-linear scaling:** Moving Llama 3.1 70B FP8 from 1xH100 to 2xH100 (TP=2) grew KV cache budget **13.9x** and total throughput **3.9x** because sharding weights frees disproportionate memory for larger batches.  <br>- Requires fast interconnect (NVLink/NVSwitch); on PCIe, all-reduce overhead can dominate. |
| **Why it matters** | TP is the default parallelism strategy for low-latency, multi-GPU serving within a single node. It reduces per-request latency by parallelizing compute. |

**Usage:** `vllm serve <model> --tensor-parallel-size N`

---

### 4.2 Pipeline Parallelism (PP)

| Attribute | Detail |
|-----------|--------|
| **What it is** | Splits the model **by depth** across GPUs. GPU 0 holds layers 0-N, GPU 1 holds layers N+1-2N, etc. Activations are passed between stages via point-to-point NCCL send/recv. vLLM uses **micro-batch scheduling** to fill pipeline bubbles (idle GPUs waiting for previous stages). |
| **When introduced** | Available in early versions; **async scheduling for PP** added experimentally in **v0.18.0** (Apr 2026) to improve throughput. |
| **Performance impact** | - Best for **multi-user API serving** on PCIe-connected GPUs (workstations, standard servers).  <br>- At high concurrency, pipeline bubbles are filled with queued requests, yielding high aggregate throughput.  <br>- Per-request latency is higher than TP because each token must traverse all stages sequentially.  <br>- Memory per GPU is reduced proportionally to the number of stages. |
| **Why it matters** | TP requires high-bandwidth all-reduce at every layer, which is expensive across nodes. PP only communicates once per stage boundary, making it viable across slower links and essential for 405B-class models that exceed single-node memory. |

**Usage:** `vllm serve <model> --pipeline-parallel-size N`  
**Combined:** `TP x PP` total GPUs (e.g., TP=8 within each node, PP=2 across nodes = 16 GPUs).

---

### 4.3 Disaggregated Serving (Prefill/Decode Separation)

| Attribute | Detail |
|-----------|--------|
| **What it is** | Physically separates the **prefill** phase (compute-bound, processes full prompt) and **decode** phase (memory-bound, generates one token at a time) onto different GPU instances. KV cache is transferred from prefill GPUs to decode GPUs via optimized interconnects (e.g., NIXL, LMCache, Mooncake connectors). |
| **When introduced** | Experimental support in **v0.7.3** (early 2025) via LMCache integration. Disaggregated prefill/decode is an active research area in the vLLM ecosystem (Mooncake, Dynamo, Arrow). |
| **Performance impact** | - Prefill and decode have opposing resource preferences: prefills want high compute, decodes want high memory bandwidth. Colocating them causes interference (long prefills stall decode ITL).  <br>- Disaggregation allows independent scaling and scheduling: prefill nodes can be optimized for throughput, decode nodes for low ITL.  <br>- KV transfer overhead is the critical path; optimized connectors (NIXL, Mooncake) aim to make this negligible on NVLink/InfiniBand. |
| **Why it matters** | As context lengths grow (100K+ tokens), the prefill phase can take seconds and starve decoding. Disaggregation is the architectural answer to keeping TTFT and ITL simultaneously bounded at extreme scale. |

---

## 5. Quantization

### 5.1 Weight-Only Quantization (AWQ, GPTQ)

| Attribute | Detail |
|-----------|--------|
| **What it is** | **AWQ** (Activation-Aware Weight Quantization): Identifies salient weight channels (approx. 1%) via activation magnitudes and applies scaling to protect them before quantization.  <br>**GPTQ** (General-purpose Post-Training Quantization): Layer-wise, calibration-data-driven quantization using approximate second-order information (Hessian). |
| **When introduced** | AWQ and GPTQ support have been present since **v0.2.x-v0.3.x** (2023). Marlin kernels for faster inference were added later. |
| **Performance impact** | - **AWQ/GPTQ W4A16:** 4x smaller weight footprint vs. FP16. Enables running Llama 70B on a single A100 80 GB (with AWQ).  <br>- **Speed:** Marlin kernels deliver near-FP16 throughput for W4A16 on Ampere+ GPUs.  <br>- **Quality:** AWQ generally shows less degradation than GPTQ at very low bit-widths (3-bit). GPTQ is more widely supported across model architectures. |
| **Why it matters** | Weight-only quantization is the easiest way to fit large models into limited VRAM. It is especially impactful for decode-phase memory bandwidth, since 4-bit weights mean 4x less HBM traffic. |

**Usage:** `vllm serve <model> --quantization awq` or `--quantization gptq`

---

### 5.2 Weight + Activation Quantization (FP8, INT8, SmoothQuant)

| Attribute | Detail |
|-----------|--------|
| **What it is** | **FP8:** 8-bit floating-point (E4M3 for weights/activations, E5M2 for gradients). Native on Hopper (H100/H200/B100) tensor cores.  <br>**INT8 (W8A8):** Both weights and activations in INT8.  <br>**SmoothQuant:** Applies a mathematically equivalent scaling transformation to migrate quantization difficulty from activations (which have outliers) to weights, enabling accurate W8A8 quantization. |
| **When introduced** | FP8 support matured in **v0.5.x-v0.6.x** (2024) with Cutlass FP8 GEMM integration. INT8 and SmoothQuant have been supported since early versions via CUTLASS/FBGEMM. llm-compressor (vLLM-project) is the modern quantization toolkit. |
| **Performance impact** | - **FP8 on H100:** ~2x higher Tensor Core throughput and 2x less HBM bandwidth vs. BF16. Benchmarks show **~33% tokens/s improvement** and **8.5% lower TTFT** vs. FP16 on H100.  <br>- **Quality:** FP8 quality loss is often within 0.1% of FP16/BF16 baseline because the floating-point exponent handles activation outliers naturally.  <br>- **SmoothQuant:** Enables W8A8 with minimal accuracy loss on models where naive INT8 fails due to activation outliers. |
| **Why it matters** | FP8 is becoming the **modern default for H100 serving**. It is simpler than INT8 (no outlier decomposition) and has native hardware support. SmoothQuant is the go-to for pre-Hopper GPUs needing W8A8. |

**Usage:** `vllm serve <model> --quantization fp8 --kv-cache-dtype fp8_e5m2`

---

### 5.3 KV Cache Quantization

| Attribute | Detail |
|-----------|--------|
| **What it is** | Quantizes the Key and Value tensors stored in the KV cache to lower precision (INT8, INT4, or FP8). Dequantization happens in SRAM during attention computation. |
| **When introduced** | Supported from **v0.5.x** onward via `--kv-cache-dtype` flag. FlashInfer FP8 KV cache backend added in **v0.6.0** (PR #7798). |
| **Performance impact** | - **INT8 KV cache:** 2x smaller cache -> 2x more concurrent sequences or 2x longer contexts.  <br>- **INT4 KV cache:** 4x smaller cache.  <br>- **FP8 KV cache:** 2x smaller with minimal quality loss on Hopper.  <br>- Overhead: small dequantization cost in the attention kernel, usually outweighed by the batch-size increase. |
| **Why it matters** | For long-context workloads (32K+), the KV cache can exceed model weights in size. Quantizing it is often the only way to serve large batches at long contexts. |

**Usage:** `vllm serve <model> --kv-cache-dtype fp8` (or `int8`, `int4`)

---

### vLLM Quantization Support Matrix (excerpt)

| Method | Bit Width | Weight | Activation | KV Cache | Hardware |
|--------|-----------|--------|------------|----------|----------|
| AWQ | W4A16 | Yes | No | No | Turing+ |
| GPTQ | W4A16 / W8A16 | Yes | No | No | Volta+ |
| Marlin | W4A16 | Yes | No | No | Ampere+ |
| FP8 | W8A8 | Yes | Yes | Yes | Hopper / Ada |
| INT8 (llm-compressor) | W8A8 | Yes | Yes | No | Turing+ |
| bitsandbytes | 4/8-bit | Yes | No | No | Volta+ |
| GGUF | Q4/Q5/Q8 | Yes | No | No | CPU/GPU |

---

## 6. Summary: Impact Timeline

| Era | Version | Key Optimizations | Approximate Date |
|-----|---------|-------------------|------------------|
| **Foundation** | v0.1 | PagedAttention, Continuous Batching, Tensor Parallelism | Jun 2023 |
| **Kernel & Flash** | v0.2-v0.3 | FlashAttention-2 integration, AWQ/GPTQ quantization, Draft Model Speculative Decoding | Late 2023 |
| **Scheduling & Memory** | v0.4-v0.5 | Prefix Caching (experimental), Chunked Prefill, N-gram Speculative Decoding, FP8 support | Mid 2024 |
| **Throughput Leap** | v0.6.0 | Multi-Step Scheduling, Async Output Processing, FlashInfer FP8 KV, Chunked Prefill + Prefix Caching together | Sep 2024 |
| **Scale & Ecosystem** | v0.7-v0.8 | Disaggregated serving (experimental, v0.7.3), EAGLE speculative decoding, expanded model support | Early 2025 |
| **V1 Re-Architecture** | v0.9.0+ / V1 | New EngineCore with unified scheduler, deeper multiprocessing, chunked prefill by default, prefix cache by default, spec decode + MTP in V1 | 2025 |
| **Production Hardening** | v0.10-v0.18 | Pipeline Parallel async scheduling, Mooncake/LMCache distributed KV connectors, prefix caching in hybrid models, expanded quantization (QuaRot, W8A8C8) | 2025-2026 |

---

## Key Takeaways

1. **PagedAttention** is the foundational innovation that made vLLM a throughput leader. It is not a latency optimization for single requests, but a memory-efficiency breakthrough that enables larger batches and higher concurrency.

2. **Continuous batching + chunked prefill** are the scheduling backbone. Together they keep GPU utilization at 75-90% on real workloads versus 30-40% for naive frameworks.

3. **Speculative decoding** offers 1.4-2.8x speedups for low-QPS, memory-bound scenarios, but can hurt at high QPS. Dynamic speculative decoding is the next evolution to make it universally safe.

4. **Prefix caching** can slash TTFT by 3-10x for repeated prompts, but requires careful prompt engineering (volatile tokens at the tail) to achieve high hit rates.

5. **FP8** is the quantization sweet spot for H100-class hardware: 2x speed/2x memory with near-zero quality loss. For older GPUs, AWQ/GPTQ weight-only quantization remains the practical choice.

6. **Disaggregated serving (PD separation)** is the architectural frontier for 2025-2026, aimed at decoupling the fundamentally conflicting resource needs of prefill (compute) and decode (memory bandwidth).

---

> **Disclaimer:** Exact version numbers and dates are based on release notes, GitHub tags, and community documentation as of July 2026. Some experimental features (e.g., disaggregated serving) have evolved rapidly; consult the latest vLLM documentation for current capabilities.
