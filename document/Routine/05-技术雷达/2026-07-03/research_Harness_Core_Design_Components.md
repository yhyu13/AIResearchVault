# Harness 核心设计组件技术调研报告
## Agent Workflow / Memory Systems / Skill Libraries / Multi-agent Orchestration

**调研维度**: Harness Core Design Components  
**数据来源**: `awesome-agent-harness` 仓库 (502 refs, 2026-05-19 更新)  
**原始论文**: *Agent Systems with Harness Engineering* (OpenReview 2026)  
**调研日期**: 2026-07-03  
**调研员**: 技术调研员 (Harness Core Design Components)

---

## 目录

1. [核心论文清单与一句话贡献](#1-核心论文清单与一句话贡献)
2. [技术演进时间线 (2018→2026)](#2-技术演进时间线-2018→2026)
3. [被证实正确的思想 vs 被淘汰的思想](#3-被证实正确的思想-vs-被淘汰的思想)
4. [核心公司与团队贡献图谱](#4-核心公司与团队贡献图谱)
5. [与实时图形/游戏产业的交叉分析](#5-与实时图形游戏产业的交叉分析)
6. [未来 2-3 年方向预测与技术论证](#6-未来-2-3-年方向预测与技术论证)
7. [参考文献](#7-参考文献)

---

## 1. 核心论文清单与一句话贡献

### 1.1 Agent Workflow (智能体工作流)

| 论文 | 作者 | 会议/期刊 | 年份 | 一句话核心贡献 |
|------|------|-----------|------|----------------|
| Chain-of-Thought Prompting Elicits Reasoning in Large Language Models | Wei et al. (Google) | NeurIPS | 2022 | 通过 few-shot 示例中的中间推理步骤，首次证明 LLM 可被 prompt 诱导出多步推理能力，打破"模型越大推理越强"的 flat scaling curve。 |
| ReAct: Synergizing Reasoning and Acting in Language Models | Yao et al. (Princeton + Google) | ICLR | 2023 | 提出 **Thought → Action → Observation** 的交错循环范式，将 chain-of-thought 推理与外部环境交互统一，在 ALFWorld 上比纯 RL 方法提升 34% 成功率。 |
| Tree of Thoughts: Deliberate Problem Solving with Large Language Models | Yao et al. | NeurIPS | 2023 | 将 CoT 的线性推理链推广为树形搜索结构，允许 LLM 通过 BFS/DFS 主动探索多条推理路径并自我评估，实现"深思熟虑"的问题求解。 |
| Graph of Thoughts: Solving Elaborate Problems with Large Language Models | Besta et al. (ETH Zürich) | AAAI | 2024 | 将推理拓扑进一步推广为有向图，支持任意聚合、循环和条件分支，使复杂多步推理的分解与重组具备图结构灵活性。 |
| AFlow: Automating Agentic Workflow Generation | FoundationAgents | ICLR | 2025 | 提出自动化 agent workflow 生成框架，通过搜索+优化自动发现最优工作流拓扑，减少对人工设计的依赖。 |
| Agentic Reasoning: A Streamlined Framework for Enhancing LLM Reasoning with Agentic Tools | — | ACL | 2025 | 将 agentic 工具调用与推理流程精简整合，提出更紧凑的 reasoning-action 统一框架。 |
| HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face | Shen et al. (Microsoft) | NeurIPS | 2023 | 以 LLM 作为中央控制器，自动解析用户意图并调度 HuggingFace 生态中的专用模型，实现多模型协作的任务解决。 |
| OpenManus: An Open-source Framework for Building General AI Agents | FoundationAgents | Repo | 2025 | 开源通用 AI Agent 构建框架，提供可扩展的 agent 工作流基础设施。 |

**子领域：Environment Perception (环境感知)**

| 论文 | 作者 | 会议 | 年份 | 一句话核心贡献 |
|------|------|------|------|----------------|
| Mind2Web: Towards a Generalist Agent for the Web | OSU NLP | NeurIPS | 2023 | 构建大规模网页交互数据集，定义了网页 agent 的 observation→action 标准范式。 |
| WebArena: A Realistic Web Environment for Building Autonomous Agents | — | ICLR | 2024 | 提供高保真真实网页环境，用于评估端到端 web agent 的自主决策能力。 |
| OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments | — | NeurIPS | 2024 | 将 agent 环境从浏览器扩展到完整操作系统，引入多模态感知与开放域任务。 |
| SeeClick: Harnessing GUI Grounding for Advanced Visual GUI Agents | — | ACL | 2024 | 提出基于视觉的 GUI grounding 方法，使 agent 能直接理解屏幕像素而非仅依赖 HTML。 |
| GUI-Actor: Coordinate-Free Visual Grounding for GUI Agents | Microsoft | NeurIPS | 2025 | 提出无坐标视觉定位，提升 GUI agent 的跨分辨率泛化能力。 |

**子领域：Task Planning (任务规划)**

| 论文 | 作者 | 会议 | 年份 | 一句话核心贡献 |
|------|------|------|------|----------------|
| Least-to-Most Prompting Enables Complex Reasoning in Large Language Models | Zhou et al. (Google) | ICLR | 2023 | 将复杂问题分解为子问题序列，由易到难逐步解决，降低单次推理的认知负荷。 |
| AvaTaR: Optimizing LLM Agents for Tool Usage via Contrastive Reasoning | — | NeurIPS | 2024 | 通过对比推理优化工具使用策略，使 agent 在工具选择时具备判别式决策能力。 |
| AFlow: Automating Agentic Workflow Generation | FoundationAgents | ICLR | 2025 | 自动搜索最优 agent 工作流拓扑，将 workflow 设计从手工工程转变为可优化问题。 |
| GAP: Graph-Based Agent Planning with Parallel Tool Use and RL | — | arXiv | 2025 | 将任务规划建模为图结构，支持并行工具调用与强化学习优化。 |

**子领域：Action Execution (动作执行)**

| 论文 | 作者 | 会议 | 年份 | 一句话核心贡献 |
|------|------|------|------|----------------|
| Toolformer: Language Models Can Teach Themselves to Use Tools | Schick et al. (Meta) | NeurIPS | 2023 | 首个自监督工具学习框架：LLM 通过预测"哪些 API 调用能降低未来 token 损失"来自学工具使用，无需人工标注。 |
| Code as Policies: Language Model Programs for Embodied Control | Google Research | ICRA | 2023 | 将自然语言指令编译为可执行代码策略，使 LLM 直接生成机器人控制程序。 |
| SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering | Princeton NLP | NeurIPS | 2024 | 设计专门的 agent-computer 接口，将 LLM 与软件工程环境桥接，实现自动化 bug 修复。 |
| AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents | — | ACL | 2024 | 构建可控的应用程序+用户交互世界，为 coding agent 提供标准化评估环境。 |
| Robust Tool Use via Fission-GRPO: Learning to Recover from Execution Errors | — | arXiv | 2026 | 通过 Fission-GRPO 训练 agent 从工具执行错误中恢复，提升鲁棒性。 |

---

### 1.2 Memory Systems (记忆系统)

#### 1.2.1 Short-term Memory (短期记忆)

**Working Memory (工作记忆)**

| 论文 | 作者 | 会议 | 年份 | 一句话核心贡献 |
|------|------|------|------|----------------|
| ReAct | Yao et al. | ICLR | 2023 | 将工作记忆隐含在 Thought-Action-Observation 循环的上下文窗口中，作为当前推理状态的载体。 |
| ReadAgent: A Human-Inspired Reading Agent with Gist Memory of Very Long Contexts | — | ICML | 2024 | 受人类 gist memory 启发，将超长文档压缩为要点记忆，支持检索增强的长文本阅读。 |
| Agent Workflow Memory | — | ICML | 2025 | 将工作记忆显式建模为 agent 工作流状态，支持跨会话的任务状态持久化。 |
| Memo: Training Memory-Efficient Embodied Agents with RL | — | NeurIPS | 2025 | 通过强化学习训练记忆高效的具身 agent，优化工作记忆的存储与检索策略。 |
| Graph-based Agent Memory: Taxonomy, Techniques, and Applications | — | arXiv | 2026 | 系统梳理基于图结构的 agent 记忆分类体系、技术方法与应用场景。 |

**Conversational Memory (对话记忆)**

| 论文 | 作者 | 会议 | 年份 | 一句话核心贡献 |
|------|------|------|------|----------------|
| MemGPT: Towards LLMs as Operating Systems | Packer et al. | arXiv | 2023 | **开创性工作**：将 OS 虚拟内存管理隐喻引入 LLM，通过分层存储（主上下文/召回/归档）和显式读写操作，突破上下文窗口限制。 |
| Zep: A Temporal Knowledge Graph Architecture for Agent Memory | — | arXiv | 2025 | 构建时序知识图谱作为对话记忆，支持时间感知的记忆检索与推理。 |
| From Isolated Conversations to Hierarchical Schemas: Dynamic Tree Memory Representation for LLMs | — | ICLR | 2025 | 将对话记忆从扁平序列提升为动态树形模式，支持层次化记忆组织。 |
| SeCom: On Memory Construction and Retrieval for Personalized Conversational Agents | — | ICLR | 2025 | 针对个性化对话 agent 的记忆构建与检索机制进行系统研究。 |
| Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for LLM Agents | — | arXiv | 2026 | 统一长短期记忆管理，通过学习方法动态决定记忆的存储、更新与遗忘策略。 |
| FluxMem: Adaptive Hierarchical Memory for Streaming Video Understanding | — | CVPR | 2026 | 为流式视频理解设计自适应层次记忆，支持实时视觉信息的动态记忆管理。 |

#### 1.2.2 Long-term Memory (长期记忆)

**Structured Memory (结构化记忆)**

| 论文 | 作者 | 会议 | 年份 | 一句话核心贡献 |
|------|------|------|------|----------------|
| Generative Agents: Interactive Simulacra of Human Behavior | Park et al. (Stanford) | UIST | 2023 | **里程碑工作**：构建 25 个 AI 智能体的虚拟小镇，提出 observation → retrieval → reflection → planning 的完整记忆架构，展现涌现社会行为。 |
| Optimus-1: Hybrid Multimodal Memory Empowered Agents Excel in Long-Horizon Tasks | — | NeurIPS | 2024 | 混合多模态记忆架构，使 agent 在长时程任务中有效利用视觉+文本记忆。 |
| A-Mem: Agentic Memory for LLM Agents | Xu et al. | NeurIPS | 2025 | 受 Zettelkasten 卡片笔记法启发，构建自主链接、动态演化的结构化记忆网络。 |
| Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory | — | ECAI | 2025 | 面向生产的可扩展长期记忆系统，支持实体关系图谱与动态记忆更新。 |
| G-Memory: Tracing Hierarchical Memory for Multi-Agent Systems | — | NeurIPS | 2025 | 为_multi-agent_ 系统追踪层次化记忆，支持跨 agent 的记忆共享与继承。 |
| Graph-Native Cognitive Memory for AI Agents: Formal Belief Revision Semantics for Versioned Memory Architectures | — | arXiv | 2026 | 提出图原生认知记忆与信念修正语义，支持版本化记忆架构的形式化推理。 |

**Unstructured Memory (非结构化记忆)**

| 论文 | 作者 | 会议 | 年份 | 一句话核心贡献 |
|------|------|------|------|----------------|
| Reflexion: Language Agents with Verbal Reinforcement Learning | Shinn et al. | NeurIPS | 2023 | 通过自然语言反思实现 verbal RL，将失败经验以非结构化文本形式存入记忆，指导后续行为改进。 |
| MemoryBank: Enhancing Large Language Models with Long-Term Memory | Zhong et al. | AAAI | 2024 | 基于艾宾浩斯遗忘曲线设计记忆强化与衰减机制，实现用户感知的长期个性化记忆。 |
| Memory-R1: Enhancing LLM Agents to Manage and Utilize Memories via RL | — | arXiv | 2025 | 通过强化学习训练 agent 主动管理记忆，将记忆操作视为可学习的策略。 |
| MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents | Microsoft | ICLR | 2026 | 学习记忆与推理的协同机制，使长时程 agent 能高效利用记忆辅助决策。 |
| MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent | ByteDance | ICLR | 2026 | 用多轮对话强化学习重塑长上下文 LLM 的记忆机制，实现动态记忆塑形。 |
| RetroAgent: From Solving to Evolving via Retrospective Dual Intrinsic Feedback | — | arXiv | 2026 | 通过回顾性双内在反馈机制，使 agent 从解决问题进化为自我进化。 |

---

### 1.3 Skill Libraries (技能库)

#### 1.3.1 Skill Acquisition (技能获取)

**Learning from Demonstration (从演示学习)**

| 论文 | 作者 | 会议 | 年份 | 一句话核心贡献 |
|------|------|------|------|----------------|
| Toolformer | Schick et al. (Meta) | NeurIPS | 2023 | 自监督学习工具使用，为 skill acquisition 提供"零标注"范式。 |
| Large Language Models as Tool Makers | — | ICLR | 2024 | LLM 不仅使用工具，还能创造新工具，将技能获取扩展到工具生成层面。 |
| Gorilla: Large Language Model Connected with Massive APIs | — | NeurIPS | 2024 | 将 LLM 与海量 API 连接，通过检索增强实现大规模工具/技能调用。 |
| Voyager: An Open-Ended Embodied Agent with Large Language Models | Wang et al. (NVIDIA/Caltech/Stanford) | TMLR | 2024 | **里程碑**：Minecraft 中首个终身学习 agent，通过自动课程+可执行代码技能库+迭代提示，实现无人类干预的开放域技能积累。 |
| Synatra: Turning Indirect Knowledge into Direct Demonstrations for Digital Agents at Scale | — | NeurIPS | 2024 | 将间接知识转化为可直接执行的数字 agent 演示，规模化技能获取。 |
| ToolACE: Winning the Points of LLM Function Calling | — | ICLR | 2025 | 针对 LLM 函数调用的系统化数据生成与训练方法。 |
| SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills | — | arXiv | 2025 | Web agent 通过发现与打磨技能实现自我改进。 |
| Agent Skill Acquisition for Large Language Models via CycleQD | Sakana AI | arXiv | 2025 | 通过 CycleQD 循环质量多样性算法实现 agent 技能获取。 |
| SoK: Agentic Skills - Beyond Tool Use in LLM Agents | — | arXiv | 2026 | 系统综述 agentic skills 的概念、分类与超越工具使用的扩展。 |
| SkillCraft: Can LLM Agents Learn to Use Tools Skillfully? | — | arXiv | 2026 | 系统研究 LLM agent 是否能真正"熟练"使用工具，而非简单调用。 |
| Trace2Skill: Distill Trajectory-Local Lessons into Transferable Agent Skills | — | arXiv | 2026 | 将轨迹中的局部经验提炼为可迁移的 agent 技能。 |

**Learning from Experience (从经验学习)**

| 论文 | 作者 | 会议 | 年份 | 一句话核心贡献 |
|------|------|------|------|----------------|
| ExpeL: LLM Agents Are Experiential Learners | — | AAAI | 2024 | 证明 LLM agent 可以通过经验学习，从过往交互中提取可复用知识。 |
| OS-Copilot: Towards Generalist Computer Agents with Self-Improvement | — | ICLR | 2024 | 通用计算机 agent 通过自我改进持续积累操作技能。 |
| Reinforcement Learning for Self-Improving Agent with Skill Library | Amazon Science | arXiv | 2025 | 用强化学习驱动带技能库的 agent 自我改进。 |
| Toward Training Superintelligent Software Agents through Self-Play SWE-RL | — | ICML | 2026 | 通过自我对弈强化学习训练超智能软件工程 agent。 |
| SkillRL: Evolving Agents via Recursive Skill-Augmented RL | — | ICLR Workshop | 2026 | 递归技能增强强化学习，使 agent 通过技能组合实现能力进化。 |
| Tool-R0: Self-Evolving LLM Agents for Tool-Learning from Zero Data | — | arXiv | 2026 | 零数据启动的自我进化工具学习 agent。 |
| AutoSkill: Experience-Driven Lifelong Learning via Skill Self-Evolution | — | arXiv | 2026 | 经验驱动的终身学习，通过技能自我进化实现持续成长。 |
| SKILL0: In-Context Agentic Reinforcement Learning for Skill Internalization | ZJU | arXiv | 2026 | 上下文内 agentic 强化学习，将技能内化到模型参数中。 |

**Learning from External Resources (从外部资源学习)**

| 论文 | 作者 | 类型 | 年份 | 一句话核心贡献 |
|------|------|------|------|----------------|
| Equipping Agents for the Real World with Agent Skills | Anthropic | Blog | 2025 | Anthropic 官方阐述 agent skills 的设计理念与工程实践。 |
| Agent Skills | OpenAI / Claude | Docs | 2025-2026 | 主流平台将 skills 作为一等公民纳入 agent 架构设计。 |
| SKILLFOUNDRY: Building Self-Evolving Agent Skill Libraries from Heterogeneous Scientific Resources | — | arXiv | 2026 | 从异构科学资源构建自我进化的 agent 技能库。 |

#### 1.3.2 Skill Management (技能管理)

**Skill Representation (技能表示)**

| 论文 | 作者 | 会议 | 年份 | 一句话核心贡献 |
|------|------|------|------|----------------|
| Voyager | Wang et al. | TMLR | 2024 | 以可执行代码（JavaScript 函数）作为技能表示，通过文本嵌入索引实现检索与组合。 |
| Inducing Programmatic Skills for Agentic Tasks | — | COLM | 2025 | 诱导生成程序化技能，使技能具备可解释性与可组合性。 |
| ToolGen: Unified Tool Retrieval and Calling via Generation | — | ICLR | 2025 | 统一工具检索与调用为生成任务，简化技能表示与使用接口。 |
| Evolving Programmatic Skill Networks | — | arXiv | 2026 | 进化式程序化技能网络，支持技能的动态演化与重组。 |
| CUA-Skill: Develop Skills for Computer Using Agent | Microsoft | arXiv | 2026 | 为计算机使用 agent 开发专用技能集。 |
| SkillFlow: Scalable and Efficient Agent Skill Retrieval System | — | arXiv | 2026 | 可扩展高效的 agent 技能检索系统。 |
| Graph of Skills: Dependency-Aware Structural Retrieval for Massive Agent Skills | — | arXiv | 2026 | 基于技能依赖关系的图结构检索，支持大规模技能库的高效组织。 |
| SkillRouter: Skill Routing for LLM Agents at Scale | — | arXiv | 2026 | 大规模 LLM agent 的技能路由机制，动态选择最优技能路径。 |

**Skill Retrieval (技能检索)**

| 论文 | 作者 | 会议 | 年份 | 一句话核心贡献 |
|------|------|------|------|----------------|
| Voyager | Wang et al. | TMLR | 2024 | 基于文本嵌入的相似度检索，从技能库中召回相关可执行代码。 |
| SRSA: Skill Retrieval and Adaptation for Robotic Assembly Tasks | — | ICLR | 2025 | 针对机器人装配任务的技能检索与自适应迁移。 |
| EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle | — | arXiv | 2025 | 经验驱动的生命周期自我进化，包含动态技能检索与更新。 |
| IntentCUA: Learning Intent-level Representations for Skill Abstraction and Multi-Agent Planning | — | arXiv | 2026 | 学习意图级表示用于技能抽象与多 agent 规划。 |
| GraphSkill: Documentation-Guided Hierarchical Retrieval-Augmented Coding for Complex Graph Reasoning | — | arXiv | 2026 | 文档引导的层次化检索增强编码，用于复杂图推理技能。 |
| WebXSkill: Skill Learning for Autonomous Web Agents | — | arXiv | 2026 | 自主 Web agent 的技能学习框架。 |
| Skill Retrieval Augmentation for Agentic AI | — | arXiv | 2026 | 系统研究技能检索增强对 agentic AI 的贡献。 |

#### 1.3.3 Skill Maintenance (技能维护)

| 论文 | 作者 | 类型 | 年份 | 一句话核心贡献 |
|------|------|------|------|----------------|
| Using Skills to Accelerate OSS Maintenance | OpenAI | Blog | 2026 | 用技能加速开源软件维护，展示技能库在工程实践中的价值。 |
| Shell + Skills + Compaction: Tips for Long-Running Agents | OpenAI | Blog | 2026 | 长时程 agent 的技能管理最佳实践：shell 访问 + 技能组合 + 上下文压缩。 |
| Testing Agent Skills Systematically with Evals | OpenAI | Blog | 2026 | 系统化评估 agent skills 的方法论。 |
| Towards Secure Agent Skills: Architecture, Threat Taxonomy, and Security Analysis | — | arXiv | 2026 | 首次系统分析 agent skills 的安全架构与威胁模型。 |

---

### 1.4 Multi-agent Orchestration (多智能体编排)

#### 1.4.1 Coordination Architectures (协调架构)

**Centralized Architectures (集中式架构)**

| 论文 | 作者 | 会议 | 年份 | 一句话核心贡献 |
|------|------|------|------|----------------|
| ChatDev: Communicative Agents for Software Development | OpenBMB | ACL | 2024 | 多 agent 通过自然语言通信协作完成软件开发，定义了角色分工（CEO/CTO/程序员等）的集中式协调范式。 |
| MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework | — | ICLR | 2024 | **里程碑**：将人类软件开发流程（SOP）编码为 meta-programming，通过角色专用 agent 实现结构化协作，ICLR 2024 oral (top 1.2%)。 |
| AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversations | Microsoft | COLM | 2024 | 以对话为核心的多 agent 框架，支持可定制的对话模式与工具使用，获 COLM 2024 best paper。 |
| AutoAgents: A Framework for Automatic Agent Generation | — | IJCAI | 2024 | 自动 agent 生成框架，根据任务需求动态创建专用 agent。 |
| Scaling Large Language Model-based Multi-Agent Collaboration | OpenBMB | ICLR | 2025 | 系统研究 LLM-based 多 agent 协作的规模化问题。 |
| Agent S2: A Compositional Generalist-Specialist Framework for Computer Use Agents | — | COLM | 2025 | 通用-专家组合框架，平衡多 agent 系统的泛化与专精能力。 |
| MegaAgent: A Large-Scale Autonomous LLM-based Multi-Agent System Without Predefined SOPs | — | ACL Findings | 2025 | 无需预定义 SOP 的大规模自主多 agent 系统。 |
| Multi-Agent Collaboration via Evolving Orchestration | OpenBMB | NeurIPS | 2025 | 通过进化式编排动态调整多 agent 协作策略。 |

**Decentralized Architectures (去中心化架构)**

| 论文 | 作者 | 会议 | 年份 | 一句话核心贡献 |
|------|------|------|------|----------------|
| CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society | — | NeurIPS | 2023 | 提出"角色扮演"驱动的去中心化多 agent 交互，探索 LLM 社会的涌现行为。 |
| AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors | OpenBMB | arXiv | 2023 | 构建多 agent 协作平台，系统研究涌现行为的产生条件。 |
| ProAgent: Building Proactive Cooperative Agents with Large Language Models | — | AAAI | 2024 | 构建主动协作 agent，使 agent 能预判他人需求并主动提供帮助。 |
| A Dynamic LLM-Powered Agent Network for Task-Oriented Agent Collaboration | SALT NLP | COLM | 2024 | 动态 agent 网络，根据任务需求自适应调整协作拓扑。 |
| CONSENSAGENT: Towards Efficient and Effective Consensus in Multi-Agent LLM Interactions Through Sycophancy Mitigation | — | ACL Findings | 2025 | 解决多 agent 交互中的谄媚问题，提升共识达成的效率与有效性。 |
| AgentOrchestra: Orchestrating Multi-Agent Intelligence with the TEA Protocol | — | arXiv | 2025 | 提出 Tool-Environment-Agent (TEA) 协议，标准化多 agent 编排接口。 |
| LLM-Driven Multi-Agent Architectures for Intelligent Self-Organizing Networks | — | IEEE Network | 2025 | 将多 agent 架构应用于智能自组织网络。 |
| Building a C Compiler with a Team of Parallel Claudes | Anthropic | Blog | 2026 | 工程实践：用并行 Claude 实例协作构建 C 编译器，展示去中心化多 agent 在复杂工程任务中的可行性。 |

#### 1.4.2 Communication Mechanisms (通信机制)

**Debate-based Methods (辩论式方法)**

| 论文 | 作者 | 会议 | 年份 | 一句话核心贡献 |
|------|------|------|------|----------------|
| Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate | — | EMNLP | 2024 | 通过多 agent 辩论激发 LLM 的发散思维，提升创意任务表现。 |
| Should we be going MAD? A Look at Multi-Agent Debate Strategies for LLMs | — | ICML | 2024 | 系统评估多 agent 辩论策略的有效性，提出最优辩论协议。 |
| RoleLLM: Benchmarking, Eliciting, and Enhancing Role-Playing Abilities of Large Language Models | — | ACL Findings | 2024 | 系统评估与增强 LLM 的角色扮演能力，为多 agent 角色分工提供基础。 |
| Debate-to-Write: A Persona-Driven Multi-Agent Framework for Diverse Argument Generation | — | COLING | 2025 | 角色驱动的辩论-写作框架，生成多样化论证。 |
| Reinforce LLM Reasoning through Multi-Agent Reflection | — | ICML | 2025 | 通过多 agent 反思强化 LLM 推理能力。 |
| Player-Coach Teamwork: Multi-agent Collaboration for Improving LLM Reasoning | — | NeurIPS Workshop | 2025 | 球员-教练式协作模式，提升 LLM 推理的多 agent 协作效率。 |

**Collaboration-based Methods (协作式方法)**

| 论文 | 作者 | 会议 | 年份 | 一句话核心贡献 |
|------|------|------|------|----------------|
| ChatDev | OpenBMB | ACL | 2024 | 自然语言通信驱动的软件开发多 agent 协作。 |
| MetaGPT | — | ICLR | 2024 | 基于 SOP 的结构化协作，将人类工作流程编码为 agent 协作协议。 |
| GPTSwarm: Language Agents as Optimizable Graphs | — | ICML | 2024 | 将语言 agent 建模为可优化图结构，支持协作拓扑的自动优化。 |
| Long-Horizon Planning for Multi-Agent Robots in Partially Observable Environments | — | NeurIPS | 2024 | 部分可观测环境下的多机器人长时程规划。 |
| MapCoder: Multi-Agent Code Generation for Competitive Problem Solving | — | ACL | 2024 | 多 agent 协作代码生成，用于竞赛级问题求解。 |
| Flow-of-Action: SOP Enhanced LLM-Based Multi-Agent System for Root Cause Analysis | — | WWW | 2025 | SOP 增强的多 agent 根因分析系统。 |
| MAPoRL: Multi-Agent Post-Co-Training for Collaborative LLMs with RL | — | ACL | 2025 | 多 agent 后协同训练，用强化学习优化协作 LLM。 |
| MARFT: Multi-Agent Reinforcement Fine-Tuning | — | arXiv | 2025 | 多 agent 强化微调，提升协作策略的稳定性。 |
| Multi-Agent Collaboration via Evolving Orchestration | OpenBMB | NeurIPS | 2025 | 进化式编排的动态协作机制。 |
| Chain-of-Agents: End-to-End Agent Foundation Models via Multi-Agent Distillation and Agentic RL | OPPO | arXiv | 2025 | 通过多 agent 蒸馏与 agentic RL 构建端到端 agent 基础模型。 |
| How and When to Build Multi-Agent Systems | LangChain | Blog | 2025 | 业界实践指南：何时以及如何选择多 agent 架构。 |
| Don't Build Multi-Agents | Cognition AI | Blog | 2025 | 反向观点：并非所有问题都需要多 agent 架构。 |
| Toward Autonomous Long-Horizon Engineering for ML Research | — | arXiv | 2026 | 面向 ML 研究的自主长时程工程多 agent 系统。 |

---

## 2. 技术演进时间线 (2018→2026)

### 2.1 总体演进脉络

```
2018-2021: 前 Agent 时代
  └── RL 环境接口 (OpenAI Gym 2016) → 软件测试 Harness (JUnit 1999)
  └── LLM 作为纯文本生成器，无环境交互能力

2022: 推理觉醒
  └── Chain-of-Thought (NeurIPS 2022) — LLM 首次展现多步推理能力
  └── "Let's think step by step" 成为标准 prompt

2023: Agent 元年 — 从推理到行动
  ├── Q1: Toolformer (NeurIPS 2023) — LLM 自学工具使用
  ├── Q2: Generative Agents (UIST 2023) — 完整记忆架构 + 涌现行为
  ├── Q2: Voyager (arXiv 2023) — 终身学习 + 技能库
  ├── Q3: ReAct (ICLR 2023) — 推理-行动交错循环
  ├── Q3: MemGPT (arXiv 2023) — OS 式虚拟内存管理
  ├── Q3: CAMEL (NeurIPS 2023) — 多 agent 角色扮演
  ├── Q4: Tree of Thoughts (NeurIPS 2023) — 树形推理搜索
  └── Q4: AgentVerse (arXiv 2023) — 多 agent 涌现行为研究

2024: 系统化与规模化
  ├── Q1: Graph of Thoughts (AAAI 2024) — 图结构推理
  ├── Q1: MemoryBank (AAAI 2024) — 遗忘曲线记忆
  ├── Q1: MetaGPT (ICLR 2024) — SOP 编码的多 agent 协作
  ├── Q1: AutoGen (COLM 2024) — 对话式多 agent 框架
  ├── Q2: ChatDev (ACL 2024) — 软件工程多 agent
  ├── Q2: ExpeL (AAAI 2024) — 经验学习 agent
  ├── Q3: OS-Copilot (ICLR 2024) — 通用计算机 agent
  ├── Q3: ReadAgent (ICML 2024) — Gist 工作记忆
  └── Q4: A-Mem (NeurIPS 2025) — Zettelkasten 记忆

2025: 自动化与自我进化
  ├── Q1: AFlow (ICLR 2025) — 自动工作流生成
  ├── Q1: Agent Workflow Memory (ICML 2025) — 工作流状态记忆
  ├── Q2: Mem0 (ECAI 2025) — 生产级长期记忆
  ├── Q2: SkillWeaver (arXiv 2025) — 自我改进技能获取
  ├── Q3: Multi-Agent Collaboration via Evolving Orchestration (NeurIPS 2025) — 进化式编排
  ├── Q4: Agentic Memory (arXiv 2026) — 统一记忆管理
  └── Q4: MARFT (arXiv 2025) — 多 agent 强化微调

2026: 收敛与工业落地
  ├── Q1: SkillsBench, SkillX — 技能评估与自动构建
  ├── Q1: MEM1 (ICLR 2026) — 记忆-推理协同
  ├── Q2: MemAgent (ICLR 2026) — RL 记忆塑形
  ├── Q2: SkillRL (ICLR Workshop 2026) — 递归技能增强 RL
  ├── Q3: SKILL0, AutoSkill — 零数据/经验驱动技能进化
  ├── Q4: AgentSys (arXiv 2026) — 安全动态层次记忆
  └── Q4: SafeHarness (arXiv 2026) — 生命周期安全架构
```

### 2.2 关键转折点

| 时间 | 事件 | 意义 |
|------|------|------|
| 2022-11 | Chain-of-Thought (NeurIPS) | **推理觉醒**：证明 LLM 可通过 prompt 诱导出多步推理，开启 agent 时代认知基础。 |
| 2023-03 | Toolformer (NeurIPS) | **工具觉醒**：LLM 首次能自主学习外部工具使用，突破纯文本生成边界。 |
| 2023-04 | Generative Agents (UIST) | **记忆觉醒**：首次构建完整记忆架构（观察-检索-反思-规划），证明涌现社会行为。 |
| 2023-05 | Voyager (arXiv) | **终身学习觉醒**：开放域终身学习 agent，自动课程+技能库+迭代提示的三位一体。 |
| 2023-10 | ReAct (ICLR) | **行动觉醒**：将推理与行动统一为交错循环，成为 agent 工作流的 de facto 标准。 |
| 2023-10 | MemGPT (arXiv) | **系统觉醒**：将 OS 虚拟内存隐喻引入 LLM，为长上下文管理提供工程化方案。 |
| 2024-01 | MetaGPT (ICLR) | **协作觉醒**：将人类 SOP 编码为 agent 协作协议，多 agent 从玩具走向工程。 |
| 2024-08 | AutoGen (COLM) | **框架觉醒**：对话式多 agent 框架获 best paper，标志多 agent 成为主流研究方向。 |
| 2025-01 | AFlow (ICLR) | **自动化觉醒**：工作流设计从手工工程转变为自动搜索优化。 |
| 2025-04 | Mem0 (ECAI) | **产品觉醒**：长期记忆从研究概念走向生产就绪系统。 |
| 2026-01 | Agentic Memory (arXiv) | **统一觉醒**：长短期记忆管理从分离架构走向统一学习框架。 |

---

## 3. 被证实正确的思想 vs 被淘汰的思想

### 3.1 被证实正确的思想 (Proven Correct)

| 思想 | 首次提出 | 证实证据 | 当前状态 |
|------|----------|----------|----------|
| **推理与行动需要交错进行** | ReAct (2023) | 在 ALFWorld 上比纯 RL 提升 34%，比纯 CoT 减少幻觉；成为 OpenAI/Anthropic/Claude Code 的默认架构 | ✅ 行业标准 |
| **工具使用可通过自监督学习** | Toolformer (2023) | 无需人工标注即可学会调用计算器/搜索引擎/日历等工具；后续 ToolLLM (16K+ APIs) 验证可扩展性 | ✅ 核心能力 |
| **记忆需要分层管理** | MemGPT (2023) | OS 虚拟内存隐喻被 Mem0/A-Mem/AgentSys 等后续工作继承；上下文窗口限制客观存在 | ✅ 工程共识 |
| **技能应以可执行代码表示** | Voyager (2023) | 代码形式的技能具备可解释性、可组合性、可验证性；被 SWE-agent/Claude Code 等工程系统采纳 | ✅ 工程共识 |
| **多 agent 需要角色分工** | MetaGPT/ChatDev (2024) | 角色化分工使多 agent 协作可结构化、可调试；AutoGen 获 COLM best paper | ✅ 设计模式 |
| **工作流应自动优化** | AFlow (2025) | 自动搜索的工作流在多个 benchmark 上超越手工设计；减少人工 prompt 工程依赖 | ✅ 新兴共识 |
| **记忆管理应通过学习优化** | Memory-R1/MEM1 (2025-2026) | 将记忆操作建模为可学习策略，通过 RL 优化，在长时程任务中超越固定启发式 | ✅ 前沿方向 |
| **多 agent 协作需要动态编排** | Evolving Orchestration (2025) | 静态 SOP 无法适应任务变化；进化式编排动态调整角色与通信拓扑 | ✅ 前沿方向 |

### 3.2 被淘汰或边缘化的思想 (Eliminated/Marginalized)

| 思想 | 首次提出 | 淘汰原因 | 当前状态 |
|------|----------|----------|----------|
| **纯 prompt 工程无需结构化工作流** | 早期 GPT-3 应用 (2020-2021) | 复杂任务中纯 prompt 无法保证一致性；ReAct/CoT 证明需要显式推理结构 | ❌ 已淘汰 |
| **单 agent 可解决所有问题** | 早期 AutoGPT/BabyAGI (2023) | 单 agent 在长时程任务中上下文爆炸、错误累积；多 agent 协作成为主流 | ❌ 已淘汰 |
| **记忆只需简单向量检索** | 早期 RAG 应用 (2022-2023) | 纯向量检索缺乏时间感知、重要性排序、遗忘机制；MemGPT/Generative Agents 证明需要分层架构 | ❌ 已边缘化 |
| **技能只需手工编写** | 早期 tool use (2022) | 手工工具无法覆盖开放域需求；Voyager/Toolformer 证明需要自动学习与积累 | ❌ 已边缘化 |
| **多 agent 必须预定义 SOP** | MetaGPT/ChatDev (2024) | 静态 SOP 无法适应动态环境；MegaAgent (2025) 证明无预定义 SOP 也可协作 | ⚠️ 正在演进 |
| **所有任务都需要多 agent** | 2024 年多 agent 热潮 | Cognition AI (2025) 提出 "Don't Build Multi-Agents"；简单任务单 agent 更高效 | ⚠️ 理性回归 |
| **记忆只需存储原始交互** | 早期对话系统 (2022) | 原始交互序列过长且噪声大；ReadAgent/Agent Workflow Memory 证明需要压缩与结构化 | ❌ 已淘汰 |

---

## 4. 核心公司与团队贡献图谱

### 4.1 学术机构

| 机构 | 代表工作 | 核心贡献 |
|------|----------|----------|
| **Princeton University** | ReAct, Tree of Thoughts | 奠定了 agent 推理-行动循环与树形搜索的理论基础 |
| **Stanford University** | Generative Agents | 开创了记忆架构与涌现社会行为的实证研究 |
| **NVIDIA + Caltech + UT Austin** | Voyager | 首次实现开放域终身学习 agent，定义技能库范式 |
| **OpenBMB (清华)** | ChatDev, MetaGPT, AgentVerse, Evolving Orchestration | 多 agent 协作的系统化研究，从角色扮演到进化编排 |
| **Microsoft Research** | AutoGen, HuggingGPT, ACON, GUI-Actor | 对话式多 agent 框架与 GUI agent 的工业级研究 |
| **FoundationAgents** | OpenManus, AFlow | 开源 agent 框架与自动工作流生成的先锋 |
| **Sakana AI** | CycleQD for Agent Skills | 质量多样性算法在 agent 技能获取中的创新应用 |

### 4.2 工业界

| 公司 | 代表工作 | 核心贡献 |
|------|----------|----------|
| **Google / Google DeepMind** | Chain-of-Thought, Least-to-Most, Code as Policies, RT-2 | 推理范式、具身智能、机器人控制的源头创新 |
| **Meta (FAIR)** | Toolformer | 自监督工具学习的开创性工作 |
| **OpenAI** | OpenAI Agents SDK, Skills in OpenAI API, Operator | 将 agent 能力产品化，定义行业 API 标准 |
| **Anthropic** | Claude Code, MCP, Agent Skills Blog, Computer Use | 安全 agent 设计的领导者，MCP 协议成为事实标准 |
| **Microsoft** | AutoGen, SWE-agent, Windows Agent Arena, ACON | 多 agent 框架与软件工程 agent 的工业落地 |
| **ByteDance** | MemAgent, Coze, DeepResearcher | 记忆系统与深度研究 agent 的大规模应用 |
| **Amazon Science** | SAGE (Skill Library + RL) | 电商场景下的技能库与强化学习结合 |

### 4.3 关键人物

| 研究者 | 机构 | 代表工作 | 影响 |
|--------|------|----------|------|
| **Shunyu Yao** | Princeton → Google | ReAct, Tree of Thoughts | 定义了 agent 推理与搜索的核心范式 |
| **Jason Wei** | Google | Chain-of-Thought | 开启了 LLM 推理时代 |
| **Joon Sung Park** | Stanford | Generative Agents | 证明了记忆架构与涌现行为的可行性 |
| **Guanzhi Wang** | NVIDIA/Caltech | Voyager | 终身学习与技能库的先驱 |
| **Chi Wang / Qingyun Wu** | Microsoft | AutoGen | 多 agent 框架的工程化领导者 |
| **Sirui Hong** | OpenBMB | MetaGPT, AFlow | 多 agent 协作与自动工作流的先锋 |

---

## 5. 与实时图形/游戏产业的交叉分析

### 5.1 架构层面的同构映射

| Agent Harness 组件 | 实时图形/游戏对应概念 | 同构性分析 |
|--------------------|----------------------|------------|
| **Agent Workflow (Planning Loop)** | **Rendering Pipeline** | 两者都是将高层目标分解为可执行步骤的管线：agent 的 Thought→Action→Observation 循环对应渲染管线的 Vertex→Raster→Pixel 阶段；都需要状态管理、错误恢复与并行调度。 |
| **Memory Systems (Short/Long-term)** | **Cache / Streaming System** | 工作记忆 ≈ 帧缓冲（高频更新、容量有限）；长期记忆 ≈ 缓存系统（低频更新、空间索引）。MemGPT 的 paging 机制与虚拟纹理/虚拟几何的流式加载同构。 |
| **Skill Libraries** | **Shader Library / Material System** | 可复用技能 ≈ 可复用 shader/material：都需要版本管理、依赖解析、运行时编译/加载。Voyager 的代码技能库与 UE5 的 Material Function Library 在组织逻辑上高度相似。 |
| **Multi-agent Orchestration** | **Multi-threaded Job System / Task Graph** | 多 agent 协作 ≈ 多线程任务图：都需要依赖追踪、负载均衡、同步屏障。AutoGen 的 GroupChat 调度器与游戏引擎的 Job Scheduler 面临相同的调度复杂性。 |
| **Environment Perception** | **Scene Understanding / Perception System** | Agent 的 GUI grounding (SeeClick, GUI-Actor) 与游戏的屏幕空间射线检测、UI 命中测试同构；都需要从像素/几何中提取语义信息。 |
| **Context Management** | **LOD / Occlusion Culling** | 上下文压缩 (ACON, LLMLingua) 与 LOD 降采样、遮挡剔除的动机一致：在有限资源（上下文窗口/帧时间预算）下保留最重要信息。 |

### 5.2 技术方法的交叉借鉴

| 方向 | 从图形/游戏到 Agent | 从 Agent 到图形/游戏 |
|------|----------------------|----------------------|
| **内存管理** | 虚拟纹理/虚拟几何的流式加载 → MemGPT 的 paging 机制 | Agent 的层次化记忆压缩 → 智能 NPC 的长期记忆系统 |
| **任务调度** | 游戏引擎的 Job Graph → AutoGen 的 conversation topology | 多 agent 的动态编排 → 大规模 crowd simulation 的群体行为控制 |
| **状态表示** | 场景图 (Scene Graph) → ESCA (Scene-Graph Generation for Embodied Agents) | Agent 的状态抽象 → 游戏 AI 的层级状态机优化 |
| **缓存策略** | GPU 缓存的 LRU/LFU → 记忆的遗忘曲线 (MemoryBank) | 记忆的注意力机制 → 渲染中的自适应采样 |
| **程序化生成** | 程序化内容生成 (PCG) → Voyager 的自动课程生成 | Agent 的技能组合 → 游戏内程序化任务生成 |

### 5.3 具体交叉点分析

#### 5.3.1 Planning Loop vs Rendering Pipeline

Agent 的 **ReAct 循环** (Thought → Action → Observation) 与实时渲染的 **Deferred Rendering Pipeline** 存在深层同构：

- **Thought (推理)** ≈ **G-Buffer 填充**：收集并结构化原始信息
- **Action (行动)** ≈ **Lighting/Shading 计算**：基于结构化信息执行核心操作
- **Observation (观察)** ≈ **Post-Processing/Composition**：整合结果并准备下一帧输入

两者都需要：
1. **管线状态管理**：当前处于哪个阶段、下一步该做什么
2. **资源绑定**：哪些工具/纹理在当前步骤可用
3. **错误恢复**：某一步失败时如何回滚或降级

#### 5.3.2 Skill Library vs Shader Library

Voyager 的 **Skill Library**（以可执行代码为技能表示，通过文本嵌入索引）与游戏引擎的 **Shader Library**（以 HLSL/GLSL 为表示，通过材质系统索引）在工程架构上几乎一致：

```
Voyager Skill Library          UE5 Material System
─────────────────────         ───────────────────
Skill (JavaScript function)    Material Function (HLSL)
Text Embedding Index           Material Parameter Collection
Skill Composition (chaining)   Material Layer Blending
Skill Verification (execution) Material Compilation (shader compile)
Skill Retrieval (similarity)   Material Instance Lookup
```

这种同构性意味着：游戏引擎的 asset pipeline 经验（版本控制、依赖管理、热更新）可直接迁移到 agent 技能库的工程化建设中。

### 5.4 游戏产业应用前景

| 应用场景 | Agent Harness 技术 | 预期影响 |
|----------|--------------------|----------|
| **智能 NPC** | 长期记忆 (Mem0) + 多 agent 编排 (MetaGPT) | NPC 具备跨会话记忆、自主社交关系、群体事件协调 |
| **自动化测试** | Agent Workflow (ReAct) + 环境感知 (SeeClick) | 自动执行 UI 测试、bug 复现、回归验证 |
| **程序化任务生成** | 技能库 (Voyager) + 自动课程 | 根据玩家行为动态生成个性化任务链 |
| **游戏内助手** | 工具使用 (Toolformer) + 上下文管理 | 智能客服、攻略生成、实时策略建议 |
| **开发工具链** | 多 agent 协作 (ChatDev) + SWE-agent | 自动化关卡设计、脚本生成、资源优化 |

---

## 6. 未来 2-3 年方向预测与技术论证

### 6.1 预测一：Agent 工作流将从"手工设计"走向"自动编译" (2026-2028)

**技术论证**：
- AFlow (ICLR 2025) 已证明工作流可通过搜索自动优化
- DSPy (ICLR 2024) 展示了声明式 pipeline 编译的可行性
- 类比：从手写 shader → Shader Graph → 材质蓝图 → 程序化生成

**预测细节**：
1. **2026-2027**：出现"Agent Compiler"——将高层任务描述自动编译为最优工作流拓扑（类似 LLVM 将 C 编译为机器码）
2. **2027-2028**：工作流编译器集成到主流框架（LangGraph, AutoGen 2.0），开发者只需定义任务目标与约束，系统自动生成、优化、部署工作流
3. **关键技术**：程序合成 + 神经架构搜索 (NAS) + 强化学习

**不确定性**：任务形式化描述的表达能力限制；编译后的工作流可解释性挑战。

---

### 6.2 预测二：记忆系统将从"外部存储"走向"内生化" (2026-2028)

**技术论证**：
- MEM1 (ICLR 2026) 和 MemAgent (ICLR 2026) 已开始将记忆管理内化为模型参数的一部分
- 当前记忆系统（MemGPT, Mem0）都是"外挂式"——模型本身不拥有记忆能力
- 类比：从虚拟内存 (paging) → 集成内存控制器 → 片上缓存 (L1/L2/L3)

**预测细节**：
1. **2026-2027**：出现"Memory-Augmented LLM"——在预训练阶段就将分层记忆机制融入模型架构（类似 Transformer 中的 KV cache 升级为持久化记忆层）
2. **2027-2028**：主流模型（GPT-5, Claude 4, Gemini 3）原生支持长时程记忆，无需外部 Mem0/MemGPT 系统
3. **关键技术**：可微分记忆网络 + 持续学习 + 灾难遗忘抑制

**不确定性**：记忆内生化与模型通用能力的权衡；隐私与数据安全的新挑战。

---

### 6.3 预测三：技能库将从"代码片段"走向"可执行语义网络" (2026-2028)

**技术论证**：
- Graph of Skills (arXiv 2026) 和 SkillRouter (arXiv 2026) 开始将技能组织为依赖感知的图结构
- 当前技能（Voyager 的 JS 函数）是扁平的、无显式依赖的
- 类比：从独立 shader → Shader Graph → 可视化编程网络

**预测细节**：
1. **2026-2027**：技能表示标准化为"可执行语义网络"——节点=原子操作，边=数据/控制依赖，支持自动类型检查、版本兼容性验证、运行时热更新
2. **2027-2028**：出现"Skill Marketplace"——类似 Unity Asset Store 的 agent 技能交易平台，技能可组合、可验证、可计费
3. **关键技术**：形式化验证 + 依赖解析 + 动态链接

**不确定性**：技能标准化组织的形成速度；跨平台技能互操作性的技术障碍。

---

### 6.4 预测四：多 agent 编排将从"角色扮演"走向"涌现组织" (2027-2029)

**技术论证**：
- MegaAgent (ACL 2025) 已证明无需预定义 SOP 的多 agent 协作可行
- 当前多 agent（MetaGPT/ChatDev）依赖人工设计的角色与通信协议
- 类比：从脚本化 AI → 行为树 → GOAP → 涌现行为系统

**预测细节**：
1. **2027-2028**：出现"Self-Organizing Multi-Agent System"——agent 根据任务需求自发形成组织拓扑（层级/网状/星型），动态选举领导者、分配资源、重组团队
2. **2028-2029**：多 agent 系统展现出类似"公司组织"的涌现结构：专业化分工、信息层级、决策委员会、甚至"组织文化"（共享价值观/工作规范）
3. **关键技术**：多 agent 强化学习 (MARL) + 机制设计 + 社会选择理论

**不确定性**：涌现行为的可控性；多 agent 系统的安全对齐问题。

---

### 6.5 预测五：Harness 安全将从"事后补丁"走向"内生安全架构" (2026-2028)

**技术论证**：
- SafeHarness (arXiv 2026), AgentSpec (ICSE 2026), OpenPort Protocol (arXiv 2026) 已出现专门的安全架构研究
- 当前安全主要依赖 prompt 过滤和输出审核（事后防御）
- 类比：从软件防火墙 → 操作系统安全模块 → 硬件可信执行环境

**预测细节**：
1. **2026-2027**：Harness 安全架构标准化——每个 agent 工作流、记忆操作、技能调用都具备内置的 capability-based access control、审计日志、回滚机制
2. **2027-2028**：出现"Agent TCB (Trusted Computing Base)"——类似操作系统内核的可信 agent 核心，确保即使上层被攻击，底层资源访问仍受控
3. **关键技术**：形式化方法 + capability security + 可信执行环境

**不确定性**：安全与效率的权衡；跨平台安全标准的制定难度。

---

### 6.6 预测总结表

| 预测 | 时间窗口 | 置信度 | 关键驱动力 | 主要风险 |
|------|----------|--------|------------|----------|
| Agent 工作流自动编译 | 2026-2028 | ████████░░ 80% | AFlow/DSPy 的延续；工程效率需求 | 任务形式化表达限制 |
| 记忆系统内生化 | 2026-2028 | ███████░░░ 70% | MEM1/MemAgent 的延续；长上下文需求 | 通用能力权衡；隐私 |
| 技能语义网络化 | 2026-2028 | ████████░░ 80% | Graph of Skills/SkillRouter 的延续；生态需求 | 标准化组织形成速度 |
| 多 agent 涌现组织 | 2027-2029 | █████░░░░░ 60% | MegaAgent 的延续；复杂任务需求 | 可控性；安全对齐 |
| Harness 内生安全 | 2026-2028 | ███████░░░ 75% | SafeHarness/AgentSpec 的延续；监管需求 | 安全-效率权衡 |

---

## 7. 参考文献

本报告基于以下数据源：

1. **awesome-agent-harness** 仓库 (2026-05-19 更新, 502 refs): `C:/Git-repo-my/AIResearchVault/document/Routine/05-技术雷达/2026-07-03/awesome-agent-harness/README.md`
2. **原始论文**: Tang et al. *Agent Systems with Harness Engineering*. OpenReview 2026.
3. **Web 搜索补充**: 针对关键论文（ReAct, MemGPT, Voyager, MetaGPT, AutoGen, Toolformer, Generative Agents, Chain-of-Thought, Tree of Thoughts 等）的 arXiv 摘要、博客解读与引用分析。

---

*报告生成时间: 2026-07-03*  
*调研维度: Harness Core Design Components (Agent Workflow / Memory Systems / Skill Libraries / Multi-agent Orchestration)*  
*格式版本: v1.0*
