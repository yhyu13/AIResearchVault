---
tags: [research-hub, game-ai, overview, roadmap]
aliases: [Game-AI-Research-Hub]
created: 2026-07-02
---

# Game AI 研究库总览

> **定位**：LLM/Agent × 游戏 的系统性研究库，覆盖 Agent 在游戏中的执行、原生 AI 游戏设计、以及人机交互未来。
> **状态**：框架已建，待填充精读笔记
> **关联**：[[Agent-Harness-Game-AI-2026-06-29]]

---

## 三大研究方向

| 方向 | 文件 | 核心问题 | 技术栈 |
|------|------|----------|--------|
| **LLM / Agent in Games** | [[01a-LLM-Agent-in-Games]] | 如何让 LLM Agent 在复杂游戏环境中可靠执行？ | RL + LLM + Tool Use + Harness |
| **Native AI Games** | [[01b-Native-AI-Games]] | 游戏设计如何围绕 AI 原生能力重新构建？ | Procedural Gen + World Model + Neuro-Symbolic |
| **Human-AI-Game Interaction** | [[01c-Human-AI-Game-Interaction]] | 玩家与 AI 的协作、竞争、社交边界在哪里？ | HCI + Coop-AI + Social Simulation |

---

## 文献地图（演进链）

```
Game AI 研究全景

├── 执行层：Agent in Game Environment
│   ├── Voyager (2023) — 代码生成 + Minecraft 终身学习
│   ├── Ghost in the Minecraft (2023) — 代码即动作
│   ├── MineDojo (2022) — 大规模 Minecraft 任务基准
│   ├── OSWorld (2024) — 通用 GUI Agent（含游戏）
│   ├── Generative Worldcrafting (2025) — 多模态内容生成
│   └── Agent Harness Survey (2026) — 六组件架构 E/T/C/S/L/V
│
├── 设计层：AI-Native Game Design
│   ├── Genie (Google DeepMind, 2024) — 生成式交互环境
│   ├── UniSim (2024) — 世界模型模拟器
│   ├── AI Dungeon (2019→2023) — 文本 LLM 驱动开放叙事
│   ├── Infinigen (Meta, 2023) — 程序化无限世界生成
│   ├── MindGame / 类似概念 — 内部世界模型即游戏
│   └── *待追踪* — 围绕 LLM 能力原生的玩法设计
│
├── 交互层：Human-AI Collaboration in Games
│   ├── Hidden Role Games (Werewolf, Resistance) — AI 欺骗与推理
│   ├── Overcooked / Co-op Games — 人机协作基准
│   ├── Diplomacy (Meta, 2022) — 自然语言谈判 + 策略
│   ├── Social Simulations (Stanford, 2023) — Generative Agents 小镇
│   ├── Companion AI (如 Baldur's Gate 3 队友) — 情感绑定
│   └── *待追踪* — 人机关系边界、AI 玩家权益
│
└── 基础设施层
    ├── Harness Engineering (2026) — 可控执行环境
    ├── World Models (Ha & Schmidhuber) — 环境压缩表示
    ├── Synthetic Environments (Agent World Model, 2026) — 无限训练数据
    └── Eval & Benchmarks — 游戏 Agent 如何评估？
```

---

## 关键概念速查

| 概念 | 一句话 | 相关论文 |
|------|--------|----------|
| **Agent Harness** | AI 的"马具"——可控执行环境六组件 | Agent Harness Survey (2026) |
| **Voyager** | 用代码生成实现 Minecraft 终身学习 | Voyager (2023) |
| **Genie** | 从视频/图像生成可交互的 2D 世界 | Genie (2024) |
| **Generative Agents** | 25 个 AI 在小镇里生活、社交、记忆 | Generative Agents (2023) |
| **Diplomacy AI** | 自然语言谈判 + 战略规划的巅峰 | Cicero (Meta, 2022) |
| **World Model** | 环境在 AI 脑中的压缩模拟器 | Dreamer, UniSim, Agent World Model |
| **Native AI Game** | 玩法设计依赖 AI 能力而非硬编码规则 | 待定义 |

---

## 面试谈资（Game AI 通用版）

### 30 秒

> Game AI 正在从"硬编码行为树"演进到"LLM Agent 在开放环境中自主执行"。三大前沿是：Agent 执行层（Voyager/MineDojo 的代码生成与 Harness）、AI 原生设计层（Genie/UniSim 的世界模型驱动内容）、以及人机交互层（Diplomacy 的谈判 AI 和 Generative Agents 的社交模拟）。核心挑战是**可靠性**——如何让 AI 在 100+ 步的长程任务中不漂移、可评估、可解释。

### 2 分钟

> 传统游戏 AI = 行为树 + 状态机 + 寻路，天花板明显。LLM 带来了两个范式转移：
> 1. **执行范式**：从"开发者写行为"到"Agent 写代码/执行命令"——Voyager 在 Minecraft 中用代码生成实现技能发现、记忆和组合，突破了手工设计的天花板；
> 2. **设计范式**：从"手工设计关卡"到"AI 生成世界"——Genie 和 Agent World Model 让游戏引擎变成"可交互的生成模型"，关卡、NPC、物理规则都可以动态生成；
> 3. **交互范式**：从" scripted NPC"到"有记忆、有目标、有社交关系的 Agent"——Generative Agents 证明了 25 个 AI 可以在开放环境中产生涌现的社交行为。
> 
> 但挑战巨大：游戏 Agent 的 Harness 需要同时处理多模态观察（像素+结构化数据+文本）、异构动作空间（键盘+鼠标+代码+自然语言）、以及创造性评估（"好房子"没有标准答案）。Harness Engineering 的六组件架构（E/T/C/S/L/V）是工程化方向。

---

## 论文追踪 Pipeline

1. **预读**（周一）：AI 生成 150 字摘要 + 3 个引导问题
2. **精读**（周一晚）：人类阅读，标记难点与公式
3. **讨论**（周二）：AI 解释难点，验证理解
4. **笔记**（周二晚）：按本库格式整理到对应方向文件
5. **复习**（周五）：AI 生成测验，检验记忆
6. **交叉链接**：在 Obsidian 中创建双向链接，构建知识图谱

---

## 待阅读队列

| 优先级 | 论文 | 方向 | 状态 |
|--------|------|------|------|
| P0 | Agent Harness Survey (精读 4.3/5.2) | 执行层 | 进行中 |
| P0 | Generative Worldcrafting | 执行层 | 待精读 |
| P1 | Voyager | 执行层 | 待预读 |
| P1 | Genie | 设计层 | 待预读 |
| P1 | Generative Agents | 交互层 | 待预读 |
| P2 | Cicero (Diplomacy) | 交互层 | 待预读 |
| P2 | Agent World Model | 基础设施 | 待预读 |
| P2 | UniSim | 设计层 | 待预读 |

---

## 最新论文批次（2026-07-20，01e 系列）

45 篇 2025–2026 论文已入库，见 [[00-README]] 索引：
- [[01e-game-agent-execution-latest]] — MindForge / Optimus-3 / ODYSSEY / NitroGen 等 8 篇（执行层）
- [[01e-world-models-latest]] — Genie 3 / MineWorld / Matrix-Game 2.0 等 7 篇（设计层）
- [[01e-human-ai-interaction-latest]] — When Agents Lie / C2C / R3D2 等 8 篇（交互层）
- [[01e-agent-harness-latest]] — ACE / MAST / AFlow / GCC 等 7 篇（Harness 工程）
- [[01e-game-benchmarks-latest]] — VideoGameBench / TextQuests / GVGAI-LLM 等 6 篇（基准评估）
- [[01e-rl-games-envs-latest]] — SPIRAL / Absolute Zero / RLVE / GEM 等 8 篇（合成环境 RL）

---

*创建时间：2026-07-02*
*维护者：AIResearchVault*
