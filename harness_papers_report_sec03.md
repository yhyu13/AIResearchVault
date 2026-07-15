# 3. Automated Harness Evolution

If the harness is a first-class design dimension, the natural next question is whether its engineering can be automated. Two complementary approaches have emerged in 2026: meta-learning over harness evolution blueprints, and self-supervised retrospective optimization from past trajectories. Both eliminate the need for domain-specific human engineering, but they differ in their assumptions about task diversity and label availability.

## 3.1 The Last Harness: Meta-Learning Over Evolution Blueprints

*The Last Harness You'll Ever Build* proposes a two-level framework that automates not only harness improvement but also the design of the improvement process itself[^last-harness].

### 3.1.1 Harness Evolution Loop (Inner Level)

At the first level, the Harness Evolution Loop optimizes a worker agent's harness $\mathcal{H}$ for a single task through a closed-loop cycle of three agents:

1. **Worker Agent $W_{\mathcal{H}}$**: Executes the task using the current harness and produces an execution trace.
2. **Evaluator Agent $V$**: Adversarially verifies task outcomes, diagnoses failure modes, and scores performance.
3. **Evolution Agent $E$**: Analyzes the full evolution history and modifies the harness—prompts, tools, orchestration logic, observations, model configuration—to address diagnosed failure patterns.

The loop iterates for $K$ steps, starting from an initial harness $\mathcal{H}^{(0)}$. At each step, the worker executes, the evaluator diagnoses and scores, and the evolution agent produces an improved harness based on the full history of prior attempts. The best-performing harness $\mathcal{H}^{(\text{best})}$ is retained. Algorithm 1 in the paper formalizes this process with explicit state verification, criteria checking, performance auditing, and two-tier scoring (pass/fail then execution time).

### 3.1.2 Meta-Evolution Loop (Outer Level)

The second level generalizes this to multiple tasks. The Meta-Evolution Loop optimizes the evolution blueprint $\Lambda = (W_{\mathcal{H}}, \mathcal{H}^{(0)}, V, E)$ itself across diverse tasks, learning a blueprint $\Lambda^{(\text{best})}$ that enables rapid harness convergence on any new task. This maps directly onto the meta-learning framework of Thrun and Pratt (1998):

$$\Lambda^{(\text{best})} = \arg\max_{\Lambda} \; \mathbb{E}_{t_i \sim \mathcal{T}_{\text{train}}} \left[ \text{best\_score}\big(\text{HarnessEvolutionLoop}(t_i, \Lambda, K)\big) \right]$$

The meta-evolution agent can modify the evaluator prompt, evolution agent prompt, worker observation structure, scoring function design, and loop hyperparameters. Generalization is evaluated on held-out tasks by measuring convergence speed, final performance, and robustness across meta-test tasks.

### 3.1.3 Current Limitations

The framework is currently theoretical. The authors state they "plan to follow up with empirical results on diverse workflows" but no experimental validation is provided in the published version. This makes the Meta-Evolution Loop an exploratory contribution rather than an established method. Nevertheless, it establishes the conceptual possibility of automating the design of automation—a significant conceptual advance.

## 3.2 Retrospective Harness Optimization (RHO)

Where The Last Harness requires a meta-training task distribution, RHO operates from a fundamentally different assumption: only past trajectories are available, and no labeled validation set exists[^rho]. This makes it suitable for deployment scenarios where future task distributions are unknown and grading is expensive or impossible.

### 3.2.1 Three-Stage Pipeline

RHO consists of three stages:

**Stage 1: Coreset Selection.** Given a large set of past trajectories $\mathcal{D}$, RHO selects a diverse and challenging coreset $\mathcal{D}_{\text{core}}$ using a Determinantal Point Process (DPP) kernel. A language model judge analyzes each trajectory to extract a difficulty score $r_i$ and textual description. The DPP kernel balances difficulty against diversity via a tunable parameter $\theta$:

$$K = \mathrm{diag}(\widetilde{r}) \, S \, \mathrm{diag}(\widetilde{r}), \qquad \widetilde{r}_i = \big(\max(r_i, \epsilon) \,/\, \max_j \max(r_j, \epsilon)\big)^{\alpha}$$

where $\alpha = \theta / (2(1-\theta))$. With $\theta = 0.7$, the coreset captures difficult, diverse failure modes.

**Stage 2: Group Rollout.** For each task in the coreset, the agent generates $G$ parallel rollouts using the current harness. Two diagnostic signals are extracted:
- **Self-validation ($\mathrm{rank}_{\text{val}}$)**: Examines correctness within each trajectory, flagging incorrect tool invocations, false assumptions, and premature stopping.
- **Self-consistency ($\mathrm{rank}_{\text{con}}$)**: Examines whether behavior remains consistent across trajectories, identifying contradictions in plans, tool sequences, or final answers.

These signals form improvement instructions $I_t$ for each task, merged across the coreset into $I$.

**Stage 3: Best-of-NN Harness Proposal.** The agent generates $N$ candidate harnesses in parallel, each incorporating the improvement instructions. Each candidate is evaluated by re-solving the coreset tasks and computing a preference score against the baseline harness. The candidate with maximum relative advantage is retained if its score is strictly positive.

### 3.2.2 Empirical Results

RHO was evaluated on three benchmarks spanning software engineering (SWE-Bench Pro), technical work (Terminal-Bench 2), and knowledge work (GAIA-2). The base agent is Codex CLI (OpenAI, 2025) with GPT-5.5. Results show consistent improvements across all domains:

| Method | Harness Surface | SWE-Bench Pro | Terminal-Bench 2 | GAIA-2 |
|--------|----------------|---------------|------------------|--------|
| Vanilla Codex | None | 0.59 | 0.71 | 0.29 |
| Dynamic Cheatsheet | Skills | 0.62 (+0.03) | 0.73 (+0.02) | 0.30 (+0.01) |
| ReasoningBank | Memory | 0.61 (+0.02) | 0.73 (+0.02) | 0.28 (−0.01) |
| Sleep-time Compute | Memory | 0.64 (+0.05) | 0.73 (+0.02) | 0.32 (+0.03) |
| **RHO** | **Skills + Tools** | **0.78 (+0.19)** | **0.76 (+0.05)** | **0.37 (+0.08)** |

The SWE-Bench Pro improvement of +19 percentage points is particularly notable because it is achieved without any validation-based grading. The optimized harness adds new tools (e.g., `check_build_and_lint` for non-standard Go toolchains) and skills targeting prior failure modes.

### 3.2.3 Comparison with Validation-Feedback Methods

RHO was compared against Meta-Harness, a validation-feedback optimizer that proposes harness edits and grades each candidate on a labeled validation split[^rho]. At matched single-round budget, Meta-Harness achieves 0.62 vs RHO's 0.78 on SWE-Bench Pro. Scaling Meta-Harness to 10 rounds (3.1× compute budget) raises its ceiling to 0.80, slightly above RHO but requiring held-out labels and substantially more computation. This establishes that self-supervised harness optimization can match or exceed validation-driven methods when labels are scarce.

## 3.3 Comparative Analysis

| Dimension | The Last Harness | RHO |
|-----------|------------------|-----|
| Learning signal | Meta-training across tasks | Past trajectories only |
| Label requirement | Evaluator agent with scoring | No validation labels |
| Scope | Full harness + evolution blueprint | Full harness (skills + tools) |
| Empirical validation | None (theoretical) | Extensive (3 benchmarks) |
| Generalization target | Zero-shot on new tasks | Same-domain future tasks |
| Compute cost | High (inner + outer loops) | Moderate (single retrospective pass) |

The two approaches are complementary rather than competing. The Last Harness provides the conceptual framework for meta-learning over harness evolution; RHO provides a practical, empirically validated method for self-supervised improvement. A natural integration would use RHO as the inner-loop harness optimizer within The Last Harness's meta-evolution framework. No such integration has been attempted.

## 3.4 Ope
## 3.4 Open Questions

Several critical questions remain unresolved. First, The Last Harness's Meta-Evolution Loop lacks empirical validation; its convergence properties and practical compute requirements are unknown. Second, RHO requires a corpus of past trajectories from the target domain, leaving cold-start scenarios unaddressed. Third, both methods assume the harness can be modified without affecting model weights; joint optimization of harness and model parameters remains unexplored. Fourth, neither method has been evaluated on safety-critical tasks where harness modifications could introduce vulnerabilities rather than improve capability.

[^last-harness]: The Last Harness You'll Ever Build. arXiv:2604.21003. 2026-05-01. https://arxiv.org/abs/2604.21003
[^rho]: Retrospective Harness Optimization: Improving LLM Agents via Self-Preference over Trajectory Rollouts. arXiv:2606.05922. 2026-06-04. https://arxiv.org/abs/2606.05922
