# AI Hardware Milestone Papers (2023–Mid-2026)

> A curated list of the most important, milestone, and trunk papers in AI Hardware from 2023 to mid-2026 (July 2026). Focused on foundational works, widely cited breakthroughs, and papers that opened new directions. Organized by sub-theme.

---

## Table of Contents

1. [Datacenter AI Accelerators (GPU / TPU / ASIC)](#1-datacenter-ai-accelerators-gpu--tpu--asic)
2. [LLM Inference Systems & Memory Optimization](#2-llm-inference-systems--memory-optimization)
3. [In-Memory & Analog Computing (CIM / PIM)](#3-in-memory--analog-computing-cim--pim)
4. [Neuromorphic Computing](#4-neuromorphic-computing)
5. [Photonic & Optical AI Accelerators](#5-photonic--optical-ai-accelerators)
6. [Advanced Packaging, Chiplets & Interconnect for AI](#6-advanced-packaging-chiplets--interconnect-for-ai)
7. [Edge AI & TinyML Accelerators](#7-edge-ai--tinyml-accelerators)
8. [Hardware-Software Co-Design & Compilation](#8-hardware-software-co-design--compilation)

---

## 1. Datacenter AI Accelerators (GPU / TPU / ASIC)

### 1.1 NVIDIA Hopper Architecture (H100 Tensor Core GPU)
- **Title:** NVIDIA H100 Tensor Core GPU Architecture
- **Authors:** NVIDIA Architecture Team (White Paper)
- **Venue:** NVIDIA Technical White Paper / Industry Release
- **Year:** 2022 (Volume Deployment 2023)
- **Why Milestone:** The H100 introduced the **4th-generation Tensor Core** with native FP8 support, the **Transformer Engine** for dynamic mixed-precision training, and **NVLink Switch System** enabling up to 256 GPU clusters. It became the workhorse of the 2023–2024 LLM training boom, powering GPT-4, Claude, and virtually every major foundation model training cluster. It represents the single most influential piece of silicon in the generative AI era, establishing FP8 as an industry standard precision format for training.

### 1.2 NVIDIA Blackwell Architecture (B200 / GB200)
- **Title:** NVIDIA Blackwell Architecture Technical Overview
- **Authors:** NVIDIA Architecture Team (White Paper)
- **Venue:** NVIDIA Technical White Paper / GTC 2024 Keynote
- **Year:** 2024 (Volume Shipment 2025)
- **Why Milestone:** Blackwell introduced a **dual-die chiplet design** (208 billion transistors) connected by a 10 TB/s chip-to-chip interconnect, **5th-generation Tensor Cores** with FP4/FP6 support, and a **2nd-generation Transformer Engine**. The NVL72 rack-scale system treats 72 GPUs as a single logical accelerator with NVLink5 at 1.8 TB/s per GPU. It marks NVIDIA's explicit pivot from general-purpose HPC to generative-AI-optimized architecture, achieving ~45% higher inference throughput than Hopper in MLPerf v5.0/v5.1. Microsoft deployed a 4,608-GPU Blackwell cluster reaching ~92 exaFLOPS FP4 inference.

### 1.3 Google TPU v4: Optical Circuit Switching at Scale
- **Title:** TPU v4: An Optically Reconfigurable Supercomputer for Machine Learning with Hardware Support for Embeddings
- **Authors:** Norman P. Jouppi et al.
- **Venue:** ISCA 2023
- **Year:** 2023
- **Why Milestone:** This paper detailed the **first production deployment of optical circuit switches (OCS)** in a datacenter AI interconnect, enabling dynamic reconfiguration of a 3D torus topology across 4,096 chips. TPU v4 introduced **SparseCores**—small dataflow units accelerating embedding lookups by 5–7x. The OCS fabric consumed <3% of pod power and enabled sub-10-ns reconfiguration, representing one of the most significant datacenter networking innovations in decades. PaLM training mobilized 6,144 TPU v4 chips.

### 1.4 Google TPU v5p / v5e and Trillium (v6)
- **Title:** Google Cloud TPU v5p and Trillium: Scaling AI Training and Inference (various technical blog posts and industry communications)
- **Authors:** Google Cloud / Google DeepMind Engineering Teams
- **Venue:** Google Cloud Blog / Industry Release
- **Year:** 2023 (v5p/v5e), 2024 (Trillium v6)
- **Why Milestone:** TPU v5p achieved ~4.45 exaFLOPS across 8,960-chip pods with 4,800 Gbps ICI bandwidth per chip, doubling v4's maximum pod size. Trillium (v6) delivered **4.7x peak per-chip performance** over v5e with 2x memory and ICI bandwidth, enabling 100K-chip pods. These generations represent Google's strategic bifurcation into training-optimized (v5p) and inference-optimized (v5e, Trillium) product lines, and powered Gemini Ultra/Gemini 2.0 training.

### 1.5 Google TPU Ironwood (v7)
- **Title:** Google Cloud TPU Ironwood: The Next Generation AI Accelerator
- **Authors:** Google Cloud Engineering
- **Venue:** Google Cloud Next 2025 / Industry Release
- **Year:** 2025 (Announced)
- **Why Milestone:** Ironwood is Google's first **"inference-first" TPU architecture**, delivering ~4,614 TOPS per chip, 192 GB HBM3 per chip, and pods scaling to 9,216 chips for 42.5 exaFLOPS FP8 aggregate. The strategic shift—removing continuous training capabilities—signals Google's bet that production AI workloads will remain inference-dominated. It sets the bar for memory capacity per accelerator (192 GB) and represents the culmination of seven generations of TPU evolution.

### 1.6 AMD Instinct MI300X / MI325X (CDNA 3 Architecture)
- **Title:** AMD Instinct MI300 Series: Advancing AI and HPC with Chiplet Architecture (ISSCC 2024 Industry Session 11.1)
- **Authors:** Alan Smith et al. (AMD)
- **Venue:** ISSCC 2024 (Invited Industry Session)
- **Year:** 2024 (MI300X), 2024/2025 (MI325X)
- **Why Milestone:** The MI300X was the first major non-NVIDIA datacenter GPU to achieve mass cloud deployment (Azure, Oracle, Meta). It uses a **chiplet-based CDNA 3 architecture** integrating up to 8 XCD compute dies, 256 MB Infinity Cache, and 192 GB HBM3 (MI300X) / 256 GB HBM3E (MI325X). The MI325X delivered 6 TB/s bandwidth and 2.6 PFLOPS FP8, directly challenging NVIDIA H200. AMD's annual cadence roadmap (MI325X -> MI350X CDNA 4 -> MI400 CDNA Next) established AMD as the credible #2 in AI accelerators.

### 1.7 Cerebras Wafer-Scale Engine 2 / 3 (WSE-2 / WSE-3)
- **Title:** Cerebras Wafer-Scale Engine: The Industry's Largest AI Processor (Industry White Papers and SEMI Award 2023)
- **Authors:** Cerebras Systems Engineering Team
- **Venue:** HotChips / Industry Publications / SEMI Award 2023
- **Year:** 2023 (WSE-2 in production), 2024 (WSE-3)
- **Why Milestone:** WSE-2 (7 nm, ~1.2 trillion transistors, 46,225 mm², 40 GB on-chip SRAM) was the **largest processor ever built**—56x larger than the largest GPU, with 1,000x more on-chip memory and 12,000x more fabric bandwidth. WSE-3 (2024) scaled to 4 trillion transistors, 900K cores, 44 GB SRAM, and 21 PB/s fabric bandwidth. Cerebras proved that wafer-scale integration is manufacturable and economically viable, training models up to 24 trillion parameters without partitioning. It won the 2023 SEMI Award for North America.

### 1.8 Groq Language Processing Unit (LPU) / Tensor Streaming Processor
- **Title:** Groq LPU: Compiler-Defined Architecture for Low-Latency AI Inference (Industry Technical Communications)
- **Authors:** Groq Engineering Team (Jonathan Ross, et al.)
- **Venue:** Groq Blog / Industry Benchmarks / MLPerf
- **Year:** 2023–2025 (Rapid Scaling)
- **Why Milestone:** Groq's LPU implements a **kernel-less, compiler-defined dataflow architecture** where tokens stream through a deterministic pipeline of functional units with no kernel switching overhead. It achieves deterministic latency critical for real-time applications, claiming 10x faster inference and 10x lower cost than GPUs for certain LLM workloads. Groq raised $750M at a $6.9B valuation in 2025 and secured a $1.5B Saudi commitment, demonstrating that non-GPU inference architectures can attract massive capital.

### 1.9 Tesla Dojo D1 / Training Supercomputer
- **Title:** Tesla Dojo D1 Chip and ExaPOD Architecture (Tesla AI Day 2021; subsequent industry disclosures)
- **Authors:** Tesla Autopilot / AI Hardware Team (Ganesh Venkataramanan, et al.)
- **Venue:** Tesla AI Day / Industry White Papers
- **Year:** 2021 (Announced), 2023 (Production Deployment), 2024–2025 (Operational at Scale)
- **Why Milestone:** Dojo D1 (TSMC 7 nm, ~50 billion transistors, 645 mm², 354 custom cores, 440 MB SRAM per chip) was designed as a **system-on-wafer** with proprietary mesh interconnect and custom CFloat8/CFloat16 formats. Training tiles (25 D1 chips in 5x5 mesh) achieved ~9 PFLOPS FP16/BF16. Dojo represented a bold vertical-integration bet by a non-semiconductor company to build custom training silicon. Though Tesla reportedly dissolved the Dojo team in 2025, the D1 architecture influenced thinking about custom floating-point formats and mesh-based AI training systems.

### 1.10 SambaNova DataScale / Reconfigurable Dataflow Unit (RDU)
- **Title:** SambaNova RDU: Reconfigurable Dataflow Architecture for Enterprise AI (Industry Communications)
- **Authors:** SambaNova Systems Engineering
- **Venue:** Industry White Papers / MLPerf Submissions
- **Year:** 2023–2025
- **Why Milestone:** SambaNova's RDU implements a **reconfigurable dataflow architecture** that dynamically maps diverse ML workloads onto a tiled compute fabric with up to 3 TB in-rack memory. Unlike fixed-function AI ASICs, the RDU supports training, inference, and non-ML data analytics on the same hardware. The company reached multi-billion-dollar valuation and demonstrated that reconfigurable dataflow can compete with GPUs in enterprise AI deployments, particularly for models that exceed single-GPU memory capacity.

---

## 2. LLM Inference Systems & Memory Optimization

### 2.1 FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning
- **Title:** FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning
- **Authors:** Tri Dao
- **Venue:** ICLR 2024
- **Year:** 2024
- **Why Milestone:** FlashAttention-2 refined the original FlashAttention algorithm with better thread-block parallelism, reduced non-matmul FLOPs, and support for head dimensions up to 256. It achieves **2–4x speedup** over standard attention in training and up to **8x speedup** in inference (with FlashDecoding). By making exact attention IO-aware and tiling-friendly, it eliminated the memory-bandwidth bottleneck for transformer attention, enabling context lengths up to millions of tokens on existing GPUs. It is now integrated into PyTorch, vLLM, SGLang, and virtually every production LLM serving stack.

### 2.2 FlashAttention-3: Asynchronous Low-Precision Attention on NVIDIA Hopper GPUs
- **Title:** FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-Precision
- **Authors:** Jay Shah et al. (Together AI / Tri Dao et al.)
- **Venue:** arXiv / Industry Release 2024
- **Year:** 2024
- **Why Milestone:** FlashAttention-3 exploits **Hopper-specific features** (WGMMA, TMA, FP8 Tensor Cores, asynchronous copy) to achieve up to **1.5–2x speedup** over FlashAttention-2 on H100 GPUs. It demonstrates that algorithm-hardware co-design—tailoring attention kernels to specific GPU generations—can extract significant performance even for the same mathematical operation. It also validated FP8 attention as production-ready, paving the way for Blackwell's FP4/FP6 attention pipelines.

### 2.3 vLLM / PagedAttention: Efficient Memory Management for LLM Serving
- **Title:** Efficient Memory Management for Large Language Model Serving with PagedAttention
- **Authors:** Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, et al. (UC Berkeley / vLLM Team)
- **Venue:** SOSP 2023
- **Year:** 2023
- **Why Milestone:** PagedAttention introduced **virtual-memory-inspired paging** for KV-cache management, eliminating memory fragmentation and enabling near-optimal GPU memory utilization. This allowed batch sizes to increase by 2–4x, directly translating to throughput gains. vLLM has become the **de facto open-source LLM serving engine**, adopted by NVIDIA (TensorRT-LLM integration), AWS, and dozens of AI startups. It demonstrated that systems-level innovation (memory management) can outperform raw hardware FLOPS for inference economics.

### 2.4 Speculative Decoding: Fast Inference from Transformers via Speculative Decoding
- **Title:** Fast Inference from Transformers via Speculative Decoding
- **Authors:** Yaniv Leviathan, Matan Kalman, Yossi Matias (Google Research)
- **Venue:** ICML 2023
- **Year:** 2023
- **Why Milestone:** Speculative decoding uses a small **draft model** to generate candidate tokens, which the large target model verifies in parallel. It achieves **2–3x latency reduction** without quality degradation, inspired by hardware speculative execution. This paper opened a major research direction (Medusa, Lookahead Decoding, Sequoia, etc.) and is now deployed in production systems including Google Cloud TPUs and vLLM. It proved that algorithmic redundancy exploitation can overcome memory-bandwidth-bound decoding.

### 2.5 SGLang: Efficient Execution of Structured Language Model Programs
- **Title:** SGLang: Efficient Execution of Structured Language Model Programs
- **Authors:** Lianmin Zheng et al. (UC Berkeley / LMSYS)
- **Venue:** NeurIPS 2024 (System Demonstration / Workshop)
- **Year:** 2024
- **Why Milestone:** SGLang introduced **RadixAttention**, a radix-tree-based KV cache management system that enables automatic prefix sharing across conversations without explicit fork bookkeeping. It also provides a structured generation runtime that co-optimizes LLM programs with execution. SGLang has emerged as a major alternative to vLLM, demonstrating that KV cache management algorithms (not just memory paging) can fundamentally change inference economics for multi-turn and agentic workloads.

### 2.6 DistServe: Disaggregating Prefill and Decoding for Goodput-Optimized LLM Serving
- **Title:** DistServe: Disaggregating Prefill and Decoding for Goodput-Optimized Large Language Model Serving
- **Authors:** Yichao Zhang et al. (Peking University / ByteDance)
- **Venue:** OSDI 2024
- **Year:** 2024
- **Why Milestone:** DistServe demonstrated that **phase disaggregation**—running prefill (compute-bound) and decode (memory-bandwidth-bound) on separate GPU pools—can improve goodput by 1.5–2.5x over co-located serving. This architectural insight has influenced cloud LLM serving designs (e.g., Mooncake, Splitwise) and is now supported by vLLM and major cloud providers. It highlights that treating LLM inference as a heterogeneous pipeline, not a uniform batch, is critical for datacenter efficiency.

---

## 3. In-Memory & Analog Computing (CIM / PIM)

### 3.1 IBM Analog AI Chip: A 64-Core Mixed-Signal In-Memory Compute Chip
- **Title:** A 64-Core Mixed-Signal In-Memory Compute Chip Based on Phase-Change Memory for Deep Neural Network Inference
- **Authors:** M. Le Gallo, R. Khaddam-Aljameh, et al. (IBM Research)
- **Venue:** Nature Electronics, 2023
- **Year:** 2023
- **Why Milestone:** IBM's chip integrated **64 million PCM (phase-change memory) cells** with 64 parallel in-memory compute cores, achieving **2.6 TOPS/W** measured efficiency on ResNet-50 with accuracy within 0.5% of floating-point baseline. It demonstrated fewer than one error per 10 billion inference operations, a critical precision benchmark for analog computing. This work established PCM-based analog computing as a viable path for production-grade AI inference, and IBM open-sourced the Aihwkit framework to enable community research.

### 3.2 Nature 2022: A Compute-in-Memory Chip Based on Resistive RAM (ReRAM)
- **Title:** A Compute-in-Memory Chip Based on Resistive Random-Access Memory
- **Authors:** W. Wan et al. (Tsinghua University / related collaboration)
- **Venue:** Nature, 2022
- **Year:** 2022 (Continued Impact 2023–2025)
- **Why Milestone:** This paper demonstrated a fully integrated **ReRAM-based compute-in-memory chip** with multi-bit MAC operations performed directly in the memory array, achieving high energy efficiency for edge AI. As one of the first complete system demonstrations of ReRAM CIM, it catalyzed a wave of follow-on work in analog CIM architectures and remains a reference design for ReRAM-based AI accelerators.

### 3.3 Samsung HBM-PIM / SK hynix AiM: Processing-in-Memory for AI
- **Title:** HBM-PIM: Processing-in-Memory for Deep Learning (Industry papers and ISSCC presentations)
- **Authors:** Samsung Advanced Institute of Technology / SK hynix Engineering
- **Venue:** ISSCC 2022 / HotChips 2023 / Industry Publications
- **Year:** 2022–2023 (Production ramp 2024–2025)
- **Why Milestone:** HBM-PIM (Samsung) and AiM (Accelerator-in-Memory, SK hynix) embedded **lightweight processing units inside HBM stacks**, enabling near-data processing for matrix operations. Samsung's HBM-PIM demonstrated 2.3x system performance and 62% energy reduction on GPT-2. These represent the first commercial **processing-in-memory (PIM)** products integrated into high-bandwidth memory, addressing the memory wall for datacenter AI by moving compute closer to data.

### 3.4 TetraMem / Memristor with Thousands of Conductance Levels (Nature 2023)
- **Title:** Thousands of Conductance Levels in Memristors Integrated on CMOS
- **Authors:** M. Y. Rao et al. (TetraMem / collaborating institutions)
- **Venue:** Nature, 2023
- **Year:** 2023
- **Why Milestone:** This paper demonstrated memristors with **thousands of stable conductance levels** (effectively >10 bits of analog precision), far exceeding the 4–6 bits typical of previous ReRAM/PCM devices. High-precision analog weights enable higher accuracy for neural network inference without frequent digital correction. This breakthrough in device physics directly addresses the precision bottleneck that has limited analog CIM to low-accuracy edge tasks, opening the door to analog accelerators for more demanding AI workloads.

### 3.5 Nature 2023: Edge Learning Using a Fully Integrated Neuro-Inspired Memristor Chip
- **Title:** Edge Learning Using a Fully Integrated Neuro-Inspired Memristor Chip
- **Authors:** W. Zhang et al.
- **Venue:** Science, 2023
- **Year:** 2023
- **Why Milestone:** A fully integrated memristor chip capable of **on-chip learning** (not just inference) at the edge, demonstrating that neuro-inspired hardware can perform local weight updates without external memory access. This is a critical step toward autonomous edge AI systems that adapt to their environment without cloud connectivity.

### 3.6 ISSCC 2024: A 22nm 16Mb Floating-Point ReRAM CIM Macro with 31.2 TFLOPS/W
- **Title:** A 22nm 16Mb Floating-Point ReRAM Compute-in-Memory Macro with 31.2 TFLOPS/W for AI Edge Devices
- **Authors:** T. H. Wen et al.
- **Venue:** ISSCC 2024
- **Year:** 2024
- **Why Milestone:** This work demonstrated **floating-point ReRAM compute-in-memory** at 22nm, achieving 31.2 TFLOPS/W—among the highest energy efficiencies reported for any AI accelerator. Floating-point support is critical for training and higher-precision inference, and this paper showed that analog CIM can support formats beyond low-bit integer quantization.

### 3.7 Science 2024: Fusion of Memristor and Digital CIM
- **Title:** Fusion of Memristor and Digital Compute-in-Memory Processing for Energy-Efficient Edge Computing
- **Authors:** T. H. Wen et al.
- **Venue:** Science, 2024
- **Year:** 2024
- **Why Milestone:** This paper proposed a **hybrid architecture** fusing memristor-based analog CIM with digital CIM in a single system, leveraging the strengths of both: analog for energy-efficient inference, digital for precision-critical operations. It demonstrated that heterogeneous CIM approaches can achieve better energy-accuracy tradeoffs than pure analog or pure digital designs alone.

---

## 4. Neuromorphic Computing

### 4.1 Nature 2025: Neuromorphic Computing at Scale
- **Title:** Neuromorphic Computing at Scale
- **Authors:** D. Kudithipudi, C. Schuman, C. M. Vineyard, et al.
- **Venue:** Nature, 2025
- **Year:** 2025
- **Why Milestone:** This comprehensive perspective article laid out the **roadmap for large-scale neuromorphic computing**, identifying near-term, medium-term, and long-term research questions. It argued that now is the ideal time to invest in scaling neuromorphic systems from lab prototypes to datacenter deployments, as both natural and AI systems would benefit. The paper was highly influential in framing neuromorphic computing as a complement—not replacement—to conventional AI accelerators, and catalyzed interdisciplinary discussions across materials, devices, circuits, and algorithms.

### 4.2 Intel Loihi 2: A New Generation of Neuromorphic Research Chip
- **Title:** Intel Loihi 2: A Neuromorphic Research Chip with On-Chip Learning and Microsecond Latency
- **Authors:** Intel Labs Neuromorphic Research Group
- **Venue:** Intel Technical White Paper / NeurIPS Workshop 2023 / ICLR 2025 Workshop
- **Year:** 2023 (Volume Research Deployment)
- **Why Milestone:** Loihi 2 is the **most advanced digital neuromorphic processor** available to researchers, supporting event-based spiking neural networks (SNNs) with on-chip learning and microsecond-latency inference. It has been used to demonstrate neuromorphic principles for efficient LLMs (ICLR 2025 workshop paper) and autonomous driving (NeurIPS 2024). As the primary platform for neuromorphic algorithm research, Loihi 2 enables exploration of brain-inspired computation that could inform next-generation low-power AI hardware.

### 4.3 Nature 2023: An Analog-AI Chip for Energy-Efficient Speech Recognition and Transcription
- **Title:** An Analog-AI Chip for Energy-Efficient Speech Recognition and Transcription
- **Authors:** S. Ambrogio et al. (IBM Research)
- **Venue:** Nature, 2023
- **Year:** 2023
- **Why Milestone:** IBM's analog AI chip demonstrated **end-to-end speech recognition and transcription** using phase-change memory-based in-memory computing, achieving orders-of-magnitude energy reduction over digital baselines. This was one of the first demonstrations of analog AI processing a real-world, complex sensory stream (audio) with production-viable accuracy, proving that analog computing can handle non-trivial AI applications beyond toy benchmarks.

### 4.4 Nature 2024: Hardware Implementation of Memristor-Based Artificial Neural Networks
- **Title:** Hardware Implementation of Memristor-Based Artificial Neural Networks
- **Authors:** F. Aguirre et al.
- **Venue:** Nature Communications, 2024
- **Year:** 2024
- **Why Milestone:** This paper presented a comprehensive **hardware implementation of memristor-based neural networks** with detailed characterization of device variability, endurance, and accuracy tradeoffs. It provided a rigorous experimental baseline for memristor-based neuromorphic hardware, addressing reproducibility concerns that have plagued the field. The work advanced memristor technology from proof-of-concept demonstrations toward reliable building blocks for neuromorphic systems.

### 4.5 Neuromorphic Photonics: Roadmap and Integrated Implementations
- **Title:** Roadmap on Neuromorphic Photonics
- **Authors:** D. Brunner, B. J. Shastri, M. A. A. Qudasi, et al.
- **Venue:** arXiv:2501.07917 (Survey / Roadmap)
- **Year:** 2025
- **Why Milestone:** This comprehensive roadmap surveyed the convergence of neuromorphic computing and photonics, identifying **spiking photonic neurons**, **optical synapses**, and **photonic reservoir computing** as key directions. It established neuromorphic photonics as a distinct sub-discipline with unique advantages (speed of light, ultra-low power, high bandwidth) over electronic neuromorphic systems, guiding research funding and industrial roadmaps in both Europe and Asia.

---

## 5. Photonic & Optical AI Accelerators

### 5.1 Nature 2025: An Integrated Large-Scale Photonic Accelerator with Ultralow Latency
- **Title:** An Integrated Large-Scale Photonic Accelerator with Ultralow Latency
- **Authors:** S. Hua et al.
- **Venue:** Nature, 2025 (Vol. 640)
- **Year:** 2025
- **Why Milestone:** This paper demonstrated a **fully integrated photonic accelerator** performing all key DNN computations entirely with light on a single chip, with no off-chip electronics required. The system achieved ultralow latency and high energy efficiency, demonstrating that photonic computing can handle modern AI workloads. It represents a milestone in moving photonic AI from laboratory demonstrations to integrated system prototypes.

### 5.2 Nature 2025: Universal Photonic Artificial Intelligence Acceleration
- **Title:** Universal Photonic Artificial Intelligence Acceleration
- **Authors:** S. R. Ahmed, R. Baghdadi, et al. (Lightmatter)
- **Venue:** Nature, 2025 (Vol. 640)
- **Year:** 2025
- **Why Milestone:** Lightmatter published results on a **universal photonic AI accelerator** capable of performing matrix multiplication—the core of AI inference—using light. The paper explicitly framed photonic computing as the answer to stalled Moore's Law, Dennard scaling, and memory scaling. As a venture-backed startup (>$800M raised), Lightmatter's publication in Nature lent credibility to the commercial viability of photonic AI, and the system demonstrated competitive performance with electronic accelerators on key benchmarks.

### 5.3 Science 2024: Large-Scale Photonic Chiplet Taichi (160 TOPS/W)
- **Title:** Large-Scale Photonic Chiplet Taichi Empowers 160-TOPS/W Artificial General Intelligence
- **Authors:** Z. Xu, T. Zhou, et al. (Tsinghua University)
- **Venue:** Science, 2024 (Vol. 384)
- **Year:** 2024
- **Why Milestone:** The Taichi chiplet achieved **160 TOPS/W**—one of the highest energy efficiencies ever reported for any AI accelerator—using a photonic architecture. It demonstrated that photonic computing can scale to large chiplet-based systems (not just single-die lab demos) and handle general AI tasks. This work established Chinese research leadership in photonic AI acceleration and proved that photonic chiplets can compete with electronic counterparts on energy efficiency.

### 5.4 Nature 2024: Partial Coherence Enhances Parallelized Photonic Computing
- **Title:** Partial Coherence Enhances Parallelized Photonic Computing
- **Authors:** B. Dong et al.
- **Venue:** Nature, 2024 (Vol. 632)
- **Year:** 2024
- **Why Milestone:** This paper demonstrated that **partially coherent light** can be harnessed to improve parallel processing in photonic tensor cores, addressing a key challenge in photonic computing: coherent light sources are power-hungry and sensitive to phase noise. By relaxing coherence requirements, the work makes photonic AI more practical for real-world deployment, reducing system complexity and power overhead.

### 5.5 Nature Reviews Physics 2023: The Physics of Optical Computing
- **Title:** The Physics of Optical Computing
- **Authors:** P. L. McMahon
- **Venue:** Nature Reviews Physics, 2023
- **Year:** 2023
- **Why Milestone:** This comprehensive review provided the **physical foundations** for optical computing as an AI acceleration paradigm, analyzing the fundamental limits of optical matrix multiplication, energy efficiency, and latency. It became the definitive reference for understanding why (and when) optical computing can outperform electronics, and has been cited by virtually every subsequent photonic AI paper. It established the intellectual framework for the field's rapid growth in 2024–2025.

---

## 6. Advanced Packaging, Chiplets & Interconnect for AI

### 6.1 IEEE Micro 2023: Memory Pooling with CXL
- **Title:** Memory Pooling with CXL
- **Authors:** Donghyun Gouk, Miryeong Kwon, Hanyeoreum Bae, Sangwon Lee, Myoungsoo Jung (KAIST)
- **Venue:** IEEE Micro, 2023
- **Year:** 2023
- **Why Milestone:** This paper proposed **directly accessible memory disaggregation** over CXL.mem, enabling hosts to access remote memory resources with cache-coherent semantics. For AI systems, this means GPU memory capacity can be expanded beyond HBM limits using CXL-attached DRAM pools. The work influenced CXL 3.0/3.1 adoption in AI servers and underpins emerging architectures where GPU, CPU, and accelerator memory are unified into a single fabric-addressable pool.

### 6.2 ISCA 2024 / HPCA 2024: PIM Is All You Need — CXL-Enabled GPU-Free LLM Inference
- **Title:** PIM Is All You Need: A CXL-Enabled GPU-Free System for Large Language Model Inference
- **Authors:** Yufeng Gu, Alireza Khadem, Sumanth Umesh, et al. (University of Michigan / Intel)
- **Venue:** arXiv 2025 / ISCA 2024 / HPCA 2024 (related works)
- **Year:** 2024–2025
- **Why Milestone:** This provocative work demonstrated that **processing-in-memory (PIM) combined with CXL memory pooling** can serve LLM inference without GPUs, by keeping weights and KV cache in disaggregated memory and performing computation near data. While not yet competitive with GPUs on all metrics, it opened a research direction questioning whether GPU-centric inference is necessary for memory-bound LLM decoding. The paper influenced CXL-PIM research at major memory vendors.

### 6.3 AMD MI300 / Intel Ponte Vecchio: Chiplet Architectures for AI
- **Title:** Advancing AI and HPC with Chiplet Architecture (AMD); Ponte Vecchio / Max Series GPU Architecture (Intel)
- **Authors:** AMD / Intel Architecture Teams
- **Venue:** ISSCC 2024 / HotChips 2023 / Industry Releases
- **Year:** 2023–2024
- **Why Milestone:** The MI300 and Ponte Vecchio represented the first **mass-produced chiplet-based AI accelerators** from major vendors (non-NVIDIA). MI300 used advanced packaging (2.5D/3D stacking) to integrate CPU, GPU, and HBM in a single package. These products validated that chiplet architectures—smaller dies yielding better manufacturing economics—can achieve competitive AI performance, and established advanced packaging as a critical technology vector for AI hardware scaling.

### 6.4 Meta 3D-Integrated AR SoC (ISSCC 2024)
- **Title:** A 3D Integrated Prototype System-on-Chip for Augmented Reality Applications Using Face-to-Face Wafer Bonded 7nm Logic at <2μm Pitch with up to 40% Energy Reduction at Iso-Area Footprint
- **Authors:** Tony F. Wu et al. (Meta)
- **Venue:** ISSCC 2024 (Invited Industry Session 11.2)
- **Year:** 2024
- **Why Milestone:** Meta demonstrated a **7nm AR SoC using face-to-face hybrid bonding** at sub-2μm pitch, enabling 3D stacking of logic and memory with 40% energy reduction. While targeted at AR, the hybrid-bonding technology is directly applicable to AI accelerators (as NVIDIA uses it for Blackwell's die-to-die interconnect). This paper validated that sub-2μm hybrid bonding is manufacturable at scale, a key enabler for future 3D-stacked AI chips.

---

## 7. Edge AI & TinyML Accelerators

### 7.1 ISSCC 2023 / 2024: Transformer Accelerators for Edge — C-Transformer, Kim et al.
- **Title:** C-Transformer: A 2.6–18.1 μJ/Token Homogeneous DNN-Transformer/Spiking-Transformer Processor with Big-Little Network and Implicit Weight Generation for Large Language Models
- **Authors:** S. Kim et al. (KAIST)
- **Venue:** ISSCC 2024
- **Year:** 2024
- **Why Milestone:** This chip demonstrated **homogeneous acceleration of both dense transformers and spiking transformers** on the same edge hardware, using big-little network architectures and implicit weight generation to reduce external memory access by 74–81%. It proved that edge processors can run LLM inference (not just CNNs) at sub-20 μJ/token, opening the door to on-device LLMs for mobile and IoT applications.

### 7.2 ISSCC 2023: ReDCIM / TranCIM — Reconfigurable Digital CIM Processors
- **Title:** ReDCIM: Reconfigurable Digital Computing-In-Memory Processor with Unified FP/INT Pipeline for Cloud AI Acceleration; TranCIM: Full-Digital Bitline-Transpose CIM-based Sparse Transformer Accelerator
- **Authors:** F. Tu, Y. Wang, Z. Wu, et al. (Tsinghua / HKUST)
- **Venue:** ISSCC 2022 / JSSC 2023 (Extensions); ISSCC 2023
- **Year:** 2022–2023
- **Why Milestone:** These papers from the Tsinghua/HKUST group demonstrated **reconfigurable digital compute-in-memory (CIM)** supporting both FP16 and INT8 in a unified pipeline, achieving 29.2 TFLOPS/W (BF16) and 36.5 TOPS/W (INT8) in 28nm. TranCIM specifically targeted sparse transformer acceleration with bitline-transpose architectures. The ReDCIM/TranCIM family was recognized as a **2023 Top-10 Research Advance in China Semiconductors** and set the efficiency benchmark for cloud CIM processors.

### 7.3 ISSCC 2023: MuTCIM — Multimodal Transformer CIM Accelerator
- **Title:** MuTCIM: A 28nm 2.24 μJ/Token Attention-Token-Bit Hybrid Sparse Digital CIM-based Accelerator for Multimodal Transformers
- **Authors:** F. Tu, Z. Wu, Y. Wang, et al.
- **Venue:** ISSCC 2023 (Highlight Paper)
- **Year:** 2023
- **Why Milestone:** MuTCIM was the **first CIM accelerator specifically designed for multimodal transformers** (vision + language), exploiting hybrid sparsity across attention, token, and bit dimensions. At 2.24 μJ/token in 28nm, it demonstrated that CIM can efficiently handle the heterogeneous computation patterns of multimodal AI, not just homogeneous CNN or transformer layers. This was a Highlight Paper at ISSCC 2023.

### 7.4 ISSCC 2024: TensorCIM — Multi-Chip-Module CIM Tensor Processor
- **Title:** TensorCIM: Digital Computing-In-Memory Tensor Processor with Multi-Chip-Module-based Architecture for Beyond-NN Acceleration
- **Authors:** Y. Wang, Z. Wu, W. Wu, L. Liu, Y. Hu, S. Wei, F. Tu, S. Yin
- **Venue:** JSSC 2025 (ISSCC 2023 Extension)
- **Year:** 2025 (Journal Extension)
- **Why Milestone:** TensorCIM extended CIM beyond neural networks to **general tensor operations** (matrix factorization, graph analytics) using a multi-chip-module architecture. It demonstrated that digital CIM can be a general-purpose acceleration fabric, not just a DNN-specialized coprocessor, broadening the applicability of in-memory computing.

### 7.5 Nature 2024: Crossmodal Sensory Neurons Based on Flexible Memristors
- **Title:** Crossmodal Sensory Neurons Based on High-Performance Flexible Memristors for Human-Machine In-Sensor Computing System
- **Authors:** Z. Li et al.
- **Venue:** Nature Communications, 2024
- **Year:** 2024
- **Why Milestone:** This work demonstrated **flexible memristor-based in-sensor computing** that can perform crossmodal sensory processing (vision + touch) directly at the sensor level, eliminating data movement from sensor to processor. It represents a new paradigm for edge AI where sensing and computation are co-located, with applications in robotics, prosthetics, and wearable AI.

---

## 8. Hardware-Software Co-Design & Compilation

### 8.1 Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations
- **Title:** Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations
- **Authors:** P. Tillet, H. Kung, D. Cox
- **Venue:** MAPL 2019 (Major adoption 2023–2025)
- **Year:** 2019 (Milestone impact in 2023–2025)
- **Why Milestone:** Triton became the **de facto open-source GPU kernel development framework** for AI in 2023–2025, with OpenAI Triton and PyTorch 2.0's torch.compile relying on it for custom kernel generation. It democratized GPU kernel writing—previously requiring CUDA expertise—enabling AI researchers to write custom attention, conv, and quantization kernels in Python-like syntax. Triton is now the compilation target for FlashAttention, vLLM, and many custom LLM kernels.

### 8.2 ISCA 2023: FACT — FFN-Attention Co-optimized Transformer Architecture
- **Title:** FACT: FFN-Attention Co-optimized Transformer Architecture with Eager Correlation Prediction
- **Authors:** Y. Qin et al.
- **Venue:** ISCA 2023
- **Year:** 2023
- **Why Milestone:** FACT co-optimized the transformer architecture and hardware mapping, demonstrating that **algorithmic changes to FFN and attention patterns** can reduce memory traffic and improve hardware utilization by 20–40%. This paper exemplified the hardware-software co-design paradigm for LLMs, where model architecture is designed with hardware costs (memory bandwidth, compute unit occupancy) in mind, rather than treating hardware as a passive execution substrate.

### 8.3 ICLR 2024 / NeurIPS 2024: AQLM, AWQ, BiLLM — Extreme Quantization for LLMs
- **Title:** AQLM: Extreme Compression of Large Language Models via Additive Quantization (ICML 2024); AWQ: Activation-aware Weight Quantization for LLM Compression (MLSys 2024); BiLLM: Pushing the Limit of Post-Training Quantization for LLMs (NeurIPS 2024); VPTQ: Extreme Low-bit Vector Post-Training Quantization (NeurIPS 2024)
- **Authors:** Various (OpenAI, MIT, Tsinghua, etc.)
- **Venue:** ICML 2024 / MLSys 2024 / NeurIPS 2024
- **Year:** 2024
- **Why Milestone:** These papers pushed LLM quantization to **sub-4-bit weights** (2-bit, 1-bit in some cases) with minimal accuracy loss, enabling LLM inference on consumer GPUs and edge devices. AQLM and VPTQ demonstrated that extreme quantization is viable for production models, directly influencing NVIDIA's Blackwell FP4/FP6 support and edge AI chip roadmaps. They represent the algorithmic foundation for the low-precision inference revolution.

### 8.4 DeepSeek-V3 / Hardware-Software Co-Design for MoE Training
- **Title:** DeepSeek-V3 Technical Report; Insights into DeepSeek-V3: Scaling Challenges and Reflections on Hardware for AI Architectures
- **Authors:** DeepSeek-AI / ISCA 2025 Industry Track
- **Venue:** arXiv 2024 / ISCA 2025 (Industry Track)
- **Year:** 2024–2025
- **Why Milestone:** DeepSeek-V3 trained a 671B-parameter MoE model for ~$5.6M using **FP8 mixed precision, optimized communication schedules, and hardware-aware expert parallelism** on NVIDIA H800 clusters. The ISCA 2025 industry track paper explicitly reflected on hardware limitations (bandwidth bottlenecks, communication overhead) that shaped the algorithmic design. It demonstrated that algorithmic innovation (not just more hardware) can achieve frontier model training at 1/10th the cost, and forced a re-evaluation of AI training economics across the industry.

---

## Summary Statistics

| Category | Count | Notes |
|----------|-------|-------|
| Datacenter GPU/TPU/ASIC | 10 | NVIDIA, Google, AMD, Cerebras, Groq, Tesla, SambaNova |
| LLM Inference Systems | 6 | FlashAttention, vLLM, SGLang, Speculative Decoding, DistServe |
| In-Memory / Analog Computing | 7 | IBM, ReRAM, PCM, Samsung HBM-PIM, TetraMem |
| Neuromorphic Computing | 5 | Intel Loihi 2, IBM Analog, Nature Reviews |
| Photonic / Optical Computing | 5 | Lightmatter, Tsinghua Taichi, Nature 2025 papers |
| Packaging / Interconnect / CXL | 4 | CXL pooling, chiplet architectures, 3D bonding |
| Edge AI / TinyML | 5 | ISSCC CIM papers, flexible memristors, KAIST transformers |
| Hardware-Software Co-Design | 4 | Triton, FACT, AQLM/AWQ, DeepSeek-V3 |
| **Total** | **~46** | Foundation + milestone papers |

---

## Research Methodology

This compilation was generated through systematic web searches across:
- **Conference proceedings:** ISSCC, ISCA, MICRO, HPCA, ASPLOS, HotChips, NeurIPS, ICML, ICLR, OSDI, SOSP, DAC
- **Journals:** Nature, Nature Electronics, Nature Communications, Nature Reviews Physics, Science, JSSC, IEEE Micro
- **Industry sources:** NVIDIA White Papers, Google Cloud Blogs, AMD Technical Briefs, Cerebras/Groq/SambaNova publications
- **Survey repositories:** GitHub awesome-lists (Neural-Networks-on-Silicon, Awesome-Efficient-LLM, etc.)
- **Patent and roadmap analyses:** Yole Group, Patsnap, TechInsights, SEMI

Papers were selected based on:
1. **Foundational impact:** Opened a new research direction or validated a new paradigm
2. **Industry adoption:** Deployed in production systems or influenced commercial product roadmaps
3. **Citations and recognition:** Best papers, highlight papers, awards, or rapidly growing citation counts
4. **Technical breadth:** Hardware architecture, device physics, systems software, or algorithm-hardware co-design
5. **Time range:** 2023 to mid-2026 (July 2026), with a few 2022 papers included if their peak impact occurred in the 2023–2026 window

---

*Compiled: July 2026*
*Curator: AI Hardware Research Agent*
*Workspace: C:/Git-repo-my/AIResearchVault/document/AI Hardware/*
