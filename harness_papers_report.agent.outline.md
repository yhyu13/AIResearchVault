# Research Report Outline: Harness System Architecture for AI Agents (2025–2026)

## 1. Executive Summary
- 300 words
- Key finding: Harness engineering has matured from implementation detail to first-class research discipline
- Eight papers reviewed across automated evolution, runtime adaptation, evaluation, safety, and infrastructure

## 2. Theoretical Foundations: Agent = Model + Harness
- 800 words
- 2.1 Formal decomposition (The Last Harness, Life-Harness, Harness-Bench)
- 2.2 Harness components taxonomy: prompts, tools, orchestration, infrastructure, middleware, model config
- 2.3 Implications for agent evaluation methodology

## 3. Automated Harness Evolution
- 1200 words
- 3.1 The Last Harness: Two-level meta-learning framework
  - Harness Evolution Loop (Worker → Evaluator → Evolution Agent)
  - Meta-Evolution Loop (blueprint optimization across tasks)
  - Meta-learning formulation and convergence metrics
- 3.2 Retrospective Harness Optimization (RHO)
  - Coreset selection via DPP-Greedy
  - Group rollout with self-validation and self-consistency
  - Best-of-NN harness proposal with self-preference
  - Results: +19% SWE-Bench Pro without validation labels
- 3.3 Comparison: meta-learning vs. self-preference approaches

## 4. Runtime Interface Adaptation
- 1000 words
- 4.1 Life-Harness architecture
  - Four lifecycle layers: Environment Contract, Procedural Skill, Action Realization, Trajectory Regulation
  - Trajectory-driven evolution with Codex agent
- 4.2 Empirical results: 116/126 settings improved, 88.5% avg gain, cross-model transfer
- 4.3 Complementarity with model training: base model outperforms specialized derivative
- 4.4 Limitations: deterministic environments only

## 5. Harness-Aware Post-Training
- 1000 words
- 5.1 Extended ALFWorld benchmark with three harness levels (h-low, h-mid, h-high)
- 5.2 Tool schema shifts: v1.0 → v1.1 → v2.0
- 5.3 Key findings
  - Harness informativeness monotonically improves performance
  - Training-time harness application > post-hoc application (20+ point gap)
  - Harness-aware post-training robust to tool environment shift
- 5.4 GiGPO vs GRPO credit assignment

## 6. Evaluation Infrastructure
- 1200 words
- 6.1 Harness-Bench: 106 tasks, 5,194 trajectories, diagnostic protocol
  - TaskScore = Security × Completion × Process
  - 23.8-point gap between best/worst harness
- 6.2 SEAGym: RL-style self-evolution evaluation
  - Train batches, frozen validation, ID/OOD transfer, replay diagnostics
  - Non-monotonic improvement dynamics (regression at epoch 4)
- 6.3 Orchard: Kubernetes-native environment service
  - 0.28s command latency, 100% reliability at 1,000 concurrent sandboxes
  - 10× cost reduction vs managed services
- 6.4 Gap analysis: no unified cross-suite protocol exists

## 7. Safety and Auditability
- 1000 words
- 7.1 HarnessAudit framework
  - Three layers: L1 Boundary Compliance, L2 Execution Fidelity, L3 System Stability
  - 210 tasks, 8 domains, 69 role templates, 525 perturbation cases
- 7.2 Key findings
  - Completion-safety misalignment: best system scores 0.32 overall
  - Resource access violations dominate
  - Multi-agent configurations exponentially expand risk surface
- 7.3 Hidden audit artifacts design

## 8. Industry and Community Landscape
- 600 words
- 8.1 OpenAI's 5-month agent experiment (1M+ LOC, 1/10th time)
- 8.2 Framework categories: context engineering, architectural constraints, entropy management
- 8.3 Community resources: awesome-agent-harness, MCP protocol, LangChain patterns
- 8.4 Enterprise tooling: Harness.io, E2B, Daytona, Modal

## 9. Synthesis and Strategic Implications
- 800 words
- 9.1 Cross-cutting themes
  - Harness as optimization target, not implementation detail
  - Runtime adaptation as model training alternative
  - Evaluation fragmentation blocking progress
- 9.2 Open research questions
  - Stochastic environment extension for Life-Harness
  - Meta-evolution empirical validation
  - Cross-benchmark transfer studies
  - Joint capability-safety optimization
- 9.3 Recommendations for practitioners
  - Report results at model+harness configuration level
  - Invest in harness engineering before model fine-tuning
  - Adopt self-hosted environment infrastructure for scale
  - Implement snapshot-level diagnostics for harness evolution

## 10. References
- All 8 papers with full citation
