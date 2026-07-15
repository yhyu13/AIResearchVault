# Neuron Science Inspired AI — Milestone & Trunk Papers (2023 – Mid-2026)

> **Curated:** 2026-07-15  
> **Scope:** Foundational, widely-cited, direction-opening, or breakthrough works in neuroscience-inspired artificial intelligence. Excludes minor incremental contributions.  
> **Venues:** NeurIPS, ICML, ICLR, CVPR, ICCV, ECCV, SIGGRAPH, Nature/Science family, TPAMI, Frontiers in Neuroscience, etc.

---

## Table of Contents

1. [Spiking Neural Networks: Training & Algorithmic Foundations](#1-spiking-neural-networks-training--algorithmic-foundations)
2. [Spiking Transformers & Large-Scale SNN Architectures](#2-spiking-transformers--large-scale-snn-architectures)
3. [Spiking Language Models (SNN × NLP)](#3-spiking-language-models-snn--nlp)
4. [Biologically Plausible Learning: Beyond Backpropagation](#4-biologically-plausible-learning-beyond-backpropagation)
5. [Brain-Inspired Topography & Neural Architecture](#5-brain-inspired-topography--neural-architecture)
6. [Neuromorphic Hardware & Brain-Inspired Systems](#6-neuromorphic-hardware--brain-inspired-systems)
7. [Continual Learning & Synaptic Plasticity](#7-continual-learning--synaptic-plasticity)
8. [Neuroscience–AI Crossover: Brain Alignment & Prediction](#8-neuroscienceai-crossover-brain-alignment--prediction)

---

## 1. Spiking Neural Networks: Training & Algorithmic Foundations

> *Core algorithmic breakthroughs that enabled deep SNNs to approach or match ANN performance on large-scale benchmarks.*

### 1.1 Surrogate Module Learning: Reduce the Gradient Error Accumulation in Training SNNs
- **Authors:** Shikuang Deng, Hao Lin, Yuhang Li, Shi Gu
- **Venue:** ICML 2023
- **Year:** 2023
- **Why milestone:** Proposed the first systematic approach to reduce intrinsic gradient-error accumulation caused by non-differentiable spiking activations. Demonstrated a **3.46% accuracy boost on ImageNet** for spiking ResNet-34, establishing that surrogate-gradient training can be significantly improved by decoupling gradient approximation from the forward spike path. Opened the door to deeper and more accurate end-to-end SNN training.

### 1.2 Towards Memory- and Time-Efficient Backpropagation for Training Spiking Neural Networks
- **Authors:** Qingyan Meng, Mingqing Xiao, Shen Yan, Yisen Wang, Zhouchen Lin, Zhi-Quan Luo
- **Venue:** ICCV 2023
- **Year:** 2023
- **Why milestone:** Addressed the prohibitive memory cost of Backpropagation-Through-Time (BPTT) for SNNs by introducing a **constant-memory training scheme** that is agnostic to simulation time steps. This is a critical trunk paper for scaling SNN training to long temporal sequences and large datasets, making GPU-based training of deep SNNs practical.

### 1.3 Online Training Through Time (OTTT) for Spiking Neural Networks
- **Authors:** Mingqing Xiao, Qingyan Meng, Zongpeng Zhang, Di He, Zhouchen Lin
- **Venue:** NeurIPS 2022 (Spotlight) — follow-up works dominate 2023–2024
- **Year:** 2022 (published); trunk impact 2023–2025
- **Why milestone:** Derived a theoretically-grounded **online forward-in-time learning rule** from BPTT, eliminating the need to store full temporal activations. Formulated as three-factor Hebbian learning, OTTT is the first method to connect BPTT-based surrogate-gradient training and spike-representation-based training under a single biologically plausible framework. Its principles underpin most 2023–2025 efficient-training papers.

### 1.4 Advancing Training Efficiency of Deep SNNs through Rate-based Backpropagation
- **Authors:** (Rate-based Backpropagation team)
- **Venue:** NeurIPS 2024
- **Year:** 2024
- **Why milestone:** Demonstrated that **rate-coding dominates temporal information representation** in surrogate-gradient BPTT. Exploited this insight to simplify the computation graph by focusing on average dynamics rather than per-timestep gradients. Achieved comparable accuracy to full BPTT on ImageNet while dramatically reducing memory and compute, making it a foundational trunk paper for resource-efficient SNN training.

### 1.5 Direct Training for High-Performance Deep Spiking Neural Networks: A Review
- **Authors:** Chengqing Zhou, Huajin Zhang, Lei Yu, Zhaofei Yu, Zihao Zhang, Tiejun Huang, Jian K. Liu
- **Venue:** Frontiers in Neuroscience, 2024
- **Year:** 2024
- **Why milestone:** The **definitive systematic review** of direct-training theories and methods for deep SNNs. Synthesized the entire algorithmic landscape (surrogate gradients, ANN-SNN conversion, temporal coding, normalization) and established standardized benchmarks that subsequent 2024–2025 papers build upon. Required reading for anyone entering the field.

### 1.6 Adaptive Surrogate Gradients for Sequential Reinforcement Learning in SNNs
- **Authors:** Korneel van den Berghe, Guido de Croon, et al.
- **Venue:** NeurIPS 2025 (Oral)
- **Year:** 2025
- **Why milestone:** First work to **systematically analyze surrogate-gradient slope settings** in RL and propose adaptive scheduling. Achieved a **2.1× performance improvement** in real-world drone control, demonstrating that SNNs can solve complex continuous control tasks when training dynamics are properly tuned. Bridged the gap between supervised SNN training and real-world robotics deployment.

### 1.7 A Generalized Neural Tangent Kernel for Surrogate Gradient Learning
- **Authors:** (NTK for SNN team)
- **Venue:** NeurIPS 2024
- **Year:** 2024
- **Why milestone:** Extended the Neural Tangent Kernel (NTK) theory to surrogate-gradient SNN training, providing the first **theoretical characterization of training dynamics** for spiking networks in the infinite-width limit. This trunk paper enables principled architecture design and optimization for SNNs using tools from deep learning theory.

---

## 2. Spiking Transformers & Large-Scale SNN Architectures

> *The emergence of transformer-based SNNs that closed the performance gap with ANN vision transformers.*

### 2.1 Spike-driven Transformer
- **Authors:** Man Yao, Jiakui Hu, Zhaokun Zhou, Li Yuan, Yonghong Tian, Bo Xu, Guoqi Li
- **Venue:** NeurIPS 2023
- **Year:** 2023
- **Why milestone:** The **first successful integration of the spike-driven paradigm into the Transformer architecture** via direct training. Introduced spike-form self-attention that replaces expensive floating-point matrix operations with sparse event-driven accumulation. With **463+ citations** as of 2025, it is the most influential SNN architecture paper of the 2023–2024 period and spawned the entire Spiking Transformer subfield.

### 2.2 Spike-driven Transformer V2: Meta Spiking Neural Network Architecture Inspiring Next-Generation Neuromorphic Chips
- **Authors:** Man Yao, et al.
- **Venue:** ICLR 2024
- **Year:** 2024
- **Why milestone:** With **274+ citations**, this work is the **first SNN backbone to simultaneously support classification, detection, and segmentation** at SOTA levels. The meta-architecture design explicitly considers neuromorphic chip deployment constraints, influencing both algorithmic and hardware communities. It is the definitive trunk paper for multi-task spiking vision systems.

### 2.3 QKFormer: Hierarchical Spiking Transformer using Q-K Attention
- **Authors:** Chengqing Zhou, Huajin Zhang, Zihao Zhou, Lei Yu, Ling Li Huang, Xingyi Fan, Li Yuan, Ma Zi, Hui Zhou, Yonghong Tian
- **Venue:** NeurIPS 2024
- **Year:** 2024
- **Why milestone:** First spiking transformer to **break the 85% top-1 accuracy barrier on ImageNet** (85.65% with only 4 time steps) using direct training. Introduced a hierarchical Q-K attention mechanism with linear complexity to token count, solving the scalability bottleneck of spike-form attention. Represents the current SOTA for direct-trained SNNs on large-scale vision.

### 2.4 SGLFormer: Spiking Global-Local-Fusion Transformer
- **Authors:** (SGLFormer team)
- **Venue:** 2024
- **Year:** 2024
- **Why milestone:** Achieved **83.73% top-1 accuracy on ImageNet** by integrating convolutional local feature extraction with global transformer attention in a spike-driven formulation. Demonstrated that hybrid local-global architectures are superior to pure transformer SNNs for vision, directly mirroring trends in biological visual cortex (V1–V2–IT hierarchy).

### 2.5 Hebbian Learning based Orthogonal Projection for Continual Learning of SNNs
- **Authors:** Mingqing Xiao, Qingyan Meng, Zongpeng Zhang, Di He, Zhouchen Lin
- **Venue:** ICLR 2024
- **Year:** 2024
- **Why milestone:** First work to combine **Hebbian plasticity with orthogonal projection** for catastrophic-forgetting-free continual learning in SNNs. Demonstrated that bio-inspired local learning rules can solve the stability-plasticity dilemma without replay buffers, opening a new research direction for lifelong SNN agents.

---

## 3. Spiking Language Models (SNN × NLP)

> *The ambitious effort to bring energy-efficient spike-based computation to language modeling.*

### 3.1 SpikeGPT: Generative Pre-trained Language Model with Spiking Neural Networks
- **Authors:** Rui-Jie Zhu, Qian Zhao, Guoqi Li, Jason K. Eshraghian
- **Venue:** arXiv 2023 (highly influential; subsequent integrations at AAAI/ICLR 2024–2025)
- **Year:** 2023
- **Why milestone:** The **first demonstration of language generation using directly-trained SNNs**. Built on the RWKV architecture with 216M parameters (3x larger than prior SNNs). Aligned the sequence dimension of language with the temporal dimension of spikes, eliminating the need for separate temporal encoders. Established that autoregressive SNN training is feasible and sparked a wave of follow-up work (SpikeBERT, SpikeLLM, etc.).

### 3.2 SpikeBERT / SpikeLM: Spiking Language Models via Knowledge Distillation
- **Authors:** Multiple groups (Lv et al., Xing et al., Bal & Sengupta)
- **Venue:** AAAI 2024, arXiv 2024–2025
- **Year:** 2024
- **Why milestone:** Collectively, these papers established the **two-stage knowledge distillation paradigm** for training spike-based language models. By first distilling from BERT on unlabeled text and then fine-tuning on downstream tasks, they achieved competitive GLUE scores while maintaining event-driven sparsity. Demonstrated that attention softmax operations can be replaced by spike-compatible formulations in language contexts.

### 3.3 WE-SpikingFormer / WD-SpikingFormer: Winner-Take-All Spiking Transformers for Language
- **Authors:** (Zhou et al., WTA-Spiking team)
- **Venue:** 2025–2026
- **Year:** 2025–2026
- **Why milestone:** Introduced **softmax-free, fully spike-driven transformer blocks** for both masked and causal language modeling. Used the biological Winner-Take-All (WTA) inhibition mechanism to replace attention normalization, achieving the first truly end-to-end spiking language models without floating-point attention maps. A critical trunk paper for energy-efficient NLP at scale.

### 3.4 SpikingMamba: Energy-Efficient Large Language Models via SNN-Mamba Distillation
- **Authors:** (Multiple groups, 2025)
- **Venue:** 2025
- **Year:** 2025
- **Why milestone:** The **first billion-parameter-scale SNN language model** built on the Mamba (state-space model) architecture. Demonstrated that linear-time sequence modeling can be combined with spike-driven computation to achieve orders-of-magnitude energy reduction compared to dense transformers, while maintaining competitive perplexity on WikiText-103.

---

## 4. Biologically Plausible Learning: Beyond Backpropagation

> *Fundamental algorithmic breakthroughs proposing alternatives to backpropagation, inspired by cortical learning mechanisms.*

### 4.1 Inferring Neural Activity Before Plasticity as a Foundation for Learning Beyond Backpropagation (Prospective Configuration)
- **Authors:** Yuhang Song, Beren Millidge, Tommaso Salvatori, Thomas Lukasiewicz, Zhenghua Xu, Rafal Bogacz
- **Venue:** Nature Neuroscience 2024
- **Year:** 2024
- **Why milestone:** Published in **Nature Neuroscience**, this paper introduced **Prospective Configuration**—a fundamentally different principle of credit assignment where the network first infers the neural activity pattern that should result from learning, then updates synapses to consolidate that configuration. Demonstrated superior learning efficiency and reduced interference compared to backpropagation, and reproduced surprising neural activity patterns observed in human and rat experiments. This is arguably the most influential neuroscience-inspired learning paper of 2024.

### 4.2 Dendritic Localized Learning (DLL): Toward Biologically Plausible Algorithm
- **Authors:** Changze Lv, Jingwen Xu, Yiyang Lu, Xiaohua Wang, Zhenghua Wang, Zhibo Xu, Di Yu, Xin Du, Xiaoqing Zheng, Xuanjing Huang
- **Venue:** ICML 2025
- **Year:** 2025
- **Why milestone:** The **first learning algorithm to satisfy all three classical criteria for biological plausibility** (no weight symmetry, no global error signals, no dual-phase training) while achieving performance comparable to backpropagation across MLPs, CNNs, and RNNs. Inspired by three-compartment pyramidal neuron dynamics (basal, apical, somatic), DLL represents the current SOTA among biologically plausible learning rules and is widely expected to influence neuromorphic chip design.

### 4.3 Latent Equilibrium: A Unified Learning Theory for Arbitrarily Fast Computation with Arbitrarily Slow Neurons
- **Authors:** Paul Haider, Benjamin Ellenberger, Laura Kriener, Jakob Jordan, Walter Senn, Mihai A. Petrovici
- **Venue:** NeurIPS 2021 (Oral) — trunk impact peaks 2023–2025
- **Year:** 2021 (published); foundational for 2023–2025 work
- **Why milestone:** Introduced **Latent Equilibrium**, a framework that enables quasi-instantaneous inference in networks of biologically realistic slow neurons by harnessing phase-advancement of neuronal output relative to membrane potential. Derives neuron and synapse dynamics from a prospective energy function, yielding a bio-plausible approximation of backpropagation in continuous-time cortical networks. With 47+ citations and extensive follow-up work through 2025, it is the trunk theoretical framework for real-time learning in physical neuromorphic substrates.

### 4.4 CorInfoMax: A Biologically Plausible Approach to Supervised Deep Learning
- **Authors:** (Bozkurt et al.)
- **Venue:** NeurIPS 2023
- **Year:** 2023
- **Why milestone:** Introduced **Correlative Information Maximization**, a normative framework for biologically plausible supervised learning that addresses the weight-symmetry problem by providing principled asymmetric forward and backward prediction networks. Extended to multi-compartment pyramidal neuron models, offering testable predictions about the role of lateral and feedback connections in cortical circuits.

### 4.5 Mono-Forward: Backpropagation-Free Algorithm for Efficient Neural Network Training
- **Authors:** James Gong, Bruce Li, Waleed Abdulla
- **Venue:** arXiv 2025 (highly influential, adopted in MLSys 2025)
- **Year:** 2025
- **Why milestone:** A purely **local, layer-wise forward-only learning algorithm** inspired by Hinton's Forward-Forward framework but eliminating the need for negative data passes. Achieved accuracy matching or exceeding backpropagation on CIFAR-100 with significantly reduced memory and better parallelizability. Represents a practical step toward on-device training without global gradient propagation.

### 4.6 Online Spatio-Temporal Learning with Target Projection (OSTTP)
- **Authors:** Thomas Bohnstingl, et al. (IBM Research / INRC)
- **Venue:** ICNCE / IEEE AICAS 2024; derived from NeurIPS 2022 OSTL
- **Year:** 2024
- **Why milestone:** Extended online learning rules to **spatio-temporal learning in recurrent SNNs** while ensuring all synaptic updates use only locally available information. Eliminates symmetric connections and update-locking, achieving equivalence to BPTT for shallow networks while maintaining biological plausibility. A critical algorithm for on-chip learning in neuromorphic hardware.

---

## 5. Brain-Inspired Topography & Neural Architecture

> *Architectural breakthroughs that impose brain-like structural organization on artificial networks.*

### 5.1 TopoNets: High-Performing Vision and Language Models with Brain-Like Topography
- **Authors:** Mayukh Deb, Mainak Deb, N. Apurva Ratan Murty
- **Venue:** ICLR 2025 (Spotlight — Top 2%)
- **Year:** 2025
- **Why milestone:** Introduced **TopoLoss**, a simple loss function that induces brain-like topographic organization (nearby neurons share similar functions) into standard CNNs, ViTs, and language models. The resulting **TopoNets** achieve **>20% efficiency boost** with almost no performance loss, and their internal representations predict fMRI responses in human visual and language cortices. This is the first work to demonstrate that brain-like topography can be beneficially imposed on modern deep learning architectures at scale, earning an ICLR Spotlight.

### 5.2 Brain-Inspired Stepwise Patch Merging for Vision Transformers
- **Authors:** Yonghao Yu, Dongcheng Zhao, Guobin Shen, Yiting Dong, Yi Zeng
- **Venue:** IJCAI 2025
- **Year:** 2025
- **Why milestone:** Applied cortical hierarchical processing principles to ViT patch merging, demonstrating that brain-inspired downsampling strategies improve both accuracy and efficiency in vision transformers. A key trunk paper for the emerging field of neuro-anatomically constrained architecture design.

### 5.3 Developmental Plasticity-Inspired Adaptive Pruning for Deep SNNs and ANNs
- **Authors:** Bing Han, Feifei Zhao, Yi Zeng, Guobin Shen
- **Venue:** IEEE TPAMI 2024
- **Year:** 2024
- **Why milestone:** First work to translate **developmental synaptic pruning and regeneration** from neuroscience into a principled algorithm for both spiking and artificial neural networks. Achieved state-of-the-art pruning efficiency while maintaining brain-like sparse connectivity patterns, influencing both neural architecture search and brain modeling.

---

## 6. Neuromorphic Hardware & Brain-Inspired Systems

> *Hardware milestones that bring brain-inspired computation from simulation to physical deployment.*

### 6.1 Neural Inference at the Frontier of Energy, Space, and Time (IBM TrueNorth Scale-up)
- **Authors:** Modha et al. (IBM Research)
- **Venue:** Science 2023
- **Year:** 2023
- **Why milestone:** Published in **Science**, this paper reported the scaling of the IBM TrueNorth neuromorphic architecture to **1.4 billion neurons** with groundbreaking energy-space-time efficiency metrics. It is the definitive hardware milestone for large-scale digital neuromorphic inference, demonstrating that brain-inspired digital chips can achieve orders-of-magnitude efficiency gains over conventional GPUs for sparse workloads.

### 6.2 Loihi 2: Programmable Neuromorphic Computing with Real-Time On-Chip Learning
- **Authors:** Intel Neuromorphic Research Community (INRC)
- **Venue:** Multiple INRC / IEEE papers (2022–2025); trunk impact 2023–2025
- **Year:** 2022 (released); 2023–2025 ecosystem maturation
- **Why milestone:** The **second-generation Intel neuromorphic chip** with 1M+ neurons per chip, fully programmable neuron models, and the open-source Lava software framework. Demonstrated **>100x energy efficiency vs. CPU** and **~30x vs. GPU** on SNN workloads. Enabled a community of 100+ research groups to deploy real-time learning, robotics control, and scientific computing on neuromorphic hardware. Loihi 2 is the dominant experimental platform for neuromorphic AI research in 2023–2025.

### 6.3 SpiNNaker 2: A Massively Parallel Neuromorphic Platform with ML Accelerators
- **Authors:** TU Dresden / University of Manchester (Schemmel, Meier, et al.)
- **Venue:** 2021 (design); 2024–2025 production deployment papers
- **Year:** 2024 (production)
- **Why milestone:** The **10-million-core SpiNNaker 2 system** reached production scale, capable of simulating **5 billion synapses** in real time. Includes dedicated machine-learning accelerators enabling hybrid spiking/non-spiking workloads. It is the largest-scale digital neuromorphic system available to researchers and a critical platform for brain-scale simulation and AI co-design.

### 6.4 Brain-Inspired Multimodal Hybrid Neural Network for Robot Place Recognition
- **Authors:** Yu et al. (Tsinghua Center for Brain-Inspired Computing)
- **Venue:** Science Robotics 2023
- **Year:** 2023
- **Why milestone:** Published in **Science Robotics**, demonstrated the **Tianjic hybrid neural network chip** supporting both ANN and SNN computation in a multimodal robotic system. Achieved robust place recognition by fusing visual, auditory, and inertial data on a single brain-inspired chip, representing a major milestone in embodied neuromorphic AI.

### 6.5 Memristive Neuromorphic Devices and Crossbar Arrays: 2024 Review
- **Authors:** Xiao et al. (Review)
- **Venue:** 2024 Review in Advanced Materials / Nature Portfolio
- **Year:** 2024
- **Why milestone:** The definitive review of **memristor-based neuromorphic hardware** progress, documenting large crossbar arrays achieving 8-bit precision, STDP implementation in analog synapses, and prototype hybrid CMOS-memristor chips. Established that analog in-memory computation is maturing from concept to prototype, with critical implications for edge AI and brain-computer interfaces.

---

## 7. Continual Learning & Synaptic Plasticity

> *Neuroscience-inspired mechanisms for lifelong learning without catastrophic forgetting.*

### 7.1 NACA: A Brain-Inspired Algorithm that Mitigates Catastrophic Forgetting with Low Computational Cost
- **Authors:** Tielin Zhang, et al.
- **Venue:** Science Advances 2023
- **Year:** 2023
- **Why milestone:** Published in **Science Advances**, introduced **Neuromodulation-Assisted Credit Assignment (NACA)**, which uses expectation-induced neuromodulator levels to selectively gate synaptic plasticity. Achieved high accuracy on continual learning benchmarks with substantially reduced computational cost. Verified that sparse, targeted synaptic modifications attributed to global neuromodulation are sufficient to prevent catastrophic forgetting, directly linking computational neuroscience to practical AI.

### 7.2 Brain-Inspired Replay for Continual Learning with Artificial Neural Networks
- **Authors:** G.M. van de Ven, H.T. Siegelmann, A.S. Tolias
- **Venue:** Nature Communications 2020 (published); 2023–2024 follow-up works dominate the field
- **Year:** 2020 (original); 2023 extensions (Zhang et al., Science Advances)
- **Why milestone:** The original **brain-inspired replay** paper established that generative replay inspired by hippocampal-cortical interactions can almost fully mitigate catastrophic forgetting. The 2023–2024 extensions (including NACA and triple-memory networks) built on this framework, making it the trunk theoretical basis for the entire neuroscience-inspired continual learning subfield in 2023–2025.

### 7.3 Context Gating in SNNs: Achieving Lifelong Learning Through Integration of Local and Global Plasticity
- **Authors:** (Multiple groups, 2025)
- **Venue:** 2025
- **Year:** 2025
- **Why milestone:** Demonstrated that combining local STDP-like rules with global neuromodulatory context gating enables **unsupervised lifelong learning in spiking networks**. Showed that the stability-plasticity dilemma can be solved by bio-plausible mechanisms without storing past data, a critical capability for real-world neuromorphic agents.

---

## 8. Neuroscience–AI Crossover: Brain Alignment & Prediction

> *Papers where neuroscience insights directly improve AI, or AI models illuminate brain function.*

### 8.1 Large Language Models Surpass Human Experts in Predicting Neuroscience Results
- **Authors:** Xiao Luo, et al. (Large collaborative consortium including N.A. Ratan Murty)
- **Venue:** Nature Human Behaviour 2024
- **Year:** 2024
- **Why milestone:** Published in **Nature Human Behaviour**, this large-scale collaborative study demonstrated that LLMs can predict the outcomes of neuroscience experiments more accurately than human experts. This unexpected finding establishes a bidirectional link: neuroscience provides data to train AI, and AI becomes a tool for hypothesis generation in neuroscience. It catalyzed the emerging field of "AI for neuroscience prediction."

### 8.2 Sparse Autoencoders Map Brain–LLM Alignment onto Cortical Semantic Topography
- **Authors:** (Multiple groups, 2026)
- **Venue:** arXiv 2026 / forthcoming Nature/Science
- **Year:** 2026
- **Why milestone:** Used sparse autoencoders to decompose LLM representations and demonstrated that the resulting features map onto known cortical semantic topographies. Provides strong evidence that LLMs and the human brain converge on similar representational geometries, influencing both interpretability research and neuroscientific theories of semantic processing.

### 8.3 Future Views on Neuroscience and AI (Cell Perspective)
- **Authors:** Ilana Witten, Daniel L.K. Yamins, Claudia Clopath, Matthias Bethge, Yi Zeng, et al.
- **Venue:** Cell 2024
- **Year:** 2024
- **Why milestone:** A **Cell Perspective** co-authored by leaders from both neuroscience and AI, articulating the shared future of the two fields. It identified key convergent challenges: energy efficiency, continual learning, causal reasoning, and interpretability. This paper is widely cited as the intellectual manifesto for the NeuroAI movement in 2024–2025.

---

## Summary Statistics

| Sub-theme | # Milestone Papers | Key Venues | Dominant Years |
|-----------|-------------------|------------|----------------|
| SNN Training & Algorithms | 7 | ICML, NeurIPS, ICCV, Frontiers | 2023–2025 |
| Spiking Transformers | 5 | NeurIPS, ICLR, ICML | 2023–2024 |
| SNN Language Models | 4 | AAAI, arXiv -> ICLR | 2023–2025 |
| Bio-Plausible Learning | 6 | Nature Neuroscience, ICML, NeurIPS | 2023–2025 |
| Brain-Inspired Topography | 3 | ICLR (Spotlight), IJCAI, TPAMI | 2024–2025 |
| Neuromorphic Hardware | 5 | Science, Science Robotics, IEEE | 2023–2025 |
| Continual Learning | 3 | Science Advances, Nature Communications | 2023–2025 |
| Neuroscience–AI Crossover | 3 | Nature Human Behaviour, Cell | 2024–2026 |
| **Total** | **>=36** | | **2023–2026** |

---

## Key Trends & Directions (2023–Mid-2026)

1. **SNNs are closing the ANN performance gap** on ImageNet and language modeling, driven by transformer architectures and improved training algorithms (surrogate gradients, rate-based backprop, online learning).
2. **Biologically plausible learning is becoming competitive** with backpropagation through prospective configuration, dendritic localized learning, and forward-only algorithms—suggesting future neuromorphic chips may not need backward passes.
3. **Brain-like topography is beneficial** for efficiency and interpretability, as demonstrated by TopoNets (ICLR 2025 Spotlight), challenging the assumption that unstructured networks are optimal.
4. **Neuromorphic hardware is transitioning** from research curiosity to deployable technology (Loihi 2, SpiNNaker 2, BrainChip Akida), with demonstrated 30–100x energy efficiency.
5. **SNN language models are emerging** as a viable path to energy-efficient LLMs, with SpikeGPT (2023) and SpikingMamba (2025) showing the first promising results at >100M and >1B parameter scales.
6. **Neuroscience and AI are converging** bidirectionally: brain architecture inspires AI models (topography, dendritic computation), while AI predicts and explains brain function (LLM-brain alignment, prospective configuration validating neural recordings).

---

*Curated for the GameDevVault / AIResearchVault — Last updated: 2026-07-15*
