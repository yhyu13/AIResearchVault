# LLM Milestone Papers (2023 – Mid-2026)

A curated list of the most important, foundational, and trunk papers in Large Language Models from 2023 to mid-2026. These papers opened new directions, established canonical architectures, or produced breakthrough capabilities. Minor incremental works are excluded.

---

## 1. Foundation Models and Open-Source Ecosystem

### GPT-4 Technical Report
**Authors:** OpenAI  
**Venue:** arXiv Technical Report  
**Year:** 2023  
**Why it matters:** The first detailed technical report on a frontier multimodal LLM, demonstrating that scaled RLHF and massive compute could produce human-level performance across professional exams, legal reasoning, and creative tasks. It established the benchmark for "frontier" capabilities and set the research direction for the entire field in 2023–2024.

### LLaMA: Open and Efficient Foundation Language Models
**Authors:** Hugo Touvron, Thibaut Lavril, Gautier Izacard, et al. (Meta AI)  
**Venue:** arXiv  
**Year:** 2023  
**Why it matters:** LLaMA ignited the open-source LLM revolution by releasing high-quality weights (7B–65B) trained exclusively on public data, proving that open models could rival early GPT-3.5 performance. It directly spawned the ecosystem of Alpaca, Vicuna, and hundreds of derivative models, fundamentally democratizing access to capable LLMs.

### Llama 2: Open Foundation and Fine-Tuned Chat Models
**Authors:** Hugo Touvron, Louis Martin, Kevin Stone, et al. (Meta AI)  
**Venue:** arXiv  
**Year:** 2023  
**Why it matters:** The first widely adopted open-source "chat model" with a permissible commercial license, paired with detailed safety evaluation and red-teaming methodology. Llama 2 set the standard for open-weight instruction-tuned models and became the backbone of enterprise AI deployments worldwide.

### The Llama 3 Herd of Models
**Authors:** Llama Team, AI @ Meta  
**Venue:** arXiv  
**Year:** 2024  
**Why it matters:** Scaled open models to 405B parameters with a massive 15T+ token dataset, achieving parity with GPT-4 on many benchmarks. The release of the 405B checkpoint (along with 8B/70B variants) became the definitive open foundation for research and industry, proving open-weight models could match closed frontier performance.

---

## 2. Architecture and Efficiency

### Mistral 7B
**Authors:** Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch, et al. (Mistral AI)  
**Venue:** arXiv  
**Year:** 2023  
**Why it matters:** Showed that a 7B parameter model could outperform LLaMA-2 13B and even LLaMA-1 34B through architectural innovations like Grouped-Query Attention (GQA) and Sliding Window Attention. It proved that efficiency, not just scale, drives capability, and sparked the "small but mighty" model movement.

### Mixtral of Experts
**Authors:** Mistral AI  
**Venue:** arXiv  
**Year:** 2024  
**Why it matters:** The first widely adopted open-source Sparse Mixture-of-Experts (MoE) LLM (8x7B), demonstrating that conditional routing could match dense model quality at significantly lower inference cost. It validated MoE as a practical architecture for production LLMs and influenced DeepSeek, Qwen, and Gemini's MoE designs.

### FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning
**Authors:** Tri Dao (Stanford / Together AI / NVIDIA)  
**Venue:** ICLR 2024  
**Year:** 2023 (arXiv) / 2024 (ICLR)  
**Why it matters:** Reduced the attention bottleneck from a quadratic memory wall to an IO-aware exact algorithm, enabling training of context lengths up to 100K+ tokens on commodity GPUs. FlashAttention-2 became the universal training kernel for modern LLMs, including Llama 2/3, GPT-4, and Claude.

### Mamba: Linear-Time Sequence Modeling with Selective State Spaces
**Authors:** Albert Gu, Tri Dao (CMU, Princeton)  
**Venue:** COLM 2023  
**Year:** 2023  
**Why it matters:** Proposed a selective state-space model (SSM) that achieves linear complexity in sequence length while maintaining Transformer-like quality. Mamba challenged the attention monopoly and opened a new research thread on subquadratic architectures, inspiring hybrid models (Jamba, Zamba) and influencing Qwen3's design.

### Mamba-2: Transformers are SSMs — Generalized Models and Efficient Algorithms Through Structured State Space Duality
**Authors:** Tri Dao, Albert Gu (CMU, Princeton)  
**Venue:** ICML 2024  
**Year:** 2024  
**Why it matters:** Established a theoretical "Structured State Space Duality" (SSD) showing that Transformers and SSMs share a unified mathematical framework, and leveraged this to build a faster, more parallelizable Mamba-2. It bridged the attention vs. RNN divide and provided the theoretical foundation for hybrid linear-attention architectures.

### DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model
**Authors:** DeepSeek-AI  
**Venue:** arXiv  
**Year:** 2024  
**Why it matters:** Introduced Multi-head Latent Attention (MLA) and an auxiliary-loss-free load balancing strategy, enabling a 236B-parameter MoE model to train efficiently on a modest budget. It demonstrated that architectural innovation could rival scale-driven brute force, and directly influenced the design of DeepSeek-V3 and Kimi.

### DeepSeek-V3 Technical Report
**Authors:** DeepSeek-AI  
**Venue:** arXiv  
**Year:** 2024  
**Why it matters:** A 671B-parameter MoE model (37B active) trained on 14.8 trillion tokens with unprecedented cost efficiency, matching GPT-4o on many benchmarks. The report detailed innovations in FP8 training, load balancing, and pipeline parallelism, becoming the canonical reference for training ultra-large MoE models economically.

---

## 3. Alignment and Preference Optimization

### Direct Preference Optimization: Your Language Model is Secretly a Reward Model
**Authors:** Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning, Chelsea Finn (Stanford)  
**Venue:** NeurIPS 2023  
**Year:** 2023  
**Why it matters:** DPO replaced the complex multi-stage RLHF pipeline (reward model + PPO) with a single supervised objective derived from the Bradley-Terry model. It democratized alignment by making preference tuning accessible to anyone with a single GPU, and spawned an entire family of algorithms (IPO, KTO, SimPO, ORPO).

### KTO: Model Alignment as Prospect Theoretic Optimization
**Authors:** Kawin Ethayarajh, Yejin Choi, Swabha Swayamdipta (Stanford, University of Washington)  
**Venue:** NeurIPS 2024  
**Year:** 2024  
**Why it matters:** Extended preference optimization to unpaired data (a single "good" or "bad" response per prompt), eliminating the need for expensive pairwise comparisons. KTO made alignment practical for real-world feedback where users rarely provide A/B comparisons, and is now standard in production RLHF pipelines.

### ORPO: Monolithic Preference Optimization without Reference Model
**Authors:** Jiwoo Hong, Noah Lee, James Thorne (KAIST)  
**Venue:** EMNLP 2024  
**Year:** 2024  
**Why it matters:** Unified supervised fine-tuning (SFT) and preference optimization into a single monolithic objective, removing the need for a frozen reference model and reducing GPU memory by approximately 40%. ORPO simplified the alignment stack for open-source fine-tuning frameworks and became the default for many community-trained chat models.

---

## 4. Reasoning and Chain-of-Thought

### Tree of Thoughts: Deliberate Problem Solving with Large Language Models
**Authors:** Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, Karthik Narasimhan (Google, Princeton)  
**Venue:** NeurIPS 2023  
**Year:** 2023  
**Why it matters:** Generalized chain-of-thought from a linear path to a tree-structured search space, allowing LLMs to explore multiple reasoning paths, backtrack, and deliberate. It established the "search + LM" paradigm that underpins modern reasoning agents and directly influenced the design of OpenAI's o1 and DeepSeek-R1.

### Learning to Reason with LLMs (OpenAI o1)
**Authors:** OpenAI  
**Venue:** OpenAI Technical Report / Blog  
**Year:** 2024  
**Why it matters:** Introduced the first large-scale "reasoning model" trained with reinforcement learning to perform extended chain-of-thought before answering, achieving PhD-level performance on math, coding, and science benchmarks. o1 proved that test-time compute scaling (longer thinking) could unlock capabilities orthogonal to model size, creating a new paradigm for LLM capability improvement.

### DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning
**Authors:** DeepSeek-AI  
**Venue:** arXiv  
**Year:** 2025  
**Why it matters:** Showed that pure reinforcement learning (without supervised fine-tuning) could elicit sophisticated reasoning behaviors, including self-verification and reflection, in an open-source model. DeepSeek-R1 matched OpenAI o1 on key benchmarks at a fraction of the cost, igniting a global race in open reasoning models and proving that RL scaling is the next frontier after pre-training.

---

## 5. Multimodal LLMs

### Gemini: A Family of Highly Capable Multimodal Models
**Authors:** Gemini Team, Google DeepMind  
**Venue:** arXiv  
**Year:** 2023  
**Why it matters:** Introduced the first natively multimodal training paradigm (text, image, audio, video, code) from the ground up, rather than bolting vision modules onto a text LLM. Gemini Ultra surpassed GPT-4 on 30 of 32 benchmarks and established "native multimodality" as the architectural standard for frontier models.

### Visual Instruction Tuning (LLaVA)
**Authors:** Haotian Liu, Chunyuan Li, Qingyang Wu, Yong Jae Lee (UW-Madison, Microsoft)  
**Venue:** NeurIPS 2023  
**Year:** 2023  
**Why it matters:** Created the first general-purpose open-source visual instruction tuning framework, showing that a simple projection layer connecting a vision encoder to an LLM could achieve strong multimodal chat performance. LLaVA became the most widely adopted open VLM architecture and spawned an entire family of vision-language models (LLaVA-1.5, LLaVA-NeXT).

### GPT-4o System Card
**Authors:** Aaron Hurst et al. (OpenAI)  
**Venue:** arXiv Technical Report  
**Year:** 2024  
**Why it matters:** The first unified, end-to-end multimodal model processing text, audio, and images in a single neural network with natural latency. GPT-4o eliminated the need for separate transcription/TTS pipelines and enabled real-time voice conversation, setting the new benchmark for "omni" multimodal AI.

### Gemini 1.5: Unlocking Multimodal Understanding Across Millions of Tokens
**Authors:** Gemini Team, Google DeepMind  
**Venue:** arXiv  
**Year:** 2024  
**Why it matters:** Extended Gemini to 1-2 million token contexts via an efficient MoE architecture and novel routing mechanisms, enabling processing of entire books, hours of video, and massive codebases in a single prompt. It redefined what "long context" means for multimodal models and made retrieval-augmented workflows optional for many tasks.

---

## 6. Open Science and Training Infrastructure

### OLMo: Accelerating the Science of Language Models
**Authors:** Dirk Groeneveld, Iz Beltagy, Pete Walsh, et al. (Ai2)  
**Venue:** arXiv  
**Year:** 2024  
**Why it matters:** The first fully open, reproducible training pipeline for a 7B/13B parameter LLM, releasing not just weights but the exact training data, code, and training logs. OLMO established a new standard for scientific transparency in LLM research, enabling controlled experiments on data attribution, memorization, and scaling that were previously impossible with closed models.

---

## 7. Frontier Models (2025–2026)

### Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities
**Authors:** Gemini Team, Google DeepMind  
**Venue:** Technical Report  
**Year:** 2025  
**Why it matters:** Gemini 2.5 Pro achieved near-perfect scores on advanced reasoning benchmarks and demonstrated native reasoning tokens, 1M+ context multimodal understanding, and deep agentic tool use. It represents the current state-of-the-art in unified multimodal reasoning and established the benchmark for 2025 frontier LLM capabilities.

---

*Compiled: July 2026*  
*Total milestone papers: 22*  
*Coverage: Foundation models, architecture and efficiency, alignment, reasoning, multimodal, open science, and frontier releases (2023–2026).*
