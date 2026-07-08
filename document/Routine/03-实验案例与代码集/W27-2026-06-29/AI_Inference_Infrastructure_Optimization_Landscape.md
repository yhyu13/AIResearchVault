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

# 1. Attention Optimizations

## 1.1 FlashAttention Family (v1 -> v2 -> v3 -> v4)

### FlashAttention v1 (2022)
- **What it is:** IO-aware exact attention algorithm that avoids materializing the N*N attention matrix in HBM by using tiling + softmax rescaling + recomputation. All operations (QK^T, softmax, PV) fused into a single kernel.
- **Project:** `Dao-AILab/flash-attention` (Stanford / Together AI)
- **Performance impact:** 2-4x faster attention, up to 10x lower memory vs. standard PyTorch attention.
- **Key insight:** The attention operation is memory-bound, not compute-bound. By keeping tiles in SRAM (fast on-chip cache) and avoiding HBM round-trips, the algorithm becomes IO-bound rather than memory-capacity-bound.
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
- **Note:** FA-3 also has custom adaptations for AMD MI300X (via Composable Kernel) with XCD-aware scheduling and LDS layout optimizations, achieving ~2x speedup over Triton baselines on MI300X.
- **Source:** Shah et al., arXiv:2407.08608 (also PyTorch blog, Jul 2024).

### FlashAttention v4 (2026)
- **What it is:** Targets Hopper and Blackwell (B200). Written in CuTeDSL. Key features: fully asynchronous MMA, larger tiles, software-emulated exponentials, conditional softmax rescaling, tensor memory, and 2-CTA MMA.
- **Project:** `flash-attn-4`
- **Performance impact:** Up to 1.3x faster than cuDNN 9.13, up to 2.7x faster than Triton; **1613 TFLOPS** (71% utilization) on B200 BF16 benchmarks.
- **Key insight:** On Blackwell, Tensor Cores scaled much faster than shared memory bandwidth and SFUs. The bottleneck shifted, requiring larger tiles and software-emulated exponentials to keep Tensor Cores fed.
- **Source:** BentoML / LLM Inference Handbook, 2025.

---

# 2. Quantization

## 2.1 GPTQ (General-purpose Post-Training Quantization)
- **What it is:** Layer-wise post-training quantization using calibration data and approximate second-order information (OBS-style weight updates). Typically 4-bit weights with FP16/FP8 activations.
- **Project:** `AutoGPTQ`, `GPTQ-for-LLaMA`, `ExLlama`, `ExLlamaV2`
- **Performance impact:** 4-bit models retain ~94-96% of FP16 quality (perplexity). ~3x memory reduction. Inference speed fast with optimized kernels (e.g., Marlin).
- **Key insight:** Quantization-aware weight updates minimize the error introduced by rounding; the method is one-shot and requires ~128-256 calibration samples.
- **Trade-offs:** Calibration time 1-4 hours for 7B on A100. Quality degradation at 2-3-bit.
- **Source:** Frantar et al., ICLR 2023.

## 2.2 AWQ (Activation-aware Weight Quantization)
- **What it is:** Identifies and protects "salient" weights (those with large activation magnitudes) during quantization. Quantizes the rest aggressively.
- **Project:** `mit-han-lab/llm-awq` (MLSys 2024 Best Paper)
- **Performance impact:** W4A16 quantization retains ~96-98% of FP16 quality; 1-3% better than GPTQ at same bit-width. MMLU scores 0.5-1.5% higher than GPTQ.
- **Key insight:** Not all weights are equally important; protecting those with high activation impact preserves model quality per bit better than uniform quantization.
- **Deployment:** vLLM, TGI both have optimized AWQ kernels. Marlin kernel backend is recommended for production.
- **Source:** Lin et al., MLSys 2024.

## 2.3 Marlin Kernel
- **What it is:** Optimized inference kernel for 4-bit quantized models (GPTQ/AWQ). Achieves near-FP16 latency on modern GPUs by using INT4 tensor core instructions and specialized memory layouts.
- **Project:** `IST-DASLab/marlin`
- **Performance impact:** Near-FP16 throughput for W4A16 models; the fastest 4-bit inference kernel on NVIDIA GPUs as of 2024-2025.
- **Key insight:** Memory bandwidth reduction from 4-bit weights dominates at batch=1; at higher batch sizes, compute throughput matters, and Marlin's tensor core utilization is critical.
- **Source:** Frantar et al., 2024.

## 2.4 FP8 / FP4 (TensorRT-LLM, NVIDIA Hopper/Blackwell)
- **What it is:** Native 8-bit or 4-bit floating point formats on H100 and B200. TensorRT-LLM automatically converts weights and activations to FP8 with minimal accuracy loss.
- **Project:** NVIDIA TensorRT-LLM
- **Performance impact:** FP8 doubles performance and halves memory vs. FP16/BF16 with minimal accuracy loss. FP4 on B200 further reduces memory.
- **Key insight:** FP8 uses E4M3/E5M2 formats with per-tensor or per-channel scaling. The hardware-native support on Hopper/Blackwell avoids the overhead of INT8/INT4 emulation.
- **Comparative note:** TensorRT-LLM's FP8 path is more mature than vLLM's FP8 support; vLLM relies on Triton kernels which may not yet achieve the same Tensor Core utilization.
- **Source:** NVIDIA TensorRT-LLM docs, 2024.

## 2.5 GGUF (llama.cpp ecosystem)
- **What it is:** Universal quantization format for CPU+GPU+Apple Silicon inference. Supports various bit-widths (Q4_K_M, Q5_K_M, Q8_0) and mixed quantization strategies.
- **Project:** `ggerganov/llama.cpp`
- **Performance impact:** Q4_K_M offers ~95-98% quality retention; works on CPU with acceptable speed for small models. On GPU, Metal (Apple Silicon) and CUDA backends are available.
- **Key insight:** CPU inference is viable for small models (7B-13B) thanks to ARM NEON and AVX2 optimizations. The ecosystem (Ollama, LM Studio, Jan) is the widest.
- **Trade-off:** CPU inference is orders of magnitude slower than GPU for large batches or long contexts.
- **Source:** localaimaster.com, 2026; llama.cpp project docs.

---

# 3. Scheduling & Memory Management

## 3.1 Continuous / In-Flight Batching
- **What it is:** Instead of static batching (waiting for all sequences to finish), the scheduler dynamically adds/removes sequences from the GPU batch at every iteration. New requests can join mid-generation.
- **Projects:** vLLM (continuous batching), TensorRT-LLM (in-flight batching), TGI, DeepSpeed-MII, SGLang
- **Performance impact:** Dramatically improves GPU utilization and throughput (2-5x over static batching) by eliminating idle time waiting for slow sequences to finish.
- **Key insight:** The critical parameter is the **arrival window**: widening the window improves throughput but increases tail latency. Production deployments must tune this based on SLO traces.
- **Comparative note:** TensorRT-LLM's in-flight batching is equivalent to vLLM's continuous batching but with tighter engine integration. SGLang adds RadixAttention for prefix caching on top.
- **Source:** vLLM docs; Skywork.ai blog, 2025; quant67.com, 2026.

## 3.2 PagedAttention / Paged KV Cache
- **What it is:** Manages KV cache as fixed-size blocks (pages), similar to OS virtual memory. Avoids memory fragmentation and enables dynamic memory allocation and prefix sharing.
- **Projects:** vLLM (original), TensorRT-LLM, SGLang (RadixAttention), TGI v3, LMDeploy
- **Performance impact:** 2-4x higher throughput in multi-turn conversations; enables serving 2-4x more concurrent requests on the same GPU memory budget.
- **Key insight:** The KV cache is the dominant memory consumer in LLM serving. Paging eliminates pre-allocation overhead and allows memory sharing across requests with common prefixes (e.g., system prompts).
- **Page size tuning:** Typical page sizes are 16-32 KB. Larger pages reduce metadata overhead but increase internal fragmentation; smaller pages improve sharing granularity.
- **Source:** Kwon et al., SOSP 2023.

## 3.3 Prefix Caching & RadixAttention (SGLang)
- **What it is:** SGLang's RadixAttention uses a radix tree to cache and reuse KV states across requests with matching prefixes. This is particularly effective for multi-turn conversations, RAG, and agent workflows where system prompts and context are reused.
- **Project:** `lm-sys/SGLang`
- **Performance impact:** Up to 10x latency reduction for requests with high prefix overlap (e.g., shared system prompts, repeated queries).
- **Key insight:** Unlike vLLM's automatic prefix caching, RadixAttention finds the longest matching prefix and can handle partial matches. This is critical for agent/tool-call workflows where conversation prefixes diverge and then reconverge.
- **Source:** Zheng et al., 2024; quant67.com, 2026.

---

# 4. Speculative Decoding

## 4.1 Classic Speculative Decoding (Leviathan et al. 2022, Chen et al. 2023)
- **What it is:** A small "draft" model generates K candidate tokens; the large "target" model verifies them in parallel in one forward pass. Accepted tokens are emitted; rejected tokens trigger a single target-model forward pass.
- **Projects:** Implemented in TensorRT-LLM, vLLM, TGI, and various standalone frameworks.
- **Performance impact:** Theoretically up to 2-3x speedup. In practice, NVIDIA reports up to **3.6x** with well-chosen draft models. Speedup depends heavily on draft-target agreement rate.
- **Key insight:** The speedup is limited by the draft model's quality and the overhead of running it. If the draft model is too small, acceptance rate drops; if too large, overhead dominates.
- **Source:** Leviathan et al., ICML 2022; Chen et al., 2023; NVIDIA TensorRT-LLM docs, 2025.

## 4.2 Medusa (Multiple Decoding Heads)
- **What it is:** Adds extra decoding heads on top of the target model's final hidden states. These heads predict multiple future tokens in parallel. No separate draft model needed.
- **Project:** `FasterDecoding/Medusa` (arXiv:2401.10774)
- **Performance impact:** Medusa-1 (frozen backbone + fine-tuned heads): **2.2x speedup** lossless. Medusa-2 (joint fine-tuning): **2.3-3.6x speedup**.
- **Key insight:** Avoids the draft model overhead entirely. Uses tree-based attention to verify multiple candidate continuations simultaneously. Training is self-distillation from the target model's own outputs.
- **Trade-off:** Requires fine-tuning the heads; not zero-shot compatible with any model without training.
- **Source:** Cai et al., arXiv:2401.10774; CSDN blog, 2024.

## 4.3 EAGLE (Extrapolative Speculative Sampling)
- **What it is:** Uses a lightweight autoregressive head on the target model's hidden states (feature-level drafting). Builds an instance-adaptive tree of candidates and verifies them in one batched forward pass.
- **Project:** `EAGLE-ml` (ICML 2024)
- **Performance impact:** Generally higher acceptance rates than Medusa because it drafts at the feature level rather than the token level. Benchmarks on Spec-Bench show it consistently outperforms Medusa and classic speculative decoding on Vicuna-7B.
- **Key insight:** Feature-level drafting captures the target model's internal state better than token-level heads, leading to higher-quality speculation and better tree verification efficiency.
- **Source:** Li et al., ICML 2024; Spec-Bench leaderboard, 2024.

## 4.4 Lookahead Decoding
- **What it is:** Training-free speculative decoding using N-gram matching from the prompt and generated text. Uses Jacobi iteration to generate multiple candidate tokens.
- **Project:** `hao-ai-lab/lookahead-decoding`
- **Performance impact:** Speedup depends on N-gram repetition in the text. Good for repetitive or structured outputs (code, JSON). Less effective for free-form creative writing.
- **Key insight:** No model training required. Works out-of-the-box on any autoregressive model. Best for tasks with high lexical overlap or template-based generation.
- **Source:** Fu et al., ICML 2024; TechRxiv survey, 2025.

## 4.5 REST (Retrieval-Based Speculative Decoding)
- **What it is:** Retrieves draft tokens from a datastore (e.g., prefix matching against past generations or a document corpus). Uses a DraftRetriever module.
- **Project:** `FasterDecoding/REST` (NAACL 2024)
- **Performance impact:** Highly variable; can be very effective for RAG and code-completion where the draft can be retrieved from a large context. Spec-Bench integration shows it is competitive with other methods.
- **Key insight:** Shifts the drafting burden from a model to a retrieval system. Excellent for long-document QA and code completion where the answer often appears verbatim in the context.
- **Source:** He et al., NAACL 2024; Spec-Bench docs.

## 4.6 Spec-Bench Unified Benchmark
- **What it is:** A comprehensive benchmark and evaluation platform for speculative decoding methods. Evaluates EAGLE, Hydra, Medusa, Speculative Sampling, Prompt Lookup Decoding, REST, Lookahead Decoding, and SPACE on the same device and environment.
- **Project:** `hemingkx/Spec-Bench` (ACL 2024 Findings)
- **Key insight:** Standardized evaluation is critical because speedup is highly dependent on model, task, and hardware. Spec-Bench provides fair comparisons under controlled conditions.
- **Source:** Xu et al., ACL 2024 Findings; https://github.com/hemingkx/Spec-Bench

---

# 5. Hardware-Level Trends

## 5.1 NVIDIA H100 / H200 / B200 Architecture Evolution
- **H100 (Hopper, 2023):** Fourth-gen Tensor Cores, TMA (Tensor Memory Accelerator), WGMMA instructions, FP8 support. HBM3 bandwidth: 3.35 TB/s (SXM). 80GB HBM3.
- **H200 (2024):** Same compute as H100 but with **141GB HBM3e** and **4.8 TB/s** bandwidth. Specifically designed for inference workloads where KV cache size and memory bandwidth are the bottleneck.
- **B200 (Blackwell, 2024):** Fifth-gen Tensor Cores. FP4 support. 2.25 PFLOPS FP16 (dense). 8 TB/s HBM3e bandwidth. Asymmetric scaling: Tensor Cores scaled much faster than shared memory bandwidth and SFUs. This shifts the bottleneck to non-matmul operations (softmax, elementwise).
- **Key insight:** For **memory-bandwidth-bound** workloads (long-context Transformers, large batch decode), H200's bandwidth premium is worth the price. For **compute-bound** workloads (SSMs like Mamba, small-batch prefill), H100's price-to-performance ratio is better because the extra bandwidth goes unused.
- **Source:** NVIDIA H100 Datasheet; NanoFlow (arXiv:2408.12757); Spheron blog, 2026.

## 5.2 AMD MI300X
- **What it is:** AMD's flagship AI accelerator. 8 XCD chiplets, 304 CUs, 192GB HBM3, 5.3 TB/s HBM bandwidth, 896 GB/s Infinity Fabric.
- **Key specs:** 2.4x HBM capacity vs. H100 (80GB). 1.6x HBM bandwidth vs. H100. Memory bandwidth to compute ratio is favorable for memory-bound workloads.
- **Performance impact:** On FlashAttention-style kernels, MI300X achieves competitive performance with H100 when kernels are optimized for its multi-chiplet NUMA architecture (e.g., XCD-aware scheduling, explicit VMEM/MFMA interleaving). However, the lack of TMA and warp-specialized async execution means some Hopper-specific optimizations cannot be directly ported.
- **Key insight:** MI300X's multi-chiplet design exposes NUMA effects to software. The L2 cache is per-die, not unified. Swizzled Head-first Mapping and other NUMA-aware scheduling strategies are essential for high L2 hit rates (80-97% reported).
- **Source:** AMD MI300X specs; arXiv:2511.02132 (NUMA-aware scheduling); 与非网, 2024.

## 5.3 Memory Bandwidth vs. Compute Bottlenecks
- **Transformer decode:** Memory-bandwidth-bound. Each iteration loads all model weights and KV cache. The FLOP/B ratio is low (~200 FLOP/B for A100, ~295 for H100).
- **Transformer prefill:** Compute-bound. The large matmuls in the prompt processing phase saturate Tensor Cores.
- **SSM (Mamba) decode:** More compute-bound than Transformers because the state update is a fixed-size matrix multiplication (state size is constant, independent of sequence length). The bottleneck shifts from memory bandwidth to FLOP throughput at long context.
- **Roofline model insight:** For decode, the achievable throughput is `MemBW / (model_size_bytes + KV_cache_bytes_per_token)`. This is why quantization (reducing weight size) and KV cache compression (e.g., KV cache quantization, paging) are so effective for decode throughput.
- **Source:** NanoFlow (arXiv:2408.12757); Table 1 in NanoFlow paper.

---

# 6. Communication & Disaggregated Serving

## 6.1 NCCL and Custom Collectives
- **NCCL (NVIDIA Collective Communications Library):** Standard for multi-GPU all-reduce, all-gather, reduce-scatter, all-to-all. Used by all major frameworks (vLLM, TensorRT-LLM, DeepSpeed, SGLang).
- **All-to-all in MoE:** Expert parallelism requires token shuffling between GPUs via all-to-all. This is the dominant communication cost in MoE inference. The cost scales with `batch_size * hidden_dim * num_experts_activated`.
- **Optimization:** Overlapping communication with compute (e.g., via NCCL's point-to-point or custom RDMA) is critical. FlowKV and others optimize the KV cache structure to reduce the number of NCCL calls.
- **Source:** vLLM MoE docs; Sem-MoE paper, 2026.

## 6.2 Disaggregated Serving (Prefill-Decode Separation)
- **What it is:** Separates the prefill phase (prompt processing, compute-bound) from the decode phase (token generation, memory-bandwidth-bound) onto different GPU pools. The KV cache is transferred from prefill nodes to decode nodes via high-speed interconnect (RDMA, NVLink, or custom transfer engines).
- **Projects:** Mooncake (Kimi / Moonshot AI), DistServe (UCSD), Splitwise (Microsoft), FlowKV, vLLM disaggregated serving, TensorRT-LLM (Beta)
- **Performance impact:**
  - DistServe: 4-8x throughput improvement at same SLO.
  - Sarathi-Serve: 2.6-5.6x improvement in throughput-latency tradeoffs over vLLM.
  - FlowKV: Optimizes KV cache structure to reduce NCCL communication overhead; eliminates transfer time relative to total request latency.
- **Key insight:** Prefill and decode have opposite resource preferences. Prefill likes large batches and high compute; decode likes small, consistent steps and high memory bandwidth. Mixing them causes interference: a large prefill job stalls decode jobs, causing inter-token latency (ITL) jitter.
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
