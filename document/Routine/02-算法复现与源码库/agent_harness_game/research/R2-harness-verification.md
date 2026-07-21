# R2 · Harness Verification/Evaluation 调研 brief

> **角色**：调研员_Harness验证
> **输入**：`01e-agent-harness-latest.md`、`Agent-Harness-Game-AI-2026-06-29.md`（均在 `01-论文阅读与研究库/`）
> **主题**：Agent Harness survey 中 V（Verification/Evaluation）组件的形式化、可靠性评估维度、**harness 自身的评估方法**
> **代码基线**：`verifier.py` 现有四维评估 structure_correctness / block_count / efficiency / inventory_match（权重 0.4/0.2/0.2/0.2，pass 阈值 overall≥0.75）

---

## 1. 相关论文/实现清单

| 名称 | 来源 | 年份 | 一句话定位 |
|------|------|------|-----------|
| Agent Harness for LLM Agents: A Survey (Meng et al.) | Preprints 202604.0428 | 2026-04 | 首次形式化六组件 H=(E,T,C,S,L,V)，指出环境漂移、任务规范歧义、harness 耦合是评估不可靠性三大根因 |
| Harness Engineering for LLM Agents: A Survey of Harness Component Taxonomy, Evaluation, and Model–Harness Coevolution | Preprints 202606.2203 | 2026-06 | 提出两层评估逻辑：先诊断模型原生能力缺口，再评估 harness 补偿的 effectiveness 与 net benefit——即"评估 harness 本身"的框架 |
| MAST: Why Do Multi-Agent LLM Systems Fail? (Cemri et al., UC Berkeley) | arXiv:2503.13657 | 2025-03 | 3 大类 14 种失败模式分类学，其中 "task verification 缺失"为独立类别；专家标注 Cohen's κ=0.88 + LLM-as-Judge 规模化管线 |
| RepoST (Xie et al., CMU) | arXiv:2503.07358, COLM 2025 | 2025-03 | "最小可执行闭包"沙箱测试；execution feedback 训练 HumanEval Pass@1 +5.5%；明确指出 RL reward hacking 风险 |
| AFlow (Zhang et al., MetaGPT) | arXiv:2410.10762, ICLR 2025 Oral | 2024-10 | MCTS 搜 workflow，用 execution score 当 reward；提出"搜索式编排的评测过拟合"问题，需要 hold-out 验证 |
| ACE: Agentic Context Engineering (Stanford) | arXiv:2510.04618 | 2025-10 | 用 AppWorld test-challenge split（更难的 held-out split）验证不过拟合；+10.6% agent 基准 |
| Confucius Code Agent (Harvard/Meta) | arXiv:2512.10398 | 2025-12 | SWE-Bench-Pro Resolve@1 = 59%，在同仓库/同模型/同工具的**受控条件**下对比 |
| GCC: Git Context Controller (Oxford) | arXiv:2508.00031 | 2025-07 | SWE-Bench Verified 相对基线 +13%，成功率 80%+，BrowseComp SOTA |
| Context Engineering Survey (中科院) | arXiv:2507.13334 | 2025-07 | 给出统一优化形式化 c* = argmax_c E[reward \| LLM(q, c)]，V 组件是该期望的估计器 |
| Gaia2 / AgentDyn / AgentLAB / DeepContext / VPI-Bench（Harness Engineering survey §6.1 引用） | 见 preprints 202606.2203 | 2025–2026 | 执行环境与安全 guardrail 缺口诊断基准族：异步环境 + 显式 action verification、长程攻击、意图漂移、视觉注入 |

---

## 2. 评估维度与指标

### 2.1 Harness survey 谱系给出的可靠性维度

1. **评估不可靠性三大根因**（Agent Harness Survey, 2026-04）：environment drift、任务规范歧义、harness-agent 耦合。→ 含义：V 组件必须报告自身配置（环境版本、seed、任务规范版本），否则分数不可复现。
2. **两层评估逻辑**（Harness Engineering Survey §6）：
   - Layer 1 *Native capability-gap diagnosis*：裸模型（无 harness 或最小 harness）跑基准，得到能力缺口基线；
   - Layer 2 *Compensation effectiveness & net benefit*：加 harness 后的提升 Δ = score(harness) − score(native)，同时扣除 harness 引入的成本（latency、token、false blocks）得 net benefit。**这是"评估 harness 而非 agent"的核心公式**。
3. **确定性检查（deterministic checks）**：lint、类型检查、contract assertion、test-suite hook、structured-output validation、executable scoring、environment-state audit——提供低成本、可复现的负反馈；工程上需要 verification step limits、early-exit、failure fallback（Harness Engineering Survey §3.6）。
4. **过程/轨迹评估（whole-trajectory evaluation）**：检查轨迹是否 coherent、economical、evidence-grounded——工具调用顺序是否满足依赖、步间是否脱节、最终答案是否基于可追踪证据。局部步评估（local evaluation）检查单步工具选择合理性、参数满足接口约束、推进子目标（Harness Engineering Survey §3.7 Observability）。
5. **失败分类学指标**（MAST）：14 种失败模式可按轨迹标注，verification 缺失是独立类别；标注一致性 Cohen's κ = 0.88 是 judge 质量门槛的参考值。

### 2.2 具体可量化指标（有公式给公式）

- **Pass@k**（代码/agent 基准通用，RepoST、SWE-bench 沿用）：
  pass@k = E_task [ 1 − C(n−c, k) / C(n, k) ]，n 为每任务采样数、c 为通过数。无偏估计器，SWE-bench 场景 k=1 即 Resolve@1。
- **成功率 + 置信区间**：n 个 episode 中 m 个 pass，报告 Wilson 区间而非裸比例（小 n 下更稳）。
- **Efficiency ratio**：turns_used / max_turns（verifier.py 现有 efficiency 维度即此形式，ASTRA 类工作"completion + efficiency 双约束"佐证其合理性）。
- **Net benefit** = Δscore − λ·(extra tokens + extra latency + extra false-block 损失)，λ 由部署预算定。
- **Guardrail 维度**：false-block rate（合法动作被拦）、bypass rate（违例动作漏拦）；安全基准族（AgentDyn/AgentLAB/DeepContext）针对长程攻击、跨轮意图漂移、memory poisoning。
- **Judge 一致性**：κ ≥ 0.8（MAST 的 0.88 为参考）；LLM-as-Judge 需防偏见继承。

---

## 3. 评测协议设计

1. **受控对比协议**（Confucius）：同环境 / 同模型 / 同工具 条件下对比 harness 变体，否则差异不可归因。落地即 ablation：native（无 V 反馈）vs full-V vs 去掉某一维度。
2. **Hold-out / 防过拟合协议**：
   - AFlow 明确提出"搜出的 workflow 可能过拟合评测集"，需要 hold-out 验证；
   - ACE 用 AppWorld **test-challenge split**（比 test 更难的 held-out）验证；
   - → V 组件协议：任务集分 train/dev/test 三层，test 的任务 spec（坐标、数量、材料）从训练中未见过的分布采样。
3. **环境可复现协议**（针对 environment drift 根因）：固定 seed、固定环境版本、记录 TaskSpec 哈希；RepoST 的"最小可执行闭包"思想→我们的 2D 沙盒天然是最小闭包，要在报告中声明这一真实性边界。
4. **Episode 设置**：每任务 n ≥ 10 episode（多 seed）；报 pass@1 为主、pass@k（k=3,5）为辅；每 episode 记录完整轨迹（trace）供过程评估与失败归因。
5. **统计方法**：成功率报 Wilson 95% CI；两组对比用配对检验（McNemar，因 pass/fail 是二值）；维度分数均值 ± std。
6. **Reward hacking 防护**（RepoST §Q2）：verifier 规则本身会被过拟合——test split 的 verifier 检查项应对 agent 不可见（hidden checks），或对同一任务准备多套等价 verifier。
7. **验证预算控制**（Harness Engineering Survey §3.6）：verification step limits + early-exit + failure fallback，防止 agent 为刷局部通过率无限消耗。

---

## 4. 对 harness V 组件的落地建议

现有 `verifier.py` 四维（structure_correctness / block_count / efficiency / inventory_match，verifier.py:77-184）全部是**结果维、确定性、单 episode、无 harness 自评**。按 survey 框架建议如下：

| # | 建议 | 与现有四维的关系 | 落地方式（2D 沙盒） |
|---|------|----------------|-------------------|
| 1 | **过程维：trajectory coherence** | 新增 | 从 trace 计算：无效动作率（非法 action 数/总动作数）、冗余动作率（放置后立即挖除等无净效果动作对）、子目标推进率（每步后 structure_correctness 单调增量占比）。对应 survey §3.7 的 local + whole-trajectory evaluation |
| 2 | **安全维：guardrail 双率** | 新增 | 注入违例任务（要求把方块放到界外/使用禁用工具），测 bypass rate；正常任务测 safety.py 的 false-block rate。对应 §3.6 与 AgentLAB 类安全基准 |
| 3 | **Judge 抽象接口** | 增强 | Verifier 拆成 `DeterministicCheck`（现有四维归入此类，即 survey 的 deterministic checks / environment-state audit）+ `JudgeCheck`（预留 LLM-as-Judge 接口，用于"房子美观/功能性"这类无标准答案维度，对应 06-29 笔记 line 106 的创造性评估问题）；judge 输出需报自一致性（多次采样一致率，对标 κ） |
| 4 | **pass@k + CI 报告** | 增强 | TaskVerifier 输出不变，外层 BenchmarkRunner 聚合 n episode：pass@1 = 1−C(n−c,1)/C(n,1) = c/n，报 Wilson 95% CI；同任务多 seed |
| 5 | **Net benefit 自评（评 harness 本身）** | 新增（最关键） | 三臂 ablation：A=native（verifier 不参与反馈）、B=V 反馈进 loop、C=B 去掉单一维度。报告 Δscore、额外 token/turn 成本、net benefit = Δscore − λ·Δcost。这直接实现 Harness Engineering Survey §6.2 的 compensation assessment |
| 6 | **任务 split 协议** | 新增 | TaskSpec 工厂增加 `split` 字段：dev 任务坐标固定（现 build_wall_2x2 等），test 任务坐标/尺寸从 held-out 分布随机采样（seed 固定可复现）；verifier 对 test 任务使用 agent 不可见的 hidden checks 防 reward hacking |
| 7 | **评估元数据自报** | 增强 | EvaluationResult 增加 harness_config 字段（环境 seed、TaskSpec 哈希、verifier 版本号），每条结果可溯源——直接回应 environment drift / 任务规范歧义两大根因 |

**优先级**：#1、#4、#6 成本最低收益最大（纯工程）；#5 是"harness 自身评估"的灵魂，应作为 v2 的核心卖点；#3 的 LLM judge 可先做接口留空实现。

---

## 5. 引用指针

**本地文件**：
- `Agent-Harness-Game-AI-2026-06-29.md:26` — H=(E,T,C,S,L,V) 六组件定义与三大评估不可靠根因
- `Agent-Harness-Game-AI-2026-06-29.md:30` — 环境漂移与可复现游戏 agent 评估问题
- `Agent-Harness-Game-AI-2026-06-29.md:106` — 创造性评估需多维度（结构完整性、美观、功能）
- `Agent-Harness-Game-AI-2026-06-29.md:137-141` — 评估层文献地图（SWE-bench / AgentBench / MineDojo）
- `01e-agent-harness-latest.md:18-19` — c* = argmax_c E[reward | LLM(q, c)] 统一形式化
- `01e-agent-harness-latest.md:86,101` — ACE AppWorld test-challenge split、+10.6%
- `01e-agent-harness-latest.md:117-139` — MAST 失败分类学、verification 类别、κ=0.88、coordination breakdown 36.9%
- `01e-agent-harness-latest.md:158-160` — AFlow 评测过拟合与 hold-out 问题
- `01e-agent-harness-latest.md:200` — Confucius Resolve@1=59% 受控对比
- `01e-agent-harness-latest.md:232` — GCC SWE-Bench Verified +13%、80%+ 成功率
- `01e-agent-harness-latest.md:253-271` — RepoST 最小可执行闭包、Pass@1 +5.5%、reward hacking 风险
- `verifier.py:77-184` — 现有四维评估与权重/阈值实现

**网络检索**（本次 brief 共 3 次检索额度内，实际使用 2 次）：
- Harness Engineering for LLM Agents: A Survey of Harness Component Taxonomy, Evaluation, and Model–Harness Coevolution, Preprints 202606.2203 (2026-06-30) — https://www.preprints.org/manuscript/202606.2203/v1 （§3.6 Verification and Guardrails、§3.7 Observability、§6 Harness Evaluation 两层评估逻辑、Table 1）
- Agent Harness Survey 原页 https://www.preprints.org/manuscript/202604.0428/v1 反爬未取到正文，其 V 组件内容以 06-29 笔记转述为准

*调研完成：2026-07-20 · 调研员_Harness验证*
