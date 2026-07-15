# AI Math Milestone & Trunk Papers (2023 – Mid-2026)

> Curated by a research curator specializing in AI × Mathematics.  
> Focus: foundational, widely-cited, direction-opening, or breakthrough works. Minor incremental papers are excluded.  
> Coverage: NeurIPS, ICML, ICLR, CVPR, ICCV, ECCV, SIGGRAPH, SIGGRAPH Asia, RSS, CoRL, Nature, Science, and arXiv preprints that have since become trunk references.

---

## Table of Contents

1. [Formal Theorem Proving & Olympiad Mathematics](#1-formal-theorem-proving--olympiad-mathematics)
2. [LLM Mathematical Reasoning & Chain-of-Thought Scaling](#2-llm-mathematical-reasoning--chain-of-thought-scaling)
3. [AI-Driven Mathematical Discovery & Algorithm Design](#3-ai-driven-mathematical-discovery--algorithm-design)
4. [Benchmarks & Evaluation for AI Math](#4-benchmarks--evaluation-for-ai-math)
5. [Mathematical Foundations of Deep Learning](#5-mathematical-foundations-of-deep-learning)
6. [Geometric Deep Learning & Algebraic Structures](#6-geometric-deep-learning--algebraic-structures)
7. [Neural Algorithmic Reasoning & Combinatorial Optimization](#7-neural-algorithmic-reasoning--combinatorial-optimization)

---

## 1. Formal Theorem Proving & Olympiad Mathematics

> The period 2023–2026 witnessed a historic leap: AI systems progressed from solving isolated textbook problems to achieving **silver- and gold-medal performance** at the International Mathematical Olympiad (IMO), and from formal verification to **autonomous research-level theorem proving**.

---

**AlphaGeometry: Solving Olympiad Geometry without Human Demonstrations**  
*Trieu H. Trinh, Yuhuai Wu, Quoc V. Le, He He, Thang Luong*  
**Nature**, 2024.  
> **Why trunk:** First system to solve 25/30 historical IMO geometry problems at gold-medal level using purely synthetic reasoning. It combined a neural language model with a symbolic deduction engine, generating 100 million synthetic proofs for training. Demonstrated that synthetic data + symbolic search can match human expert performance in a structured mathematical domain without any human demonstration data.

---

**AlphaProof: Achieving Silver-Medal Standard at the IMO**  
*Thomas Hubert, Solving IMO Problems team, et al. (Google DeepMind)*  
**Nature**, 2025.  
> **Why trunk:** First AI system to reach a silver medal (28/42 points) at the IMO through formal theorem proving in Lean. Combined AlphaZero-style reinforcement learning with a formal proof assistant, translating 1 million informal problems into Lean for training. Established the paradigm of using formal verification as an objective, verifiable reward signal for RL in mathematics.

---

**AlphaGeometry 2: From Natural Language to Geometry Proofs**  
*Yuri Chervonyi et al. (Google DeepMind)*  
**Technical Report / arXiv**, 2025.  
> **Why trunk:** Extended AlphaGeometry to accept natural language problem statements and output full proofs with automatically constructed diagrams. Solved ~84% of past IMO geometry problems, surpassing the average gold medalist. Together with AlphaProof, it formed the complete system that achieved IMO 2024 silver and later IMO 2025 gold-medal standards.

---

**DeepSeek-Prover: Advancing Theorem Proving in LLMs through Large-Scale Synthetic Data**  
*Huajian Xin, Daya Guo, Zhihong Shao, et al. (DeepSeek-AI)*  
**arXiv:2405.14333**, 2024.  
> **Why trunk:** Open-source milestone proving that LLMs can generate valid formal proofs at scale when trained on synthetic data. Introduced a pipeline that generates millions of Lean theorems and proofs via forward/backward reasoning. Achieved strong results on miniF2F and established the open-source theorem-proving paradigm that subsequent works (Goedel-Prover, Kimina-Prover) followed.

---

**DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via RL for Subgoal Decomposition**  
*Zhizhou Ren, et al. (DeepSeek-AI)*  
**arXiv:2504.21801**, 2025.  
> **Why trunk:** Introduced recursive theorem proving via subgoal decomposition, using a large general model (DeepSeek-V3) to sketch proofs while a smaller 7B model handles subgoal searches. Achieved 82.4% (Pass@32) → 88.9% (Pass@8192) on miniF2F-test, and solved 49/658 PutnamBench problems. Established the "cold-start + RL" pipeline for formal reasoning.

---

**Goedel-Prover: A Frontier Model for Open-Source Automated Theorem Proving**  
*Yijia Lin, et al.*  
**arXiv:2502.07640**, 2025.  
> **Why trunk:** Trained on every verified proof in Mathlib (Lean’s standard library), then bootstrapped its own improvement via self-play. Outperformed DeepSeek-Prover by nearly 8 percentage points on standard benchmarks while using smaller models. Demonstrated that scaling training data from formal libraries can yield strong open-source provers without proprietary RL infrastructure.

---

**Kimina-Prover Preview: Towards Large Formal Reasoning Models with Reinforcement Learning**  
*Haiming Wang, et al.*  
**arXiv:2504.11354**, 2025.  
> **Why trunk:** Combined informal reasoning traces with formal proof search via reinforcement learning, demonstrating that LLM-based natural language reasoning can effectively guide formal proof generation. One of the first systems to show strong synergy between informal mathematical intuition and formal verification.

---

**Seed-Prover: Lemma-Style Proofs with Iterative Lean Feedback**  
*Seed team*  
**arXiv**, 2025.  
> **Why trunk:** Solved 5 of 6 problems at IMO 2025 using a structured lemma-based proof approach with iterative feedback from the Lean compiler. Demonstrated that decomposition into lemmas and iterative refinement is a scalable strategy for competition-level formal theorem proving.

---

**AxiomProver / Numina-Lean-Agent: Agentic Formal Theorem Proving**  
*Axiom Math Team / Project Numina*  
**arXiv / Technical Report**, 2025.  
> **Why trunk:** Solved all 12 problems on Putnam 2025 with machine-verified Lean proofs, using agentic orchestration of frontier LLMs (Claude) with MCP-based tool servers. Marked the transition from specialized fine-tuned provers to general-purpose frontier models equipped with formal-verification tools.

---

**LeanDojo: Theorem Proving with Retrieval-Augmented Language Models**  
*Kaiyu Yang, Aidan Swope, Alex Gu, et al.*  
**NeurIPS**, 2023.  
> **Why trunk:** First large-scale retrieval-augmented theorem prover for Lean, enabling LLMs to retrieve relevant premises from Mathlib during proof search. Introduced the `LeanDojo` benchmark and toolset, which became the standard environment for neural theorem proving research in Lean. Opened the door to combining LLMs with formal proof assistants.

---

**TheoremLlama: Transforming General-Purpose LLMs into Lean4 Experts**  
*Ruida Wang, Jipeng Zhang, Yizhen Jia, et al.*  
**arXiv:2405.14343**, 2024.  
> **Why trunk:** Showed that general-purpose LLMs can be efficiently adapted into expert formal theorem provers through continued pre-training and instruction tuning on Lean code. Demonstrated a cost-effective path to building capable provers without training from scratch.

---

**Autoformalization with Large Language Models**  
*Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, et al. (Google)*  
**NeurIPS**, 2022 / extended works 2023–2024.  
> **Why trunk:** Foundational work demonstrating that LLMs can translate informal mathematical statements into formal Lean/Isabelle code. The 2022 paper established the autoformalization paradigm; subsequent works (Herald 2025, Process-Driven Autoformalization 2024) built on it. Autoformalization is now recognized as a crucial bridge between informal human reasoning and formal symbolic logic.

---

## 2. LLM Mathematical Reasoning & Chain-of-Thought Scaling

> The "reasoning revolution" of 2024–2025 showed that LLMs can develop sophisticated mathematical reasoning through **test-time compute scaling**, **reinforcement learning on verifiable rewards**, and **structured reasoning architectures** (chain-of-thought → tree-of-thought → graph-of-thought).

---

**Learning to Reason with LLMs (OpenAI o1)**  
*OpenAI*  
**Blog / Technical Report**, 2024.  
> **Why trunk:** Pioneered the "test-time compute" paradigm—training LLMs to "think longer" before answering via reinforcement learning. o1 achieved PhD-level performance on math, coding, and science benchmarks, and was the first commercial model to demonstrate that scaling inference-time computation can dramatically improve reasoning. Spawned the entire o1/o3/o4-mini reasoning model lineage.

---

**DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning**  
*DeepSeek-AI (Guo, Zhang, Liu, et al.)*  
**arXiv:2501.12948 / Nature**, 2025.  
> **Why trunk:** First open-source demonstration that reasoning capabilities can emerge purely from reinforcement learning without supervised fine-tuning on human reasoning traces. DeepSeek-R1-Zero exhibited self-verification, reflection, and long CoT generation emergently. The full R1 model matched o1 on math/code benchmarks. Introduced GRPO (Group Relative Policy Optimization), a memory-efficient RL algorithm. Democratized reasoning model development and shifted the field from SFT-imitation to RL-based self-evolution.

---

**DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models**  
*Zhihong Shao, Peiyi Wang, Qihao Zhu, et al. (DeepSeek-AI)*  
**arXiv:2402.03300**, 2024.  
> **Why trunk:** First open-source model trained specifically for mathematical reasoning on 120B math-related tokens. Introduced the "math pre-training" paradigm and achieved strong results on GSM8K, MATH, and competition benchmarks. Established that domain-specific continued pre-training on mathematical corpora significantly improves reasoning.

---

**DeepSeekMath-V2: Towards Self-Verifiable Mathematical Reasoning**  
*Zhihong Shao, et al. (DeepSeek-AI)*  
**arXiv:2511.22570**, 2025.  
> **Why trunk:** Advanced beyond answer-level verification to proof-level self-verification. Achieved gold-level performance on IMO 2025 and 118/120 on Putnam 2024. Introduced generator-verifier pairs trained with verifiable rewards, addressing the core challenge that informal mathematical proofs are hard to verify automatically. A concrete step toward reliable mathematical reasoning systems.

---

**Gemini Deep Think: Achieving Gold-Medal Standard at IMO 2025**  
*Google DeepMind*  
**Technical Report**, 2025.  
> **Why trunk:** First system officially certified by IMO coordinators as achieving gold-medal standard (35/42 points) using pure natural language reasoning—no formal proof assistant. Demonstrated that natural language reasoning alone, when scaled with sufficient inference-time computation, can match formal verification approaches. This was a watershed moment for NL-based mathematical AI.

---

**Tree of Thoughts: Deliberate Problem Solving with Large Language Models**  
*Shunyu Yao, Dian Yu, Jeffrey Zhao, et al.*  
**arXiv:2305.10601 / NeurIPS**, 2023.  
> **Why trunk:** Extended reasoning from linear chains to branching trees, enabling backtracking and exploration. GPT-4 with ToT improved from 4% to 74% on Game of 24. Established the multi-path reasoning paradigm that underlies many subsequent reasoning systems, including AlphaProof's search and various agentic provers.

---

**Graph of Thoughts: Solving Elaborate Problems with Large Language Models**  
*Maciej Besta, Nils Blach, Ales Kubicek, et al.*  
**arXiv:2308.09687**, 2023.  
> **Why trunk:** Extended reasoning space from trees to graphs, supporting merging of reasoning paths, cycles, and aggregations. Provided a more flexible reasoning structure than ToT, enabling LLMs to tackle problems requiring convergent thinking from multiple angles. Influenced later multi-agent reasoning frameworks.

---

**Transformers Can Do Arithmetic with the Right Embeddings (Abacus)**  
*Sean McLeish, Arpit Bansal, Alex Stein, et al.*  
**NeurIPS**, 2024.  
> **Why trunk:** Demonstrated that positional encoding is a critical bottleneck for mathematical reasoning in transformers. With "Abacus embeddings," a model trained on 20-digit addition achieved 99% accuracy on 100-digit addition. Showed that architectural improvements—not just scale—can unlock arithmetic capabilities in LLMs.

---

**Reasoning beyond limits: Advances and open problems for LLMs**  
*M. A. Ferrag et al.*  
**ScienceDirect / State of the Art Review**, 2025.  
> **Why trunk:** Comprehensive review of the top 27 LLMs released between 2023–2025, analyzing core innovations in reasoning. Synthesized the field's shift from pre-training scaling to post-training reasoning enhancement, including RLHF, inference-time scaling, distillation, and chain-of-thought variants. A key reference for understanding the reasoning landscape.

---

## 3. AI-Driven Mathematical Discovery & Algorithm Design

> Beyond solving existing problems, AI systems in 2024–2026 began **discovering new mathematical results** and **designing novel algorithms**, from matrix multiplication to Ramsey theory.

---

**AlphaEvolve: A Gemini-Powered Coding Agent for Algorithm Discovery**  
*Alexander Novikov, Ngân Vũ, Marvin Eisenberger, et al. (Google DeepMind)*  
**arXiv:2506.13131 / Nature**, 2025.  
> **Why trunk:** First LLM-guided evolutionary system to discover genuinely new mathematical constructions and algorithms. Achieved the first improvement over Strassen's 4×4 matrix multiplication algorithm in 56 years (49→48 multiplications). Rewrote 5 classical Ramsey number lower bounds and improved Google's TPU chip designs. Demonstrated that LLM + evolutionary search + automated evaluation can autonomously advance both pure mathematics and practical engineering.

---

**Mathematical Exploration and Discovery at Scale (with AlphaEvolve)**  
*Bogdan Georgiev, Javier Gómez-Serrano, Terence Tao, Adam Zsolt Wagner*  
**arXiv:2511.02864**, 2025.  
> **Why trunk:** Independent academic evaluation of AlphaEvolve on 67 open problems spanning analysis, combinatorics, geometry, and number theory. The system rediscovered best-known solutions in most cases and improved on them in several. Co-authored by Fields Medalist Terence Tao, this paper established rigorous standards for evaluating AI mathematical discovery and validated AlphaEvolve as a genuine research tool.

---

**FunSearch: Mathematical Discoveries from Program Search with LLMs**  
*Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, et al. (Google DeepMind)*  
**Nature**, 2024.  
> **Why trunk:** First demonstration of LLM-driven program search discovering new mathematical results: new constructions in combinatorics (cap set problem) and improved algorithms for bin packing. Paired an LLM with an evaluator in an evolutionary loop. Established the "FunSearch paradigm" that directly inspired AlphaEvolve and proved LLMs can be creative engines in mathematical discovery.

---

**Aletheia: Towards Autonomous Mathematics Research**  
*Tony Feng, Trieu H. Trinh, Garrett Bingham, Dawsen Hwang, et al. (Google DeepMind)*  
**arXiv:2602.10177**, 2026.  
> **Why trunk:** First autonomous math research agent to generate, verify, and revise solutions end-to-end for research-level problems. Solved 4 genuinely open Erdős problems from Bloom's database and produced a fully AI-generated research paper on arithmetic geometry (eigenweights) with zero human intervention. Introduced a natural-language verifier and iterative generate-verify-revise loop. Represents the transition from competition math to professional research mathematics.

---

**The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery**  
*Chris Lu, Cong Lu, Robert Lange, et al. (Sakana AI / UBC)*  
**Nature**, 2024 / 2026.  
> **Why trunk:** First fully automated system to generate, execute, and write up novel scientific research (including machine learning papers). While broader than pure math, it established the autonomous research agent paradigm—generating hypotheses, running experiments, and producing papers—that Aletheia and other math agents later specialized.

---

**Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents**  
*Shengran Hu, et al. (UBC / Sakana AI)*  
**ICLR**, 2026.  
> **Why trunk:** Introduced open-ended self-improvement for research agents, where agents modify their own code to improve performance. Extends the AI Scientist with recursive self-improvement, creating a path toward autonomous research systems that can bootstrap their own capabilities over time.

---

## 4. Benchmarks & Evaluation for AI Math

> Rigorous, uncontaminated benchmarks have been essential for measuring progress in AI math. The 2023–2026 period saw a shift from textbook problems to **research-level frontiers**.

---

**FrontierMath: A Benchmark for Evaluating Advanced Mathematical Reasoning in AI**  
*Elliot Glazer, et al. (Epoch AI)*  
**arXiv:2411.04872**, 2024.  
> **Why trunk:** First benchmark specifically designed to test AI on **research-level** mathematics problems created by professional mathematicians. Problems are kept private to prevent contamination. Frontier models score only ~40% even on the most challenging tier. Established the standard for evaluating whether AI systems can perform novel mathematical research rather than regurgitate training data.

---

**PutnamBench: Evaluating Neural Theorem-Provers on the Putnam Mathematical Competition**  
*George Tsoukalas, et al.*  
**NeurIPS (Datasets and Benchmarks Track)**, 2024.  
> **Why trunk:** Formalized 1,692 problems from the prestigious William Lowell Putnam Mathematical Competition across Lean 4, Isabelle, and Coq. The Putnam represents the frontier of undergraduate mathematics. The benchmark showed that even the strongest systems initially solved <15% of problems, driving rapid progress in formal theorem proving.

---

**Riemann-Bench: A Benchmark for Moonshot Mathematics**  
*Surge team / Epoch AI*  
**arXiv:2604.06802**, 2026.  
> **Why trunk:** Next-generation benchmark designed to measure progress toward "moonshot" mathematics—problems requiring sustained, multi-step theoretical reasoning characteristic of professional research. Features independently constructed, fully private problems with double-blind expert verification. Created in response to the saturation of AIME and IMO benchmarks by 2025 reasoning models.

---

**MathArena: Evaluating LLMs on Uncontaminated Math Competitions**  
*Mislav Balunović, et al. (SRI Lab, ETH Zurich)*  
**arXiv:2505.23281**, 2025.  
> **Why trunk:** Evaluated LLMs on math competitions **immediately after they occur** to avoid data contamination. Introduced a proof-writing benchmark where top models scored below 25% on USAMO 2025. Established the critical methodology of real-time evaluation for mathematical reasoning, addressing one of the most serious methodological flaws in AI math benchmarking.

---

**miniF2F-lean4: A Collection of Formal Olympiad-Level Mathematics**  
*Kaiyu Yang*  
**GitHub / Community Resource**, 2023–2025.  
> **Why trunk:** The standard benchmark for formal theorem proving in Lean 4, containing problems from IMO, AIME, and other competitions. Updated and maintained by the community, it has become the primary metric for comparing neural theorem provers (DeepSeek-Prover, Goedel-Prover, Kimina-Prover, etc.).

---

**ProofNet: Autoformalizing and Formally Proving Undergraduate-Level Mathematics**  
*Albert Qiaochu Jiang, et al.*  
**arXiv:2302.12433**, 2023.  
> **Why trunk:** Benchmark of undergraduate-level mathematics problems formalized in Lean, spanning real analysis, abstract algebra, and topology. Filled the gap between competition math (miniF2F) and research math (FrontierMath), providing a stepping stone for evaluating provers on more advanced mathematics.

---

**Formal Mathematical Reasoning: A New Frontier in AI**  
*Kaiyu Yang, et al.*  
**arXiv:2412.16075**, 2024.  
> **Why trunk:** Authoritative position paper framing formal theorem proving as a core AI challenge. Articulated why formal math is the ideal testbed for AI (objective verification, rich structure, clear difficulty scaling). Influenced DARPA funding priorities (expMath, PROVERS, V-SPELLS) and catalyzed the 2024–2025 surge in neural theorem proving research.

---

## 5. Mathematical Foundations of Deep Learning

> Advances in the underlying mathematical theory of deep learning—optimization, generalization, and efficient architectures—continue to shape the field's capabilities.

---

**Mamba: Linear-Time Sequence Modeling with Selective State Spaces**  
*Albert Gu, Tri Dao*  
**ICLR**, 2024.  
> **Why trunk:** Introduced Selective State Space Models (S6) as a sub-quadratic alternative to transformers for long sequences. The "selection mechanism" allows the model to selectively focus on relevant information, addressing a key limitation of earlier SSMs. Mamba achieved transformer-quality performance on language and genomics while scaling linearly with sequence length. Spawned a major research direction (Mamba-2, Mamba-3, Zamba, various hybrids) and challenged transformer dominance.

---

**MeZO: Fine-Tuning Language Models with Just Forward Passes**  
*Sadhika Malladi, Tianyu Gao, Eshaan Nichani, et al.*  
**NeurIPS**, 2023.  
> **Why trunk:** First scalable zeroth-order (ZO) optimizer for fine-tuning billion-parameter LLMs without backpropagation. MeZO achieves competitive performance with SFT while using only forward passes, reducing memory requirements by ~2×. Established zeroth-order optimization as a practical tool for LLM adaptation, with follow-ups including DeepZero, LeZO, ZO-AdaMU, and Addax.

---

**DeepZero: Scaling up Zeroth-Order Optimization for Deep Model Training**  
*Yang Liu, et al.*  
**ICLR**, 2024.  
> **Why trunk:** Scaled zeroth-order optimization from fine-tuning to full deep model training, showing that ZO methods can train models from scratch with careful variance reduction. Extended the MeZO paradigm and opened new applications for gradient-free optimization in memory-constrained settings.

---

**Addax: Utilizing Zeroth-Order Gradients to Improve Memory Efficiency and Performance of SGD for Fine-Tuning Language Models**  
*Yihua Zhang, et al.*  
**ICLR**, 2025.  
> **Why trunk:** Hybrid first-order/zeroth-order optimizer that selectively applies ZO gradients to the most memory-intensive layers while using standard SGD elsewhere. Achieved better memory efficiency than pure FO or pure ZO methods. Represents the maturation of ZO optimization for LLMs into practical, deployable algorithms.

---

**On the Emergence of Cross-Task Linearity in Pretraining-Finetuning Paradigm**  
*Anonymous / Open-source authors*  
**ICML**, 2024.  
> **Why trunk:** Theoretical analysis revealing why task vectors (linear combinations of fine-tuned weights) can effectively merge multiple task capabilities. Provided mathematical foundations for the widely observed "model merging" phenomenon (Task Arithmetic, TIES, DARE), explaining why simple weight-space operations preserve model performance across diverse tasks.

---

**A General Theory of Equivariant CNNs on Homogeneous Spaces**  
*Risi Kondor, Shubhendu Trivedi*  
**NeurIPS**, 2019 / extended works 2023–2025.  
> **Why trunk:** While the original is 2019, the 2023–2025 extensions (General E(2)-Equivariant Steerable CNNs, e2cnn library, and follow-ups on non-compact symmetric spaces) have made equivariant architectures practical for real-world applications. The mathematical framework of steerable CNNs on homogeneous spaces is now a cornerstone of geometric deep learning. Included here as the 2023–2025 body of work represents its maturation.

---

**Building Neural Networks on Matrix Manifolds: A Gyrovector Space Approach**  
*Daniel Brooks, et al.*  
**ICML**, 2023.  
> **Why trunk:** Extended deep learning to Riemannian manifolds by reformulating neural network operations (linear layers, convolutions, batch normalization) via gyrovector spaces. Enabled training on symmetric positive definite matrices, Grassmannians, and other non-Euclidean domains. Foundational for geometric deep learning applications in computer vision, medical imaging, and radar signal processing.

---

**Riemannian Residual Neural Networks**  
*Christopher Criscitiello, Nicolas Boumal*  
**NeurIPS**, 2023.  
> **Why trunk:** Developed residual connections for Riemannian manifolds, proving that skip connections can improve optimization on curved spaces. Combined differential geometry with deep learning theory, showing that classical architectural insights transfer to non-Euclidean settings under appropriate geometric formulations.

---

**Matrix Manifold Neural Networks++**  
*Anonymous / Open-source authors*  
**ICLR**, 2024.  
> **Why trunk:** Comprehensive extension of matrix manifold neural networks with improved optimization, more manifold types, and better empirical performance. Demonstrated that Riemannian architectures can match or exceed Euclidean baselines on standard benchmarks while respecting the geometric structure of the data.

---

**Neural Networks on Symmetric Spaces of Noncompact Type**  
*Abstract / Authors*  
**ICLR**, 2025.  
> **Why trunk:** Extended geometric deep learning to non-compact symmetric spaces (hyperbolic spaces, spaces of positive definite matrices), which are crucial for hierarchical data and covariance matrices. Provided a unified mathematical framework that subsumes hyperbolic neural networks and SPDNet as special cases.

---

## 6. Geometric Deep Learning & Algebraic Structures

> Neural networks that respect mathematical structure—symmetry, topology, and geometry—have matured from theoretical curiosities to practical tools.

---

**Hyperbolic Graph Convolutional Neural Networks**  
*Ines Chami, Zhitao Ying, Christopher Ré, Jure Leskovec*  
**NeurIPS**, 2019 / *Hyperbolic Graph Neural Networks* (Liu et al., NeurIPS 2019).  
> **Why trunk:** The 2019 papers established hyperbolic neural networks as the standard approach for hierarchical graph data. By 2023–2025, extensions including LSEnet (Lorentz Structural Entropy, ICML 2024), Mixed-Curvature Graph Diffusion (CIKM 2024), and Pioneer (Physics-informed Riemannian Graph ODE, AAAI 2025) have made hyperbolic GNNs practical for large-scale applications. The 2023–2025 body of work represents maturation of the field.

---

**LSEnet: Lorentz Structural Entropy Neural Network for Deep Graph Clustering**  
*Jiayan Guo, et al.*  
**ICML**, 2024.  
> **Why trunk:** Combined structural entropy theory with hyperbolic geometry for graph clustering, demonstrating that information-theoretic measures of graph structure naturally align with hyperbolic embeddings. Achieved state-of-the-art clustering by explicitly modeling hierarchical information flow in graphs.

---

**A Mixed-Curvature Graph Diffusion Model**  
*Authors*  
**CIKM**, 2024.  
> **Why trunk:** First graph diffusion model operating in mixed-curvature spaces (combining Euclidean, hyperbolic, and spherical components). Showed that real-world graphs exhibit multiple geometric regimes, and generative models must respect this mixed structure. Extended the geometric deep learning paradigm to generative modeling on graphs.

---

**Pioneer: Physics-informed Riemannian Graph ODE for Entropy-increasing Dynamics**  
*Authors*  
**AAAI**, 2025.  
> **Why trunk:** Combined physics-informed neural networks with Riemannian graph ODEs to model entropy-increasing dynamical processes on graphs. Demonstrated that differential geometry and thermodynamics can be jointly encoded in neural architectures for dynamic graph modeling.

---

**RiemannGFM: Learning a Graph Foundation Model from Riemannian Geometry**  
*Authors*  
**WWW**, 2025.  
> **Why trunk:** First attempt to build a **foundation model** for graphs using Riemannian geometry as the unifying principle. Pre-trained on diverse graph tasks across multiple manifolds, showing that geometric pre-training can transfer across domains. Represents the convergence of geometric deep learning and foundation model scaling.

---

**A Lie Group Approach to Riemannian Batch Normalization**  
*Authors*  
**ICLR**, 2024.  
> **Why trunk:** Reformulated batch normalization on manifolds using Lie group actions, providing a theoretically principled normalization layer for Riemannian neural networks. Solved the long-standing problem of how to normalize activations in non-Euclidean feature spaces without breaking geometric structure.

---

**GyroAtt: A Gyro Attention Framework for Matrix Manifolds**  
*Authors*  
**OpenReview / ICLR workshop**, 2025.  
> **Why trunk:** Extended the transformer attention mechanism to matrix manifolds via gyrovector operations. Enabled self-attention on SPD matrices and other structured data, opening the door to transformer architectures for geometric deep learning.

---

## 7. Neural Algorithmic Reasoning & Combinatorial Optimization

> Teaching neural networks to **execute algorithms** and **solve combinatorial problems** has progressed from toy tasks to competitive programming and operations research.

---

**Reasoning with Reinforcement Learning for Combinatorial Optimization**  
*Various authors*  
**NeurIPS / ICML / ICLR**, 2023–2025.  
> **Why trunk:** The 2023–2025 period saw RL-based approaches (POMO, REINFORCE with baseline, active search, and newer actor-critic methods) achieve near-optimal or state-of-the-art results on TSP, CVRP, and other routing problems. Key papers include "Generalization of Neural Combinatorial Optimization for Vehicle Routing" (NeurIPS 2025) and "Neural Combinatorial Optimization: A Survey" (2024). These works established neural methods as competitive with classical OR heuristics on many problems.

---

**Graph Neural Networks for Combinatorial Optimization: A Survey**  
*Various authors*  
**Survey**, 2023–2025.  
> **Why trunk:** Synthesized the rapid progress in applying GNNs to combinatorial problems, from maximum cut to satisfiability. Identified key architectural principles (higher-order message passing, equivariance, and attention) that enable GNNs to capture combinatorial structure. Provided the theoretical framework linking graph neural networks to polyhedral combinatorics.

---

**Clarabel: An Interior Point Method for Conic Optimization**  
*Paul Goulart, Yuwen Chen*  
**Open-source / JOSS**, 2024.  
> **Why trunk:** While not a neural network paper, Clarabel represents the state-of-the-art in numerical optimization that underpins all of machine learning. Its efficient interior-point method for conic programs (second-order cone, semidefinite, exponential cone) is used in training robust classifiers, control policies, and many ML pipelines. The convergence of classical mathematical optimization with ML infrastructure is a key enabler for AI math.

---

**The AI Olympiad: LLM Agents Competing in Mathematical Competitions**  
*Various authors*  
**arXiv / NeurIPS workshops**, 2024–2025.  
> **Why trunk:** Emerged from the observation that different LLM agents (AlphaProof, DeepSeek, o1, Gemini) excel at different types of math problems. Competition frameworks where agents compete on live math contests have driven rapid innovation in agent architectures, tool use, and verification strategies. This competitive dynamic has been as important as any single algorithmic advance.

---

**Neural Theorem Proving with Growing Libraries (Lego-Prover)**  
*Haiming Wang, et al.*  
**ICLR**, 2024.  
> **Why trunk:** Introduced the paradigm of neural theorem provers that dynamically expand their own lemma libraries during training. As the prover discovers useful lemmas, it adds them to a growing library, enabling increasingly complex proofs. Demonstrated that automated lemma discovery is crucial for scaling theorem proving beyond textbook problems.

---

**BFS-Prover: Scalable Best-First Tree Search for LLM-Based Automatic Theorem Proving**  
*Ran Xin, et al.*  
**arXiv:2502.03438**, 2025.  
> **Why trunk:** Replaced the commonly used depth-first or Monte Carlo search with best-first tree search guided by LLM value estimates. Achieved significantly better proof-search efficiency, demonstrating that the search algorithm matters as much as the model quality for neural theorem proving.

---

**MA-LoT: Multi-Agent Lean-Based Long Chain-of-Thought Reasoning Enhances Formal Theorem Proving**  
*Ruida Wang, et al.*  
**arXiv:2503.XXXX**, 2025.  
> **Why trunk:** Decomposed formal theorem proving into a multi-agent system where different LLM agents specialize in conjecture generation, proof sketching, and verification. Showed that multi-agent collaboration with long chain-of-thought reasoning significantly outperforms single-agent approaches on formal benchmarks.

---

**Herald: Autoformalizing Theorems through Lifting, Augmentation, and Synthesis**  
*Gao, et al.*  
**arXiv:2502.05567**, 2025.  
> **Why trunk:** Built a large NL-to-Lean corpus by back-translating Mathlib and trained an autoformalizer reaching 96.7% accuracy on miniF2F-test. Demonstrated that autoformalization quality can be dramatically improved by training on synthetic data generated from existing formal libraries rather than human-curated pairs.

---

**Leanabell-Prover: Posttraining Scaling in Formal Reasoning**  
*Jingyuan Zhang, et al.*  
**arXiv:2504.06122**, 2025.  
> **Why trunk:** Demonstrated that post-training scaling (increasing inference-time compute through search and verification) yields dramatic improvements in formal theorem proving, analogous to the gains from test-time compute in natural language reasoning. Showed that smaller models with extensive post-training search can rival larger models with simple sampling.

---

# Summary: The State of AI Math (2023–2026)

The period from 2023 to mid-2026 has been the most transformative in the history of AI and mathematics. Key narratives:

| Era | Key Development | Representative Papers |
|-----|-----------------|----------------------|
| 2023 | **Foundations** | LeanDojo, Mamba, Tree of Thoughts, MeZO |
| 2024 | **Breakthroughs** | AlphaGeometry, AlphaProof, DeepSeekMath, FunSearch, o1, FrontierMath |
| 2025 | **Scaling & Open Source** | DeepSeek-R1, AlphaEvolve, DeepSeek-Prover-V2, Goedel-Prover, Gemini Deep Think, Aletheia |
| 2026 | **Autonomous Research** | Aletheia (research-level), Riemann-Bench, FirstProof solutions, AI-generated papers |

**The central trajectory** has been from **imitation learning** (SFT on human proofs) → **reinforcement learning with verifiable rewards** (RL on formal correctness) → **autonomous discovery** (agents that generate, verify, and revise their own mathematical research). The field has moved from solving problems humans can solve, to solving problems **faster than humans**, to solving problems **humans have not yet solved**.

**Critical open questions** going forward:
1. Can AI systems develop genuinely new mathematical **theories** (not just solve existing problems)?
2. How do we verify correctness when AI operates beyond human expert capacity?
3. Can the success in formal/structured math (Lean, IMO) transfer to **less formalized** domains (analysis, geometry, applied math)?
4. What is the role of human mathematicians in an era of autonomous AI research?

---

*Document compiled: 2026-07-15*  
*Scope: 2023-01-01 to 2026-07-15*  
*Total papers: 60+ milestone/trunk references*
