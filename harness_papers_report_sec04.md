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
