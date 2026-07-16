---
tags: [optimization, LLM, agent-memory, Mem0, LightMem, MemOS, Zep, KV-cache, retrieval, latency]
aliases: [Agent-Memory-Performance-Optimization]
---

# Agent Memory System 性能优化：从全上下文到「写入离线化 + KV-form 记忆」

> **研究日期**: 2026-07-16
> **素材来源**: 本周技术雷达 LLM Agent Memory 研究简报（2026-07-14）+ 同日调研简报（含一手来源核实）
> **核心问题**: LLM Agent 的外部记忆系统，其 token/延迟开销的主矛盾在哪里，生产上如何把成本压到可用区间？

---

## 优化场景

- **问题**：长期运行的 Agent 需要跨会话记忆。朴素方案是把全部历史对话塞进 context（full-context stuffing），但历史随时间无限增长，token 成本、TTFT、KV cache 显存三重不可扩展。引入外部记忆系统（embedding 检索 + 文本注入）后，检索本身只花百毫秒级，但**写入/整合路径上的 LLM-in-the-loop** 把每轮对话的在线成本翻倍。如何在不显著牺牲记忆质量的前提下重构这条开销曲线？
- **主题**：[[LLM]] / [[Agent]] / [[Retrieval]] / [[System Optimization]]

---

## 优化前：瓶颈画像

### 1. 全上下文基线（不优化的对照组）

Mem0 论文（Chhikara et al., 2025, arXiv:2504.19413）在 LOCOMO 基准上给出的 full-context 基线：

| 指标 | Full-context | 备注 |
|------|-------------|------|
| tokens / query | ≈26,000（chunk 级，正文；第三方转述精确值 26,031，🟡 Atlan 2026） | 历史全量注入 |
| p95 端到端延迟 | ≈17 s（正文 "around 17 seconds"；第三方转述 17.12 s，🟡） | LLM 生成主导 |
| LOCOMO LLM-as-Judge (J) | ≈72.9%（全文最高） | 质量上界，但经济上不可用 |
| KV cache 显存（26K tokens, 70B 级） | ≈8.5 GB / 会话（推导见下） | 高并发下显存先爆 |

### 2. 记忆系统延迟的构成分解

单次带记忆的请求，其端到端延迟分解为检索段与生成段：

$$
T_{\text{e2e}} = \underbrace{T_{\text{embed}}(q) + T_{\text{ANN}}(q) + T_{\text{rerank}}(q, k) + T_{\text{inject}}}_{T_{\text{retrieval}}} + \underbrace{T_{\text{prefill}}(n_{\text{ctx}}) + T_{\text{decode}}}_{T_{\text{generation}}}
$$

各项的典型量级与瓶颈属性：

| 组件 | 典型量级 | 瓶颈属性 |
|------|---------|---------|
| $T_{\text{embed}}$ | 本地小模型 <10 ms；远程 embedding API 50–200 ms（网络主导） | 可本地化消除 |
| $T_{\text{ANN}}$ | HNSW 平均查询复杂度 $O(\log N)$，毫秒级 | 随记忆库规模对数增长，可控 |
| $T_{\text{rerank}}$ | cross-encoder 约 $k$ 次 forward（百毫秒内）；**若用 LLM rerank 则直接进入百毫秒–秒级** | LLM-in-the-loop 是重尾来源 |
| $T_{\text{prefill}}$ | 随注入 token 数近似线性（attention 部分随 $n^2$，见下文推导） | 由注入策略决定 |
| 写入路径（异步/同步） | Mem0 每消息对 ≥2 次额外 LLM 调用 | **在线开销的主矛盾** |

**关键实测锚点（第三方复现，SwiftMem, arXiv:2601.08160, Table 2, ✅）**：Mem0 的 search 阶段耗时 784 ms，而其纯索引检索仅需 11 ms——70 倍的差距几乎全部来自检索链路中引入的 LLM 调用（查询处理/结果仲裁），而非向量索引本身。A-MEM 亦存在重尾检索延迟（🟡 经 arXiv:2604.07798 引述）。

---

## 优化方法

### 一、主矛盾判定：在线开销在写入/整合路径，而非检索路径

#### 1.1 Mem0 写入路径的开销模型（✅ 正文核实）

Mem0 的记忆写入是两阶段流水线（arXiv:2504.19413 §2）：

1. **Extraction**：LLM 函数 $\varphi(P)$ 从消息对 $(m_{t-1}, m_t)$ 提取候选事实集 $\Omega = \{\omega_1, \dots, \omega_n\}$，其中 prompt $P = (S, \{m_{t-m}, \dots, m_{t-2}\}, m_{t-1}, m_t)$，$S$ 为异步刷新的会话摘要（不阻塞主流水线），实验配置 $m = 10$。
2. **Update**：对每个候选事实先检索 top-$s$（$s = 10$）条语义相似记忆，再由 LLM 通过 tool call 仲裁 ADD / UPDATE / DELETE / NOOP 之一。

形式化每轮写入成本：

$$
C_{\text{write/turn}} \;\geq\; \underbrace{C_{\text{LLM}}^{\text{extract}}}_{1 \text{ 次}} + \underbrace{C_{\text{ANN}}(s)}_{s=10} + \underbrace{C_{\text{LLM}}^{\text{update}}}_{\geq 1 \text{ 次}} \;\geq\; 2 \cdot C_{\text{LLM-call}} + C_{\text{ANN}}(s)
$$

即**每条消息对的在线写入至少引入 2 次额外 LLM 调用**，与回答本身的 1 次主调用同量级。检索路径可以压到 100–200 ms（见第三节），但写入路径的 LLM 调用是秒级且逐轮发生的。这就是"主矛盾在写入侧"的定量含义。

#### 1.2 LightMem 的 sleep-time 离线整合：转移成本而非消除成本

LightMem（Fang et al., 2025, arXiv:2510.18866, ✅ 摘要核实）用 Atkinson-Shiffrin 三阶段模型重构这条路径：sensory memory（轻量压缩过滤 + 按 topic 分组）→ topic-aware short-term memory（整合摘要）→ long-term memory with **sleep-time update**（离线整合，与在线推理解耦）。在线路径只留轻量过滤与分组，重的合并/仲裁移到离线。

其报告的四个成本口径（LongMemEval / LoCoMo，GPT 与 Qwen 骨干）：

| 口径 | 节省倍数 | 含义 |
|------|---------|------|
| 纯在线 test-time token | 最高 ↓106× / ↓117× | 用户感知路径上的成本 |
| 纯在线 API 调用 | 最高 ↓159× / ↓310× | 在线 LLM 调用次数 |
| **总** token（含离线整合） | 最高 ↓38× / ↓20.9× | 系统真实总成本 |
| **总** API 调用（含离线） | 最高 ↓30× / ↓55.5× | 系统真实调用总量 |

设在线成本为 $C_{\text{on}}$、离线整合成本为 $C_{\text{off}}$、Mem0 类在线整合基线为 $C_{\text{base}}$。LightMem 的数字结构为：

$$
\frac{C_{\text{base}}}{C_{\text{on}}} \approx 106\text{–}117\times \qquad \text{而} \qquad \frac{C_{\text{base}}}{C_{\text{on}} + C_{\text{off}}} \approx 20.9\text{–}38\times
$$

两式联立可反解离线成本占比。以 LongMemEval 口径估计（$106\times$ 与 $38\times$）：

$$
\frac{C_{\text{on}}}{C_{\text{on}} + C_{\text{off}}} = \frac{C_{\text{base}}/106}{C_{\text{base}}/38} = \frac{38}{106} \approx 0.358 \qquad \Rightarrow \qquad \frac{C_{\text{off}}}{C_{\text{on}} + C_{\text{off}}} = 1 - \frac{38}{106} \approx 0.642
$$

即离线整合约占总成本的 64%。

直接计算更简洁：令 $C_{\text{base}} = 1$，则 $C_{\text{on}} \approx 1/106$，$C_{\text{on}} + C_{\text{off}} \approx 1/38$，故

$$
C_{\text{off}} \approx \frac{1}{38} - \frac{1}{106} = \frac{106 - 38}{38 \times 106} = \frac{68}{4028} \approx 0.0169, \qquad \frac{C_{\text{off}}}{C_{\text{on}}} \approx \frac{106}{38} - 1 \approx 1.79
$$

即**离线整合的绝对成本约是在线剩余成本的 1.8 倍**。结论：sleep-time update 把成本从用户感知的在线路径**转移**到离线路径，并未消除——总成本口径的节省倍数（20.9–38×）才是系统设计的真实预算，纯在线口径（106–117×）只是延迟/SLO 视角。写作与汇报时必须区分这两个口径。

#### 1.3 异步化的工程对应物

MemOS 官方仓库（🟡 厂商自报）：MemScheduler 异步写入（标称"毫秒级延迟"）+ Redis Streams 任务队列 + queue isolation + 任务优先级 + 自动恢复 + quota 调度（v2.0, 2025-12-24）——把记忆写入做成异步后台任务，避免阻塞在线推理。这与 LightMem 的 sleep-time update 是同一思想的生产工程实现。

### 二、检索路径优化：纯检索已进入 100–200 ms 区间

实测数据汇总：

| 系统 | 检索延迟 | 来源（核实级别） |
|------|---------|----------------|
| LightMem | p50/p95 = 83/167 ms | 🟡 经 arXiv:2604.07798 引述 |
| Zep auto search | p50/p95 = 115/173 ms | 🟡 getzep.com/research（2026 抓取，厂商自报） |
| SwiftMem 纯索引 | search = 11 ms | ✅ arXiv:2601.08160 Table 2 |
| Mem0（第三方复现口径） | search = 784 ms | ✅ arXiv:2601.08160 Table 2 |
| A-MEM | 重尾延迟（heavy tail） | 🟡 经 arXiv:2604.07798 引述 |

结论：**纯 embedding + ANN + 轻量 rerank 的路径可稳定压进 200 ms 内**；一旦在检索链路引入 LLM（查询重写、LLM rerank、agentic 多跳仲裁），延迟即进入秒级并出现重尾。检索路径的优化原则是「去 LLM 化」：Zep 的 auto search 用单次 API 调用、免调参的 hybrid search（vector + BM25 + graph traversal 统一排序，🟡 官方页），把中位注入 context 压到 2,680 tokens，比 multi-scope 手工组合 -53%（🟡 同上）。

### 三、token 成本与 prefill/显存的定量关系

#### 3.1 break-even 模型

设历史对话共 $n_{\text{hist}}$ tokens，每次查询注入 $n_{\text{ret}}$ tokens 检索结果，问题本身 $n_q$ tokens，输入单价 $c_{\text{in}}$。全上下文与外部记忆的 per-query 成本：

$$
C_{\text{full}} = n_{\text{hist}} \cdot c_{\text{in}}, \qquad C_{\text{mem}} = (n_{\text{ret}} + n_q) \cdot c_{\text{in}} + \frac{C_{\text{write}}}{Q} + C_{\text{retrieve}}
$$

其中 $C_{\text{write}}$ 为写入/整合总开销，$Q$ 为一次写入后服务的查询数（摊销因子）。外部记忆占优的 break-even 条件为

$$
n_{\text{hist}} \;>\; n_{\text{ret}} + n_q + \frac{1}{c_{\text{in}}}\left(\frac{C_{\text{write}}}{Q} + C_{\text{retrieve}}\right)
$$

Mem0 实测点：$n_{\text{hist}} \approx 26{,}031$ vs $n_{\text{ret}} \approx 1{,}764$ tokens/query，单次查询输入 token 约 -93%（幅度 >90% 为 ✅ 论文摘要；精确值为 🟡 Atlan 转述）。不等式右边即使计入写入摊销，只要 $Q$ 不太小，仍远小于 26K——外部记忆在 token 口径下占优是稳健的；写入摊销项真正影响的是「记忆系统值得做到多重的整合」这一设计点。

#### 3.2 prefill 计算量的平方项推导

self-attention 在 prefill 阶段的 FLOPs（只算 attention 矩阵部分，忽略线性投影）。对每一层，序列长 $n$、隐维 $d$：

- $QK^{\top}$：$(n \times d) \cdot (d \times n)$ 矩阵乘，FLOPs $= 2nd \cdot n = 2dn^2$（每个输出元素一次乘加算 2 FLOPs，输出 $n^2$ 个元素，每个元素 $d$ 次乘加：$2 \cdot n^2 \cdot d$）。
- $\text{softmax}(QK^\top/\sqrt{d})\,V$：$(n \times n) \cdot (n \times d)$，同理 $2dn^2$。

合计每层 $4dn^2$，$L$ 层共

$$
\text{FLOPs}_{\text{attn}}(n) \approx 4\,L\,d_{\text{model}}\,n^2
$$

$n$ 从 26,000 降至 1,764 时，attention 部分 FLOPs 变为

$$
\left(\frac{1{,}764}{26{,}000}\right)^2 \approx (0.0678)^2 \approx 0.46\% \quad (\text{约 } 217\times \text{ 缩减})
$$

线性投影部分 FLOPs $\approx 8Ld^2n$ 随 $n$ 线性缩放（约 14.7× 缩减）。由于实际 prefill 中线性项与平方项的占比取决于 $n$ 与 $d$ 的相对大小（交叉点约在 $n \sim 2d$），26K → 1.7K 的总 prefill 成本下降介于两者之间、更靠近线性——与 Mem0 观察到的「token 节省 >90% ⇒ 成本近似成比例下降」一致（✅ arXiv:2504.19413）。

#### 3.3 KV cache 显存推导（GQA）

$$
M_{\text{KV}} = 2 \cdot L \cdot H_{\text{kv}} \cdot d_h \cdot n \cdot b
$$

其中因子 2 对应 K、V 两份，$H_{\text{kv}}$ 为 KV head 数，$d_h$ 为 head 维，$b$ 为每元素字节数。以 Llama-3-70B 量级（$L = 80$，$H_{\text{kv}} = 8$，$d_h = 128$，FP16 即 $b = 2$）：

$$
\frac{M_{\text{KV}}}{n} = 2 \times 80 \times 8 \times 128 \times 2 \text{ B} = 327{,}680 \text{ B} \approx 0.33 \text{ MB/token}
$$

26K tokens 的历史即 $26{,}000 \times 0.33 \approx 8.5$ GB KV cache——**每会话**。高并发下显存先被 KV cache 打满而非权重，这是全上下文方案在系统层不可扩展、必须走外部记忆路线的硬约束（推导为本备忘录自算，参数取公开模型配置）。

### 四、前沿：memory × KV cache 的交互

#### 4.1 KV-form 记忆（activation memory）：绕开 prefill

MemOS（Li et al., 2025, arXiv:2507.03724, ✅）把记忆统一为三态并调度其转化：

$$
\text{plaintext（文本，检索注入）} \;\rightleftharpoons\; \text{activation（KV-form，attention cache 直注）} \;\rightleftharpoons\; \text{parameter（蒸馏进权重）}
$$

MemScheduler 持续监控交互，识别「高频访问 + 语义稳定」的 plaintext 条目，预编码为 KV 格式注入 attention cache 并预置 GPU——与 OS 的 page promotion（磁盘 → 内存 → TLB）同构。论文正文含 prompt 注入 vs KV-cache 注入的对照实验，context 长度分 583 / 2,773 / 6,064 tokens 三档（✅ 实验设置；具体加速数值在正文图表，本轮未提取，❌ 不引用数字）。SleepGate（arXiv:2603.14517，🟡 经 arXiv:2604.12034 引述）进一步把 forgetting gate + consolidation 直接作用于 KV 层，做周期触发的 sleep micro-cycle。

成本逻辑：plaintext 注入每查询都要付 $T_{\text{prefill}}(n_{\text{ret}})$；KV-form 直注把这笔成本一次性预付，之后每查询的边际成本趋近于零（仅 attention 时多读 $n_{\text{ret}}$ 个 KV 位置，带宽开销而非 prefill 计算）。对「高频稳定」条目，预付摊销后净收益为正——这正是 1.2 节 break-even 模型中 $C_{\text{write}}/Q$ 项被 $Q$ 摊薄的极限形态。

#### 4.2 记忆注入与 prefix caching 的冲突（研究空白）

若记忆以文本注入且位置在共享前缀之后，不同查询检索到不同记忆 ⇒ 前缀在记忆块处断裂，prefix cache miss，prefill 成本回升。设前缀命中率 $\eta$：

$$
C_{\text{prefill}} = (1 - \eta)\, C_{\text{full-prefill}} + \eta\, C_{\text{incremental}}
$$

注入策略（固定槽位、按稳定度排序、记忆块置前）直接决定 $\eta$。**截至 2026-07-16，未找到针对该交互的公开量化研究（$\eta$ 的实测数据），标注为研究空白**（调研简报存疑点 D4）。这是 memory 系统与 serving 系统交叉处一个可以直接做实验发结果的点。

### 五、质量-成本权衡：token 节省不是免费的

Mem0 论文的完整权衡（✅ arXiv:2504.19413）：

| 指标 | Full-context | Mem0 | Mem0^g（图变体） |
|------|-------------|------|------------------|
| LOCOMO J | ≈72.9% | 66.9%（-6 pt） | 68.4% |
| p95 延迟 | ≈17 s | ≈1.44 s（-91%~-92%） | ≈2.6 s（-85%） |
| tokens/query | ≈26,000 | ≈1,764（-93%，🟡 精确值） | N/A |

三个要点：

1. **token 节省 >90% 的代价是 J 分数 72.9% → 66.9%（-6 pt）**。外部记忆用精度换经济性与延迟，不是帕累托改进。
2. **图记忆层（Mem0^g）用 +81% 的 p95 延迟（1.44 s → 2.6 s）换回约 +1.5 pt 精度**——结构化关系建模的边际收益递减，是否值得取决于任务对多跳关系的依赖度。
3. **可复现性警示**：第三方复现（SwiftMem, arXiv:2601.08160, Table 2, GPT-4o-mini, ✅）中 Mem0 的 J 仅 0.613，同一复现口径下 FullContext 0.723、Zep 0.585。与论文自报的 66.9% 存在显著偏差。引用 Mem0 精度数字时必须注明「作者自报 + LLM-as-Judge 口径 + 版本」。Mem0 官方博客 2026-06-26 的新数字（LOCOMO 91.6%、均值 <7K tokens、🟡 厂商自报）是 2026 新版结果，与 2025 论文的 66.9% 不可混用。

LightMem 一侧的权衡方向相反：成本数量级下降的同时 QA 准确率最高 +7.7%（LongMemEval）/ +29.3%（LoCoMo）（✅ arXiv:2510.18866 摘要）——说明「写入路径重构」与「注入压缩」不同，前者在降低在线成本的同时通过更干净的整合还可能提升质量。

### 六、生产级优化手段清单

#### 6.1 记忆压缩与摘要

| 手段 | 机制 | 量化锚点 | 来源 |
|------|------|---------|------|
| 抽取式事实化 | 对话对 → 候选事实集 $\Omega$ → LLM 仲裁 ADD/UPDATE/DELETE/NOOP | token -93%（>90% ✅；精确值 🟡） | arXiv:2504.19413 |
| 异步分层摘要 | 会话摘要 $S$ 周期刷新、不阻塞主流程 | 提供 extraction 全局上下文 | 同上（✅ 正文） |
| 逐级压缩 | sensory → STM → LTM 逐层过滤整合 | 在线 token ↓106×/117× | arXiv:2510.18866（✅ 摘要） |
| 单层 raw+索引 | raw-episode + sentence-level index 双层 | 约 -80% token（🟡 二手引述，未回溯原文） | 经 arXiv:2604.11243 引述 MemMachine |
| 高压缩注入 | — | 1,294 tokens/query（约全上下文 5%）、LoCoMo 81.95%（🟡 同上，未回溯原文） | 经 arXiv:2604.11243 引述 Memori |

#### 6.2 分层记忆的检索复杂度

flat 向量库 HNSW 查询 $O(\log N)$，但 $N$ 随会话无限增长，且候选集噪声随 $N$ 上升（精度问题先于复杂度问题出现）。分层结构先检索高层摘要/主题层再 drill-down：设分支因子 $B$、深度 $D$，总条目数 $N = O(B^D)$，每层在小索引上查询，检索复杂度

$$
T_{\text{hier}} = O\!\left(D \cdot \log B\right) = O\!\left(\frac{\log N}{\log B} \cdot \log B\right) = O(\log N)
$$

渐进阶相同，但常数与精度特性不同：每层的候选集规模从 $N$ 降为 $B$，ANN 的召回质量在小而语义同构的子索引上更高，高层节点充当语义路由、减少低层噪声。已核实实例：HiMem（arXiv:2601.06377, ✅ 摘要）Episode Memory（Topic-Aware Event–Surprise 双通道切分）+ Note Memory 两层语义链接，支持 hybrid / best-effort 两种检索策略平衡 accuracy/efficiency——但**无公开量化延迟数字**（🟡）。

#### 6.3 gating / 遗忘策略：存储与检索成本的显式建模

1. **Utility gating**（CraniMem, arXiv:2603.15642, ✅ 定性）：写入仅当效用 $u(x) > \tau$，效用信号 = importance / surprise / emotional salience。设每轮到达 1 条、门控通过率 $\rho$、平均条目大小 $\bar{s}$，则期望存储 $E[S(N)] = \rho N \bar{s}$，检索候选集同比缩小 $\rho$ 倍。
2. **Bounded buffer**（CraniMem FIFO episodic buffer, ✅ 定性）：存储硬上界 $S \le B$ ⇒ 检索复杂度从 $O(\log N)$ 变 $O(\log B)$，**存储增长从 $O(N)$ 压到 $O(1)$**——这是「遗忘是成本特性而非精度特性」的最直接论证。
3. **指数时间衰减**（spreading activation 系，SYNAPSE 的 temporal decay）：activation 演化

$$
a_i(t) = a_i(t_0)\, e^{-\lambda (t - t_0)}, \qquad a_i = \sum_j w_{ji}\, a_j \ \ (\text{spreading})
$$

衰减至阈值以下的条目批量 prune，存储与候选集规模随 $\lambda$ 指数收缩；Ebbinghaus 遗忘曲线 $R = e^{-t/S}$ 同属一族。
4. **Scheduled consolidation**（CraniMem / LightMem / HiMem 共有，✅ 定性）：离线 replay 高效用 trace 进长期存储、prune 低效用项——把删除与合并成本移出在线路径（见第一节）。

#### 6.4 离线整合调度的工程形态

- **队列化**：Redis Streams 任务队列 + queue isolation + 优先级 + quota 调度 + 自动恢复（MemOS v2.0，🟡 官方仓库）。
- **触发策略**：周期触发（sleep-time）vs 事件触发（buffer 满/效用积压），周期触发对延迟 SLO 更友好。
- **RL 学习记忆操作本身**：Memory-R1（Yan et al., 2025, arXiv:2508.19828, ✅ 摘要）用 PPO/GRPO 训练 Memory Manager 的 ADD/UPDATE/DELETE/NOOP 策略，仅 152 个训练 QA pair 即在 LoCoMo/MSC/LongMemEval、3B–14B 规模上超启发式基线——把「何时写、写什么、删什么」从手工规则变为可优化策略（摘要无具体效率数字，不引用量级）。

---

## 优化后：基准画像

| 场景 | 方案 | 指标 | 对照基线 | 来源（核实级别） |
|------|------|------|----------|----------------|
| 长历史问答 token 成本 | Mem0 外部记忆 | ≈1,764 tokens/query | 全上下文 ≈26,000（-93%） | arXiv:2504.19413（幅度 ✅，精确值 🟡） |
| 长历史问答延迟 | Mem0 | p95 ≈1.44 s | 全上下文 ≈17 s（-91.6%） | 同上（✅） |
| 在线写入成本 | LightMem sleep-time update | 在线 token ↓106×/117×，API 调用 ↓159×/310× | Mem0 类在线整合 | arXiv:2510.18866（✅ 摘要） |
| 系统总成本 | LightMem（含离线） | 总 token ↓38×/20.9×，API ↓30×/55.5× | 同上 | 同上（✅ 摘要） |
| 检索路径延迟 | Zep auto search | p50/p95 = 115/173 ms，中位注入 2,680 tokens | multi-scope 组合 -53% tokens | getzep.com/research（🟡 厂商自报） |
| 检索去 LLM 化 | SwiftMem 纯索引 | search 11 ms；端到端 3.54 s → 1.29 s | Mem0 search 784 ms | arXiv:2601.08160（✅ 第三方复现） |
| 时序知识图质量 | Zep | DMR 94.8%（GPT-4 Turbo）/ 98.2%（4o-mini）；LongMemEval +18.5% 且延迟 -90% | MemGPT 等 | arXiv:2501.13956（✅ 论文） |
| KV-form 记忆 | MemOS MemScheduler | KV 注入 vs prompt 注入对照（583/2,773/6,064 tokens 三档） | prompt 注入 | arXiv:2507.03724（✅ 实验存在；数值 ❌ 未提取） |
| OS 级记忆调度 | MemOS | OpenClaw 任务完成率 36.63% → 50.87%；仓库标称 token savings 35.24%（Cloud Plugin -72%） | 无记忆基线 | github.com/MemTensor/MemOS（🟡 厂商自报） |
| KV cache 压缩（对照路线） | LeanKV | KV 2.7–5.7× 压缩、吞吐 1.9–5.4×、内存管理时间占比 76% → <1% | 无压缩 | arXiv:2412.03131（✅） |

---

## 经验教训

### 1. 先分清两个成本口径再谈优化幅度

「在线成本」与「总成本」是两个口径。LightMem 纯在线 token ↓106×/117× 但总口径仅 ↓38×/20.9×（✅ arXiv:2510.18866），反解离线成本约为在线剩余的 1.8 倍。**sleep-time 整合是转移成本而非消除成本**——向面试官汇报时只说在线口径数字是误导；系统设计预算必须按总口径。

### 2. 写入路径才是 Agent memory 的在线开销主矛盾

Mem0 每消息对 ≥2 次额外 LLM 调用（extraction + update 仲裁，✅ 正文核实），与回答本身同量级。检索路径已能压到 100–200 ms（Zep 115/173 ms 🟡、LightMem 83/167 ms 🟡），但写入侧的 LLM 调用逐轮发生。优化优先级：写入离线化 > 检索去 LLM 化 > 注入压缩。

### 3. LLM-in-the-loop 是延迟重尾的唯一主要来源

第三方复现（✅ arXiv:2601.08160）：同一系统 search 阶段 784 ms vs 纯索引 11 ms（≈70×）；A-MEM 存在 heavy tail（🟡 引述）。任何在检索/写入链路中放 LLM 的设计，都要显式预算其 p95/p99 并准备降级路径（超时 → 跳过记忆 → 裸答）。

### 4. token 节省与精度是显式交换，不是帕累托改进

Mem0 的 -93% token 代价是 J 72.9% → 66.9%（-6 pt，✅）；Mem0^g 用 +81% p95 换 +1.5 pt。选型时先把任务的质量容忍度（J 分数可接受的下降幅度）写成约束，再在该约束下最大化成本节省，而不是反过来。

### 5. 可复现性警示：作者自报 + LLM-as-Judge 数字必须带口径标签

Mem0 论文自报 J = 66.9%，第三方复现仅 0.613（✅ arXiv:2601.08160）；厂商 2026 新数字（91.6%，🟡）与 2025 论文不是同一版本。**点名警示：中文二手文章流传的「Mem0 LOCOMO 92.5 / OpenAI 73.4 / P95 <50ms」表格与 arXiv:2504.19413 原文严重不符（原文为 66.9% / p95 1.44 s），系张冠李戴，禁止使用**（调研简报存疑点 D3）。引用任何记忆系统精度数字，三件套缺一不可：来源版本、评测口径（LLM-as-Judge 模型）、自报还是第三方复现。

### 6. 遗忘/gating 是成本特性，按成本特性设计

Bounded buffer 把存储增长从 $O(N)$ 压到 $O(1)$、检索从 $O(\log N)$ 压到 $O(\log B)$；utility gating 以通过率 $\rho$ 线性缩放存储与候选集；指数衰减以 $\lambda$ 指数收缩候选集。这三个旋钮的调参目标首先是 SLO 与预算，其次才是精度——精度损失用 LOCOMO/LongMemEval 类基准回归兜底。

### 7. memory × KV cache 是下一个系统优化前沿，且有研究空白

KV-form activation memory 把高频稳定记忆的注入从「每查询付 prefill」变为「一次性预付、边际近零」（MemOS, ✅ 机制）；而**记忆文本注入对 prefix caching 命中率 $\eta$ 的量化影响目前无公开研究**（调研简报 D4）——固定槽位、稳定度排序、记忆块置前三个策略对 $\eta$ 的影响是可以直接测量的实验点。

---

## 参考

1. Chhikara, P., Khant, D., Aryan, S., Singh, T., Yadav, D. **"Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory"**, arXiv:2504.19413, Apr 2025. https://arxiv.org/abs/2504.19413
2. Fang, J. et al. **"LightMem"**（三阶段记忆 + sleep-time update）, arXiv:2510.18866, Oct 2025 (v4 Feb 2026). https://arxiv.org/abs/2510.18866
3. Li, Z. et al. **"MemOS: A Memory OS for AI System"**, arXiv:2507.03724, Jul 2025 (v4 Dec 2025). https://arxiv.org/abs/2507.03724 ；短版 arXiv:2505.22101. https://arxiv.org/abs/2505.22101
4. Rasmussen, P. et al. **"Zep: A Temporal Knowledge Graph Architecture for Agent Memory"**, arXiv:2501.13956, Jan 2025. https://arxiv.org/abs/2501.13956
5. Yan, S. et al. **"Memory-R1: Enhancing LLM Agents to Manage and Utilize Memories via RL"**, arXiv:2508.19828, Aug 2025 (v5 Jan 2026). https://arxiv.org/abs/2508.19828
6. Mody, P. et al. **"CraniMem: Cranial Inspired Gated and Bounded Memory for Agentic Systems"**, arXiv:2603.15642, Mar 2026. https://arxiv.org/abs/2603.15642
7. Zhang, N. et al. **"HiMem: Hierarchical Long-Term Memory for LLM Long-Horizon Agents"**, arXiv:2601.06377, Jan 2026. https://arxiv.org/abs/2601.06377
8. **SwiftMem**（第三方复现基准，含 Mem0/Zep 延迟与 J 分数对照表）, arXiv:2601.08160, Jan 2026. https://arxiv.org/pdf/2601.08160
9. **LeanKV: Unifying KV Cache Compression for Large Language Models**, arXiv:2412.03131, Dec 2024. https://arxiv.org/pdf/2412.03131
10. MemTensor. **MemOS 官方仓库**（benchmark 与 token savings 声明，厂商自报）, 2026-07 抓取. https://github.com/MemTensor/MemOS
11. Zep AI. **官方 benchmark 页**（auto search 延迟/context 数字，厂商自报）, 2026-05 抓取. https://www.getzep.com/research/
12. Mem0 官方博客. **"Memory vs Context Window for LLM and AI Agents"**（2026 新版 LOCOMO 数字，与 2025 论文区分版本）, 2026-06-26. https://mem0.ai/blog/context-window-is-ram-not-storage-why-most-agent-failures-happen-how-to-fix-them-in-2026
13. **"Memory as Metabolism"**, arXiv:2604.12034, Apr 2026（二手引述 SleepGate arXiv:2603.14517）. https://arxiv.org/abs/2604.12034
14. arXiv:2604.07798, Apr 2026（二手引述 LightMem 检索 p50/p95 83/167 ms、A-MEM 重尾延迟）. https://arxiv.org/pdf/2604.07798
15. arXiv:2604.11243, Apr 2026（二手引述 MemMachine -80% token、Memori 81.95%@1,294 tokens）. https://arxiv.org/pdf/2604.11243
16. Atlan. **"Agent Memory Architectures: 5 Patterns and Trade-offs (2026)"**（Mem0 17.12 s/26,031/1,764 tokens 精确值转述）, 2026-04-17. https://atlan.com/know/agent-memory-architectures/

---

> **编制说明**：本文从性能优化视角重构本周技术雷达的 LLM Agent Memory 简报，主线为「瓶颈定位 → 写入路径离线化 → 检索去 LLM 化 → KV-form 记忆前沿 → 质量-成本权衡」。数据点核实状态沿用调研简报（2026-07-16）：✅ 一手核实、🟡 二手/厂商自报、❌ 未核实（已舍弃或标注）。所有公式推导见对应小节。
