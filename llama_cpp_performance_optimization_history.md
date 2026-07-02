# llama.cpp Performance Optimization History

**Research Date:** 2026-07-02  
**Project:** llama.cpp / ggml ecosystem (https://github.com/ggml-org/llama.cpp)  
**Original Author:** Georgi Gerganov (released March 10, 2023)

---

## 1. Quantization Evolution

### 1.1 Early Quantization (Q4_0, Q4_1, Q5_0, Q5_1, Q8_0)

| Technique | What It Is | Introduced | Performance Impact | Notes |
|-----------|------------|------------|-------------------|-------|
| **Q4_0** | 4-bit uniform quantization with a single block scale. 32 weights per block, each weight stored in 4 bits. | March 2023 (initial release) | Reduces 7B model from ~13GB → ~3.56GB. Inference on CPU at interactive speeds. | Baseline legacy format. Still supported but k-quants generally preferred. |
| **Q4_1** | 4-bit quantization with per-block minimum + scale. Slightly higher precision than Q4_0. | March 2023 | Similar size to Q4_0, slightly better PPL. | Legacy format. |
| **Q5_0 / Q5_1** | 5-bit variants with per-block scale (and min for Q5_1). | March 2023 | ~4.33GB for 7B. Better quality than 4-bit at ~25% size increase. | Legacy formats. |
| **Q8_0** | 8-bit integer quantization with per-block scale. | March 2023 | ~6.7GB for 7B. Near-FP16 quality (+0.0004 PPL on LLaMA-7B). | Useful for GPU inference where bandwidth matters less than precision. |
| **F16 / F32** | Half and single precision. | March 2023 | Baseline for quality comparisons. F16 ~13GB for 7B. | Used as source for quantization and for GPU offloading. |

**Why it matters:** The original Q4_0 quantization enabled the seminal achievement of llama.cpp: running LLaMA-7B on a MacBook Air M1 at ~15 tokens/sec, sparking the entire local-LLM movement.

### 1.2 K-Quants (Q2_K through Q6_K)

| Technique | What It Is | Introduced | Performance Impact | Notes |
|-----------|------------|------------|-------------------|-------|
| **Q2_K** | 2-bit k-quant with super-block quantization. | June 2023 (PR #1684, author: ikawrakow) | ~2.63GB for 7B (+0.67 PPL). | Aggressive compression. |
| **Q3_K_S / M / L** | 3-bit k-quants with Small/Medium/Large size/quality tradeoffs. | June 2023 | Q3_K_M ~3.07GB (+0.25 PPL). Q3_K_L ~3.35GB (+0.18 PPL). | Provides a quality/size dial. |
| **Q4_K_S / M** | 4-bit k-quants replacing legacy Q4_0/1. | June 2023 | Q4_K_M ~3.80GB (+0.053 PPL). | Widely recommended default. |
| **Q5_K_S / M** | 5-bit k-quants. | June 2023 | Q5_K_M ~4.45GB (+0.012 PPL). | Near-imperceptible quality loss. |
| **Q6_K** | 6-bit k-quant. | June 2023 | ~5.15GB (+0.0008 PPL). | Essentially indistinguishable from F16. |

**Technical details:** K-quants ("K" from the contributor ikawrakow/Kawrakow) use a **super-block** structure where multiple blocks share a common scale factor, reducing the overhead of quantization metadata. This allows more bits to be spent on weights rather than on per-block scales.

**Why it matters:** K-quants made 4-bit quantization practical for production use. Q4_K_M became the community standard for 7B models because it provided ~3.8GB model size with negligible perplexity increase (+0.05 PPL). Metal backend support for k-quants was added shortly after in PR #1807 (June 13, 2023).

### 1.3 IQ Quants (Importance-aware / Non-Linear Quantization)

| Technique | What It Is | Introduced | Performance Impact | Notes |
|-----------|------------|------------|-------------------|-------|
| **IQ2_XXS / IQ2_XS / IQ2_S / IQ2_M** | Importance-weighted 2-bit variants, ranging from ~2.06 to ~2.7 bits-per-weight (bpw). | 2024 (exact commit date unclear; confirmed by mid-2024) | 2.06–2.7 bpw. Enables running 70B models on ~24GB VRAM. | Non-linear codebook quantization. |
| **IQ3_XXS / IQ3_XS / IQ3_S / IQ3_M** | Importance-weighted 3-bit variants. | 2024 | 3.06–3.66 bpw. Better quality than Q3_K family. | Uses learned/importance-aware bit allocation. |
| **IQ4_XS / IQ4_NL** | 4-bit non-linear/importance-aware variants. | 2024 | ~4.25–4.50 bpw. | IQ4_NL is non-linear 4-bit. |
| **IQ1_S / IQ1_M** | Extreme 1-bit quantization (~1.56–1.75 bpw). | 2024 | Experimental. Very high quality loss but enables enormous models on consumer hardware. | For emergency "it runs at all" scenarios. |

**Why it matters:** IQ quants use **non-linear quantization grids** and **importance weighting** to allocate more precision to more important weights. This achieves better effective bits-per-weight than uniform quantization at the same storage cost. IQ quants are the key to running 70B+ models on single-consumer GPUs.

### 1.4 Importance Matrix (imatrix)

| Technique | What It Is | Introduced | Performance Impact | Notes |
|-----------|------------|------------|-------------------|-------|
| **imatrix** | An importance matrix computed from calibration data that guides quantization to spend more bits on more sensitive weights/tensors. | 2024 | Can improve low-bit quantization (IQ2/IQ3/Q2_K) quality dramatically. Without it, Q2_K_S is essentially unusable (+9.06 PPL). | Computed via `llama-imatrix` tool. |

**Why it matters:** The imatrix is the reason sub-3-bit quantization became usable. The `--imatrix` flag in the quantize tool uses calibration data to identify which tensors are most sensitive to quantization error, then adjusts quantization parameters accordingly. This is especially critical for IQ quants and Q2_K.

### 1.5 GGUF Format (Replacing GGML)

| Technique | What It Is | Introduced | Performance Impact | Notes |
|-----------|------------|------------|-------------------|-------|
| **GGUF** | Generic GGML Format — a self-contained binary format with extensible metadata, tokenizer, and aligned tensor data. | August 2023 | Enables memory-mapped loading (instant load), no external tokenizer files, and format stability. | Replaced GGML/GGMF/GGJT formats. |

**Why it matters:** GGUF made model distribution practical. Unlike the old GGML format which required separate tokenizer files and hardcoded architecture support, GGUF is self-contained and architecture-agnostic. It also supports memory-mapping (`mmap`), allowing models larger than RAM to load via OS paging. By August 2023, llama.cpp dropped GGML support entirely.

---

## 2. Kernel & Backend Evolution

### 2.1 CPU Optimizations

| Technique | What It Is | Introduced | Performance Impact | Notes |
|-----------|------------|------------|-------------------|-------|
| **ARM NEON** | SIMD instruction set optimization for Apple Silicon and ARM64 CPUs. | March 2023 (initial) | Core enabling optimization for M1/M2 Macs. | First-class citizen from day one. |
| **AVX / AVX2 / AVX512** | x86 SIMD extensions for parallel quantization dequantization and matmul. | March 2023+ | 2-8x speedup over scalar code on x86. | AVX512 support added incrementally. |
| **F16C / FMA** | x86 instructions for fast FP16 conversion and fused multiply-add. | March 2023 | Critical for FP16 inference on CPU. | Detected at compile time. |
| **LLAMAFILE / AARCH64_REPACK** | Specialized packing/repacking kernels for ARM64. | 2024 | Optimized memory layout for ARM CPU inference. | Listed in `system_info` output. |
| **AMX Support** | Intel Advanced Matrix Extensions for accelerated INT8/BF16 on Sapphire Rapids+. | 2024-2025 | Further matmul acceleration on newer Intel CPUs. | Mentioned in feature lists. |
| **BLAS / OpenBLAS / MKL** | External BLAS library integration for prompt processing (large batch matmul). | Early 2023 | Accelerates prompt processing (batch evaluation) significantly when batch > 32. | cuBLAS for CUDA, Accelerate for macOS, OpenBLAS/MKL for Linux. |

### 2.2 GPU Backends

| Technique | What It Is | Introduced | Performance Impact | Notes |
|-----------|------------|------------|-------------------|-------|
| **Metal (Apple GPU)** | Apple's Metal Performance Shaders backend for M1/M2/M3 GPUs. | March 2023 | Enables GPU inference on Apple Silicon. ~2-3x faster than CPU for token generation. | Native first-class support. Metal k-quants added June 2023. |
| **CUDA / cuBLAS** | NVIDIA GPU backend with custom CUDA kernels + cuBLAS for prompt processing. | April 2023 (PR #1065 improved dequantization on GPU) | Massive speedup for prompt processing. Custom kernels for quantized matmul. | `--gpu-layers` / `-ngl` flag. |
| **CUDA: MMVQ / DMMV** | Custom CUDA kernels for quantized matrix-vector multiply (MMVQ = mul_mat_vec_q). | 2023 | Enables fast quantized inference on CUDA without dequantizing first. | `LLAMA_CUDA_FORCE_DMMV` flag for tuning. |
| **Vulkan** | Cross-platform GPU backend using Vulkan compute shaders. | Late 2023 / Early 2024 (merged around Jan 2024, Discussion #5138) | Enables AMD/Intel GPU inference on Linux/Windows. Competitive with CUDA on some AMD cards. | Supports coopmat on RDNA3+. Supports integer dot products. |
| **SYCL (Intel GPUs)** | Intel oneAPI/DPC++ backend for Intel Arc / integrated / datacenter GPUs. | Early 2024 | Enables Intel GPU inference. | Added Q4_0 matmul optimization in 2025 (+21-87% on Intel GPUs). FlashAttention added ~March 2025. |
| **HIP / ROCm** | AMD GPU backend via HIP (CUDA-compatible API). | 2023 | AMD GPU support on Linux. | `LLAMA_HIPBLAS=1`. |
| **OpenCL** | Original GPU backend, largely superseded by Vulkan. | 2023 | Early GPU support. Still present but Vulkan is preferred. | `LLAMA_CLBLAST=1`. |
| **Kompute** | Vulkan-based compute backend (alternative implementation). | Early 2024 | Another Vulkan path, merged around same time as main Vulkan backend. | Part of the multi-backend wave. |
| **Hexagon / Qualcomm** | Qualcomm DSP/NPU backend for mobile. | 2025-2026 | Mobile/edge deployment on Snapdragon. | Mentioned in recent backend docs. |

**Backend Architecture Note:** Around late 2023, llama.cpp underwent a major refactor to introduce the **ggml-backend** abstraction. This decouples the compute graph (ggml) from the hardware-specific backends, allowing automatic scheduling of operations across CPU, GPU, and multiple devices.

---

## 3. Memory Optimizations

### 3.1 KV Cache Management

| Technique | What It Is | Introduced | Performance Impact | Notes |
|-----------|------------|------------|-------------------|-------|
| **KV Cache (basic)** | Stores attention Keys and Values from previous tokens to avoid recomputation during autoregressive generation. | March 2023 | Reduces generation from O(n²) per token to O(n) after prompt processing. | Fundamental to LLM inference. |
| **KV Cache Quantization** | Quantizes K/V cache to lower precision (Q8_0, Q4_0, etc.) at runtime. | 2024-2025 | Halves (Q8_0) or quarters (Q4_0) KV memory usage. | `--cache-type-k q8_0 --cache-type-v q8_0`. Requires FlashAttention for some backends. |
| **Flash Attention (`-fa`)** | Tiled attention computation that reduces HBM memory traffic and KV memory footprint. | 2024 | ~30-50% speedup at long context; reduces KV memory by ~50%. | Native llama.cpp implementation (not Dao Lab's flash-attn library). Works on CUDA, Metal, Vulkan, SYCL. |
| **KV Cache Defragmentation** | Reorganizes KV cache memory to eliminate fragmentation when sequences are evicted or resized. | 2023-2024 | Prevents gradual memory waste in long-running server sessions. | `--defrag-thold N` (default 0.1). |
| **KV Cache Offloading** | Offloads KV cache to GPU alongside model weights. | 2023 | Faster attention on GPU for long contexts. | `--no-kv-offload` to disable. |
| **Persistent KV Cache** | Reuses cached KV states across requests when prompt prefixes match (prefix caching). | 2024-2025 | Reduces Time-To-First-Token (TTFT) for repeated system prompts. | Used in production deployments. |
| **TurboQuant (KV)** | Advanced 3-bit KV cache quantization with reduced dequantization overhead. | 2025 (experimental) | Enables 262K+ context on consumer GPUs. | Community fork; may merge upstream. |
| **Per-Phase KV Quantization** | Proposed feature to use different KV precision for "thinking" vs "answer" phases in reasoning models. | 2026 (proposed) | Could reduce distortion by 58% for reasoning models. | Feature request #21679. |

### 3.2 Model Loading & Memory Management

| Technique | What It Is | Introduced | Performance Impact | Notes |
|-----------|------------|------------|-------------------|-------|
| **mmap** | Memory-mapped model loading. OS pages data from disk on demand. | Early 2023 | Instant model "load" regardless of file size. Enables models > RAM. | Default behavior. `--no-mmap` to disable. |
| **mlock** | Locks model pages in RAM to prevent OS swapping. | Early 2023 | Prevents inference stutter from page faults. | `--mlock` flag. |
| **NUMA Support** | Non-Uniform Memory Access optimizations for multi-socket servers. | June 2023 | Improves performance on AMD EPYC / Intel Xeon multi-socket systems. | `--numa distribute/isolate/numactl` |
| **Context Window Scaling** | RoPE scaling (linear, NTK-aware, YaRN) to extend context beyond training length. | 2023-2024 | Enables 2x-8x context extension without retraining. | `--rope-scale`, `--rope-freq-base`. |

---

## 4. Parallelism & Scheduling

### 4.1 Multi-GPU & Hybrid Execution

| Technique | What It Is | Introduced | Performance Impact | Notes |
|-----------|------------|------------|-------------------|-------|
| **Layer Splitting (`--tensor-split`)** | Distributes model layers across multiple GPUs by proportion. | 2023 | Enables running models larger than single-GPU VRAM. | `18,17` syntax. |
| **Row Splitting** | Alternative tensor parallelism that splits weight matrices by rows. | 2023 | Can help on older GPUs with limited VRAM. | `--split-mode row` vs `layer`. |
| **CPU+GPU Hybrid** | Automatic scheduling of layers between CPU RAM and GPU VRAM. | 2023 | Core feature: offload whatever fits to GPU, rest stays on CPU. | `--n-gpu-layers` / `-ngl`. |
| **Multi-GPU Peer Access** | NVLink/PCIe P2P access for cross-GPU tensor communication. | 2023 | Faster multi-GPU for batch sizes above threshold. | `LLAMA_CUDA_PEER_MAX_BATCH_SIZE`. |
| **Backend Scheduling (`ggml_backend_sched`)** | Automatic graph splitting and scheduling across heterogeneous backends. | Late 2023 | Transparently handles CPU+GPU+multiple GPUs. | The core of modern llama.cpp backend architecture. |

### 4.2 Threading & Batching

| Technique | What It Is | Introduced | Performance Impact | Notes |
|-----------|------------|------------|-------------------|-------|
| **Thread Tuning (`-t`, `--threads-batch`)** | Separate thread counts for generation vs prompt processing. | 2023 | Prompt processing benefits from more threads; generation often doesn't. | `--threads` for generation, `--threads-batch` for prompt eval. |
| **Batch Processing (`-b`, `-ub`)** | Evaluates multiple tokens simultaneously during prompt processing. | March 2023 | Critical for fast prompt ingestion. | `-b 512` or `-b 2048` common. |
| **Ubatch (`-ub`)** | Micro-batch size for actual compute dispatch. | 2024 | Fine-grained control over GPU dispatch granularity. | `-ub 512` for throughput. |
| **Parallel Sequences (`-np`)** | Multiple independent sequences sharing the same model weights. | 2024 | Enables batched inference and multi-user serving. | Server feature. |

### 4.3 Speculative Decoding & Lookahead

| Technique | What It Is | Introduced | Performance Impact | Notes |
|-----------|------------|------------|-------------------|-------|
| **Draft Model Speculative Decoding** | Uses a smaller draft model to predict future tokens, then verifies them with the main model in parallel. | 2023-2024 | 1.5x–3x speedup when draft acceptance is high. | `--draft` / `-md` flags. |
| **Multi-Token Prediction (MTP)** | Built-in speculative heads within the model itself (e.g., Qwen3.6). No separate draft model needed. | 2025-2026 | ~1.71x speedup observed (38→65 t/s on RTX 3090). | `--spec-type mtp --spec-draft-n-max 3`. |
| **N-gram Cache Speculation** | Reuses token sequences from the context or across requests to draft tokens. | 2024 | Lightweight, no extra model. Good for repetitive text. | `--spec-type ngram-simple`, `ngram-map-k`, `ngram-mod`. |
| **EAGLE-3 / Draft-Eagle** | Advanced draft model that reads target model hidden states for better draft quality. | 2025 | Higher acceptance rate than simple draft models. | `--spec-type draft-eagle3`. |
| **DFlash Diffusion Drafting** | Block-diffusion draft model that emits multiple tokens per step. | 2025 | Experimental. | `--spec-type draft-dflash`. |
| **GPU Sampling** | Moves sampling/logits processing to GPU instead of CPU round-trip. | 2025 (PR #17004) | Reduces CPU-GPU synchronization overhead. | Improves throughput at small batch sizes. |

**Why speculative decoding matters:** LLM inference is memory-bandwidth bound during token generation. Speculative decoding reduces the number of memory-bound forward passes by verifying multiple draft tokens in a single batch, which is compute-efficient.

---

## 5. Recent Innovations (2024–2026)

### 5.1 FlashAttention-like Optimizations in llama.cpp

- **What it is:** llama.cpp implements its own FlashAttention-style kernels (not the original CUDA-only FlashAttention library). These use tiling to keep the attention computation in SRAM/shared memory, reducing HBM traffic.
- **When introduced:** Available by 2024, with ongoing improvements across backends. `--flash-attn` / `-fa` flag.
- **Performance impact:** ~30-50% speedup at 4K+ context; ~50% KV memory reduction. On some backends (e.g., Polaris/RDNA without int8 acceleration), the speedup is primarily memory savings rather than raw throughput.
- **Why it matters:** Enables long-context inference on consumer GPUs without quadratic memory blowup. Effectively required for KV cache quantization on some backends.

### 5.2 LoRA Adapters

- **What it is:** Low-Rank Adapter support allows applying fine-tuned adapters on top of a base model without merging weights. Formula: `W' = W + (alpha/r) * scale * B @ A`.
- **When introduced:** API `llama_model_apply_lora_from_file()` present by April 2023 (visible in `llama.h`). Python bindings (llama-cpp-python) followed shortly after.
- **Performance impact:** Near-zero inference overhead if merged at load time. Dynamic adapter switching adds small overhead.
- **Why it matters:** Enables serving multiple specialized personas from a single base model, reducing memory footprint.

### 5.3 Grammar-Based Sampling (GBNF)

- **What it is:** GBNF (Georgi Gerganov BNF) is a context-free grammar format that constrains model output to valid syntax (JSON, SQL, etc.). It filters the token probability distribution at each step.
- **When introduced:** 2023 (Grant Slatton's commit referenced; integrated by ~mid-2023).
- **Performance impact:** Minimal per-step overhead when implemented efficiently. GPU-accelerated grammar FSM initialization and masking was later optimized.
- **Why it matters:** Makes LLMs reliable for structured outputs (APIs, code generation, config files) without post-processing. Integrated with `--grammar` and `--grammar-file` flags.
- **Recent:** LLGuidance (Rust-based) integration provides ~50μs token mask computation for JSON Schema.

### 5.4 Multi-Modal (LLaVA, CLIP, Qwen2-VL)

- **What it is:** Support for vision-language models. A CLIP ViT encoder processes images into embeddings that are fed into the LLM via a projector (`mmproj` file).
- **When introduced:** LLaVA support merged in PR #3436 (October 2023). MiniCPM, Qwen2-VL, and others followed in 2024.
- **Performance impact:** Image processing adds a one-time prefill cost. The rest of generation proceeds at normal LLM speed.
- **Why it matters:** Extends llama.cpp from text-only to visual understanding, enabling local image captioning and visual QA.

### 5.5 MoE (Mixture of Experts) Support

- **What it is:** Sparse routing for MoE models (Mixtral, Qwen-MoE, DeepSeek-V3). Only a subset of experts are activated per token.
- **When introduced:** 2024 (Vulkan MoE support merged in 2024; CUDA/Metal followed).
- **Performance impact:** Reduces effective FLOPs per token. On Vulkan, `mul_mat_id` kernels were added for sparse routing. Fused MoE kernels added to SYCL in 2025.
- **Why it matters:** MoE models (e.g., DeepSeek-V3 671B) are the frontier of open-source LLMs. Running them locally requires efficient sparse routing.

### 5.6 Mamba / SSM / Hybrid Architectures

- **What it is:** Support for state-space models (Mamba, Mamba2) and hybrid Transformer+SSM architectures.
- **When introduced:** 2025-2026. `SSM_SCAN`, `SSM_CONV`, `GATED_DELTA_NET` operations added to CUDA/WebGPU/Vulkan backends. SYCL support lagged behind.
- **Performance impact:** SSMs have linear-time sequence modeling, avoiding the quadratic attention cost. This is transformative for ultra-long context.
- **Why it matters:** Hybrid architectures represent the next generation beyond pure Transformers. llama.cpp's backend abstraction allows these ops to be scheduled across hardware.

---

## 6. Summary: The llama.cpp Optimization Philosophy

1. **Start on CPU, optimize everywhere:** llama.cpp was born from the idea that LLMs don't require GPUs. Every optimization was first made to work on CPU (NEON, AVX), then ported to GPU backends.

2. **Quantization as a first-class concern:** Unlike frameworks that bolt quantization on later, llama.cpp treats quantization as fundamental. The quantize tool is a core binary, and new quantization methods are integrated immediately into all backends.

3. **Memory bandwidth is the bottleneck:** Most optimizations (quantization, FlashAttention, KV cache compression, speculative decoding) target memory bandwidth, not compute. This is the correct optimization target for LLM inference.

4. **Hardware portability over peak performance:** llama.cpp prioritizes running everywhere (Raspberry Pi, smartphone, MacBook, Intel Arc, AMD, NVIDIA) rather than being the absolute fastest on one platform. The ggml-backend abstraction enables this.

5. **Community-driven:** Many of the most impactful contributions came from individual contributors (e.g., k-quants by ikawrakow, Vulkan by 0cc4m, SYCL by abhilash1910, grammar by grantslatton). The project is a case study in open-source optimization.

---

## Sources & References

- Primary source: https://github.com/ggml-org/llama.cpp (releases, PRs, discussions)
- Key PRs referenced: #1684 (k-quants), #1807 (Metal k-quants), #1065 (CUDA dequantize), #3436 (LLaVA), #22673 (MTP), #2059 (Vulkan), #2690 (SYCL)
- Discussion #5138: "Incoming backends: Vulkan, Kompute, SYCL"
- `docs/backend/SYCL.md` — Intel SYCL backend timeline
- `docs/speculative.md` — Speculative decoding documentation
- ArXiv: "Which Quantization Should I Use? A Unified Evaluation of llama.cpp Quantization" (2026)
- KoboldCpp wiki, LM Studio blog, and community benchmarks from r/LocalLLaMA
- Various GitHub issues documenting FlashAttention, KV quantization, and MoE support

---

*Note: Some specific dates are approximate, inferred from commit discussions and release notes. Where exact dates could not be verified, they are marked with approximate ranges. The project moves extremely fast; features mentioned as "experimental" in 2025 may be stable by the time of reading.*
