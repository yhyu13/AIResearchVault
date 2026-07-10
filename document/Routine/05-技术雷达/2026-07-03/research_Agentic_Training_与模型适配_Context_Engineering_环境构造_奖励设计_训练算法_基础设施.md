# Agentic Training 与模型适配：技术调研报告

> **调研维度**：Context Engineering / 环境构造 / 奖励设计 / 训练算法 / 基础设施  
> **数据来源**：awesome-agent-harness 仓库（README.md 第 3 章 + 相关交叉引用）  
> **调研时间**：2026-07-11  
> **调研员**：技术调研员（子代理）

---

## 目录

1. [核心发现摘要](#1-核心发现摘要)
2. [论文全景提取](#2-论文全景提取)
3. [时间线演变（2018→2026）](#3-时间线演变20182026)
4. [被证明正确的思路 vs 被淘汰的思路](#4-被证明正确的思路-vs-被淘汰的思路)
5. [核心公司/团队与贡献](#5-核心公司团队与贡献)
6. [与实时图形学/游戏产业的关联分析](#6-与实时图形学游戏产业的关联分析)
7. [未来 2-3 年发展方向预测](#7-未来-2-3-年发展方向预测)
8. [关键公式与算法精要](#8-关键公式与算法精要)
9. [参考文献](#9-参考文献)

---

## 1. 核心发现摘要

### 1.1 五大子维度的关键结论

| 子维度 | 关键结论 | 证据强度 |
|---|---|---|
| **Context Engineering** | 从静态 prompt 设计演进为动态、自进化的上下文 playbook（ACE 框架）；核心挑战是 brevity bias 和 context collapse | ★★★★★ |
| **环境构造** | 从规则-based 环境（ALFWorld）→ 仿真环境（WebWorld）→ 真实世界环境（DigiRL）；2025-2026 年出现大规模合成环境（Agent World Model, WebWorld） | ★★★★★ |
| **奖励设计** | Outcome Reward → Process Reward → Rule-based Verifiable Reward 的演进；GRPO/DAPO 证明无需单独 reward model 即可有效训练 | ★★★★★ |
| **训练算法** | PPO → DPO → GRPO → DAPO/ACT 的清晰演进线；核心趋势是**去价值模型化**（critic-free）和**token-level 信用分配** | ★★★★★ |
| **基础设施** | 从单 GPU colocated 训练 → Ray+vLLM 分布式 → 异步解耦（AReaL）→ 硬件异构分离（RollArt）；训练吞吐量提升 1.35-3.2x | ★★★★☆ |

### 1.2 最重要的三个技术转折点

1. **2024 年：GRPO 的提出（DeepSeekMath）** —— 首次证明无需 critic model 的 group-relative advantage 估计在数学推理上有效，内存节省约 50%。
2. **2025 年初：DeepSeek-R1（Nature 2025）** —— 纯 RL 无需 SFT 即可激发推理能力，开源复现了 OpenAI o1 的核心方法论。
3. **2025 年中：DAPO（ByteDance）** —— 四项改进（Clip-Higher、Dynamic Sampling、Token-Level Loss、Overlong Penalty）将 GRPO 推向生产级稳定训练。

### 1.3 与实时图形学的最深层关联

Agent 的 **planning loop**（感知→决策→执行→反馈）与实时渲染的 **rendering pipeline**（G-Buffer → Lighting → Shading → Post-processing）存在结构性同构；Agent 的 **memory system**（MemGPT/Agent Workflow Memory）与 **radiance cache**（ReSTIR GI 的 cached radiance estimate）在"时空复用近似信息"这一核心哲学上完全一致。

---

## 2. 论文全景提取

### 2.1 Context Engineering（上下文工程）

#### 2.1.1 Prompt Engineering（提示工程）

| # | 论文 | 作者/机构 | 会议/年份 | 核心贡献 |
|---|---|---|---|---|
| 1 | Chain-of-Thought Prompting Elicits Reasoning in Large Language Models | Wei et al., Google | NeurIPS 2022 | 首次系统证明中间推理步骤（CoT）可显著提升 LLM 推理能力，奠定 agent 推理基础 |
| 2 | Large Language Models are Zero-Shot Reasoners | Kojima et al. | NeurIPS 2022 | "Let's think step by step" 零样本触发推理，无需微调 |
| 3 | Tree of Thoughts | Yao et al., Princeton | NeurIPS 2023 | 将推理从线性链扩展为树形搜索，允许回溯和探索多条路径 |
| 4 | Graph of Thoughts | Besta et al., SPCL | AAAI 2024 | 进一步扩展为图结构，支持聚合和循环推理 |
| 5 | Role play with large language models | Sharma et al. | Nature 2023 | 角色扮演可改变模型行为模式，为 persona-based agent 提供科学依据 |
| 6 | CAMEL: Communicative Agents for "Mind" Exploration | Li et al. | NeurIPS 2023 | 多 agent 协作框架，通过角色扮演实现自主任务分解 |
| 7 | Generative Agents | Park et al. | UIST 2023 | 交互式人类行为模拟，记忆-反思-计划架构成为后续 agent 记忆系统模板 |
| 8 | CoSER | Neph0s | ICML 2025 | 全面的文学数据集和角色扮演评估框架 |
| 9 | Large Language Models Are Human-Level Prompt Engineers | Zhou et al. | ICLR 2023 | APE：自动提示工程，用 LLM 生成和筛选最优提示 |
| 10 | Self-Refine | Madaan et al. | NeurIPS 2023 | 迭代自精炼，无需外部反馈即可改进输出 |
| 11 | Promptbreeder | Fernando et al. | ICML 2024 | 自指涉的提示进化，通过遗传算法迭代优化提示 |

#### 2.1.2 Context Retrieval（上下文检索）

| # | 论文 | 作者/机构 | 会议/年份 | 核心贡献 |
|---|---|---|---|---|
| 1 | Interleaving Retrieval with Chain-of-Thought | Trivedi et al. | ACL 2023 | IRCoT：交替检索与推理，解决知识密集型多步问题 |
| 2 | ReAct | Yao et al. | ICLR 2023 | 推理+行动协同，Thought → Action → Observation 循环成为 agent 标准架构 |
| 3 | Self-RAG | Asai et al. | ICLR 2024 | 自反思检索增强生成，模型自主决定何时检索 |
| 4 | RAPTOR | Sarthi et al. | ICLR 2024 | 递归抽象处理树组织检索，多层次语义聚合 |
| 5 | DSPy | Khattab et al. | ICLR 2024 | 声明式语言模型调用编译为自改进 pipeline |
| 6 | Search-o1 | RUC-NLPIR | EMNLP 2025 | Agentic 搜索增强大推理模型 |
| 7 | MCP Landscape | Security-Pride | arXiv 2025 | Model Context Protocol 安全威胁全景分析 |
| 8 | A-RAG | arXiv 2026 | arXiv 2026 | 分层检索接口扩展 agentic RAG |

#### 2.1.3 Context Management（上下文管理）

| # | 论文 | 作者/机构 | 会议/年份 | 核心贡献 |
|---|---|---|---|---|
| 1 | Lost in the Middle | Liu et al. | TACL 2024 | 系统证明 LLM 对长上下文中间部分信息丢失，催生上下文压缩研究 |
| 2 | LLMLingua | Jiang et al. | EMNLP 2023 | 基于困惑度的提示压缩，加速推理 |
| 3 | ACON | Microsoft | arXiv 2025 | 长 horizon agent 上下文压缩优化 |
| 4 | AgentFold | arXiv 2025 | arXiv 2025 | 主动上下文管理的长 horizon web agent |
| 5 | SWE-Pruner | arXiv 2026 | arXiv 2026 | 编码 agent 自适应上下文剪枝 |
| 6 | CEDAR | Fraunhofer-IIS | arXiv 2026 | Agentic 数据科学的上下文工程 |
| 7 | IterResearch | ICLR 2026 | ICLR 2026 | 交互缩放重新思考长 horizon agent |
| 8 | MemGPT | Packer et al. | arXiv 2023 | 将 LLM 视为操作系统，分页内存管理 |
| 9 | Agent Workflow Memory | Zora et al. | ICML 2025 | 工作流记忆，跨 episode 复用策略 |
| 10 | Mem0 | ECAI 2025 | ECAI 2025 | 生产级可扩展长期记忆 |
| 11 | A-Mem | Xu et al. | NeurIPS 2025 | Agentic 记忆，主动管理记忆内容 |
| 12 | HiAgent | ACL 2025 | ACL 2025 | 层次化工作记忆管理 |
| 13 | **ACE** | **Zhang et al., Stanford/SambaNova** | **ICLR 2026** | **Agentic Context Engineering：将上下文视为进化 playbook，Generator→Reflector→Curator 模块化流程，+10.6% agent 基准，+8.6% 金融基准** |
| 14 | Meta Context Engineering | MetaEvo-AI | ICML 2026 | 通过 agentic 技能进化实现元上下文工程 |
| 15 | AgentSys | arXiv 2026 | arXiv 2026 | 显式层次记忆管理的安全动态 agent |

### 2.2 Agentic Training（Agent 训练）

#### 2.2.1 Environment Construction（环境构造）

**规则型环境：**

| # | 论文 | 作者/机构 | 会议/年份 | 核心贡献 |
|---|---|---|---|---|
| 1 | ALFWorld | Shridhar et al. | ICLR 2021 | 文本与具身环境对齐的交互学习 |
| 2 | ScienceWorld | Wang et al. | EMNLP 2022 | 科学任务 agent 评估 |
| 3 | WebShop | Yao et al. | NeurIPS 2022 | 可扩展真实世界 web 交互 |
| 4 | InterCode | Qin et al. | NeurIPS 2023 | 标准化交互式编码评估 |
| 5 | AppWorld | StonyBrookNLP | ACL 2024 | 可控的 app 与人交互世界 |
| 6 | MLGym | arXiv 2025 | arXiv 2025 | AI 研究 agent 新框架和基准 |
| 7 | REASONING GYM | arXiv 2025 | arXiv 2025 | 可验证奖励的推理环境 |
| 8 | R-Zero | arXiv 2025 | arXiv 2025 | 零数据自进化推理 LLM |
| 9 | EnterpriseOps-Gym | arXiv 2026 | arXiv 2026 | 企业级状态化 agentic 规划和工具使用环境 |

**仿真型环境：**

| # | 论文 | 作者/机构 | 会议/年份 | 核心贡献 |
|---|---|---|---|---|
| 1 | Reasoning with Language Model is Planning with World Model | Hao et al. | EMNLP 2023 | 语言模型推理即世界模型规划 |
| 2 | NeuralOS | arXiv 2025 | arXiv 2025 | 通过神经生成模型模拟操作系统 |
| 3 | BuilderBench | arXiv 2025 | arXiv 2025 | 智能 agent 构建模块基准 |
| 4 | Agent World Model | arXiv 2026 | arXiv 2026 | 无限合成环境用于 agentic RL |
| 5 | **WebWorld** | **arXiv 2026** | **arXiv 2026** | **大规模 web 世界模型用于 web agent 训练** |

**真实世界环境：**

| # | 论文 | 作者/机构 | 会议/年份 | 核心贡献 |
|---|---|---|---|---|
| 1 | PaLM-E | Driess et al., Google | ICML 2023 | 具身多模态语言模型 |
| 2 | RT-2 | Zitkovich et al., Google | CoRL 2023 | VLA 模型将 web 知识迁移到机器人控制 |
| 3 | WebArena | Zhou et al. | ICLR 2024 | 真实 web 环境构建自主 agent |
| 4 | AgentBench | Liu et al., THUDM | ICLR 2024 | 多维度 LLM agent 评估 |
| 5 | **DigiRL** | **Bai et al., UC Berkeley** | **NeurIPS 2024** | **野外设备控制 agent 自主 RL 训练；1.3B VLM 从 17.7% → 67.2% 成功率，超越 17B CogAgent** |
| 6 | BrowserGym | arXiv 2025 | TMLR 2025 | Web agent 研究生态系统 |
| 7 | Digi-Q | arXiv 2025 | ICLR 2025 | 学习 Q 值函数训练设备控制 agent |
| 8 | WebRL | THUDM | ICLR 2025 | 自进化在线课程 RL 训练 web agent |
| 9 | DeepResearcher | GAIR-NLP | EMNLP 2025 | 真实环境 RL 扩展深度研究 |
| 10 | EnterpriseBench Corecraft | arXiv 2026 | arXiv 2026 | 高保真 RL 环境训练可泛化 agent |
| 11 | MolmoWeb | arXiv 2026 | arXiv 2026 | 开放视觉 web agent 和开放数据 |

#### 2.2.2 Reward Design（奖励设计）

**Outcome-Level Rewards（结果级奖励）：**

| # | 论文 | 作者/机构 | 会议/年份 | 核心贡献 |
|---|---|---|---|---|
| 1 | DeepSeek-Prover-V1.5 | DeepSeek | ICLR 2025 | 利用证明助手反馈进行 RL 和 MCTS |
| 2 | ACECODER | ACL 2025 | ACL 2025 | 自动测试用例合成实现 coder RL |
| 3 | Search-R1 | Jin et al. | COLM 2025 | 训练 LLM 推理并利用搜索引擎进行 RL |
| 4 | TTRL | arXiv 2025 | arXiv 2025 | 测试时强化学习 |
| 5 | Agent RL Scaling Law | arXiv 2025 | arXiv 2025 | 自发代码执行的 agent RL 规模律 |
| 6 | DeepCoder | Together AI | Blog 2025 | 完全开源 14B 编码器达到 O3-mini 水平 |
| 7 | DeepSWE | Together AI | Blog 2025 | 通过扩展 RL 训练完全开源 SOTA 编码 agent |

**Process-Level Rewards（过程级奖励）：**

| # | 论文 | 作者/机构 | 会议/年份 | 核心贡献 |
|---|---|---|---|---|
| 1 | **Let's Verify Step by Step** | **Lightman et al., OpenAI** | **ICLR 2024** | **PRM800K 数据集：首次大规模人类标注过程监督，PRM 在 MATH 上 78.2% 超越 ORM** |
| 2 | Math-Shepherd | Wang et al. | ACL 2024 | 无需人类标注的逐步验证和强化 |
| 3 | Improve Mathematical Reasoning by Automated Process Supervision | arXiv 2024 | arXiv 2024 | 自动化过程监督改进数学推理 |
| 4 | **ToolRL** | **Cheng et al.** | **NeurIPS 2025** | **"Reward is All Tool Learning Needs"：工具学习的奖励设计** |
| 5 | GUI-G² | arXiv 2026 | AAAI 2026 | GUI 定位的高斯奖励建模 |
| 6 | **Process Reward Models That Think** | **Mukhal et al.** | **TMLR 2026** | **生成式过程奖励模型，每步生成 CoT 验证，仅用 1% 监督标签匹配判别式 PRM** |

#### 2.2.3 Training Optimization Algorithms（训练优化算法）

**监督微调（SFT）：**

| # | 论文 | 作者/机构 | 会议/年份 | 核心贡献 |
|---|---|---|---|---|
| 1 | Toolformer | Schick et al., Meta | NeurIPS 2023 | LLM 自学使用工具 |
| 2 | Gorilla | Patil et al., UC Berkeley | NeurIPS 2024 | 连接大规模 API 的 LLM |
| 3 | ToolLLM | Qin et al., OpenBMB | ICLR 2024 | 掌握 16000+ 真实世界 API |
| 4 | FireAct | Chen et al. | arXiv 2023 | 语言 agent 微调初步探索 |
| 5 | AgentTuning | Zeng et al., THUDM | ACL 2024 Findings | 通用化 agent 能力的指令调优 |
| 6 | **AgentOhana** | **Zhang et al., Salesforce** | **arXiv 2024** | **统一数据和训练 pipeline；聚合 10 个环境数据，标准化多轮轨迹格式；xLAM-v0.1 大动作模型** |
| 7 | CodeAct | Wang et al. | ICML 2024 | 可执行代码动作激发更好 agent |
| 8 | Agent-FLAN | Bai et al. | ACL 2024 Findings | 有效 agent 调优的数据和方法设计 |
| 9 | On-Policy Distillation | arXiv 2024 | ICLR 2024 | 从自生成错误中学习 |
| 10 | AgentTrek | XLang AI | ICLR 2025 | 通过 web 教程引导重放合成 agent 轨迹 |
| 11 | Efficient Agent Training | arXiv 2025 | arXiv 2025 | 计算机使用的高效 agent 训练 |
| 12 | Structured Agent Distillation | arXiv 2025 | arXiv 2025 | 结构化 agent 蒸馏 |
| 13 | ZPD-Guided Data Synthesis | ICLR 2026 | ICLR 2026 | 最近发展区引导数据合成扩展 agent 能力 |

**强化学习方法：**

| # | 论文 | 作者/机构 | 会议/年份 | 核心贡献 |
|---|---|---|---|---|
| 1 | Proximal Policy Optimization (PPO) | Schulman et al. | arXiv 2017 | 经典 RL 算法，InstructGPT/ChatGPT 原始 RLHF 基础 |
| 2 | **Direct Preference Optimization (DPO)** | **Rafailov et al.** | **NeurIPS 2023** | **无需 reward model，直接用偏好数据优化策略；LLM  secretly a reward model** |
| 3 | Secrets of RLHF Part I: PPO | OpenLMLab | arXiv 2023 | 中文社区对 PPO 在 LLM 中应用的深度分析 |
| 4 | Secrets of RLHF Part II: Reward Modeling | OpenLMLab | arXiv 2024 | Reward modeling 深度分析 |
| 5 | KTO | Ethayarajh et al. | arXiv 2024 | 前景理论优化模型对齐 |
| 6 | **ArCHer** | **Zhou et al.** | **ICML 2024** | **层次化多轮 RL 训练语言模型 agent** |
| 7 | DeepSeekMath | Shao et al., DeepSeek | arXiv 2024 | **提出 GRPO，数学推理 MATH 51.7%，无需 critic model** |
| 8 | ORPO | Hong et al. | EMNLP 2024 | 无需参考模型的整体偏好优化 |
| 9 | SimPO | Meng et al., Princeton | NeurIPS 2024 | 无参考奖励的简单偏好优化 |
| 10 | WARP | Ramé et al. | arXiv 2024 | 权重平均奖励策略的好处 |
| 11 | ReMax | Li et al. | ICML 2024 | 简单有效的 RL 对齐方法 |
| 12 | VinePPO | Kazemnejad et al. | ICML 2025 | 精炼 LLM RL 训练中的信用分配 |
| 13 | **Kimi k1.5** | **Kimi Team** | **arXiv 2025** | **长上下文 RL 扩展，无需 MCTS/PRM 达到 o1 水平** |
| 14 | **DeepSeek-R1** | **Guo et al., DeepSeek** | **Nature 2025** | **纯 RL 激发推理能力，开源复现 o1；GRPO + rule-based reward** |
| 15 | **DAPO** | **Yu et al., ByteDance** | **arXiv 2025** | **GRPO 四项改进：Clip-Higher、Dynamic Sampling、Token-Level Loss、Overlong Penalty；开源大规模长序列 RL 训练系统** |
| 16 | RAGEN | arXiv 2025 | arXiv 2025 | 多轮 RL 理解自进化 |
| 17 | WebThinker | RUC-NLPIR | NeurIPS 2025 | 深度研究能力的推理模型 |
| 18 | Group-in-Group PO | arXiv 2025 | arXiv 2025 | LLM agent 训练的组内组策略优化 |
| 19 | ARPO | arXiv 2025 | arXiv 2025 | Agentic 增强策略优化 |
| 20 | LLM Collaboration with MARL | arXiv 2026 | AAAI 2026 | 多 agent 强化学习协作 |
| 21 | Tree Search for LLM Agent RL | arXiv 2025 | arXiv 2025 | LLM agent RL 的树搜索 |
| 22 | ML-Agent | arXiv 2025 | arXiv 2025 | 自主 ML 工程的 LLM agent 强化 |
| 23 | **ACT** | **arXiv 2026** | **arXiv 2026** | **Agentic Critical Training：批判式训练** |

#### 2.2.4 Infrastructure（基础设施）

**通用框架：**

| # | 论文 | 作者/机构 | 会议/年份 | 核心贡献 |
|---|---|---|---|---|
| 1 | **OpenRLHF** | **Hu et al.** | **arXiv 2024** | **首个 Ray+vLLM 分布式 RLHF 框架；支持 70B+ 模型；RLHF 训练速度 3-4x DeepSpeedChat** |
| 2 | NeMo-Aligner | NVIDIA | arXiv 2024 | NVIDIA 可扩展模型对齐工具包 |
| 3 | ReaL | OpenPsi | arXiv 2024 | 参数重新分配的高效 RLHF 训练 |
| 4 | AgentGym | WooooDyy et al. | arXiv 2024 | 多样化环境进化 LLM agent |
| 5 | **HybridFlow (verl)** | **Sheng et al., Volcengine** | **EuroSys 2025** | **灵活高效的 RLHF 框架；流式实验管理** |
| 6 | Open-Reasoner-Zero | arXiv 2025 | arXiv 2025 | 开源基础模型 RL 扩展方法 |
| 7 | RAGEN | arXiv 2025 | arXiv 2025 | 自进化多轮 RL |
| 8 | Group-in-Group PO | arXiv 2025 | arXiv 2025 | verl-agent 扩展 |
| 9 | **AReaL** | **Fu et al., Inclusion AI** | **arXiv 2025** | **大规模异步 RL 系统；1→1000 GPU 可扩展；完全异步消除同步瓶颈** |
| 10 | **Agent Lightning** | **Microsoft** | **arXiv 2025** | **统一 MDP；解耦执行与训练；可扩展 worker** |
| 11 | AgentGym-RL | arXiv 2025 | arXiv 2025 | 多轮 RL 长 horizon 决策 |
| 12 | GEM | Axon-RL | arXiv 2025 | Agentic LLM 的 gym |
| 13 | AgentRL | arXiv 2025 | arXiv 2025 | 多轮多任务异步框架 |
| 14 | SkyRL-Agent | NovaSky-AI | arXiv 2025 | 多轮 LLM agent 高效 RL 训练 |
| 15 | **Agent-R1** | **arXiv 2025** | **arXiv 2025** | **端到端 RL 训练强大 LLM agent** |
| 16 | **RollArt** | **Gao et al., HKUST/Alibaba** | **arXiv 2025** | **分离式基础设施扩展 agentic RL；1.35-2.05x 训练时间减少；3000+ GPU 训练百亿参数 MoE** |

**专用框架：**

| # | 论文 | 作者/机构 | 会议/年份 | 核心贡献 |
|---|---|---|---|---|
| 1 | Multimodal RL with Agentic Verifier | arXiv 2025 | arXiv 2025 | 多模态 RL 与 agentic 验证器 |
| 2 | Dr. MAS | arXiv 2026 | arXiv 2026 | 多 agent LLM 系统稳定 RL |
| 3 | **MARTI** | **Zhang et al.** | **ICLR 2026** | **多 agent LLM 系统强化训练和推理框架；AT-GRPO 算法；独立资源池支持并发 on-policy 训练** |
| 4 | LLM Collaboration with MARL | AAAI 2026 | AAAI 2026 | 多 agent 协作 RL |
| 5 | WideSeek-R1 | arXiv 2026 | arXiv 2026 | 多 agent RL 宽度缩放 |
| 6 | MM-DeepResearch | arXiv 2026 | arXiv 2026 | 多模态 agentic 搜索基线 |
| 7 | GrandCode | arXiv 2026 | arXiv 2026 | Agentic RL 达到竞赛编程大师级 |
| 8 | **LiteResearcher** | **Lee et al.** | **arXiv 2026** | **可扩展 agentic RL 训练框架用于深度研究 agent** |

---

## 3. 时间线演变（2018→2026）

### 3.1 总体时间线表格

| 阶段 | 时间 | 标志性事件 | 技术特征 | 代表论文/系统 |
|---|---|---|---|---|
| **Pre-History** | 2017-2020 | PPO 提出；OpenAI Gym | 经典 RL 算法；离散环境交互 | PPO (2017), OpenAI Gym (2016) |
| **Prompt Era** | 2020-2022 | GPT-3 + CoT | 静态提示工程；零样本/少样本推理 | CoT (NeurIPS 2022), Zero-Shot Reasoners (NeurIPS 2022) |
| **SFT Era** | 2022-2023 | InstructGPT; Toolformer | 监督微调；工具学习；人类反馈 | InstructGPT (2022), Toolformer (NeurIPS 2023), DPO (NeurIPS 2023) |
| **RLHF Era** | 2023-2024 | PPO-based RLHF; GRPO | 偏好优化；奖励模型；策略优化 | PPO RLHF (2023), GRPO (DeepSeekMath, 2024), ArCHer (ICML 2024) |
| **Critic-Free Era** | 2024-2025 | DeepSeek-R1; DAPO | 无需价值模型；规则奖励；长思维链 | DeepSeek-R1 (Nature 2025), DAPO (2025), Kimi k1.5 (2025) |
| **Agentic RL Era** | 2025-2026 | Agent-R1; RollArt; MARTI | 端到端 agent 训练；多轮交互；分离式基础设施 | Agent-R1 (2025), RollArt (2025), MARTI (ICLR 2026), ACT (2026) |
| **Self-Evolving Era** | 2026+ | ACE; Meta Context Engineering | 上下文自进化；元学习；无监督适应 | ACE (ICLR 2026), Meta Context Engineering (ICML 2026) |

### 3.2 各子维度详细时间线

#### Context Engineering 时间线

```
2022: CoT Prompting → 2023: ReAct / Self-Refine / APE → 2023: MemGPT (OS-like memory)
  → 2024: DSPy / RAPTOR / Self-RAG → 2025: Agent Workflow Memory / A-Mem / HiAgent
  → 2026: ACE (evolving playbooks) / Meta Context Engineering / AgentSys
```

**关键转折点**：
- **2023 年 MemGPT**：首次将 OS 分页内存管理概念引入 LLM，将上下文视为有限资源进行主动管理。
- **2025 年 Agent Workflow Memory**：跨 episode 复用工作流策略，记忆从"存储信息"变为"存储策略"。
- **2026 年 ACE**：上下文从"被压缩的摘要"转变为"自进化的 playbook"，通过 Generator→Reflector→Curator 循环实现无监督自我改进。

#### Environment Construction 时间线

```
2021: ALFWorld (规则) → 2022: WebShop/ScienceWorld → 2023: InterCode/ReAct
  → 2024: AppWorld/AgentBench/WebArena → 2024: DigiRL (真实世界 RL)
  → 2025: NeuralOS/BuilderBench/MEAL → 2026: WebWorld/Agent World Model (大规模合成)
```

**关键转折点**：
- **2024 年 DigiRL**：首次在真实世界 Android 环境中用自主 RL 训练设备控制 agent，证明离线→在线 RL 的有效性。
- **2026 年 WebWorld/Agent World Model**：从"仿真现有环境"转向"生成无限合成环境"，解决训练数据稀缺问题。

#### Reward Design 时间线

```
2022: ORM (Outcome Reward Model) → 2023: PRM (Process Reward Model, OpenAI)
  → 2024: Math-Shepherd (自动过程监督) → 2024: Rule-based verifiable reward (GRPO)
  → 2025: ToolRL (工具奖励) / GUI-G² (高斯奖励) → 2026: ThinkPRM (生成式 PRM)
```

**关键转折点**：
- **2023 年 OpenAI PRM**：PRM800K 人类标注数据集证明过程监督优于结果监督。
- **2024 年 GRPO**：DeepSeekMath 证明无需单独 reward model，仅用规则验证即可有效训练。
- **2026 年 ThinkPRM**：生成式 PRM 每步生成 CoT 验证，将监督标签需求降低 99%。

#### Training Algorithm 时间线

```
2017: PPO → 2022: InstructGPT RLHF → 2023: DPO (无 reward model)
  → 2024: GRPO (无 critic model) → 2024: ArCHer (层次化多轮 RL)
  → 2025: DeepSeek-R1 (纯 RL 无 SFT) → 2025: DAPO (GRPO 改进)
  → 2025: VAPO (value-augmented) / Group-in-Group PO → 2026: ACT (批判训练)
```

**关键转折点**：
- **2023 年 DPO**：证明 preference data 可直接优化策略，无需 reward model。
- **2024 年 GRPO**：证明无需 critic model，group-relative advantage 即可有效估计。
- **2025 年 DeepSeek-R1**：证明纯 RL（无需 SFT）即可激发推理能力，涌现长思维链。
- **2025 年 DAPO**：四项工程改进将 GRPO 推向生产级稳定训练。

#### Infrastructure 时间线

```
2023: DeepSpeed-Chat → 2024: OpenRLHF (Ray+vLLM) / NeMo-Aligner / ReaL
  → 2025: HybridFlow/verl (EuroSys) → 2025: AReaL (异步) / Agent Lightning (统一 MDP)
  → 2025: RollArt (分离式) / ROLL (多 GPU 并行) → 2026: MARTI (多 agent) / LiteResearcher
```

**关键转折点**：
- **2024 年 OpenRLHF**：首个 Ray+vLLM 分布式 RLHF 框架，训练速度 3-4x。
- **2025 年 HybridFlow (verl)**：EuroSys 接收，流式实验管理。
- **2025 年 RollArt**：首次将 agentic RL 训练负载分离到异构硬件（prefill GPU + decode GPU + CPU cluster），1.35-2.05x 加速。
- **2026 年 MARTI**：首个支持多 agent 并发 on-policy 训练的专用系统架构。

---

## 4. 被证明正确的思路 vs 被淘汰的思路

### 4.1 对比表格

| 被证明正确的思路 | 为什么对 | 被淘汰/边缘化的思路 | 为什么错/为什么边缘化 |
|---|---|---|---|
| **Critic-free RL (GRPO/DAPO)** | 节省 ~50% 内存；无需训练价值模型；group-relative advantage 在推理任务上足够准确 | **PPO + 独立 Critic Model** | 内存开销大；critic 训练不稳定；在 LLM 场景下优势估计误差大 |
| **Rule-based verifiable reward** | 无需人类标注；可自动验证（代码编译、数学正确性）；无 reward hacking | **Learned Reward Model (RLHF)** | 需要大量人类偏好标注；存在 reward hacking；泛化性差；训练成本高 |
| **Process Reward (PRM)** | 细粒度信用分配；逐步验证减少错误累积；特别适合长推理链 | **纯 Outcome Reward (ORM)** | 信用分配稀疏；长链推理中错误传播难以定位；样本效率低 |
| **Token-level policy gradient** | 细粒度梯度信号；解决长序列中的信用分配问题 | **Sequence-level loss** | 梯度信号粗糙；长序列中早期 token 的梯度被稀释 |
| **Context 作为 evolving playbook** | 保留领域知识；防止 brevity bias；支持自进化 | **Context 压缩为静态摘要** | 丢失细节；context collapse；无法适应新场景 |
| **异步解耦训练** | 生成与训练并行；环境交互不阻塞 GPU；吞吐量提升 1.35-3.2x | **同步 colocated 训练** | GPU 在环境执行时空闲；长 tail rollout 阻塞整个 batch；资源利用率低 |
| **分离式硬件部署** | prefill/decode/environment 各用最适合的硬件；总成本最优 | **所有阶段共用同构 GPU** | 昂贵 GPU 执行 CPU-bound 任务；资源浪费 |
| **纯 RL 无需 SFT (R1-Zero)** | 证明推理能力可自发涌现；减少对人类标注数据的依赖 | **SFT 后必须接 RLHF** | 不是必要条件；SFT 可能限制模型探索空间 |
| **多轮 on-policy RL** | 策略与环境实时交互；避免 off-policy 数据过时问题 | **Off-policy / 行为克隆** | 数据分布不匹配；无法适应环境动态变化 |
| **Long-CoT Distillation** | 将长推理链知识迁移到小模型；保持性能降低成本 | **直接训练小模型推理** | 小模型难以自发涌现长推理链；需要教师模型引导 |

### 4.2 详细分析

#### 4.2.1 Critic-free vs Critic-based

**GRPO 的数学本质**：

GRPO 消除了 PPO 中的价值模型 $V_\phi(s)$，改为对每个问题 $q$ 采样一组输出 $\{o_1, o_2, ..., o_G\}$，用组内相对奖励估计优势：

$$\hat{A}_{i} = \frac{r_i - \text{mean}(\{r_j\})}{\text{std}(\{r_j\})}$$

这一估计在以下条件下无偏：
1. 组内样本足够多（$G \geq 8$ 通常足够）
2. 奖励函数与真实质量单调相关
3. 任务具有可验证的正确性（数学、代码）

在推理任务中，这些条件通常满足，因此 GRPO 的简化是合理的。但在开放域生成任务中（如创意写作），缺乏客观验证标准，critic model 仍有价值。

#### 4.2.2 Rule-based vs Learned Reward

**Rule-based reward 的胜利条件**：
- 任务具有**客观可验证性**：代码编译通过/失败、数学答案正确/错误
- 规则可被**精确编码**：单元测试、类型检查、形式验证
- 无**reward hacking**空间：规则是硬约束，模型无法欺骗

**Learned reward model 的存活场景**：
- 开放域偏好对齐（helpful/harmless）
- 主观质量评估（写作风格、创意性）
- 多目标权衡（准确性 vs 简洁性）

#### 4.2.3 Context as Playbook vs Context as Summary

**ACE 的核心洞察**：

传统上下文压缩（如 LLMLingua）将历史信息压缩为摘要，导致：
- **Brevity bias**：为保持简洁丢弃关键领域知识
- **Context collapse**：迭代重写导致细节逐层丢失

ACE 的解决方案是**结构化增量更新**：
- **Generator**：基于当前状态生成新策略片段
- **Reflector**：评估新片段与现有 playbook 的一致性
- **Curator**：执行增量 delta 更新（添加/修改/删除），而非全量重写

这类似于版本控制系统（Git）的增量提交，而非每次生成新快照。

---

## 5. 核心公司/团队与贡献

### 5.1 主要贡献者图谱

| 公司/机构 | 核心贡献 | 代表工作 | 时间 |
|---|---|---|---|
| **DeepSeek** | Critic-free RL；纯 RL 推理；开源 o1 复现 | DeepSeekMath (GRPO), DeepSeek-R1 (Nature 2025) | 2024-2025 |
| **OpenAI** | PRM；过程监督；o1/o3 推理系统 | Let's Verify Step by Step (PRM800K), o1/o3 | 2023-2025 |
| **ByteDance** | DAPO；生产级 RL 训练系统 | DAPO (arXiv 2025) | 2025 |
| **Alibaba** | 分离式 RL 基础设施；大规模 agent 训练 | RollArt (arXiv 2025), Qwen3 | 2025 |
| **Microsoft** | Agent 基础设施；上下文压缩；统一 MDP | Agent Lightning (arXiv 2025), ACON | 2025 |
| **Salesforce** | 统一 agent 数据 pipeline；大动作模型 | AgentOhana (arXiv 2024), xLAM | 2024 |
| **THUDM (清华)** | Web agent RL；AgentBench；WebRL | AgentBench (ICLR 2024), WebRL (ICLR 2025) | 2024-2025 |
| **UC Berkeley** | 真实世界 RL；设备控制；VLA | DigiRL (NeurIPS 2024), Gorilla | 2024 |
| **Stanford** | Agentic 上下文工程；自进化系统 | ACE (ICLR 2026) | 2026 |
| **Princeton** | 偏好优化；推理搜索 | SimPO (NeurIPS 2024), Tree of Thoughts | 2023-2024 |
| **NVIDIA** | RL 训练工具包；GPU 优化 | NeMo-Aligner (arXiv 2024) | 2024 |
| **Volcengine (字节)** | 高效 RLHF 框架 | HybridFlow/verl (EuroSys 2025) | 2025 |
| **Inclusion AI** | 异步 RL 系统 | AReaL (arXiv 2025) | 2025 |
| **HKUST** | 分离式基础设施；多任务 RL | RollArt (arXiv 2025) | 2025 |

### 5.2 学术-工业协作模式

观察到以下协作模式：

1. **学术首创 → 工业放大**：
   - GRPO (DeepSeek, 学术) → DAPO (ByteDance, 工业级改进)
   - PRM (OpenAI, 学术) → 生产级 PRM 系统 (各公司)

2. **工业开源 → 学术跟进**：
   - OpenRLHF (社区) → 被 CMU 课程采用；衍生 MARTI、LMM-R1
   - verl/HybridFlow (Volcengine) → 成为多个学术工作的基础

3. **端到端闭环**：
   - DeepSeek：算法 (GRPO) → 模型 (R1) → 基础设施 (内部) → 开源释放
   - Alibaba：算法 (Qwen) → 产品 (Qoder) → 基础设施 (RollArt, 3000+ GPU) → 论文

---

## 6. 与实时图形学/游戏产业的关联分析

### 6.1 结构性同构分析

#### 6.1.1 Planning Loop ↔ Rendering Pipeline

| Agent Planning Loop | 实时渲染管线 | 同构点 |
|---|---|---|
| **感知 (Perception)** | G-Buffer 生成（几何、材质、深度） | 都从原始输入中提取结构化表示 |
| **推理 (Reasoning/CoT)** | Lighting 计算（直接光、间接光） | 都是核心计算密集型阶段；可并行/可近似 |
| **决策 (Action Selection)** | Shading（材质响应合成） | 都基于中间结果做出最终选择 |
| **执行 (Action Execution)** | Post-processing（Bloom、TAA、色调映射） | 都作用于输出，可反馈到下一帧 |
| **环境反馈 (Observation)** | 帧缓冲反馈（TAA 历史、运动向量） | 都提供时序信息用于下一迭代 |

**深层洞察**：Agent 的 ReAct loop（Thought→Action→Observation）与渲染的 frame loop（G-Buffer→Lighting→Shading→Post）在**控制流结构**上完全同构。两者都是：
- **数据流管线**：阶段间传递结构化数据
- **时序迭代**：当前帧/步的输出是下一帧/步的输入
- **可近似性**：中间结果可缓存/复用（radiance cache ↔ agent memory）

#### 6.1.2 Memory System ↔ Radiance Cache

| Agent Memory | Radiance Cache | 同构点 |
|---|---|---|
| **MemGPT (分页内存)** | **ReSTIR GI Reservoir (缓存池)** | 都是有限资源的动态分配；都有 eviction 策略 |
| **Agent Workflow Memory** | **ReSTIR 的 temporal reuse** | 都跨时间步复用历史信息；都需验证有效性 |
| **A-Mem (主动记忆管理)** | **Neural Radiance Cache (NRC)** | 都主动决定存储/更新/检索；都学习型 |
| **ACE (进化 playbook)** | **World Space Radiance Cache** | 都累积结构化知识；都支持增量更新 |
| **Context Compression** | **Radiance 的 wavelet 压缩** | 都在保真度和存储间权衡；都有有损压缩 |

**深层洞察**：ReSTIR GI 的核心优化是**缓存 radiance estimate** $LC_k(x_2 \rightarrow x_1)$ 来避免重复路径追踪：

$$LC_k(x_2 \rightarrow x_1) = L_e(y_{mix,k} \rightarrow y_{mix,k-1}) \prod_{i=3}^{k} \frac{f \cdot G}{p_a(y_{mix,i})}$$

Agent memory 的对应优化是**缓存策略/知识片段**来避免重复推理。两者都面临：
- **一致性问题**：缓存值在新条件下是否仍然有效？
- **更新策略**：何时更新缓存？全量还是增量？
- **存储限制**：有限带宽/上下文窗口下的最优分配

#### 6.1.3 Reward Design ↔ Importance Sampling

| Agent Reward | 渲染重要性采样 | 同构点 |
|---|---|---|
| **Outcome Reward (稀疏)** | **Path Tracing 均匀采样** | 都方差高；都样本效率低 |
| **Process Reward (密集)** | **Multiple Importance Sampling (MIS)** | 都多源组合降低方差；都需权重平衡 |
| **Rule-based Verifiable Reward** | **Next Event Estimation (NEE)** | 都直接计算贡献；都无偏/可验证 |
| **GRPO Group Relative** | **Resampled Importance Sampling (RIS)** | 都组内比较选择最优；都重采样降低方差 |

**深层洞察**：GRPO 的 group-relative advantage 估计：

$$\hat{A}_i = \frac{r_i - \bar{r}}{\sigma_r}$$

与 ReSTIR 的 RIS 权重：

$$w(y) = \frac{1}{M} \sum_{j=1}^{M} \frac{p(y)}{p_j(y)}$$

在数学结构上都是**组内归一化比较**，目的都是降低方差。

### 6.2 技术迁移可能性

| 图形学技术 | 可迁移到 Agent 领域 | 迁移路径 |
|---|---|---|
| **ReSTIR 的 Reservoir 采样** | Agent 的轨迹选择 | 用 reservoir 维护 top-K 策略轨迹，避免存储全部历史 |
| **Temporal Reprojection** | Agent 的跨 episode 知识迁移 | 将上一 episode 的"有效策略"投影到当前 episode 的上下文 |
| **Level of Detail (LOD)** | Agent 的层次化推理 | 远距离/低优先级任务用粗粒度推理，近距离用细粒度 |
| **Deferred Shading** | Agent 的延迟决策 | 先收集全部信息（G-Buffer），再统一决策（Lighting），避免过早承诺 |
| **TAA (Temporal Anti-Aliasing)** | Agent 的决策平滑 | 当前决策与历史决策混合，避免抖动 |
| **Neural Radiance Cache** | Agent 的神经记忆缓存 | 用小型 MLP 近似存储/检索策略知识，而非显式文本 |

### 6.3 游戏产业的具体应用前景

1. **NPC Agent**：
   - 当前：行为树/状态机，预设脚本
   - 未来：Agentic RL 训练的自适应 NPC，能根据玩家行为动态调整策略
   - 技术需求：实时环境（游戏引擎）+ 可验证奖励（任务完成度）+ 高效训练（RollArt 式分离基础设施）

2. **自动化测试**：
   - 当前：人工编写测试用例
   - 未来：Agent 自主探索游戏状态空间，发现 bug 和边界情况
   - 技术需求：DigiRL 式真实环境 RL + Process Reward（逐步验证游戏状态合法性）

3. **内容生成**：
   - 当前：程序化生成（PCG）
   - 未来：Agent 根据设计目标自主生成关卡/剧情/对话
   - 技术需求：ACE 式上下文进化 + 规则验证（游戏机制一致性）

---

## 7. 未来 2-3 年发展方向预测

### 7.1 预测与根因分析

| 预测 | 时间框架 | 技术根因 | 置信度 |
|---|---|---|---|
| **Critic-free 成为默认配置** | 2026-2027 | 内存节省 50%；训练稳定性已验证（DAPO）；社区基础设施成熟（OpenRLHF/verl） | ★★★★★ |
| **Process Reward 完全自动化** | 2026-2027 | ThinkPRM 已证明 1% 标签足够；LLM-as-verifier 趋势；合成数据生成成熟 | ★★★★☆ |
| **Agent 训练基础设施云化** | 2026-2028 | RollArt 证明分离式可行；AReaL 证明异步可扩展；成本下降推动 democratization | ★★★★☆ |
| **Context Engineering 成为独立学科** | 2027-2028 | ACE 建立范式；Meta Context Engineering 推进；从"调参"到"系统工程" | ★★★★☆ |
| **多 Agent 协作训练标准化** | 2027-2029 | MARTI 建立多 agent RL 系统；通信协议（MCP）成熟；博弈论基础 | ★★★☆☆ |
| **Agent 与游戏引擎深度集成** | 2026-2028 | Unreal/Unity 已支持 Python 脚本；DigiRL 证明真实环境 RL 有效；产业需求强烈 | ★★★★☆ |
| **Test-time Compute 持续扩展** | 2026-2029 | o1/o3/R1 已证明方向；推理时搜索（MCTS/Beam）与训练时 RL 互补；硬件（GPU/TPU）持续扩展 | ★★★★★ |
| **Self-evolving Agent 闭环** | 2028-2030 | ACE 上下文自进化 + ACT 批判训练 + 基础设施自动化；最终目标是"发布后即自我改进" | ★★★☆☆ |

### 7.2 关键技术挑战

1. **Credit Assignment in Long-Horizon**：
   - 当前：VinePPO、GTPO 尝试解决，但长 horizon（>100 步）的信用分配仍不稳定
   - 根因：梯度传播深度限制；奖励稀疏性
   - 可能方向：层次化 RL（ArCHer）+ 子目标发现（Option Framework）

2. **Reward Hacking in Complex Environments**：
   - 当前：规则奖励在简单任务有效，复杂任务（如创意写作）难以定义
   - 根因：真实世界目标函数不可知；代理目标与真实目标错位
   - 可能方向：LLM-as-Judge + 多目标优化 + 对抗性验证

3. **Sample Efficiency in Real-World RL**：
   - 当前：DigiRL 需要大量环境交互（Android 模拟器可并行，但真实 API 成本高）
   - 根因：真实环境状态转移不可逆；探索成本高
   - 可能方向：World Model（WebWorld/Agent World Model）+ 离线 RL + 模型预测控制（MPC）

4. **Context Window Limitation**：
   - 当前：即使 1M token 上下文，长 horizon agent 仍面临信息丢失
   - 根因：Transformer 注意力二次复杂度；长序列推理误差累积
   - 可能方向：稀疏注意力（MSA）+ 显式记忆管理（Mem0/AgentSys）+ 层次化压缩

### 7.3 与实时图形学的交叉预测

| 预测 | 根因 | 时间 |
|---|---|---|
| **游戏引擎内置 Agent 训练框架** | Unreal/Unity 已支持 Python；RL 训练需要环境接口；产业需求 | 2026-2027 |
| **Radiance Cache 思想用于 Agent Memory** | 同构性已证明；缓存一致性问题相似；图形学社区有成熟方案 | 2026-2028 |
| **GPU 光线追踪用于 Agent 感知** | RTX 硬件普及；NeRF/3DGS 场景表示；agent 需要空间推理 | 2027-2029 |
| **实时渲染与 Agent 决策统一管线** | 两者都是 frame-based 循环；可共享基础设施（GPU、内存管理） | 2028-2030 |

---

## 8. 关键公式与算法精要

### 8.1 GRPO（Group Relative Policy Optimization）

**目标函数**：

$$\mathcal{J}_{\text{GRPO}}(\theta) = \mathbb{E}_{q \sim P(Q), \{o_i\}_{i=1}^G \sim \pi_{\theta_{old}}(\cdot|q)} \left[ \frac{1}{G} \sum_{i=1}^{G} \left( \min\left( \frac{\pi_\theta(o_i|q)}{\pi_{\theta_{old}}(o_i|q)} \hat{A}_i, \text{clip}\left(\frac{\pi_\theta(o_i|q)}{\pi_{\theta_{old}}(o_i|q)}, 1-\epsilon, 1+\epsilon\right) \hat{A}_i \right) - \beta \mathbb{D}_{KL}(\pi_\theta \| \pi_{\text{ref}}) \right) \right]$$

**KL 散度估计**：

$$\mathbb{D}_{KL}(\pi_\theta \| \pi_{\text{ref}}) = \frac{\pi_{\text{ref}}(o_i|q)}{\pi_\theta(o_i|q)} - \log \frac{\pi_{\text{ref}}(o_i|q)}{\pi_\theta(o_i|q)} - 1$$

**Group Relative Advantage**：

$$\hat{A}_i = \frac{r_i - \text{mean}(\{r_j\}_{j=1}^G)}{\text{std}(\{r_j\}_{j=1}^G)}$$

**关键洞察**：无需 $V_\phi(s)$，用组内统计量替代。

### 8.2 DAPO（Decoupled Clip and Dynamic Sampling Policy Optimization）

**四项改进**：

1. **Clip-Higher**：非对称裁剪 $\epsilon_{low} \neq \epsilon_{high}$，放松上界防止 entropy collapse
2. **Dynamic Sampling**：过滤全成功/全失败样本组，确保有效梯度
3. **Token-Level Loss**：

$$J_{DAPO}(\theta) = \mathbb{E}\left[ \frac{1}{\sum |o_i|} \sum_{i=1}^{G} \sum_{t=1}^{|o_i|} \min\left( \frac{\pi_\theta(o_{i,t})}{\pi_{\theta_{old}}(o_{i,t})} \hat{A}_{i,t}, \text{clip}\left(\frac{\pi_\theta(o_{i,t})}{\pi_{\theta_{old}}(o_{i,t})}, 1-\epsilon_{low}, 1+\epsilon_{high}\right) \hat{A}_{i,t} \right) \right]$$

4. **Overlong Reward Penalty**：惩罚过长生成序列，减少奖励噪声

**关键洞察**：DAPO 优化的是 loss 的**归一化方式**，而非解决 token-level 的 credit assignment（这是 GTPO 的方向）。

### 8.3 ACE（Agentic Context Engineering）

**核心循环**：

```
Generator: 基于当前状态生成新策略片段
    ↓
Reflector: 评估新片段与现有 playbook 的一致性
    ↓
Curator: 执行增量 delta 更新（ADD/MODIFY/DELETE）
    ↓
更新后的 Playbook → 下一迭代输入
```

**关键约束**：
- **Grow-and-Refine**：增量更新，禁止全量重写
- **Structured Updates**：预定义操作类型，保持 playbook 结构完整性
- **No Labeled Supervision**：仅使用执行反馈和环境信号

### 8.4 RollArt 分离式架构

**三层硬件映射**：

| 阶段 | 计算特征 | 最佳硬件 | 原因 |
|---|---|---|---|
| Prefill | Compute-bound | Compute-optimized GPU (A100/H100) | 需要大量矩阵乘法 |
| Decode | Bandwidth-bound | Bandwidth-optimized GPU | 内存带宽限制生成速度 |
| Environment | CPU-heavy, Stateful | CPU Cluster | 需要执行工具/模拟器 |
| Reward | Stateless, Bursty | Serverless (弹性) | 无需持续占用资源 |

**核心指标**：
- 1.35-2.05x 端到端训练时间减少
- 3000+ GPU 集群上训练百亿参数 MoE
- 轨迹级异步：慢/失败环境不阻塞其他轨迹

---

## 9. 参考文献

### 9.1 必读论文（按重要性排序）

1. **DeepSeek-R1**: Guo et al. "Incentivizing Reasoning Capability in LLMs via Reinforcement Learning." *Nature* 2025. — 纯 RL 激发推理的开源里程碑。
2. **DAPO**: Yu et al. "Decoupled Clip and Dynamic Sampling Policy Optimization." arXiv 2025. — GRPO 生产级改进。
3. **ACE**: Zhang et al. "Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models." *ICLR* 2026. — 上下文自进化范式。
4. **DigiRL**: Bai et al. "Training In-The-Wild Device-Control Agents with Autonomous Reinforcement Learning." *NeurIPS* 2024. — 真实世界 RL 训练。
5. **RollArt**: Gao et al. "Scaling Agentic RL Training via Disaggregated Infrastructure." arXiv 2025. — 分离式训练基础设施。
6. **OpenRLHF**: Hu et al. "An Easy-to-use, Scalable and High-performance RLHF Framework." arXiv 2024. — 开源 RLHF 基础设施。
7. **AgentOhana**: Zhang et al. "Design Unified Data and Training Pipeline for Effective Agent Learning." arXiv 2024. — 统一 agent 数据 pipeline。
8. **MARTI**: Zhang et al. "A Framework for Multi-Agent LLM Systems Reinforced Training and Inference." *ICLR* 2026. — 多 agent RL 系统。
9. **Let's Verify Step by Step**: Lightman et al. "Process Supervision for Reasoning." *ICLR* 2024. — PRM 奠基工作。
10. **DPO**: Rafailov et al. "Direct Preference Optimization." *NeurIPS* 2023. — 无 reward model 的偏好优化。

### 9.2 关键开源项目

| 项目 | 链接 | 用途 |
|---|---|---|
| OpenRLHF | https://github.com/OpenRLHF/OpenRLHF | 通用 RLHF 训练 |
| verl (HybridFlow) | https://github.com/volcengine/verl | 灵活 RLHF 框架 |
| RAGEN | https://github.com/RAGEN-AI/RAGEN | 多轮 agent RL |
| Agent-R1 | https://github.com/AgentR1/Agent-R1 | 端到端 agent RL |
| RollArt (ROLL) | https://github.com/alibaba/ROLL | 分离式训练 |
| AgentOhana (xLAM) | https://github.com/SalesforceAIResearch/xLAM | 统一数据 pipeline |
| ACE | https://github.com/ace-agent/ace | 上下文工程 |
| DeepSeek-R1 | https://github.com/deepseek-ai/DeepSeek-R1 | 推理模型 |

---

> **报告生成时间**：2026-07-11  
> **数据源**：awesome-agent-harness README.md (695 行) + 网络搜索验证  
> **覆盖论文数**：第 3 章直接引用 80+ 篇，交叉引用总计 200+ 篇  
> **置信度说明**：带 ★ 评级基于会议声誉、引用量、社区验证度和工业部署情况综合评估
