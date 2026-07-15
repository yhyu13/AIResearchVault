# Milestone & Trunk Papers in Reinforcement Learning (2023 – Mid-2026)

> **Curated:** 2026-07-15  
> **Scope:** Foundational, breakthrough, and direction-opening papers in RL from 2023 to July 2026. Minor incremental works are excluded.  
> **Focus Areas:** RLHF & alignment, world models & model-based RL, embodied robotics, offline RL & sequence modeling, RL-driven algorithmic/scientific discovery, multi-agent RL, and LLM-agent RL systems.

---

## 1. RLHF, Preference Learning & LLM Alignment

The post-2023 era saw a dramatic simplification and democratization of alignment pipelines. The field moved from unstable multi-stage RLHF (SFT → RM → PPO) toward direct preference optimization, verifiable-reward RL, and model-free reasoning elicitation.

---

### 1.1 Direct Preference Optimization (DPO)
- **Title:** Direct Preference Optimization: Your Language Model is Secretly a Reward Model
- **Authors:** Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning, Chelsea Finn
- **Venue:** NeurIPS 2023
- **Year:** 2023
- **Why milestone:** DPO analytically eliminates the separate reward model and PPO loop by deriving a closed-form optimal policy under the Bradley-Terry preference model. This reduces the 3-stage RLHF pipeline to a single supervised classification loss, cutting compute by ~35× and making alignment accessible to the open-source community. It remains the de-facto baseline for all subsequent preference-learning research.

---

### 1.2 KTO (Model Alignment as Prospect-Theoretic Optimization)
- **Title:** KTO: Model Alignment as Prospect Theoretic Optimization
- **Authors:** Kawin Ethayarajh, Yejin Choi, Swabha Swayamdipta
- **Venue:** NeurIPS 2024 (arXiv 2024)
- **Year:** 2024
- **Why milestone:** KTO showed that alignment is possible with only binary (good/bad) feedback signals, completely removing the need for paired preference comparisons. By grounding the loss in prospect theory, it opened alignment to domains where pairwise labels are expensive or impossible to collect, and spawned a family of reference-free, binary-signal alignment methods.

---

### 1.3 SimPO (Simple Preference Optimization)
- **Title:** SimPO: Simple Preference Optimization with a Reference-Free Reward
- **Authors:** Yu Meng, Mengzhou Xia, Danqi Chen
- **Venue:** NeurIPS 2024 (arXiv 2024)
- **Year:** 2024
- **Why milestone:** SimPO removes both the reward model and the reference model from DPO, using only an average log-probability reward with a target margin. This makes the pipeline even simpler and more compute-efficient than DPO, while matching or exceeding its performance. It represents the extreme end of the "simplification arc" in alignment algorithms.

---

### 1.4 Self-Rewarding Language Models
- **Title:** Self-Rewarding Language Models
- **Authors:** Weizhe Yuan, Richard Yuanzhe Pang, Kyunghyun Cho, Sainbayar Sukhbaatar, Jing Xu, Jason Weston
- **Venue:** ICML 2024
- **Year:** 2024
- **Why milestone:** This work demonstrated that LLMs can generate their own preference data and reward signals for iterative self-improvement, bypassing the need for human or external AI judges entirely. It established the concept of self-play preference optimization and proved that small models can bootstrap themselves to stronger performance through autonomous RL loops.

---

### 1.5 Constitutional AI / RLAIF Lineage (Active Refinement 2023–2024)
- **Title:** Constitutional AI: Harmlessness from AI Feedback (expanded follow-ups and open-source implementations through 2023–2024)
- **Authors:** Yuntao Bai, et al. (Anthropic); follow-up implementations by multiple groups
- **Venue:** Various (Anthropic technical report, 2022; widespread adoption and refinement in 2023–2024)
- **Year:** 2023–2024 (refinement period)
- **Why milestone:** While originally published in 2022, the RLAIF (RL from AI Feedback) paradigm matured in 2023–2024 as the primary scalable alternative to human RLHF. It demonstrated that explicit principles (a "constitution") can replace human preference labelers, enabling alignment to scale beyond human supervision limits. This became the backbone of Anthropic's Claude training and influenced all subsequent synthetic-data alignment pipelines.

---

### 1.6 Reinforcement Learning with Verifiable Rewards (RLVR) — Paradigm Crystallization
- **Title:** RLVR — Key implementations in DeepSeek-R1, OpenAI o1, Kimi k1.5
- **Authors:** Nathan Lambert et al. (conceptual framing); DeepSeek-AI; OpenAI; Moonshot AI
- **Venue:** Blog/technical reports, 2024; NeurIPS / ICLR 2025 papers
- **Year:** 2024–2025
- **Why milestone:** RLVR replaces learned reward models with deterministic, verifiable feedback (e.g., unit-test pass/fail, math answer correctness). This eliminated reward hacking and made RL scalable to reasoning domains. The paradigm was independently validated by OpenAI o1 (Sept 2024), DeepSeek-R1 (Jan 2025), and Kimi k1.5, establishing a new standard for post-training on STEM tasks.

---

### 1.7 OpenAI o1 — Large-Scale Reasoning via RL
- **Title:** Learning to Reason with LLMs (o1 system card / technical reports)
- **Authors:** Aaron Jaech, et al. (OpenAI)
- **Venue:** OpenAI technical report, 2024
- **Year:** 2024
- **Why milestone:** o1 was the first large-scale demonstration that RL on verifiable rewards (with extended chain-of-thought training) could elicit emergent, deliberate reasoning in LLMs. It introduced the dual scaling laws: performance improves with both train-time RL compute and test-time inference compute. This shifted the entire industry from "bigger pre-training" to "better post-training + longer thinking."

---

### 1.8 DeepSeek-R1 — Open-Source RL-First Reasoning
- **Title:** DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning
- **Authors:** DeepSeek-AI
- **Venue:** arXiv, 2025
- **Year:** 2025
- **Why milestone:** DeepSeek-R1 proved that open-weight base models can match or exceed closed proprietary reasoning models (OpenAI o1) using purely RL-based post-training—without expensive supervised CoT data. R1-Zero (the ablation) showed emergent self-verification and "aha moments" arise purely from reward signals, validating that reasoning is a trainable RL behavior rather than a pre-training emergent property.

---

### 1.9 DeepSeekMath / GRPO (Group Relative Policy Optimization)
- **Title:** DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models
- **Authors:** Zhihong Shao, et al. (DeepSeek-AI)
- **Venue:** arXiv, 2024 (introduced GRPO); ICLR 2025
- **Year:** 2024
- **Why milestone:** GRPO removes PPO's value/critic network entirely, estimating advantages by normalizing rewards across a group of responses to the same prompt. This halves GPU memory requirements and stabilizes training, making RL feasible for 70B+ models on modest hardware. GRPO became the algorithmic backbone of DeepSeek-R1 and the broader open-source reasoning movement.

---

### 1.10 DAPO / Advanced GRPO Variants
- **Title:** DAPO: An Open-Source LLM Reinforcement Learning System (and related: VAPO, Dr.GRPO, RLOO)
- **Authors:** ByteDance Seed / Tsinghua (DAPO); various groups for VAPO, Dr.GRPO
- **Venue:** arXiv 2025; NeurIPS 2025 / ICLR 2026
- **Year:** 2025
- **Why milestone:** DAPO and its siblings fixed critical stability issues in vanilla GRPO (length bias, reward collapse, token-level gradient imbalance) through techniques like dynamic sampling, clip-higher, and token-level loss aggregation. These system-level improvements pushed AIME scores from ~30 to ~50+ on 32B models, proving that algorithmic engineering matters as much as model scale for RL reasoning.

---

### 1.11 Process Reward Models & Step-Level Supervision
- **Title:** Let\'s Verify Step by Step (PRM lineage; follow-ups: Lightman et al. 2023; Wang et al. 2024; Lu et al. 2024)
- **Authors:** Hunter Lightman, et al. (OpenAI); subsequent works by multiple groups
- **Venue:** arXiv 2023; NeurIPS / ICLR 2024–2025
- **Year:** 2023–2025
- **Why milestone:** Process Reward Models (PRMs) provide dense, step-by-step correctness feedback rather than sparse outcome rewards. This line of work established that fine-grained process supervision dramatically outperforms outcome-only ORMs on multi-step reasoning, and became the theoretical foundation for tree-search RL algorithms (Tree-GRPO, TreeRPO) that dominate 2025–2026 agent training.

---

## 2. World Models & Model-Based Reinforcement Learning

Model-based RL experienced a renaissance from 2023 onward, driven by scalable latent dynamics, transformer-based world models, and the convergence of video generation with control.

---

### 2.1 DreamerV3 — Universal World Model
- **Title:** Mastering Diverse Domains through World Models
- **Authors:** Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, Timothy P. Lillicrap
- **Venue:** Nature, 2025 (arXiv 2023)
- **Year:** 2023 (arXiv); 2025 (Nature)
- **Why milestone:** DreamerV3 solved 150+ diverse tasks (Atari, MuJoCo, Crafter, DMLab, BSuite) with a single set of hyperparameters—no per-task tuning. Key innovations included symlog losses for reward-scale invariance, discrete latent representations, and elimination of KL annealing. It was the first model-based RL algorithm to comprehensively outperform model-free SOTA across domains, proving general world-model learning is feasible.

---

### 2.2 TD-MPC2 — Scalable Continuous Control World Models
- **Title:** TD-MPC2: Scalable, Robust World Models for Continuous Control
- **Authors:** Nicklas Hansen, Hao Su, Xiaolong Wang
- **Venue:** ICLR 2024
- **Year:** 2024
- **Why milestone:** TD-MPC2 scaled temporal-difference learning for model predictive control to large multi-task domains, combining latent dynamics with local trajectory optimization. It demonstrated that model-based RL can match or exceed SAC/PPO on challenging continuous-control benchmarks while being more sample-efficient, and established the TD-MPC family as a standard baseline for robot learning.

---

### 2.3 I-JEPA — Image World Models via Joint-Embedding Prediction
- **Title:** Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture
- **Authors:** Mahmoud Assran, Quentin Duval, Ishan Misra, Piotr Bojanowski, Pascal Vincent, Yann LeCun, Nicolas Ballas, Michael Rabbat
- **Venue:** CVPR 2023
- **Year:** 2023
- **Why milestone:** I-JEPA was the first practical implementation of LeCun's non-generative world-model vision. Instead of reconstructing pixels, it predicts representations of masked image regions in latent space, discarding unpredictable noise. This established a new paradigm for self-supervised learning that directly inspired the video and robotics world models that followed (V-JEPA, V-JEPA 2).

---

### 2.4 V-JEPA — Video Joint-Embedding Predictive Architecture
- **Title:** V-JEPA: Revisiting Feature Prediction for Learning Visual Representations from Video
- **Authors:** Adrien Bardes, Jérôme Revaud, Yann LeCun, et al. (Meta FAIR)
- **Venue:** ICLR 2025 (arXiv 2024)
- **Year:** 2024
- **Why milestone:** V-JEPA extended JEPA to video, learning spatio-temporal representations purely by predicting masked video features in latent space—without pixel reconstruction, text labels, or pre-trained image encoders. It demonstrated that video world models can learn physical intuitions (gravity, object permanence) from unlabeled footage alone, rivaling and sometimes exceeding supervised pre-training on downstream tasks.

---

### 2.5 V-JEPA 2 — Video World Models for Planning
- **Title:** V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning
- **Authors:** Mido Assran, et al. (Meta FAIR)
- **Venue:** arXiv 2025
- **Year:** 2025
- **Why milestone:** Trained on over 1 million hours of video, V-JEPA 2 is a 1.2B-parameter world model capable of zero-shot robotic planning. Its action-conditioned variant (V-JEPA 2-AC) predicts how latent states change under robot actions, enabling real-time planning without task-specific training. This is the first large-scale demonstration that a generic video world model can transfer directly to embodied control.

---

### 2.6 EfficientZero V2 — Discrete & Continuous Control with Limited Data
- **Title:** EfficientZero V2: Mastering Discrete and Continuous Control with Limited Data
- **Authors:** Various (DeepMind / Tsinghua collaboration)
- **Venue:** ICML 2024 (Spotlight)
- **Year:** 2024
- **Why milestone:** EfficientZero V2 unified MuZero-style planning for both discrete and continuous action spaces while dramatically improving sample efficiency. It demonstrated that model-based MCTS can be made data-efficient enough for real-world robotics, bridging the gap between board-game success (AlphaZero) and physical control.

---

### 2.7 UniZero — Generalized Planning with Scalable World Models
- **Title:** UniZero: Generalized and Efficient Planning with Scalable World Models
- **Authors:** Yao Pu, et al.
- **Venue:** arXiv 2024 (ICLR 2025)
- **Year:** 2024
- **Why milestone:** UniZero integrated transformer-based latent world models with MCTS planning, addressing long-term dependency modeling in partially observable environments. It unified the Dreamer (actor-critic imagination) and MuZero (MCTS planning) lineages into a single architecture, demonstrating that transformer world models can support both policy gradients and tree search.

---

### 2.8 Genie — Generative Interactive Environments
- **Title:** Genie: Generative Interactive Environments
- **Authors:** Jake Bruce, et al. (Google DeepMind)
- **Venue:** ICML 2024
- **Year:** 2024
- **Why milestone:** Genie showed that text-conditioned generative models can produce interactive, explorable 2D game worlds from a single image or text prompt. Unlike prior world models that learned single-environment dynamics, Genie generates diverse, controllable environments, opening a path toward "training in the dream" on procedurally infinite simulated worlds.

---

### 2.9 DIAMOND / EMERALD — Diffusion & Masked Generative World Models
- **Title:** DIAMOND: Diffusion for World Modeling; EMERALD: Masked Generative Transformers for World Models
- **Authors:** Alonso et al. (DIAMOND); Burchi & Timofte (EMERALD)
- **Venue:** NeurIPS 2024 / 2025
- **Year:** 2024–2025
- **Why milestone:** These works demonstrated that diffusion models and masked generative transformers can serve as high-fidelity world simulators for RL. DIAMOND produced visually faithful Atari rollouts; EMERALD achieved state-of-the-art Crafter performance. They established that generative world models are not just for video generation but can be directly integrated into RL policy training.

---

## 3. Robotics & Embodied Reinforcement Learning

Robotics RL was transformed by vision-language-action (VLA) models, diffusion policies, and large-scale cross-embodiment datasets. The field moved from task-specific controllers to generalist policies.

---

### 3.1 RT-2 — Vision-Language-Action Models for Robot Control
- **Title:** RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control
- **Authors:** Anthony Brohan, et al. (Google DeepMind)
- **Venue:** CoRL 2023
- **Year:** 2023
- **Why milestone:** RT-2 was the first VLA model, co-fine-tuning large vision-language models (PaLI-X, PaLM-E) on robot trajectories by treating actions as text tokens. It transferred internet-scale semantic knowledge to physical control, enabling emergent skills (e.g., "pick up the object about to fall off the table") never seen in robot data. This established the VLA paradigm that dominates robot learning today.

---

### 3.2 RT-X / Open X-Embodiment — Cross-Embodiment Generalist Policies
- **Title:** Open X-Embodiment: Robotic Learning Datasets and RT-X Models
- **Authors:** Open X-Embodiment Collaboration (Quan Vuong, Pannag Sanketi, et al.)
- **Venue:** ICRA 2024 (DeepMind blog Oct 2023)
- **Year:** 2023–2024
- **Why milestone:** RT-X pooled data from 22 robot types across 33 academic labs into a single dataset, training one model that generalizes across embodiments. RT-1-X achieved 50% higher success rates than embodiment-specific methods, and RT-2-X tripled performance on real-world skills. This proved that cross-embodiment training—similar to web-scale pre-training in NLP—works for robotics.

---

### 3.3 Q-Transformer — Scalable Offline RL for Robot Manipulation
- **Title:** Q-Transformer: Scalable Offline Reinforcement Learning via Autoregressive Q-Functions
- **Authors:** Yevgen Chebotar, Quan Vuong, Alex Irpan, et al. (Google DeepMind)
- **Venue:** CoRL 2023
- **Year:** 2023
- **Why milestone:** Q-Transformer scaled Q-learning to large transformer architectures for robotic manipulation, enabling training on massive, mixed-quality offline datasets. It combined the expressiveness of transformers with the conservative value estimation needed for offline RL, demonstrating that Q-learning (not just imitation or sequence modeling) can work at scale in robotics.

---

### 3.4 Diffusion Policy — Visuomotor Control via Action Diffusion
- **Title:** Diffusion Policy: Visuomotor Policy Learning via Action Diffusion
- **Authors:** Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, Shuran Song
- **Venue:** RSS 2023
- **Year:** 2023
- **Why milestone:** Diffusion Policy replaced deterministic action regression with conditional diffusion models for robot control, enabling multimodal action distributions (critical for tasks with multiple valid solutions). It became one of the most influential robot learning frameworks, with hundreds of follow-up works, and proved that generative models can serve as expressive policy representations for physical systems.

---

### 3.5 Octo — Open-Source Generalist Robot Policy
- **Title:** Octo: An Open-Source Generalist Robot Policy
- **Authors:** Octo Model Team (Berkeley / Stanford / DeepMind collaboration)
- **Venue:** RSS 2024
- **Year:** 2024
- **Why milestone:** Octo is an open-source, transformer-based generalist policy trained on 800k+ diverse trajectories, supporting image, language, and proprioception inputs. It demonstrated that open-weight robot policies can match the performance of closed proprietary models (RT-2, RT-X), democratizing access to generalist robot control and establishing an open standard for VLA architectures.

---

### 3.6 OpenVLA — Open-Source Vision-Language-Action Model
- **Title:** OpenVLA: An Open-Source Vision-Language-Action Model
- **Authors:** Kim et al. (Stanford / Berkeley / various)
- **Venue:** CoRL 2024
- **Year:** 2024
- **Why milestone:** OpenVLA released a 7B-parameter open-source VLA model that achieves strong results across diverse manipulation tasks. It proved that smaller, open models can compete with large proprietary VLAs when trained on curated cross-embodiment data, and it catalyzed the open-source robotics ecosystem (LeRobot, Pi0, etc.).

---

### 3.7 π0 (Pi-Zero) — Flow-Matching Generalist Robot Policy
- **Title:** π0: A Vision-Language-Action Flow Model for Generalist Robot Control
- **Authors:** Kevin Black, et al. (Physical Intelligence)
- **Venue:** CoRL 2024
- **Year:** 2024
- **Why milestone:** π0 introduced flow matching (a continuous normalizing flow variant) to robot policy learning, enabling high-frequency, dexterous control with a mixture-of-experts architecture. Trained on 10M+ demonstrations, it demonstrated few-shot generalization to new tasks and embodiments, and established flow-based policies as a viable alternative to autoregressive/discrete VLA models.

---

### 3.8 GR00T N1 — NVIDIA Humanoid Foundation Model
- **Title:** GR00T N1: An Open Foundation Model for Generalist Humanoid Robots
- **Authors:** NVIDIA GEAR Team
- **Venue:** arXiv / Technical Report 2025
- **Year:** 2025
- **Why milestone:** GR00T N1 is a 1.5B-parameter open foundation model for humanoid robots, supporting multi-task visuomotor control across embodiments. It represents the industry's first major open-source humanoid foundation model, enabling transfer of policies across different humanoid hardware platforms and catalyzing standardization in the humanoid robotics race.

---

## 4. Offline RL, Sequence Modeling & Decision Transformers

The Decision Transformer line evolved from pure sequence modeling toward hybrid methods that integrate Q-learning, value guidance, and hierarchical structures for generalization.

---

### 4.1 Q-Learning Decision Transformer (QDT)
- **Title:** Q-learning Decision Transformer: Leveraging Dynamic Programming for Conditional Sequence Modelling in Offline RL
- **Authors:** Taku Yamagata, Ahmed Khalil, Raul Santos-Rodriguez
- **Venue:** ICML 2023
- **Year:** 2023
- **Why milestone:** QDT bridged the gap between Q-learning and Decision Transformers, showing that dynamic programming (value estimation) can be fused with sequence modeling to overcome DT\'s limitations in stochastic environments. It established that hybrid value+sequence architectures outperform pure return-conditioned supervised learning on standard offline RL benchmarks.

---

### 4.2 Elastic Decision Transformer
- **Title:** Elastic Decision Transformer
- **Authors:** Yueh-Hua Wu, Xiaolong Wang, Masashi Hamaya
- **Venue:** NeurIPS 2023
- **Year:** 2023
- **Why milestone:** Elastic DT introduced adaptive context length and token selection for decision transformers, enabling the model to dynamically allocate attention to relevant historical states/actions. This solved the quadratic attention cost problem for long-horizon tasks and improved generalization to unseen task lengths.

---

### 4.3 Supported Policy Optimization (SPOT)
- **Title:** Supported Policy Optimization for Offline Reinforcement Learning
- **Authors:** Jialong Wu, Haixu Wu, Zihan Qiu, Jianmin Wang, Mingsheng Long
- **Venue:** NeurIPS 2022 (arXiv); widely adopted and extended in 2023–2024
- **Year:** 2022 (foundational); 2023–2024 (extensions)
- **Why milestone:** SPOT introduced a pluggable, VAE-based behavior density regularizer that can be added to any off-policy RL algorithm for offline training. It achieved SOTA on D4RL and AntMaze benchmarks and seamlessly enabled online fine-tuning after offline initialization. Its modular design made it the standard "add-on" for offline-to-online RL pipelines.

---

### 4.4 Value-Guided Decision Transformer (VDT)
- **Title:** Value-Guided Decision Transformer: A Unified RL Framework for Online and Offline Settings
- **Authors:** Hongling Zheng, Li Shen, Yong Luo, Deheng Ye, Shuhan Xu, Bo Du, Jialie Shen, Dacheng Tao
- **Venue:** NeurIPS 2025
- **Year:** 2025
- **Why milestone:** VDT unified offline and online RL under a single decision transformer architecture, using value functions for advantage-weighted behavior regularization during offline pre-training and switching to value-based policy improvement during online fine-tuning. It proved that DTs can be a universal backbone for both settings, not just offline imitation.

---

### 4.5 Long-Short Decision Transformer
- **Title:** Long-Short Decision Transformer: Bridging Global and Local Dependencies for Generalized Decision-Making
- **Authors:** Jincheng Wang, Penny Karanasou, Pengyuan Wei, Elia Gatti, Diego Martinez Plasencia, Dimitrios Kanoulas
- **Venue:** ICLR 2025
- **Year:** 2025
- **Why milestone:** This work addressed the critical limitation of DTs in capturing both long-range strategic dependencies and short-term reactive control. By explicitly modeling dual timescales, it enabled generalization to new tasks and environments without re-training, marking a significant step toward transferable sequence-modeling policies.

---

## 5. RL for Algorithmic & Scientific Discovery

RL was deployed to discover new algorithms, mathematical proofs, and physical control strategies—demonstrating that RL can innovate beyond human-designed solutions.

---

### 5.1 AlphaDev — Discovering Faster Sorting Algorithms
- **Title:** AlphaDev: Faster Sorting Algorithms Discovered Using Deep RL
- **Authors:** Daniel Mankowitz, et al. (Google DeepMind)
- **Venue:** Nature, 2023
- **Year:** 2023
- **Why milestone:** AlphaDev used deep RL to discover new sorting and hashing algorithms that outperformed decades of human-optimized code. Its sorting improvement was integrated into the C++ Standard Library—marking the first time an RL-discovered algorithm was adopted into core software infrastructure used trillions of times daily. It proved RL can optimize low-level computational primitives.

---

### 5.2 AlphaProof — Formal Mathematical Reasoning via RL
- **Title:** AlphaProof: Formal Mathematical Reasoning via RL (part of IMO 2024 solution system)
- **Authors:** Google DeepMind
- **Venue:** Nature / Technical Report, 2024
- **Year:** 2024
- **Why milestone:** AlphaProof combined a language model with AlphaZero-style RL to solve formal mathematical proof problems. At the 2024 International Mathematical Olympiad, AlphaProof + AlphaGeometry 2 solved problems at the silver-medalist level. This established RL as a viable approach to formal theorem proving and mathematical reasoning at the highest human competition levels.

---

### 5.3 AlphaTensor / AlphaGeometry 2 — Mathematical Discovery (Active Period 2023–2024)
- **Title:** AlphaTensor (Nature 2022); AlphaGeometry 2 (2024 IMO system)
- **Authors:** Alhussein Fawzi, et al. (AlphaTensor); DeepMind team (AlphaGeometry 2)
- **Venue:** Nature 2022; 2024 IMO demonstration
- **Year:** 2022 (AlphaTensor); 2024 (AlphaGeometry 2)
- **Why milestone:** AlphaTensor discovered new matrix multiplication algorithms, beating Strassen\'s 1969 record for 4×4 matrices. AlphaGeometry 2 extended the geometry solver to human-IMO gold-medal level. Together, they demonstrated that RL + search can make novel discoveries in pure mathematics, shifting the perception of AI from "tool" to "discoverer."

---

## 6. Multi-Agent Reinforcement Learning (MARL)

MARL advanced through LLM-based agents, scalable sequence models, and principled game-theoretic frameworks.

---

### 6.1 MAPPO / HAPPO — Principled Multi-Agent Policy Optimization
- **Title:** The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games (MAPPO); HAPPO: Trust Region Policy Optimisation in Multi-Agent RL
- **Authors:** Chao Yu, et al. (MAPPO, 2021); Jakub Grudzien Kuba, et al. (HAPPO, ICLR 2022)
- **Venue:** AAMAS 2021; ICLR 2022
- **Year:** 2021–2022 (foundational); dominant adoption 2023–2025
- **Why milestone:** While published pre-2023, MAPPO and HAPPO became the dominant MARL baselines during 2023–2025. HAPPO provided the first theoretically grounded multi-agent trust-region method, proving monotonic improvement guarantees under multi-agent factorization. They established the standard for multi-agent policy gradient training in game AI, autonomous driving, and swarm robotics.

---

### 6.2 Sable — Scalable Sequence Models for MARL
- **Title:** Sable: A Performant, Efficient and Scalable Sequence Model for Multi-Agent Reinforcement Learning
- **Authors:** O. Mahjoub, et al.
- **Venue:** arXiv 2024; ICLR 2025
- **Year:** 2024–2025
- **Why milestone:** Sable scaled transformer sequence models to multi-agent settings, demonstrating that attention-based architectures can handle large agent populations without exponential state-space blowup. It established sequence modeling as a viable alternative to value decomposition (QMIX/VDN) for many-agent scenarios.

---

### 6.3 ZSC-Eval & Coordinated Multi-Agent Imitation
- **Title:** ZSC-Eval: An Evaluation Toolkit and Benchmark for Multi-agent Zero-shot Coordination
- **Authors:** Xihuai Wang, Shao Zhang, Wenhao Zhang, et al.
- **Venue:** NeurIPS 2024
- **Year:** 2024
- **Why milestone:** ZSC-Eval provided the first rigorous benchmark for zero-shot coordination—training agents to collaborate with unseen partners, a critical capability for human-AI teaming. It established standardized metrics and environments that unified previously fragmented MARL evaluation practices.

---

### 6.4 LLM-Based Multi-Agent Collaboration (Survey & Frameworks)
- **Title:** Large Language Model Based Multi-Agents: A Survey of Progress and Challenges; CoMAS: Co-Evolving Multi-Agent Systems via Interaction Rewards
- **Authors:** Guo et al. (Survey, 2024); Xue et al. (CoMAS, 2025)
- **Venue:** arXiv 2024; 2025
- **Year:** 2024–2025
- **Why milestone:** These works formalized the intersection of LLMs and MARL, showing that language agents can serve as negotiators, planners, and coordinators in multi-agent environments. CoMAS introduced interaction rewards for emergent collaboration, establishing that LLM agents can evolve social behaviors through multi-turn RL.

---

## 7. LLM Agents, Tool Use & Interactive RL Systems

A new subfield emerged: treating LLM-based agents as RL policies in interactive environments, with multi-turn reasoning, tool use, and environment feedback.

---

### 7.1 ReAct — Reasoning + Acting in Language Models
- **Title:** ReAct: Synergizing Reasoning and Acting in Language Models
- **Authors:** Shunyu Yao, Jeffrey Zhao, Yuhan Du, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, Karthik Narasimhan
- **Venue:** ICLR 2023
- **Year:** 2023
- **Why milestone:** ReAct interleaved chain-of-thought reasoning with action execution (tool calls, API requests, web navigation) in a single LLM trajectory. It established the "thought → action → observation" loop that became the standard architecture for all LLM agents, bridging reasoning and RL-style environment interaction.

---

### 7.2 Reflexion — Verbal Reinforcement Learning for Agents
- **Title:** Reflexion: Language Agents with Verbal Reinforcement Learning
- **Authors:** Noah Shinn, Beck Labash, Ashwin Gopinath
- **Venue:** NeurIPS 2023
- **Year:** 2023
- **Why milestone:** Reflexion replaced scalar RL rewards with natural-language self-reflection, allowing agents to critique their own trajectories and formulate improvement strategies in text. This introduced "verbal RL"—a new paradigm where language itself serves as the reward/gradient signal, making failure analysis interpretable and enabling zero-shot adaptation without parameter updates.

---

### 7.3 Toolformer — LLMs Teaching Themselves Tool Use
- **Title:** Toolformer: Language Models Can Teach Themselves to Use Tools
- **Authors:** Timo Schick, et al. (Meta AI)
- **Venue:** NeurIPS 2023
- **Year:** 2023
- **Why milestone:** Toolformer demonstrated that LLMs can autonomously learn when and how to invoke external tools (calculators, search engines, APIs) through self-supervised training on tool-augmented text. It established the foundation for all subsequent tool-integrated LLM agents, proving that tool use is an emergent, trainable skill rather than a hard-coded pipeline.

---

### 7.4 AgentGym / AgentGym-RL — Unified Platform for LLM Agent RL
- **Title:** AgentGym: Evolving Large Language Model-based Agents across Diverse Environments; AgentGym-RL: Training LLM Agents for Long-Horizon Decision Making through Multi-Turn Reinforcement Learning
- **Authors:** Zhiheng Xi, et al. (Fudan / various)
- **Venue:** ACL 2025 (AgentGym); ICLR 2026 Oral (AgentGym-RL)
- **Year:** 2024–2025
- **Why milestone:** AgentGym created the first unified, modular platform for training and evaluating LLM agents across diverse environments (web, games, coding, embodied tasks). AgentGym-RL added multi-turn RL training with curriculum scaling (ScalingInter-RL), demonstrating that open-source 7B models can match or exceed commercial agents (o3, Gemini-2.5-Pro) on 27 tasks. It established the standard infrastructure for the emerging LLM-agent RL field.

---

### 7.5 SWE-agent / OpenManus-RL — RL for Software Engineering Agents
- **Title:** SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering; OpenManus-RL: RL Tuning for LLM Agents
- **Authors:** John Yang, et al. (Princeton / CMU); UIUC / MetaGPT team (OpenManus-RL)
- **Venue:** NeurIPS 2024 (SWE-agent); arXiv 2025 (OpenManus-RL)
- **Year:** 2024–2025
- **Why milestone:** SWE-agent designed specialized agent-computer interfaces for autonomous coding, achieving state-of-the-art performance on SWE-bench. OpenManus-RL extended this with RL fine-tuning, proving that multi-turn RL on software environments can significantly improve bug-fixing and code-generation capabilities. Together, they established RL for software engineering as a distinct, high-impact subfield.

---

### 7.6 R3 / Reverse Curriculum RL for Reasoning
- **Title:** R3: Training Large Language Models for Reasoning through Reverse Curriculum Reinforcement Learning
- **Authors:** (ICML 2024 paper; related to AgentGym authors)
- **Venue:** ICML 2024
- **Year:** 2024
- **Why milestone:** R3 introduced reverse curriculum learning for RL-based reasoning, where agents start from solution states and work backward to problem statements. This dramatically improved exploration efficiency for long-horizon reasoning tasks, and demonstrated that curriculum design is as critical as algorithm choice for LLM agent RL.

---

## 8. Key RL Theory, Convergence & Safety (2023–2026)

Fundamental theoretical work advanced understanding of RL convergence, robustness, and the limitations of standard algorithms.

---

### 8.1 Counteractive RL — Rethinking Core Principles
- **Title:** Counteractive RL: Rethinking Core Principles for Efficient and Scalable Deep Reinforcement Learning
- **Authors:** Ezgi Korkmaz
- **Venue:** NeurIPS 2025 (Spotlight)
- **Year:** 2025
- **Why milestone:** This NeurIPS Spotlight paper challenged fundamental RL assumptions, proposing counteractive mechanisms that improve sample efficiency and scalability. It provided theoretical and empirical evidence that standard RL design paradigms have hidden inefficiencies, and offered principled solutions with strong guarantees.

---

### 8.2 Global Convergence of Multi-Agent Policy Gradient
- **Title:** Global Convergence of Multi-Agent Policy Gradient in Markov Potential Games
- **Authors:** Stefanos Leonardos, Will Overman, Ioannis Panageas, Georgios Piliouras
- **Venue:** AISTATS / NeurIPS 2021 (foundational); extended and validated in 2023–2025
- **Year:** 2021 (theory); 2023–2025 (empirical validation)
- **Why milestone:** This paper proved global convergence guarantees for multi-agent policy gradient methods in Markov potential games—a broad class of cooperative-competitive environments. During 2023–2025, it became the theoretical backbone for scalable MARL training, as empirical works validated its assumptions in large-scale experiments.

---

### 8.3 Understanding and Diagnosing Deep RL
- **Title:** Understanding and Diagnosing Deep Reinforcement Learning
- **Authors:** Ezgi Korkmaz
- **Venue:** ICML 2024
- **Year:** 2024
- **Why milestone:** This work provided a systematic diagnostic framework for identifying failure modes in deep RL training (value divergence, policy collapse, representation degeneration). It became a standard reference for practitioners debugging unstable RL pipelines, and established rigorous evaluation protocols adopted in NeurIPS/ICML 2024–2025 works.

---

## 9. Emergent Directions & Cross-Cutting Themes (2025–2026)

These are not single papers but convergent research directions that crystallized in 2025–2026 and are reshaping RL.

---

### 9.1 RL for Reasoning = "RL is so back"
- **Key works:** DeepSeek-R1, OpenAI o3, Kimi k1.5, QwQ, Gemini 2.5, DAPO, VAPO, Tree-GRPO, SimpleRL-Reason
- **Year:** 2024–2026
- **Why milestone:** The 2024–2026 period saw RL transition from an alignment/robotics technique to the primary driver of LLM reasoning capability. Pure RL (no SFT) on base models can elicit CoT, self-verification, and backtracking—behaviors previously thought to require massive supervised data. This paradigm shift is arguably the most significant RL development of the period.

---

### 9.2 Video Generators as World Models (World Action Models)
- **Key works:** World Action Models (WAMs), Sora-as-simulator, Genie 3, Video Prediction Policies
- **Year:** 2025–2026
- **Why milestone:** Video generation models (diffusion, flow, autoregressive) are increasingly being repurposed as action-conditioned world models for robotics and planning. Unlike traditional RL world models that predict single-environment dynamics, these models capture general physical laws from internet-scale video, enabling zero-shot transfer to new tasks.

---

### 9.3 RL for Post-Training Dominance
- **Key works:** OpenAI o-series, DeepSeek-R1, Claude 3.7/4, Llama 4, GLM-4.5+
- **Year:** 2024–2026
- **Why milestone:** By 2025, post-training (RL + preference optimization) accounted for the majority of usable model capability gains, surpassing pre-training scaling for many tasks. Liquid AI and Meta benchmarks showed 20–40% improvements from post-training alone—gains that would require orders of magnitude more pre-training compute to achieve. RL has become the bottleneck and frontier of foundation model development.

---

## Summary Statistics

| Category | Papers | Key Venues |
|----------|--------|------------|
| RLHF & Alignment | 11 | NeurIPS, ICML, ICLR, arXiv |
| World Models & MBRL | 9 | Nature, ICLR, ICML, CVPR, NeurIPS |
| Robotics & Embodied RL | 8 | CoRL, RSS, ICRA, ICLR, NeurIPS |
| Offline RL & Sequence Modeling | 5 | NeurIPS, ICML, ICLR |
| RL for Algorithm/Science Discovery | 3 | Nature, IMO 2024 |
| Multi-Agent RL | 4 | NeurIPS, ICLR, AAMAS |
| LLM Agents & Tool Use | 6 | ICLR, NeurIPS, ACL, ICML |
| RL Theory & Safety | 3 | NeurIPS, ICML |
| **Total** | **49** | |

---

> **Disclaimer:** Author lists and exact venue names are compiled from public sources (arXiv, conference proceedings, official repositories). For papers with very large author lists, "et al." is used. For papers with evolving venue status (e.g., arXiv preprints later accepted to conferences), both are noted where known. Curated in July 2026; some 2025–2026 papers may have pending final publication details.
