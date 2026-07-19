---
tags: [paper, agent-harness, context-engineering, agent-scaffolding, multi-agent, workflow, sandbox, llm-agent]
aliases: [Agent-Harness-Latest-2025-2026]
created: 2026-07-20
---

# 方向五：Agent Harness 工程与上下文工程（2025–2026 最新论文）

> **核心问题**：模型固定后，Agent 的性能从哪里来？如何系统化地优化 inference-time context、设计 agent 脚手架（scaffolding）、诊断多 agent 失败、自动化 workflow 编排，并构建可控可扩展的执行环境？
> **技术栈**：Context Engineering + Agent Scaffolding + Workflow Search (MCTS) + Memory Versioning + Sandbox Execution
> **关联**：[[01d-sandbox-latest]], [[01a-LLM-Agent-in-Games]], [[01-Game-AI-研究库总览]]

---

## 核心问题定义

```
问题形式化：给定固定模型 LLM，Agent 系统的优化目标是上下文分布 c：
  c* = argmax_c  E[ reward | LLM(query, c) ]

其中 c 由以下组件合成：
1. Context Retrieval & Generation：RAG、prompt 设计、任务描述生成
2. Context Processing：压缩、长上下文推理、结构化表示
3. Context Management：memory、版本化、跨 session 持久化
4. 系统实现层：RAG 系统 / memory 系统 / tool-integrated reasoning / multi-agent orchestration

Agent Harness 的核心矛盾：
- 透明可控 vs 规模性能：研究级 agent 可解释但扛不住生产负载，反之亦然
- 上下文增长 vs 上下文质量：长 horizon 交互无界膨胀，压缩与重写会引入 brevity bias / context collapse
- 编排收益 vs 编排失败：多 agent 的收益常被 coordination breakdown 吃掉
- 执行信号真实性 vs 环境构建成本：整仓环境真实但不可扩展，最小闭包可扩展但丢失部分真实性
```

**Harness 在 Agent 技术栈中的位置**：
- **内容层**（Context Engineering Survey / ACE）：上下文里放什么、怎么演化
- **结构层**（GCC / MemGPT 类比）：上下文如何组织、版本化、复用
- **编排层**（AFlow / MAST / Confucius）：workflow 与多 agent 怎么搭、为什么翻车
- **执行层**（RepoST）：agent 训练/评测的可控执行环境从哪来

---

## 关键论文

### 1. A Survey of Context Engineering for Large Language Models

- **作者**：Lingrui Mei, Jiayu Yao, Yuyao Ge, Yiwei Wang, Baolong Bi, Jiafeng Guo, Shenghua Liu 等（中国科学院计算技术研究所等联合团队）
- **来源**：arXiv:2507.13334, 2025-07-17（v2 2025-07-21），166 页、引用 1400+ 文献
- **链接**：https://arxiv.org/abs/2507.13334
- **项目**：关联 GitHub awesome-list（Meirtz/Awesome-Context-Engineering，见论文页）

#### AI 预读（150 字）

> 首次将 Context Engineering 形式化为一门系统学科的 166 页综述。核心主张：LLM 性能主要由 inference-time context 而非权重决定。综述把上下文工程分解为三大基础组件（context retrieval & generation、context processing、context management）与四大系统实现（RAG、memory 系统、tool-integrated reasoning、multi-agent systems），构建统一 taxonomy，并指出当前模型"理解长上下文"与"生成等长输出"之间存在不对称性这一核心瓶颈。引用文献 1411 篇，已成为 2025 下半年该领域的标准引用框架。

#### 3 个引导问题

1. **上下文作为优化变量**：综述把 agent 系统视为"在给定模型下对上下文分布 c 做优化"，RAG 是检索侧求解器、compression 是带宽求解器、memory 是时序求解器、多 agent 编排是分布式求解器。这种统一视角下，还存在哪些未被归入任何求解器类别的技术？taxonomy 的边界（如 memory vs retrieval）划分主观性有多大？

2. **理解-生成不对称（understanding–generation asymmetry）**：模型能读 1M token 却写不出等长连贯输出。这一不对称是否可被 KV-cache / 稀疏注意力类方法直接缓解？还是说它本质上是解码策略与训练目标的问题，需要 inference-time 之外的手段？

3. **协议层上下文的覆盖**：该 taxonomy 如何覆盖或遗漏 MCP / A2A 这类协议层上下文？协议约定的上下文格式（工具 schema、消息结构）是否应被视为 context engineering 的一等公民，还是仅仅是 transport 细节？

#### 重点章节标记

1. **基础组件部分**：context retrieval & generation / processing / management 的三分法定义
2. **系统实现部分**：RAG、memory、tool-integrated reasoning、multi-agent systems 四大实现
3. **开放问题部分**：understanding–generation asymmetry 的提出与讨论
4. **评估维度与基准盘点**：context engineering 各方向的 benchmark 综述

#### 面试谈资

- **30 秒**：2025 年 7 月的 166 页综述，第一次把 prompt、RAG、memory、tool use、multi-agent 统一为"Context Engineering"一门学科——模型固定后，所有 agent 性能都来自你对上下文做的优化。
- **2 分钟**：可以讲"上下文作为优化变量"的视角：c* = argmax E[reward | LLM(query, c)]，RAG 是检索侧求解器、compression 是带宽求解器、memory 是时序求解器、多 agent 编排是分布式求解器；并指出其识别的核心开放问题——模型能读 1M token 但写不出等长连贯输出，这一理解-生成不对称决定了 agent 系统的架构上限。局限是 survey 范围极大导致单点深度有限，taxonomy 边界有主观性。

---

### 2. ACE: Agentic Context Engineering

- **作者**：Qizheng Zhang, Changran Hu, Shubhangi Upasani, …, James Zou, Kunle Olukotun（Stanford 等，含产业界合作方）
- **来源**：arXiv:2510.04618, 2025-10-06（v3 2026-03-29）
- **链接**：https://arxiv.org/abs/2510.04618
- **代码**：开源框架 ace-framework（社区实现随论文发布；以论文页链接为准）

#### AI 预读（150 字）

> 针对 context adaptation（改输入而非改权重）中的两大失败模式——brevity bias（为简洁丢掉领域知识）与 context collapse（迭代重写侵蚀细节）——提出 ACE：把上下文当作"活的 playbook"，通过 Generator → Reflector → Curator 模块化循环做结构化、增量式更新。离线可优化 system prompt，在线可优化 agent memory，无需人工标注、仅靠自然执行反馈即可自我改进。agent 基准 +10.6%、金融推理 +8.6%，adaptation latency 降低 82–91%；AppWorld 上以更小开源模型追平排名第一的生产级 agent，并在更难的 test-challenge split 上反超。

#### 3 个引导问题

1. **增量 delta 更新的一致性**：Curator 不重写整个 context，而是以 item 为单位追加/修订 playbook。这种"versioned patch"如何避免 playbook 条目间的矛盾与过期？当条目数无限增长后，检索与干扰问题如何解决？

2. **与 test-time memory 方法的本质差异**：ACE 与 Dynamic Cheatsheet、ReasoningBank 等方法的本质差异是什么？是更新粒度（delta vs rewrite）、反馈来源（execution feedback vs self-reflection）、还是存储结构（playbook vs flat notes）？

3. **playbook 的跨模型迁移**：当底层模型升级时，积累的 playbook 能否迁移？为新模型提炼的策略是否会成为旧模型的"过拟合上下文"？

#### 重点章节标记

1. **失败模式诊断**：brevity bias 与 context collapse 的定义与机制分析
2. **ACE 架构**：Generator / Reflector / Curator 三段式循环
3. **增量 delta 更新**：item 级追加/修订 + 去重组织机制
4. **实验**：agent 基准 +10.6%、金融 +8.6%、AppWorld 追平/反超生产级 agent、latency 降 82–91%

#### 面试谈资

- **30 秒**：把 system prompt 当成会进化的 playbook 而非静态字符串——Generator/Reflector/Curator 循环做增量 patch，解决了"越改写越空洞"的 context collapse，用开源小模型在 AppWorld 反超生产级 agent。
- **2 分钟**：展开两大失败模式的机制：brevity bias 来自 LLM 倾向总结的 prior；collapse 来自 iterative rewriting 的误差累积，类似无 checkpoint 的递归自蒸馏。ACE 的 delta 更新本质是 context 空间的 SGD-with-momentum——不重写、只打 patch。它可以与 GCC 的 git 式版本化互补：ACE 管"内容怎么改"，GCC 管"版本怎么存"。开放问题：playbook 无限增长后的检索干扰、Reflector 质量依赖底层模型自省能力。

---

### 3. Why Do Multi-Agent LLM Systems Fail? (MAST)

- **作者**：Mert Cemri, Melissa Z. Pan, Shuyi Yang, Lakshya A. Agrawal, Kurt Keutzer, Ion Stoica, Joseph E. Gonzalez 等（UC Berkeley）
- **来源**：arXiv:2503.13657, 2025-03-17（v3 2025-10-26）
- **链接**：https://arxiv.org/abs/2503.13657
- **数据/代码**：MAST-Data、taxonomy 与 LLM annotator 均已公开（见论文页）

#### AI 预读（150 字）

> 尽管 multi-agent LLM systems（MAS）热度很高，其在流行基准上的收益却常常微弱。作者构建 MAST-Data——跨 7 个主流 MAS 框架（AutoGen、CrewAI、MetaGPT 等）的 1600+ 标注执行轨迹，并推出首个 MAS 失败分类学 MAST：3 大类、14 种失败模式（系统设计缺陷、inter-agent misalignment、task verification 缺失）。标注由专家完成（Cohen's kappa = 0.88），并配 LLM-as-a-Judge 规模化标注管线。核心结论：多数失败不是"模型不够聪明"，而是 harness/编排层问题。

#### 3 个引导问题

1. **MAS 特有 vs 单 agent 共有的失败**：14 种失败模式中，哪些是单 agent 系统同样存在的（如 verification 缺失），哪些是 MAS 特有的（如 inter-agent misalignment）？区分这两类对"何时该用多 agent"的工程决策有什么指导意义？

2. **verification 失败的形式化修复**：task verification 类失败能否用形式化 contract / guardrail 在 harness 层消除？还是说它本质上需要语义理解，无法纯规则化？

3. **LLM-as-Judge 的偏见继承**：用 LLM 标注失败模式时，judge 模型自身的偏见会不会被继承进 taxonomy？kappa = 0.88 的一致性是否足以排除系统性标注偏差？

#### 重点章节标记

1. **MAST taxonomy**：3 大类 14 种失败模式的定义与示例
2. **MAST-Data 构建**：1600+ 轨迹、7 框架、grounded theory 式开放编码方法
3. **标注管线**：专家标注（kappa 0.88）+ LLM-as-Judge 规模化
4. **失败分布分析**：跨 4 个模型家族 × 3 类任务的失败模式分布；coordination breakdown 约占 36.9%

#### 面试谈资

- **30 秒**：Berkeley 的 MAST 论文把"多 agent 为什么翻车"做成了科学：1600 条真实轨迹、14 种失败模式，结论是多 agent 的收益常被 orchestration 失败吃掉——问题在 harness 不在模型。
- **2 分钟**：可讲 taxonomy 三大类的工程映射：system design issues → 脚手架/角色划分问题；inter-agent misalignment → 通信协议与共享上下文问题；task verification → 缺少 end-to-end 验证环节。研究方法学是 grounded theory：先对 150 条轨迹开放编码聚类出 taxonomy，再回标全量数据。这是"agent harness 工程"作为独立学科存在的经验证据：同样的模型，harness 决定成败。作者明确指出这些失败需要比 prompt 修补更复杂的解法。

---

### 4. AFlow: Automating Agentic Workflow Generation

- **作者**：Jiayi Zhang, Jinyu Xiang, Zhaoyang Yu, Fengwei Teng, …, Sirui Hong, Chenglin Wu（DeepWisdom / 港科大（广州）等，MetaGPT 团队）
- **来源**：arXiv:2410.10762, 2024-10-14（v4 2025-04-15），ICLR 2025 Oral
- **链接**：https://arxiv.org/abs/2410.10762
- **代码**：随 MetaGPT 仓库开源（见论文页）

#### AI 预读（150 字）

> 手工构造 agentic workflow 成本高且难以泛化。AFlow 把 workflow 优化重新表述为"代码表示的 workflow 空间上的搜索问题"：节点为 LLM 调用、边为控制流，用 Monte Carlo Tree Search 结合执行反馈、代码修改与树状经验记录进行迭代探索，实现无需人工初始化的全自动 workflow 生成与优化。六个基准（GSM8K、MATH、HumanEval、MBPP、HotpotQA、DROP）平均超 SOTA 基线 5.7%；小模型 + AFlow 生成的工作流可超过 GPT-4o，推理成本仅为其 4.55%。

#### 3 个引导问题

1. **稀疏/延迟 reward 下的搜索退化**：MCTS 的 reward 用 execution score。当 reward 稀疏或延迟（如多步 agent 任务）时，搜索会退化成什么样？是否需要 reward shaping 或 value network 辅助？

2. **代码表示 vs 图表示**：相比 ADAS / DyLan 的图表示，代码表示的表达力与可搜索性各有什么取舍？代码空间的 LLM mutation 是否更容易产生语义漂移（语法正确但逻辑变质）？

3. **搜索结果的评测过拟合**：搜索出的 workflow 是否过拟合到评测集？如何做 hold-out 验证？"搜一次、部署多次"的 amortization 论点在分布偏移下是否仍然成立？

#### 重点章节标记

1. **形式化**：workflow = 代码图，优化 = 该空间上的搜索（operator 化代码变异）
2. **MCTS 搜索循环**：选择-扩展-回传由执行分数驱动；LLM 作为 mutation operator；树状经验记录避免重复踩坑
3. **实验**：6 基准平均 +5.7%；小模型超 GPT-4o @ 4.55% 成本
4. **与基线对比**：人工 workflow、ADAS 类自动化方法的对比

#### 面试谈资

- **30 秒**：ICLR 2025 Oral，把"搭 agent 脚手架"本身变成 MCTS 搜索问题——workflow 写成代码、LLM 当变异算子、执行分数当 reward，小模型配搜出来的 workflow 只用 GPT-4o 4.55% 的钱就能反超它。
- **2 分钟**：可对比三条自动化脚手架路线：AFlow（代码空间 + MCTS）、ADAS/Agent-as-optimizer（程序归纳）、LangGraph 式人工编排。核心洞察是 workflow 空间离散且组合爆炸，必须用带经验复用的树搜索而非随机变异。延伸讨论"搜索成本 vs 收益"的 amortization 论点——搜一次、部署很多次才划算；每次 rollout 都要跑 LLM，搜索成本本身不低，且对需要环境交互的多步 agent 任务泛化证据较少。

---

### 5. Confucius Code Agent: Scalable Agent Scaffolding for Real-World Codebases

- **作者**：Sherman Wong, Zhenting Qi, Zhaodong Wang, …, Wenlin Chen, Yilun Du, Minlan Yu, Ying Zhang（Harvard University / Meta 等联合团队）
- **来源**：arXiv:2512.10398, 2025-12-11（v6 2026-02-03）
- **链接**：https://arxiv.org/abs/2512.10398
- **代码/平台**：Confucius SDK（agent 开发平台，随论文发布；以论文页为准）

#### AI 预读（150 字）

> 研究级 coding agent 透明但扛不住生产负载，生产级系统强但不可控不可扩展。CCA 基于 Confucius SDK——一个从 Agent Experience (AX)、User Experience (UX)、Developer Experience (DX) 三视角设计的 agent 开发平台：统一 orchestrator 支持长上下文推理的 context management、跨 session 持续学习的持久 note-taking 系统、可靠工具使用的模块化扩展系统；并引入 meta-agent 自动完成 agent 的 build-test-improve 循环。SWE-Bench-Pro Resolve@1 达 59%，在相同仓库/模型/工具条件下超过研究基线与商业系统。

#### 3 个引导问题

1. **AX（Agent Experience）作为一等设计目标**：AX 具体改变了哪些接口/上下文决策？为 agent 的可消费性设计 API（而非为人类开发者）与 MCP 协议的设计哲学有何呼应？

2. **meta-agent vs AFlow**：meta-agent 的 build-test-improve 循环与 AFlow 的 MCTS 搜索相比，搜索效率与工程可用性如何权衡？生产级场景是否更偏好"greedy 迭代"而非"全局树搜索"？

3. **note-taking 的记忆污染**：持久 note-taking 实现跨 session continual learning，但"错误笔记"如何在长期 session 中被识别和清除，而不是被不断放大？是否需要类似 ACE Reflector 的定期反思机制？

#### 重点章节标记

1. **AX/UX/DX 三视角方法论**：agent scaffolding 作为平台工程
2. **运行时四层架构**：orchestrator / context manager / memory (note-taking) / tool extension
3. **meta-agent**：agent 配置的自动化 build-test-improve
4. **实验**：SWE-Bench-Pro Resolve@1 = 59%（同仓库/同模型/同工具条件下超研究基线与商业系统）

#### 面试谈资

- **30 秒**：Harvard/Meta 把 coding agent 脚手架做成了平台：AX/UX/DX 三视角 SDK + 会自己 build-test-improve 的 meta-agent，SWE-Bench-Pro 59% 超过商业系统——脚手架工程正式成为独立研究方向。
- **2 分钟**：可讲"research-grade vs production-grade agent 的鸿沟"这一框架性论点：透明可控与规模性能不可兼得。CCA 的解法是把 agent 运行时平台化（orchestrator / context / memory / tool 四层分离），再让 meta-agent 在平台抽象上做自动化迭代——这是 "agents building agents" 在工业界的落地形态。局限：59% 依赖强模型后端；note-taking 的记忆污染与错误累积问题未充分讨论；v2 曾撤稿后重投，细节以 v6 为准。

---

### 6. Git Context Controller: Manage the Context of LLM-based Agents like Git

- **作者**：Junde Wu, Minhao Hu, Jiayuan Zhu, Jiazhen Pan, Yuyuan Liu, Min Xu, Yueming Jin（Oxford 等）
- **来源**：arXiv:2508.00031, 2025-07-30（v2 2026-03-01）
- **链接**：https://arxiv.org/abs/2508.00031
- **代码**：论文声明将开源（以论文页链接为准）

#### AI 预读（150 字）

> 长 horizon agent 的上下文管理是根本瓶颈：交互历史无界增长、维护昂贵、难以跨 session/agent 复用。GCC 借鉴版本控制思想，把 agent context 从瞬时 token 流升级为持久、可导航的记忆工作区，提供 COMMIT、BRANCH、MERGE、CONTEXT 四个显式操作：里程碑式 checkpoint、替代推理路径的隔离探索、历史上下文的层次化检索。SWE-Bench Verified 相对强长上下文基线提升 13%+，超过 26 个已有开源/商业系统，成功率超 80%；BrowseComp 上达到 SOTA。

#### 3 个引导问题

1. **MERGE 的冲突消解机制**：MERGE 是符号操作还是 LLM 语义操作？当两个 branch 对同一"事实"有矛盾记录时，冲突消解的失败模式是什么？质量是否完全依赖模型能力？

2. **分支爆炸与剪枝**：分支数增长时如何选择保留哪些 trajectory？与 MCTS 的剪枝（AFlow）有何异同？是否存在"branch 的 value function"？

3. **COMMIT 粒度的自动决定**：快照粒度（何时 COMMIT）如何自动决定？固定间隔、事件触发、还是 LLM 自主判断？与 Crab（沙箱 C/R）的"语义感知 checkpoint 粒度分类"有何呼应？

#### 重点章节标记

1. **四个 git 原语**：COMMIT / BRANCH / MERGE / CONTEXT 的定义与语义
2. **versioned file system 组织**：context 作为可导航记忆工作区
3. **实验**：SWE-Bench Verified +13%、超 26 个系统、80%+ 成功率；BrowseComp SOTA
4. **跨 session 恢复与多轨迹并行探索**的支持机制

#### 面试谈资

- **30 秒**：把 agent 的上下文当成 git 仓库来管——COMMIT 存档、BRANCH 探索、MERGE 合并，SWE-Bench Verified 干到 80%+，超过 26 个开源和商业系统。
- **2 分钟**：可展开"从 token stream 到 structured memory workspace"的范式转变：传统 agent 的上下文是 append-only 日志，GCC 给它加了版本语义，使长 horizon 任务可恢复、可并行探索、可跨 agent 移植。再对比三套操作系统类比谱系：MemGPT 式分页（虚拟内存）、GCC（git 版本控制）、ACE（playbook 内容演化）——2025 下半年 context engineering 已形成完整的"OS 类比"工具箱。局限：MERGE 语义由 LLM 执行、存储检索开销随分支增长、非软件任务的验证主要依赖 BrowseComp。

---

### 7. RepoST: Scalable Repository-Level Coding Environment Construction with Sandbox Testing

- **作者**：Yiqing Xie, Alex Xie, Divyanshu Sheth, Pengfei Liu, Daniel Fried, Carolyn Rosé（Carnegie Mellon University）
- **来源**：arXiv:2503.07358, 2025-03-10；COLM 2025 收录
- **链接**：https://arxiv.org/abs/2503.07358
- **代码/数据**：RepoST-Train / RepoST-Eval 数据集随论文发布

#### AI 预读（150 字）

> 为 repository-level 代码生成提供执行反馈（execution feedback）的环境构建非常昂贵——整仓构建对人机都困难。RepoST 提出 sandbox testing：把目标函数及其依赖隔离到独立脚本中测试（"最小可执行闭包"），大幅降低外部依赖复杂度，从而可规模化构建可控执行环境。产出 RepoST-Train（832 个仓库、7,415 个函数）与 RepoST-Eval；基于该执行反馈训练，HumanEval Pass@1 +5.5%、RepoEval Pass@1 +3.5%，并在 RepoST-Eval 上评测 12 个代码模型。

#### 3 个引导问题

1. **信号质量 trade-off**：sandbox testing 与 SWE-bench 式整仓 Docker 环境在信号质量上的 trade-off 是什么？函数级隔离丢失的跨模块交互类 bug 占比多大？什么时候"真实但昂贵"不可替代？

2. **RL 中的 reward hacking**：函数级执行反馈用于 RL / rejection sampling 时，如何避免模型过拟合测试脚本（reward hacking）？测试脚本本身的覆盖率与质量如何进入 reward 设计？

3. **推广到非代码环境**："最小可执行闭包"思路能否推广到非代码 agent 环境——如 web agent 的"最小页面闭包"、游戏 agent 的"最小场景闭包"？依赖提取在非代码领域的等价物是什么？

#### 重点章节标记

1. **sandbox testing 方法**：函数 + 依赖级隔离替代整仓 build
2. **RepoST-Train 构建**：832 仓库 / 7,415 函数的可扩展 pipeline
3. **训练实验**：execution feedback 训练 → HumanEval +5.5%、RepoEval +3.5% Pass@1
4. **RepoST-Eval 基准**：12 个代码模型评测

#### 面试谈资

- **30 秒**：CMU 的 RepoST 回答了"agent 训练的执行环境从哪来"：不 build 整个仓库，把函数和依赖抽进沙箱脚本测试，环境构建规模化后，execution feedback 训练直接涨 5.5 个点 HumanEval。
- **2 分钟**：可讲 agent runtime 基础设施的成本结构：整仓环境（SWE-bench）真实但 O(仓库) 构建成本不可扩展；RepoST 的"最小可执行闭包"把成本降到 O(函数依赖)，牺牲部分真实性换规模——这是"训练数据/环境供给"侧的关键工程路线，与 SWE-smith、SWE-rebench 同属 2025 年 execution-grounded 数据流水线浪潮。局限：依赖提取以 Python 工具链为主；沙箱内 mock 的外部行为可能引入虚假反馈；跨模块交互 bug 覆盖缺失。

---

## 方向横向观察

1. **"模型固定，优化上下文"成为统一范式**：Survey 给出形式化（c* = argmax E[reward | LLM(q, c)]），ACE 管"内容增量演化"、GCC 管"结构版本化"、AFlow 管"编排搜索"——2025 下半年的 harness 论文几乎都可以映射为对该优化问题某一维度的求解器。
2. **OS 类比工具箱成型**：MemGPT 式分页（虚拟内存）→ GCC（git 版本控制）→ ACE playbook（增量 patch）→ RepoST（最小可执行闭包，类似动态链接/按需加载）。context engineering 正在重走操作系统抽象的老路。
3. **Harness 层失败 > 模型层失败**：MAST 的经验证据（多 agent 失败多在编排而非模型）+ Confucius 的平台化解法，共同确立 "agent harness 工程" 作为独立学科。
4. **执行环境的成本-真实性谱系**：SWE-bench 整仓 Docker（真实/贵）→ RepoST 函数级闭包（降维/可扩展），与 [[01d-sandbox-latest]] 中 Crab（C/R 降本）、Agent-World（合成环境）构成完整的"环境供给侧"工程版图。
5. **开放问题**：playbook/分支的无限增长治理、MERGE 语义可靠性、搜索式编排的评测过拟合、错误记忆的长期污染——这些"治理问题"是 2026 年的明确空白。

## 相关链接

| 资源 | 类型 | 链接 | 备注 |
|------|------|------|------|
| Context Engineering Survey | 论文 | https://arxiv.org/abs/2507.13334 | 166 页标准引用框架 |
| ACE | 论文 | https://arxiv.org/abs/2510.04618 | playbook 式上下文演化 |
| MAST | 论文 | https://arxiv.org/abs/2503.13657 | MAS 失败分类学 + MAST-Data |
| AFlow | 论文 | https://arxiv.org/abs/2410.10762 | ICLR 2025 Oral，MCTS workflow 搜索 |
| Confucius Code Agent | 论文 | https://arxiv.org/abs/2512.10398 | 生产级 agent SDK |
| Git Context Controller | 论文 | https://arxiv.org/abs/2508.00031 | git 式上下文版本化 |
| RepoST | 论文 | https://arxiv.org/abs/2503.07358 | COLM 2025，sandbox testing |
| SWE-rebench | 候选 | https://arxiv.org/abs/2505.20411 | 简报标注的后续补充候选 |
| Agent Interoperability Protocols Survey (MCP/ACP/A2A/ANP) | 候选 | https://arxiv.org/abs/2505.02279 | 简报标注的后续补充候选 |

---

## 人类执行任务

- [ ] 精读 ACE 失败模式章节，复述 brevity bias 与 context collapse 的机制差异（30 min）
- [ ] 浏览 MAST taxonomy 的 14 种失败模式，归类"单 agent 共有 vs MAS 特有"（30 min）
- [ ] 精读 GCC 四个原语，画出 COMMIT/BRANCH/MERGE 在长 horizon 任务中的时序图（30 min）
- [ ] 思考并回答："如果给 Obsidian 笔记库加上 GCC 式 BRANCH/MERGE，AI 插件的并行写作流应如何设计？"（写 200 字）（15 min）
- [ ] 在 Obsidian 中创建 [[ACE]], [[MAST]], [[AFlow]], [[Confucius-Code-Agent]], [[Git-Context-Controller]], [[RepoST]] 笔记卡片

---

*创建时间：2026-07-20*
*维护者：AIResearchVault*
