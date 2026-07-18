# LLM Tool Use, MCP, and Agent Infrastructure: 2025–2026 Research Brief

> **Topic**: LLM Tool Use / Model Context Protocol (MCP) / Agent Infrastructure Ecosystem  
> **Search Date**: 2026-07-18  
> **Sources**: arXiv, AAAI, NeurIPS, official specification changelogs, vendor engineering blogs, production benchmarks  
> **Coverage**: 6 sub-domains — MCP ecosystem · evaluation & training · orchestration frameworks · vector DB & embedding · inference engines · skill libraries & automatic tool generation

---

## 1. The MCP Ecosystem: Primitives, Spec Evolution, Adoption, and the Security Backlash

### 1.1 Core Primitives (Precise Definitions)

MCP (Model Context Protocol) exposes a host–client–server JSON-RPC architecture with the following primitives:

- **Tools** — model-controlled executable functions. The server declares a name, description, and JSON Schema for inputs; the *model* decides when to invoke them (analogous to function calling, but server-side supplied).
- **Resources** — application-controlled read-only data (files, DB rows, API responses) addressed by URIs; the *application/user*, not the model, decides what enters context.
- **Prompts** — user-controlled reusable prompt templates with typed arguments, exposed as first-class slash-command-like objects.
- **Roots** — client-declared filesystem/workspace boundaries (URIs) that tell the server what it may legitimately operate on.
- **Sampling** — the inverse direction: a *server* may request an LLM completion from the client, keeping API keys and model choice on the host side.
- **Elicitation** — a server-initiated request for structured user input mid-interaction, so tools can ask clarifying questions with a schema-constrained form rather than free text.

### 1.2 Spec Version Evolution

| Date | Highlights |
|------|-----------|
| **2025-03-26** | Streamable HTTP transport (replacing HTTP+SSE), OAuth 2.1 authorization framework, JSON-RPC batching |
| **2025-06-18** | Structured tool output (`outputSchema`), elicitation, resource links in tool results, Resource Indicators (RFC 8707) |
| **2025-11-25** | **Tasks (SEP-1686)** — async long-running task abstraction with status polling; **CIMD** (Client ID Metadata Documents) to fix OAuth dynamic client registration at scale; **XAA** (cross-app access / enterprise delegation extensions) |

### 1.3 Official Registry

The **official MCP Registry** ("metaregistry") entered public preview in **2025-09** as a federated index of MCP servers, with its **API frozen at v0.1**. It functions as upstream metadata aggregation; downstream marketplaces (Docker, GitHub, vendor catalogs) mirror from it.

### 1.4 Adoption Timeline

- **OpenAI**: adopted MCP across Agents SDK / ChatGPT desktop — **2025-03**
- **Google** (Gemini / DeepMind): — **2025-04**
- **Microsoft** (Copilot Studio, Windows integration): — **2025-05**
- **AWS**: — **2025-07**
- Python + TypeScript SDKs: **~97 million monthly downloads** combined; `modelcontextprotocol/servers` repo: **~82k stars**

### 1.5 Headwinds

- **Perplexity's CTO publicly deprecated MCP** for internal use, arguing token/round-trip overhead outweighs standardization benefits in a vertically integrated stack.
- Measured **context-injection cost ~55k tokens** for a typical multi-server setup (tool schemas dominate the prompt before any work begins) — the "schema bloat" argument for code-mode / progressive-disclosure alternatives.

### 1.6 Security Attack Surface

- **Tool Poisoning Attack (TPA)**: malicious instructions hidden in tool descriptions are injected into the model's context at registration time.
- **MCPTox (AAAI 2026)**: benchmark of poisoned MCP servers; **o1-mini attack success rate 72.8%** — frontier reasoning does not confer robustness.
- **Rug pull / tool shadowing**: a server mutates tool definitions post-approval, or a second server registers a same-named tool to intercept calls.
- **ETDI (arXiv:2506.01333)**: proposed mitigation — Enhanced Tool Definition Interface with signed, immutable tool definitions and deployment-time integrity checks.
- **postmark-mcp backdoor**: real-world npm supply-chain incident; a compromised MCP server package exfiltrated email data.
- **mcp-remote CVE-2025-6514**: remote code execution in the popular OAuth bridge.
- **OWASP MCP Top 10**: community-curated vulnerability taxonomy formalizing these classes.

### 1.7 MCP vs. Function Calling

Function calling remains the per-vendor in-API mechanism (schema → arguments → result). **MCP is a standardized supply layer**: it standardizes how tools are *discovered, described, and hosted*, not how the model emits calls. They compose — hosts typically bridge MCP tools into their native function-calling interface — which is why adoption converged rather than competed.

---

## 2. Evaluation & Training: BFCL, τ-bench, Synthetic Data, and RL Paradigms

### 2.1 BFCL v3 / v4 (Berkeley Function Calling Leaderboard)

- **Dual judging**: *AST eval* (structural match of function name + parameters against ground truth) plus *executable eval* (actually running calls against sandboxed APIs).
- **v4 weighting**: agentic categories **40%** + multi-turn **30%** — the leaderboard deliberately de-emphasizes static single-call accuracy.
- **2026-07 snapshot**: Qwen3.7 Max **75.0** overall. Stanford AI Index 2026 reports Claude Opus 4.5 at **77.5%** — note this discrepancy is due to **snapshot timing and evaluation mode differences** (different BFCL versions / agentic-vs-AST mode mixes), not a contradiction.
- Systematic finding: **multi-turn scores run 5–10 points below single-turn** for the same model — state tracking and error recovery are the bottleneck.

### 2.2 τ-bench and τ²-bench

- **τ-bench (arXiv:2406.12045)**: user-simulator + agent in retail/airline domains; success = **exact match of final database state**, no LLM-judge. **pass^k** metric measures reliability: probability all of k independent runs succeed. GPT-4o on retail: **pass^1 ≈ 50%**, but **pass^8 < 25%** — reliability collapses under repetition even when single-run accuracy looks acceptable.
- **τ²-bench (arXiv:2506.07982)**: adds a telecom domain with agent-controlled shared state and user-side actions. Telecom has since **saturated at 99%+** for frontier models; **discriminative power has shifted back to retail**.

### 2.3 ToolACE Series (Synthetic Tool-Learning Data)

- **ToolACE (arXiv:2409.00920)**: TSS (Tool Self-evolution Synthesis) pipeline generating **26,507 APIs** with diverse tool-use dialogues via multi-agent collaboration.
- **ToolACE-R (arXiv:2504.01400)**: retrieval-aware variant — trains models to select tools from large candidate pools rather than fixed shortlists.
- **ToolACE-MT (arXiv:2508.12685)**: multi-turn extension with iterative self-critique; **reduces LLM calls in data generation by 32%** while maintaining quality.

### 2.4 RL for Tool Use: ToolRL and the Converging Paradigm

- **ToolRL (arXiv:2504.13958, NeurIPS 2025)**: systematic study of reward design. Reward decomposed into *format* + *correctness*, with correctness scored by **optimal matching** of predicted vs. ground-truth calls:

$$R_{correct} = \frac{6 \cdot R_{max}}{S_{max}} - 3$$

  where $R_{max}$ is the maximal matching score and $S_{max}$ its normalization bound. **GRPO beats SFT by ~+15%**; on BFCL-v3 the RL model reaches **52.98% vs. 45.71%** for the SFT baseline.
- **ARTIST (arXiv:2505.01441)**: agentic RL integrating tool use directly into multi-turn reasoning rollouts; together with **ToRL / ReTool / OTC** it forms a lineage that has **converged on the paradigm: SFT cold-start → GRPO/PPO with outcome + format rewards**.

---

## 3. Orchestration Frameworks: Consolidation and Production Hardening

### 3.1 LangGraph 1.0 (2025-10-17)

- Execution model: **super-step / Pregel-inspired BSP** — nodes run in parallel within a super-step, state updates applied at barriers.
- **Checkpointer-based durable execution**: every super-step persists state, enabling crash recovery, time travel, and long-running agents.
- **interrupt()**: first-class human-in-the-loop — pauses the graph, persists state, resumes from the same point with human input.
- **Middleware**: three hooks (`before_model`, `modify_model_request`, `after_model`) for cross-cutting concerns (PII redaction, summarization, guardrails) without touching node logic.
- Production adoption: **Klarna, Uber, LinkedIn**. Counter-signal: **Grid Dynamics migrated off LangGraph to a two-layer Temporal architecture**, citing the framework's leaky abstraction for truly durable long-horizon workflows.

### 3.2 LlamaIndex Workflows 1.0 (2025-06-30)

- **Event-driven `@step` model**: steps subscribe to event types; the runtime builds the graph implicitly from event flow.
- `ctx.collect_events` for fan-out/fan-in synchronization; `Context[State]` for typed shared state across steps. Minimalist compared to LangGraph — closest to the data layer (RAG) it grew from.

### 3.3 AutoGen → Maintenance Mode; AG2; Microsoft Agent Framework

- **AutoGen entered maintenance mode**; community forked **AG2**, now pursuing a ground-up **Beta rewrite**.
- **Microsoft Agent Framework** (successor unifying AutoGen + Semantic Kernel) reached **GA 2026-04** — Microsoft consolidated rather than maintained two stacks.

### 3.4 CrewAI

- Role-based paradigm: agents defined by **(role, goal, backstory)** triple; fast to prototype.
- Measured token overhead is real: identical task burned **1432 tokens (CrewAI) vs 1288 (LangGraph)** — the persona scaffolding is not free.

### 3.5 OpenAI Agents SDK

- Lightweight: **handoff implemented as a tool call** (the routing model emits a `transfer_to_X` call), tools are plain decorated functions, guardrails as input/output validators. **No built-in persistence** — you bring your own checkpointer, a deliberate minimal-core stance.

### 3.6 Google ADK

- **Hierarchical agent tree** (parent orchestrates sub-agents), **A2A protocol native** for cross-vendor agent interop, SDKs in **four languages** (Python, Java, Go, TypeScript). Best fit for GCP-anchored multi-agent systems.

### 3.7 Comparison & Selection

| Framework | Model | Persistence | HITL | Best fit |
|-----------|-------|-------------|------|----------|
| LangGraph 1.0 | Pregel super-steps | Checkpointer (built-in) | interrupt() | Complex stateful production agents |
| LlamaIndex Workflows | Event-driven steps | Via Context | Events | RAG-centric pipelines |
| MS Agent Framework | AutoGen+SK unified | Yes | Yes | Microsoft ecosystem |
| CrewAI | Role/crew metaphor | Limited | Basic | Rapid prototyping |
| OpenAI Agents SDK | Handoff-as-tool | None built-in | Manual | OpenAI-native lightweight apps |
| Google ADK | Agent tree + A2A | Yes | Yes | GCP, multi-vendor interop |

Selection rule: durability requirements first (LangGraph/Temporal-style), ecosystem lock-in second, prototyping speed third.

---

## 4. Vector DB & Embedding: Benchmark Protocols, Model Rankings, Hybrid Retrieval

### 4.1 Vector Database Benchmarks

- **pgvectorscale** on 50M vectors × 1536d at **99% recall: 471 QPS vs. Qdrant's 41 QPS** (~11×) — PostgreSQL is back in contention for large-scale ANN.
- **Qdrant** retains differentiation on **filtered ANN**: its query planner chooses between payload-index-first vs. HNSW-first strategies per query cardinality, which matters for heavy metadata filtering.
- **HNSW vs. DiskANN** watershed: HNSW wins when the index fits RAM; DiskANN wins beyond memory scale. 
- **Correct benchmark protocol**: fix recall (e.g., 99%), *then* compare QPS / p99 latency. Comparing raw QPS at unspecified recall is meaningless — recall and throughput trade on the same curve.

### 4.2 Embedding Models

- **Qwen3-Embedding-8B: MTEB(Multilingual) 70.58**, surpassing **Gemini Embedding (68.32)** and **OpenAI text-embedding-3-large (64.52)** — open weights now lead the multilingual leaderboard.
- **jina-embeddings-v3**: Multi-LoRA task adapters, **65.52**; **jina-v4** moves to **late interaction** (ColBERT-style multi-vector).
- **BGE-M3**: tri-modal output (dense + sparse + multi-vector) in one model, **MIT license**.
- **MRL (Matryoshka Representation Learning)** is now standard — truncate dimensions to trade accuracy for storage/latency without retraining.
- **Economics**: embedding cost differences across providers reach **~26×** per million tokens — model choice is a budget decision, not just an accuracy one.

### 4.3 Hybrid Retrieval & Reranking

- Standard recipe: **BM25 + dense + RRF**, with RRF score $= \sum_i \frac{1}{k + rank_i}$, **k = 60**.
- **Cross-encoder reranker** on top: typical **+5~15 nDCG@10**; Cohere Rerank v4 Pro reports **+17.2pp** on enterprise search suites.
- Strong open rerankers: **bge-reranker-v2-m3**; **Qwen3-Reranker-8B (CMTEB-R 77.45)**.

---

## 5. Inference Engines: vLLM V1, Speculative Decoding, PD Disaggregation

### 5.1 vLLM V1

- **Multi-process architecture** (separate API / scheduler / executor processes), **chunked prefill on by default**, PagedAttention with **block size 16**, **~1.7× throughput** vs. V0; **~85k GitHub stars**.

### 5.2 Speculative Decoding Under Load

- **arXiv:2510.22876**: speedup from speculative decoding **collapses at high concurrency** — EAGLE's speedup degrades **1.73× → 1.21× at batch 128**, because **verification consumes 42–95%** of compute once the GPU is saturated. Speculative decoding is a *latency* tool for low-batch regimes, not a throughput tool.

### 5.3 PD Disaggregation

- Splitting prefill and decode onto separate GPU pools: **RTP-LLM on Qwen3-Coder-480B reports TTFT improvement of 4.7–5.3×** — the strongest current lever for long-prompt agentic workloads.

### 5.4 Engine Positioning

- **SGLang**: **RadixAttention** — radix-tree prefix reuse across requests; best-in-class for **agentic workloads** (shared system prompts, multi-turn re-use); benchmarked **52.3K input tok/s on 96 GPUs**.
- **TensorRT-LLM 1.0**: **PyTorch-native refactor**; **broadest speculative-decoding support matrix** (Medusa, EAGLE, lookahead, draft-target), but **NVIDIA lock-in**.
- **llama.cpp**: edge/consumer positioning — GGUF quantization, CPU/Metal/Vulkan backends.

### 5.5 Memory Math

- Weights (BF16): $\approx 2N$ bytes for $N$ parameters.
- KV cache per token: $\approx 2 \cdot L \cdot n_{kv} \cdot d_{head} \cdot 2\text{B}$ ($L$ = layers, $n_{kv}$ = KV heads).
- Worked example: **Qwen3-32B ≈ 1 MB/token** KV cache — long-context agentic sessions are KV-capacity-bound before they are weight-bound.

---

## 6. Skill Libraries & Automatic Tool Generation: From Voyager to Agent Skills

### 6.1 Voyager (arXiv:2305.16291)

- Minecraft agent; a **skill = executable JavaScript code**. Skills are written into a library keyed by embedding of the generated description — store pairs $(e(d(p)), p)$ where $p$ is the program.
- Retrieval: **cosine top-k with k = 5**; **iterative prompting** loop consuming three feedback types (execution errors, environment state, self-verification critique).
- Results: **3.3× more unique items, 15.3× faster tech-tree progression** vs. baselines.

### 6.2 The Mathematics of Skill Retrieval

Top-k retrieval over skill embeddings can be described as follows: the "ideal" selection distribution over skills given query $q$ is a Gibbs/softmax distribution

$$p_T(s \mid q) = \frac{\exp(\cos(q, s)/T)}{\sum_{s'} \exp(\cos(q, s')/T)},$$

whose low-temperature limit concentrates on the argmax. Top-k retrieval is a **mode-truncated approximation** of this distribution — equivalently, a cheap **importance-sampling proposal** for the full skill posterior, but applied **without importance-weight correction, hence biased**: skills outside the retrieved support have zero probability mass regardless of their true relevance. This is the formal statement of the **retrieval blind-spot problem**: the library's recall ceiling caps the agent's competence, and the bias does not vanish with more sampling.

### 6.3 Automatic Tool Makers

- **CREATOR (arXiv:2305.14318)**: separates **abstract reasoning** (tool creation) from **concrete execution** (tool use); disentangles the model's reasoning from off-the-shelf tool bias. **MATH 59.7%**, beating tool-augmented baselines.
- **LATM (arXiv:2305.17126)**: **maker–user division** — a strong model (maker) writes reusable Python tools once; a cheap model (user) calls them; a **functional cache** stores verified tools, amortizing creation cost.
- **ToolMaker (arXiv:2502.11797)**: converts raw API documentation into unit-tested tools — **$0.94 per tool, 80% test pass rate**.
- **Alita (arXiv:2505.20286)**: generalist agent that generates **MCP servers on demand** — minimal predefinitions, maximal self-evolution; the skill-library thesis ported onto the MCP substrate.

### 6.4 Anthropic Agent Skills

- Released **2025-10**, open-sourced as a standard **2025-12**. A Skill = a folder with `SKILL.md` + resources, loaded via **progressive disclosure** (three layers: metadata always in context → full SKILL.md on trigger → referenced files/scripts on demand).
- Notably replaces embedding top-k retrieval with **LLM-as-retriever**: the model reads skill *metadata* and decides what to load — sidestepping (but not solving) the retrieval blind spot of §6.2.
- **Compatible with OpenAI, Google, Cursor** — the de-facto cross-vendor skill packaging format.
- Security risk documented in **arXiv:2601.10338**: skill files are an instruction-injection vector; unsigned third-party skills are MCP tool-poisoning's sibling.

### 6.5 Trend Conclusion

The frontier has moved from "can agents make tools" (solved: CREATOR/LATM/ToolMaker/Alita) to **"what breaks at scale"**: once libraries hold thousands of tools/skills, the bottleneck is **retrieval precision** (the biased top-k problem) and **security governance** (poisoned skills/tools). Expect the next wave of work on skill-index structure, verified skill signing, and retrieval-aware library organization.

---

*Brief compiled 2026-07-18. Series: k1 Agent Harness (2026-07-03) → k2 Agent Memory (2026-07-14) → k3 Tool Use / MCP / Agent Infra (this document).*
