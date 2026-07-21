# R3 Brief：执行与交互评估（Execution & Interaction Evaluation）

> 角色标签：调研员_执行交互评估
> 输入：01e-game-agent-execution-latest.md、01e-human-ai-interaction-latest.md、01a-LLM-Agent-in-Games.md（+ 1 次网络补充：GameWorld 指标公式）
> 目标：为 harness V 组件设计过程/轨迹级评估、LLM-as-judge、人机交互指标、长程中间里程碑评估
> 日期：2026-07-22

---

## 1. 相关论文/实现清单

| 名称 | 来源/年份 | 一句话定位 |
|------|-----------|-----------|
| GameWorld | arXiv:2604.07429, NUS/Oxford, 2026 | 状态断言式可验证评测：34 游戏 170 任务，SR + normalized Progress 全部从序列化 gameAPI 状态计算，不用截图/LLM judge |
| FlashAdventure | arXiv:2509.01052, EMNLP 2025 | 完整故事线 benchmark；提出 CUA-as-a-Judge 自动评测器与 milestone completion 指标；定义 observation-behavior gap |
| OmniGameArena | arXiv:2606.09826, 2026 | UE5 基准；核心创新 Improvement Dynamics Curve (IDC) + held-out 泛化衰减，区分"记住答案"与"学会技能" |
| Orak | arXiv:2506.03610, 2025–2026 | 12 游戏 MCP 统一接口；leaderboard + Elo 式 battle arena + 模态×策略×微调消融矩阵 |
| ODYSSEY | arXiv:2407.15325, IJCAI 2025 | planner-actor-critic 架构；LLM Critic 自验证动作效果；三类任务基准（长程规划/动态即时/自主探索） |
| Optimus-3 | arXiv:2506.10357, 2025–2026 | DGRPO 过程-结果双粒度奖励：Dependency-Aware Synthesis Reward + Hallucination-Aware Consistency Reward |
| MindForge | arXiv:2411.12977, NeurIPS 2025 | 科技树 milestone 数 + unique items 数作为 Minecraft 长程进展指标（3× / 2.3× 于 Voyager） |
| Beyond Survival | arXiv:2510.11389, 2025 | strategy-alignment 评测：以赢家策略为 reference 的 Speech MC + Decision 一致性，即 reference-ification |
| When Agents Lie | arXiv:2607.05132, ICML NExT-Game WS Best Paper 2026 | plan → announcement → action 三阶段协议；premeditation rate = plan-action 一致性 |
| C2C | arXiv:2604.25088, Berkeley, 2026 | 人 vs AI 谈判行为定量指标（deal complexity、直接接受率 56.3% vs 67.6%），行为差异→targeted prompting |
| Among Us Deception | arXiv:2603.26635, AAMAS 2026 | speech act + IDT 标注框架，role-conditioned 言语行为分布作为可计算指标 |
| Scheming in LLM-to-LLM | arXiv:2510.12826, 2025 | ability vs propensity 区分；Peer Evaluation 100% 欺骗率、Cheap Talk 95–100% 成功率 |
| Bounded Autonomy | arXiv:2604.04703, 2026 | whisper steering 成功率、embedding grounding 质量、reply-chain 稳定性——runtime 可控性指标 |
| R3D2 (Hanabi) | arXiv:2503.14555, ICLR 2025 | ad hoc coordination 评估：与异构 agent 池零样本协作得分 |
| Voyager | NeurIPS 2023 | 自动课程 + 技能库；任务完成度 + 技能库增长曲线作为终身学习证据 |

---

## 2. 评估维度与指标

### 2.1 结果级（outcome-based）——GameWorld 范式 [出处：01e L255, L267；gameworld-project.github.io]
- **Success Rate**：`SR = (1/N) Σ_i 1[status_i = success]`，二元，来自序列化 gameAPI 状态断言（坐标、分数、checkpoint）。
- **normalized Progress**（单次运行）：
  `progress_i = clip_[0,1]( (q_i^max − b_i) / (τ_i − b_i) )`
  其中 `q_i^max` 为运行中观测到的最高任务分数，`b_i` 初始分数，`τ_i` 目标分数。聚合 `PG = (1/N) Σ progress_i`。
  意义：区分"一开始就失败"与"完成 90% 后失败"（论文 Minecraft Clone 案例：agent 达 ~90% progress 但 SR=0）。
- **人类基线锚定**：GameWorld 报 Novice (PG 64.1%) / Expert (82.6%) 人类基线，agent 分数以人类差距解读。

### 2.2 过程/轨迹级
- **Milestone completion rate**（FlashAdventure / MindForge）：把长程任务分解为有序里程碑序列，报完成比例；MindForge 用 tech-tree milestones + unique items 计数（3× / 2.3× 于 Voyager）。[01e L52, L203]
- **Plan-action consistency / premeditation rate**（When Agents Lie）：三阶段协议 plan → announcement → action，度量偏离公开宣告的行动中已在私有 plan 中写好的比例（实验中 >90%）。通用化为：**agent 声明的子目标与实际执行动作的一致率**。[01e-human L50, L63]
- **过程奖励可验证化**（Optimus-3 DGRPO）：crafting 依赖路径直接作为 thinking reward；Dependency-Aware Synthesis Reward + Hallucination-Aware Consistency Reward——"好结果必须配好过程"。[01e L86, L101]
- **Action validity diagnostics**（GameWorld）：非法/未注册动作调用率、超出 control space 的动作比例，作为 instruction-following 可靠性指标。[网络补充: swiftscholar]

### 2.3 动态/学习曲线级
- **Improvement Dynamics Curve (IDC)**（OmniGameArena）：分数随反思轮数演化的曲线；斜率 = learnability；形状（线性/对数/饱和）各有含义。[01e L288, L292]
- **Held-out 泛化衰减**：学到的 skill/prompt 在任务变体上的得分衰减幅度，区分"记住答案"vs"学会技能"——skill 在 held-out 上普遍衰减是关键证伪设计。[01e L288, L294]

### 2.4 LLM-as-judge 及其可靠性
- **CUA-as-a-Judge**（FlashAdventure）：用 computer-use agent 自动评判游戏进度；需量化 judge 的假阳性（误判成功）与假阴性（漏判成功），judge 能力上限约束评测有效性。[01e L187, L195]
- **Critic 自验证降级设计**（Odyssey 引导问题）：LLM critic 误判成功（false positive）会沿规划链累积错误；建议用游戏内状态（inventory、位置）做 ground-truth 校验，把 LLM critic 降级为"语义解释器"而非"裁判"。[01e L125]
- **横向判断**（01e L30）："LLM-as-judge 便宜但不可靠，状态断言可靠但需逐游戏人工编写"——V 组件应状态断言优先，judge 仅兜底无 ground-truth 的维度。

### 2.5 人机交互/社交指标
- **Reference-ification / strategy-alignment**（Beyond Survival）：把 open-ended 行为转成有 reference 的判别式评测——"该说什么"形式化为 MC，"该怎么做"形式化为决策一致性；绕开生成式评测无标准答案。[01e-human L151, L168]
- **行为分布指标**（C2C / Among Us）：deal complexity、承诺接受率、speech-act 分布（directive vs representative）、equivocation 率——role-conditioned 分布差异可测。[01e-human L98, L129]
- **Runtime 可控性指标**（Bounded Autonomy）：whisper steering 成功率、grounding 质量（意图→可执行动作映射成功率 + fallback 触发率）、reply-chain 长度分布。[01e-human L286, L296]
- **Ad hoc 协作得分**（R3D2）：与异构伙伴池零样本协作的平均得分。

---

## 3. 评测协议设计

1. **状态断言协议**（GameWorld）：每任务 = 自然语言目标 + 可配置初始化 + 目标度量 + 基于序列化状态的可验证 evaluator。推理时暂停环境（decouple latency），固定 seed，隔离实例，readiness gate 保证一致起始条件。重复运行 σ 仅 0.5–1.1% → 协议本身可复现性需自证（repeated-evaluation robustness study）。
2. **里程碑协议**（FlashAdventure）：完整故事线 = 有序 milestone 序列；报 milestone completion rate 而非单一终局分数；配人类基线量化人机差距。
3. **IDC 协议**（OmniGameArena）：bounded skill prompt（限制大小/结构防无限堆 prompt）+ tool-using reflector 多轮精炼；skill 必须在 held-out 任务变体上验证；PvP/Coop 模式归因困难，建议固定对手做"训练伴侣"。
4. **三阶段协议**（When Agents Lie）：private plan / public announcement / final action 分离记录，使 plan-action consistency 可计算——轨迹日志协议设计的范本。
5. **消融矩阵**（Orak）：输入模态 × agentic 策略 × 微调的系统消融；Elo 排名注意非平稳 agent 问题（可用 Glicko-2 替代）。
6. **能力对齐课程**（GameWorld）：任务按 5 级能力课程组织（timing grounding → reactive control → … → long-horizon coordination），性能按级别分解定位瓶颈。
7. **2D 沙盒落地**：固定 seed × 每任务 N≥5 次重复；报 SR 与 PG 双指标 + 标准差；episode 内按 turn 记录状态快照形成轨迹。

---

## 4. 对 harness V 组件的落地建议

现有 `verifier.py` 四维评估（structure_correctness / block_count / efficiency / inventory_match）全部是**终局状态断言**，对应 GameWorld 的 SR 范式，但缺 PG、缺过程级、缺协议层。建议：

### 4.1 增强（enhance 现有维度）
- **efficiency → normalized Progress**：将 `1 − turn/max_turns` 线性惩罚替换为 GameWorld 公式
  `progress = clip[0,1]((achieved − baseline) / (target − baseline))`，
  其中 achieved 可取"已正确放置的目标方块数"等任务相关量。structure_correctness 本身即一种 PG，但应把 `correct/total` 推广为**运行中历史最高值**（`q_i^max`，防止终局恰好被破坏而低估能力）——当前只评估终局 state。
- **新增 penalty 维度**：`extra_blocks` 已计算但未进分。加入 `precision = correct / (correct + extra)`，与 recall（现 structure_correctness）配对，防止"铺满全图"刷分。

### 4.2 新增（new dimensions）
1. **trajectory_milestone（轨迹级）**：TaskSpec 增加 `milestones: List[partial target state]`（如 craft_planks 任务：获得 wood → 合成 plank ×1 → plank ×4）。每 turn 检查里程碑命中，报 milestone completion rate + 首次命中 turn。实现成本低：复用现有断言逻辑对中间快照求值。对应 FlashAdventure/MindForge。
2. **action_validity（过程级）**：统计无效动作率（非法位置、材料不足的 craft、解析失败的指令）= 无效动作数 / 总动作数。对应 GameWorld action-validity diagnostics；直接反映 agent 幻觉率。
3. **plan_action_consistency（过程级）**：若 agent 有 L（Learning/规划）模块输出子目标序列，记录"声明子目标 → 实际达成"的一致率（When Agents Lie 协议的正面用法：用于可靠性而非欺骗检测）。
4. **improvement_curve（动态级，跨 episode）**：同一任务变体族上，agent 经验/技能库增长后 SR/PG 的演化曲线（IDC）；配 held-out 变体验证技能泛化（ OmniGameArena 的"记住 vs 学会"证伪）。2D 沙盒极易生成任务变体（平移目标位置、换方块类型），是天然优势。

### 4.3 协议层建议（不改维度，改 evaluate() 用法）
- **终局 + 轨迹双轨**：`evaluate(state)` 保留终局 SR；新增 `evaluate_trajectory(snapshots)` 报 PG（取 q^max）与 milestone 命中率。
- **N 次重复 + σ 报告**：pass 阈值判断改为 `SR ≥ threshold over N seeds`，并报告标准差自证可复现性（GameWorld robustness 做法）。
- **LLM-judge 定位为兜底**：仅用于无状态断言维度（如"建筑美观/功能"这类开放目标，见 01a L144），且必须配 false-positive/negative 抽检；所有可状态化的判断一律走断言（GameWorld 教训 + Odyssey critic 教训）。

### 4.4 关系总结表

| 现有维度 | 处置 | 说明 |
|----------|------|------|
| structure_correctness | 增强 | 改为 recall + 新增 precision；支持 q^max 历史最高取值 |
| block_count | 保留 | 已被 precision 部分覆盖，可降为诊断 details |
| efficiency | 增强/替换 | 用 normalized Progress 替代线性 turn 惩罚 |
| inventory_match | 保留 | 状态断言范式正确，无需改 |
| trajectory_milestone | 新增 | 长程中间里程碑完成率 |
| action_validity | 新增 | 无效/幻觉动作率 |
| plan_action_consistency | 新增 | 声明-执行一致率 |
| improvement_curve + held-out | 新增（跨 episode） | IDC + 泛化衰减 |

---

## 5. 引用指针

- 01e-game-agent-execution-latest.md:30（judge vs 断言矛盾）, :52（MindForge milestone/items）, :86/:101（DGRPO 过程奖励）, :125（critic 降级）, :187/:195/:203（FlashAdventure CUA-judge/milestone）, :221/:235（Orak Elo/消融）, :255/:267（GameWorld SR/PG/状态断言）, :288/:292/:294（IDC/held-out）, :316（评测三范式总结）
- 01e-human-ai-interaction-latest.md:50/:63（三阶段协议/premeditation）, :98（C2C 行为指标）, :129/:132（speech-act 分布）, :151/:168（strategy-alignment/reference-ification）, :184（scheming ability vs propensity）, :252/:269（R3D2 ad hoc 评估）, :286/:296/:302（bounded autonomy 可控性指标）
- 01a-LLM-Agent-in-Games.md:23（V 形式化 V(a_t,s_t)→pass/fail/retry）, :144（"好房子"多维评估问题）, :134（评估方式对比表）
- 网络补充（GameWorld 公式与协议细节）：
  - https://gameworld-project.github.io/ （SR/PG 定义、人类基线 Novice 64.1 / Expert 82.6）
  - https://www.swiftscholar.net/paper/69dae0ace63e77db717ca0de （progress_i = clip[0,1]((q_i^max − b_i)/(τ_i − b_i))；σ 0.5–1.1%；5 级课程）
  - https://www.alphaxiv.org/overview/2604.07429v1 （双接口、paused execution、memory 敏感性）
- 本地代码：agent_harness_game/verifier.py:91-180（现有四维 evaluate 实现）
