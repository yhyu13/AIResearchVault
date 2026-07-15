## Dimension 2: Runtime Interface Adaptation Without Model Updates

### Key Findings
- **Life-Harness** (arXiv 2026-05-19, Peking University) improves frozen LLM agents by adapting the runtime interface rather than model weights.
- Four lifecycle layers: (1) Environment Contract Layer, (2) Procedural Skill Layer, (3) Action Realization Layer, (4) Trajectory Regulation Layer.
- Results: 116/126 model-environment settings improved, 88.5% average relative gain across 18 model backbones including Qwen, Llama, xLAM families.
- Harnesses evolved from Qwen3-4B-Instruct trajectories transfer to 17 other models, showing environment-side structure capture.

### Major Players & Sources
- Authors: Tianshi Xu, Huifeng Wen, Meng Li (Peking University)
- Code: https://github.com/tianshixu/life-harness (inferred)
- Benchmarks: τ-bench, τ²-bench, AgentBench (7 environments total)

### Trends & Signals
- Runtime interface adaptation as alternative to parameter adaptation
- Cross-model harness reuse suggests environment-side structure is model-agnostic
- Complementary to model training: base Qwen2.5-32B-Instruct outperforms its tool-specialized derivative xLAM-2-32b-fc-r when paired with Life-Harness

### Controversies & Conflicting Claims
- Only evaluated on deterministic environments; stochastic settings (e.g., web navigation with live sites) unverified
- Action Realization Layer uses deterministic environment evidence—may not generalize to environments with ambiguous action spaces

### Recommended Deep-Dive Areas
- Stochastic environment extension
- Theoretical characterization of when runtime adaptation outperforms parameter adaptation
- Integration with model training (joint optimization)
