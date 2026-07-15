# AI Infrastructure Milestone & Trunk Papers (2023 – Mid-2026)

> **Curated:** 2026-07-15  
> **Scope:** Foundational, widely-cited, and direction-defining papers in AI infrastructure — systems, compilers, training frameworks, inference engines, and agent runtimes. Focus on works that opened new sub-fields or became de facto standards. Minor incremental works are excluded.  
> **Venue Coverage:** NeurIPS, ICML, ICLR, SOSP, OSDI, MLSys, ASPLOS, ISCA, SIGGRAPH, EuroSys, COLM, ACL, EMNLP, arXiv (when industry-adopted).

---

## Table of Contents

1. [Distributed Training & Parallelism](#1-distributed-training--parallelism)
2. [Memory-Efficient Attention & Kernels](#2-memory-efficient-attention--kernels)
3. [LLM Inference Serving Engines](#3-llm-inference-serving-engines)
4. [Compiler & Kernel Infrastructure](#4-compiler--kernel-infrastructure)
5. [Quantization & Model Compression](#5-quantization--model-compression)
6. [Mixture-of-Experts (MoE) Infrastructure](#6-mixture-of-experts-moe-infrastructure)
7. [Scheduling & Cluster Management](#7-scheduling--cluster-management)
8. [Agent Infrastructure & OS Abstractions](#8-agent-infrastructure--os-abstractions)
9. [KV Cache & Memory Management](#9-kv-cache--memory-management)
10. [Fault Tolerance & Checkpointing](#10-fault-tolerance--checkpointing)

---

## 1. Distributed Training & Parallelism

### 1.1 PyTorch FSDP: Fully Sharded Data Parallel
- **Title:** PyTorch FSDP: Experiences on Scaling Fully Sharded Data Parallel
- **Authors:** Yanli Zhao, Andrew Gu, Liang Luo, et al. (Meta AI)
- **Venue:** arXiv:2304.11277 (PyTorch production release, 2023)
- **Year:** 2023
- **Why Milestone:** Became the standard distributed training primitive in PyTorch, replacing third-party sharding libraries. Enabled training models with trillions of parameters by sharding parameters, gradients, and optimizer states across data-parallel workers. FSDP2 (2024) further refined per-parameter Distributed Tensor representation, becoming the backbone of virtually all open-source LLM training (OPT, OLMo, Llama, etc.).

### 1.2 DeepSpeed ZeRO-Infinity & ZeRO-3
- **Title:** ZeRO-Infinity: Breaking GPU Memory Wall for Extreme Scale Deep Learning
- **Authors:** Samyam Rajbhandari, Olatunji Ruwase, et al. (Microsoft)
- **Venue:** SC21 / arXiv:2104.07857 (ZeRO family); DeepSpeed-ZeRO widely adopted 2020–2023
- **Year:** 2021 (ZeRO-3 formalized 2021; ZeRO++ 2023)
- **Why Milestone:** The ZeRO (Zero Redundancy Optimizer) family fundamentally redefined how optimizer states, gradients, and parameters are partitioned across GPUs. ZeRO-3 enabled training models with hundreds of billions of parameters on commodity clusters by offloading to CPU/NVMe. DeepSpeed became the de facto training infrastructure for early large model training (GPT-3 scale, BLOOM, OPT).

### 1.3 Megatron-LM: Tensor & Pipeline Parallelism
- **Title:** Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM
- **Authors:** Deepak Narayanan, Mohammad Shoeybi, et al. (NVIDIA)
- **Venue:** SC21 / arXiv:2104.04473
- **Year:** 2021 (dominant production use 2022–2026)
- **Why Milestone:** Established the standard implementation of tensor parallelism (TP) and pipeline parallelism (PP) for Transformer training. The interleaved PP schedule and TP/PP/DP hybrid strategy became the template for training GPT-3, GPT-4, Llama, and virtually all large dense models. Still the reference implementation in NVIDIA NeMo.

### 1.4 TorchTitan: Native PyTorch LLM Training
- **Title:** TorchTitan: One-stop PyTorch Native Solution for Production-Ready LLM Pretraining
- **Authors:** PyTorch Team (Meta)
- **Venue:** arXiv:2410.06511 (production toolkit)
- **Year:** 2024
- **Why Milestone:** Represents the convergence of PyTorch native distributed training into a single reference implementation combining FSDP2, Tensor Parallel, Pipeline Parallel, Context Parallel, and Composability. Became the canonical template for new LLM training projects, replacing fragmented third-party training scripts.

### 1.5 Ring Attention with Blockwise Transformers
- **Title:** Ring Attention with Blockwise Transformers for Near-Infinite Context
- **Authors:** Lianmin Zheng, et al. (UC Berkeley / LMSYS)
- **Venue:** ICLR 2024 (arXiv:2310.01889)
- **Year:** 2024
- **Why Milestone:** Enabled training and inference on context lengths previously impossible (millions of tokens) by distributing sequence blocks across devices in a ring topology with blockwise attention. Opened the sub-field of context-parallel training and directly inspired later long-context models (Claude 3, Gemini 1.5).

### 1.6 DiLoCo: Distributed Low-Communication Training
- **Title:** DiLoCo: Distributed Low-Communication Training of Language Models
- **Authors:** Arthur Douillard, et al. (Meta AI)
- **Venue:** arXiv:2311.08105
- **Year:** 2023
- **Why Milestone:** Pioneered federated-averaging-style training for large language models, enabling distributed training across poorly connected nodes (e.g., geo-distributed clusters). Demonstrated that local optimization with periodic global averaging can match centralized training quality, opening a new paradigm for decentralized foundation model training.

---

## 2. Memory-Efficient Attention & Kernels

### 2.1 FlashAttention-2
- **Title:** FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning
- **Authors:** Tri Dao
- **Venue:** ICLR 2024 (arXiv:2307.08691)
- **Year:** 2023/2024
- **Why Milestone:** The FlashAttention lineage (1.0 at NeurIPS 2022, 2.0 at ICLR 2024) is the single most impactful kernel-level optimization for Transformer training/inference. By tiling attention with online softmax and fusing the attention computation into a single CUDA kernel, FlashAttention eliminated the quadratic memory bottleneck in HBM, achieving 2–4× wall-clock speedup without approximation. Integrated into virtually every training and inference stack (PyTorch, JAX, vLLM, SGLang, TensorRT-LLM).

### 2.2 FlashAttention-3
- **Title:** FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-Precision
- **Authors:** Jay Shah, Ganesh Bikshandi, Ying Zhang, Vijay Thakkar, Pradeep Ramani, Tri Dao
- **Venue:** NeurIPS 2024 (arXiv:2407.08608)
- **Year:** 2024
- **Why Milestone:** Pushed the frontier to 85% of H100 theoretical peak FLOPS by exploiting Hopper-specific hardware features: asynchronous WGMMA (warp-group matrix multiply accumulate), TMA (Tensor Memory Accelerator), and FP8 low-precision. Demonstrated that hardware-native asynchrony is essential for extracting full performance from next-generation GPUs. Became the reference kernel for H100/Blackwell training.

### 2.3 Liger Kernel: Efficient Triton Kernels for LLM Training
- **Title:** Liger Kernel: Efficient Triton Kernels for LLM Training
- **Authors:** Heraldo L. et al. (LinkedIn / Open Source)
- **Venue:** arXiv:2410.10989 (widely adopted in HuggingFace ecosystem)
- **Year:** 2024
- **Why Milestone:** Open-sourced a comprehensive suite of production-quality fused Triton kernels for LLM training (RMSNorm, RoPE, SwiGLU, CrossEntropy, attention variants). Achieved 30% training time reduction and 60–70% CUDA memory savings. Became the standard kernel library for efficient fine-tuning and training in the HuggingFace ecosystem, complementing FlashAttention.

### 2.4 DeepGEMM / FP8 GEMM Kernels (DeepSeek)
- **Title:** DeepGEMM: Clean and efficient FP8 GEMM kernels with fine-grained scaling
- **Authors:** DeepSeek-AI
- **Venue:** GitHub / arXiv (2024–2025, released as core training infrastructure)
- **Year:** 2025
- **Why Milestone:** The open-sourcing of DeepSeek's FP8 GEMM kernels alongside DeepSeek-V3 demonstrated that sub-1-bit training at scale is not only feasible but optimal. Achieved near-peak utilization on H800 clusters, enabling the training of a 671B-parameter MoE model for ~$5.6M. These kernels became a reference for low-precision training infrastructure.

---

## 3. LLM Inference Serving Engines

### 3.1 vLLM: Efficient Memory Management for LLM Serving with PagedAttention
- **Title:** Efficient Memory Management for Large Language Model Serving with PagedAttention
- **Authors:** Wonsuk Kwon, Zhuohan Li, et al. (UC Berkeley / vLLM Team)
- **Venue:** SOSP 2023 (arXiv:2309.06180)
- **Year:** 2023
- **Why Milestone:** Arguably the single most impactful inference systems paper of the 2023–2026 period. Introduced PagedAttention, which applies OS virtual-memory paging concepts to KV cache management, eliminating memory fragmentation and enabling 2–4× throughput improvement. vLLM became the industry-standard open-source inference engine (67,000+ GitHub stars by 2026), powering the majority of production LLM deployments. Spawned an entire ecosystem of derivatives and integrations.

### 3.2 SGLang: Efficient Execution of Structured LLM Programs
- **Title:** SGLang: Efficient Execution of Structured Language Model Programs
- **Authors:** Lianmin Zheng, Liangsheng Yin, et al. (UC Berkeley / LMSYS / Together AI)
- **Venue:** SOSP 2024 (arXiv:2312.07104)
- **Year:** 2024
- **Why Milestone:** Introduced RadixAttention, a radix-tree-based KV cache reuse mechanism that automatically exploits prefix sharing across multi-turn conversations, agent workflows, and structured generation. Co-designed a frontend language with the backend runtime, achieving up to 5× throughput on agent workloads. Became the primary competitor and complement to vLLM, with adoption by 400,000+ GPUs worldwide by 2026. SGLang also became the standard rollout backend for RL training frameworks (AReaL, Miles, verl, etc.).

### 3.3 Orca: A Distributed Serving System for Transformer Models
- **Title:** Orca: A Distributed Serving System for Transformer-Based Generative Models
- **Authors:** Gyeong-In Yu, Joo Seong Jeong, et al. (Seoul National University / Microsoft)
- **Venue:** OSDI 2022 (arXiv:2201.03848)
- **Year:** 2022 (foundational impact throughout 2023–2026)
- **Why Milestone:** Introduced **iteration-level scheduling** (continuous batching), which breaks the rigid request-level batching paradigm and allows the GPU to remain saturated by adding/removing requests at every iteration. This scheduling philosophy became the foundation of all modern LLM serving systems (vLLM, TGI, SGLang, TensorRT-LLM). Without Orca, PagedAttention would not have achieved its full throughput potential.

### 3.4 DistServe / Splitwise: Disaggregated Prefill-Decode
- **Title:** DistServe: Disaggregating Prefill and Decoding for Goodput-Optimized Large Language Model Serving
- **Authors:** Yichao Zhong, Junda Chen, et al. (Peking University / Stanford)
- **Venue:** OSDI 2024 (arXiv:2406.02069)
- **Year:** 2024
- **Why Milestone:** Identified that the prefill (compute-bound) and decode (memory-bound) phases have fundamentally conflicting resource requirements. By disaggregating them onto separate GPU pools, achieved up to 2.3× goodput improvement at strict SLOs. Spawned the "disaggregated serving" paradigm now adopted by vLLM, SGLang, and cloud inference platforms. Splitwise (ISCA 2024, Patel et al.) extended this with phase-aware placement across heterogeneous clusters.

### 3.5 Mooncake: KVCache-Centric Disaggregated Architecture
- **Title:** Mooncake: A KVCache-Centric Disaggregated Architecture for LLM Serving
- **Authors:** Ruoyu Qin, et al. (Moonshot AI / Tsinghua)
- **Venue:** arXiv:2407.08516 (Kimi production system)
- **Year:** 2024
- **Why Milestone:** The first production-grade documentation of a KVCache-centric serving architecture, where the KV cache is treated as a first-class distributed object stored separately from compute nodes. Enabled Kimi to serve extremely long contexts (200K+ tokens) with low TTFT. Inspired the broader ecosystem of KV cache disaggregation (LMCache, CacheGen, etc.).

---

## 4. Compiler & Kernel Infrastructure

### 4.1 Triton: An Intermediate Language for Tiled Neural Network Computations
- **Title:** Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations
- **Authors:** Philippe Tillet, H. T. Kung, David Cox (Harvard / OpenAI)
- **Venue:** MAPL 2019 (arXiv:1910.00015); Triton 3.0+ released 2023–2024
- **Year:** 2019 (mature adoption as default backend 2023–2026)
- **Why Milestone:** Triton evolved from a research prototype into the **default kernel compilation layer** for PyTorch 2.0+ (`torch.compile` / Inductor), vLLM, SGLang, FlashAttention, and virtually all new LLM kernels. Its Python-like syntax and block-level programming model eliminated the need for hand-written CUDA C++ for most ML use cases. By 2026, Triton is supported on NVIDIA, AMD, Intel, and custom AI accelerators, making it the lingua franca of ML kernel development.

### 4.2 TorchInductor & torch.compile (PyTorch 2.0)
- **Title:** torch.compile: A compiler for PyTorch 2.0
- **Authors:** Jason Ansel, et al. (Meta AI)
- **Venue:** arXiv:2312.16881 (PyTorch 2.0 release, 2023)
- **Year:** 2023
- **Why Milestone:** `torch.compile` with TorchInductor as its default backend automated the generation of optimized Triton kernels from captured PyTorch graphs, achieving 2.27× inference and 1.41× training speedup across 180+ models with a single decorator. This represented a paradigm shift from hand-optimized kernels to compiler-driven optimization, becoming the standard entry point for PyTorch performance tuning.

### 4.3 CUTLASS: Composable Templates for CUDA GEMMs
- **Title:** CUTLASS: Fast Linear Algebra in CUDA C++
- **Authors:** Andrew Kerr, et al. (NVIDIA)
- **Venue:** CUDA ecosystem release (ongoing, major releases 2022–2024)
- **Year:** 2022–2024 (CUTLASS 3.x with Hopper support)
- **Why Milestone:** CUTLASS 3.0 introduced CuTe (CUDA Template Extensions), a composable tensor-core GEMM abstraction that underpins FlashAttention-3, TensorRT-LLM, and all high-performance NVIDIA inference. It remains the performance ceiling that Triton and other compilers aim to match, and the reference for hand-tuned CUDA kernel development.

### 4.4 MLIR: Multi-Level Intermediate Representation
- **Title:** MLIR: A Compiler Infrastructure for the End of Moore's Law
- **Authors:** Chris Lattner, et al. (Google / LLVM)
- **Venue:** arXiv:2002.11054 (CIRCT/MLIR ecosystem maturation 2023–2026)
- **Year:** 2020 (industry maturation 2023–2026)
- **Why Milestone:** MLIR became the compiler backbone for TensorFlow, PyTorch (via Torch-MLIR), JAX, and custom AI accelerators (TPU, Gaudi, Ascend). Its multi-level IR design enables retargetable optimization across CPUs, GPUs, and NPUs. By 2026, MLIR-based compilers are the standard for deploying models to non-NVIDIA hardware.

---

## 5. Quantization & Model Compression

### 5.1 GPTQ: Accurate Post-Training Quantization for Generative Pretrained Transformers
- **Title:** GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers
- **Authors:** Elias Frantar, Saleh Ashkboos, Torsten Hoefler, Dan Alistarh
- **Venue:** ICLR 2023 (arXiv:2210.17323)
- **Year:** 2023
- **Why Milestone:** GPTQ became the standard method for 4-bit and 3-bit post-training quantization of LLMs, enabling deployment of 70B+ models on consumer GPUs. Its layer-wise optimal weight allocation and OBQ (Optimal Brain Quantization) foundation made it the default quantization path for local LLM deployment (Ollama, llama.cpp, vLLM, Text Generation Inference).

### 5.2 AWQ: Activation-aware Weight Quantization
- **Title:** AWQ: Activation-aware Weight Quantization for On-Device LLM Compression and Acceleration
- **Authors:** Ji Lin, Jiaming Tang, Haotian Tang, et al. (MIT / NVIDIA)
- **Venue:** MLSys 2024 (arXiv:2306.00978)
- **Year:** 2023/2024
- **Why Milestone:** AWQ protected "salient" weight channels based on activation distributions, achieving better accuracy at 4-bit than GPTQ for on-device inference. Became the default quantization method for edge deployment (mobile, laptop) and is integrated into vLLM, TensorRT-LLM, and llama.cpp. Demonstrated that quantization-aware hardware deployment requires activation-distribution awareness, not just weight magnitude.

### 5.3 QLoRA: Efficient Finetuning of Quantized LLMs
- **Title:** QLoRA: Efficient Finetuning of Quantized LLMs
- **Authors:** Tim Dettmers, Artidoro Pagnoni, et al. (UW / Meta)
- **Venue:** NeurIPS 2023 (arXiv:2305.14314)
- **Year:** 2023
- **Why Milestone:** Combined 4-bit quantization (via NormalFloat4) with LoRA adapters, enabling fine-tuning of 65B models on a single consumer GPU. Democratized LLM fine-tuning and became the backbone of the open-source fine-tuning ecosystem (HuggingFace PEFT, Axolotl, unsloth). The most widely adopted parameter-efficient training method for resource-constrained practitioners.

### 5.4 QuIP: 2-Bit Quantization with Guarantees
- **Title:** QuIP: 2-Bit Quantization of Large Language Models with Guarantees
- **Authors:** Jerry Chee, Yaohui Cai, Volodymyr Kuleshov, Christopher M. De Sa
- **Venue:** NeurIPS 2023 (arXiv:2307.13304)
- **Year:** 2023
- **Why Milestone:** Pushed the quantization frontier to 2-bit with theoretical guarantees on reconstruction error, challenging the assumption that 4-bit is the practical limit. Spawned a family of follow-ups (QuIP#, SpinQuant) and demonstrated that extreme quantization at scale is feasible without catastrophic quality loss.

---

## 6. Mixture-of-Experts (MoE) Infrastructure

### 6.1 DeepSeek-V3: Multi-Level MoE with Auxiliary-Loss-Free Load Balancing
- **Title:** DeepSeek-V3 Technical Report
- **Authors:** DeepSeek-AI
- **Venue:** arXiv:2412.19437
- **Year:** 2024
- **Why Milestone:** Trained a 671B-parameter MoE model (37B active per token) with 2.788M H800 GPU hours (~$5.6M), demonstrating that trillion-parameter MoE training is economically viable with the right infrastructure. Introduced auxiliary-loss-free load balancing and multi-token prediction, achieving stable training without loss spikes. Its training log became a canonical reference for MoE infrastructure design, directly inspiring DeepSeek-R1 and Qwen3-MoE.

### 6.2 Mixtral 8x7B: Open MoE for the Masses
- **Title:** Mixtral of Experts
- **Authors:** Albert Q. Jiang, Alexandre Sablayrolles, Antoine Roux, et al. (Mistral AI)
- **Venue:** arXiv:2401.04088 (released Dec 2023)
- **Year:** 2023/2024
- **Why Milestone:** The first widely adopted open-source MoE model, proving that sparse activation (8 experts, 2 active, ~47B total / ~13B active) could match Llama 2 70B quality with far lower active compute. Brought MoE from Google/GShard's internal infrastructure into the open-source LLM ecosystem, directly enabling DeepSeek-MoE, Qwen-MoE, and DBRX.

### 6.3 DeepSpeed-MoE & Tutel: Expert Parallelism Frameworks
- **Title:** DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training to Power Next-Generation AI Scale
- **Authors:** Samyam Rajbhandari, Conglong Li, et al. (Microsoft)
- **Venue:** ICML 2022 (arXiv:2201.05596); Tutel (OSDI 2023)
- **Year:** 2022 (dominant production use 2023–2026)
- **Why Milestone:** Established the software infrastructure for expert parallelism (EP), enabling training of trillion-parameter MoE models. Tutel (OSDI 2023) introduced dynamic EP/DP switching and adaptive expert routing. These frameworks became the reference for all subsequent MoE training systems (including DeepSeek's custom infrastructure).

### 6.4 UltraEP / DeepEP: Expert Communication Optimization
- **Title:** DeepEP: An Efficient Expert-Communication Library for MoE
- **Authors:** DeepSeek-AI
- **Venue:** GitHub / arXiv (2025)
- **Year:** 2025
- **Why Milestone:** Open-sourced the communication kernel library that enabled DeepSeek-V3's training efficiency. Optimized all-to-all communication for expert parallelism with fused dispatch/combine kernels, achieving near-wire-speed on InfiniBand. Became the reference implementation for MoE communication optimization, with adoption by UltraEP (Alibaba) and other frameworks.

---

## 7. Scheduling & Cluster Management

### 7.1 Sia: Heterogeneity-Aware, Goodput-Optimized ML-Cluster Scheduling
- **Title:** Sia: Heterogeneity-Aware, Goodput-Optimized ML-Cluster Scheduling
- **Authors:** Jiachen Mao, et al. (UC Berkeley / Princeton)
- **Venue:** SOSP 2023
- **Year:** 2023
- **Why Milestone:** Introduced goodput (useful throughput per dollar) as the scheduling objective rather than raw throughput, and demonstrated heterogeneity-aware scheduling across GPU generations. Addressed the reality that production clusters contain mixed hardware (A100, H100, etc.), making it foundational for cost-aware ML infrastructure.

### 7.2 Pollux: Co-adaptive Cluster Scheduling for Goodput-Optimized Deep Learning
- **Title:** Pollux: Co-adaptive Cluster Scheduling for Goodput-Optimized Deep Learning
- **Authors:** Aurick Qiao, et al. (Petuum / Carnegie Mellon)
- **Venue:** OSDI 2021 (widespread adoption 2023–2026)
- **Year:** 2021 (impactful throughout 2023–2026)
- **Why Milestone:** Pollux co-adapted batch size and learning rate with cluster scheduling, dynamically reallocating GPUs based on training progress. Its goodput-optimization philosophy became the standard for cloud ML training platforms (AWS SageMaker, Google Vertex AI, Azure ML).

### 7.3 MARS: Efficient, Adaptive Co-Scheduling for Heterogeneous Agentic Systems
- **Title:** MARS: Efficient, Adaptive Co-Scheduling for Heterogeneous Agentic Systems
- **Authors:** Various (2026)
- **Venue:** arXiv:2604.26963
- **Year:** 2026
- **Why Milestone:** The first scheduling system designed explicitly for multi-agent inference workloads, closing the control loop across CPU-GPU telemetry to jointly coordinate admission, prioritization, and residency. Represents the evolution from request-centric scheduling to workflow-aware scheduling for agentic AI.

---

## 8. Agent Infrastructure & OS Abstractions

### 8.1 AIOS: LLM Agent Operating System
- **Title:** AIOS: LLM Agent Operating System
- **Authors:** Kai Mei, Zheng Wang, et al. (Rutgers / others)
- **Venue:** COLM 2025 (arXiv:2403.16971)
- **Year:** 2024/2025
- **Why Milestone:** Proposed the first comprehensive kernel-shaped architecture for running multiple LLM agents concurrently, with modules for scheduling, context management, memory management, storage, tool mediation, and access control. Accepted at COLM 2025 as a foundational paper. Spawned an open-source ecosystem (AIOS SDK, Cerebrum) and established the vocabulary for agent runtime design (scheduler, context manager, tool manager).

### 8.2 MemGPT: Virtual Memory for LLM Context
- **Title:** MemGPT: Towards LLMs as Operating Systems
- **Authors:** Charles Packer, Vivian Fang, et al. (UC Berkeley / Stanford)
- **Venue:** arXiv:2310.08560
- **Year:** 2023
- **Why Milestone:** Introduced the OS paging metaphor to LLM context management, explicitly framing limited context windows as "fast memory" and external storage as "slow memory." Demonstrated that hierarchical memory with model-driven paging could enable agents to operate on effectively infinite context. Inspired the entire sub-field of agent memory hierarchies (MemOS, A-MEM, ClawVM, etc.).

### 8.3 AgentOS / MemOS: Memory-Centric Agent Runtimes
- **Title:** MemOS: Memory Operating System for Language Model Agents
- **Authors:** Various (2025)
- **Venue:** arXiv:2502.xxxxx (follow-up to AIOS/MemGPT)
- **Year:** 2025
- **Why Milestone:** Extended the AIOS kernel metaphor with unified representation and evolution across heterogeneous memory types (episodic, semantic, procedural). Represents the maturation of agent runtime research from proof-of-concept to structured memory operating systems.

---

## 9. KV Cache & Memory Management

### 9.1 H2O: Heavy-Hitter Oracle for KV Cache Compression
- **Title:** H2O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models
- **Authors:** Zhenyu Zhang, et al. (PKU / Microsoft)
- **Venue:** ICML 2023 / ES-FoMo Workshop (arXiv:2306.14098)
- **Year:** 2023
- **Why Milestone:** Formally identified and exploited the "heavy-hitter" phenomenon in KV caches: a small subset of tokens carries disproportionate attention weight. By retaining only these heavy-hitters and evicting the rest, achieved up to 5× KV cache compression with minimal accuracy loss. Established the theoretical foundation for all subsequent KV cache eviction strategies (Scissorhands, StreamingLLM, SnapKV, etc.).

### 9.2 StreamingLLM: Attention Sinks for Infinite Context
- **Title:** Efficient Streaming Language Models with Attention Sinks
- **Authors:** Guangxuan Xiao, Yuandong Tian, Beidi Chen, et al. (MIT / Meta)
- **Venue:** ICLR 2024 (arXiv:2309.17453)
- **Year:** 2024
- **Why Milestone:** Discovered that keeping the first 4 "sink" tokens (plus recent tokens) is sufficient to stabilize infinite-length generation. Combined with KV cache eviction, enabled LLMs to process millions of tokens without retraining. Became the standard technique for streaming/long-context inference in production systems.

### 9.3 CacheGen / LMCache: Modular KV Cache Compression & Transfer
- **Title:** CacheGen: Fast Context Loading for Language Model Applications
- **Authors:** various (Microsoft / Stanford)
- **Venue:** OSDI 2024 / arXiv:2403.01208
- **Year:** 2024
- **Why Milestone:** Pioneered the idea of KV cache as a transferable, compressible artifact. Enabled storing pre-computed KV caches on disk/network and rapidly loading them for inference, reducing TTFT for long-context RAG and multi-turn conversations. LMCache (2025) extended this to a full KV cache storage system, making cache transfer a first-class infrastructure primitive.

---

## 10. Fault Tolerance & Checkpointing

### 10.1 Oobleck: Resilient Distributed Training with Pipeline Templates
- **Title:** Oobleck: Resilient Distributed Training of Large Models Using Pipeline Templates
- **Authors:** Insu Jang, et al. (UIUC / Microsoft)
- **Venue:** SOSP 2023
- **Year:** 2023
- **Why Milestone:** Addressed the reality that large-scale training jobs face frequent failures (hardware, network, software). Oobleck used pipeline templates to enable fast reconfiguration after node failures without full restart. Became a reference for fault-tolerant training design in the pre-MegaScale era.

### 10.2 MegaScale: Production-Scale Fault Tolerance at ByteDance
- **Title:** MegaScale: Scaling Large Language Model Training to More Than 10,000 GPUs
- **Authors:** various (ByteDance)
- **Venue:** arXiv:2402.11235
- **Year:** 2024
- **Why Milestone:** Documented the first public 10,000+ GPU training cluster with systematic fault tolerance (RAS, automatic diagnosis, fast checkpointing). Demonstrated that training at extreme scale requires treating failures as a first-class system design constraint. The MegaScale checkpointing approach (snapshot-stall + async persist) became standard practice.

### 10.3 DataStates-LLM / FastPersist: Asynchronous Checkpointing
- **Title:** DataStates-LLM: Low-Latency Distributed Checkpointing for Large Language Models
- **Authors:** various (2024)
- **Venue:** arXiv:2404.xxxxx
- **Year:** 2024
- **Why Milestone:** Optimized the checkpointing pipeline by pre-allocating pinned host memory and pipelining snapshot/persist phases with training iterations. Reduced checkpoint stall time to near-zero, making high-frequency checkpointing (every few minutes) practical for billion-dollar training runs. FastPersist (2024) further hardened this with double-buffering and subset-rank writing.

---

## Summary Statistics

| Sub-theme | Papers Listed | Key Venues |
|-----------|---------------|------------|
| Distributed Training & Parallelism | 6 | SOSP, OSDI, ICLR, arXiv |
| Memory-Efficient Attention & Kernels | 4 | ICLR, NeurIPS, arXiv |
| LLM Inference Serving Engines | 5 | SOSP, OSDI, arXiv |
| Compiler & Kernel Infrastructure | 4 | MAPL, ICLR, arXiv |
| Quantization & Model Compression | 4 | ICLR, MLSys, NeurIPS |
| Mixture-of-Experts (MoE) Infrastructure | 4 | arXiv, ICML, OSDI |
| Scheduling & Cluster Management | 3 | SOSP, OSDI, arXiv |
| Agent Infrastructure & OS Abstractions | 3 | COLM, arXiv |
| KV Cache & Memory Management | 3 | ICML, ICLR, OSDI |
| Fault Tolerance & Checkpointing | 3 | SOSP, arXiv |
| **Total** | **39** | |

---

## Citation & Further Reading

- LLM Systems Paper List: [AmberLJC/LLMSys-PaperList](https://github.com/AmberLJC/LLMSys-PaperList)
- Awesome Distributed ML: [Shenggan/awesome-distributed-ml](https://github.com/Shenggan/awesome-distributed-ml)
- Awesome LLM Inference Serving: [zenrran4nlp/Awesome-LLM-Inference-Serving](https://github.com/zenrran4nlp/Awesome-LLM-Inference-Serving)
- Efficient Training of Large Language Models on Distributed Infrastructures: A Survey (2024): [arXiv:2407.20018](https://arxiv.org/abs/2407.20018)
- SGLang Documentation: [sgl-project/sglang](https://github.com/sgl-project/sglang)
- vLLM Documentation: [vllm-project/vllm](https://github.com/vllm-project/vllm)
- FlashAttention Repository: [dao-ailab/flash-attention](https://github.com/dao-ailab/flash-attention)
