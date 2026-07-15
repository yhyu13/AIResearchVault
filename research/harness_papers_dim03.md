## Dimension 3: Diagnostic Benchmarks for Harness Evaluation

### Key Findings
- **Harness-Bench** (arXiv 2026-05-27, Peking University/Qiyuan Tech) contains 106 sandboxed offline tasks across 8 workflow categories.
- Evaluates 6 configurable harnesses × 8 model backends = 5,088 trajectories + 106 Codex trajectories.
- Key metric: TaskScore = Security × Completion × Process, where Process = (Robustness + ToolUse + Consistency)/3.
- NanoBot achieves highest configurable-harness score (76.2), OpenClaw lowest (52.4)—23.8-point gap.
- **HarnessAudit** (arXiv 2026-05-14, UCSB/Stanford/MSR) audits full trajectories across 3 safety layers: L1 Boundary Compliance, L2 Execution Fidelity, L3 System Stability.
- 210 tasks across 8 real-world domains, 69 unique role templates, 525 perturbation cases.
- Best system achieves only 0.32 overall safety score; resource access violations dominate.

### Major Players & Sources
- Harness-Bench: Yilun Yao, Xinyu Tan, Chao-Hsuan Liu, Yaoming Li, Zhengyang Wang, Wenhan Yu, Zhewen Tan, Yuxuan Tian, Guangxiang Zhao, Lin Sun, Xiangzheng Zhang, Tong Yang (Peking University, Qiyuan Tech)
- HarnessAudit: Yichen Guo, Yepeng Liu, Yuzhe Yang, Qianqi Yan, Xuandong Zhao, Wenyue Hua, Sheng Liu, Sharon Li, Yuheng Bu, Xin Eric Wang (UCSB, UCB, Wisconsin, Stanford, MSR)

### Trends & Signals
- Benchmarks moving from final-output evaluation to full-trajectory auditing
- Safety and capability metrics are misaligned: high completion ≠ safe execution
- Multi-agent configurations exponentially expand safety risk surface

### Controversies & Conflicting Claims
- Harness-Bench uses LLM-based process assessment (Claude Sonnet 4.6 as judge)—introduces judge bias
- HarnessAudit's hidden audit artifacts assumption may not hold for adversarial agents that probe the evaluation infrastructure

### Recommended Deep-Dive Areas
- Cross-benchmark transfer of harness designs
- Human evaluation correlation with automated trajectory auditing
- Adversarial robustness of audit frameworks
