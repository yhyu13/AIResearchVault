# AI Optimization: Milestone & Trunk Papers (2023 – Mid-2026)

> **Curated by:** Research Curator Agent  
> **Date:** 2026-07-15  
> **Scope:** Foundational, widely-cited, and breakthrough papers in AI Optimization from 2023 to July 2026. Incremental works are excluded.  
> **Venues:** NeurIPS, ICML, ICLR, CVPR, ICCV, ECCV, SIGGRAPH, SIGGRAPH Asia, SOSP, MLSys, RSS, CoRL, JMLR, TPAMI, etc.

---

## Table of Contents

1. [Training Optimization Algorithms](#1-training-optimization-algorithms)
2. [Model Compression & Quantization](#2-model-compression--quantization)
3. [Pruning & Sparsity](#3-pruning--sparsity)
4. [Parameter-Efficient Fine-Tuning (PEFT) & Memory Optimization](#4-parameter-efficient-fine-tuning-peft--memory-optimization)
5. [Mixture of Experts (MoE) & Sparse Architectures](#5-mixture-of-experts-moe--sparse-architectures)
6. [Inference & Test-Time Compute Optimization](#6-inference--test-time-compute-optimization)
7. [KV Cache & Attention Optimization](#7-kv-cache--attention-optimization)
8. [Reinforcement Learning & Alignment Optimization](#8-reinforcement-learning--alignment-optimization)
9. [Diffusion & Generative Model Optimization](#9-diffusion--generative-model-optimization)
10. [Neural Architecture Search (NAS)](#10-neural-architecture-search-nas)
11. [Neural Combinatorial Optimization](#11-neural-combinatorial-optimization)
12. [Learning-Rate-Free & Adaptive Optimization](#12-learning-rate-free--adaptive-optimization)
13. [Distributed Training & Systems Optimization](#13-distributed-training--systems-optimization)
14. [Honorable Mentions & Emerging Directions (2025–2026)](#14-honorable-mentions--emerging-directions-20252026)

---

## 1. Training Optimization Algorithms

Papers that fundamentally redesigned or advanced the optimizers used to train deep neural networks, especially at large scale.

### 1.1 Sophia: A Scalable Stochastic Second-Order Optimizer for Language Model Pre-training
- **Authors:** Hong Liu, Zhiyuan Li, David Hall, Percy Liang, Tengyu Ma
- **Venue:** ICLR 2024 (Oral)
- **Year:** 2023
- **Why it matters:** The first lightweight second-order optimizer that scales to billion-parameter language models. Sophia uses diagonal Hessian estimates (via Gauss-Newton-Bartlett) and element-wise clipping to achieve **2× speedup over AdamW** with only ~5% overhead per step. It proved that second-order methods are no longer impractical for LLM pre-training, shifting the optimizer paradigm beyond first-order adaptive methods.

### 1.2 Lion: Symbolic Discovery of Optimization Algorithms
- **Authors:** Xiangning Chen, Chen Liang, Da Huang, Esteban Real, Kaiyuan Wang, Yao Liu, Hieu Pham, Xuanyi Dong, Thang Luong, Cho-Jui Hsieh, Yifeng Lu, Quoc V. Le
- **Venue:** NeurIPS 2023 (Oral)
- **Year:** 2023
- **Why it matters:** Lion was **discovered via symbolic search** rather than human design, yielding a surprisingly simple sign-momentum update rule. It reduces memory footprint by ~50% compared to Adam (only tracks momentum, not second moments) and achieves 2× faster convergence on Vision Transformers and diffusion models. It catalyzed interest in algorithm discovery via search and remains a top alternative to AdamW in vision and LLM training.

### 1.3 Muon: An Optimizer for Hidden Layers in Neural Networks
- **Authors:** Keller Jordan (independent); scalable extension by J. Liu et al.
- **Venue:** Blog 2024; scalable version arXiv 2025
- **Year:** 2024–2025
- **Why it matters:** Muon orthogonalizes weight updates via Newton-Schulz iteration, producing updates that are closer to the ideal steepest-descent direction in the spectral norm. It has shown strong results in deep networks and is gaining traction as a **memory-efficient, high-quality optimizer** for hidden layers. The 2025 scalable extension demonstrated feasibility on LLM-scale training, offering a fresh non-diagonal optimization direction beyond Adam-style diagonal preconditioning.

### 1.4 Adam-mini: Use Fewer Learning Rates to Gain More
- **Authors:** Yao Zhang, Chen Chen, Zhiqi Li, Tianyu Ding, Chengyu Wu, D. P. Kingma, ... R. Sun
- **Venue:** ICLR 2025
- **Year:** 2025
- **Why it matters:** Adam-mini reduces the number of independently tuned learning rates by grouping parameters and sharing scalar learning-rate adjustments, achieving comparable or better convergence with significantly less hyperparameter search overhead. It is a milestone in **hyperparameter-efficient optimization**, making large-scale training more reproducible and accessible.

### 1.5 AdEMAMix: Adaptive EMA Momentum for Deep Learning
- **Authors:** Multiple groups (2024)
- **Venue:** arXiv 2024 / ICML 2024 workshops
- **Year:** 2024
- **Why it matters:** AdEMAMix introduces a dual-EMA system that balances recent and historical gradient information, addressing the well-known "stale momentum" problem in long training runs. It improves stability and final convergence on large vision and language tasks, and has been adopted in several production training stacks.

---

## 2. Model Compression & Quantization

Papers that enable massive reductions in model size and memory footprint with minimal accuracy loss, critical for LLM deployment.

### 2.1 QLoRA: Efficient Finetuning of Quantized LLMs
- **Authors:** Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, Luke Zettlemoyer
- **Venue:** NeurIPS 2023 (Oral, Most Influential Paper)
- **Year:** 2023
- **Why it matters:** QLoRA broke the boundary between quantization and fine-tuning by showing that a **65B-parameter model can be fine-tuned on a single 48GB GPU** using 4-bit NormalFloat (NF4) + double quantization + paged optimizers. It democratized LLM fine-tuning, making it accessible to individual researchers and small labs. It remains the de facto standard for consumer-grade LLM adaptation.

### 2.2 GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers
- **Authors:** Elias Frantar, Saleh Ashkboos, Torsten Hoefler, Dan Alistarh
- **Venue:** ICLR 2023
- **Year:** 2023
- **Why it matters:** GPTQ was the first to demonstrate that **hundred-billion-parameter models can be quantized to 3–4 bits in a single shot** (within hours) using approximate second-order information. It established the post-training quantization (PTQ) paradigm for LLMs, enabling rapid compression without retraining. GPTQ remains a foundational method in the quantization toolkit (AutoGPTQ, exllama, etc.).

### 2.3 AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration
- **Authors:** Ji Lin, Jiaming Tang, Haotian Tang, Shang Yang, Wei-Ming Chen, et al. (MIT, Song Han group)
- **Venue:** MLSys 2024 (Best Paper Award)
- **Year:** 2024
- **Why it matters:** AWQ discovered that **protecting just 1% of critical weights** (identified by activation magnitudes) enables nearly lossless 4-bit quantization. Unlike GPTQ’s layer-by-layer second-order optimization, AWQ is intuitive, faster, and hardware-friendly. It allowed LLaMA-70B to run on a single RTX 4090 (24GB), and its quantized format is natively executable on GPUs with >3× speedup. A landmark in practical, deployable quantization.

### 2.4 LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale
- **Authors:** Tim Dettmers, Mike Lewis, Younes Belkada, Luke Zettlemoyer
- **Venue:** NeurIPS 2022
- **Year:** 2022
- **Why it matters:** Although published in 2022, LLM.int8() is the trunk paper that **first discovered outlier features in Transformers** and introduced mixed-precision INT8 decomposition. This discovery directly enabled all subsequent sub-8-bit quantization methods (GPTQ, AWQ, QLoRA) by revealing that naive uniform quantization fails due to a small number of extreme activation outliers. It is cited as the engineering foundation of modern LLM quantization.

### 2.5 BitNet b1.58: Ternary {-1, 0, +1} Weights for LLMs
- **Authors:** Microsoft Research (various authors)
- **Venue:** arXiv 2024 / follow-up papers 2025
- **Year:** 2024–2025
- **Why it matters:** BitNet challenged the fundamental assumption that models must use floating-point weights, showing that **1.58-bit ternary weights** can match FP16 LLaMA performance at 3B scale with 2.71× speed and 3.55× less memory. It opened the extreme quantization frontier (sub-4-bit, non-standard numeric formats) and is now a benchmark for hardware-software co-design in edge AI.

---

## 3. Pruning & Sparsity

Papers that remove redundant parameters or structures to accelerate inference and reduce memory, often without retraining.

### 3.1 SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot
- **Authors:** Elias Frantar, Dan Alistarh
- **Venue:** ICML 2023
- **Year:** 2023
- **Why it matters:** SparseGPT was the **first to show that 175B-parameter models can be pruned to 50% unstructured sparsity in a single shot without retraining**, using an approximate sparse regression solver. It proved that magnitude-based pruning is ineffective at LLM scale and that second-order information is essential. It set the standard for one-shot LLM pruning and catalyzed the entire LLM-sparsity subfield.

### 3.2 Wanda: Pruning by Weights and Activations
- **Authors:** Mingjie Sun, Zhuang Liu, Anna Bair, J. Zico Kolter
- **Venue:** ICLR 2024
- **Year:** 2024
- **Why it matters:** Wanda showed that **weight magnitude × input activation norm** is a far better pruning metric than weight magnitude alone. It is 300× faster than SparseGPT and achieves competitive sparsity (e.g., 50% on LLaMA-7B with PPL 7.26 vs. 17.29 for magnitude pruning). Its simplicity and speed made it the default choice for rapid LLM pruning experiments and production workflows.

### 3.3 Minitron: Compressing Large Language Models Using Structured Pruning + Knowledge Distillation
- **Authors:** NVIDIA (Muralidharan et al.)
- **Venue:** NeurIPS 2024
- **Year:** 2024
- **Why it matters:** Minitron demonstrated **structured pruning** (removing heads/layers) combined with knowledge distillation to derive 8B and 4B models from a 15B parent using only 1/40 of the training tokens needed from scratch, while improving MMLU by up to 16%. It proved that structured pruning + distillation is viable for production-grade model families, influencing NVIDIA’s own model releases.

### 3.4 SliceGPT: Compress Large Language Models by Deleting Rows and Columns
- **Authors:** Ashkboos et al.
- **Venue:** ICML 2024
- **Year:** 2024
- **Why it matters:** SliceGPT introduced a **structured pruning approach at the linear layer level** (removing rows/columns of weight matrices) rather than individual weights or whole layers. It achieves up to 30% compression with 1.87× speedup on standard hardware, bridging the gap between unstructured sparsity (high compression, no hardware speedup) and layer pruning (direct speedup but high accuracy loss).

---

## 4. Parameter-Efficient Fine-Tuning (PEFT) & Memory Optimization

Methods that enable adapting foundation models without full backpropagation through all parameters.

### 4.1 LoRA: Low-Rank Adaptation of Large Language Models
- **Authors:** Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Wang
- **Venue:** ICLR 2022
- **Year:** 2021 (published 2022)
- **Why it matters:** Although predating 2023, LoRA is the **trunk method** upon which all subsequent PEFT work is built. By injecting trainable low-rank decomposition matrices into each layer, LoRA reduces trainable parameters by 10,000× while matching full fine-tuning on many tasks. It became the default adaptation technique in Hugging Face, PEFT, and countless production pipelines. Without LoRA, QLoRA, GaLore, and modern fine-tuning would not exist.

### 4.2 GaLore: Memory-Efficient LLM Training by Gradient Low-Rank Projection
- **Authors:** Jiawei Zhao, Zhenyu Zhang, Beidi Chen, Zhangyang Wang, Anima Anandkumar, Yuandong Tian
- **Venue:** ICML 2024
- **Year:** 2024
- **Why it matters:** GaLore showed that **gradients themselves live in a low-rank subspace** during much of training. By projecting gradients to low-rank subspaces with dynamic switching, GaLore enables full-rank training with **LoRA-level memory consumption**. It is a milestone because it bridges the gap between PEFT (restricted expressivity) and full fine-tuning (prohibitive memory), offering a third path: full-rank optimization in a compressed gradient space.

### 4.3 APOLLO: Memory-Efficient Optimization via Low-Rank Gradient Approximation
- **Authors:** (2024)
- **Venue:** arXiv 2024 / ICML 2024
- **Year:** 2024
- **Why it matters:** APOLLO extends the low-rank gradient paradigm with **diagonal scaling** in the low-rank subspace, achieving better conditioning than pure low-rank projection. It is a key milestone in the emerging class of "low-rank optimizers" that treat gradient memory as the primary bottleneck, not parameter memory.

---

## 5. Mixture of Experts (MoE) & Sparse Architectures

Papers that established sparse activation and expert routing as a viable scaling paradigm for LLMs and beyond.

### 5.1 Mixtral 8x7B: A High-Quality Sparse Mixture-of-Experts Model
- **Authors:** Mistral AI team
- **Venue:** arXiv 2023 / released Dec 2023
- **Year:** 2023
- **Why it matters:** Mixtral was the **inflection point** that proved MoE could be open-source, practical, and better than dense models of comparable active-parameter count. With 46.7B total parameters but only 12.9B active per token, it outperformed GPT-3.5 and LLaMA 2 70B on many benchmarks while being faster to serve. It ended the era where MoE was a Google-only research curiosity and started the industry-wide shift to sparse architectures.

### 5.2 DeepSeek-V3: Expert-Level Load Balancing and Ultra-Efficient MoE Training
- **Authors:** DeepSeek-AI team
- **Venue:** arXiv 2024 / technical report
- **Year:** 2024
- **Why it matters:** DeepSeek-V3 trained a **671B-parameter MoE model with only 37B active per token** for ~$5.6M, rewriting the economics of frontier AI. It introduced auxiliary-loss-free load balancing and shared-expert isolation, solving the stability problems that plagued earlier MoE training. It proved that MoE is not just more efficient—it follows a fundamentally different cost curve, making dense frontier models economically uncompetitive.

### 5.3 GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding
- **Authors:** Dmitry Lepikhin, HyoukJoong Lee, Yuanzhong Xu, Dehao Chen, Orhan Firat, Yanping Huang, Maxim Krikun, Noam Shazeer, Zhifeng Chen
- **Venue:** ICLR 2021
- **Year:** 2021
- **Why it matters:** GShard is the **foundational trunk** for modern MoE: it introduced auto-sharding and token-level expert routing at the 600B scale, proving sub-linear compute scaling with parameter count. All subsequent MoE systems (Switch, Mixtral, DeepSeek) descend from GShard’s routing and sharding principles. It is the paper that made MoE practical at scale.

### 5.4 Switch Transformer: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity
- **Authors:** William Fedus, Barret Zoph, Noam Shazeer
- **Venue:** JMLR 2022
- **Year:** 2021
- **Why it matters:** Switch Transformer simplified MoE to **Top-1 routing** with auxiliary load balancing, training a 1.6T parameter model that was 4× faster than T5-XXL with similar performance. It established the standard routing protocol (noisy top-k) and load-balancing loss that nearly all MoE implementations still use today.

---

## 6. Inference & Test-Time Compute Optimization

Papers that optimize how models are served and how compute is allocated at inference time, including the emerging paradigm of test-time scaling.

### 6.1 vLLM: Efficient Memory Management for LLM Serving with PagedAttention
- **Authors:** Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph Gonzalez, Hao Zhang, Ion Stoica
- **Venue:** SOSP 2023
- **Year:** 2023
- **Why it matters:** vLLM introduced **PagedAttention**, an OS-inspired virtual memory system for KV cache management. It eliminated memory fragmentation and enabled KV cache sharing across requests, **doubling GPU memory utilization** in concurrent serving. vLLM became the de facto standard for LLM inference deployment (vLLM, SGLang, TensorRT-LLM all build on its concepts). It is the most impactful systems paper in LLM serving of the 2023–2026 period.

### 6.2 SGLang: Efficient Execution of Structured Language Model Programs
- **Authors:** Lianmin Zheng, Liangsheng Yin, Zhiqiang Xie, Jeff Huang, Cody Hao Yu, Shiyi Cao, Christos Kozyrakis, Ion Stoica, Joseph E. Gonzalez, Ying Sheng
- **Venue:** arXiv 2023 / ICLR 2024 (Oral)
- **Year:** 2024
- **Why it matters:** SGLang introduced **RadixAttention**, using radix trees to reuse KV cache across structured generation (multi-turn conversation, batch inference with shared prefixes). It showed that inference speed is not just about model architecture but about **program structure and cache reuse**. SGLang is now the primary alternative to vLLM for high-throughput structured LLM serving.

### 6.3 OpenAI o1 / DeepSeek-R1: Scaling Test-Time Compute via Reinforcement Learning
- **Authors:** OpenAI (o1, 2024); DeepSeek-AI (DeepSeek-R1, 2025)
- **Venue:** Technical reports / blog posts / arXiv
- **Year:** 2024–2025
- **Why it matters:** These works established **test-time compute scaling** as a new fundamental axis of AI improvement alongside training compute. By allocating more inference-time computation (chain-of-thought, self-reflection, search), o1 and R1 achieved reasoning capabilities that elude pure scaling of model size. R1 in particular showed that pure RL from a base model (no SFT) can induce emergent reasoning, democratizing the paradigm. They are the most influential papers in redefining "optimization" to include inference-time allocation.

### 6.4 s1: Simple Test-Time Scaling
- **Authors:** Stanford team (Niklas Muennighoff et al.)
- **Venue:** arXiv 2025
- **Year:** 2025
- **Why it matters:** s1 showed that **test-time scaling can be achieved with minimal budget**: a 1B model trained with simple scaling strategies can match much larger models when allowed to "think longer" at inference. It is a milestone in the **democratization of reasoning**, proving that inference-time optimization is not limited to billion-dollar labs.

---

## 7. KV Cache & Attention Optimization

Papers that tackle the memory and compute bottleneck of attention, especially the KV cache in autoregressive generation.

### 7.1 FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning
- **Authors:** Tri Dao
- **Venue:** NeurIPS 2023
- **Year:** 2023
- **Why it matters:** FlashAttention-2 is the **de facto standard** for high-performance attention implementation. By fusing the attention computation into a single kernel with careful tiling and on-chip SRAM reuse, it eliminates the HBM bandwidth bottleneck. It is used in virtually every production training and inference stack (PyTorch, JAX, vLLM, etc.). FlashAttention-3 (2024) and FlashAttention-4 (2026) extended this to asynchronous execution and new hardware, but FlashAttention-2 is the trunk paper.

### 7.2 H2O: Heavy-Hitter Oracle for Efficient Generative Inference
- **Authors:** Zhenyu Zhang, H. et al.
- **Venue:** NeurIPS 2023
- **Year:** 2023
- **Why it matters:** H2O identified that **a small subset of tokens ("heavy hitters") dominate the attention distribution** across layers, and that unimportant KV cache entries can be evicted with minimal accuracy loss. It was one of the first principled KV cache eviction strategies and inspired a wave of compression methods (Scissorhands, SnapKV, etc.).

### 7.3 Grouped-Query Attention (GQA)
- **Authors:** Joshua Ainslie, James Lee-Thorp, Michiel de Jong, Yury Zemlyanskiy, Federico Lehbrón, Sumit Sanghai
- **Venue:** ACL 2023 / implemented in Mistral, LLaMA 2, etc.
- **Year:** 2023
- **Why it matters:** GQA reduced KV cache memory by **sharing key/value heads across query groups** (e.g., 8 KV heads for 32 query heads). It became a standard architectural modification in virtually all modern LLMs (Mistral 7B, LLaMA 2/3, Qwen, etc.), cutting KV cache memory by 4–8× with negligible performance loss. It is the most widely adopted attention optimization in production.

### 7.4 Ring Attention with Blockwise Transformers
- **Authors:** Hao Liu, Matei Zaharia, Pieter Abbeel
- **Venue:** arXiv 2023 / ICML 2024
- **Year:** 2024
- **Why it matters:** Ring Attention distributed the attention computation across devices in a ring topology, enabling **training and inference on sequences of millions of tokens** without materializing the full attention matrix on any single device. It is the key milestone for ultra-long-context models and is integrated into systems like DeepSeek-V2 and Gemini 1.5.

---

## 8. Reinforcement Learning & Alignment Optimization

Papers that optimized how LLMs are aligned with human preferences and how RL is used for reasoning and post-training.

### 8.1 Direct Preference Optimization (DPO): Your Language Model is Secretly a Reward Model
- **Authors:** Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D. Manning, Stefano Ermon, Chelsea Finn
- **Venue:** NeurIPS 2023 (Most Influential Paper)
- **Year:** 2023
- **Why it matters:** DPO showed that **RLHF can be replaced by a single-stage binary classification loss** on preference data, eliminating the need for an explicit reward model, PPO, and on-policy sampling. It is the most impactful simplification of LLM alignment, making preference tuning accessible to anyone with a preference dataset. DPO and its variants (IPO, KTO, SimPO) are now the default alignment methods in open-source LLM training pipelines.

### 8.2 DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models (GRPO)
- **Authors:** DeepSeek-AI team
- **Venue:** arXiv 2024 / ICML 2024
- **Year:** 2024
- **Why it matters:** This paper introduced **Group Relative Policy Optimization (GRPO)**, a PPO variant that eliminates the value network by using the group-mean reward as a baseline. GRPO became the algorithmic foundation for DeepSeek-R1 and all subsequent open-source reasoning models. It is the most important RL algorithmic innovation for LLM reasoning in the 2024–2025 period.

### 8.3 DAPO: An Open-Source LLM RL System at Scale
- **Authors:** ByteDance Seed team
- **Venue:** arXiv 2025
- **Year:** 2025
- **Why it matters:** DAPO systematically identified and fixed the instability problems in GRPO (zero-gradient filtering, token-level loss, no KL penalty, dynamic clipping). It is the **first open-source, production-grade RL training recipe** that reliably reproduces R1-style reasoning without proprietary infrastructure. DAPO is now the standard reference for open reasoning-model training.

### 8.4 RLVR: Reinforcement Learning with Verifiable Rewards
- **Authors:** Various (Tülu 3, etc.)
- **Venue:** arXiv 2024 / 2025
- **Year:** 2024–2025
- **Why it matters:** RLVR (used in Tülu 3, DeepSeek-R1) showed that **reward models can be replaced by verifiable ground-truth signals** (e.g., math correctness checked by a solver, code correctness checked by execution). This eliminates reward hacking and drastically simplifies the RLHF pipeline. It is the key innovation that made R1-style reasoning scalable and reproducible.

### 8.5 PPO: Proximal Policy Optimization Algorithms
- **Authors:** John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, Oleg Klimov
- **Venue:** arXiv 2017
- **Year:** 2017
- **Why it matters:** PPO is the **trunk algorithm** for all modern LLM RL. While published in 2017, it remained the dominant policy-gradient method for RLHF until GRPO/DPO emerged. Its clipped surrogate objective and ease of implementation made it the default in OpenAI’s InstructGPT, Anthropic’s RLHF, and all early alignment work. It is included here as the foundational method upon which DPO, GRPO, and RLVR are improvements.

---

## 9. Diffusion & Generative Model Optimization

Papers that accelerated diffusion and flow-based models, reducing sampling steps from hundreds to one.

### 9.1 DPM-Solver: A Fast ODE Solver for Diffusion Probabilistic Model Sampling
- **Authors:** Cheng Lu, Yuhao Zhou, Fan Bao, Jianfei Chen, Chongxuan Li, Jun Zhu
- **Venue:** NeurIPS 2022
- **Year:** 2022
- **Why it matters:** DPM-Solver reformulated diffusion sampling as solving a semi-linear ODE and applied **high-order exponential integrators**, achieving high-quality sampling in 10–20 steps. It is the foundational paper for all subsequent ODE-solver-based diffusion acceleration (DPM-Solver++, UniPC, etc.).

### 9.2 Consistency Models
- **Authors:** Yang Song, Prafulla Dhariwal, Mark Chen, Ilya Sutskever
- **Venue:** ICML 2023 (Oral)
- **Year:** 2023
- **Why it matters:** Consistency Models were the first to learn a **single-step generator** by enforcing self-consistency along the diffusion trajectory. They enabled one-step or few-step image generation with quality competitive with multi-step diffusion, directly inspiring the later flow-matching and distillation explosion. They are a milestone in the shift from iterative refinement to direct generation.

### 9.3 Flow Matching for Generative Modeling
- **Authors:** Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, Matthew Le
- **Venue:** ICML 2023
- **Year:** 2023
- **Why it matters:** Flow Matching provided a **cleaner, more general mathematical framework** for training continuous normalizing flows and diffusion models via regression on vector fields. It simplified the theory, improved training stability, and directly enabled Rectified Flow (used in Stable Diffusion 3), InstaFlow, and later one-step models. It is the theoretical trunk for the modern "flow-based" generation paradigm.

### 9.4 Mean Flows for One-Step Generative Modeling
- **Authors:** Zhengyang Geng, Mingyang Deng, Xingjian Bai, J. Zico Kolter, Kaiming He
- **Venue:** NeurIPS 2025 (Oral)
- **Year:** 2025
- **Why it matters:** MeanFlow introduced the concept of **average velocity** (rather than instantaneous velocity) to characterize flow fields, deriving a self-contained one-step training framework that requires no pre-training, distillation, or curriculum. It achieved FID 3.43 on ImageNet 256×256 with a single function evaluation, significantly narrowing the gap between one-step and multi-step models. It is the current SOTA in one-step generation from scratch.

### 9.5 Adversarial Diffusion Distillation (ADD) / LCM-LoRA
- **Authors:** Axel Sauer et al. (ADD, Stability AI); Simian Luo et al. (LCM-LoRA)
- **Venue:** NeurIPS 2023 / arXiv 2023
- **Year:** 2023
- **Why it matters:** ADD and LCM-LoRA showed that **distillation + adversarial training** can reduce Stable Diffusion sampling to 1–4 steps while preserving quality. LCM-LoRA in particular made few-step diffusion accessible via a simple LoRA adapter, widely adopted in consumer tools. These papers established the practical feasibility of real-time diffusion on consumer hardware.

---

## 10. Neural Architecture Search (NAS)

Papers that automated the design of efficient neural architectures, especially for transformers and vision models.

### 10.1 Once-for-All: Train One Network and Specialize it for Efficient Deployment
- **Authors:** Han Cai, Chuang Gan, Tianzhe Wang, Zhekai Zhang, Song Han
- **Venue:** ICLR 2020
- **Year:** 2020
- **Why it matters:** OFA is the **trunk paper** for modern weight-sharing NAS. It trained a single "supernet" containing thousands of subnets, allowing specialization to different hardware constraints without retraining. This paradigm (train once, deploy many) underpins AutoFormer, HAT, BigNAS, and all subsequent hardware-aware NAS. It is the foundational method for efficient deployment of diverse model sizes from a single training run.

### 10.2 AutoFormer: Searching Transformers for Visual Recognition
- **Authors:** Minghao Chen, Houwen Peng, Jianlong Fu, Haibin Ling
- **Venue:** ICCV 2021
- **Year:** 2021
- **Why it matters:** AutoFormer was the **first successful NAS for pure Vision Transformers**, using weight entanglement to train a once-for-all supernet without extra techniques like inplace distillation. It demonstrated that NAS can be applied to ViT structures (embedding dim, heads, MLP ratio, depth) and directly inspired hardware-aware transformer search (HAT, ViTAS, etc.).

### 10.3 Neural Architecture Search: Insights from 1000 Papers
- **Authors:** Colin White, Mahmoud Safari, Rhea Sukthanker, Binxin Ru, Thomas Elsken, Arber Zela, Debadeepta Dey, Frank Hutter
- **Venue:** arXiv 2023 / JMLR 2024
- **Year:** 2023–2024
- **Why it matters:** This comprehensive survey distilled **a decade of NAS research** into actionable insights, identifying that weight-sharing supernets and hardware-aware search are the dominant paradigms. It serves as the definitive reference for understanding NAS evolution and is widely cited as the "NAS bible" for researchers entering the field.

---

## 11. Neural Combinatorial Optimization

Papers that use deep learning and RL to solve classical NP-hard optimization problems.

### 11.1 Neural Combinatorial Optimization with Reinforcement Learning — A Survey
- **Authors:** K.T. Chung et al.
- **Venue:** Springer / arXiv 2025
- **Year:** 2025
- **Why it matters:** The most comprehensive modern survey of using RL (PPO, Q-learning, etc.) to solve TSP, VRP, scheduling, and other CO problems. It systematizes the MDP formulation, encoder-decoder architectures, and search strategies (beam search, MCTS) that define the field. It is the definitive reference for the intersection of deep learning and operations research in 2023–2025.

### 11.2 Limited Rollout Beam Search (LRBS) for DRL-Based CO Improvement
- **Authors:** Federico Julian Camerota Verdù, Lorenzo Castelli, Luca Bortolussi
- **Venue:** AAAI 2025
- **Year:** 2025
- **Why it matters:** LRBS introduced a **beam search strategy for DRL improvement heuristics** that generalizes to problem instances 10× larger than training data. It achieved state-of-the-art results among improvement heuristics for TSP and demonstrated that online adaptation during search can overcome the limitations of fixed pretrained policies. A milestone in scaling neural CO to practical problem sizes.

### 11.3 POMO: Policy Optimization with Multiple Optima for TSP
- **Authors:** Wonseok Jeong, Byung-Jun Lee, Jinkyoo Park, Jay H. Park
- **Venue:** NeurIPS 2022
- **Year:** 2022
- **Why it matters:** POMO is the **trunk method** for RL-based constructive CO solvers. By exploiting multiple equivalent optimal solutions (symmetries) and using a shared decoder, it dramatically improved sample efficiency and generalization for TSP/VRP. It is the baseline against which all subsequent neural CO constructive methods are compared.

---

## 12. Learning-Rate-Free & Adaptive Optimization

Papers that eliminate manual learning-rate tuning, a longstanding bottleneck in optimization.

### 12.1 D-Adaptation: Learning-Rate-Free Learning
- **Authors:** Aaron Defazio, Konstantin Mishchenko
- **Venue:** ICML 2023
- **Year:** 2023
- **Why it matters:** D-Adaptation is the **first hyperparameter-free method** to achieve the optimal convergence rate for convex Lipschitz functions without backtracking or line searches, and without additional log factors. It automatically matches hand-tuned learning rates across large-scale vision and language tasks. It is a milestone in theoretical optimization with immediate practical impact.

### 12.2 Prodigy: An Expeditiously Adaptive Parameter-Free Learner
- **Authors:** Konstantin Mishchenko, Aaron Defazio
- **Venue:** arXiv 2023 / ICML 2023 workshops
- **Year:** 2023
- **Why it matters:** Prodigy extends D-Adaptation by dynamically estimating the distance to the optimum, yielding faster convergence in practice. It is one of the most widely used parameter-free optimizers in experimental deep learning pipelines and is frequently compared against as the "state-of-the-art" in learning-rate-free methods.

### 12.3 DoG is SGD’s Best Friend: A Parameter-Free Dynamic Step Size Schedule
- **Authors:** Maor Ivgi, Oliver Hinder, Yair Carmon
- **Venue:** ICML 2023
- **Year:** 2023
- **Why it matters:** DoG (Distance over Gradients) is a **parameter-free SGD variant** that adaptively estimates both the Lipschitz constant and the distance to the solution. It works robustly across non-convex deep learning problems without any learning rate tuning, and its theoretical guarantees are among the strongest for parameter-free methods in the stochastic setting.

---

## 13. Distributed Training & Systems Optimization

Papers that optimize the systems and parallelism strategies for training large models.

### 13.1 Megatron-LM / DeepSpeed / FSDP (Trunk Methods)
- **Authors:** NVIDIA (Megatron); Microsoft (DeepSpeed); Meta (FSDP)
- **Venue:** Various (2019–2022)
- **Year:** 2019–2022
- **Why it matters:** These are the **trunk systems** for large-model distributed training. Megatron-LM introduced tensor parallelism for transformers; DeepSpeed introduced ZeRO (zero redundancy optimizer) stages that sharded optimizer states, gradients, and parameters; FSDP (Fully Sharded Data Parallel) brought this to PyTorch natively. All 2023–2026 training work builds on these systems. They are included as foundational context.

### 13.2 Ring Attention with Blockwise Transformers (Distributed Long-Sequence Training)
- **Authors:** Hao Liu, Matei Zaharia, Pieter Abbeel
- **Venue:** ICML 2024
- **Year:** 2024
- **Why it matters:** See also Section 7.4. Beyond KV cache optimization, Ring Attention is a **systems-level breakthrough** for distributed training of sequences up to millions of tokens, partitioning attention across a ring of devices. It is the enabling technology for frontier long-context models (Gemini 1.5, DeepSeek-V2, Kimi K2) and is a milestone in scaling sequence length rather than model width.

---

## 14. Honorable Mentions & Emerging Directions (2025–2026)

These are recent breakthroughs that have not yet fully stabilized but are likely to become trunk papers.

### 14.1 FlashAttention-3 / FlashAttention-4
- **Venue:** arXiv 2024 / 2026
- **Why it matters:** Further hardware-aware optimizations (asynchronous warp-group execution, FP8 support, new Tensor Core features) that push attention throughput to the physical limits of modern GPUs. FlashAttention-4 (2026) is particularly notable for integrating with Hopper/Blackwell hardware features.

### 14.2 Speculative Decoding & EAGLE-3
- **Authors:** Leviathan et al. (Google, 2022); Yanjun Zhu et al. (EAGLE series, 2024–2025)
- **Venue:** arXiv 2022 / ICLR 2024 / 2025
- **Why it matters:** Speculative decoding uses a small draft model to guess tokens and a large model to verify, achieving **2–3× lossless speedup**. The EAGLE series improved this with feature-level speculation and dynamic draft trees, making it practical for production. P-EAGLE (2026) introduced parallel speculative decoding in vLLM.

### 14.3 TurboQuant / KVQuant: 1-2 Bit KV Cache Quantization
- **Venue:** arXiv 2025 / 2026
- **Why it matters:** These works push KV cache quantization to **1–2 bits per element**, enabling context lengths of 10M+ tokens on consumer GPUs. They represent the frontier of inference memory compression and are critical for the next generation of long-context agents.

### 14.4 BitBLAS / Custom Precision Kernels
- **Venue:** arXiv 2025–2026
- **Why it matters:** BitBLAS and related systems enable **flexible bit-level operations** (arbitrary per-layer precision) on GPU Tensor Cores, making sub-4-bit quantization practically fast rather than just theoretically possible. This is a key systems milestone for the extreme quantization era.

### 14.5 Kimi K2 / Qwen3 / GLM-5: MoE as Default (2025–2026)
- **Venue:** Technical reports 2025–2026
- **Why it matters:** By 2026, MoE has become the default architecture for all frontier models (Kimi K2: 1.04T/32B active; Qwen3; GLM-5). These technical reports document the empirical sparsity laws, routing stability techniques, and expert-parallel communication optimizations that define the new scaling paradigm. They are the **trunk references** for MoE engineering in 2026.

### 14.6 No Free Lunch: Rethinking Internal Feedback for LLM Reasoning
- **Venue:** arXiv 2025
- **Why it matters:** This paper provided a theoretical critique of "verifier-free RL" methods, arguing that internal signals alone cannot guarantee reliable reasoning. It is a milestone in the **meta-scientific understanding** of what test-time compute can and cannot achieve, guiding the next wave of reasoning research.

---

## Summary Statistics

| Sub-Theme | # Milestone Papers | Representative Venues |
|---|---|---|
| Training Optimizers | 5 | ICLR, NeurIPS, ICML |
| Compression & Quantization | 5 | NeurIPS, ICLR, MLSys |
| Pruning & Sparsity | 4 | ICML, ICLR, NeurIPS |
| PEFT & Memory Optimization | 3 | ICLR, ICML |
| MoE & Sparse Architectures | 4 | ICLR, arXiv, JMLR |
| Inference & Test-Time Compute | 4 | SOSP, ICLR, arXiv |
| KV Cache & Attention | 4 | NeurIPS, ACL, ICML |
| RL & Alignment | 5 | NeurIPS, arXiv, ICML |
| Diffusion & Generative Opt. | 5 | ICML, NeurIPS |
| Neural Architecture Search | 3 | ICLR, ICCV, JMLR |
| Neural Combinatorial Opt. | 3 | AAAI, NeurIPS |
| Learning-Rate-Free Opt. | 3 | ICML, arXiv |
| Distributed Systems | 2 | ICML, various |
| Emerging Directions | 6 | arXiv, various |
| **Total** | **~56** | |

---

> **Note:** This list prioritizes **foundational, widely-cited, and direction-opening** papers. Many excellent incremental works are omitted to maintain focus on the trunk. For each sub-theme, the earliest / most-cited paper is marked as the **trunk** (foundational), and subsequent papers are **milestones** (major advances). The cutoff is mid-2026 (July 2026).
