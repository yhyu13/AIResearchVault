# 1. Executive Summary

The period 2025–2026 has witnessed a decisive shift in how the AI research community conceptualizes and engineers agent systems. No longer treated as mere "scaffolding" around a foundation model, the **agent harness**—encompassing prompts, tools, orchestration logic, infrastructure, middleware, and model configuration—has emerged as a first-class object of study, optimization, and evaluation. This report synthesizes findings from eight peer-reviewed and preprint papers published between May and June 2026, representing the state of the art in harness system architecture for large language model (LLM) agents.

The central thesis unifying these works is the formal decomposition **Agent = Model + Harness**[^last-harness]. This equation, now explicitly adopted across multiple independent research groups, reframes agent capability as a joint function of model weights and the execution substrate surrounding them. The implications are profound: performance improvements can originate from either component, and attributing success solely to the base model systematically overestimates its contribution.

Three major technical directions have crystallized. First, **automated harness evolution** eliminates manual engineering through meta-learning (The Last Harness) or self-supervised retrospective optimization (RHO). Second, **runtime interface adaptation** improves frozen models without weight updates by evolving the model–environment boundary (Life-Harness). Third, **diagnostic evaluation infrastructure** enables rigorous measurement of harness effects on capability (Harness-Bench), safety (HarnessAudit), and self-evolution dynamics (SEAGym). Complementing these, **open-source environment services** (Orchard) reduce the infrastructure cost of large-scale agent training by an order of magnitude.

The empirical results are substantial. Life-Harness improves performance in 116 of 126 model–environment settings, yielding an average relative gain of 88.5% across 18 model backbones without modifying a single weight[^life-harness]. Retrospective Harness Optimization (RHO) raises SWE-Bench Pro pass rates from 59% to 78% in a single optimization round, using no validation labels whatsoever[^rho]. Harness-Bench reveals a 23.8-point score gap between the best and worst harness configurations under identical task conditions and model backends[^harness-bench]. Yet HarnessAudit exposes a critical misalignment: even the highest-performing systems achieve only a 0.32 overall safety score, with resource access violations dominating failure profiles[^harness-audit].

The strategic implications for practitioners are immediate. Agent performance should be reported at the **model–harness configuration level**, not attributed to the base model alone. For resource-constrained deployments, harness engineering may deliver higher return on investment than model fine-tuning. Self-hosted environment infrastructure is essential for scaling, and snapshot-level diagnostics are required for safe harness evolution. Looking forward, the integration of meta-learning over harness evolution blueprints with standardized evaluation environments represents the next frontier—one that could enable zero-shot harness adaptation to novel domains.

[^last-harness]: The Last Harness You'll Ever Build. arXiv:2604.21003. 2026-05-01. https://arxiv.org/abs/2604.21003
[^life-harness]: Adapting the Interface, Not the Model: Runtime Harness Adaptation for Deterministic LLM Agents. arXiv:2605.22166. 2026-05-19. https://arxiv.org/abs/2605.22166
[^rho]: Retrospective Harness Optimization: Improving LLM Agents via Self-Preference over Trajectory Rollouts. arXiv:2606.05922. 2026-06-04. https://arxiv.org/abs/2606.05922
[^harness-bench]: Harness-Bench: Measuring Harness Effects across Models in Realistic Agent Workflows. arXiv:2605.27922. 2026-05-27. https://arxiv.org/abs/2605.27922
[^harness-audit]: Auditing Agent Harness Safety. arXiv:2605.14271. 2026-05-14. https://arxiv.org/abs/2605.14271
# 2. Theoretical Foundations: Agent = Model + Harness

The conceptual bedrock of the 2025–2026 harness engineering wave is a formal decomposition that treats the agent as the sum of two separable, independently optimizable components: the foundation model and the harness. This section traces the emergence of this formulation, catalogs the constituent elements of a harness, and examines its methodological implications for agent evaluation.

## 2.1 From Scaffolding to First-Class Design Dimension

Historically, the harness surrounding an LLM agent was regarded as implementation detail—prompt templates, tool wrappers, and logging infrastructure that varied idiosyncratically across projects. The shift toward treating it as a first-class object began with empirical observations: identical models achieved drastically different success rates when wrapped in different execution substrates[^life-harness]. By early 2026, multiple independent research groups had converged on an explicit formalization.

The most rigorous statement appears in *The Last Harness You'll Ever Build*, which defines a harness $\mathcal{H}$ as "every piece of code, configuration, and execution logic that is not the model itself"[^last-harness]. The paper adopts the equation $\mathbf{Agent} = \mathbf{Model} + \mathbf{Harness}$ from Trivedy (2026) and expands it into a six-component taxonomy:

| Component | Description | Example Systems |
|-----------|-------------|-----------------|
| System & task prompts | Identity, constraints, goals, in-context examples | Claude Code system prompts |
| Tools, skills, descriptions | Invocable capabilities (file editing, shell, browser, MCP) | Codex CLI tool set |
| Bundled infrastructure | Execution environment (filesystem, sandboxes, observability) | E2B, Daytona sandboxes |
| Orchestration logic | Control flow (subagent spawning, handoffs, routing, feedback loops) | AutoGen multi-agent conversations |
| Hooks & middleware | Deterministic guarantees (lint checks, verification, compaction) | OpenClaw middleware |
| Model configurations | Backbone choice, temperature, sampling, token limits, routing rules | GPT-5.4 with high reasoning effort |

This taxonomy is not merely descriptive—it is prescriptive. By enumerating the editable surfaces of a harness, it enables systematic optimization rather than ad hoc tuning.

## 2.2 Harness Constituents in Production Systems

The taxonomy maps directly onto production agent systems. AdaL (SylphAI, 2026), Claude Code (Anthropic, 2025), and Codex (OpenAI, 2025) are general-purpose software-engineering harnesses wrapping LLMs with filesystem access, shell execution, web search, and multi-file editing[^last-harness]. OpAgent (Guo et al., 2026) combines a Planner, Grounder, Reflector, and Summarizer into a multi-agent pipeline that achieved state-of-the-art results on WebArena[^last-harness]. In each case, the harness—not the model—determines what the agent perceives, how it acts, and how its work is orchestrated and verified.

The *Interplay* paper extends this view by restricting the harness to wrappers acting through the system prompt $p$ and the tool environment $\texttt{TE}$[^interplay]. In their formulation, the harness determines which tools are exposed, how they are described, and what auxiliary information accompanies each per-step observation. This narrower definition is tailored to their controlled study of harness informativeness, but it is consistent with the broader taxonomy above.

## 2.3 Methodological Implications for Evaluation

The formal decomposition has immediate consequences for how agent performance is measured and reported. If $\mathbf{Agent} = \mathbf{Model} + \mathbf{Harness}$, then holding the harness fixed while varying the model measures only a slice of the capability space. Conversely, holding the model fixed while varying the harness measures a different slice. Neither alone characterizes the full system.

Harness-Bench operationalizes this insight by fixing external task conditions (task, sandbox, budget, timeout, evaluator) while varying the harness configuration[^harness-bench]. Its results show that NanoBot achieves a 76.2 aggregate score while OpenClaw achieves 52.4 under the same task suite and model-backend pool—a 23.8-point gap attributable solely to harness design. The paper concludes that "agent capability should be reported at the model–harness configuration level rather than attributed to the base model alone."

This methodological shift is not without controversy. Some researchers argue that harness optimization is merely "prompt engineering at scale" and that true advances require model-level improvements. The empirical evidence contradicts this: Life-Harness enables a base Qwen2.5-32B-Instruct model to outperform its tool-specialized derivative xLAM-2-32b-fc-r, demonstrating that harness improvements can dominate model specialization[^life-harness].

## 2.4 The Agent as a Policy-Constrained Execution System

HarnessAudit pushes the formalization further by defining the harness as a policy-constrained execution system[^harness-audit]. Given a user goal $G$ and environment state $\mathcal{D}$, the harness decomposes the goal, dispatches subtasks to components, and constrains their actions:

$$\mathcal{H} := (\mathcal{A}, \mathcal{T}, \mathcal{R}, \Pi, \Phi, \Sigma), \qquad \mathcal{H}(G; \mathcal{D}_0) \longrightarrow (\tau_{\mathcal{H}}, y)$$

where $\mathcal{A}$ is the set of acting components, $\mathcal{T}$ the callable tools, $\mathcal{R}$ the environment resources, $\Pi$ the permission policy, $\Phi$ the information-flow policy, and $\Sigma$ the coordination protocol. This formulation makes explicit what the broader taxonomy leaves implicit: the harness is not merely a collection of components but a system governed by policies that enforce boundaries on execution.

The policy-centric view is essential for safety evaluation. A harness can return a correct, benign final answer while traversing a trajectory that accesses unauthorized resources or leaks context to the wrong agent[^harness-audit]. Output-level evaluation misses these failures; only trajectory-level auditing can detect them. This motivates the three-layer safety framework (Boundary Compliance, Execution Fidelity, System Stability) that HarnessAudit introduces and that will be examined in detail in Chapter 7.

[^last-harness]: The Last Harness You'll Ever Build. arXiv:2604.21003. 2026-05-01. https://arxiv.org/abs/2604.21003
[^life-harness]: Adapting the Interface, Not the Model: Runtime Harness Adaptation for Deterministic LLM Agents. arXiv:2605.22166. 2026-05-19. https://arxiv.org/abs/2605.22166
[^interplay]: The Interplay of Harness Design and Post-Training in LLM Agents. arXiv:2606.25447. 2026-06-24. https://arxiv.org/abs/2606.25447
[^harness-bench]: Harness-Bench: Measuring Harness Effects across Models in Realistic Agent Workflows. arXiv:2605.27922. 2026-05-27. https://arxiv.org/abs/2605.27922
[^harness-audit]: Auditing Agent Harness Safety. arXiv:2605.14271. 2026-05-14. https://arxiv.org/abs/2605.14271
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
# 4. Runtime Interface Adaptation Without Model Updates

While automated harness evolution methods modify the harness through meta-learning or retrospective analysis, *Life-Harness* explores a complementary question: can the runtime interface between a frozen model and its environment be adapted to improve performance without any model weight updates at all? The answer, demonstrated across seven deterministic agent environments and 18 model backbones, is a decisive yes.

## 4.1 The Case for Runtime Interface Adaptation

Most agent adaptation methods focus on parameter adaptation—updating model weights through supervised fine-tuning, reinforcement learning, or distillation. Life-Harness argues that in deterministic, rule-governed domains, much of the relevant structure lives outside the model: tool schemas, admissible action spaces, API contracts, feedback rules, stopping conditions, and recovery strategies[^life-harness]. The gap between static capability and interactive performance is often a boundary mismatch, not a reasoning deficit. For example, Qwen3.5-4B scores 74.0% on HMMT (a competition-level mathematics benchmark) but only 43.1% on ALFWorld (a deterministic embodied interaction benchmark), suggesting that the model possesses latent reasoning ability that is not effectively exercised through the current interface.

Life-Harness formalizes this distinction. Parameter adaptation updates model weights:

$$\theta' \leftarrow \mathcal{A}_{\mathrm{param}}(\theta, \mathcal{T}_{\mathrm{train}})$$

In contrast, runtime interface adaptation keeps model weights fixed and adapts the harness:

$$H' \leftarrow \mathcal{A}_{\mathrm{harness}}(H, \mathcal{T}_{\mathrm{train}}), \qquad \theta \; \text{fixed}$$

The adapted harness $H'$ changes how the frozen model interacts with the environment, while leaving both model weights and evaluation environment unchanged. This is environment-specific but model-agnostic: a harness evolved for a given environment can be applied across different model backbones adhering to the same interaction protocol.

## 4.2 Life-Harness Architecture

Life-Harness organizes runtime adaptation into four lifecycle layers, each operating at a distinct stage of the agent–environment interaction:

| Layer | Stage | Function | Failure Mode Addressed |
|-------|-------|----------|------------------------|
| Environment Contract | Before interaction | Calibrates tool descriptions and interface constraints | Tool contract mismatches |
| Procedural Skill | Task conditioning | Retrieves reusable procedures from training trajectories | Missing domain knowledge |
| Action Realization | Before execution | Validates and canonicalizes model-generated actions | Action realization failures |
| Trajectory Regulation | After execution | Monitors for repetition, stagnation, budget exhaustion | Trajectory degeneration |

### 4.2.1 Environment Contract Layer

This layer produces an enhanced contract $C' = C \oplus \Delta_C$ where $\Delta_C$ contains concise updates derived from environment policies, API behavior, and recurring failures in training trajectories. The enhanced contract is shown to the model in place of the original, enabling better tool utilization. For example, if training trajectories show that agents frequently call a tool with incorrect parameter ordering, $\Delta_C$ explicitly documents the correct ordering.

### 4.2.2 Procedural Skill Layer

A skill library $\mathcal{S}$ is constructed from training trajectories. For a task description $x$, the harness retrieves relevant skills using BM25 scoring:

$$\mathcal{K}_x = \mathrm{TopK}_{k \in \mathcal{S}} \; \mathrm{score}(x, k)$$

Retrieved skills are inserted into the initial system prompt to guide the model on solving common subproblems. This provides non-parametric guidance without modifying model weights.

### 4.2.3 Action Realization Layer

Given model action $a_t$, current trajectory $\tau_t$, and state $s_t$, this layer either submits the action to the environment or returns a model-visible block message $m_t$:

$$z_t = \textsc{RealizeAction}(a_t, \tau_t, C', s_t) \in \{\textsc{EXEC}(a_t), \textsc{Block}(m_t)\}$$

It uses deterministic environment evidence (tool schemas, admissible action sets, argument constraints) to prevent erroneous tool calls at the execution level. This is a critical safety mechanism: the model's intent may be correct, but its expression may violate environment contracts.

### 4.2.4 Trajectory Regulation Layer

After environment feedback, this layer monitors the updated trajectory for non-progressing patterns:

$$r_t = \textsc{RegulateTrajectory}(\tau_{t+1}, C', s_{t+1})$$

The output may be empty (no intervention), a soft recovery message, a warning regarding repeated failures, or a stronger corrective directive when degradation is detected. This specifically targets the trajectory degeneration failure mode where individual actions are valid but the episode as a whole fails to progress.

## 4.3 Empirical Results

Life-Harness was evaluated on seven deterministic environments from $\tau$-bench, $\tau^2$-bench, and AgentBench, covering household interaction (ALFWorld), web shopping (WebShop), operating-system control, database tasks, and policy-guided business workflows. The harness was evolved using Qwen3-4B-Instruct trajectories and a coding agent (Codex) to inspect traces and iteratively update the harness. The final harness was then frozen and evaluated on 17 additional model backbones.

### 4.3.1 Main Results

Across 18 model backbones (instruction-tuned, reasoning, and agent-specialized models), Life-Harness improves performance in 116 of 126 model–environment settings, with an average relative improvement of 88.5%. Key per-environment results include:

| Benchmark | Metric | Without Life-Harness | With Life-Harness | Relative Gain |
|-----------|--------|---------------------|-------------------|---------------|
| ALFWorld | Pass@1 | 41.1% | 75.7% | +84% |
| WebShop | Pass@1 | 31.4% | 44.0% | +40% |
| OS | Pass@1 | 34.7% | 41.2% | +19% |
| DBBench | Pass@1 | 48.4% | 64.6% | +34% |
| Airline ($\tau$-bench) | Pass@1 | 49.7% | 62.6% | +26% |
| Telecom ($\tau^2$-bench) | Pass@1 | 55.3% | 69.0% | +25% |

### 4.3.2 Cross-Model Transfer

The harnesses evolved only from Qwen3-4B-Instruct trajectories transfer to all 17 other models, including Llama-family and xLAM-family models. This demonstrates that Life-Harness captures reusable environment-side structure rather than model-specific behavior. The cross-model transfer is a strong indicator that the harness improvements are genuine interface adaptations, not merely overfitting to the source model's idiosyncrasies.

### 4.3.3 Complementarity with Model Training

Life-Harness is not merely an alternative to model training—it is complementary. The base Qwen2.5-32B-Instruct model, when paired with Life-Harness, outperforms its tool-specialized derivative xLAM-2-32b-fc-r. Furthermore, applying Life-Harness to xLAM itself yields additional improvements. This suggests that harness optimization and model specialization optimize different aspects of agent performance and can be stacked.

## 4.4 Limitations and Open Questions

The evaluation is limited to deterministic environments where tool schemas and action spaces are well-defined. Stochastic environments (e.g., web navigation with live sites, social media interaction) introduce ambiguity that may challenge the Action Realization Layer's deterministic validation. Additionally, the four-layer architecture was designed based on manual failure analysis of training trajectories; whether the same layer decomposition generalizes to other environment classes remains an open question. Finally, the method requires a coding agent (Codex) to evolve the harness from training trajectories, introducing a dependency on a capable external model.

[^life-harness]: Adapting the Interface, Not the Model: Runtime Harness Adaptation for Deterministic LLM Agents. arXiv:2605.22166. 2026-05-19. https://arxiv.org/abs/2605.22166
# 5. Harness-Aware Post-Training

While Life-Harness demonstrates that runtime interface adaptation can improve frozen models, the *Interplay* paper investigates a different but related question: how does harness design influence agents that *are* being post-trained? The study extends ALFWorld into a benchmark for tool-integrated agentic tasks and systematically varies harness informativeness, tool schemas, and task types to measure in-distribution (ID) and out-of-distribution (OOD) performance.

## 5.1 Experimental Design

The authors reformulate ALFWorld's text actions as tool calls: verbs correspond to tools and entities serve as arguments. For example, "Go to drawer 1" becomes `Go(receptacle='drawer 1')`. This reformulation enables controlled manipulation of three independent variables.

### 5.1.1 Harness Informativeness

Three harness versions are defined, each building on the previous:

| Harness | Tool Description (in $p$) | Valid Tools (in $\mathcal{T}_t$) | Carrying State (in $\mathcal{T}_t$) |
|---------|--------------------------|----------------------------------|-----------------------------------|
| h-low | Short one-line | — | — |
| h-mid | Short one-line | Listed | — |
| h-high | Rich (preconditions, interactions, roles) | Listed | Appended |

The h-low harness represents minimal design effort; h-mid adds admissible tool lists to each per-step history; h-high further expands tool descriptions and appends the agent's current inventory. Notably, prior work on ALFWorld typically used an even more informative harness than h-high—providing the full set of feasible tool calls at every step—without acknowledging this design choice.

### 5.1.2 Tool Schema Shifts

Three schema versions create controlled environment shifts:

| Schema | Example Tool Call for "move to drawer 1" |
|--------|------------------------------------------|
| v1.0 (base) | `Go(receptacle='drawer 1')` |
| v1.1 (paraphrase) | `NavigateTo(destination='drawer 1')` |
| v2.0 (grouped) | `ReceptacleControl(action='navigate_to', target='drawer 1')` |

Version v1.1 applies semantics-preserving renaming; v2.0 additionally groups tools by structural and functional similarity, reducing cardinality from 13 to 5. Each consolidated tool exposes sub-operations through a discrete action parameter. A tool call is valid only under the schema in which it is defined; otherwise, the environment returns "Invalid tool format."

### 5.1.3 Task Type Grouping

Six ALFWorld task categories are grouped by minimum sub-goals required:

| Group | Tasks | Sub-goals | Example |
|-------|-------|-----------|---------|
| t-easy | Pick, Look | 3–4 | "Put a plate on the coffee table" |
| t-med | Clean, Heat, Cool | 5 | "Clean the knife and put in the drawer" |
| t-hard | Pick 2 | 8 | "Put two pencils in the drawer" |

## 5.2 Key Findings

### 5.2.1 Zero-Shot Performance (Observation 1)

Harness informativeness monotonically improves zero-shot performance, and the magnitude of gain scales with model capacity. GPT-5 Mini shows the largest gain, achieving 61.0% on Pick 2 (t-hard) under h-high compared to 0.0% for most open-source models. Even under h-low, GPT-5 Mini achieves 17.1% on Pick 2, illustrating that model capacity is essential to drive harness-induced gains.

### 5.2.2 In-Distribution Post-Training (Observation 2)

The monotonic harness gain observed at zero-shot largely carries over after post-training. Qwen2.5-3B-Instruct post-trained with GRPO under h-high outperforms Qwen2.5-7B-Instruct post-trained with GRPO under h-low by 14.1 points, indicating that harness choice can outweigh model capacity even after post-training. GiGPO (group-in-group policy optimization) consistently outperforms GRPO across all configurations, consistent with its finer credit assignment in long-horizon tasks.

### 5.2.3 Post-Hoc vs. Training-Time Harness Application (Observation 3)

Applying a harness only after training recovers little of the benefit of training with it in place. The gap is particularly large for Qwen2.5-7B-Instruct with GRPO: training-time h-mid application outperforms post-hoc application by 20.7 points; training-time h-high outperforms post-hoc by 22.5 points. This suggests that the harness should be specified before post-training so the agent can adapt to the interface it will ultimately use.

### 5.2.4 Tool Environment Shift Robustness (Observation 4)

Harness-aware post-training is robust to tool environment shift, while post-training under h-low suffers a drastic performance drop under stronger shift. Qwen2.5-7B-Instruct post-trained with GRPO under h-low achieves only 2.7% under v2.0, which is 10.8 points below the base model without post-training (13.5%). This demonstrates that harness-aware post-training is not merely about improving ID performance—it is essential for OOD robustness when the action interface itself changes.

## 5.3 Implications

The findings have immediate practical consequences. First, the cost of harness design must be made explicit: h-mid and h-high require expert knowledge of environment transition dynamics, yet prior work rarely acknowledges this assumption. Second, training-time harness application is strongly preferred over post-hoc application, suggesting that practitioners should invest in harness design before initiating post-training campaigns. Third, the combination of harness-aware post-training with runtime interface adaptation (Life-Harness) could yield synergistic improvements—an integration that has not been explored.

[^interplay]: The Interplay of Harness Design and Post-Training in LLM Agents. arXiv:2606.25447. 2026-06-24. https://arxiv.org/abs/2606.25447
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
# 7. Safety and Auditability

The most sobering finding across the 2025–2026 harness literature is that capability and safety are misaligned. A harness can achieve high task completion while systematically violating permission boundaries, leaking information, or accessing unauthorized resources. HarnessAudit addresses this gap by treating the harness itself as the unit of safety evaluation and auditing complete execution trajectories rather than final outputs.

## 7.1 HarnessAudit Framework

HarnessAudit defines an agent harness as a policy-constrained execution system and evaluates it along three trajectory-level layers[^harness-audit]:

### 7.1.1 L1: Boundary Compliance

This layer evaluates whether each action stays within the permission and information-flow boundaries specified by the harness. Violations are recorded across three channels:

- **Tool violations**: Invoking unauthorized, task-irrelevant, or role-exceeding tools
- **Resource violations**: Accessing protected or out-of-scope files, records, fields, or objects
- **Information-flow violations**: Disclosing information through communication, forwarding, or final outputs when not permitted

The Safety Adherence Rate (SAR) for each channel is computed from weighted violation counts, with severity levels (low/high) assigned corresponding weights.

### 7.1.2 L2: Execution Fidelity

This layer evaluates whether the trajectory reaches the goal through valid intermediate steps:

- **Action validity**: Whether tool selection, arguments, and target objects are correct; whether redundant operations are avoided
- **Checkpointed task completion**: Whether task milestones verified from the trajectory or state are achieved

The Task Completion Rate (TCR) is computed from weighted checkpoint scores, and the Action Validity Score (AVS) measures intermediate action correctness.

### 7.1.3 L3: System Stability

This layer evaluates whether L1 and L2 remain satisfied under controlled stressors:

- Indirect prompt injection through tool-returned content
- Ambiguous or underspecified user goals
- Tool or runtime errors and noise

The Perturbation Stability (PB) score averages rubric-graded stability across all perturbation variants.

### 7.1.4 Overall Harness Safety Score

The composite score multiplies safety adherence by a weighted combination of fidelity and stability:

$$Score_i = \overline{SAR}_i \times (0.7 \cdot TCR_i + 0.15 \cdot AVS_i + 0.15 \cdot PB_i)$$

The multiplicative form ensures that high scores require both task completion and boundary respect—a harness cannot compensate for safety violations with better task performance.

## 7.2 HarnessAudit-Bench

HarnessAudit-Bench instantiates the framework on 210 tasks across eight real-world domains and 24 fine-grained scenarios[^harness-audit]:

| Domain | Scenarios | Role Templates | Key Risk Patterns |
|--------|-----------|----------------|-------------------|
| Finance | Portfolio management, compliance reporting | 5–14 per domain | Unauthorized data access, regulatory boundary crossing |
| E-commerce | Order processing, inventory management | 5–14 per domain | Payment tool misuse, customer data leakage |
| Healthcare | Patient records, appointment scheduling | 5–14 per domain | PHI disclosure, unauthorized diagnosis tools |
| Office Operations | Document workflows, meeting coordination | 5–14 per domain | Calendar privilege escalation, file sharing violations |
| Social Interaction | Messaging, content moderation | 5–14 per domain | Information forwarding, impersonation |
| Daily Life | Travel booking, home automation | 5–14 per domain | Location data leakage, device control misuse |
| Legal Compliance | Contract review, case research | 5–14 per domain | Privileged information access, unauthorized legal advice |
| Software Engineering | Code review, deployment | 5–14 per domain | Production access, secret exposure |

Each task is paired with audit rules covering tool rules (required vs. forbidden), resource rules (required vs. out-of-scope), and information-flow rules (communication constraints, data leakage). The benchmark constructs 11,586 role-tool authorization entries, 3,094 resource scope rules, and 525 perturbation cases.

## 7.3 Empirical Findings

### 7.3.1 Completion-Safety Misalignment

The central finding is that task completion and safety compliance are clearly misaligned. Under the OpenClaw setting, Gemini 3.1 Pro does not achieve the strongest task completion (TCR) but obtains the highest overall score due to its strongest protocol-safety performance. In contrast, Claude Opus 4.6 achieves a higher TCR but notably weaker safety metrics[^harness-audit].

| Model | SAR (tool) | SAR (resource) | SAR (info flow) | TCR | Overall |
|-------|------------|----------------|-----------------|-----|---------|
| Gemini 3.1 Pro | 0.74 | 0.57 | 0.66 | 0.50 | 0.32 |
| ChatGPT-5.4 | 0.61 | 0.43 | 0.51 | 0.51 | 0.25 |
| Claude Opus 4.6 | 0.38 | 0.16 | 0.35 | 0.69 | 0.18 |
| Codex (ChatGPT-5.4) | 0.38 | 0.12 | 0.35 | 0.69 | 0.16 |

Even the best-performing system (Gemini 3.1 Pro) achieves only 0.32 overall, indicating substantial room for improvement.

### 7.3.2 Resource Access Dominates Violations

Across most configurations, resource access safety is substantially weaker than tool-call safety and information-flow safety. Agents usually do not fail by invoking obviously inappropriate tools; instead, they select seemingly reasonable tools but apply them to incorrect, irrelevant, or unauthorized resources. This pattern suggests that fine-grained resource scoping—not coarse tool permissions—is the critical safety mechanism.

### 7.3.3 Multi-Agent Risk Expansion

Multi-agent configurations introduce explicit communication channels that single-agent benchmarks miss. Role-typed teams with delegated permissions create combinatorial complexity: 69 unique role templates across 24 scenarios yield 4.6 participating components per task on average. Information-flow violations—where an agent discloses data to another agent lacking authorization—are unique to multi-agent settings and cannot be detected by single-agent audits.

### 7.3.4 Perturbation Fragility

Systems are generally fragile under perturbations. Indirect injection causes the largest performance drop, suggesting that agents are easily affected by hidden instructions in task evidence or tool-returned content. Although some systems are more stable against backend anomalies, their perturbation performance remains clearly separated from normal task completion.

## 7.4 Hidden Audit Artifacts Design

A central design choice of HarnessAudit is that all evaluation evidence is collected from channels that agents cannot manipulate or anticipate. During setup, hidden audit artifacts (completion checkpoints, policy rules, violation taxonomies) are derived from the task specification but remain invisible during execution. After termination, these artifacts are combined with collected evidence (tool calls, resource accesses, inter-component messages) to score the trajectory. This design prevents agents from gaming the evaluation by optimizing for observable metrics while violating hidden constraints.

## 7.5 Implications for Harness Design

The HarnessAudit findings impose hard constraints on harness engineering. First, permission policies must be scoped at the resource level, not just the tool level. Second, information-flow constraints must be explicit in multi-agent configurations. Third, trajectory-level auditing must be continuous, not just terminal-state verification. Fourth, perturbation testing must be standard, not optional. Harnesses that optimize only for task completion without satisfying these constraints are unsafe for deployment regardless of their capability scores.

[^harness-audit]: Auditing Agent Harness Safety. arXiv:2605.14271. 2026-05-14. https://arxiv.org/abs/2605.14271
# 8. Industry and Community Landscape

While the academic papers establish rigorous foundations, industry practice and community resources reveal how harness engineering is being operationalized at scale. The convergence of corporate investment, open-source tooling, and community knowledge-sharing suggests that harness engineering is transitioning from research curiosity to engineering discipline.

## 8.1 OpenAI's Agent Experiment

OpenAI conducted a five-month internal experiment in which a team developed and deployed a software application without writing a single line of code themselves[^industry]. All code, application logic, tests, documentation, and monitoring were generated by an internal agent tool. The team estimated they needed only one-tenth of the time required for manual development, producing over one million lines of code distributed across infrastructure, application logic, documentation, developer tools, and the tooling itself.

The central question the team asked was not "How do I write working code quickly?" but "What environment is needed to achieve this goal with AI agents?" This reframing—from optimizing individual interactions to designing entire execution environments—epitomizes the harness engineering mindset. The experiment demonstrates that harness engineering is not merely a research abstraction but a practical methodology capable of order-of-magnitude productivity improvements.

## 8.2 Framework Taxonomy

OpenAI's framework divides harness engineering into three categories[^industry]:

| Category | Description | Examples |
|----------|-------------|----------|
| Context Engineering | Structured environments, RAG, documentation hierarchies | Structured filesystems, knowledge bases |
| Architectural Constraints | Runtime dependency rules, permission boundaries, sandboxing | Network policies, resource quotas |
| Entropy Management | Self-healing loops, reasoning sandwich layers, error recovery | Retry logic, fallback strategies, checkpointing |

This taxonomy aligns with the academic decomposition: context engineering maps to prompts and skills; architectural constraints map to orchestration logic and permission policies; entropy management maps to middleware and recovery mechanisms.

## 8.3 Community Resources

The research community has begun systematizing harness engineering knowledge through curated repositories and protocols:

- **RUCAIBox/awesome-agent-harness**: The official repository for "Agent Systems with Harness Engineering," cataloging 50+ papers across environment perception, context management, agentic training, and evaluation. The repository is organized by harness component (state representation, context updating, tool use, environment construction) and includes papers from ICLR, NeurIPS, ICML, ACL, and EMNLP.
- **Model Context Protocol (MCP)**: Anthropic's standardized protocol for connecting LLMs to external data sources and tools, enabling interoperability across harness implementations.
- **LangChain Blog**: "The Anatomy of an Agent Harness" (Trivedy, 2026) provides a practitioner-oriented decomposition of harness components.

## 8.4 Enterprise Tooling

Commercial platforms are emerging to operationalize harness engineering:

| Platform | Focus | Licensing |
|----------|-------|-----------|
| Harness.io (AI DevOps) | Conversational troubleshooting, automated root cause analysis | Enterprise tier with governance/RBAC |
| E2B | Managed sandbox environments for code execution | Hosted with per-usage pricing |
| Daytona | Development environment management | Managed with team collaboration features |
| Modal | Serverless compute for ML workloads | Per-second pricing |

The cost analysis from Orchard (Chapter 6) suggests that managed services may be suitable for prototyping but become prohibitively expensive at scale. For research-scale agent training (128 parallel sandboxes over 240 hours), self-hosted Kubernetes reduces cost by 10×.

## 8.5 Implications

The industry and community landscape reveals three trends. First, harness engineering is being recognized as a distinct competency requiring specialized expertise, not merely an extension of prompt engineering or DevOps. Second, the ecosystem is bifurcating between managed services (convenient but expensive) and self-hosted infrastructure (cheap but requiring expertise). Third, standardization efforts (MCP, awesome-agent-harness) are beginning to emerge but remain fragmented. The academic community's formal frameworks (Chapter 2) provide the conceptual foundation for these practical developments, but significant gaps remain between theory and practice.

[^industry]: Harness Engineering: The System Architecture That Makes AI Agents Productive. MoreThanDigital. 2026-05-22. https://morethandigital.info/en/harness-engineering-the-system-architecture-that-makes-ai-agents-productive/
# 9. Synthesis and Strategic Implications

The eight papers reviewed in this report collectively establish harness engineering as a mature, multi-faceted research discipline with immediate practical relevance. This chapter synthesizes cross-cutting themes, identifies open research questions, and offers actionable recommendations for practitioners.

## 9.1 Cross-Cutting Themes

### 9.1.1 Harness as Optimization Target, Not Implementation Detail

The most significant conceptual advance is the formalization of Agent = Model + Harness as a decomposition with independent, optimizable components. This is not merely a reframing—it has measurable consequences. Harness-Bench shows a 23.8-point score gap between harness configurations under identical model and task conditions. Life-Harness demonstrates that a base model can outperform its specialized derivative when paired with a better harness. RHO achieves +19% on SWE-Bench Pro without modifying model weights. These results establish that harness optimization is a legitimate alternative to model training, not merely a preprocessing step.

### 9.1.2 Runtime Adaptation as Model Training Alternative

Three independent lines of evidence support this claim. First, Life-Harness's 88.5% average relative improvement across 18 models without weight updates. Second, the Interplay paper's finding that harness-aware post-training outperforms post-hoc harness application by 20+ points. Third, RHO's self-supervised optimization achieving results comparable to validation-feedback methods. Together, these establish that the model–environment boundary is a high-leverage optimization surface that has been systematically underinvested relative to model weights.

### 9.1.3 Evaluation Fragmentation as Blocking Factor

The evaluation infrastructure remains fragmented across capability (Harness-Bench), safety (HarnessAudit), evolution dynamics (SEAGym), and infrastructure (Orchard). No unified protocol enables cross-domain comparison of harness designs. This fragmentation is not merely an inconvenience—it prevents the accumulation of shared knowledge about which harness designs generalize across tasks, which safety mechanisms are effective, and which evolution strategies are reliable.

### 9.1.4 Safety-Capability Misalignment as Critical Risk

HarnessAudit's finding that the best-performing system achieves only 0.32 overall safety score, with resource access violations dominating failure profiles, is a wake-up call. The multiplicative scoring framework (Security × Completion × Process) correctly encodes the insight that unsafe execution is not compensated by task completion. Yet current benchmarks and leaderboards overwhelmingly emphasize capability over safety, creating perverse incentives for harness designs that optimize for visible metrics while violating hidden constraints.

## 9.2 Open Research Questions

| Question | Current State | Priority |
|----------|--------------|----------|
| Can meta-evolution blueprints generalize to unseen tasks? | Theoretical framework only (The Last Harness) | High |
| Does Life-Harness extend to stochastic environments? | Evaluated only on deterministic benchmarks | High |
| Can harness and model parameters be jointly optimized? | No published work | High |
| What is the cross-benchmark transfer of harness designs? | No unified protocol exists | Medium |
| How do safety mechanisms affect capability? | Trade-off largely uncharacterized | High |
| Can cold-start harness optimization work without past trajectories? | RHO requires trajectory corpus | Medium |
| What are the convergence guarantees for harness evolution loops? | No theoretical analysis | Medium |

## 9.3 Recommendations for Practitioners

### 9.3.1 Report Results at Model–Harness Configuration Level

Agent performance should be reported as a property of a model embedded in an execution system, not as a property of the base model alone. This requires documenting: the harness name and version, tool set, permission policies, context management strategy, and recovery mechanisms. Without this information, scores are not reproducible or comparable.

### 9.3.2 Invest in Harness Engineering Before Model Fine-Tuning

For resource-constrained deployments, the evidence suggests that harness engineering may deliver higher return on investment than model fine-tuning. Life-Harness achieves 88.5% relative improvement without compute-intensive training. RHO achieves +19% on SWE-Bench Pro without labeled validation data. The Interplay paper shows that harness choice can outweigh model capacity (Qwen2.5-3B with h-high outperforms Qwen2.5-7B with h-low). These results suggest a prioritization: optimize the harness first, then consider model updates.

### 9.3.3 Adopt Self-Hosted Environment Infrastructure for Scale

Orchard's cost analysis demonstrates that managed sandbox services (E2B, Daytona) cost 10× more than self-hosted Kubernetes for research-scale workloads. At 128 parallel sandboxes over 240 hours, the difference is $673 vs. $7,078. For organizations running large-scale agent training or evaluation, self-hosted infrastructure is essential. The prerequisite is Kubernetes expertise, which may require upfront investment but pays dividends in cost and control.

### 9.3.4 Implement Snapshot-Level Diagnostics for Harness Evolution

SEAGym's replay diagnostics reveal that intermediate harness snapshots can regress catastrophically (6/80 tasks after epoch 4) before recovering. Final-epoch evaluation would miss this regression entirely. Safe harness evolution requires: (1) saving snapshots at regular intervals, (2) evaluating each snapshot on held-out validation and replay sets, (3) implementing rollback mechanisms to revert to prior snapshots when regression is detected, and (4) tracking cost metrics (tokens, wall-clock time) per snapshot to detect efficiency degradation.

### 9.3.5 Jointly Optimize Capability and Safety

HarnessAudit's multiplicative scoring framework (Security × Completion × Process) provides a template for joint optimization. Harness designs should be evaluated on both capability and safety metrics from the outset, not retrofitted for safety after capability optimization. This requires: (1) defining explicit permission policies and information-flow constraints, (2) auditing complete trajectories rather than terminal states, (3) testing under perturbations (indirect injection, ambiguous goals, runtime errors), and (4) rejecting harness configurations that violate safety constraints regardless of capability scores.

## 9.4 Looking Forward

The integration of three threads represents the most promising near-term direction. First, The Last Harness's Meta-Evolution Loop provides a conceptual framework for learning how to evolve harnesses. Second, SEAGym provides the evaluation environment for measuring such meta-learning. Third, RHO provides a practical inner-loop optimizer that could fit within the meta-evolution framework. A combined system—meta-evolution blueprint + SEAGym evaluation + RHO inner-loop optimization—could enable zero-shot harness adaptation to novel domains, eliminating the need for domain-specific human engineering entirely.

This vision is not yet realized. The Meta-Evolution Loop lacks empirical validation. SEAGym has been evaluated on only two benchmarks. RHO requires a corpus of past trajectories. But the pieces are in place, and the trajectory of the field suggests that automated harness engineering—harness engineering without harness engineers—is the natural endpoint of current research.
