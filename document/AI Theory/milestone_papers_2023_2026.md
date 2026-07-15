# AI Theory Milestone Papers (2023 – mid-2026)

> A curated list of the most important, foundational, and direction-opening papers in AI Theory from 2023 to July 2026.
> Focus: trunk papers that establish new paradigms, settle long-standing debates, or open major research directions.
> Excludes minor incremental works.

---

## Table of Contents

- [1. Scaling Laws & Neural Network Theory](#1-scaling-laws--neural-network-theory)
- [2. In-Context Learning Theory](#2-in-context-learning-theory)
- [3. Mechanistic Interpretability](#3-mechanistic-interpretability)
- [4. Grokking, Emergence & Phase Transitions](#4-grokking-emergence--phase-transitions)
- [5. Reasoning, Chain-of-Thought & Test-Time Compute](#5-reasoning-chain-of-thought--test-time-compute)
- [6. Model Merging & Loss Landscape Geometry](#6-model-merging--loss-landscape-geometry)
- [7. Learning Theory, Generalization & Optimization](#7-learning-theory-generalization--optimization)
- [8. AI Alignment, Safety & Formal Methods](#8-ai-alignment-safety--formal-methods)

---

## 1. Scaling Laws & Neural Network Theory

### 1.1 Explaining Neural Scaling Laws
- **Authors:** Yasaman Bahri, Ethan Dyer, Jared Kaplan, Jaehoon Lee, Utkarsh Sharma
- **Venue:** PNAS, 2024
- **Year:** 2024
- **Why it matters:** This paper provides a first-principles theoretical explanation for why neural scaling laws follow power-law behavior. It connects scaling exponents to the spectral properties of data covariance and the structure of the target function, moving scaling laws from empirical observation to predictive theory. A foundational work for any principled discussion of model-size vs. data-size trade-offs.

### 1.2 A Dynamical Model of Neural Scaling Laws
- **Authors:** Blake Bordelon, Alexander Atanasov, Cengiz Pehlevan
- **Venue:** arXiv (widely cited in 2024–2025 scaling-law literature)
- **Year:** 2024
- **Why it matters:** Proposes a unified dynamical-systems perspective that predicts both the power-law and the data-limited regimes of scaling. The model explicitly links scaling exponents to the eigenspectrum of the NTK and shows how feature learning modifies the classical Kaplan/Chinchilla picture. It became the go-to theoretical framework for understanding why different architectures and tasks yield different scaling exponents.

### 1.3 How Feature Learning Can Improve Neural Scaling Laws
- **Authors:** Blake Bordelon, Alexander Atanasov, Cengiz Pehlevan
- **Venue:** ICLR 2025
- **Year:** 2025
- **Why it matters:** Extends the dynamical scaling model to the rich/feature-learning regime, demonstrating that feature learning can produce steeper (more favorable) scaling exponents than the lazy/NTK regime. This directly addresses the question of whether current scaling-law pessimism is a fundamental limit or merely an artifact of poorly optimized training dynamics. It provides actionable guidance for how to train to achieve better scaling.

### 1.4 Tensor Programs VI: Feature Learning in Infinite-Depth Neural Networks
- **Authors:** Greg Yang, Dingli Yu, Chen Zhu, S. Hayou
- **Venue:** arXiv, 2023
- **Year:** 2023
- **Why it matters:** The Tensor Programs framework is the most rigorous tool for deriving infinite-width limits and understanding hyperparameter scaling. This installment extends the theory to infinite depth, enabling principled depth-scaling analysis and hyperparameter transfer across depth. It is essential for understanding why muP (Maximal Update Parameterization) works and for engineering training recipes that transfer across model scales.

---

## 2. In-Context Learning Theory

### 2.1 Transformers Learn In-Context by Gradient Descent
- **Authors:** Johannes von Oswald, Eyvind Niklasson, Ettore Randazzo, João Sacramento, Alexander Mordvintsev, Andrey Zhmoginov, Max Vladymyrov
- **Venue:** ICML 2023
- **Year:** 2023
- **Why it matters:** The seminal paper that proved transformers implement a form of gradient descent inside their forward pass during in-context learning. By showing that linear self-attention layers effectively perform preconditioned gradient steps on a linear regression objective defined by the context, this paper transformed in-context learning from a mysterious empirical phenomenon into a mechanistically understood algorithm. It spawned an entire subfield of transformers-as-algorithms research.

### 2.2 Transformers Learn to Implement Preconditioned Gradient Descent for In-Context Learning
- **Authors:** Kwangjun Ahn, Xiang Cheng, Hadi Daneshmand, Suvrit Sra
- **Venue:** NeurIPS 2023
- **Year:** 2023
- **Why it matters:** Strengthens and generalizes the gradient descent in context thesis by showing that transformers learn to implement preconditioned gradient descent, explaining why they outperform naive gradient descent baselines. It provides convergence-rate analysis and clarifies the role of the attention mechanism as an adaptive optimizer, establishing a rigorous theoretical foundation for understanding how LLMs learn from few-shot prompts.

### 2.3 Trained Transformers Learn Linear Models In-Context
- **Authors:** Ruiqi Zhang, Spencer Frei, Peter L. Bartlett
- **Venue:** JMLR, 2024
- **Year:** 2024
- **Why it matters:** A rigorous statistical-learning-theory treatment showing that trained transformers provably learn to perform linear regression in-context, with explicit generalization bounds. This paper bridges the gap between the algorithmic/mechanistic view (transformers run GD) and the statistical view (transformers generalize from in-context examples), providing a unified theoretical framework that connects to classical learning theory.

### 2.4 One Step of Gradient Descent is Provably the Optimal In-Context Learner with One Layer of Linear Self-Attention
- **Authors:** Arvind V. Mahankali, Tatsunori Hashimoto, Tengyu Ma
- **Venue:** ICLR 2024
- **Year:** 2024
- **Why it matters:** Proves a sharp optimality result: for the linear-regression in-context learning task, a single layer of linear self-attention is equivalent to the optimal single-step gradient-descent algorithm. This is not merely an analogy but a provable equivalence, giving the first instance where a transformer component is shown to be uniquely optimal for a well-defined learning problem. It sets the standard for what understanding ICL should mean.

---

## 3. Mechanistic Interpretability

### 3.1 Towards Monosemanticity: Decomposing Language Models with Dictionary Learning
- **Authors:** Trenton Bricken, Adly Templeton, Joshua Batson, Brian Chen, Adam Jermyn, Tom Conerly, Nick Turner, Cem Anil, Carson Denison, Amanda Askell, et al. (Anthropic)
- **Venue:** Transformer Circuits Thread, 2023
- **Year:** 2023
- **Why it matters:** Introduced Sparse Autoencoders (SAEs) as a scalable method for extracting monosemantic (human-interpretable) features from polysemantic neurons in language models. This work moved mechanistic interpretability from manual circuit-tracing of toy models to an automated, large-scale feature-extraction paradigm. It established the technical foundation for the explosion of SAE research in 2024–2025 and is arguably the most important interpretability advance since the original Transformer Circuits thread.

### 3.2 Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet
- **Authors:** Adly Templeton, Tom Conerly, Jonathan Marcus, Jack Lindsey, Trenton Bricken, Brian Chen, Adam Pearce, Craig Citro, Emmanuel Ameisen, Andy Jones, et al. (Anthropic)
- **Venue:** Transformer Circuits Thread, 2024
- **Year:** 2024
- **Why it matters:** Scaled sparse autoencoder feature extraction to a production-grade model (Claude 3 Sonnet), demonstrating that SAEs can find features at scale that are not only interpretable but also causally actionable (e.g., a Golden Gate Bridge feature that can be amplified or suppressed to change model behavior). This paper proved that mechanistic interpretability is feasible on state-of-the-art models, not just GPT-2-small, and opened the door to safety-relevant intervention at the feature level.

### 3.3 Circuit Tracing: Revealing Computational Graphs in Language Models
- **Authors:** Emmanuel Ameisen, Jack Lindsey, Adam Pearce, Wes Gurnee, Nicholas L. Turner, Brian Chen, Craig Citro, David Abrahams, Shan Carter, Basil Hosmer, et al. (Anthropic)
- **Venue:** Transformer Circuits Thread, 2025
- **Year:** 2025
- **Why it matters:** Introduces automated circuit-tracing as a scalable alternative to hand-crafted circuit analysis. By combining attribution graphs with SAE features, the authors can automatically discover the computational graph responsible for specific behaviors in large models. This is a major methodological advance that attempts to make mechanistic interpretability systematic and reproducible rather than artisanal.

### 3.4 Position: Mechanistic Interpretability Must Disclose Identification Assumptions for Causal Claims
- **Authors:** (Position paper, 2026)
- **Venue:** arXiv, 2026
- **Year:** 2026
- **Why it matters:** A critical methodological intervention that diagnoses a systematic weakness in the MI literature: causal claims are often made without stated identification assumptions. The paper documents how downstream work repeatedly discovers that earlier causal claims fail under scrutiny, and proposes a strict disclosure protocol. This is a milestone for the metascience of interpretability, ensuring that the field matures with epistemic rigor rather than accumulating false-positive circuit claims.

---

## 4. Grokking, Emergence & Phase Transitions

### 4.1 Are Emergent Abilities of Large Language Models a Mirage?
- **Authors:** Rylan Schaeffer, Brando Miranda, Sanmi Koyejo
- **Venue:** NeurIPS 2023
- **Year:** 2023
- **Why it matters:** Provoked a major debate by arguing that many emergent abilities are metric artifacts: sharp transitions appear only because nonlinear metrics (e.g., accuracy) are plotted against model scale, while the underlying loss improves smoothly. This paper forced the field to re-examine the empirical basis of the emergence narrative and led to a wave of follow-up work clarifying which abilities are genuinely unpredictable vs. merely poorly visualized. A trunk paper for the science of LLM capabilities.

### 4.2 Grokking as the Transition from Lazy to Rich Training Dynamics
- **Authors:** Tanishq Kumar, Blake Bordelon, Samuel J. Gershman, Cengiz Pehlevan
- **Venue:** arXiv, 2023
- **Year:** 2023
- **Why it matters:** Unifies the mysterious grokking phenomenon (sudden generalization after prolonged overfitting) with the lazy-to-rich training dichotomy. Shows that grokking is not a strange anomaly but a natural consequence of the model transitioning from a kernel regime to a feature-learning regime. This reframes grokking as a window into the fundamental dynamics of representation learning, making it a tool rather than a curiosity.

### 4.3 Grokked Transformers Are Implicit Reasoners: A Mechanistic Journey to the Edge of Generalization
- **Authors:** Neel Nanda et al. (interpretability community)
- **Venue:** NeurIPS 2024
- **Year:** 2024
- **Why it matters:** Combines grokking analysis with mechanistic interpretability to show that transformers trained on algorithmic tasks develop implicit reasoning circuits during the grokking phase. It provides a detailed mechanistic account of how circuits form and consolidate, linking the training dynamics (grokking) to the emergence of internal algorithms. Essential for understanding how reasoning capabilities may spontaneously crystallize during LLM training.

### 4.4 Progress Measures for Grokking via Mechanistic Interpretability
- **Authors:** Neel Nanda, Lawrence Chan, Tom Lieberum, Jacob Steinhardt
- **Venue:** ICLR 2023
- **Year:** 2023
- **Why it matters:** Introduced the use of mechanistic interpretability tools to track grokking in real time, showing that specific circuits can be monitored as they form during training. It established a methodology for using internal representations as early-warning signals for generalization, providing a principled alternative to merely waiting for test-loss drops. This approach is now standard in grokking and dynamics research.

---

## 5. Reasoning, Chain-of-Thought & Test-Time Compute

### 5.1 Towards Revealing the Mystery behind Chain of Thought: A Theoretical Perspective
- **Authors:** Yao Fu, Hao Peng, Ashish Sabharwal, Peter Clark, Tushar Khot
- **Venue:** NeurIPS 2023
- **Year:** 2023
- **Why it matters:** One of the first rigorous theoretical analyses of why Chain-of-Thought (CoT) prompting improves reasoning. It frames CoT as a way to enlarge the effective model capacity by decomposing a hard problem into a multi-step computation, and provides formal bounds showing that CoT can solve problems that direct prompting cannot. This established the theoretical basis for CoT as a computational primitive rather than merely a prompting trick.

### 5.2 Coconut: Continuous Latent Reasoning in Language Models
- **Authors:** Shibo Hao, Sainbayar Sukhbaatar, et al.
- **Venue:** ICLR 2025
- **Year:** 2025
- **Why it matters:** Introduces the paradigm of continuous latent-space reasoning, where the model reasons in hidden states rather than discrete tokens. This is a fundamental departure from explicit CoT and opens a new research direction on inference-time scaling in the latent space. It challenges the assumption that reasoning must be verbalized and suggests that the best reasoning may be inherently non-linguistic.

### 5.3 Reasoning by Superposition
- **Authors:** Zhu et al.
- **Venue:** NeurIPS 2025
- **Year:** 2025
- **Why it matters:** Proposes that transformers can perform reasoning via superposition of multiple concepts in the same latent space, enabling parallel rather than sequential reasoning. This connects the theory of superposition (from Toy Models of Superposition) to the practice of reasoning, suggesting that models exploit high-dimensional geometry to reason in ways that are not captured by chain-of-thought traces. It opens a new theoretical angle on how multi-hop reasoning may occur in parallel.

### 5.4 DeepSeek-R1: Incentivizing Reasoning Capability via Reinforcement Learning
- **Authors:** DeepSeek-AI
- **Venue:** arXiv, 2025
- **Year:** 2025
- **Why it matters:** While primarily an engineering report, the R1 paper is a theoretical milestone because it demonstrated that complex reasoning (long CoT, self-verification, backtracking) can emerge from pure RL without supervised fine-tuning on reasoning traces. This challenges the prevailing paradigm that reasoning must be taught through imitation learning and suggests that reasoning is an intrinsic capability that can be elicited through appropriate reward shaping. It reopens the debate about the nature of LLM reasoning (learned vs. innate).

---

## 6. Model Merging & Loss Landscape Geometry

### 6.1 Git Re-Basin: Merging Models modulo Permutation Symmetries
- **Authors:** Samuel Ainsworth, Jonathan Hayase, Siddhartha Srinivasa
- **Venue:** ICLR 2023
- **Year:** 2023
- **Why it matters:** Discovered that independently trained neural networks can be merged into a single model with almost no loss barrier if weights are permuted to align the symmetries of the networks. This is a foundational result for the model-merging subfield, showing that the loss landscape is not a single basin but a vast connected manifold under permutation symmetry. It underpins essentially all subsequent work on model soups, task arithmetic, and federated learning with merged models.

### 6.2 Mechanistic Mode Connectivity
- **Authors:** Ekdeep Singh Lubana, Eric J. Bigelow, Robert P. Dick, David Scott Krueger, Hidenori Tanaka
- **Venue:** ICML 2023
- **Year:** 2023
- **Why it matters:** Connects the geometric concept of mode connectivity (linear paths between minima) to mechanistic interpretability, showing that models connected by low-loss paths share similar internal circuits. This bridges two previously disconnected fields, loss-landscape geometry and circuit analysis, and suggests that model merging preserves not just performance but also internal computation. A trunk paper for understanding why model merging works.

### 6.3 Understanding Mode Connectivity via Parameter Space Symmetry
- **Authors:** Bo Zhao, Nima Dehmamy, Robin Walters, Rose Yu
- **Venue:** ICML 2025
- **Year:** 2025
- **Why it matters:** Provides a clean theoretical framework linking mode connectivity to the symmetry group of the parameter space (permutations, rotations, and scaling symmetries). It shows that the number of distinct minima modulo symmetry is much smaller than the apparent number of disconnected minima, explaining the empirical success of re-basin methods. This is the most principled mathematical treatment of the re-basin/merging phenomenon to date.

### 6.4 ZipIt! Merging Models from Different Tasks without Training
- **Authors:** George Stoica, Daniel Bolya, Jakob Bjorner, Taylor Hearn, Judy Hoffman
- **Venue:** ICLR 2024
- **Year:** 2024
- **Why it matters:** Extends model merging from the same-task, different initialization setting to the much harder different-task setting. By identifying which features are shared vs. task-specific and zipping them together, the method merges models trained on completely different tasks with minimal performance degradation. This dramatically expands the applicability of model merging and is a key step toward modular, composable AI systems.

---

## 7. Learning Theory, Generalization & Optimization

### 7.1 Deep Learning is Not So Mysterious or Different
- **Authors:** Andrew Gordon Wilson
- **Venue:** ICML 2025
- **Year:** 2025
- **Why it matters:** A position/theory paper arguing that deep learning generalization can be understood through classical statistical lenses: implicit regularization, neural tangent kernels, and PAC-Bayes, without invoking mysterious new physics. It provides a unifying framework that reconciles the deep learning is alien narrative with classical learning theory, and serves as a key reference point for debates about whether new scientific paradigms are needed to understand neural networks.

### 7.2 Generalization at the Edge of Stability
- **Authors:** Mario Tuci, Caner Korkmaz, Umut Simsekli, Tolga Birdal
- **Venue:** arXiv, 2026
- **Year:** 2026
- **Why it matters:** Analyzes the Edge of Stability (EoS) phenomenon, where large learning rates produce non-monotonic loss curves yet still generalize well, through the lens of stability and implicit regularization. It provides the first rigorous generalization bounds under EoS conditions, showing that the sharpness-aware minimization implicit in EoS training acts as a strong regularizer. This resolves a major puzzle in optimization theory and explains why practitioners can use learning rates far above the classical stability threshold.

### 7.3 There Will Be a Scientific Theory of Deep Learning
- **Authors:** (Multiple authors; emerging consensus paper)
- **Venue:** arXiv, 2026
- **Year:** 2026
- **Why it matters:** Makes the case that a mechanics of learning is emerging, analogous to the mechanics of physical systems. It articulates seven desiderata for a scientific theory of deep learning (useful, predictive, comprehensive, intuitive, humble, etc.) and surveys the converging evidence from scaling laws, feature-learning theory, and optimization dynamics. This paper is a milestone for the metascience of deep learning, attempting to coordinate theoretical effort around a shared vision rather than fragmented subfields.

### 7.4 The Features at Convergence Theorem: A First-Principles Alternative to the Neural Feature Ansatz
- **Authors:** Eitan Boix-Adsera, Neil Mallinar, J. Braxton Simon, Mikhail Belkin
- **Venue:** arXiv, 2025
- **Year:** 2025
- **Why it matters:** Proposes a rigorous first-principles theorem for how networks learn features at convergence, replacing the heuristic neural feature ansatz with a provable characterization. It shows that the learned features at convergence are determined by the spectral decomposition of a certain data-dependent operator, yielding explicit formulas for feature quality. This is a major step toward making feature-learning theory as precise as NTK theory.

### 7.5 Beyond Lipschitz: Sharp Generalization and Excess Risk Bounds for Full-Batch GD
- **Authors:** Konstantinos E. Nikolakakis, Farzin Haddadpour, Amin Karbasi, Dionysios S. Kalogerias
- **Venue:** ICLR 2023
- **Year:** 2023
- **Why it matters:** Provides sharp generalization bounds for full-batch gradient descent that go beyond the standard Lipschitz/smoothness assumptions, capturing the benign behavior of GD in overparameterized settings. It shows that the excess risk can be much smaller than classical bounds predict, explaining the empirical observation that full-batch GD often generalizes as well as SGD despite lacking the implicit regularization of noise. A key paper for reconciling optimization theory with practice.

---

## 8. AI Alignment, Safety & Formal Methods

### 8.1 Representation Engineering: A Top-Down Approach to AI Transparency
- **Authors:** Andy Zou, Long Phan, Sarah Chen, et al.
- **Venue:** NeurIPS 2023 (Representation Engineering / MI for Safety)
- **Year:** 2023
- **Why it matters:** Introduces Representation Engineering (RepE), a paradigm for AI safety and control that operates on the model's internal representations rather than on inputs or outputs. By extracting and modifying direction vectors in activation space (e.g., an honesty vector), RepE enables post-hoc behavioral control without retraining. It became the foundation for a major strand of safety research and is a practical complement to RLHF for alignment.

### 8.2 Refusal in Language Models is Mediated by a Single Direction
- **Authors:** Arditi, Obeso, Syed, Paleka, Panickssery, Gurnee, Nanda
- **Venue:** NeurIPS 2024
- **Year:** 2024
- **Why it matters:** A striking interpretability-for-safety result showing that a model's refusal behavior (a key safety mechanism) is controlled by a single linear direction in representation space. This demonstrates that safety-critical behaviors can be surprisingly low-dimensional and raises important questions about the robustness of safety training: if refusal is a one-dimensional knob, it can potentially be easily disabled by adversaries. It is a trunk paper for the intersection of MI and safety.

### 8.3 SMLE: Safe Machine Learning via Embedded Overapproximation
- **Authors:** Matteo Francobaldi, Michele Lombardi
- **Venue:** AAAI 2025
- **Year:** 2025
- **Why it matters:** A rare example of formal-methods-meets-ML safety that scales to practical deep networks. It embeds overapproximation-based verification into the training loop, producing models that come with provable input-output safety guarantees. This is a milestone for the field of certified ML, moving from post-hoc verification to training-time certification, and is essential for safety-critical applications where empirical robustness is insufficient.

### 8.4 Formal Methods for Safety-Critical Machine Learning: A Systematic Literature Review
- **Authors:** A. Newcomb et al.
- **Venue:** Frontiers in Artificial Intelligence, 2026
- **Year:** 2026
- **Why it matters:** The most comprehensive synthesis of formal methods applied to ML safety as of 2026. It surveys reachability analysis, SMT-based verification, model checking, runtime verification, and shielding techniques, identifying which techniques scale and which remain theoretical. This paper serves as the definitive reference for anyone attempting to bridge formal verification and ML, and it maps the frontier of certifiable AI.

---

## Honorable Mentions (Highly Influential but Slightly Outside Core Theory)

- **Inference-Time Intervention: Eliciting Truthful Answers from a Language Model** (Li et al., NeurIPS 2023) – Elicits truthfulness by shifting activations at inference time, bridging MI and honesty.
- **The Internal State of an LLM Knows When It is Lying** (Azaria & Mitchell, EMNLP 2023) – Shows that hallucination can be detected from internal representations, a foundational result for truthfulness monitoring.
- **Disentangling Memory and Reasoning Ability in Large Language Models** (ACL 2025) – Shows that memory and reasoning are separable capabilities, with major implications for evaluation and architecture design.
- **Understanding Emergent Abilities of Language Models from the Loss Perspective** (Du et al., 2024) – Complements the Schaeffer mirage paper by showing which abilities genuinely emerge from loss curves.
- **The Platonic Representation Hypothesis** (Huh et al., ICML 2024) – Proposes that representations across different models converge to a shared Platonic ideal, sparking debates about universality in representation learning.
- **Muon: An Optimizer for Hidden Layers in Neural Networks** (Jordan et al., 2024) – Introduces a theoretically motivated optimizer for hidden layers that uses orthogonalization, showing strong empirical gains and theoretical properties.
- **Birth of a Transformer: A Memory Viewpoint** (Bietti et al., NeurIPS 2023) – Analyzes how transformers learn associative memory and induction heads through a memory-theoretic lens, connecting to Hopfield networks.
- **Opening the AI Black Box: Program Synthesis via Mechanistic Interpretability** (Michaud et al., 2024) – Uses MI to extract human-readable programs from trained networks, showing that reverse-engineering can produce verifiable algorithms.
- **Label Words are Anchors: An Information Flow Perspective for Understanding In-Context Learning** (EMNLP 2023) – Traces the information flow in ICL, showing that label words act as anchors for task recognition.
- **The Geometry of Truth: Emergent Linear Structure in LLM Representations of True/False Datasets** (2023) – Shows that truth and falsehood are organized along a linear axis in representation space, foundational for truthfulness research.

---

> **Curated:** 2026-07-15
> **Scope:** Papers from 2023 to July 2026 that are foundational, widely cited, open new directions, or settle major debates in AI Theory.
> **Methodology:** Synthesis from NeurIPS, ICML, ICLR, ACL, EMNLP, AAAI, PNAS, JMLR, and key arXiv preprints; cross-referenced across multiple survey and paper-list repositories.
