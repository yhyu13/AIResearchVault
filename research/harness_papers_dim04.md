## Dimension 4: Self-Evolving Agents & Environment Infrastructure

### Key Findings
- **SEAGym** (arXiv 2026-06-16, Tsinghua) is an RL-style evaluation environment for self-evolving LLM agents.
- Converts static benchmarks into dynamic task sources with train batches, frozen validation views, held-out ID/OOD transfer views, replay diagnostics.
- Built on Harbor framework for containerized task execution.
- Experiments on Terminal-Bench 2.0 and HLE compare ACE, TF-GRPO, and AHE.
- Key finding: frequent updates may fail to improve held-out performance; useful intermediate snapshots may collapse later.
- **Orchard** (arXiv 2026-05-06, Microsoft Research/Columbia/UIUC) is a thin, Kubernetes-native environment service.
- Three recipes: Orchard-SWE (67.5% on SWE-bench Verified), Orchard-GUI (68.4% avg on WebVoyager/Online-Mind2Web/DeepShop), Orchard-Claw (73.9% pass@3 with ZeroClaw harness).
- Cost: $673 with spot instances vs $7,078 for Daytona/E2B (10× reduction).
- Execution latency: 0.28s avg command latency, matching SkyPilot Code Sandbox.

### Major Players & Sources
- SEAGym: Congjie Zheng, Chuanyi Xue, Bin Liang, Jun Yang, Changshui Zhang (Tsinghua University, BNRist)
- Orchard: Baolin Peng, Wenlin Yao, Qianhui Wu, Hao Cheng, Xiao Yu, Rui Yang, Tao Ge, Alessandro Sordoni, Xingdi Yuan, Yelong Shen, Pengcheng He, Tong Zhang, Zhou Yu, Jianfeng Gao (Microsoft Research, Columbia, UIUC)

### Trends & Signals
- Environment layer becoming a standalone, reusable service boundary
- Self-evolution evaluation requires snapshot-level diagnostics, not just final-epoch scores
- Credit-assignment SFT and Balanced Adaptive Rollout (BAR) for sparse-reward RL are emerging training techniques

### Controversies & Conflicting Claims
- SEAGym's batch-size ablation shows non-monotonic optimal (batch 20); contradicts "more data is better" assumption
- Orchard's cost advantage assumes Kubernetes expertise; managed services may still be preferable for smaller teams

### Recommended Deep-Dive Areas
- Standardized environment service APIs (interoperability across frameworks)
- Long-horizon RL training stability in agentic settings
- Cross-domain transfer of environment infrastructure
