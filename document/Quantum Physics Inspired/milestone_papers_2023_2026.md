# Quantum Physics Inspired AI — Milestone & Trunk Papers (2023–Mid-2026)

> **Curator's note:** This list covers the most impactful, foundational, and direction-opening papers at the intersection of quantum physics and AI from 2023 through July 2026. It includes both **quantum-enhanced machine learning** (quantum algorithms for AI) and **AI-enabled quantum computing** (AI methods for quantum physics / error correction), as these two directions have become deeply intertwined since 2024. Papers are selected for being widely cited, opening new sub-fields, or representing experimental breakthroughs. Incremental follow-ups are excluded.

---

## 1. AI for Quantum Error Correction — The Decoding Revolution

The most consequential convergence of AI and quantum physics in 2023–2026 has been the application of deep learning to **quantum error correction (QEC) decoding**. Real-time decoding is the bottleneck for fault-tolerant quantum computing, and neural-network decoders have recently outperformed decades-old classical algorithms.

### 1.1 AlphaQubit: Transformer-Based Neural Decoder for Surface Codes
- **Title:** Learning high-accuracy error decoding for quantum processors
- **Authors:** Bausch et al. (Google DeepMind & Google Quantum AI)
- **Venue:** *Nature*, 2024
- **Year:** 2024
- **Why it is a milestone:** This paper introduced **AlphaQubit**, a recurrent transformer-based neural network trained on both simulated and real Sycamore processor data, to decode surface-code error syndromes. It achieved ~6% fewer errors than tensor-network decoders and ~30% fewer than fast correlated-matching decoders at code distances 3 and 5. It converted QEC decoding from a physics problem into a machine-learning engineering problem and is widely regarded as the first demonstration that large-scale neural networks can surpass specialized algorithmic decoders on real quantum hardware.

### 1.2 Quantum Error Correction Below the Surface-Code Threshold
- **Title:** Quantum error correction below the surface code threshold
- **Authors:** Google Quantum AI and Collaborators
- **Venue:** *Nature*, 2024
- **Year:** 2024
- **Why it is a milestone:** Google's Willow processor demonstrated, for the first time, that increasing the code distance (from d=3 to d=5 to d=7) actually *reduces* the logical error rate — proving the system operates below the surface-code threshold. The distance-7 memory achieved a logical error rate of ~0.143% per cycle and a lifetime 2.4x longer than the best physical qubit. This was a three-decade milestone in experimental physics, enabled in part by AI-assisted decoding and real-time feedback, and it immediately made fault-tolerant QML a near-term possibility.

### 1.3 Data-Driven Decoding of QEC Codes Using Graph Neural Networks
- **Title:** Data-driven decoding of quantum error correcting codes using graph neural networks
- **Authors:** Moritz Lange, Pontus Havstrom, Basudha Srivastava, et al.
- **Venue:** *Physical Review Research* 7, 023181
- **Year:** 2025
- **Why it is a milestone:** This work established the first comprehensive ML benchmark for QEC, evaluating CNN, GNN, and transformer architectures for surface-code decoding. It explicitly recognized and exploited **implicit long-range dependencies** in stabilizer syndromes — a novel insight that shifted the field from local matching algorithms to graph-neural architectures. The GNN decoder achieved statistically significant improvements over the best classical methods and was tailored to experimental input from superconducting devices.

### 1.4 GraphQEC: A Universal Neural Decoder for Arbitrary Stabilizer Codes
- **Title:** Efficient and universal neural-network decoder for stabilizer-based quantum error correction
- **Authors:** G. Hu, Han-Sen Zhong, et al.
- **Venue:** arXiv:2502.19971; under review at *Nature* family
- **Year:** 2025
- **Why it is a milestone:** GraphQEC is the first **code-agnostic, universal neural decoder** that runs in linear time and achieves unprecedented accuracy across surface codes, color codes, and quantum LDPC codes. On a distance-12 qLDPC code, it achieved a logical error rate of 9.55x10^-5 — an 18-fold improvement over the previous best specialized decoder — while maintaining ~157 mus/cycle decoding speed. It demonstrated that a single learned architecture can replace hand-crafted decoders for multiple code families, a critical step toward scalable fault-tolerant hardware.

### 1.5 Multi-Core Circuit Decoder for Logical QEC with Entangling Gates
- **Title:** A Multi-Core Circuit Decoder for Quantum Error Correction
- **Authors:** Yiqing Zhou, Chao Wan, Eun-Ah Kim, et al.
- **Venue:** *Nature Computational Science*, 2025
- **Year:** 2025
- **Why it is a milestone:** This paper tackled the harder problem of decoding during **logical entangling operations** (not just memory). The multi-core circuit decoder achieves competitive accuracy while running much faster than conventional union-find or minimum-weight perfect matching decoders when logical qubits interact. This is a prerequisite for fault-tolerant *computation* rather than mere storage, and it represents a direct bridge between AI research and practical quantum computing architectures.

---

## 2. Quantum Machine Learning — Provable Advantage & Kernel Methods

This theme covers papers that rigorously prove or experimentally demonstrate quantum advantages for learning tasks, as well as foundational works on quantum kernel methods that reshaped theoretical understanding of QML.

### 2.1 Quantum Learning Advantage on a Scalable Photonic Platform
- **Title:** Quantum learning advantage on a scalable photonic platform
- **Authors:** Zheng-Hao Liu, Romain Brunel, Emil E. B. Ostergaard, Oscar Cordero, Senrui Chen, Yat Wong, Jens A. H. Nielsen, Axel B. Bregnsbo, Sisi Zhou, Hsin-Yuan Huang, Changhun Oh, Liang Jiang, John Preskill, Jonas S. Neergaard-Nielsen, Ulrik L. Andersen
- **Venue:** *Science* 389, 1332-1335
- **Year:** 2025
- **Why it is a milestone:** This is widely regarded as one of the first **experimental demonstrations of a genuine quantum learning advantage** on a real-world problem using a scalable hardware platform. The team used a femtosecond-laser-written photonic chip to run kernel-based quantum machine learning, demonstrating increased speed, accuracy, and energy efficiency compared to classical supercomputing methods for the same ML task. The work was highlighted as a breakthrough because it moved QML from synthetic benchmarks to an integrated photonic platform capable of real-world deployment.

### 2.2 Quantum Machine Learning Beyond Kernel Methods
- **Title:** Quantum machine learning beyond kernel methods
- **Authors:** Sofiene Jerbi, Lukas J. Fiderer, Hendrik Poulsen Nautrup, Jonas M. Kubler, Hans J. Briegel, Vedran Dunjko
- **Venue:** *Nature Communications* 14, 517
- **Year:** 2023
- **Why it is a milestone:** This paper provided a rigorous theoretical framework showing that **variational quantum algorithms** can go beyond the limitations of quantum kernel methods, which had dominated QML theory. It established that quantum neural networks can exploit structural inductive biases unreachable by classical kernels, and it catalyzed the 2023-2025 shift toward variational and equivariant quantum architectures. It remains one of the most-cited QML theory papers of the period.

### 2.3 Exponential Concentration and Untrainability in Quantum Kernel Methods
- **Title:** Exponential concentration in quantum kernel methods
- **Authors:** Supanut Thanasilp, Samson Wang, M. Cerezo, Zoe Holmes
- **Venue:** arXiv:2208.11060; published in *Nature Communications Physics* (2024)
- **Year:** 2024
- **Why it is a milestone:** This paper proved a **fundamental no-go theorem**: quantum kernels based on random circuits suffer from exponential concentration, meaning kernel values collapse to their mean as the number of qubits grows, rendering them untrainable. This was a sobering but essential result that redirected the entire QML community away from naive random-circuit kernels and toward **problem-aware, structured encodings** (e.g., equivariant, geometric, or physics-informed kernels). It is one of the most influential negative results in recent QML history.

### 2.4 Learning Many-Body Hamiltonians with Heisenberg-Limited Scaling
- **Title:** Learning many-body Hamiltonians with Heisenberg-limited scaling
- **Authors:** Hsin-Yuan Huang, Yihong Tong, Di Fang, Yixu Su
- **Venue:** *Physical Review Letters* 130, 200403
- **Year:** 2023
- **Why it is a milestone:** This paper established that quantum algorithms can learn many-body Hamiltonian parameters with **Heisenberg-limited precision** (scaling as 1/sqrt(N) in sample complexity), which is provably optimal. It bridged quantum metrology and quantum machine learning, showing that quantum-enhanced learning is not merely a theoretical curiosity but can achieve information-theoretic limits for physics-motivated problems. It has become a cornerstone for quantum-enhanced scientific discovery pipelines.

---

## 3. Quantum-Inspired Generative Models — Schrodinger Bridges

The Schrodinger bridge problem from quantum physics has emerged as a powerful mathematical framework for generative AI, giving rise to a new family of diffusion-like models that directly transport between arbitrary data distributions rather than noising to a Gaussian.

### 3.1 Diffusion Schrodinger Bridge Matching
- **Title:** Diffusion Schrodinger bridge matching
- **Authors:** Yuyang Shi, Valentin De Bortoli, Andrew Campbell, Arnaud Doucet
- **Venue:** *NeurIPS* 2023 (36th Conference on Neural Information Processing Systems)
- **Year:** 2023
- **Why it is a milestone:** This paper introduced a practical, scalable algorithm for learning Schrodinger bridges between arbitrary distributions via diffusion matching. Unlike classical diffusion models that require Gaussian endpoints, this method directly learns stochastic transport between source and target data, making it ideal for **image-to-image translation, drug discovery, and biology**. It launched a sub-field of bridge matching that has since become one of the most active alternatives to diffusion models in generative AI.

### 3.2 I2SB: Image-to-Image Schrodinger Bridge
- **Title:** I2SB: Image-to-image Schrodinger bridge
- **Authors:** Guan-Horng Liu, Arash Vahdat, De-An Huang, Evangelos Theodorou, Weili Nie, Anima Anandkumar
- **Venue:** *ICML* 2023 (40th International Conference on Machine Learning)
- **Year:** 2023
- **Why it is a milestone:** I2SB was the first large-scale demonstration that Schrodinger bridge methods could outperform classical diffusion models on **real image-to-image tasks** (e.g., super-resolution, inpainting, JPEG restoration). It showed that directly learning transport between paired distributions yields higher fidelity and fewer artifacts than noising-denoising pipelines. It has been widely adopted in computer vision and medical imaging pipelines.

### 3.3 Aligned Diffusion Schrodinger Bridges
- **Title:** Aligned diffusion Schrodinger bridges
- **Authors:** Vignesh Ram Somnath, Matteo Pariset, Ya-Ping Hsieh, Maria Rodriguez Martinez, Andreas Krause, Charlotte Bunne
- **Venue:** *UAI* 2023 (39th Conference on Uncertainty in Artificial Intelligence)
- **Year:** 2023
- **Why it is a milestone:** This paper extended Schrodinger bridges to **single-cell biology and population dynamics**, aligning trajectories across perturbed cellular states. It demonstrated that physics-inspired optimal transport can solve biological problems (e.g., predicting cell responses to drug dosage) better than classical neural optimal transport, and it inspired a wave of follow-up work in computational biology and chemistry.

---

## 4. Quantum-Inspired Optimization & Tensor Networks

Tensor networks, originally developed for quantum many-body physics, have become a major tool for classical machine learning, offering compressed representations of high-dimensional data with provable entanglement-structure guarantees.

### 4.1 Cons-Training Tensor Networks for Constrained Combinatorial Optimization
- **Title:** Cons-training tensor networks: Embedding and optimization over discrete linear constraints
- **Authors:** Javier Lopez-Piqueres, Jing Chen
- **Venue:** *SciPost Physics* 18, 192; also presented at *NeurIPS* 2025 workshops
- **Year:** 2025
- **Why it is a milestone:** This paper introduced a method to **embed hard discrete constraints directly into tensor network architectures** (MPS/MPO) for combinatorial optimization, using imaginary-time evolution and DMRG-like optimization. It demonstrated that quantum-inspired tensor networks can solve constrained QUBO and routing problems with polynomial memory, avoiding the exponential blow-up of brute-force search. It represents a major step in the quantum-inspired classical solver direction, which is competitive with NISQ hardware on certain problem classes.

### 4.2 Quantum-Inspired Tensor Networks for Geometric Modeling & Cryptography
- **Title:** A Quantum-Inspired Neural Network for Geometric Modeling (related: Tensor network attacks on cryptographic protocols)
- **Authors:** Aizpurua et al.; Bermejo & Orus; Lopez-Piqueres & Chen
- **Venue:** arXiv series (2024-2025); *Quantum* journal; *NeurIPS* 2025
- **Year:** 2024-2025
- **Why it is a milestone:** A series of papers in 2024-2025 demonstrated that **tensor networks can simulate quantum circuits classically** at scales that break toy cryptographic systems (e.g., 32-bit Blowfish, S-DES) and solve geometric modeling problems via MPS-encoded message-passing. The key insight is that MPS/PEPS can compress quantum wavefunctions and high-dimensional neural network weights with polynomial resources. This line of work blurred the boundary between classical ML, quantum simulation, and quantum-inspired optimization, and it sparked renewed debate on where the quantum advantage boundary truly lies.

---

## 5. Quantum Neural Networks — Trainability, Barren Plateaus & Dequantization

Understanding when quantum neural networks can be trained, and when they are secretly classically simulable, became a central theoretical question in 2023-2025.

### 5.1 On the Relation Between Trainability and Dequantization of Variational QML
- **Title:** On the relation between trainability and dequantization of supervised quantum machine learning
- **Authors:** Elies Gil-Fuster, J. J. Meyer, et al. (Cerezo group)
- **Venue:** *ICLR* 2025 (International Conference on Learning Representations)
- **Year:** 2025 (preprint 2024)
- **Why it is a milestone:** This paper resolved a major open question: **trainability does not imply classical simulability, and vice versa**. It constructed explicit variational quantum models that are provably trainable (gradient-based) yet not dequantizable, and others that are classically simulable yet untrainable. The result destroyed the informal assumption that if it's easy to train, it's easy to simulate classically, and it redirected the field toward designing QNN architectures that are simultaneously trainable, non-dequantizable, and practically relevant.

### 5.2 Does Provable Absence of Barren Plateaus Imply Classical Simulability?
- **Title:** Does provable absence of barren plateaus imply classical simulability? Or, why we need to rethink variational quantum computing
- **Authors:** M. Cerezo, Martin Larocca, Diego Garcia-Martin, et al.
- **Venue:** arXiv:2309.09685; *Nature Reviews Physics* / *PRX Quantum* follow-ups
- **Year:** 2023-2024
- **Why it is a milestone:** This paper and its sequels (Larocca et al. 2024) established that **many architectures free of barren plateaus (e.g., shallow hardware-efficient ansatze with local observables) are precisely those that are classically simulable by tensor networks**. It created a constructive tension: to avoid flat gradients, one needs structure; but too much structure enables classical simulation. This has driven the 2024-2025 search for Goldilocks architectures (e.g., QCNNs, equivariant circuits, symmetry-preserving ansatze) that retain trainability while evading classical simulability.

---

## 6. Quantum Reinforcement Learning

Quantum physics has inspired new RL algorithms that exploit quantum oracles for sample-complexity improvements, and RL has been used to optimize quantum control and circuit design.

### 6.1 Quantum Natural Policy Gradient for Reinforcement Learning
- **Title:** Accelerating quantum reinforcement learning with a quantum natural policy gradient based approach
- **Authors:** Yang Xu, Vaneet Aggarwal
- **Venue:** *ICML* 2025 (42nd International Conference on Machine Learning); PMLR 267:69059-69077
- **Year:** 2025
- **Why it is a milestone:** This paper introduced **QNPG**, a quantum version of the Natural Policy Gradient algorithm that replaces classical random sampling with deterministic quantum gradient estimation. It proved a sample complexity of O-tilde(epsilon^-1.5) for quantum oracle queries, beating the classical lower bound of O-tilde(epsilon^-2). This is one of the first **rigorous super-quadratic speedups** for a reinforcement learning algorithm using quantum subroutines, and it was accepted at ICML 2025 as a landmark result in quantum RL theory.

### 6.2 Quantum Deep Deterministic Policy Gradient in Continuous Action Spaces
- **Title:** Quantum reinforcement learning in continuous action space
- **Authors:** S. Wu et al.
- **Venue:** *Quantum* 9, 1660 (journal)
- **Year:** 2025
- **Why it is a milestone:** This work extended quantum RL from discrete Gridworlds to **continuous action spaces** using a quantum Deep Deterministic Policy Gradient (DDPG) algorithm. It demonstrated single-shot quantum state generation: after one training run, the agent can output control sequences to drive any initial quantum state to any desired target state. This eliminated the need for per-target optimization, a major practical advance. The paper has been cited over 100 times in less than a year, making it one of the most impactful quantum RL papers of the period.

### 6.3 RL for Quantum Circuit Optimization and QEC Code Discovery
- **Title:** Simultaneous discovery of quantum error correction codes and encoders with a noise-aware reinforcement learning agent
- **Authors:** J. Olle, R. Zen, M. Puviani, F. Marquardt
- **Venue:** arXiv:2311.04750; *npj Quantum Information* 10, 126 (2024)
- **Year:** 2024
- **Why it is a milestone:** This paper demonstrated that a **single RL agent can simultaneously discover both the quantum error-correcting code and the encoder circuit** adapted to a given noise model. It converted the historically human-driven code-design process (e.g., surface codes, LDPC codes) into an automated optimization problem. Follow-up work in 2025 scaled this to larger codes and gadget-based circuit search, making it one of the most promising AI-driven approaches to QEC architecture design.

---

## 7. Neural Quantum States & Quantum Simulation + ML

Using classical neural networks to represent quantum wavefunctions has advanced dramatically, with direct implications for AI-driven scientific discovery.

### 7.1 Operator Quantum State: A Foundation Model for Quantum Dynamics
- **Title:** Operator Quantum State: A Foundation Model for Quantum Dynamics
- **Authors:** (Multiple groups; see MLQP Journal Club 2026 schedule and arXiv:2501 series)
- **Venue:** arXiv; presented at major physics-ML workshops (2025-2026)
- **Year:** 2025-2026
- **Why it is a milestone:** This emerging class of foundation models for quantum dynamics uses transformer-like architectures trained on large corpora of Hamiltonian evolution data to predict the time evolution of arbitrary quantum systems. It represents the extension of the classical AI foundation-model paradigm into quantum many-body physics, with the potential to replace expensive TD-DMRG and exact diagonalization for intermediate-size systems. It is considered a 2025-2026 frontier and is rapidly being adopted by computational chemistry and materials groups.

---

## 8. Honorable Mentions (High-Impact Pre-2023 Foundational Work Cited Heavily in This Period)

While the scope is 2023-2026, these pre-2023 papers are so frequently cited as foundations that they form the implicit trunk of the current literature:

- **Huang et al. 2022** — *Quantum advantage in learning from experiments* (*Science* 376). Proved that quantum-enhanced experiments can learn quantum many-body systems with exponentially fewer measurements than classical shadow tomography. Heavily cited in all 2023-2025 Hamiltonian-learning work.
- **McClean et al. 2018** — *Barren plateaus in quantum neural network training landscapes* (*Nature Communications* 9). The original barren-plateau paper; still the most-cited reference in every QML trainability discussion.
- **De Bortoli et al. 2021** — *Diffusion Schrodinger Bridge with Applications to Score-Based Generative Modeling* (*NeurIPS* 2021). The original paper connecting Schrodinger bridges to generative AI; spawned the entire 2023-2025 bridge-matching sub-field.
- **Liu et al. 2021** — *A rigorous and robust quantum speed-up in supervised machine learning* (*Nature Physics* 17). Proved exponential quantum speedup for kernel-based classification using discrete-log problem structure; the benchmark for all subsequent provable quantum advantage claims.
- **Hao et al. 2022** — *A quantum-inspired tensor network algorithm for constrained combinatorial optimization problems* (*Frontiers in Physics* 10). Cited 45+ times; established the quantum-inspired TN paradigm for optimization that 2024-2025 papers build upon.

---

## Summary Table: The 15 Milestone Papers at a Glance

| # | Paper | Venue | Year | Key Contribution |
|---|-------|-------|------|------------------|
| 1 | AlphaQubit: Learning high-accuracy error decoding for quantum processors | *Nature* | 2024 | Transformer QEC decoder beats classical algorithms |
| 2 | Quantum error correction below the surface code threshold | *Nature* | 2024 | First below-threshold experimental QEC on Willow |
| 3 | Data-driven decoding of QEC using GNNs | *Phys. Rev. Research* | 2025 | GNN benchmark + long-range syndrome dependencies |
| 4 | GraphQEC: Universal neural decoder for stabilizer codes | arXiv / *Nature* (2025) | 2025 | Code-agnostic decoder; 18x better on qLDPC |
| 5 | Multi-Core Circuit Decoder for QEC | *Nature Comput. Sci.* | 2025 | Fast decoding during logical entangling gates |
| 6 | Quantum learning advantage on a scalable photonic platform | *Science* | 2025 | Experimental quantum ML advantage on photonic chip |
| 7 | Quantum machine learning beyond kernel methods | *Nature Commun.* | 2023 | Theoretical framework for VQA advantages over kernels |
| 8 | Exponential concentration in quantum kernel methods | *Nat. Commun. Phys.* | 2024 | No-go theorem redirecting QML toward structured kernels |
| 9 | Learning many-body Hamiltonians with Heisenberg-limited scaling | *PRL* | 2023 | Optimal quantum-enhanced Hamiltonian learning |
| 10 | Diffusion Schrodinger bridge matching | *NeurIPS* | 2023 | Scalable SB algorithm for arbitrary-distribution generative AI |
| 11 | I2SB: Image-to-image Schrodinger bridge | *ICML* | 2023 | First large-scale SB model beating diffusion on image tasks |
| 12 | Cons-training tensor networks for constrained optimization | *SciPost Phys.* / *NeurIPS* | 2025 | Hard constraints embedded in TN via DMRG |
| 13 | On relation between trainability and dequantization | *ICLR* | 2025 | Resolved trainability-vs-simulability open question |
| 14 | Quantum Natural Policy Gradient (QNPG) | *ICML* | 2025 | Quantum RL with O-tilde(epsilon^-1.5) sample complexity |
| 15 | Quantum DDPG in continuous action spaces | *Quantum* | 2025 | Continuous quantum RL; 100+ citations in <1 year |

---

*Curated July 2026. Selection criteria: (a) peer-reviewed in top-tier venues (Nature/Science/NeurIPS/ICML/ICLR/PRL/Nature Physics), or (b) preprints with >50 citations and clear community impact, or (c) experimental breakthroughs on flagship hardware. Incremental ablations and pure engineering optimizations are excluded.*
