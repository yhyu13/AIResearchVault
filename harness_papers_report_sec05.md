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
