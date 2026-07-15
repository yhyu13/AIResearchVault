# Milestone Papers in AI Training-Technique (2023 – Mid-2026)

> Curated: 2026-07-15  
> Scope: Foundational, widely-cited, direction-opening, or breakthrough papers in training methodology, optimization, architecture, and scaling.  
> Excludes: Minor incremental works, pure application papers, and inference-only techniques.

---

## 1. Pre-training & Scaling Laws

Papers that define how large models should be trained, how compute should be allocated, and how performance scales with resources.

---

### 1.1 Training Compute-Optimal Large Language Models (Chinchilla)
**Title:** Training Compute-Optimal Large Language Models  
**Authors:** Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, et al.  
**Venue:** arXiv / NeurIPS 2022 (deep impact through 2023–2026)  
**Year:** 2022 (foundational for 2023+ training strategies)

> **Why milestone:** Established the "Chinchilla scaling laws" — the compute-optimal prescription that model parameters and training tokens should scale proportionally (~20 tokens per parameter). This directly shaped LLaMA, LLaMA 2/3, Mistral, and virtually all modern open-weight pre-training recipes. The 70B Chinchilla outperformed much larger Gopher, cementing "train smaller on more data" as the dominant paradigm.

---

### 1.2 LLaMA: Open and Efficient Foundation Language Models
**Title:** LLaMA: Open and Efficient Foundation Language Models  
**Authors:** Hugo Touvron, Thibaut Lavril, Gautier Izacard, et al. (Meta AI)  
**Venue:** arXiv (released Feb 2023)  
**Year:** 2023

> **Why milestone:** Demonstrated that competitive LLMs (LLaMA-13B matching GPT-3) can be trained exclusively on publicly available data, catalyzing the entire open-source LLM ecosystem. Introduced architectural standards (Pre-RMSNorm, SwiGLU, RoPE) that became universal in subsequent open models. The 1.4T-token training recipe proved Chinchilla-optimal scaling in practice.

---

### 1.3 Scaling Laws for Predicting Downstream Performance in LLMs
**Title:** Scaling Laws for Predicting Downstream Performance in LLMs  
**Authors:** Yao et al. (follow-up line); extensive 2023–2025 literature  
**Venue:** Multiple (arXiv, NeurIPS, ICML)  
**Year:** 2023–2025

> **Why milestone:** Extended scaling laws from pre-training loss to downstream task accuracy, knowledge capabilities, and data-constrained regimes. Papers like "Scaling Laws for Data Filtering" (Goyal et al., CVPR 2024) and "Data Mixing Laws" (Ye et al., 2025) showed that data curation strategy must be compute-aware — aggressive filtering is optimal for small compute, while larger budgets require broader data. These became essential tooling for industrial pre-training decisions.

---

### 1.4 Scaling Laws for Optimal Data Mixtures
**Title:** Scaling Laws for Optimal Data Mixtures  
**Authors:** Mustafa Shukor, Louis Bethune, Dan Busbridge, David Grangier, et al. (Apple)  
**Venue:** NeurIPS 2025  
**Year:** 2025

> **Why milestone:** First systematic scaling laws predicting model loss as a function of *domain mixture weights*, validated across LLMs, native multimodal models, and large vision models. Enables extrapolation from small-scale runs to optimal mixture design at billion-parameter scale, replacing costly trial-and-error with principled prediction.

---

## 2. Post-Training Alignment & Preference Optimization

Papers that revolutionized how models are aligned to human preferences after pre-training, moving from complex multi-stage RL pipelines to simpler, more stable optimization objectives.

---

### 2.1 Direct Preference Optimization (DPO)
**Title:** Direct Preference Optimization: Your Language Model is Secretly a Reward Model  
**Authors:** Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D. Manning, Stefano Ermon, Chelsea Finn  
**Venue:** NeurIPS 2023  
**Year:** 2023

> **Why milestone:** Eliminated the need for explicit reward modeling and PPO-based RL in alignment. DPO reformulates RLHF as a single supervised classification objective over preference pairs, achieving comparable or better performance with dramatically simpler training. Became the *de facto* standard for open-source model alignment (Zephyr, Tulu, Mistral Instruct) and was adopted by DeepSeek and LLaMA 3.

---

### 2.2 SimPO: Simple Preference Optimization with a Reference-Free Reward
**Title:** SimPO: Simple Preference Optimization with a Reference-Free Reward  
**Authors:** Yu Meng, Mengzhou Xia, Danqi Chen  
**Venue:** ICML 2024 / arXiv 2024  
**Year:** 2024

> **Why milestone:** Simplified DPO further by removing the reference model entirely, using a length-normalized implicit reward based on average log probability. Eliminated memory overhead and length-bias issues of DPO, making preference alignment feasible on even more constrained hardware while matching or exceeding DPO performance.

---

### 2.3 KTO: Model Alignment as Prospect Theoretic Optimization
**Title:** KTO: Model Alignment as Prospect Theoretic Optimization  
**Authors:** Kawin Ethayarajh, Yejin Choi, Swabha Swayamdipta  
**Venue:** NeurIPS 2024 / arXiv 2024  
**Year:** 2024

> **Why milestone:** Enabled alignment from *binary* feedback (thumbs up/down per example) rather than pairwise preference comparisons, drastically reducing data collection cost. Grounded in Kahneman-Tversky prospect theory, KTO showed that per-example utility maximization can match pairwise DPO — opening alignment to domains where preference pairs are impractical to collect.

---

## 3. Reasoning & Test-Time Compute Training

Papers that established training paradigms for models that reason through long chains of thought and benefit from increased inference-time computation.

---

### 3.1 Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
**Title:** Chain-of-Thought Prompting Elicits Reasoning in Large Language Models  
**Authors:** Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, et al. (Google)  
**Venue:** NeurIPS 2022 (impact peak 2023–2025)  
**Year:** 2022

> **Why milestone:** The foundational paper showing that simply prompting LLMs to "think step by step" dramatically improves arithmetic, commonsense, and symbolic reasoning. This single prompting insight spawned the entire reasoning-training subfield and was the conceptual precursor to supervised CoT fine-tuning, process reward models, and eventually RL-trained reasoning.

---

### 3.2 Tree of Thoughts: Deliberate Problem Solving with Large Language Models
**Title:** Tree of Thoughts: Deliberate Problem Solving with Large Language Models  
**Authors:** Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, Karthik Narasimhan  
**Venue:** NeurIPS 2023  
**Year:** 2023

> **Why milestone:** Extended CoT from linear reasoning chains to branching search trees, enabling LLMs to explore multiple reasoning paths, backtrack, and vote. Established the conceptual bridge between LLM prompting and classical search/planning algorithms, directly inspiring later RL-based reasoning systems (o1, R1) that internalize this search behavior.

---

### 3.3 Scaling LLM Test-Time Compute Optimally
**Title:** Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters  
**Authors:** Charlie Snell, Jaehoon Lee, Kelvin Xu, Aviral Kumar  
**Venue:** arXiv 2024  
**Year:** 2024

> **Why milestone:** Provided the first rigorous scaling-law treatment of *inference-time* compute, proving that investing FLOPs at test time (via parallel sampling, verification, search) can outperform scaling model size by orders of magnitude. This paper mathematically justified the test-time compute paradigm that OpenAI o1 and DeepSeek-R1 would later exploit at scale.

---

### 3.4 DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models
**Title:** DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models  
**Authors:** Zhihin Shao, Peiyi Wang, Qihao Zhu, et al. (DeepSeek-AI)  
**Venue:** arXiv 2024 / ICLR 2024  
**Year:** 2024

> **Why milestone:** Introduced **Group Relative Policy Optimization (GRPO)**, a critic-free RL algorithm that estimates advantages from group-level reward comparisons rather than a learned value model. GRPO eliminated the memory and stability overhead of PPO + value model, making large-scale RL for reasoning computationally feasible. Became the algorithmic backbone of DeepSeek-R1.

---

### 3.5 DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning
**Title:** DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning  
**Authors:** DeepSeek-AI (Daya Guo et al.)  
**Venue:** arXiv 2025  
**Year:** 2025

> **Why milestone:** Landmark open-source model proving that pure RL (without supervised CoT data) can elicit sophisticated long-chain reasoning, self-verification, and "aha moments" in LLMs. DeepSeek-R1 matched OpenAI o1 performance on math and code benchmarks, released open weights and training details, and triggered a global shift toward reinforcement-dominant training pipelines. Demonstrated GRPO at scale and validated the RLVR (Reinforcement Learning with Verifiable Rewards) paradigm.

---

### 3.6 s1: Simple Test-Time Scaling
**Title:** s1: Simple Test-Time Scaling  
**Authors:** Niklas Muennighoff, Zitong Yang, Weijia Shi, et al. (Stanford)  
**Venue:** EMNLP 2025 / arXiv 2025  
**Year:** 2025

> **Why milestone:** Showed that supervised fine-tuning on just **1,000 carefully curated reasoning examples** with "budget forcing" (controlling maximum thinking tokens) can create competitive reasoning models. This dramatically lowered the data barrier for reasoning training and established that test-time scaling behavior can be trained in, not just prompted.

---

## 4. Efficient Training & Parameter-Efficient Fine-Tuning

Papers that made training and adapting large models accessible by drastically reducing memory, compute, or data requirements.

---

### 4.1 LoRA: Low-Rank Adaptation of Large Language Models
**Title:** LoRA: Low-Rank Adaptation of Large Language Models  
**Authors:** Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen  
**Venue:** ICLR 2022 (adoption peak 2023–2026)  
**Year:** 2022

> **Why milestone:** The foundational parameter-efficient fine-tuning (PEFT) method. LoRA freezes pre-trained weights and injects trainable low-rank matrices (ΔW ≈ BA), reducing trainable parameters by orders of magnitude (e.g., 256× for r=8 on d=4096). Enabled fine-tuning 7B+ models on single consumer GPUs, democratizing LLM adaptation and becoming the backbone of virtually all open-source fine-tuning pipelines (Alpaca, Vicuna, etc.).

---

### 4.2 QLoRA: Efficient Finetuning of Quantized LLMs
**Title:** QLoRA: Efficient Finetuning of Quantized LLMs  
**Authors:** Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, Luke Zettlemoyer  
**Venue:** NeurIPS 2023  
**Year:** 2023

> **Why milestone:** Combined 4-bit NormalFloat (NF4) quantization with LoRA adapters, enabling fine-tuning of 65B-parameter models on a single 48GB GPU without performance degradation. Introduced double quantization and paged optimizers to manage memory. QLoRA became the standard toolkit for resource-constrained fine-tuning and directly enabled the proliferation of open-source instruct models.

---

### 4.3 GaLore: Memory-Efficient LLM Training by Gradient Low-Rank Projection
**Title:** GaLore: Memory-Efficient LLM Training by Gradient Low-Rank Projection  
**Authors:** Jiawei Zhao, Zhenyu Zhang, Beidi Chen, et al.  
**Venue:** ICML 2024  
**Year:** 2024

> **Why milestone:** Extended low-rank efficiency from *fine-tuning* to *full pre-training* by projecting optimizer states (Adam moment estimates) into low-rank subspaces. GaLore enabled full training of 7B-parameter models on consumer hardware — previously impossible — by reducing optimizer memory from 2× model size to a small fraction, without altering convergence dynamics.

---

## 5. Mixture of Experts (MoE) Training

Papers that established sparse expert architectures as the dominant paradigm for scaling model capacity without proportional compute increase.

---

### 5.1 Mixtral 8x7B: A Sparse Mixture of Experts Model
**Title:** Mixtral 8x7B: A Sparse Mixture of Experts Model  
**Authors:** Albert Q. Jiang, Alexandre Sablayrolles, Antoine Roux, Arthur Mensch, et al. (Mistral AI)  
**Venue:** arXiv (Dec 2023) / technical report 2024  
**Year:** 2023/2024

> **Why milestone:** First open-weight MoE LLM to match or exceed dense 70B models (LLaMA 2 70B, GPT-3.5) with only ~13B active parameters per token. Demonstrated that top-2 routing with 8 experts per layer is production-viable, with total params ~47B. Proved the "capacity vs. active compute" separation that became the blueprint for DeepSeek-V2/V3, Qwen-MoE, and all subsequent open sparse models.

---

### 5.2 DeepSeek-V3: A Strong and Efficient Mixture-of-Experts Language Model
**Title:** DeepSeek-V3 Technical Report  
**Authors:** DeepSeek-AI  
**Venue:** arXiv 2024  
**Year:** 2024

> **Why milestone:** 671B-parameter MoE with only 37B active parameters per token, achieved via fine-grained expert routing and auxiliary-loss-free load balancing. DeepSeek-V3 demonstrated that MoE training at massive scale can match frontier dense models at a fraction of training cost, establishing the engineering blueprint for efficient trillion-parameter pre-training. Combined with FP8 training and optimized pipeline parallelism, it became the most cost-efficient frontier model training recipe published.

---

## 6. Alternative Architectures: Beyond Attention

Papers that challenged the Transformer monopoly with linear-time alternatives, opening new design spaces for long-context and efficient training.

---

### 6.1 Mamba: Linear-Time Sequence Modeling with Selective State Spaces
**Title:** Mamba: Linear-Time Sequence Modeling with Selective State Spaces  
**Authors:** Albert Gu, Tri Dao  
**Venue:** ICLR 2024 (Oral / Top 1%)  
**Year:** 2023 (arXiv Dec 2023)

> **Why milestone:** First state-space model to match or exceed Transformer quality across language modeling scales while maintaining **O(n)** training and inference complexity (vs. O(n²) attention). Introduced *input-dependent* (selective) state transitions, solving the content-awareness problem that plagued prior SSMs (S4, H3). Sparked a wave of Mamba-based models (Jamba, Vision Mamba, VideoMamba) and proved attention is not the only viable path to scale.

---

### 6.2 Mamba-2: Transformers Are SSMs
**Title:** Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality  
**Authors:** Tri Dao, Albert Gu  
**Venue:** ICML 2024  
**Year:** 2024

> **Why milestone:** Established the theoretical "Structured State Space Duality" (SSD) showing that attention and state-space models share deep mathematical structure. Mamba-2 simplified the selective mechanism to scalar-identity transitions, enabling efficient tensor-parallel training and closing the hardware-efficiency gap with Transformers. This unified framework enabled hybrid models (attention + SSM) that became competitive alternatives to pure Transformer stacks.

---

## 7. Vision Model Training

Papers that advanced how visual representations are learned, from self-supervised pretraining to interactive segmentation.

---

### 7.1 Segment Anything (SAM)
**Title:** Segment Anything  
**Authors:** Alexander Kirillov, Eric Mintun, Nikhila Ravi, et al. (Meta AI)  
**Venue:** ICCV 2023 (Best Paper Honorable Mention)  
**Year:** 2023

> **Why milestone:** Introduced a new training paradigm for segmentation: train on 11M images with 1B+ masks (semi-automatically generated) to achieve **zero-shot, class-agnostic, promptable segmentation**. SAM demonstrated that interactive visual tasks can be trained at unprecedented scale with synthetic/assisted labels, spawning the "segment anything" paradigm across computer vision and becoming a standard backbone for downstream vision tasks.

---

### 7.2 DINOv2: Learning Robust Visual Features without Supervision
**Title:** DINOv2: Learning Robust Visual Features without Supervision  
**Authors:** Maxime Oquab, Timothée Darcet, Théo Moutakanni, et al. (Meta AI)  
**Venue:** ICLR 2024  
**Year:** 2023 (arXiv Apr 2023)

> **Why milestone:** Scaled self-supervised discriminative pre-training (DINO + iBOT + SwAV centering) to 1B+ web images, producing vision features that rival or exceed weakly-supervised CLIP on downstream tasks *without any text labels*. DINOv2 features work out-of-the-box for classification, detection, depth estimation, and segmentation — proving pure visual self-supervision can match multi-modal training. Became the default frozen vision backbone for many research and production systems.

---

## 8. Diffusion & Generative Model Training

Papers that transformed how generative models are trained, from diffusion objectives to transformer backbones and flow matching.

---

### 8.1 Scalable Diffusion Models with Transformers (DiT)
**Title:** Scalable Diffusion Models with Transformers  
**Authors:** William Peebles, Saining Xie  
**Venue:** ICCV 2023  
**Year:** 2023

> **Why milestone:** Replaced U-Net backbones with pure Vision Transformers for diffusion, demonstrating superior scaling behavior with model size. DiT established the **Diffusion Transformer** architecture that became the backbone of Stable Diffusion 3, Sora, Flux, Lumina, and virtually all state-of-the-art image/video generation systems in 2024–2025. Proved that transformers scale better than convolutions for generative modeling.

---

### 8.2 Flow Matching for Generative Modeling
**Title:** Flow Matching for Generative Modeling  
**Authors:** Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, Matt Le  
**Venue:** ICLR 2023  
**Year:** 2023

> **Why milestone:** Provided a simpler, more direct training objective for continuous normalizing flows by regressing on a target vector field rather than score matching. Flow matching (and its Rectified Flow variant) supplanted DDPM as the training objective of choice for diffusion transformers, enabling faster convergence, fewer sampling steps, and better theoretical tractability. Powering Stable Diffusion 3, Flux, and Sora.

---

### 8.3 Consistency Models
**Title:** Consistency Models  
**Authors:** Yang Song, Prafulla Dhariwal, Mark Chen, Ilya Sutskever  
**Venue:** ICML 2023  
**Year:** 2023

> **Why milestone:** Enabled single-step (or few-step) generative modeling by training to map any point on a diffusion trajectory directly to the data manifold. Consistency models bypassed the iterative sampling bottleneck of diffusion, achieving generation in 1–4 steps with quality approaching full diffusion. This training paradigm opened the door to real-time diffusion inference and influenced subsequent distillation methods (Adversarial Diffusion Distillation, etc.).

---

## 9. Data Curation & Quality for Training

Papers that established data quality, filtering, and mixture design as first-class citizens in model training, not afterthoughts.

---

### 9.1 DataComp: Filtering Pre-training Data at Scale
**Title:** DataComp: In search of the next generation of multimodal datasets  
**Authors:** Samir Yitzhak Gadre, Gabriel Ilharco, Alex Fang, et al.  
**Venue:** NeurIPS 2023  
**Year:** 2023

> **Why milestone:** Created a standardized benchmark for comparing data filtering strategies for CLIP-style training, treating data curation as a competitive optimization problem. Showed that better filtering of noisy web data can outperform expensive model-scale increases. DataComp established the empirical foundation for all subsequent data-centric pre-training work (FineWeb, DCLM, etc.).

---

### 9.2 Scaling Laws for Data Filtering — Data Curation Cannot Be Compute Agnostic
**Title:** Scaling Laws for Data Filtering — Data Curation Cannot Be Compute Agnostic  
**Authors:** Samir Yitzhak Gadre, Gabriel Ilharco, et al. (follow-up); S. Goyal et al.  
**Venue:** CVPR 2024  
**Year:** 2024

> **Why milestone:** Proved that the optimal data filtering strategy *depends on the training compute budget* — aggressive top-10% filtering is best for small budgets, but top-30% or broader filtering wins at larger scales because high-quality data suffers diminishing returns when repeated. This compute-aware curation insight fundamentally changed how industrial labs design pre-training datasets, replacing static heuristic filtering with budget-adaptive strategies.

---

### 9.3 DCLM: DataComp for Language Models
**Title:** DCLM: DataComp for Language Models  
**Authors:** Li et al. (Apple / multi-institution)  
**Venue:** arXiv 2024  
**Year:** 2024

> **Why milestone:** Extended the DataComp paradigm to language-only pre-training, providing a modular, reproducible evaluation framework for data curation pipelines. DCLM demonstrated that careful web filtering, deduplication, and heuristic/model-based quality scoring can match or exceed proprietary curated datasets, making high-quality pre-training accessible to the open community and establishing standard baselines for data engineering research.

---

## 10. Multimodal Training

Papers that advanced how vision and language are jointly trained, enabling the modern generation of vision-language models.

---

### 10.1 LLaVA: Visual Instruction Tuning
**Title:** Visual Instruction Tuning  
**Authors:** Haotian Liu, Chunyuan Li, Qingyang Wu, Yong Jae Lee  
**Venue:** NeurIPS 2023  
**Year:** 2023

> **Why milestone:** Demonstrated that simple projection-layer alignment between a frozen CLIP visual encoder and a frozen LLM (Vicuna), followed by lightweight end-to-end instruction tuning on synthetic GPT-4-generated data, creates surprisingly capable multimodal dialogue models. LLaVA established the "minimal viable architecture" for open-source VLMs and spawned an entire ecosystem (LLaVA-1.5, LLaVA-NeXT, LLaVA-Video, etc.).

---

### 10.2 Qwen-VL: A Frontier Large Vision-Language Model
**Title:** Qwen-VL: A Versatile Vision-Language Model for Understanding, Localization, Text Reading, and Beyond  
**Authors:** Alibaba Qwen Team  
**Venue:** arXiv 2023  
**Year:** 2023

> **Why milestone:** Among the first open-source VLMs to unify visual understanding, OCR, grounding, and multi-image reasoning in a single model. Qwen-VL's training recipe (three-stage: alignment → multi-task pre-training → instruction tuning) became the standard template for open VLM development. The Qwen2-VL and Qwen2.5-VL successors maintained state-of-the-art open performance through 2025.

---

## 11. Test-Time Training (Emerging 2025–2026)

A nascent but potentially transformative direction where models learn during inference by adapting to each input.

---

### 11.1 ViT3: Unlocking Test-Time Training in Vision
**Title:** ViT3: Unlocking Test-Time Training in Vision  
**Authors:** D. Han et al.  
**Venue:** CVPR 2026  
**Year:** 2026

> **Why milestone:** First systematic empirical study and practical architecture for test-time training (TTT) in vision transformers. ViT3 replaces standard attention with a TTT block that performs inner-loop gradient descent on each input, achieving linear complexity while matching or exceeding standard attention and Mamba on image classification and diffusion tasks. Represents a potential paradigm shift: training *during* inference rather than only before it.

---

## Summary Table: Quick Reference

| # | Paper | Year | Venue | Key Contribution |
|---|-------|------|-------|------------------|
| 1.1 | Chinchilla (Hoffmann et al.) | 2022 | NeurIPS | Compute-optimal scaling laws |
| 1.2 | LLaMA (Touvron et al.) | 2023 | arXiv | Open-source Chinchilla-optimal LLMs |
| 1.3 | Scaling Laws for Data Filtering | 2024 | CVPR | Compute-aware data curation |
| 1.4 | Scaling Laws for Data Mixtures | 2025 | NeurIPS | Predictive mixture optimization |
| 2.1 | DPO (Rafailov et al.) | 2023 | NeurIPS | Reward-free alignment |
| 2.2 | SimPO | 2024 | ICML | Reference-free preference optimization |
| 2.3 | KTO | 2024 | NeurIPS | Binary-feedback alignment |
| 3.1 | Chain-of-Thought (Wei et al.) | 2022 | NeurIPS | Step-by-step reasoning prompting |
| 3.2 | Tree of Thoughts (Yao et al.) | 2023 | NeurIPS | Search-based reasoning |
| 3.3 | Scaling Test-Time Compute (Snell et al.) | 2024 | arXiv | Inference-compute scaling laws |
| 3.4 | DeepSeekMath / GRPO | 2024 | ICLR | Critic-free RL for reasoning |
| 3.5 | DeepSeek-R1 | 2025 | arXiv | Pure RL reasoning at scale |
| 3.6 | s1: Simple Test-Time Scaling | 2025 | EMNLP | 1K-example reasoning training |
| 4.1 | LoRA (Hu et al.) | 2022 | ICLR | Low-rank fine-tuning |
| 4.2 | QLoRA (Dettmers et al.) | 2023 | NeurIPS | 4-bit quantized fine-tuning |
| 4.3 | GaLore | 2024 | ICML | Low-rank full pre-training |
| 5.1 | Mixtral 8x7B | 2023 | arXiv | Open-weight MoE LLM |
| 5.2 | DeepSeek-V3 | 2024 | arXiv | Trillion-scale MoE training |
| 6.1 | Mamba (Gu & Dao) | 2023 | ICLR | Linear-time selective SSM |
| 6.2 | Mamba-2 (Dao & Gu) | 2024 | ICML | SSM-attention duality |
| 7.1 | SAM (Kirillov et al.) | 2023 | ICCV | Zero-shot promptable segmentation |
| 7.2 | DINOv2 (Oquab et al.) | 2023 | ICLR | Billion-scale visual self-supervision |
| 8.1 | DiT (Peebles & Xie) | 2023 | ICCV | Transformer diffusion backbones |
| 8.2 | Flow Matching (Lipman et al.) | 2023 | ICLR | Direct vector-field training |
| 8.3 | Consistency Models (Song et al.) | 2023 | ICML | Single-step generative training |
| 9.1 | DataComp (Gadre et al.) | 2023 | NeurIPS | Benchmarking data filtering |
| 9.2 | Data Filtering Scaling Laws | 2024 | CVPR | Budget-dependent curation |
| 9.3 | DCLM (Li et al.) | 2024 | arXiv | Language data curation standard |
| 10.1 | LLaVA (Liu et al.) | 2023 | NeurIPS | Minimal VLM architecture |
| 10.2 | Qwen-VL | 2023 | arXiv | Unified open VLM training |
| 11.1 | ViT3 | 2026 | CVPR | Test-time training in vision |

---

> **Curator note:** This list prioritizes *training methodology* papers — those that changed *how* models are trained, not merely *what* models achieve. Papers from 2022 with peak impact in 2023–2026 are included because they shaped the training landscape of the target period. The 2025–2026 entries reflect the emerging paradigms of reasoning-first RL training, test-time compute, and test-time training that are actively redefining the field.
