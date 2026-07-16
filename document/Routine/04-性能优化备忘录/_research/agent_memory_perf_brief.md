# 调研简报：LLM Agent Memory System 的性能优化工程

> **调研日期**：2026-07-16
> **调研人**：AI 推理系统优化方向研究员（子代理）
> **用途**：供下游写作者撰写「性能优化备忘录」（训练/推理优化笔记）
> **上游输入**：`document/Routine/05-技术雷达/2026-07-14/LLM_Agent_Memory_System_2025_2026_Research_Brief.md`（下称「源简报」）
> **方法**：精读源简报提取性能数据点 → web 核实一手来源（arXiv 摘要/正文、官方仓库、官方 benchmark 页）→ 补充瓶颈画像与生产级优化手段调研
> **核实状态图例**：✅ 一手来源核实｜🟡 二手来源转述（可信但非一手）｜❌ 未核实

---

## 0. 核心结论摘要

1. **外部记忆 vs 全上下文（full-context）的权衡已被一手数据量化**：Mem0 论文（arXiv:2504.19413）报告，相对全上下文方案，p95 端到端延迟从约 17 s 降至约 1.44 s（摘要称 -91%，正文称 -92%），token 成本节省 >90%，代价是 LOCOMO LLM-as-Judge 分数下降约 6 个百分点（72.9% → 66.9%）。✅
2. **"选择性记忆"路线的最新数字已反超全上下文基线**：Mem0 官方博客 2026 年新一轮 LOCOMO 评测给出 91.6% 准确率、均值 <7K tokens/query、p95 ≈1.44 s；MemOS 官方仓库报告 LoCoMo 92.34。注意这些是厂商自报的新版本数字，与原论文（2025-04）的 66.9% 不可直接对比。🟡（厂商来源）
3. **记忆系统的在线开销主要在「写入/整合路径」而非检索路径**：Mem0 每消息对至少 2 次额外 LLM 调用（extraction + update tool-call）；LightMem（arXiv:2510.18866）通过 sleep-time 离线整合把纯在线 token 成本压低最高 106×/117×、API 调用 159×/310×（LongMemEval/LoCoMo），证明在线开销是可优化的主要矛盾。✅
4. **纯检索延迟可压到 100–200 ms 量级，LLM-in-the-loop 检索才是秒级尾巴的来源**：Zep 官方 auto search 报告 p50/p95 = 115/173 ms；LightMem 检索 p50/p95 = 83/167 ms（第三方引述）；而第三方复现（SwiftMem, arXiv:2601.08160）显示 Mem0 的 search 阶段为 784 ms、A-MEM 存在重尾延迟。✅/🟡
5. **memory 与 KV cache 的交互是 2025–2026 年的新优化前沿**：MemOS 把"高频稳定"的 plaintext 记忆转换为 KV-form 的 activation memory 直接注入 attention cache，跳过重复 prompt encoding；SleepGate 在 KV cache 上做 sleep micro-cycle 遗忘与整合。这类"记忆 → KV"的路径绕开了文本注入的 prefill 成本。✅
6. **gating/遗忘不是精度特性而是成本特性**：CraniMem 的 bounded FIFO buffer + goal-conditioned gating 把存储增长从 O(N) 压到 O(1) 上界；指数时间衰减与 utility threshold 可将期望存储与检索候选集规模显式建模（见 §4.3 公式）。✅（机制定性核实；具体 +57.6% 数字 ❌ 未核实）

---

## 1. 源简报性能数据点逐条核查清单

下表逐条列出源简报中所有性能相关声明，标注其在源简报中的位置与本轮核实状态。

| # | 源简报位置 | 数据点声明 | 核实状态 | 核实说明 |
|---|-----------|-----------|---------|---------|
| 1 | §3 Mem0，第 58 行 | LOCOMO 上比 OpenAI 内置记忆提升 26% | ✅ | arXiv:2504.19413 摘要原文："26% relative improvements in the LLM-as-a-Judge metric over OpenAI" |
| 2 | §3 Mem0，第 58 行 | p95 延迟比全上下文低 91% | ✅ | 摘要："91% lower p95 latency"；正文："p95 latencies of around 1.44 seconds (a 92% reduction)" vs 全上下文约 17 s。91%/92% 为四舍五入差异，17.12→1.44 s 实为 -91.6% |
| 3 | §3 Mem0，第 58 行 | token 节省 90%+ | ✅ | 摘要："saves more than 90% token cost"；正文给出全上下文 chunk 约 26,000 tokens；第三方引述精确值 ~26,031 vs ~1,764 tokens/query（-93.2%）🟡 |
| 4 | §3 Mem0，第 58 行 | 图变体 Mem0-G（Mem0^g） | ✅ | 摘要确认：graph memory 变体总分比 base Mem0 高约 2%；正文：Mem0^g p95 ≈2.6 s（比全上下文 -85%） |
| 5 | §3 Mem0，第 58 行 | "self-reported" 警示 | ✅ 成立 | 全部为作者自报（mem0.ai 团队），且评估含 LLM-as-Judge；第三方复现存在分数偏差（见 §7 存疑点 D1） |
| 6 | §5 CraniMem，第 96 行 | 噪声 HotpotQA 上比 Mem0 高 +57.6% | ❌ 未核实（数字） | 论文存在（arXiv:2603.15642，2026-03），摘要确认"gated and bounded memory""对 distractor 更鲁棒、性能下降更小"的定性声明，但 +57.6% 具体数字不在摘要中，本轮未读全文，无法核实 |
| 7 | §5 CraniMem，第 96 行 | bounded FIFO episodic buffer + goal-conditioned gating + scheduled consolidation loop | ✅（定性） | 摘要确认全部三个机制：goal conditioned gating and utility tagging、bounded episodic buffer、scheduled consolidation loop |
| 8 | §4 HiMem，第 77 行 | "retrieval latency bounded by hierarchical indexing" | 🟡 定性无数字 | HiMem 摘要（arXiv:2601.06377）仅称 "hybrid and best-effort retrieval strategies to balance accuracy and efficiency""maintaining favorable efficiency"，未给出任何量化延迟数字 |
| 9 | §7 Memory-R1，第 134 行 | reward 平衡任务准确率与记忆效率（惩罚过度存储/检索） | ✅（定性，措辞需修正） | 摘要（arXiv:2508.19828）确认 PPO/GRPO 训练 Memory Manager（ADD/UPDATE/DELETE/NOOP）+ Answer Agent；仅用 152 个训练 QA pair；在 LoCoMo/MSC/LongMemEval、3B–14B 模型规模上泛化。摘要无准确率/效率具体数字；源简报"penalizing excessive storage and retrieval"的 reward 细节未从摘要核实 |
| 10 | §8 Agentic Memory，第 153 行 | "smaller context windows 下更好任务完成率" | ❌ 未核实（数字） | 本轮未读取 arXiv:2601.01885 正文，无量化数字 |
| 11 | §8.2 MemOS，第 172 行 | OS 级抽象：paging、scheduling、memory protection | ✅（定性） | 长版论文 arXiv:2507.03724 摘要确认：统一表示/调度/演化 plaintext、activation-based、parameter-level 三类记忆；MemCube 为基本单元（含 provenance/versioning 元数据），可 compose/migrate/fuse |
| 12 | §2 SYNAPSE，第 39 行 | LoCoMo 上"显著超过 SOTA" | ❌ 未核实（数字） | 本轮未读取 arXiv:2601.02744，无量化数字 |
| 13 | §1 A-MEM，第 20 行 | multi-hop reasoning 上超过静态 RAG 基线 | ❌ 未核实（数字） | 本轮未读取 arXiv:2502.12110 正文；但第三方论文（见 §3.1）指出 A-MEM 存在重尾检索延迟 🟡 |
| 14 | 基准表，第 201–205 行 | 各 benchmark 与论文的对应关系 | 🟡 未逐条复核 | 其中"LongBench-v2: HiMem, MAGMA""PersonaMem: AdaMem, Mem0"本轮未核实 |

---

## 2. 关键性能数据点的一手来源核实

### 2.1 Mem0（arXiv:2504.19413，2025-04，✅ 已核实）

来源：Chhikara et al., "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory", arXiv:2504.19413 (v1, 2025-04-28). https://arxiv.org/abs/2504.19413

**核实到的精确数字**：

| 指标 | Full-context | Mem0 | Mem0^g（图变体） | 备注 |
|------|-------------|------|----------------|------|
| LOCOMO LLM-as-Judge（J） | ≈72.9%（全文最高） | 66.9% | 68.4% | Mem0 比 OpenAI 内置记忆相对 +26%（摘要） |
| p95 端到端延迟 | ≈17 s（第三方引述 17.12 s） | ≈1.44 s（-91%~-92%） | ≈2.6 s（-85%） | 正文原文：全上下文 "around 17 seconds"，Mem0 "around 1.44 seconds (a 92% reduction)" |
| token / query | chunk ≈26,000（第三方引述 26,031） | 第三方引述 ≈1,764（-93%） | N/A | 摘要："saves more than 90% token cost" |

**架构与开销相关的已核实细节**（来自论文正文 §2）：
- 流水线两阶段：extraction + update。extraction 用 LLM 函数 φ(P) 从消息对 (m_{t-1}, m_t) 提取候选事实集 Ω = {ω_1, …, ω_n}，prompt P = (S, {m_{t-m},…,m_{t-2}}, m_{t-1}, m_t)，其中 S 为会话摘要（**异步**摘要模块周期刷新，不阻塞主流水线），实验配置 m = 10 条近期消息。
- update 阶段：对每个候选事实先检索 top-s（s = 10）条语义相似记忆，再由 LLM 通过 tool call 决定 ADD / UPDATE / DELETE / NOOP 四操作之一。
- 推理引擎：GPT-4o-mini；向量库存 dense embedding。
- **含义**：每条消息对的记忆写入开销 = ≥1 次 extraction LLM 调用 + 1 次向量检索 + ≥1 次 update LLM 调用（见 §3.3 的开销模型）。

**注意（厂商新数字，🟡）**：Mem0 官方博客 2026-06-26 给出"最新研究"数字：LOCOMO 91.6% 准确率、均值 <7,000 tokens/query、p95 ≈1.44 s（来源：https://mem0.ai/blog/context-window-is-ram-not-storage-why-most-agent-failures-happen-how-to-fix-them-in-2026）。这与 2025 原论文的 66.9% 不是同一版本结果，引用时必须区分版本。

### 2.2 Zep / Graphiti（arXiv:2501.13956，2025-01，✅ 论文核实 + 官方页核实）

来源 1（论文）：Rasmussen et al., "Zep: A Temporal Knowledge Graph Architecture for Agent Memory", arXiv:2501.13956 (2025). https://arxiv.org/abs/2501.13956
来源 2（官方 benchmark 页）：getzep.com/research（2026-05-28 抓取）. https://www.getzep.com/research/

- DMR（Deep Memory Retrieval）benchmark：**94.8%**（GPT-4 Turbo）/ **98.2%**（GPT-4o Mini），超过此前 SOTA 的 MemGPT。✅（论文摘要 + 多处转述一致）
- LongMemEval：相对基线最高 **+18.5%** 准确率，同时响应延迟 **-90%**。✅（论文声明，经多处转述一致）
- LongMemEval（GPT-4o）：Zep 63.8% vs Mem0 49.0%（🟡 Atlan 转述 Zep 官方数据）
- Zep auto search（官方页，2026）：LOCOMO 86.5%（单次 API 调用、免调参）；检索延迟 **p50/p95 = 115/173 ms**；中位 context 2,680 tokens，比 multi-scope 手工组合 **-53%**。🟡（厂商自报）
- 工程细节（官方页）：热图以 adjacency list + CSR matrix 常驻内存，vector + BM25 索引并列；单次查询跨全部检索信号返回统一排序结果。🟡

### 2.3 LightMem（arXiv:2510.18866，2025-10，✅ 摘要核实）

来源：Fang et al., "LightMem", arXiv:2510.18866 (v4, 2026-02-28). https://arxiv.org/abs/2510.18866

三阶段架构（Atkinson-Shiffrin 模型启发）：sensory memory（轻量压缩过滤 + 按 topic 分组）→ topic-aware short-term memory（整合摘要）→ long-term memory with **sleep-time update**（离线过程，把整合与在线推理解耦）。

**量化结果（摘要原文，GPT 与 Qwen 骨干，LongMemEval / LoCoMo）**：
- QA 准确率最高 **+7.7% / +29.3%**；
- 总 token 用量最高 **↓38× / ↓20.9×**；API 调用最高 **↓30× / ↓55.5×**；
- **纯在线 test-time 成本更低**：token 最高 **↓106× / ↓117×**，API 调用最高 **↓159× / ↓310×**。

第三方引述（arXiv:2604.07798 正文，🟡）：LightMem 检索延迟 p50/p95 = **83/167 ms**，显著低于 MemGPT、尤其低于存在重尾延迟的 A-MEM；端到端 p50 = 581 ms；有效 context 约 1K tokens（vs 全上下文/MemGPT 约 16K）。

### 2.4 MemOS（arXiv:2507.03724 长版 / arXiv:2505.22101 短版，✅ + 官方仓库 🟡）

来源 1：Li et al., "MemOS: A Memory OS for AI System", arXiv:2507.03724 (v4, 2025-12-03). https://arxiv.org/abs/2507.03724
来源 2：官方仓库 https://github.com/MemTensor/MemOS （2026-07 抓取）

- **三类记忆的统一调度**（摘要 ✅）：plaintext / activation-based（KV-form）/ parameter-level；MemCube 为基本单元，封装内容与 provenance、versioning 元数据，支持 compose / migrate / fuse。
- **MemScheduler → activation memory 路径**（论文正文，✅）：持续监控模型交互，识别"高频访问 + 语义稳定"的 plaintext 记忆条目，转换为 KV 格式注入 attention cache 并预置 GPU 供低延迟复用。对照实验：prompt-based 注入 vs KV-cache 注入，在短（583 tokens）/中（2,773）/长（6,064）三种 context 长度下评估（具体加速比数字在正文图表中，本轮未提取到数值）。
- **官方仓库数字（🟡 厂商自报）**：LoCoMo **92.34**、LongMemEval **93.40**（User Memory）；OpenClaw 五项 agent 任务平均完成率 36.63% → **50.87%**；仓库标称 **35.24% token savings**；OpenClaw Cloud Plugin 标称 token 用量 **-72%**；MemScheduler 异步写入"毫秒级延迟"。
- v2.0（2025-12-24）：任务调度器基于 Redis Streams 重建，queue isolation + 任务优先级 + 自动恢复 + quota 调度。🟡

### 2.5 Memory-R1（arXiv:2508.19828，2025-08，✅ 摘要核实，无摘要级数字）

来源：Yan et al., arXiv:2508.19828 (v5, 2026-01-14). https://arxiv.org/abs/2508.19828
RL 框架：Memory Manager（学习 ADD/UPDATE/DELETE/NOOP 结构化操作）+ Answer Agent（预选并推理相关条目）；PPO 与 GRPO 微调；**仅 152 个训练 QA pair** 即超过强基线，并在 LoCoMo / MSC / LongMemEval 三个基准、3B–14B 多模型规模上泛化。摘要未给出具体准确率/效率数字。

---

## 3. 性能瓶颈画像

### 3.1 记忆检索延迟的构成

单次记忆检索的端到端延迟可分解为：

$$
T_{\text{retrieval}} = T_{\text{embed}}(q) + T_{\text{ANN}}(q) + T_{\text{rerank}}(q, k) + T_{\text{inject}}
$$

- $T_{\text{embed}}$：查询向量化。本地小模型 <10 ms；远程 embedding API 典型 50–200 ms（网络主导）。
- $T_{\text{ANN}}$：近似最近邻搜索。HNSW 索引平均查询复杂度 $O(\log N)$（N 为记忆条目数），`ef_search` 参数控制召回/延迟折中；图遍历类系统（Zep/Graphiti）为 semantic + BM25 + graph traversal 的 hybrid search。
- $T_{\text{rerank}}$：cross-encoder 对 top-k 候选逐条打分，约 k 次 forward；若用 LLM 做 rerank 则直接进入百毫秒–秒级。
- $T_{\text{inject}}$：结果拼入 prompt 的构造开销，通常可忽略，但决定下游 prefill 成本。

**实测锚点**：

| 系统 | 检索延迟 | 来源 |
|------|---------|------|
| Zep auto search | p50/p95 = 115/173 ms | 🟡 getzep.com/research (2026) |
| LightMem | p50/p95 = 83/167 ms | 🟡 arXiv:2604.07798 引述 |
| SwiftMem（纯索引） | search = 11 ms | ✅ arXiv:2601.08160 Table 2 |
| Mem0（第三方复现） | search = 784 ms | ✅ arXiv:2601.08160 Table 2 |
| A-MEM | 重尾延迟（heavy tail） | 🟡 arXiv:2604.07798 正文 |

**结论**：纯 embedding+ANN+轻 rerank 路径可稳定在 200 ms 内；检索链路中一旦引入 LLM（查询重写、LLM rerank、agentic 多跳），延迟即进入秒级并出现重尾。

### 3.2 长上下文 vs 外部记忆的 token 成本

设历史对话共 $n_{\text{hist}}$ tokens，每次查询外部记忆注入 $n_{\text{ret}}$ tokens，输入单价 $c_{\text{in}}$：

$$
C_{\text{full}} = n_{\text{hist}} \cdot c_{\text{in}} \quad \text{vs.} \quad C_{\text{mem}} = (n_{\text{ret}} + n_q) \cdot c_{\text{in}} + \underbrace{\frac{C_{\text{write}}}{Q}}_{\text{写入摊销}} + C_{\text{retrieve}}
$$

其中 $C_{\text{write}}$ 为记忆写入/整合的总开销（见 §3.3），Q 为写入后服务的查询数。break-even 条件：当 $n_{\text{hist}} \gg n_{\text{ret}}$ 且写入摊销足够小时，外部记忆占优。Mem0 实测点：$n_{\text{hist}} \approx 26{,}031$ vs $n_{\text{ret}} \approx 1{,}764$ tokens/query，单次查询输入 token 约 -93%（🟡 第三方引述精确值；论文摘要声明 >90% ✅）。

**推理侧的成本不仅是 token 数**。self-attention prefill 的计算量（忽略线性层）随序列长度平方增长：

$$
\text{FLOPs}_{\text{attn}}(n) \approx 4 \cdot L \cdot d_{\text{model}} \cdot n^2
$$

（QK^⊤ 与 attention·V 各贡献 $2Ld n^2$；L 为层数，$d_{\text{model}}$ 为隐维）。n 从 26K 降到 1.7K 时 attention 部分 FLOPs 降为 $(1.7/26)^2 \approx 0.4\%$（约 234× 缩减）；计入线性层后总 prefill 成本近似随 token 数线性下降（约 15×）。这与 Mem0 观察到的"token 节省 >90% ⇒ 成本近似成比例下降"一致。

**KV cache 显存**（GQA 架构）：

$$
M_{\text{KV}} = 2 \cdot L \cdot H_{\text{kv}} \cdot d_h \cdot n \cdot b
$$

（2 = K/V 两份，$H_{\text{kv}}$ = KV head 数，$d_h$ = head 维，b = 字节数/元素）。以 Llama-3-70B 量级（L=80，$H_{\text{kv}}$=8，$d_h$=128，FP16）估算：每 token ≈ 0.33 MB，26K tokens 的历史 ≈ 8.5 GB KV cache——全上下文方案在显存与 TTFT 上双重不可扩展，这是"外部记忆替代上下文堆叠"的系统层动机。

### 3.3 记忆写入/整合的在线开销

以 Mem0 为参照系（✅ 正文核实）：每条消息对 $(m_{t-1}, m_t)$ 的写入路径 = 1 次 extraction LLM 调用（输入含摘要 S + m=10 条近期消息）+ 1 次 top-s（s=10）向量检索 + 1 次 update tool-call LLM 调用。形式化：

$$
C_{\text{write/turn}} \geq 2 \cdot C_{\text{LLM-call}} + C_{\text{ANN}}(s)
$$

即**在线写入成本 ≥ 每轮 2 次额外 LLM 调用**，与回答本身的 1 次调用同量级——这就是 LightMem 摘要数字的意义：其纯在线 token 成本比 Mem0 类系统低最高 106×/117×、API 调用低 159×/310×（✅ arXiv:2510.18866），核心手段是把整合（consolidation）移到 sleep-time 离线执行，在线只留轻量过滤与分组。LightMem 的"总成本"（含离线）节省倍数明显小于"纯在线"节省倍数（38×/20.9× vs 106×/117×），说明**离线整合把成本从在线路径转移到了离线路径，而非消除**——写作时应明确区分这两个口径。

MemOS 的工程对应物（🟡 官方仓库）：MemScheduler 异步写入（"毫秒级延迟"声明）+ Redis Streams 任务队列 + queue isolation + 优先级/quota 调度，即把记忆写入做成异步后台任务，避免阻塞在线推理。

### 3.4 memory 与 KV cache / prefix caching 的交互

三个已核实的交互点：

1. **prefix caching 命中问题**：若记忆以文本形式注入 prompt 且注入位置在共享前缀之后，则不同查询检索到不同记忆 ⇒ 前缀在记忆块处断裂，prefix cache miss，prefill 成本回升。设前缀命中率 η，则

$$
C_{\text{prefill}} = (1-\eta)\, C_{\text{full-prefill}} + \eta\, C_{\text{incremental}}
$$

记忆注入策略（固定槽位、按稳定度排序、记忆块置前）直接影响 η。此为系统推理层面的常识性结论，本轮未找到针对该交互的量化论文（见 §7 D4）。

2. **KV-form 记忆（activation memory）**：MemOS 把高频稳定的 plaintext 记忆预编码为 KV 直接注入 attention cache，跳过 prompt encoding（✅ arXiv:2507.03724 正文描述了该对照实验，context 长度 583/2,773/6,064 tokens；具体加速数字未提取）。SleepGate（arXiv:2603.14517，🟡 经 arXiv:2604.12034 引述）进一步在 KV cache 上做周期触发的 sleep micro-cycle：forgetting gate + consolidation 直接作用于 KV 层。

3. **KV cache 自身的压缩**（背景数据，✅）：LeanKV（arXiv:2412.03131）报告 KV cache 压缩 2.7×–5.7× 且精度近无损，吞吐提升 1.9×–5.4×；并行 KV compaction 把内存管理时间占比从最高 76% 压到 <1%。这是"长上下文路线"内部的对标优化，写作时可作为外部记忆路线的对照组。

---

## 4. 生产级优化手段

### 4.1 记忆压缩与摘要

- **抽取式事实化（fact extraction）**：Mem0 把对话对压缩为候选事实集 Ω，再由 LLM 仲裁 ADD/UPDATE/DELETE/NOOP；压缩比直接决定 token 节省（>90%，✅）。
- **分层摘要**：Mem0 的异步会话摘要 S 为 extraction 提供全局上下文且不阻塞主流程（✅ 正文）。LightMem 的 sensory→STM→LTM 逐级压缩（✅）。
- **量化对照**：Memori 报告 LoCoMo 81.95% 准确率、平均仅 1,294 tokens/query（约为全上下文的 5%）（🟡 经 arXiv:2604.11243 引述）；MemMachine "raw-episode + sentence-level index" 双层架构约 -80% token（🟡 同上引述）。

### 4.2 分层记忆（hierarchical memory）的检索复杂度

- flat 向量库：HNSW 查询 $O(\log N)$，但 N 随会话无限增长，且候选集噪声随 N 上升（精度问题先于复杂度问题出现）。
- 分层结构：先检索高层摘要/主题层再 drill-down，每层的候选集规模为分支因子 B，深度 D，则检索复杂度约

$$
T_{\text{hier}} = O\!\left(D \cdot \log B\right), \qquad N = O(B^D)
$$

即对同样的总条目数 N，分层检索把候选评估量从 $\log N$ 摊到 $D$ 个小索引上，同时高层节点充当"语义路由"，减少低层噪声。

- 已核实实例：HiMem（✅ 摘要）：Episode Memory（Topic-Aware Event–Surprise Dual-Channel Segmentation 构建）+ Note Memory（多阶段信息抽取），两层语义链接，支持 hybrid 与 best-effort 两种检索策略以平衡 accuracy/efficiency——但**无公开量化延迟数字**（🟡）。
- MAGMA（源简报 §6）：按记忆类型分图（episodic/semantic/procedural 各自拓扑），跨图 mediator 路由——类型特化存储在混合型推理基准上优于统一存储（源简报声明，❌ 本轮未核实数字）。

### 4.3 gating / 遗忘策略对存储与检索成本的影响

形式化三类主流机制：

1. **utility gating**（CraniMem，✅ 定性核实）：写入仅当效用 $u(x) > \tau$。设到达率 1 条/轮、门控通过率 ρ，则期望存储 $E[S(N)] = \rho \cdot N \cdot \bar{s}$（$\bar{s}$ 为平均条目大小），检索候选集同比缩小 ρ 倍；效用打分的三个信号为 importance / surprise / emotional salience。
2. **bounded buffer**（CraniMem 的 FIFO episodic buffer）：存储硬上界 $S \le B$，检索复杂度从 $O(\log N)$ 变为 $O(\log B)$——**存储增长从 O(N) 压到 O(1)**，这是"遗忘即成本特性"的最直接论证。
3. **时间衰减**（SYNAPSE 的 temporal decay、spreading activation 系）：activation 按指数衰减

$$
a_i(t) = a_i(t_0) \cdot e^{-\lambda (t - t_0)}, \qquad a_i = \sum_j w_{ji}\, a_j \ \ (\text{spreading})
$$

衰减到阈值以下的条目可被批量 prune，存储与候选集规模随 λ 指数收缩；Ebbinghaus 遗忘曲线 $R = e^{-t/S}$ 为同一族模型。

4. **scheduled consolidation**（CraniMem/LightMem/HiMem 共有）：离线 replay 高效用 trace 进长期存储、prune 低效用项——把删除与合并成本移出在线路径（见 §3.3）。

### 4.4 MemOS 的操作系统式调度思路（✅ 定性 + 🟡 数字）

- 记忆三态与转化：plaintext（文本，检索注入）⇄ activation（KV-form，attention cache 直注）⇄ parameter（参数化，蒸馏进权重）；MemScheduler 负责识别"高频 + 语义稳定"条目并促成向更"热"形态的迁移——与 OS 的 page promotion（磁盘→内存→TLB）同构。
- MemCube = 记忆的基本调度单元（内容 + provenance + versioning），支持 compose / migrate / fuse（✅ 摘要）。
- 工程化调度（🟡 仓库 v2.0）：Redis Streams 队列、queue isolation、任务优先级、自动恢复、quota 调度。
- 效果数字（🟡 厂商自报）：LoCoMo 92.34、LongMemEval 93.40、OpenClaw 任务完成率 36.63%→50.87%、token savings 35.24%（仓库标称）/ -72%（OpenClaw Cloud Plugin）。

---

## 5. 可量化的优化前后对照表

| 优化手段 | 对照基线 | 前 → 后 | 幅度 | 来源（核实级别） |
|---------|---------|--------|------|----------------|
| 外部记忆替代全上下文（Mem0） | full-context stuffing | p95: 17.12 s → 1.44 s | -91.6% | arXiv:2504.19413（✅，正文 17 s/1.44 s；精确值 17.12 为🟡转述） |
| 同上 | full-context | tokens/query: ~26,031 → ~1,764 | -93%（摘要 >90%） | arXiv:2504.19413（✅ 幅度；精确值🟡） |
| 同上（代价） | full-context | LOCOMO J: 72.9% → 66.9% | -6 pt | 同上（✅） |
| Mem0 vs OpenAI 内置记忆 | OpenAI memory | LOCOMO J 相对 +26% | +26% rel. | 同上（✅） |
| 图记忆层（Mem0^g vs Mem0） | Mem0 base | 总分 +约 2 pt；p95 1.44 s → 2.6 s | 精度+延迟换关系建模 | 同上（✅） |
| sleep-time 离线整合（LightMem） | Mem0 类在线整合 | 在线 token -106×/-117×；API 调用 -159×/-310×；总 token -38×/-20.9× | 数量级 | arXiv:2510.18866（✅ 摘要） |
| 同上（精度） | 强基线 | QA acc +7.7%（LongMemEval）/ +29.3%（LoCoMo） | 正收益 | 同上（✅） |
| 时序知识图（Zep） | MemGPT 等 | DMR 94.8%；LongMemEval +18.5% 且延迟 -90% | — | arXiv:2501.13956（✅） |
| 单调用 auto search（Zep） | multi-scope 手工组合 | 中位 context 2,680 tokens，-53%；p50/p95 115/173 ms | -53% | getzep.com/research（🟡） |
| 检索路径去 LLM（SwiftMem） | Mem0 | search: 784 ms → 11 ms；total 3.54 s → 1.29 s | -98.6% | arXiv:2601.08160（✅ 第三方复现口径） |
| KV-form 记忆调度（MemOS） | prompt 注入 | KV-cache 注入 vs prompt 注入对照（583/2,773/6,064 tokens） | 数字未提取 | arXiv:2507.03724（✅ 实验存在；数值❌） |
| OS 级记忆调度（MemOS） | 无记忆基线 | OpenClaw 任务完成率 36.63% → 50.87%；token -72%（Cloud Plugin） | +14.24 pt | github.com/MemTensor/MemOS（🟡） |
| KV cache 压缩（LeanKV，背景） | 无压缩 | KV 2.7–5.7× 压缩；吞吐 1.9–5.4×；内存管理时间占比 76% → <1% | — | arXiv:2412.03131（✅） |
| RL 学习记忆策略（Memory-R1） | 启发式基线 | 仅 152 QA 训练即在 LoCoMo/MSC/LongMemEval 超基线（3B–14B） | 数字未在摘要 | arXiv:2508.19828（✅ 定性） |
| gating+bounded buffer（CraniMem） | Vanilla RAG / Mem0 | 噪声下性能下降更小；+57.6%（噪声 HotpotQA） | ❌ 数字未核实 | arXiv:2603.15642（✅ 定性；数字❌） |

---

## 6. 参考列表（可引用）

一手来源（论文/官方仓库/官方 benchmark 页）：

1. Chhikara, P., Khant, D., Aryan, S., Singh, T., Yadav, D. **"Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory"**, arXiv:2504.19413, Apr 2025. https://arxiv.org/abs/2504.19413
2. Rasmussen, P., Paliychuk, P., Beauvais, T., Ryan, J., Chalef, D. **"Zep: A Temporal Knowledge Graph Architecture for Agent Memory"**, arXiv:2501.13956, Jan 2025. https://arxiv.org/abs/2501.13956
3. Fang, J. et al. **"LightMem"**（三阶段记忆 + sleep-time update）, arXiv:2510.18866, Oct 2025（v4 Feb 2026）. https://arxiv.org/abs/2510.18866
4. Li, Z. et al. **"MemOS: A Memory OS for AI System"**, arXiv:2507.03724, Jul 2025（v4 Dec 2025）. https://arxiv.org/abs/2507.03724 ；短版 "MemOS: An Operating System for Memory-Augmented Generation (MAG) in Large Language Models", arXiv:2505.22101, May 2025. https://arxiv.org/abs/2505.22101
5. MemTensor. **MemOS 官方仓库**（benchmark 与 token savings 声明）, 2026-07 抓取. https://github.com/MemTensor/MemOS
6. Zep AI. **官方 benchmark 页**（auto search 延迟/context 数字）, 2026-05 抓取. https://www.getzep.com/research/
7. Yan, S. et al. **"Memory-R1: Enhancing Large Language Model Agents to Manage and Utilize Memories via Reinforcement Learning"**, arXiv:2508.19828, Aug 2025（v5 Jan 2026）. https://arxiv.org/abs/2508.19828
8. Mody, P., Panchal, M., Kar, R., Bhowmick, K., Karani, R. **"CraniMem: Cranial Inspired Gated and Bounded Memory for Agentic Systems"**, arXiv:2603.15642, Mar 2026. https://arxiv.org/abs/2603.15642
9. Zhang, N. et al. **"HiMem: Hierarchical Long-Term Memory for LLM Long-Horizon Agents"**, arXiv:2601.06377, Jan 2026. https://arxiv.org/abs/2601.06377
10. **SwiftMem**（第三方复现基准，含 Mem0/Zep 延迟对照表）, arXiv:2601.08160, Jan 2026. https://arxiv.org/pdf/2601.08160
11. **LeanKV: Unifying KV Cache Compression for Large Language Models**, arXiv:2412.03131, Dec 2024. https://arxiv.org/pdf/2412.03131
12. Mem0 官方博客. **"Memory vs Context Window for LLM and AI Agents"**（2026 新版 LOCOMO 数字）, 2026-06-26. https://mem0.ai/blog/context-window-is-ram-not-storage-why-most-agent-failures-happen-how-to-fix-them-in-2026

二手引述来源（仅作线索，引用其数据须回溯原文）：

13. **"Memory as Metabolism"**, arXiv:2604.12034, Apr 2026（引述 SleepGate arXiv:2603.14517、LightMem 的 sleep-consolidation 谱系）. https://arxiv.org/abs/2604.12034
14. arXiv:2604.11243, Apr 2026（引述 MemMachine -80% token、Memori 81.95%@1,294 tokens）. https://arxiv.org/pdf/2604.11243
15. arXiv:2604.07798, Apr 2026（引述 LightMem 检索 p50/p95 83/167 ms、A-MEM 重尾延迟）. https://arxiv.org/pdf/2604.07798
16. Atlan. **"Agent Memory Architectures: 5 Patterns and Trade-offs (2026)"**（Mem0 17.12 s/1.44 s、26,031/1,764 tokens 精确值转述）, 2026-04-17. https://atlan.com/know/agent-memory-architectures/

---

## 7. 未能核实 / 存疑的点

- **D1（重要，可复现性）**：Mem0 原论文自报 LOCOMO J = 66.9%，但第三方复现（SwiftMem, arXiv:2601.08160 Table 2，GPT-4o-mini）中 Mem0 仅 0.613，且该复现口径下 FullContext 为 0.723、Zep 为 0.585。同一基准不同复现间分数差异显著，引用 Mem0 精度数字时必须注明"作者自报 + LLM-as-Judge 口径"。
- **D2**：CraniMem "+57.6%（噪声 HotpotQA vs Mem0）"——论文存在且定性声明成立（✅），但具体数字未核实（未读全文）；且源简报已自注"使用作者注入的 distractor 而非标准基准"。建议写作时降级为定性表述或读全文后回填。
- **D3**：CSDN 等中文二手文章流传一张"Mem0 LOCOMO 92.5 / OpenAI 73.4 / P95 <50ms"表格，标注来源为 arXiv:2504.19413，但与论文原文（Mem0 66.9%、p95 1.44 s）严重不符，疑为把 2026 年厂商新版数字与旧论文张冠李戴。**不要使用该表**。mem0.ai 博客的 91.6% 新数字亦应与 2025 论文明确区分版本。
- **D4**：memory 注入策略对 prefix caching 命中率的量化影响（η 的实测数据）本轮未找到公开量化研究，仅有机制层面的推理（§3.4 第 1 点）。这是一个可以标注为"研究空白"的点。
- **D5**：MemOS KV-cache 注入 vs prompt 注入的具体加速数字在论文正文图表中，本轮只确认了实验设置（583/2,773/6,064 tokens 三档 context），未提取到数值；仓库的 35.24%/72% token savings 为厂商自报。
- **D6**：SYNAPSE（arXiv:2601.02744）的 LoCoMo "显著超 SOTA"、A-MEM（arXiv:2502.12110）的 multi-hop 提升、MAGMA（arXiv:2601.03236）的类型特化优势、Agentic Memory（arXiv:2601.01885）的"更小 context window"声明——本轮均未读取全文，无量化数字，状态 ❌ 未核实。
- **D7**：Memori（81.95% @ 1,294 tokens）与 MemMachine（-80% token）数字均来自 arXiv:2604.11243 的二手引述，未回溯原论文。
- **D8**：源简报基准对应表（"LongBench-v2: HiMem, MAGMA"、"PersonaMem: AdaMem, Mem0" 等）未逐条复核；"AdaMem" 一文的出处未确认。

---

*简报结束。所有标注 ✅ 的数据点均在本轮（2026-07-16）经一手来源核实；🟡 为二手转述或厂商自报；❌ 为未核实。下游写作者引用 ❌ 项前请先回填核实。*
