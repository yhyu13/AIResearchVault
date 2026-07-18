# Plan — 04-性能优化备忘录 · W29 (2026-07-13 ~ 2026-07-19)

## 背景与选题依据

- W28 复盘 → W29 任务清单 P2 项：「AI-Infra 备忘录：Speculative Decoding 的蒙特卡洛框架分析」(成功标准：一份附录，分析"先猜后验"的采样策略)
- 本周技术雷达产出：`05-技术雷达/2026-07-14/LLM_Agent_Memory_System_2025_2026_Research_Brief.md` — Agent 记忆系统的检索延迟 / token 成本属典型推理优化议题
- 格式基准：`04-性能优化备忘录/00-README.md` 的优化案例模板 + `AI-Infra-性能优化全景.md` 的文风（瓶颈表格 + 技术迭代 + 量化数据 + 经验教训）

## 本周备忘录主题（2 篇）

| # | 主题 | 归属 | 核心内容 |
|---|------|------|----------|
| 1 | Speculative Decoding 的蒙特卡洛框架分析 | 推理优化 | "先猜后验" = rejection sampling；接受率 α = 1 − TV(p,q)；期望加速比推导；输出分布无偏性证明；EAGLE/MTP/n-gram 变体 |
| 2 | LLM Agent Memory System 性能优化 | 推理/部署优化 | 记忆检索延迟、token 成本削减、KV/上下文压缩、生产级记忆系统（Mem0 等）的性能工程 |

## Stage 1 — Research（explore workers × 2，并行）

- **R1 (SpecDec_Researcher)**：调研 speculative decoding 的蒙特卡洛/拒绝采样框架：Leviathan et al. 2023、Chen et al. 2023 原始论文的数学表述、接受概率与期望 token 数公式、无偏性证明思路、高 QPS 下 slowdown 的工程数据、EAGLE/Medusa/MTP 变体。产出 → `document/Routine/04-性能优化备忘录/_research/specdec_research_brief.md`
- **R2 (MemSys_Researcher)**：精读本地 `05-技术雷达/2026-07-14/LLM_Agent_Memory_System_2025_2026_Research_Brief.md` 提取性能相关数据（Mem0 token 节省、延迟数字、benchmark），并核实关键数据点来源。产出 → `document/Routine/04-性能优化备忘录/_research/agent_memory_perf_brief.md`

## Stage 2 — Writing（coder workers × 2，并行，依赖 Stage 1 产出）

- **W1 (MemoWriter_SpecDec)**：按 00-README.md 模板撰写 `04-性能优化备忘录/Speculative-Decoding-蒙特卡洛框架分析.md`。要求：数学严谨（接受率公式、期望加速比、无偏性证明完整推导），中文行文 + 英文术语。
- **W2 (MemoWriter_MemSys)**：按模板撰写 `04-性能优化备忘录/Agent-Memory-System-性能优化.md`。要求：数据均有来源标注，优化前后指标表格化。

## Stage 3 — Review（plan worker × 1）

- **Reviewer_FormatMath**：对照模板校验结构、frontmatter、数学推导正确性、引用可验证性。WARNING/REVISE → 修复。

## Stage 4 — 索引更新（主 agent 直接执行）

- 更新 `04-性能优化备忘录/00-README.md` 分类索引表（推理优化 / 部署优化行）
- 清理 `_research/` 中间文件或保留（保留，供溯源）

## 质量红线（继承 W29 调整原则）

- 每篇必须包含至少一个完整公式推导（非概念描述）
- 不生成 HTML 版本（HTML 冻结线）
- 数据点必须可溯源
