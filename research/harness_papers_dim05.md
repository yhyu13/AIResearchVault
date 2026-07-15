## Dimension 5: Harness-Aware Post-Training & OOD Robustness

### Key Findings
- **The Interplay of Harness Design and Post-Training in LLM Agents** (arXiv 2606.25447, POSTECH) extends ALFWorld to treat harness as controllable design dimension.
- Three harness versions: h-low (minimal design effort), h-mid (admissible tools listed), h-high (rich tool descriptions + carrying state).
- Tool schema shifts: v1.0 (base), v1.1 (paraphrased names), v2.0 (grouped tools, cardinality 13→5).
- Key result: harness-aware post-training improves ID performance and enables OOD robustness; post-training under h-low suffers drastic drop under v2.0 shift.
- Training-time harness application outperforms post-hoc application by 20.7 (h-mid) and 22.5 (h-high) points.
- GiGPO (group-in-group policy optimization) consistently outperforms GRPO across all configurations.

### Major Players & Sources
- Authors: Kyungmin Kim, Youngbin Choi, Seoyeon Lee, Suhyeon Jun, Dongwoo Kim, Sangdon Park (POSTECH)
- Benchmark: Extended ALFWorld (3,827 task instances across 6 household categories)
- Models: GPT-5 Mini, Qwen2.5-3B, Qwen2.5-7B

### Trends & Signals
- Harness informativeness monotonically improves zero-shot performance; gain scales with model capacity
- Post-training under low-effort harness yields inferior performance to harness-aware post-training
- Tool environment shift (v2.0) is more severe than task shift for agent robustness

### Controversies & Conflicting Claims
- ALFWorld is a simplified text-based environment; generalization to real-world tool APIs unverified
- h-high harness requires expert knowledge of environment transition dynamics—cost rarely made explicit in prior work

### Recommended Deep-Dive Areas
- Scaling harness-aware post-training to web/API environments
- Joint optimization of harness design and model architecture
- Automated harness informativeness estimation
