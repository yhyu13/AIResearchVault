# Cross-Verification: Harness System Architecture Papers 2025–2026

## High Confidence Findings

| Finding | Supporting Papers | Evidence |
|---------|-------------------|----------|
| Harness is a first-class design dimension | 1, 2, 3, 5, 6 | All papers formally define harness as non-model component affecting performance |
| Life-Harness improves 116/126 settings without model updates | 2 | Table 1: cross-model, cross-environment results with 88.5% avg relative gain |
| Harness-Bench shows 23.8-point gap between best/worst harness | 3 | Table 2: NanoBot (76.2) vs OpenClaw (52.4) under same task set |
| HarnessAudit reveals completion-safety misalignment | 6 | Table 2: Gemini 3.1 Pro highest overall (0.32) but far from safe; Claude Opus 4.6 higher TCR but lower safety |
| Orchard reduces sandbox cost 10× vs managed services | 7 | Table 2: $673 (spot) vs $7,078 (Daytona/E2B) for 30,720 sandbox-hours |

## Medium Confidence Findings

| Finding | Supporting Papers | Evidence |
|---------|-------------------|----------|
| Batch size 20 is optimal for AHE harness evolution | 4 | Table 3: batch 20 only setting with positive validation and ID gains; 10 and 80 regress |
| RHO outperforms validation-feedback optimizers at matched budget | 8 | Table 2: RHO 0.78 vs Meta-Harness 0.62 at 1-round budget |
| Harness-aware post-training outperforms post-hoc harness application | 5 | Figure 4: training-time application outperforms post-hoc by 20.7 (h-mid) and 22.5 (h-high) points |

## Low Confidence / Exploratory

| Finding | Supporting Papers | Evidence | Caveat |
|---------|-------------------|----------|--------|
| Meta-evolution blueprint can generalize to unseen tasks | 1 | Algorithm 2 and meta-learning formulation | No empirical results provided; paper is theoretical |
| Cross-model harness transfer is viable | 2 | Life-Harness evolved from Qwen3-4B transfers to 17 models | Only tested on deterministic environments; stochastic settings unverified |
| Open-source agentic modeling can match proprietary systems | 7 | Orchard-GUI 68.4% avg vs OpenAI/Google proprietary | Evaluated on different benchmarks; direct head-to-head not conducted |

## Conflict Zones

| Conflict | Papers | Description |
|----------|--------|-------------|
| **Validation requirement** | 1 vs 8 | The Last Harness uses evaluator agent with explicit scoring; RHO claims no ground-truth validation needed. Both achieve improvements but with different assumptions about label availability. |
| **Harness scope definition** | 2 vs 5 | Life-Harness restricts harness to runtime interface (p, TE); Interplay paper restricts to p and TE only. Life-Harness includes action realization and trajectory regulation layers beyond prompt/tool description. |
| **Cost-optimal batch size** | 4 vs 7 | SEAGym finds batch 20 optimal for AHE; Orchard uses 128 parallel sandboxes. Different optimization targets (harness evolution vs RL training) may explain discrepancy. |
