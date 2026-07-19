# Plan — 扩充论文阅读与研究库（AI Games × Harness）

目标：为 `document/Routine/01-论文阅读与研究库` 新增一批 2025–2026 最新论文研究笔记，聚焦 **AI Games** 与 **Agent Harness**，产出 `.md` 笔记 + 自包含 QA `.html` 面试卡牌，并更新 README 索引与总览队列。

## Stage 1 — Research（explore workers，并行，不可见彼此输出）
按 6 个方向各派一名调研员，检索 arXiv/web 2025–2026 最新论文，返回结构化研究简报（论文元数据、核心贡献、方法、实验、局限、面试角度、可验证链接）。简报写入 `document/Routine/01-论文阅读与研究库/_research/` 临时目录。

| Worker | 方向 |
|--------|------|
| R1 | LLM Agent in Games（执行层，Voyager 后继、游戏长程任务） |
| R2 | World Models & AI-Native Games（设计层，Genie 后继、可玩世界模型） |
| R3 | Human-AI Interaction in Games（交互层，社交模拟、人机协作） |
| R4 | Agent Harness Engineering（六组件 E/T/C/S/L/V、可控执行环境） |
| R5 | Game Agent Benchmarks & Eval（游戏基准、可靠评估） |
| R6 | Synthetic Environments & RL-in-Games（合成环境、游戏 RL 训练） |

## Stage 2 — Writing（coder workers，并行）
每个 writer 读对应方向简报 + 既有笔记格式样例（`01d-sandbox-latest.md`），产出：
1. `01e-<topic>-latest.md` —— 沿用既有 frontmatter/AI 预读/引导问题/面试谈资格式
2. `01e-<topic>-latest.html` —— 自包含互动 QA 卡牌，遵循 skill `interview-card-system`（path: C:\Users\yuhang\AppData\Roaming\kimi-desktop\daimon-share\daimon\skills\interview-card-system\SKILL.md，by reference）

Stage-gate：研究简报验证后才启动写作。

## Stage 3 — Integrate（Orchestrator 本人）
更新 `00-README.md` 分类索引、`01-Game-AI-研究库总览.md` 待阅读队列；清理 `_research/` 临时文件；汇报产出清单。
