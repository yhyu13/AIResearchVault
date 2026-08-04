# 01-论文阅读与研究库

> **用途**：存放 AI 论文精读笔记、前沿追踪、文献综述
> **输入**：Arxiv、会议论文、博客、演讲
> **输出**：结构化笔记、知识图谱、面试素材

---

## 笔记格式

```markdown
---
tags: [paper, <topic>]
aliases: [<paper-short-name>]
created: YYYY-MM-DD
---

# 论文标题

- **作者**：...
- **来源**：Arxiv / NeurIPS / ICML / ICLR / CVPR / ...
- **链接**：...
- **主题**：[[LLM]] / [[RL]] / ...

## 核心贡献

1. ...
2. ...

## 方法概述

## 关键实验

## 局限性与思考

## 相关论文
- [[...]]

## 面试谈资
- 30秒：...
- 2分钟：...
```

---

## 分类索引

| 主题 | 论文数 | 最近更新 |
|------|--------|----------|
| Game-AI | 22 | 2026-07-20 |
| Agent Harness | 8 | 2026-07-20 |
| Agent Verification/Eval | 1 | 2026-07-20 |
| World Models | 7 | 2026-07-20 |
| Human-AI Interaction | 8 | 2026-07-20 |
| Game Benchmarks | 6 | 2026-07-20 |
| RL-in-Games / Synthetic Envs | 8 | 2026-07-20 |
| Sandbox | 6 | 2026-07-15 |
| Tool Calling | 6 | 2026-07-15 |
| Memory | 8 | 2026-07-15 |
| LLM | 0 | - |
| RL | 0 | - |
| Multi-Modal | 0 | - |
| AIGC | 0 | - |
| AI-Theory | 0 | - |
| AI-Training | 0 | - |
| AI-Optimization | 0 | - |
| AI-Math | 0 | - |
| NeRF | 0 | - |
| time-series | 0 | - |

---

## 阅读 Pipeline

1. **预读**（周一）：AI 生成 150 字摘要 + 3 个引导问题
2. **精读**（周一晚）：你阅读，标记难点
3. **讨论**（周二）：AI 解释难点，你验证理解
4. **笔记**（周二晚）：整理到本库
5. **复习**（周五）：AI 生成测验，你回答

---

## Game AI 研究库（2026-07-02 新建）

覆盖 **LLM/Agent in Games**、**Native AI Games**、**Human-AI-Game Interaction** 三大方向。

| Markdown | QA HTML | 内容 | 方向 |
|----------|---------|------|------|
| [[01-Game-AI-研究库总览]] | [🎯 自测](01-Game-AI-研究库总览.html) | 全景文献地图、概念速查、面试谈资 | 总览 |
| [[01a-LLM-Agent-in-Games]] | [🎯 自测](01a-LLM-Agent-in-Games.html) | Voyager, MineDojo, OSWorld, Harness 执行层 | 执行层 |
| [[01b-Native-AI-Games]] | [🎯 自测](01b-Native-AI-Games.html) | Genie, Infinigen, AI Dungeon, 世界模型设计 | 设计层 |
| [[01c-Human-AI-Game-Interaction]] | [🎯 自测](01c-Human-AI-Game-Interaction.html) | Cicero, Generative Agents, Companion AI, 人机交互 | 交互层 |
| [[Agent-Harness-Game-AI-2026-06-29]] | [🎯 自测](Agent-Harness-Game-AI-2026-06-29.html) | 6-29 预读：Harness Survey + Generative Worldcrafting + Agent World Model | 预读 |

---

## Agent 基础设施研究库（2026-07-15 新建）

覆盖 **Harness 系统**、**Memory 记忆**、**Tool Calling 工具调用**、**Sandbox 沙箱安全** 四大基础设施方向。

| Markdown | QA HTML | 内容 | 方向 |
|----------|---------|------|------|
| [[01d-memory-latest]] | [🎯 自测](01d-memory-latest.html) | Mem0, Zep/Graphiti, A-MEM, Memory-R1, HiMem, MemP, LEGOMem, MemAgent | 记忆系统 |
| [[01d-tool_calling-latest]] | [🎯 自测](01d-tool_calling-latest.html) | When2Tool, Atomix, PASTE/SPORK, ReTool, ToolACE-R, Tool Use Survey | 工具调用 |
| [[01d-sandbox-latest]] | [🎯 自测](01d-sandbox-latest.html) | LLM-in-Sandbox, Crab, SafeArena, ceLLMate, EnvSimBench, Agent-World | 沙箱安全 |

---

## Game-AI × Harness 最新论文库（2026-07-20 新建）

覆盖 **游戏 Agent 执行**、**世界模型**、**人机交互**、**Harness 工程**、**游戏基准**、**合成环境 RL** 六大方向，共 45 篇 2025–2026 最新论文。

| Markdown | QA HTML | 内容 | 方向 |
|----------|---------|------|------|
| [[01e-game-agent-execution-latest]] | [🎯 自测](01e-game-agent-execution-latest.html) | MindForge, Optimus-3, ODYSSEY, NitroGen, FlashAdventure, Orak, GameWorld, OmniGameArena | 游戏 Agent 执行 |
| [[01e-world-models-latest]] | [🎯 自测](01e-world-models-latest.html) | Genie 3, MineWorld, Matrix-Game 2.0, Hunyuan-GameCraft, Vid2World, IGV Survey, WorldPlay | 世界模型 |
| [[01e-human-ai-interaction-latest]] | [🎯 自测](01e-human-ai-interaction-latest.html) | When Agents Lie, C2C, Among Us, Beyond Survival, Scheming, Game-Theory Survey, R3D2, Bounded Autonomy | 人机交互 |
| [[01e-agent-harness-latest]] | [🎯 自测](01e-agent-harness-latest.html) | Context Engineering Survey, ACE, MAST, AFlow, Confucius, GCC, RepoST | Harness 工程 |
| [[01e-game-benchmarks-latest]] | [🎯 自测](01e-game-benchmarks-latest.html) | VideoGameBench, Orak, TextQuests, GVGAI-LLM, FlashAdventure, VisEscape | 游戏基准 |
| [[01e-rl-games-envs-latest]] | [🎯 自测](01e-rl-games-envs-latest.html) | SPIRAL, Absolute Zero, R-Zero, Vision-Zero, RLVE, GEM, AutoForge, GIFT | 合成环境 RL |

## Agent Verification/Eval 综合库（2026-07-20 新建）

| Markdown | QA HTML | 内容 | 方向 |
|----------|---------|------|------|
| [[01e-agent-verification-eval-latest]] | [🎯 自测](01e-agent-verification-eval-latest.html) | 四维指标体系（结果/过程/安全/开放）、评测协议（pass@k、Wilson CI、dev/test split、ablation）、agent_harness_game v2 落地映射，约 58 条引用 | 验证与评估 |

## AI Harness 单篇深度笔记 · 工业派双壁（2026-07-27 起）

聚焦 **Anthropic + OpenAI 两大头部厂商对 agentic systems 的工业级分类法**，作为 [[01e-agent-harness-latest]]（综述 7 篇）的工业补完，与 GameDevVault AI Harness 6 篇（5 GDC + 1 arxiv）形成 cross-ref。**两套分类法 80% 重叠 20% 互补**——任务类型用 Anthropic 6 原语（控制流视角），实现细节用 OpenAI 3+2+2+1+2（组件视角），安全层用 OpenAI 7 类 Guardrails，兜底层用 OpenAI 2 个 Human-in-Loop 触发点。

| Markdown | QA HTML | 内容 | 方向 |
|----------|---------|------|------|
| [[2024-Anthropic-Building-Effective-Agents]] | [🎯 自测](2024-Anthropic-Building-Effective-Agents.html) | 5 workflow 模式（prompt chaining / routing / parallelization / orchestrator-workers / evaluator-optimizer）+ 1 autonomous agent 模式 = 6 原语；MCP 作为 augmented LLM 工具集成协议层；"simple composable patterns > complex frameworks" 反共识判断；8 核心创新点 + 6 局限 + GameDevVault 6 篇对位 | AI Harness 工业框架（Anthropic 视角）|
| [[2025-OpenAI-A-Practical-Guide-to-Building-Agents]] | [🎯 自测](2025-OpenAI-A-Practical-Guide-to-Building-Agents.html) | 3 组件（Model / Tools / Instructions）+ 2 类编排（Single / Multi-agent）+ 2 种多 agent 拓扑（Manager / Decentralized handoff）+ 7 类 Guardrails + 2 个人工干预触发点；"code-first > declarative graphs" 反共识；8 核心创新点 + 7 局限 + Anthropic / GameDevVault 6 篇三方对位 | AI Harness 工业框架（OpenAI 视角）|

---

## MCP 生态 2025–2026 Deep Dive（2026-08-04 起）

**直接服务 day-job「Mac Game Harness 工具层」**：把 LLM 对 UE 工具的访问从 ad-hoc function calling 升级为**协议层抽象**。MCP（Model Context Protocol，Anthropic 2024-11 开源）已被定位为"agent 的 USB-C / TCP/IP"——5 个原语（Resources / Prompts / Tools / Roots / Sampling）+ JSON-RPC 2.0 + Stdio/SSE transport + capability negotiation。**核心结论**：fork 现有 UE 5.7 MCP 实现（[DandyDay/UnrealMCP](https://github.com/DandyDay/UnrealMCP)，100+ 命令 / 11 类别）+ 补 Mac-specific 工具（xcodebuild / xcrun simctl / metal / instruments / vulkaninfo），vendor-neutral Stdio-only 即可被 Claude Code / Cursor / Zed 任何 client 复用。**8 核心创新点 + 5 来源 + 3 个 day-job 关键设计决策**（工具层 fork vs 自研 / harness 模式选型 6+3+2+1+2+7+2 / vendor-neutral 多 client 兼容）。

| Markdown | QA HTML | 内容 | 方向 |
|----------|---------|------|------|
| [[01f-mcp-ecosystem-2025-2026]] | （QA 卡牌待补，下次 session） | 5 来源：Anthropic 2024-11 blog + MCP 2025-06 spec + modelcontextprotocol/servers 官方仓 + DandyDay/UnrealMCP（UE 5.7 / 100+ 命令 / 11 类别）+ Hou et al. 2025 安全综述（10 类风险 / arxiv ID 待验证）；覆盖 8 创新点 / MCP vs Function Calling vs OpenAPI / 生态时间线 2024-11→2026-07 | AI Harness 工具协议层（day-job 直用） |

---

## QA 面试卡牌使用说明

每个 `.html` 文件都是**完全自包含**的互动式面试自测页面，可直接在浏览器打开：

| 功能 | 操作 |
|------|------|
| **拖拽填空** | 桌面端 drag-and-drop / 移动端点击填充 |
| **单选/多选/判断** | 点击选项选择 |
| **检查答案** | 点击「检查答案」查看解析 |
| **题目总览** | 点击「总览」打开网格面板，点击缩略图跳转 |
| **随机选项** | 点击「随机选项」打乱单选/多选答案位置 |
| **键盘导航** | ← → 箭头键切换题目 |
| **重置** | 重置当前题 / 重置所有记录 |

**建议复习流程**：
1. 先读 Markdown 笔记（精读）
2. 打开对应 HTML 做自测（检验记忆）
3. 错题回到 Markdown 查原文（查漏补缺）
4. 重复直到全部正确

---
