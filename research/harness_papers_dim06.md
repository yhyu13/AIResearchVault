## Dimension 6: Retrospective Harness Optimization (RHO)

### Key Findings
- **Retrospective Harness Optimization** (arXiv 2606.05922, CityU HK / MSR Asia) optimizes harness using only past trajectories, no validation labels.
- Three-stage pipeline: (1) Coreset Selection (DPP-Greedy for diverse, challenging tasks), (2) Group Rollout (G parallel solves per task, self-validation + self-consistency diagnostics), (3) Best-of-NN Harness Proposal (N candidates, pairwise self-preference selection).
- Results: SWE-Bench Pro pass rate 59% → 78% (+19%) in single round without external grading.
- RHO adds new tools (e.g., check_build_and_lint for non-standard Go toolchains) and skills targeting prior failure modes.
- At matched budget, RHO (0.78) outperforms Meta-Harness (0.62); at 3× budget, Meta-Harness reaches 0.80.

### Major Players & Sources
- Authors: Wenbo Pan, Shujie Liu, Chin-Yew Lin, Jingying Zeng, Xianfeng Tang, Xiangyang Zhou, Yan Lu, Xiaohua Jia (City University of Hong Kong, Microsoft Research Asia)
- Code: https://github.com/wbopan/retro-harness
- Base agent: Codex CLI (OpenAI, 2025) with GPT-5.5
- Benchmarks: SWE-Bench Pro, Terminal-Bench 2, GAIA-2

### Trends & Signals
- Self-supervised harness optimization eliminates dependency on labeled validation sets
- Self-preference ranking substitutes for latent utility function
- Optimized harness shifts agent behavior: more verification on SWE-Bench, more execution on Terminal-Bench/GAIA-2

### Controversies & Conflicting Claims
- RHO requires past trajectories from the target domain; cold-start scenarios unaddressed
- Self-preference may reinforce existing biases rather than discover novel solutions
- Comparison with The Last Harness (meta-learning) not conducted

### Recommended Deep-Dive Areas
- Cold-start harness optimization without past trajectories
- Theoretical guarantees for self-preference convergence
- Multi-round RHO with harness composition
