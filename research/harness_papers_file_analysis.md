# Research Artifact: Harness System Architecture Papers (2025–2026)

## File Inventory

| # | Paper Title | Venue/Date | URL | Core Contribution |
|---|-------------|------------|-----|-----------------|
| 1 | The Last Harness You'll Ever Build | arXiv 2026-05-01 | https://arxiv.org/abs/2604.21003 | Two-level meta-learning framework for automated harness evolution |
| 2 | Adapting the Interface, Not the Model: Runtime Harness Adaptation for Deterministic LLM Agents | arXiv 2026-05-19 | https://arxiv.org/abs/2605.22166 | Life-Harness: lifecycle-aware runtime harness improving frozen LLM agents without model weight updates |
| 3 | Harness-Bench: Measuring Harness Effects across Models in Realistic Agent Workflows | arXiv 2026-05-27 | https://arxiv.org/abs/2605.27922 | Diagnostic benchmark for evaluating configuration-level harness effects |
| 4 | SEAGym: An Evaluation Environment for Self-Evolving LLM Agents | arXiv 2026-06-16 | https://arxiv.org/abs/2606.17546 | RL-style evaluation environment for self-evolving agent harness updates |
| 5 | The Interplay of Harness Design and Post-Training in LLM Agents | arXiv 2026-06-24 | https://arxiv.org/abs/2606.25447 | Systematic analysis of harness design influence on post-training under ID and OOD settings |
| 6 | Auditing Agent Harness Safety (HarnessAudit) | arXiv 2026-05-14 | https://arxiv.org/abs/2605.14271 | Framework for auditing full execution trajectories across boundary compliance, execution fidelity, and system stability |
| 7 | Orchard: An Open-Source Agentic Modeling Framework | arXiv 2026-05-06 | https://arxiv.org/abs/2605.15040 | Thin, Kubernetes-native environment service for scalable agentic modeling across domains |
| 8 | Retrospective Harness Optimization (RHO) | arXiv 2026-06-04 | https://arxiv.org/abs/2606.05922 | Self-supervised harness optimization using past trajectories and self-preference |

## Cross-Paper Mapping

### Overlapping Themes
- **Harness as a first-class design dimension**: Papers 1, 2, 3, 5, 6, 8 all treat harness engineering as central to agent performance, not merely an implementation detail.
- **Evaluation infrastructure**: Papers 3, 4, 6 introduce benchmarks/environments specifically for harness evaluation.
- **Self-evolution / automated harness improvement**: Papers 1, 4, 8 focus on automating harness evolution without human engineering.
- **Environment layer decoupling**: Papers 4, 7 emphasize thin, reusable environment services.

### Complementary Contributions
- Papers 2 + 5: Life-Harness adapts runtime interface without model updates; Paper 5 studies harness-aware post-training with model updates.
- Papers 3 + 6: Harness-Bench measures capability; HarnessAudit measures safety.
- Papers 1 + 8: Both automate harness evolution, but The Last Harness uses meta-learning over tasks while RHO uses self-preference over trajectories.

### Gaps
- Limited cross-benchmark comparison: most papers evaluate on disjoint benchmark suites.
- Cost analysis: only Orchard provides detailed cost benchmarking of environment infrastructure.
- Real-world deployment: most work is sandboxed; live-service evaluation remains underexplored.
