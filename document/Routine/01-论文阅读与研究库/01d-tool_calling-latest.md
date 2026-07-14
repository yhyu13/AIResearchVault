---
tags: [paper, tool-calling, llm-agent, function-calling, agentic-systems, 2025-2026]
aliases: [tool_calling-latest]
created: 2026-07-12
---

# Tool Calling 前沿论文追踪（2025–2026）

> **核心问题**：如何让 LLM Agent 高效、可靠、安全地调用外部工具（API / 函数 / 代码解释器）？
> **技术栈**：Function Calling + Speculative Execution + RL for Tool Use + Transactional Tool Orchestration + Caching
> **关联**：[[01-Game-AI-研究库总览]], [[01a-LLM-Agent-in-Games]], [[Agent-Harness-Game-AI-2026-06-29]]

---

## 核心问题定义

```
问题形式化：给定用户请求 q、候选工具集 T = {t₁, t₂, ...} 和当前对话历史 H，
LLM Agent π_θ 需要：
1. 必要性判断：N(q, H, T) → {need_tool, direct_answer} — 是否必须调用工具
2. 工具选择：Select(q, H, T) → t* ∈ T ∪ {∅} — 选择最合适的工具
3. 参数生成：Args(q, H, t*) → a — 生成结构化调用参数
4. 执行与验证：Exec(t*, a) → r；V(r, q) → {pass, retry, abort} — 执行并验证结果
5. （多步场景）序列规划：Plan(q, H, T) → [t₁, t₂, ...] — 多工具组合调用顺序
```

**Tool Calling 场景的特殊性**（vs. 单轮文本生成）：
- **延迟敏感**：每次工具调用引入网络/API 延迟（50ms–2000ms），多步任务累积严重
- **状态外部化**：工具可能修改数据库、文件系统、第三方服务状态——需要事务语义
- **必要性模糊**：模型常过度调用工具（over-tooling），浪费 token 和延迟
- **错误级联**：参数错误、工具选择错误会在多步任务中传播放大
- **并发与推测**：现代系统开始并行/推测执行工具以隐藏延迟，但引入一致性和隐私风险

---

## 关键论文

### 1. LLM Agents Already Know When to Call Tools — 工具必要性判断

- **作者**：Chung-En Sun et al.
- **来源**：arXiv 2026-05-10
- **链接**：https://arxiv.org/abs/2605.09252
- **代码**：https://github.com/（论文提及开源）

#### AI 预读（150 字）

> 本文发现 LLM Agent 存在严重的 **over-tooling** 问题：即使可以直接回答，仍会调用工具。作者构建 When2Tool 基准（18 个环境，覆盖计算规模、知识边界、执行可靠性三类工具必要性），系统评估工具调用的必要性判断。关键发现：工具必要性可以从模型的 **hidden states** 中线性解码（AUROC 0.89–0.96），说明模型"已经知道"何时需要工具，但生成阶段未能利用这一知识。基于此提出 **Probe&Prefill**：用轻量级线性探针读取 hidden-state 信号，预填充 steering sentence 引导生成。结果：工具调用减少 48%，准确率仅下降 1.7%，显著优于所有基线。

#### 3 个引导问题

1. **Hidden-state 解码 vs. Verbalized Reasoning**：Probe&Prefill 的 hidden-state 信号（AUROC 0.89+）远优于模型自己 verbalize 的推理。这说明工具必要性是一种"前语言"的表征知识。在更复杂的规划任务中，是否所有决策都可以从 hidden states 中提前解码？这对 CoT 的必要性有什么启示？

2. **Over-tooling 的代价模型**：论文量化了不必要的工具调用对 API 费用和延迟的影响。在实际生产系统中，如何设计一个动态的"工具调用预算"机制，平衡准确率与成本？

3. **Probe&Prefill 的泛化性**：线性探针是在特定模型上训练的。当模型更新（如 GPT-4→GPT-5）或切换到不同架构（如 MoE）时，探针是否需要重新训练？能否设计跨模型的通用工具必要性探针？

#### 重点章节标记

1. **Section 3**：When2Tool 基准设计（18 环境的三类必要性定义）
2. **Section 4.2**：Prompt-only 和 Reason-then-Act 基线的失败分析
3. **Section 5**：Hidden-state 探测实验（AUROC 分析，关键证据）
4. **Section 6**：Probe&Prefill 方法设计与实现
5. **Table 3**：主结果对比（48% 工具调用减少 vs. 基线 6%）

#### 面试谈资

- **30 秒**：LLM Agent 经常过度调用工具。这篇论文发现工具必要性可以从 hidden states 线性解码，提出 Probe&Prefill 方法，减少 48% 工具调用，准确率几乎无损。
- **2 分钟**：核心洞察是 **模型已经知道何时需要工具，但生成机制没有利用这一知识**。When2Tool 基准系统定义了三类工具必要性（计算规模、知识边界、执行可靠性），并通过 hidden-state 探测证明必要性是可解码的。Probe&Prefill 用轻量级探针读取这一信号，通过预填充 steering sentence 引导生成，实现训练无关的干预。局限：探针需要模型访问权限（对黑盒 API 不适用），且线性探针的泛化性有待验证。

---

### 2. Atomix: Timely, Transactional Tool Use for Reliable Agentic Workflows — 工具事务语义

- **作者**：Bardia Mohammadi, Nearchos Potamitis, Lars Klein, Akhil Arora, Laurent Bindschaedler
- **来源**：arXiv 2026-02-16
- **链接**：https://arxiv.org/abs/2602.14849

#### AI 预读（150 字）

> 现代 LLM Agent 工作流日益并发化：多 Agent 共享资源、并行计划探索、推测执行提前启动下游任务。这些模式引入核心问题——**工具效果何时永久化？** Atomix 在工具接口层引入**事务结算（transactional settlement）**机制，将执行、密封（seal）、边界检查（frontier check）、结算（settle）分离。执行阶段记录事务读取资源和可能产生的效果；密封后不再添加新读取/效果；边界检查确认无更早的并发工作可能到达；结算时释放暂存效果、允许不可逆效果出闸。设计适配 Saga、Try-Confirm-Cancel 和流式水位线到 LLM 工具接口，无需修改工具本身。

#### 3 个引导问题

1. **事务粒度与性能**：Atomix 的事务隔离增加了协调开销。在延迟敏感的实时 Agent（如语音助手）中，事务检查是否会成为新的瓶颈？能否设计**乐观事务**或**最终一致性**变体？

2. **不可逆工具的处理**：论文提到"不可逆效果一旦出闸就无法撤销"（如发送邮件）。对于这类工具，是否应该在 Agent 规划阶段就引入**预确认（pre-commit）**机制，让用户或上层策略在结算前审核？

3. **与现有框架的集成**：Atomix 需要 orchestrator 配合进行进度跟踪。在 LangChain、CrewAI 等现有框架中集成 Atomix 的适配层设计复杂度如何？工具适配器（adapter）是否需要为每个工具手写？

#### 重点章节标记

1. **Section 1**：三类并发场景（推测执行、资源争用、不可逆效果）的动机
2. **Section 3**：Atomix 四阶段模型（Execute → Seal → Frontier Check → Settle）
3. **Section 4**：边界检查的形式化定义与 advancement rule
4. **Section 5**：与 Saga、Try-Confirm-Cancel 的对比
5. **Section 6**：实验评估（事务成功率、延迟开销、并发度）

#### 面试谈资

- **30 秒**：Atomix 为 LLM Agent 工具调用引入事务语义，解决并发执行、推测执行和资源争用中的状态一致性问题，无需修改底层工具。
- **2 分钟**：核心设计是**四阶段事务结算**：执行阶段记录读写集合 → 密封阶段冻结事务范围 → 边界检查确认无并发冲突 → 结算阶段提交或补偿。关键洞察来自分布式数据库事务理论（Saga、2PC），但创新在于将其适配到 LLM 工具接口——工具本身无感知，通过适配器拦截和记录。特别处理了**不可逆工具**（如发送邮件）的出闸控制。局限：需要 orchestrator 配合，增加了系统复杂度；延迟开销在实时场景可能成为瓶颈。

---

### 3. PASTE / Act While Thinking — 推测执行加速

- **作者**：Y. Sui, H. Zhao, R. Ma, Z. He, H. Wang, J. Li, Y. Yang
- **来源**：arXiv 2026-03-19
- **链接**：https://arxiv.org/abs/2603.18897
- **相关**：SPORK (arXiv 2607.03333), B-PASTE (arXiv 2604.16469)

#### AI 预读（150 字）

> LLM Agent 的串行"推理→工具调用→观察→再推理"循环中，工具执行时间占总延迟 35–61%，且 GPU 在等待期间空闲。PASTE 提出**模式感知推测工具执行（Pattern-Aware Speculative Tool Execution）**：从 Agent 历史轨迹中挖掘控制流和数据流规律，预测未来工具调用并提前执行。推测结果被隔离直到 LLM 确认；若预测错误则丢弃。PASTE 还联合调度工具执行和返回的 LLM 会话，避免将瓶颈转移到 GPU。实验显示：平均任务完成时间减少 43.5%，工具执行延迟降低 1.8×。后续 SPORK 进一步提出**自推测分叉（Self-Speculative Forking）**，无需历史轨迹，直接从运行中的模型分叉探针预测工具调用。

#### 3 个引导问题

1. **推测错误的代价**：PASTE 从历史模式推测，SPORK 从模型自身推测。当推测错误时，已执行的工具可能产生副作用（如重复查询、资源锁定）。Atomix 的事务机制能否与推测执行结合，实现**可回滚的推测工具调用**？

2. **隐私风险**：推测执行可能提前调用涉及敏感数据的工具（如用户邮箱查询）。Ghost Tool Calls 论文（arXiv 2606.02483）指出推测轨迹会泄露推断意图。如何在加速与隐私之间权衡？

3. **从单工具推测到分支推测**：B-PASTE 将推测从单工具提升到局部执行子图（beam of branches）。在多分支规划中，如何评估不同分支的期望关键路径减少量，而非原始执行概率？

#### 重点章节标记

1. **Section 2**：Agent 执行模型与延迟瓶颈分析（Figure 2：工具时间占比 16–37%）
2. **Section 3**：控制流与数据流模式挖掘
3. **Section 4**：推测执行与隔离机制
4. **Section 5**：联合调度（LLM-Tool Co-Scheduler）
5. **Section 6**：消融实验（PASTE-Tool-Only vs. PASTE-LLM-Only）

#### 面试谈资

- **30 秒**：PASTE 通过从历史轨迹挖掘模式来预测并提前执行工具调用，将 Agent 延迟降低 43.5%；SPORK 进一步实现无需历史数据的自推测分叉。
- **2 分钟**：核心洞察是 **Agent 请求语义多样但控制流稳定**（如"搜索→读取→总结"的固定序列）。PASTE 离线挖掘这些模式，在线推测执行并隔离结果。SPORK 更进一步，利用指令微调模型在完整 CoT 之前就暴露工具意图的特点，从运行模型分叉探针进行自推测。这是一个从**系统优化**到**模型-系统协同设计**的演进。但推测执行引入副作用和隐私风险，需要与事务机制（Atomix）和隐私策略（Ghost Tool Calls 的 Shadow/Rewrite 策略）结合使用。

---

### 4. ReTool: Reinforcement Learning for Strategic Tool Use in LLMs — RL 驱动工具策略

- **作者**：Jiazhan Feng, Shijue Huang, Xingwei Qu, Ge Zhang, Yujia Qin, Baoquan Zhong, Chengquan Jiang, Jinxin Chi, Wanjun Zhong
- **来源**：arXiv 2025-04-15
- **链接**：https://arxiv.org/abs/2504.11536
- **被引**：337+

#### AI 预读（150 字）

> 现有工具学习方法主要依赖 SFT（监督微调）或提示工程，但无法让模型**自主发现何时、如何、以何种顺序调用工具**的最优策略。ReTool 将工具调用建模为强化学习问题，在 RL 训练阶段让模型灵活使用代码解释器。基于 Qwen2.5-32B-Instruct，ReTool 在 AIME2024 达到 67.0%、AIME2025 达到 49.3%，仅用 400 训练步，显著超越文本 RL 基线（40.0% / 36.7%，需 1000+ 步）。结合 DeepSeek-R1-Distill-Qwen-32B 后进一步提升至 72.5% / 54.3%。核心发现：RL 训练不仅扩展了推理能力，还发现了更高效的解题策略。

#### 3 个引导问题

1. **RL 奖励函数设计**：ReTool 的奖励信号来自任务最终正确性（稀疏奖励）。在多步工具调用中，中间步骤的错误选择可能导致探索效率低下。能否设计**过程奖励模型（PRM）**来指导工具调用策略的中间步骤？

2. **工具空间的组合爆炸**：ReTool 聚焦代码解释器（单一工具类型）。在真实场景中，工具集可能包含数十个异构 API。RL 的 action space 如何扩展到高维异构工具选择？

3. **与 SFT 的协同**：ReTool 基于预训练模型进行 RL。如果模型初始不具备基本工具理解能力，RL 是否仍能收敛？是否需要先 SFT 建立工具基础，再用 RL 优化策略？

#### 重点章节标记

1. **Section 3.1**：RL 训练框架（环境定义、状态、动作、奖励）
2. **Section 3.2**：主结果（Table 1：ReTool vs. 文本 RL 基线 vs. s1-32B vs. o1-preview）
3. **Section 4**：训练效率分析（400 步 vs. 1000+ 步的对比）
4. **Section 5**：案例研究——RL 发现的策略 vs. 人类直觉策略的差异
5. **Appendix**：奖励函数细节与超参数

#### 面试谈资

- **30 秒**：ReTool 用强化学习训练 LLM 自主发现最优工具使用策略，在 AIME 数学竞赛上仅用 400 步就超越文本 RL 基线和 OpenAI o1-preview。
- **2 分钟**：核心创新是**将工具调用从监督学习范式转移到策略学习范式**。传统方法（SFT/提示）告诉模型"如何调用工具"，ReTool 让模型在 RL 环境中**探索"何时、是否、以何顺序调用工具"的最优策略**。实验表明 RL 不仅提升最终性能，还**发现了人类未预料到的高效策略**（如跳过某些中间计算步骤）。但局限在于：稀疏奖励导致探索困难，且目前仅验证于代码解释器单一工具；扩展到多工具、多模态工具（如搜索+代码+数据库）的 RL 训练稳定性仍是开放问题。

---

### 5. ToolACE-R: Model-aware Iterative Training and Adaptive Refinement for Tool Learning — 迭代自精炼

- **作者**：Xingshan Zeng, Weiwen Liu, Xu Huang, Zezhong Wang, Lingzhi Wang, Liangyou Li, Yasheng Wang, Lifeng Shang, Xin Jiang, Ruiming Tang, Qun Liu
- **来源**：AAAI 2026
- **链接**：https://ojs.aaai.org/index.php/AAAI/article/view/40759
- **代码**：https://github.com/（论文提及）

#### AI 预读（150 字）

> 现有工具学习方法主要关注数据合成和 SFT，但忽略了如何**充分激发模型自身潜力**。ToolACE-R 提出**模型感知迭代训练（Model-aware Iterative Training）**：根据模型演化中的能力动态调整训练样本难度，实现渐进式学习。同时构建**自精炼语料（Self-Refinement Corpus）**，让模型学习在迭代中改进工具调用，无需外部反馈。在推理阶段，**自适应自精炼（Adaptive Self-Refine）**让模型自主决定何时停止迭代——当连续两次输出相同时终止。在 BFCL 和 API-Bank 基准上，ToolACE-R 达到 GPT-4o 级别性能，且通过自适应精炼可进一步提升。

#### 3 个引导问题

1. **模型感知难度度量**：ToolACE-R 的核心是"模型感知难度"——根据当前模型能力选择合适难度的训练样本。这个难度度量如何定义？是基于模型当前在样本上的错误率，还是基于更细粒度的置信度信号？

2. **自精炼的停止条件**：自适应停止条件是"连续两次输出相同"。这是否会导致过早停止（局部最优）或过晚停止（计算浪费）？能否设计基于**置信度阈值**或**收益递减检测**的更优停止策略？

3. **迭代训练的收敛性**：迭代训练在样本数量不再增加时停止。这是否保证收敛到全局最优？如果模型在某一难度级别"卡住"，迭代训练是否会停滞？

#### 重点章节标记

1. **Section 3.1**：模型感知难度度量定义
2. **Section 3.2**：迭代训练流程（数据选择 → SFT → 新模型 → 重新选择）
3. **Section 3.3**：自精炼语料构建（保留 A₁=A 的样本教模型"无需修改"）
4. **Section 4**：BFCL 和 API-Bank 主结果
5. **Algorithm 1**：自适应自精炼推理流程

#### 面试谈资

- **30 秒**：ToolACE-R 通过模型感知迭代训练和自适应自精炼，让开源模型在工具调用上达到 GPT-4o 水平，且能自主决定何时停止改进。
- **2 分钟**：核心设计是**双循环**：外循环是模型感知迭代训练（根据模型当前能力动态调整训练数据难度），内循环是自适应自精炼（推理时迭代改进直到收敛）。关键洞察是：**保留"无需修改"的样本（A₁=A）教模型学会停止**，这比单纯教模型"如何修改"更重要。实验显示在 BFCL 上超越 GPT-4o，且自适应精炼比固定轮数精炼更高效。局限：迭代训练计算成本高；自精炼的停止条件简单，可能不是最优；目前仅在单轮工具调用验证，多轮对话中的自精炼行为尚未充分研究。

---

### 6. The Evolution of Tool Use in LLM Agents — 综述

- **作者**：Maolin Wang, Yingyi Zhang, Cunyin Peng, Yicheng Chen, Wei Zhou, Jinjie Gu, Chenyi Zhuang, Ruocheng Guo, Bowen Yu, Wanyu Wang, Xiangyu Zhao
- **来源**：ACM Computing Surveys 2026
- **链接**：https://dl.acm.org/doi/10.1145/3788284
- **GitHub 资源索引**：https://github.com/Applied-Machine-Learning-Lab/Awesome-Function-Callings

#### AI 预读（150 字）

> 这是工具调用领域最全面的综述，系统覆盖**工业实践、技术挑战和未来方向**。将工具调用流程分为三阶段：预调用处理（Pre-call）、调用执行（On-call）、调用后验证（Post-call）。涵盖样本构建与微调、部署与推理优化、评估框架（BFCL、API-Bank、ToolSandbox 等）、行业产品（OpenAI Functions、Claude Tools、MCP 等）。特别分析了 200 篇+ 论文，提出未来方向：多模态工具调用、安全与隐私、工具组合推理、边缘部署优化。

#### 3 个引导问题

1. **评估碎片化**：综述列举了 10+ 个评估基准（BFCL、API-Bank、ToolSandbox、τ-Bench 等），但各基准侧重点不同。是否存在一个**统一的评估协议**能覆盖单轮/多轮、简单/复杂、安全/性能全维度？

2. **MCP 生态的标准化**：Model Context Protocol（MCP）正在成为工具调用的"USB-C"标准。综述如何评价 MCP 对工具生态的影响？标准化是否会限制创新，还是促进互操作性？

3. **从工具调用到 Agent 评估**：BFCL 从工具调用评估扩展到 Agent 评估（BFCL-V4）。工具调用能力是否是 Agent 能力的充分指标？还需要哪些额外维度（如长期规划、错误恢复、用户交互）？

#### 重点章节标记

1. **Section 2**：三阶段工具调用流程（Pre-call / On-call / Post-call）
2. **Section 3**：样本构建与微调方法分类
3. **Section 4**：部署与推理优化（缓存、批处理、推测执行）
4. **Section 5**：评估框架对比表
5. **Section 9**：开放问题与未来方向

#### 面试谈资

- **30 秒**：这是工具调用领域的权威综述，覆盖工业实践、技术挑战和未来方向，将工具调用流程系统化分为三阶段，并整理了 200+ 论文和开源资源。
- **2 分钟**：综述的最大价值是**系统化分类**：将碎片化的工具调用研究纳入统一框架（Pre-call → On-call → Post-call），并指出领域正从**单一工具调用**向**多工具编排**、从**能力评估**向**Agent 评估**演进。特别关注了 MCP 协议作为标准化接口的崛起，以及推测执行、缓存优化等系统级创新。作为入门或面试准备，这篇综述提供了完整的知识地图。

---

## 技术栈对比

| 维度 | When2Tool (Sun 2026) | Atomix (Mohammadi 2026) | PASTE/SPORK (Sui 2026) | ReTool (Feng 2025) | ToolACE-R (Zeng 2026) |
|------|----------------------|-------------------------|------------------------|-------------------|----------------------|
| **核心问题** | 过度调用工具 | 并发状态一致性 | 工具延迟瓶颈 | 工具策略优化 | 训练效率与自精炼 |
| **方法类型** | 表征干预（探针） | 事务系统 | 推测执行 | 强化学习 | 迭代训练 + 自精炼 |
| **训练需求** | 无（训练无关） | 无（系统层） | 无/轻量（模式挖掘） | 需 RL 训练 | 需 SFT 迭代训练 |
| **延迟影响** | 降低（减少调用） | 增加（事务开销） | 显著降低（43.5%） | 训练时高，推理时正常 | 推理时增加（迭代） |
| **状态安全** | 无直接影响 | 强（事务隔离） | 弱（推测副作用） | 依赖环境 | 无直接影响 |
| **适用场景** | 所有工具调用 | 并发/多 Agent | 高频工具调用 | 数学/代码推理 | 通用工具调用 |
| **开源代码** | 有 | 未提及 | 未提及 | 未提及 | 未提及 |

---

## 开放问题（面试追问）

1. **推测执行 + 事务 + 隐私的三方权衡**：PASTE 加速但引入副作用和隐私泄露；Atomix 保证一致性但增加延迟；Ghost Tool Calls 保护隐私但限制推测。能否设计一个**统一的推测执行框架**，同时满足加速、安全和一致？

2. **RL 工具策略的泛化性**：ReTool 在数学任务上验证。对于开放式任务（如"帮我规划旅行"），奖励信号稀疏且主观，RL 是否仍然适用？如何设计**可学习的奖励函数**或**人类反馈集成**？

3. **工具调用的"编译时"优化**：现有优化都在运行时（推测、缓存、事务）。能否在 Agent 部署前，通过**静态分析用户请求模式**预生成工具调用计划模板，实现类似"预编译"的加速？

4. **从 Function Calling 到 Agent 生态**：MCP 标准化工具接口，但 Agent 还需要记忆、规划、多 Agent 协作。工具调用是否是 Agent 的"最低层"？上层架构（如 MemGPT、Agent Harness）如何与底层工具优化协同？

5. **多模态工具调用**：现有工作主要聚焦文本 API。当工具涉及图像生成、视频处理、3D 渲染时，参数空间从结构化 JSON 扩展到高维张量，工具调用框架需要哪些根本改变？

---

## 相关资源

| 资源 | 类型 | 链接 | 备注 |
|------|------|------|------|
| Awesome-Function-Callings | GitHub 索引 | https://github.com/Applied-Machine-Learning-Lab/Awesome-Function-Callings | 工具调用论文/代码/数据集全索引 |
| Berkeley Function Calling Leaderboard (BFCL) | 评估基准 | https://gorilla.cs.berkeley.edu/leaderboard.html | 工具调用能力标准评估 |
| Model Context Protocol (MCP) | 协议规范 | https://modelcontextprotocol.io | 工具接口标准化协议 |
| ToolSandbox | 评估基准 | https://arxiv.org/abs/2408.04682 | 有状态、对话式工具评估 |
| When2Tool | 基准/代码 | https://arxiv.org/abs/2605.09252 | 工具必要性判断基准 |
| Atomix | 论文 | https://arxiv.org/abs/2602.14849 | 事务性工具调用 |
| PASTE | 论文 | https://arxiv.org/abs/2603.18897 | 推测执行加速 |
| SPORK | 论文 | https://arxiv.org/abs/2607.03333 | 自推测分叉 |
| ReTool | 论文 | https://arxiv.org/abs/2504.11536 | RL 工具策略 |
| ToolACE-R | 论文 | https://ojs.aaai.org/index.php/AAAI/article/view/40759 | 迭代自精炼 |
| Ghost Tool Calls | 论文 | https://arxiv.org/abs/2606.02483 | 推测执行隐私风险 |

---

## 人类执行任务

- [ ] 精读 When2Tool Section 5（hidden-state 探测实验）+ Section 6（Probe&Prefill）（30 min）
- [ ] 精读 Atomix Section 3（四阶段事务模型）+ Section 4（边界检查形式化）（30 min）
- [ ] 精读 PASTE Section 2（延迟分析）+ Section 4（推测隔离机制）（25 min）
- [ ] 精读 ReTool Section 3（RL 框架）+ Section 5（策略案例）（25 min）
- [ ] 精读 ToolACE-R Section 3.2（迭代训练）+ Algorithm 1（自适应停止）（25 min）
- [ ] 在 Obsidian 中创建 [[When2Tool]], [[Atomix]], [[PASTE]], [[ReTool]], [[ToolACE-R]] 笔记卡片
- [ ] 回答上述引导问题，写入笔记

---

*创建时间：2026-07-12*
*维护者：AIResearchVault*
