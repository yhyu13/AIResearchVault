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
