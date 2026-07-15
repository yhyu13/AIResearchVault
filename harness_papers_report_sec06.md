# 6. Evaluation Infrastructure

The maturation of harness engineering as a research discipline has created urgent demand for evaluation infrastructure that can measure harness effects independently of model capabilities. Three complementary systems have emerged in 2026: Harness-Bench for diagnostic capability evaluation, SEAGym for self-evolution dynamics, and Orchard for scalable environment infrastructure. Together they address the measurement gap, but significant fragmentation remains.

## 6.1 Harness-Bench: Diagnostic Capability Evaluation

Harness-Bench is the first benchmark to make the harness a primary axis of evaluation under common external task conditions[^harness-bench]. Rather than comparing heterogeneous agent stacks or holding execution setup fixed, it fixes the task environment, budget, timeout, and evaluator while varying the harness surrounding the model.

### 6.1.1 Task Suite and Protocol

The benchmark contains 106 sandboxed offline tasks across eight workflow categories:

| Category | Count | Description |
|----------|-------|-------------|
| Software Engineering & Codebase Maintenance | 22 | Repository-level reasoning, multi-file edits |
| Data, BI & Finance Analytics | 14 | Structured data analysis, visualization |
| Workspace, Tool Use & Multimodal Operations | 15 | File manipulation, tool orchestration |
| Knowledge, Evidence & Retrieval | 13 | Grounded research, citation verification |
| Office & Business Communication | 12 | Document generation, email workflows |
| Vertical Professional Workflows | 12 | Domain-specific tasks (legal, medical) |
| Long-running Autonomy & State Adaptation | 11 | Multi-session persistence, state recovery |
| SRE, DevOps & Release Ops | 7 | Deployment, monitoring, incident response |

Each task requires a concrete deliverable and is paired with an oracle or rubric. Tasks are manually reviewed for realism, solvability, oracle-checkability, and integrity (agents cannot bypass constraints by reading hidden answers).

### 6.1.2 Scoring Framework

Harness-Bench scores each run using both final outcome and execution trace:

$$\text{TaskScore}_i = \text{Security}_i \times \text{Completion}_i \times \text{Process}_i$$

where Security is binary (0 for violations, 1 otherwise), Completion measures task-specific output quality, and Process averages Robustness, ToolUse, and Consistency. The multiplicative form is intentionally conservative: high aggregate credit requires task completion, no security violation, and reliable execution behavior.

### 6.1.3 Main Results

The factorial evaluation uses 6 configurable harnesses and 8 API model backends, producing 5,088 trajectories plus 106 Codex trajectories. Key findings include:

- **Configuration-level variation**: NanoBot achieves the highest configurable-harness score (76.2), while OpenClaw achieves the lowest (52.4)—a 23.8-point gap under identical task conditions.
- **Harness dependence**: Stronger model backends exhibit lower cross-harness variance, suggesting they are more tolerant of harness differences. Weaker backends show larger variance, indicating their performance is more sensitive to execution substrate.
- **Process-quality correlation**: Higher-scoring harnesses tend to have stronger process profiles (tool-use appropriateness, consistency, robustness), but the causal direction is not established.

## 6.2 SEAGym: Self-Evolution Dynamics

SEAGym addresses a different evaluation need: measuring how agent harnesses evolve over time, not just their static performance[^seagym]. It converts static benchmarks into dynamic task sources with explicit schedules for training, validation, and assessment.

### 6.2.1 MDP-Style Evaluation Process

SEAGym models a self-evolution run as a Markov decision process where each state contains the current agent snapshot $A_t = (M, H_t)$, with $M$ the fixed base model and $H_t$ the mutable harness state. The environment samples a task batch $B_t$, the agent solves tasks producing trajectories $\mathcal{T}_t$ and feedback $F_t$, then applies its update rule:

$$H_{t+1} = U(H_t, B_t, \mathcal{T}_t, F_t)$$

SEAGym specifies the observed environment (task distribution, feedback, schedules, evaluation views) but leaves the policy and update rule to each agent.

### 6.2.2 Evaluation Views

SEAGym separates dataset splits from evaluation views:

| View | Purpose | Data Source |
|------|---------|-------------|
| Update-validation | Tracks intermediate snapshot quality | $D_{\text{val}}$ |
| ID transfer | Tests held-out in-distribution generalization | $D_{\text{test}}$ (same domain) |
| OOD transfer | Tests out-of-distribution generalization | $D_{\text{test}}$ (different domain) |
| Replay | Measures retention, forgetting, regression | $D_{\text{train}}$ re-evaluated |

This design enables fine-grained analysis of whether updates improve or regress performance, whether gains transfer, and whether intermediate snapshots collapse.

### 6.2.3 Key Findings

Experiments on Terminal-Bench 2.0 and HLE compare three self-evolution methods (ACE, TF-GRPO, AHE) under a shared epoch/batch protocol:

- **AHE is the only method that improves validation, ID, and OOD together**. AHE changes the agent harness itself (prompts, tool-use constraints, middleware), giving it broader leverage but also higher reliability burden.
- **Non-monotonic improvement**: AHE's replay diagnostics show the final agent solves 43/80 train-replay tasks vs. 34/80 for the initial agent, but after epoch 4 performance drops to 6/80 before recovering. This demonstrates that intermediate snapshots can regress catastrophically.
- **Batch size is non-monotonic**: Batch 20 is the only setting with positive validation and ID gains; batch 10 and batch 80 both regress. This suggests that update quality depends on evidence diversity, not just quantity.

## 6.3 Orchard: Scalable Environment Infrastructure

Orchard addresses the infrastructure bottleneck that limits large-scale agent training and evaluation[^orchard]. It provides a thin, Kubernetes-native environment service that decouples sandbox management from agent harness, trainer, and inference backend.

### 6.3.1 Architecture

Orchard Env follows a three-layer architecture:
- **Client SDK**: Synchronous and asynchronous Python interfaces for sandbox creation, command execution, file I/O
- **Orchestrator**: FastAPI service managing sandbox lifecycle, readiness tracking, execution scheduling
- **In-Pod Agent**: Lightweight FastAPI server inside each sandbox container, handling command execution with configurable timeouts

Key design choices include runtime agent injection (arbitrary Docker images need no per-image modifications), direct Pod-IP communication (bypassing Kubernetes API server for low latency), and watch-based readiness tracking.

### 6.3.2 System Performance

| Metric | Orchard Env | E2B | Modal | SkyPilot |
|--------|-------------|-----|-------|----------|
| Avg command latency | 0.28 s | 0.747 s | 2.046 s | 0.284 s |
| 1,000 sandbox stress test | 100% success, 26 s total | — | — | — |
| Cost (128 sandboxes × 240 hrs, spot) | $673 | $7,078 | $10,305 | — |

Orchard's 0.28 s latency matches SkyPilot Code Sandbox and significantly outperforms E2B (2.7× slower) and Modal (7.3× slower). The cost advantage is dramatic: self-hosted Kubernetes with spot instances reduces sandboxing cost by 10× compared to managed alternatives.

### 6.3.3 Training Recipes

Orchard instantiates three domain-specific recipes:
- **Orchard-SWE**: 67.5% on SWE-bench Verified (Qwen3-30B-A3B-Thinking), using credit-assignment SFT and Balanced Adaptive Rollout (BAR) for sparse-reward RL
- **Orchard-GUI**: 68.4% average on WebVoyager/Online-Mind2Web/DeepShop (4B vision-language model), competitive with proprietary OpenAI/Google systems
- **Orchard-Claw**: 73.9% pass@3 on Claw-Eval with ZeroClaw harness, using only 0.2K synthetic tasks

## 6.4 Gap Analysis

Despite these advances, the evaluation landscape remains fragmented:

| System | Tasks | Domains | Focus | Limitation |
|--------|-------|---------|---
| System | Tasks | Domains | Focus | Limitation |
|--------|-------|---------|-------|------------|
| Harness-Bench | 106 | 8 | Capability diagnostics | No self-evolution tracking |
| SEAGym | 2 benchmarks | Terminal + reasoning | Self-evolution dynamics | Limited task diversity |
| HarnessAudit | 210 | 8 | Safety auditing | No capability benchmarking |
| Orchard | 3 recipes | SWE + GUI + Claw | Infrastructure + training | No standardized evaluation protocol |

No unified cross-suite protocol exists, making it impossible to compare harness designs across domains. The community would benefit from a meta-benchmark that integrates capability, safety, and evolution metrics under a common task framework.

[^harness-bench]: Harness-Bench: Measuring Harness Effects across Models in Realistic Agent Workflows. arXiv:2605.27922. 2026-05-27. https://arxiv.org/abs/2605.27922
[^seagym]: SEAGym: An Evaluation Environment for Self-Evolving LLM Agents. arXiv:2606.17546. 2026-06-16. https://arxiv.org/abs/2606.17546
[^orchard]: Orchard: An Open-Source Agentic Modeling Framework. arXiv:2605.15040. 2026-05-06. https://arxiv.org/abs/2605.15040
