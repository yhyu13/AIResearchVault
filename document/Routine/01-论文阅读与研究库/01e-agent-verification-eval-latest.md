---
tags: [paper, verification, evaluation, game-ai, agent-harness]
aliases: [Agent-Verification-Eval]
created: 2026-07-20
---

# 01e-Agent 验证与评估综合：Game-Making Agent 的 V 组件设计

> **核心问题**：game-making agent（建造/合成/规划类游戏任务）的产出如何被可靠、可复现、不可作弊地验证与评估？
> **来源**：agent_harness_game 项目 2026-07-20 调研轮 4 份 brief（R1 基准评测 / R2 Harness 验证 / R3 执行与交互评估 / R4 支撑组件评估）
> **关联**：[[01e-game-benchmarks-latest]]、[[01e-rl-games-envs-latest]]、[[01e-agent-harness-latest]]、[[01e-game-agent-execution-latest]]、[[01e-human-ai-interaction-latest]]、[[01d-tool_calling-latest]]、[[01d-sandbox-latest]]、[[01d-memory-latest]]、[[01e-world-models-latest]]、[[Agent-Harness-Game-AI-2026-06-29]]、[[01-Game-AI-研究库总览]]

---

## 0. 一页纸总览：为什么 verification/evaluation 是 game-making agent 的核心瓶颈

Agent Harness survey 把系统形式化为六组件 H=(E,T,C,S,L,V)，其中 V 是唯一对"agent 到底做对了没有"给出答案的组件——但它同时是**评估不可靠性的汇聚点**。Survey 给出三大根因（R2）：

1. **Environment drift**：环境版本/seed 不固定，分数不可复现；
2. **任务规范歧义**：任务 spec 不明确，"完成"没有可判定标准；
3. **Harness-agent 耦合**：harness 既当教练又当裁判，提升无法归因到模型还是 scaffolding。

在游戏侧，瓶颈更尖锐（R1）：TextQuests / VisEscape 上 SOTA 模型的完整通关率为 0——粗粒度 binary 指标完全没有区分度，必须用细粒度进度指标才能度量"完成了 90% 还是一开始就失败"（GameWorld 的 Minecraft Clone 案例：agent 达 ~90% progress 但 SR=0，R3）。同时 verifier 自身会被过拟合：RepoST 明确指出 RL reward hacking 风险，AFlow 提出"搜索式编排的评测过拟合"，AutoForge 的环境 bug 被 agent exploit——**verifier 不是中立裁判，它本身也需要被评估**（R2/R4）。

结论（四份 brief 一致）：game-making agent 的 V 组件必须从"单任务、单轨迹、静态阈值的终局检查器"升级为**四维指标体系 + 统计化评测协议 + harness 自评（net benefit）**的组合。

---

## 1. 评估维度体系

> 统一判断原则（R3 横向判断）："LLM-as-judge 便宜但不可靠，状态断言可靠但需逐游戏人工编写"——**可状态化的判断一律走断言，judge 仅兜底无 ground-truth 的维度**。

### 1.1 结果维（outcome-based，状态断言）

| 指标 | 公式 | 出处 |
|------|------|------|
| Success Rate（二元终局） | `SR = (1/N) Σ_i 1[status_i = success]` | GameWorld（arXiv:2604.07429） |
| normalized Progress | `progress_i = clip_[0,1]((q_i^max − b_i)/(τ_i − b_i))`，聚合 `PG = (1/N) Σ progress_i`；q^max 取运行中历史最高值，防止终局恰好被破坏而低估能力 | GameWorld（R3） |
| Checkpoint / milestone 进度占比 | `progress = |completed checkpoints| / |total checkpoints| ∈ [0,1]` | VideoGameBench / FlashAdventure / TextQuests Game Progress（R1） |
| Goal-state diff（终态匹配） | episode 结束 world state 与目标 state 的逐格 **precision / recall / F1 over cells**，同时报结构级（连通区域）匹配；`precision = correct/(correct+extra)` 防止"铺满全图"刷分 | ToolSandbox 有状态终态比对思想（R4）；R3 建议 recall+precision 配对 |
| 人类基线锚定 | agent 分数以人类差距解读（GameWorld：Novice PG 64.1% / Expert 82.6%） | GameWorld（R3） |
| 长程进展计数 | tech-tree milestone 数 + unique items 数 | MindForge（NeurIPS 2025，3×/2.3× 于 Voyager）（R3） |

### 1.2 过程维（trajectory / process）

| 指标 | 公式 | 出处 |
|------|------|------|
| action_validity（无效动作率） | 无效动作数 / 总动作数（非法位置、材料不足的 craft、解析失败的指令） | GameWorld action-validity diagnostics（R3） |
| meaningful_step_ratio | 真正推进游戏状态的步数占比（放置/拆除/合成/移动成功 vs 无效动作）；公式细节见论文正文，摘要未给出——**待补充** | GVGAI-LLM（arXiv:2508.08501）（R1） |
| redundancy / 冗余动作率 | 无净效果动作对占比（放置后立即挖除等）；等价于 When2Tool 的 over-tooling rate（不必要调用数/总调用数） | R2 survey §3.7 / When2Tool（R4） |
| trajectory_progress（子目标推进率） | 每步后 structure_correctness 单调增量占比 | Harness Engineering Survey §3.7 whole-trajectory evaluation（R2） |
| plan_action_consistency | 声明子目标与实际执行动作的一致率；源自三阶段协议（private plan → public announcement → final action），实验中偏离动作 >90% 已预写于 plan | When Agents Lie（arXiv:2607.05132）（R3） |
| 过程奖励可验证化 | Dependency-Aware Synthesis Reward + Hallucination-Aware Consistency Reward：crafting 依赖路径直接作为 thinking reward，"好结果必须配好过程" | Optimus-3 DGRPO（arXiv:2506.10357）（R3） |
| 时序一致性校验 | 记录资源"获得/消耗/失效"事件流（双时间戳思想），抓"用了还没有的资源"这类幻觉动作 | Zep/Graphiti 双时间戳移植（R4） |

### 1.3 安全维（compliance / guardrail）

| 指标 | 公式/定义 | 出处 |
|------|-----------|------|
| SafeArena 四态 compliance | 对违例任务集报告 Compliant / Partial（可操作化为完成 ≥80% 非法步骤）/ Refusal / Error 四级分布，分类别报告而非聚合 | SafeArena（ICML 2025）（R4） |
| Harmful completion rate | 完成的有害任务数 / 有害任务总数（GPT-4o 34.7%、Qwen-2 27.3%、Claude-3.5 22.8%） | SafeArena（R4） |
| Guardrail 双率 | false-block rate（合法动作被拦）+ bypass rate（违例动作漏拦） | Harness Engineering Survey §3.6（R2） |
| Mean Harm | 危险/破坏性操作计数（游戏侧：误拆目标方块、破坏已有正确结构、无效合成） | TextQuests（arXiv:2507.23701）（R1） |

### 1.4 开放维（无 ground-truth，judge 兜底）

| 指标 | 定义 | 出处 |
|------|------|------|
| LLM-as-judge / CUA-as-a-Judge | 用 computer-use agent 自动评判进度；必须量化 judge 的假阳性/假阴性并人工抽检校准——judge 能力上限约束评测有效性，同源模型可能产生系统性偏置 | FlashAdventure（arXiv:2509.01052）（R1/R3） |
| Judge 一致性 | Cohen's κ ≥ 0.8 作为质量门槛参考（MAST 专家标注 κ=0.88） | MAST（arXiv:2503.13657）（R2） |
| Critic 降级设计 | LLM critic 误判成功会沿规划链累积错误 → 用游戏内状态做 ground-truth 校验，把 LLM critic 降级为"语义解释器"而非"裁判" | ODYSSEY（arXiv:2407.15325）（R3） |
| Reference-ification | 把 open-ended 行为转成有 reference 的判别式评测（Speech MC + Decision 一致性），绕开生成式评测无标准答案 | Beyond Survival（arXiv:2510.11389）（R3） |

### 1.5 Harness 自评维（评估 harness 本身，R2 独有）

- **两层评估逻辑**（Harness Engineering Survey §6）：
  - Layer 1 *Native capability-gap diagnosis*：裸模型跑基准，得能力缺口基线；
  - Layer 2 *Compensation effectiveness & net benefit*：Δ = score(harness) − score(native)；
- **Net benefit** = Δscore − λ·(extra tokens + extra latency + extra false-block 损失)，λ 由部署预算定。
- 统一优化形式化：c* = argmax_c E[reward | LLM(q, c)]，V 组件是该期望的估计器（Context Engineering Survey，arXiv:2507.13334）。

---

## 2. 评测协议

### 2.1 统计可靠性

- **多 seed × 多 episode**：每任务 n ≥ 10 episode（R2）/ N ≥ 5（R3）；同一 TaskSpec 在 N 个随机初始布局上跑 M 次，报告 mean ± std 与 pass rate，而非单次 rollout 布尔值（AutoForge env-level 聚合思想，R1）。
- **pass@k**：`pass@k = E_task[1 − C(n−c,k)/C(n,k)]`（无偏估计器，k=1 即 SWE-bench Resolve@1）；报 pass@1 为主、pass@k（k=3,5）为辅（R2）。注：R4 标注 pass@k 与 generalization split 在其所读四个文件中未显式定义，公式如需更细版本**待补充**（查 BFCL-v4 / τ-bench 原文）。
- **Wilson CI**：成功率报 Wilson 95% CI 而非裸比例（小 n 更稳）；两组对比用配对 McNemar 检验（pass/fail 二值）（R2）。
- **可复现性自证**：GameWorld 重复运行 σ 仅 0.5–1.1%，协议本身需做 repeated-evaluation robustness study；固定 seed、固定环境版本、记录 TaskSpec 哈希、暂停环境隔离 latency、隔离实例、readiness gate 保证一致起始条件（R3）。
- **Elo 排名注意**：Orak battle arena 对采样方差、随机种子、先手优势敏感；非平稳 agent 可用 Glicko-2 替代；先手优势需校准（SPIRAL RAE 在训练侧按 game×role 去偏，评估侧同样需要 per-role/per-seed 分层统计）（R1/R3）。

### 2.2 防过拟合：dev/test split 与"藏、标记、造"

三条防污染路线（R1）：
1. **藏（保密 split）**：VideoGameBench dev/test split + 3 款保密游戏；
2. **标记（canary GUID）**：TextQuests 数据集内嵌 canary，审计是否进入训练语料；
3. **造（程序化生成）**：GVGAI-LLM 用 VGDL 无限生成规则与关卡；RLVE 同路线；需"生成-验证"闭环确认可解性。

评测过拟合防护（R2）：
- AFlow 明确提出"搜出的 workflow 可能过拟合评测集"，需 hold-out 验证；
- ACE 用 AppWorld **test-challenge split**（比 test 更难的 held-out）验证不过拟合（+10.6%）；
- 任务集分 train/dev/test 三层，test 的 spec 参数从训练中未见过的分布采样；
- **Hidden checks**：test split 的 verifier 检查项对 agent 不可见，或同一任务准备多套等价 verifier（RepoST reward hacking 防护）；
- Held-out 泛化衰减：学到的 skill/prompt 在任务变体上的得分衰减，区分"记住答案" vs "学会技能"（OmniGameArena IDC 协议，R3）。

### 2.3 Ablation-as-protocol（变量隔离）

- **受控对比**：同环境/同模型/同工具条件下对比 harness 变体，否则差异不可归因（Confucius 协议，SWE-Bench-Pro Resolve@1 = 59%）（R2）；
- **模块消融**：Orak 用 MCP plug-and-play 接口对 memory/planner/self-reflection 模块做即插即用消融；输入模态 × agentic 策略 × 微调消融矩阵（R1/R3）；
- **Lite 设置**：暂停游戏时钟隔离 inference latency（VideoGameBench：实时 0.48% vs Lite 1.6% 的落差本身是诊断指标）（R1）；
- **禁工具设定**：无搜索/无计算器/无代码执行，隔离 intrinsic reasoning（TextQuests）（R1）；
- **Autosave 对照**："给 clue + autosave"前后对比归因瓶颈（长上下文状态管理而非知识）（R1）；
- **三臂 ablation（评 harness 本身）**：A=native（V 不参与反馈）vs B=V 反馈进 loop vs C=B 去掉单一维度，报 Δscore、Δcost、net benefit（R2）。

### 2.4 分类别分解报告

- SafeArena 式配比：safe : harmful = 1:1（250:250），harmful 分类别（虚假信息/非法活动/骚扰/网络犯罪/偏见五类），每类单独报告 completion rate，避免聚合掩盖弱点（misinformation 最高 28–30%）（R4）；
- 按任务难度分桶报告成功率，避免单一总分掩盖"只会做简单题"（RLVE edge-of-learnability 教训：通过率居中 ~50% 的任务信息量最大）（R1）；
- 按能力课程分级报告：GameWorld 5 级课程（timing grounding → reactive control → … → long-horizon coordination），性能按级别分解定位瓶颈（R3）；
- 长程衰减曲线而非点估计：fidelity/一致性随交互步数作图（EnvSimBench 10 步后显著偏离）（R4）。

---

## 3. 对 agent_harness_game 复现项目的落地映射

> 详细复现计划见 [[02-Agent-Harness-Game-AI-2026-07-01]]。现有基线：`verifier.py` 的 `TaskVerifier.evaluate()` 四维 —— structure_correctness(0.4) / block_count(0.2) / efficiency(0.2) / inventory_match(0.2)，pass 阈值 overall ≥ 0.75 且关键维 ≥ 0.75/0.8。

### 3.1 现有四维处置总表

| 现有维度 | 处置 | 依据 |
|----------|------|------|
| structure_correctness | 增强：改 recall + 新增 precision；支持 q^max 历史最高取值；milestone 加权 | GameWorld PG / ToolSandbox state-match / VideoGameBench checkpoint |
| block_count | 降为诊断 details，被 precision / Mean Harm 覆盖 | TextQuests Mean Harm / R3 |
| efficiency | 增强：normalized Progress 替代线性 turn 惩罚；联合 meaningful_step_ratio（区分"慢但在推进"与"快但在空转"） | GameWorld / GVGAI-LLM |
| inventory_match | 保留 + 时序化 tracking（双时间戳事件流，抓幻觉动作） | Zep 双时间戳移植 |

### 3.2 新增维度（按优先级）

1. **milestone_progress（高）**：TaskSpec.target_blocks 改造为有序 milestone 序列，报 `completed/total` + 首次命中 turn，解决 binary 区分度不足（FlashAdventure/MindForge/TextQuests 教训）。
2. **meaningful_step_ratio（高）**：environment.step 返回结果即可判定，efficiency 的分子级细化（GVGAI-LLM）。
3. **action_validity（高）**：非法动作/总动作，直接反映 agent 幻觉率（GameWorld）。
4. **mean_harm（中）**：拆除 target_blocks 中方块次数 + extra blocks，负进展计数（TextQuests）。
5. **compliance 安全维（中）**：违例任务集（挖基岩/越界放置/非法物品 ID）报 SafeArena 四态分布（R4）。
6. **world-model consistency（中）**：用规则化 ground-truth 引擎预测执行动作后状态与实际比对，检测 agent 错误心智模型；长期训练轻量 world model 作软验证器，用 fidelity 衰减曲线自评（MineWorld action-following 逆向使用 / EnvSimBench，R4）。
7. **plan_action_consistency（低，依赖 L 模块）**：声明子目标→实际达成一致率（When Agents Lie 正面用法，R3）。
8. **improvement_curve + held-out（跨 episode）**：IDC + 任务变体泛化衰减；2D 沙盒极易生成变体（平移目标位置、换方块类型），是天然优势（OmniGameArena，R3）。

### 3.3 协议层

- **多 seed pass rate ± std**：`passed` 布尔值 → `SR ≥ threshold over N seeds`（R3/R1）；
- **任务 split**：TaskSpec 工厂增加 `split` 字段；dev 坐标固定，test 从 held-out 分布采样（seed 固定可复现）；test 用 hidden checks 防 reward hacking（R2）；
- **三臂 ablation**：native vs full-V vs 去单维，报 net benefit——harness 自评核心卖点（R2）；
- **评估元数据自报**：EvaluationResult 增加 harness_config（环境 seed、TaskSpec 哈希、verifier 版本号），回应 environment drift / 任务规范歧义两大根因（R2）；
- **验证预算控制**：verification step limits + early-exit + failure fallback（Harness Engineering Survey §3.6，R2）；
- **验证器自评**：人工标注小样本集计算 verifier 判定与人工判定一致率，防 verifier 自身 Goodhart（R4）；
- **LLM-judge 定位为兜底**：仅用于"建筑美观/功能"这类无状态断言维度，配 false-positive/negative 抽检（R3）。

---

## 4. 引用清单

> 全部转录自 4 份 brief，未新增。R2 标注 "Agent Harness Survey 原页反爬未取到正文，其 V 组件内容以 06-29 笔记转述为准"；R4 标注 "pass@k 确切公式与 generalization split 设计待补充"。

### Benchmark 与评测协议（R1/R3）

| 名称 | 来源 | 年份 |
|------|------|------|
| VideoGameBench | arXiv:2505.18134 | 2025 |
| Orak | arXiv:2506.03610 | 2025 |
| TextQuests | arXiv:2507.23701 | 2025 |
| GVGAI-LLM | arXiv:2508.08501 | 2025 |
| FlashAdventure | arXiv:2509.01052（EMNLP 2025 Main） | 2025 |
| VisEscape | arXiv:2503.14427 | 2025 |
| SPIRAL | arXiv:2506.24119 | 2025 |
| RLVE | arXiv:2511.07317 | 2025 |
| GEM | arXiv:2510.01051 | 2025 |
| AutoForge | arXiv:2512.22857 | 2025 |
| R-Zero / Absolute Zero | arXiv:2508.05004 / 2505.03335 | 2025 |
| GameWorld | arXiv:2604.07429（NUS/Oxford） | 2026 |
| OmniGameArena | arXiv:2606.09826 | 2026 |
| ODYSSEY | arXiv:2407.15325（IJCAI 2025） | 2024 |
| Optimus-3 | arXiv:2506.10357 | 2025 |
| MindForge | arXiv:2411.12977（NeurIPS 2025） | 2024 |
| Voyager | NeurIPS 2023 | 2023 |

### Harness / Agent 系统评估（R2）

| 名称 | 来源 | 年份 |
|------|------|------|
| Agent Harness for LLM Agents: A Survey（Meng et al.） | Preprints 202604.0428（**原页未取到，以 06-29 笔记转述为准**） | 2026-04 |
| Harness Engineering for LLM Agents（Component Taxonomy, Evaluation, Coevolution） | Preprints 202606.2203 | 2026-06 |
| MAST: Why Do Multi-Agent LLM Systems Fail?（Cemri et al., UC Berkeley） | arXiv:2503.13657 | 2025-03 |
| RepoST（Xie et al., CMU） | arXiv:2503.07358（COLM 2025） | 2025-03 |
| AFlow（Zhang et al., MetaGPT） | arXiv:2410.10762（ICLR 2025 Oral） | 2024-10 |
| ACE: Agentic Context Engineering（Stanford） | arXiv:2510.04618 | 2025-10 |
| Confucius Code Agent（Harvard/Meta） | arXiv:2512.10398 | 2025-12 |
| GCC: Git Context Controller（Oxford） | arXiv:2508.00031 | 2025-07 |
| Context Engineering Survey（中科院） | arXiv:2507.13334 | 2025-07 |
| Gaia2 / AgentDyn / AgentLAB / DeepContext / VPI-Bench | 见 Preprints 202606.2203 §6.1 引用 | 2025–2026 |

### 交互/社交/可控性评估（R3）

| 名称 | 来源 | 年份 |
|------|------|------|
| Beyond Survival | arXiv:2510.11389 | 2025 |
| When Agents Lie | arXiv:2607.05132（ICML NExT-Game WS Best Paper） | 2026 |
| C2C | arXiv:2604.25088（Berkeley） | 2026 |
| Among Us Deception | arXiv:2603.26635（AAMAS 2026） | 2026 |
| Scheming in LLM-to-LLM | arXiv:2510.12826 | 2025 |
| Bounded Autonomy | arXiv:2604.04703 | 2026 |
| R3D2（Hanabi） | arXiv:2503.14555（ICLR 2025） | 2025 |

### 支撑组件评估：tool / sandbox / memory / world model（R4）

| 名称 | 来源 | 年份 |
|------|------|------|
| When2Tool / Probe&Prefill | arXiv:2605.09252 | 2026 |
| Atomix | arXiv:2602.14849 | 2026 |
| PASTE / SPORK / B-PASTE | arXiv:2603.18897 等 | 2026 |
| ReTool | arXiv:2504.11536 | 2025 |
| ToolACE-R | AAAI 2026 | 2026 |
| Tool Use 综述（Wang et al.）+ BFCL / API-Bank / ToolSandbox / τ-Bench | ACM Computing Surveys | 2026 |
| SafeArena | ICML 2025（PMLR 267） | 2025 |
| ceLLMate | arXiv:2512.12594 | 2025 |
| Crab | arXiv:2604.28138 | 2026 |
| LLM-in-Sandbox | arXiv:2601.16206 | 2026 |
| EnvSimBench | arXiv:2605.07247 | 2026 |
| Agent-World | arXiv:2604.18292 | 2026 |
| Mem0 | arXiv:2504.19413 | 2025 |
| Zep / Graphiti | arXiv:2501.13956 | 2025 |
| A-MEM | arXiv:2502.12110（NeurIPS 2025） | 2025 |
| Memory-R1 | arXiv:2508.19828 | 2025 |
| HiMem | arXiv:2601.06377 | 2026 |
| MemP / LEGOMem | arXiv:2508.06433 / 2510.04851 | 2025 |
| LoCoMo / LongMemEval | arXiv:2402.17753 / 2410.10813 | 2024 |
| MineWorld | arXiv:2504.08388 | 2025 |
| Matrix-Game 2.0 | arXiv:2508.13009 | 2025 |
| Vid2World | arXiv:2505.14357（ICLR 2026） | 2025 |
| WorldPlay | arXiv:2512.14614 | 2025 |
| WBench / WorldMark | arXiv:2605.25874 等 | 2026 |

### 本地引用指针

- 4 份调研 brief：`document/Routine/02-算法复现与源码库/agent_harness_game/research/R1-benchmarks.md`、`R2-harness-verification.md`、`R3-execution-interaction.md`、`R4-supporting-evals.md`
- 代码基线：`agent_harness_game/verifier.py:77-184`（现有四维 evaluate 实现）

---

*综合整理：作家_调研笔记 · 2026-07-20 · 基于 R1–R4 四份 brief，未新增 brief 之外的论文或数据*
