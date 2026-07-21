# Plan v2 · Verification/Evaluation 深化 — Agent Harness × Game AI

> **触发**：2026-07-20，聚焦 game-making agent 的验证评估（V 组件）
> **参考**：`01-论文阅读与研究库` 中的 benchmarks / harness / execution / tool-calling 文献
> **基线**：六组件已实现，24/24 测试通过（见 `02-Agent-Harness-Game-AI-2026-07-01.md`）

---

## Stage 1 — 文献调研（4 个并行调研员，explore→coder 代写 brief）

| 角色 | 输入文件 | 输出 brief |
|------|----------|-----------|
| 调研员_基准评测 | `01e-game-benchmarks-latest.md` + `01e-rl-games-envs-latest.md` | `research/R1-benchmarks.md` |
| 调研员_Harness验证 | `01e-agent-harness-latest.md` + `Agent-Harness-Game-AI-2026-06-29.md` | `research/R2-harness-verification.md` |
| 调研员_执行交互评估 | `01e-game-agent-execution-latest.md` + `01e-human-ai-interaction-latest.md` + `01a-LLM-Agent-in-Games.md` | `research/R3-execution-interaction.md` |
| 调研员_支撑组件评估 | `01d-tool_calling-latest.md` + `01d-sandbox-latest.md` + `01d-memory-latest.md` + `01e-world-models-latest.md` | `research/R4-supporting-evals.md` |

每个 brief 必须包含：论文/实现清单、评估维度与指标（含公式）、评测协议、可落地到 2D 沙盒 harness 的建议。

**Stage-Gate**：Orchestrator 检查 4 份 brief 合格后才进入 Stage 2。

## Stage 2 — 实现与写作（并行，文件互不冲突）

| 角色 | 产出 | 说明 |
|------|------|------|
| 实现员_Verifier扩展 | `verifier.py` 扩展 | 新增维度：轨迹/过程评估、安全违例率、动作冗余度、judge 抽象接口 |
| 实现员_BenchmarkRunner | 新建 `evaluation.py` | 任务套件、多 seed/多 episode、pass@k、成功率+置信区间、JSON/MD 报告 |
| 实现员_Demo补全 | `demo/craft_item.py` + `demo/run_benchmark.py` | 补齐 plan 缺口，演示基准评测 |
| 作家_调研笔记 | `01-论文阅读与研究库/01e-agent-verification-eval-latest.md` | 综合 4 份 brief，按研究库笔记格式 |

## Stage 3 — 测试与收尾（并行）

| 角色 | 产出 |
|------|------|
| 测试员 | `tests/test_verification_eval.py` + 全量回归 |
| 文档员 | 更新 `02-Agent-Harness-Game-AI-2026-07-01.md`、两边 `00-README.md` 索引、新笔记 HTML |

---

*创建：2026-07-20 · Orchestrator  swarm 模式*
