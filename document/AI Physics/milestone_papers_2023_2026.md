# AI Physics Milestone & Trunk Papers (2023 – Mid-2026)

> **Curated:** 2026-07-15  
> **Scope:** Foundational, widely-cited, or direction-opening papers in AI for Physics from 2023 to July 2026. Incremental works are excluded.  
> **Coverage:** Neural operators, physics-informed learning, weather/climate forecasting, molecular/materials science, differentiable simulation, and scientific foundation models.

---

## 1. Neural Operators & PDE Learning

### 1.1 Fourier Neural Operator with Learned Deformations for PDEs on General Geometries
- **Authors:** Z. Li, D. Z. Huang, B. Liu, A. Anandkumar  
- **Venue:** *Journal of Machine Learning Research* (JMLR)  
- **Year:** 2023  
- **Why milestone:** Extends the original Fourier Neural Operator (FNO) to arbitrary, non-rectangular domains by learning adaptive coordinate deformations. This removes FNO's long-standing restriction to regular grids and opens spectral neural operators to real-world engineering geometries.

### 1.2 Geometry-Informed Neural Operator for Large-Scale 3D PDEs
- **Authors:** Z. Li, N. Kovachki, C. Choy, B. Li, J. Kossaifi, S. Otta, et al.  
- **Venue:** *NeurIPS* 2023  
- **Year:** 2023  
- **Why milestone:** Scales neural operators to industrial-scale 3D PDE problems by incorporating geometric inductive biases directly into the architecture. Demonstrates that learned operators can generalize across complex 3D domains at resolutions previously intractable for pure neural surrogates.

### 1.3 Transolver: A Fast Transformer Solver for PDEs on General Geometries
- **Authors:** H. Wu, H. Luo, H. Wang, J. Wang, M. Long  
- **Venue:** *ICML* 2024  
- **Year:** 2024  
- **Why milestone:** Introduces a pure-attention architecture tailored for PDE solving that rivals FNOs and GNNs without relying on spectral or mesh-specific assumptions. Its strong general-geometry performance validated transformers as a viable backbone for scientific surrogate modeling.

### 1.4 Mamba Neural Operator
- **Authors:** H. Zheng et al.  
- **Venue:** *NeurIPS* 2024  
- **Year:** 2024  
- **Why milestone:** First application of state-space models (Mamba) to operator learning, offering linear-time complexity versus the quadratic cost of transformer-based PDE solvers. Provides a new scaling axis for high-resolution spatiotemporal PDE surrogates where attention becomes prohibitive.

### 1.5 D-FNO: A Decomposed Fourier Neural Operator for Large-Scale Parametric PDEs
- **Authors:** K. Li, W. Ye  
- **Venue:** *Computer Methods in Applied Mechanics and Engineering* (CMAME)  
- **Year:** 2025  
- **Why milestone:** Decomposes the FNO kernel into separable sub-operators, enabling training on parametric PDE families at scales unreachable by monolithic FNOs. Achieves competitive accuracy with orders-of-magnitude memory reduction for multi-query design problems.

---

## 2. Physics-Informed Neural Networks: Architecture Breakthroughs

### 2.1 Separable Physics-Informed Neural Networks (SPINN)
- **Authors:** J. Cho, S. Kim, et al.  
- **Venue:** *NeurIPS* 2023  
- **Year:** 2023  
- **Why milestone:** Replaces the dense MLP backbone of PINNs with a per-axis separable architecture, reducing forward-pass and memory costs exponentially in dimensionality. Enables training with >10^7 collocation points and proved that dimensionality decomposition is a viable path to high-dimensional PINNs.

### 2.2 Physics-Informed Neural Operator for Learning PDEs
- **Authors:** Z. Li, H. Zheng, N. Kovachki, D. Jin, H. Chen, B. Liu, K. Azizzadenesheli, A. Anandkumar  
- **Venue:** *ACM/IMS Journal of Data Science*  
- **Year:** 2024  
- **Why milestone:** Unifies the neural operator paradigm with physics-informed loss functions, enabling zero-shot and few-shot operator learning while enforcing differential constraints. Showed that combining operator generalization with physical regularity produces more robust extrapolation to unseen parameter regimes.

### 2.3 Dual Cone Gradient Descent for Training Physics-Informed Neural Networks
- **Authors:** Y. Hwang, D.-Y. Lim  
- **Venue:** *NeurIPS* 2024  
- **Year:** 2024  
- **Why milestone:** Proposes a second-order geometry-aware optimizer specifically designed for the multi-objective loss landscape of PINNs (data vs. physics vs. boundary terms). Achieved state-of-the-art convergence on several benchmark PDEs and reduced the notorious PINN training instability.

### 2.4 KAN: Kolmogorov-Arnold Networks
- **Authors:** Z. Liu, Y. Wang, et al.  
- **Venue:** *ICLR* 2025 (arXiv 2024)  
- **Year:** 2024/2025  
- **Why milestone:** Replaces fixed MLP activations with learnable univariate spline functions on edges, yielding superior scaling laws and interpretability for function approximation and PDE solving. Sparked a massive research thread (PIKAN, KINN, SPIKAN, Legend-KINN) and is widely viewed as a potential successor architecture to MLPs in scientific machine learning.

### 2.5 One-Shot Operator Learning from Single Solution Trajectories
- **Authors:** J. Jiao et al.  
- **Venue:** *Nature Communications* 2025  
- **Year:** 2025  
- **Why milestone:** Demonstrates that self-supervised meta-learning can learn PDE solution operators from a *single* trajectory, whereas prior methods required hundreds of examples. This is revolutionary for expensive physics simulations where data generation is the primary bottleneck.

---

## 3. AI for Weather & Climate Forecasting

### 3.1 GraphCast: Learning Skillful Medium-Range Global Weather Forecasting
- **Authors:** R. Lam, A. Sanchez-Gonzalez, et al. (Google DeepMind)  
- **Venue:** *Science* 2023  
- **Year:** 2023  
- **Why milestone:** First graph-neural-network-based global weather model to surpass ECMWF's operational high-resolution forecast (HRES) on the majority of 10-day forecast variables. Marked the inflection point where data-driven ML models became genuinely competitive with operational numerical weather prediction.

### 3.2 Pangu-Weather: Accurate Medium-Range Global Weather Forecasting with 3D Neural Networks
- **Authors:** K. Bi, L. Xie, et al. (Huawei)  
- **Venue:** *Nature* 2023  
- **Year:** 2023  
- **Why milestone:** Introduced a 3D Earth-specific transformer trained on 39 years of ERA5 reanalysis, outperforming ECMWF IFS on deterministic forecasts up to 7 days. Its open weights and efficient inference catalyzed the rapid proliferation of AI weather models in operational meteorology.

### 3.3 FourCastNet v2 / Spherical Fourier Neural Operator (SFNO)
- **Authors:** B. Bonev, T. Kurth, et al. (NVIDIA)  
- **Venue:** *NeurIPS* / NVIDIA Earth-2  
- **Year:** 2023  
- **Why milestone:** Adapted Fourier Neural Operators to the spherical geometry of the Earth, replacing patch-based Vision Transformers with a spectral backbone that respects global boundary conditions. Delivered 80,000x speedup over traditional NWP and became a cornerstone of NVIDIA's digital-twin initiative.

### 3.4 Neural General Circulation Models for Weather and Climate (NeuralGCM)
- **Authors:** S. Kochkov, J. Yuval, et al. (Google Research)  
- **Venue:** *Nature* 2024  
- **Year:** 2024  
- **Why milestone:** First fully differentiable hybrid GCM that couples a spectral dynamical core with neural-network physics parameterizations, trained end-to-end. Unlike pure data-driven models, it stably simulates multi-decadal climate while retaining realistic tropical cyclones and seasonal cycles—proving that hybrid physics+ML is the most viable path to long-term climate emulation.

### 3.5 Aurora: A Foundation Model of the Atmosphere for Weather & Climate
- **Authors:** C. Bodnar et al. (Microsoft Research)  
- **Venue:** *Nature* 2025  
- **Year:** 2025  
- **Why milestone:** Pretrained on >1 million hours of heterogeneous geophysical data (ERA5, CAMS, MERRA-2), Aurora is the first true atmospheric foundation model to outperform specialized weather models across forecasting, air quality, and wave prediction. Demonstrated that multi-dataset pretraining on a general-purpose transformer yields superior generalization over narrow task-specific training.

### 3.6 GenCast: Diffusion-Based Ensemble Weather Forecasting
- **Authors:** I. Price et al. (Google DeepMind)  
- **Venue:** *Nature* 2024 / 2025  
- **Year:** 2024/2025  
- **Why milestone:** First operational-quality diffusion model for probabilistic weather ensemble generation, producing large ensembles with calibrated uncertainty that rival ECMWF's 51-member ENS. Established generative models as a viable paradigm for weather forecasting, addressing the deterministic limitations of earlier GNN and transformer forecasters.

---

## 4. AI for Molecular & Materials Science

### 4.1 AlphaFold 3: Accurate Structure Prediction of Biomolecular Interactions
- **Authors:** J. Abramson, J. Adler, J. Dunger, J. Jumper, et al. (Google DeepMind / Isomorphic Labs)  
- **Venue:** *Nature* 2024  
- **Year:** 2024  
- **Why milestone:** Generalizes protein folding to universal biomolecular modeling (protein-ligand, protein-nucleic acid, antibodies, post-translational modifications) via a diffusion-based architecture replacing the Evoformer. With >5,900 citations in its first year and a 2024 Nobel Prize legacy, it is the most impactful structural-biology AI paper of the period.

### 4.2 MACE: Higher-Order Equivariant Message Passing Neural Networks for Fast and Accurate Force Fields
- **Authors:** I. Batatia, D. P. Kovacs, G. N. C. Simm, C. Ortner, G. Csanyi  
- **Venue:** *arXiv* (2022) / *NeurIPS* / *Nature Computational Science* ecosystem (2023)  
- **Year:** 2023 (wide adoption)  
- **Why milestone:** Unifies atomic cluster expansion with deep equivariant message passing, achieving state-of-the-art accuracy and transferability across organic molecules, solids, and interfaces. MACE and its pretrained variant MACE-MP-0 are rapidly becoming the default machine-learning interatomic potential in computational chemistry and materials modeling.

### 4.3 DeepH-E3 / xDeepH: Deep-Learning DFT Hamiltonian for Magnetic & Large-Scale Materials
- **Authors:** Y. Xu, W. Duan, et al. (Tsinghua University)  
- **Venue:** *Nature Computational Science* 2022 / *Nature Communications* 2023 / *Science Bulletin* 2024  
- **Year:** 2023–2024  
- **Why milestone:** Developed a general E(3)-equivariant neural-network framework that learns the Kohn-Sham Hamiltonian from small-scale DFT data and predicts electronic structure for large-scale systems with sub-meV accuracy. Delivered orders-of-magnitude speedups over conventional DFT and expanded from non-magnetic to magnetic materials, making it a universal surrogate for first-principles calculations.

### 4.4 MatterGen: Diffusion-Based Generative Model for Inorganic Materials Design
- **Authors:** Z. Zeni et al. (Microsoft Research AI for Science)  
- **Venue:** *Nature* 2025  
- **Year:** 2025  
- **Why milestone:** First generative model to design novel inorganic crystals with specified property targets (band gap, bulk modulus, chemistry) that were experimentally validated (e.g., synthesized TaCr2O6). Achieved >2x higher likelihood of generating stable, novel structures compared to prior methods, marking a shift from property prediction to closed-loop materials *generation*.

### 4.5 CHGNet: Universal Pretrained Neural Network Potential with Charge Awareness
- **Authors:** Berkeley Lab team  
- **Venue:** *Nature Machine Intelligence* (cover) 2023  
- **Year:** 2023  
- **Why milestone:** Pretrained on 1.5M+ Materials Project structures, CHGNet is the first universal neural potential to explicitly model charge state and magnetic moment, enabling charge-informed molecular dynamics and phase-diagram prediction. Demonstrated that pretraining on large inorganic datasets can yield general-purpose force fields comparable to DFT across the periodic table.

---

## 5. Differentiable Physics & Learned Simulation

### 5.1 Improving Gradient Computation for Differentiable Physics Simulation with Contacts
- **Authors:** Y. D. Zhong et al.  
- **Venue:** *ICML* 2023  
- **Year:** 2023  
- **Why milestone:** Introduced continuous collision detection with time-of-impact (TOI) gradients, solving the long-standing gradient breakdown in differentiable simulators at contact events. Enabled gradient-based optimization to learn optimal control sequences that match analytical solutions, unlocking differentiable physics for robotics and animation tasks with frequent collisions.

### 5.2 Neural SPH: Improved Neural Modeling of Lagrangian Fluid Dynamics
- **Authors:** Various (ICML 2024)  
- **Venue:** *ICML* 2024  
- **Year:** 2024  
- **Why milestone:** Advances neural surrogates for Lagrangian (particle-based) fluid simulation by learning correction terms over classical Smoothed Particle Hydrodynamics. Bridges the gap between pure data-driven fluid simulators and physically consistent Lagrangian methods, offering better generalization to novel initial conditions.

### 5.3 PlasticityNet: Learning to Simulate Metal, Sand, and Snow for Optimization Time Integration
- **Authors:** X. Li, Y. Cao, M. Li, Y. Yang, C. Schroeder, C. Jiang  
- **Venue:** *NeurIPS* 2022 / wide adoption 2023–2024  
- **Year:** 2022 (influence peak 2023–2024)  
- **Why milestone:** Although published in late 2022, its influence peaked in 2023–2024 as a canonical demonstration of learning constitutive relations for elastoplastic materials within a differentiable simulation loop. Enabled gradient-based design optimization across heterogeneous materials and became a benchmark for learned material-point-method simulators.

### 5.4 MeshMask: Physics-Based Simulations with Masked Graph Neural Networks
- **Authors:** P. Garnier, V. Lannelongue, J. Viquerat, E. Hachem  
- **Venue:** *ICLR* 2025  
- **Year:** 2025  
- **Why milestone:** Adapts masked pretraining strategies from vision transformers to mesh-based physics simulations, enabling self-supervised learning of PDE dynamics on unstructured meshes. Shows that masked autoencoding can pretrain generalizable physics surrogates with far less labeled simulation data than supervised alternatives.

---

## 6. Foundation Models for Scientific Discovery

### 6.1 GPhyT: General Physics Transformer
- **Authors:** RWTH Aachen / University of Virginia  
- **Venue:** *SciFM* / *arXiv* 2025  
- **Year:** 2025  
- **Why milestone:** Trained on 1.8 TB of simulation data spanning multiple physics domains, GPhyT achieved up to 29x better performance than specialized models and generalized to physics problems outside its training data without task-specific fine-tuning. Represents the first large-scale demonstration that a single transformer can serve as a universal surrogate for disparate physical phenomena.

### 6.2 MACE-MP-0: A General-Purpose Machine Learning Interatomic Potential
- **Authors:** D. P. Kovacs et al. (University of Cambridge / BAM / UC Berkeley)  
- **Venue:** *arXiv* / *Nature* ecosystem 2024  
- **Year:** 2024  
- **Why milestone:** A pretrained foundation-model variant of MACE trained on the Open Materials 2024 dataset, enabling zero-shot atomistic simulation across nearly all materials in the periodic table. Demonstrated that foundation-model pretraining in materials science can rival DFT accuracy with million-fold inference speedups, catalyzing community adoption of pretrained MLIPs.

### 6.3 PDE-Transformer: Transformer for Physics PDEs on Grids
- **Authors:** Technical University of Munich  
- **Venue:** *SciFM* / *arXiv* 2025  
- **Year:** 2025  
- **Why milestone:** Outperforms state-of-the-art vision architectures across 16 distinct types of physics simulations, treating PDE solving as a general sequence-to-sequence problem over gridded fields. Supports the emerging paradigm that physics simulation can be unified under a single pretrained transformer rather than hand-crafted PDE-specific architectures.

### 6.4 PhysiX: First Large-Scale Physics Simulation Foundation Model
- **Authors:** UCLA  
- **Venue:** *SciFM* / *arXiv* 2025  
- **Year:** 2025  
- **Why milestone:** A 4.5B-parameter model pretrained on diverse natural and synthetic video, then transferred to physics simulation tasks. Represents the first attempt to bridge natural-video foundation models with physical-dynamics prediction, suggesting that large-scale pretraining on visual data can bootstrap generalizable physical reasoning.

### 6.5 Walrus: Fluid Mechanics Foundation Model
- **Authors:** Flatiron Institute / NYU / University of Cambridge  
- **Venue:** *arXiv* 2025  
- **Year:** 2025  
- **Why milestone:** Open-weights foundation model trained across 19 fluid-mechanics scenarios spanning astrophysics, geoscience, plasma physics, and acoustics. Demonstrates that a single neural operator pretrained on diverse fluid regimes can be fine-tuned to out-of-domain flows, establishing a general-purpose surrogate for computational fluid dynamics.

---

## Summary Table

| Sub-Theme | # Papers | Key Direction |
|---|---|---|
| Neural Operators & PDE Learning | 5 | Scaling to 3D, general geometries, and linear-time operators |
| PINN Architecture Breakthroughs | 5 | KAN, separable architectures, physics-informed operators, one-shot learning |
| Weather & Climate Forecasting | 6 | Hybrid GCMs, foundation models, diffusion ensembles, operational deployment |
| Molecular & Materials Science | 5 | Universal force fields, generative materials design, DFT surrogates |
| Differentiable Physics & Simulation | 4 | Contact gradients, masked pretraining, Lagrangian neural surrogates |
| Foundation Models for Science | 5 | Multi-domain transformers, pretrained potentials, open-weights fluid FMs |
| **Total** | **~30** | |

---

## Notes on Selection Criteria

1. **Temporal cutoff:** Only papers from 2023 through mid-2026 (July 2026) are included. Papers with 2022 publication dates were included only if their community impact peaked during 2023–2026 (e.g., PlasticityNet).  
2. **Impact filter:** Preference given to papers in *Nature*, *Science*, *NeurIPS*, *ICML*, *ICLR*, *JMLR*, and top-tier journals in computational physics/mechanics.  
3. **Exclusions:** Pure methodological papers without a physics domain application, incremental hyperparameter studies, and narrow ablation works were excluded.  
4. **Architecture vs. Application:** The list balances *trunk* architectural innovations (KAN, SPINN, Mamba Neural Operator) with *milestone* application papers (AlphaFold 3, MatterGen, NeuralGCM) that demonstrated real-world scientific impact.
