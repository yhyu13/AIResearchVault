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
