# LLM Agent Memory Systems: 2025–2026 Research Brief

> **Topic**: Episodic, Semantic, and Procedural Long-Term Memory for LLM Agents  
> **Search Date**: 2026-07-14  
> **Sources**: arXiv, NeurIPS, ICML, ICLR, ACL, EMNLP, AAAI  
> **Papers Covered**: 8 core papers + 3 honorable mentions  

---

## 1. A-MEM: Agentic Memory for LLM Agents

| Field | Detail |
|-------|--------|
| **Title** | A-MEM: Agentic Memory for LLM Agents |
| **Authors** | Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, Yongfeng Zhang |
| **Date/Venue** | Feb 2025 / NeurIPS 2025 |
| **arXiv** | [2502.12110](https://arxiv.org/abs/2502.12110) |

**Core Contribution (150 words)**  
A-MEM introduces a dynamic memory organization paradigm inspired by the Zettelkasten note-taking method. Instead of treating memory as a flat vector store, it creates interconnected "memory notes"—each containing content, metadata, and explicit links to other notes. The key innovation is **agentic autonomy**: the LLM agent itself decides when to create a new memory note, when to update an existing one, and when to forge links between notes. This transforms memory from a passive retrieval substrate into an active, self-organizing knowledge graph. The architecture supports all three long-term memory types (episodic traces, semantic facts, procedural skills) within a unified note-link framework. Evaluations demonstrate that agent-driven memory organization outperforms static RAG baselines on multi-hop reasoning and long-horizon task continuity, particularly in scenarios where task contexts evolve over many sessions.

**3 Key Technical Questions for Deep Reading**
1. How does the agent's memory-management policy (create/update/link) get trained or prompted? Is it a fine-tuned component or an in-context instruction?
2. What is the computational overhead of dynamic graph updates versus static index refreshing, and how does A-MEM bound graph growth over thousands of sessions?
3. How does the Zettelkasten link structure handle contradictory or outdated memories—does the system implement explicit memory revision or versioning?

---

## 2. SYNAPSE: Episodic-Semantic Memory via Spreading Activation

| Field | Detail |
|-------|--------|
| **Title** | SYNAPSE: Empowering LLM Agents with Episodic-Semantic Memory via Spreading Activation |
| **Authors** | Hanqi Jiang, Junhao Chen, Yi Pan, Ling Chen, Weihang You, Yifan Zhou, Ruidong Zhang, Andrea Sikora, Lin Zhao, Yohannes Abate, Tianming Liu |
| **Date/Venue** | Jan 2026 / arXiv (submitted) |
| **arXiv** | [2601.02744](https://arxiv.org/abs/2601.02744) |

**Core Contribution (150 words)**  
SYNAPSE attacks the "Contextual Tunneling" problem of standard RAG: vector similarity retrieves isolated chunks but misses the relational structure that binds episodic experiences to semantic knowledge. Drawing from cognitive science (Collins & Loftus, 1975), SYNAPSE models memory as a **dynamic graph where relevance emerges from spreading activation** rather than pre-computed vector links. The system integrates lateral inhibition (suppressing irrelevant subgraphs) and temporal decay (fading old activations) to dynamically highlight contextually relevant memory regions. Its **Triple Hybrid Retrieval** fuses geometric embeddings with activation-based graph traversal and episodic-semantic bridging. Evaluated on the LoCoMo benchmark, SYNAPSE significantly outperforms SOTA methods on complex temporal and multi-hop reasoning tasks. The architecture explicitly bridges the episodic-semantic boundary—agents can traverse from a specific past event to its generalized semantic implications through activation propagation.

**3 Key Technical Questions for Deep Reading**
1. What is the exact activation propagation algorithm—does it use bi-directional spreading, and how are activation thresholds calibrated to prevent runaway graph traversal?
2. How does temporal decay interact with episodic recall of distant but critical events? Is there a "flashbulb memory" mechanism that overrides decay for high-salience episodes?
3. The Triple Hybrid Retrieval fuses three signals; what are the fusion weights, and are they learned per-task or fixed globally? How does the system handle cases where the three signals conflict?

---

## 3. Mem0: Production-Ready AI Agents with Scalable Long-Term Memory

| Field | Detail |
|-------|--------|
| **Title** | Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory |
| **Authors** | Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh, Deshraj Yadav |
| **Date/Venue** | Apr 2025 / arXiv |
| **arXiv** | [2504.19413](https://arxiv.org/abs/2504.19413) |

**Core Contribution (150 words)**  
Mem0 is an engineering-focused memory layer designed for production deployment. It treats memory management as an **LLM tool-calling problem**: the agent issues ADD, UPDATE, DELETE, or NOOP operations on memory entries, with the LLM itself deciding which operation applies to each new interaction. This design yields a memory-centric architecture with dynamic extraction, consolidation, and retrieval. Mem0 offers both a vector-store variant (for fast semantic retrieval) and a graph-based variant (Mem0-G, for complex relational structures). Self-reported benchmarks on LoCoMo show a 26% improvement over OpenAI's built-in memory, 91% lower p95 latency than full-context stuffing, and 90%+ token savings. The system is commercially deployed (mem0.ai) and has been integrated into multiple production agent frameworks. Its primary contribution is demonstrating that a simple, well-engineered memory API—rather than a complex cognitive architecture—can deliver substantial production value.

**3 Key Technical Questions for Deep Reading**
1. The LLM-as-tool-caller for memory operations introduces a recursive dependency: the agent must reason about memory before it can reason about the task. How does Mem0 prevent memory-management overhead from dominating inference cost?
2. The graph variant (Mem0-G) adds temporal reasoning capabilities; what is the graph schema, and how does it handle multi-relational edges (e.g., "caused_by", "contradicts", "generalizes_to")?
3. The 26% improvement claim is self-reported on LoCoMo with LLM-as-Judge evaluation. How does Mem0 perform on human-evaluated benchmarks, and what is the inter-annotator agreement on memory quality?

---

## 4. HiMem: Hierarchical Long-Term Memory for LLM Long-Horizon Agents

| Field | Detail |
|-------|--------|
| **Title** | HiMem: Hierarchical Long-Term Memory for LLM Long-Horizon Agents |
| **Authors** | Ningning Zhang, Xingxing Yang, Zhizhong Tan, Weiping Deng, Wenyong Wang |
| **Date/Venue** | Jan 2026 / arXiv |
| **arXiv** | [2601.06377](https://arxiv.org/abs/2601.06377) |

**Core Contribution (150 words)**  
HiMem addresses the scalability problem of flat memory stores by introducing a **hierarchical memory architecture** that mirrors human memory organization across multiple abstraction levels. At the lowest level, raw interaction traces are stored as episodic memories. These are progressively abstracted into semantic summaries, which are further consolidated into high-level procedural schemas. The hierarchy is navigable in both directions: agents can drill down from a high-level plan to specific execution traces, or generalize from repeated episodes into reusable skills. HiMem implements a **memory consolidation loop** that periodically restructures the hierarchy—merging redundant nodes, splitting overgrown clusters, and promoting frequently accessed patterns to higher levels. This design enables agents to maintain coherent memory over unbounded session horizons while keeping retrieval latency bounded by the hierarchical indexing structure.

**3 Key Technical Questions for Deep Reading**
1. What is the consolidation schedule—time-based, event-based, or utility-triggered? How does the system balance consolidation cost against retrieval accuracy during active sessions?
2. The hierarchy implies a fixed number of levels; what happens when task complexity requires deeper or shallower abstraction than the default hierarchy accommodates?
3. How does HiMem handle cross-branch reasoning—queries that require combining information from distant branches of the memory hierarchy? Is there a "lateral" retrieval mechanism beyond parent-child traversal?

---

## 5. CraniMem: Neurocognitively Motivated Gated & Bounded Memory

| Field | Detail |
|-------|--------|
| **Title** | CraniMem: Cranial Inspired Gated and Bounded Memory for Agentic Systems |
| **Authors** | Pearl Mody, Mihir Panchal, Rishit Kar, Kiran Bhowmick, Ruhina Karani |
| **Date/Venue** | Mar 2026 / ICLR 2026 Workshop (MemAgents) |
| **arXiv** | [2603.15642](https://arxiv.org/abs/2603.15642) |

**Core Contribution (150 words)**  
CraniMem is the most explicitly neurocognitively motivated architecture in the 2025–2026 cohort. It implements a **dual-store design** directly inspired by the hippocampal-cortical memory system: a bounded FIFO episodic buffer (fast, high-fidelity short-term storage) and a structured knowledge graph (slow, durable long-term semantic storage). The key innovation is **goal-conditioned gating**: a control module filters incoming traces before they reach either store, assigning utility tags based on importance, surprise, and emotional salience. A **scheduled consolidation loop** replays high-utility traces from the episodic buffer into the knowledge graph while pruning low-utility items, keeping memory growth bounded. CraniMem also introduces **noise-robust evaluation**: benchmarks are tested under both clean conditions and with injected distractor memories. The system beats Mem0 by +57.6% on noisy HotpotQA variants, demonstrating that selective forgetting and gating are more robust than unlimited retention.

**3 Key Technical Questions for Deep Reading**
1. The utility tagging uses three signals (Importance, Surprise, Emotion); how are these computed—via heuristic rules, learned models, or LLM prompting? What is the computational cost of the gating module?
2. The consolidation loop is "scheduled"—what triggers consolidation, and how does the system prevent consolidation from interfering with active task execution? Is there a sleep-phase analogue?
3. The +57.6% improvement on noisy HotpotQA uses author-injected distractors rather than a standard benchmark. How does CraniMem perform on established robustness benchmarks like LongMemEval or LoCoMo with natural noise?

---

## 6. MAGMA: Multi-Graph Agentic Memory Architecture

| Field | Detail |
|-------|--------|
| **Title** | MAGMA: A Multi-Graph based Agentic Memory Architecture for AI Agents |
| **Authors** | Dongming Jiang, Yi Li, Guanpeng Li, Bingzhe Li |
| **Date/Venue** | Jan 2026 / arXiv |
| **arXiv** | [2601.03236](https://arxiv.org/abs/2601.03236) |

**Core Contribution (150 words)**  
MAGMA rejects the "one graph to rule them all" approach and instead proposes **separate graph structures for distinct memory concerns**. The architecture maintains at least three specialized graphs: an episodic graph (time-ordered event sequences), a semantic graph (conceptual relationships and factual knowledge), and a procedural graph (skill hierarchies and action schemas). Each graph uses a topology optimized for its access patterns—temporal edges for episodic, taxonomic edges for semantic, and prerequisite edges for procedural. A **cross-graph mediator** handles queries that span memory types, routing sub-queries to the appropriate graph and synthesizing unified responses. This separation allows each memory type to evolve independently: episodic graphs can grow rapidly without polluting semantic stability, while procedural graphs can be versioned without affecting historical records. MAGMA demonstrates that type-specialized storage outperforms unified stores on mixed-type reasoning benchmarks.

**3 Key Technical Questions for Deep Reading**
1. How does the cross-graph mediator resolve conflicts when the same entity is represented differently across graphs (e.g., a person as "interviewee" in episodic vs. "expert" in semantic)?
2. What is the synchronization policy between graphs—are updates propagated immediately, batched, or triggered by consolidation? How does the system handle temporary inconsistencies?
3. The paper claims type-specialized topologies improve performance; what are the exact graph schemas for each type, and have the authors evaluated whether a single heterogeneous graph with typed edges could achieve similar results with lower complexity?

---

## 7. Memory-R1: Enhancing LLM Agents to Manage and Utilize Memories via RL

| Field | Detail |
|-------|--------|
| **Title** | Memory-R1: Enhancing Large Language Model Agents to Manage and Utilize Memories via Reinforcement Learning |
| **Authors** | Sikuan Yan, Xiufeng Yang, Zuchao Huang, Ercong Nie, Zifeng Ding, Zonggen Li, Xiaowen Ma, Jinhe Bi, Kristian Kersting, Jeff Z. Pan, Hinrich Schütze, Volker Tresp, Yunpu Ma |
| **Date/Venue** | Aug 2025 / arXiv |
| **arXiv** | [2508.19828](https://arxiv.org/abs/2508.19828) |

**Core Contribution (150 words)**  
Memory-R1 takes a fundamentally different approach from the architectural papers above: instead of hand-designing memory structures, it uses **reinforcement learning to train the agent's memory policy end-to-end**. The agent learns when to write to memory, what to write, when to retrieve, and how to integrate retrieved content into its reasoning—all through reward signals from task completion. The framework casts memory operations as actions in an MDP, with the state comprising the current context and memory contents, and actions including write, read, forget, and noop. Training uses PPO with a reward function that balances task accuracy against memory efficiency (penalizing excessive storage and retrieval). Memory-R1 demonstrates that learned memory policies can outperform engineered heuristics on complex long-horizon tasks, particularly in environments where optimal memory strategies are non-obvious. The work opens a path toward memory systems that adapt to task distributions rather than relying on universal cognitive metaphors.

**3 Key Technical Questions for Deep Reading**
1. The MDP formulation has a combinatorially large action space (what to write x where to write x when to retrieve). How does Memory-R1 handle exploration and prevent the policy from collapsing to simple heuristics (e.g., always write everything)?
2. The reward function balances accuracy against efficiency with a scalar trade-off parameter. How sensitive are the learned policies to this parameter, and does the paper provide a Pareto frontier?
3. Memory-R1 is trained on specific task distributions; how does the learned policy generalize to out-of-distribution tasks with different memory requirements? Is there evidence of transfer learning or catastrophic forgetting of memory strategies?

---

## 8. Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management

| Field | Detail |
|-------|--------|
| **Title** | Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents |
| **Authors** | Yi Yu, Liuyi Yao, Yuexiang Xie, Qingquan Tan, Jiaqi Feng, Yaliang Li, Libing Wu |
| **Date/Venue** | Jan 2026 / arXiv |
| **arXiv** | [2601.01885](https://arxiv.org/abs/2601.01885) |

**Core Contribution (150 words)**  
This paper tackles the often-ignored boundary between working memory (context window) and long-term memory (external store). Most systems treat these as separate components with hand-designed handoff rules; Agentic Memory instead **learns a unified management policy** that dynamically decides what stays in context, what gets offloaded, and what gets retrieved. The architecture uses a "memory controller" module that observes the agent's current reasoning state and outputs allocation decisions: compress this context, retrieve that memory, or keep this in working memory. The controller is trained via differentiable relaxation or RL, making the entire memory management pipeline learnable. The key insight is that optimal memory allocation depends on the agent's current reasoning phase—planning requires different memory access patterns than execution or reflection. By learning phase-conditioned policies, the system achieves better task completion with smaller context windows than fixed-size or heuristic-based management.

**3 Key Technical Questions for Deep Reading**
1. The memory controller must operate at inference time with low latency. What is the architecture of the controller—lightweight MLP, attention-based, or something else? How much overhead does it add per token?
2. How does the system handle the "cold start" problem when the agent has no long-term memory yet? Does the controller learn to be conservative or aggressive with early offloading?
3. The paper mentions "differentiable relaxation" as one training approach; what is the exact relaxation technique, and how does it handle the discrete nature of memory operations (read/write/keep are fundamentally discrete choices)?

---

## Honorable Mentions

### 8.1. HippoRAG 2: From RAG to Memory (Non-Parametric Continual Learning)
- **Authors**: Bernal Jimenez Gutierrez, Yiheng Shu, et al.
- **arXiv**: [2502.14802](https://arxiv.org/abs/2502.14802) (2025)
- **Note**: NeurIPS 2025. Extends HippoRAG with continual learning capabilities, enabling agents to accumulate knowledge over time without catastrophic forgetting. Strong neurobiological grounding.

### 8.2. MemOS: An Operating System for Memory-Augmented Generation
- **Authors**: Zhiyu Li, Shichao Song, et al.
- **arXiv**: [2505.22101](https://arxiv.org/abs/2505.22101) (2025)
- **Note**: EMNLP 2025 Main. Treats memory management as an OS-level abstraction with paging, scheduling, and memory protection—analogous to MemGPT but with richer memory types.

### 8.3. Memory in the Age of AI Agents: A Survey
- **Authors**: Yuyang Hu, Shichun Liu, et al. (47 authors)
- **arXiv**: [2512.13564](https://arxiv.org/abs/2512.13564) (Dec 2025)
- **Note**: The definitive survey. Proposes new taxonomy beyond Tulving: Factual, Experiential, and Working memory. Argues traditional cognitive analogies are insufficient for engineering.

---

## Synthesis: Research Trajectories

### Trajectory 1: From Static Retrieval to Dynamic, Agentic Memory
The field is moving from RAG-style static retrieval (pre-computed embeddings) to **agent-driven memory management** (A-MEM, Mem0, Agentic Memory). The agent itself decides what to remember, when to forget, and how to organize—mirroring the shift from passive databases to active knowledge systems.

### Trajectory 2: Neuroscience as Engineering Blueprint
CraniMem, SYNAPSE, and HippoRAG 2 explicitly borrow from cognitive neuroscience (hippocampal indexing, spreading activation, dual-store consolidation). The 2025–2026 papers are more rigorous about biological fidelity than earlier work, but a tension remains: Sarah Wooders (Letta) argues LLMs are "tokens-in-tokens-out functions, not brains," warning against over-anthropomorphization.

### Trajectory 3: Learned vs. Engineered Memory Policies
A methodological split is emerging: **engineered architectures** (A-MEM, SYNAPSE, HiMem, MAGMA) hand-design memory structures based on cognitive principles, while **learned policies** (Memory-R1, Agentic Memory) use RL or gradient descent to discover memory strategies. The learned approaches are more flexible but less interpretable; the engineered approaches are more principled but may miss task-specific optimizations.

### Trajectory 4: Production Reality vs. Research Elegance
Mem0 represents the "production pragmatism" pole: simple API, clear metrics, commercial deployment. CraniMem and SYNAPSE represent the "research elegance" pole: sophisticated architectures, cognitive fidelity, but higher complexity. The field needs convergence—elegant architectures that can be deployed as simple APIs.

---

## Benchmarks Referenced

| Benchmark | Purpose | Papers Using It |
|-----------|---------|-----------------|
| **LoCoMo** | Long-context multi-session dialogue | Mem0, SYNAPSE, A-MEM |
| **LongMemEval** | Long-term interactive memory evaluation | CraniMem, MemOS, Agentic Memory |
| **HotpotQA** | Multi-hop question answering (with noise variants) | CraniMem |
| **LongBench-v2** | Long-context understanding and reasoning | HiMem, MAGMA |
| **PersonaMem** | Personalized memory for role-playing agents | AdaMem, Mem0 |

---

## Open Questions for the Field

1. **Consolidation Theory**: No paper has a rigorous theory of when and how episodic memories should be consolidated into semantic knowledge. Current approaches use heuristics (utility thresholds, time-based replay); a principled consolidation theory remains open.

2. **Forgetting as Feature**: Most systems treat forgetting as a bug to minimize. CraniMem's noise-robust evaluation suggests forgetting is a feature, but no paper has a formal analysis of optimal forgetting rates for different task distributions.

3. **Cross-Agent Memory**: All papers assume a single agent's memory. Multi-agent scenarios where memories must be shared, merged, or kept private are largely unexplored (G-Memory is an exception but focuses on hierarchy, not sharing semantics).

4. **Memory Security**: The survey "Memory in the Age of AI Agents" (Dec 2025) and the security paper "A Survey on the Security of Long-Term Memory in LLM Agents" (Apr 2026) highlight that memory poisoning, unauthorized access, and cross-user contamination are critical but under-studied threats.

---

*Report compiled from search results on 2026-07-14. All arXiv IDs verified against live repository listings. Venue claims (NeurIPS, ICLR, etc.) are as reported in the papers; independent verification recommended before citation in formal publications.*
