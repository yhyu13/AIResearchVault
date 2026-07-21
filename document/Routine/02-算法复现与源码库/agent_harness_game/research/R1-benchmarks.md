# R1 — 游戏 Agent Benchmark 与评测协议调研（调研员_基准评测）

> 输入文件：`01e-game-benchmarks-latest.md`、`01e-rl-games-envs-latest.md`
> 目标：为 agent_harness_game 的 V（Verification/Evaluation）组件提供 benchmark 级的评估维度、指标公式与评测协议设计依据。
> 现有 V 组件基线：`verifier.py` 中 `TaskVerifier.evaluate()`，四维评估 —— `structure_correctness`(0.4) / `block_count`(0.2) / `efficiency`(0.2) / `inventory_match`(0.2)，pass 阈值 overall ≥ 0.75 且关键维 ≥ 0.75/0.8。

---

## 1. 相关论文/实现清单

| 名称 | 来源 | 年份 | 一句话定位 |
|------|------|------|-----------|
| VideoGameBench | arXiv:2505.18134 | 2025 | VLM 实时通关 90 年代游戏，checkpoint 进度度量 + Lite 设置隔离 latency |
| Orak | arXiv:2506.03610 | 2025 | 12 款全 genre 游戏 benchmark，MCP 接口支持 agentic 模块消融 + battle arena 排名 |
| TextQuests | arXiv:2507.23701 | 2025 | Infocom 文字冒险 long-horizon benchmark，Game Progress + Mean Harm 双指标 + autosave 协议 |
| GVGAI-LLM | arXiv:2508.08501 | 2025 | 118 款 ASCII 街机游戏，VGDL 程序化生成防污染，meaningful step ratio / step efficiency 可解释指标 |
| FlashAdventure | arXiv:2509.01052 (EMNLP 2025 Main) | 2025 | 34 款 Flash 冒险游戏 full story arc，CUA-as-a-Judge 自动裁判，milestone 完成率 |
| VisEscape | arXiv:2503.14427 | 2025 | 20 个虚拟密室逃脱，最小化目标（"逃出去"）下的 exploration-driven planning |
| SPIRAL | arXiv:2506.24119 | 2025 | 零和 self-play RL，RAE（role-conditioned advantage）按 game×role 去偏（先手优势校准） |
| RLVE | arXiv:2511.07317 | 2025 | 400 个自适应 verifiable 环境，难度跟随策略能力（zone of proximal development） |
| GEM | arXiv:2510.01051 | 2025 | agentic LLM 的 Gym，异步向量化 rollout + PPO/GRPO/REINFORCE 公平基准协议 |
| AutoForge | arXiv:2512.22857 | 2025 | 自动环境合成 + environment-level advantage（按环境去均值的分层 baseline） |
| R-Zero / Absolute Zero | arXiv:2508.05004 / 2505.03335 | 2025 | edge-of-learnability reward：通过率居中（~50%）的任务信息量最大 |

---

## 2. 评估维度与指标

### 2.1 进度/成功率类

- **Checkpoint / milestone 进度占比**：VideoGameBench 用自动检测的 checkpoint 占比度量游戏进度（无需读游戏内存）；FlashAdventure 用 milestone 完成率；TextQuests 用专家标注 checkpoint 的 Game Progress。统一形式：`progress = |completed checkpoints| / |total checkpoints| ∈ [0,1]`。（来源：01e-game-benchmarks-latest.md:18-22, 56, 66, 186）
- **完整通关率（binary success）**：TextQuests / VisEscape 均以"是否完整通关"为终极指标——结果是 SOTA 模型通关率为 0，说明粗粒度 binary 指标区分度不足，必须与细粒度进度指标配合。（来源：01e-game-benchmarks-latest.md:119, 134, 221）
- **Full story arc completion**：从"单任务完成"升级为"完整故事线通关"（FlashAdventure），是 long-horizon 任务的评估目标范式。（来源：01e-game-benchmarks-latest.md:198）

### 2.2 效率/行为质量类

- **Meaningful step ratio（GVGAI-LLM）**：度量 agent 每一步是否"有意义"（真正推进游戏状态），可解释、可从评估指标转化为训练信号。风险：用作奖励可能鼓励短视策略。（来源：01e-game-benchmarks-latest.md:152, 158, 167；公式细节见论文正文，摘要未给出）
- **Step efficiency / overall score（GVGAI-LLM）**：与 meaningful step ratio 并列的可解释指标组。（来源：同上）
- **Turn/episode 效率**：harness 现有 `efficiency = max(0, 1 − turns_used / max_turns)` 与该类指标同族。（来源：verifier.py:136）

### 2.3 安全/代价类

- **Mean Harm（TextQuests）**：agent 在游戏中的危险/破坏性操作计数，把安全维度纳入游戏评估；可迁移为通用 agent 的"harm 计数"（误删文件、误下单）。（来源：01e-game-benchmarks-latest.md:119, 127, 132）

### 2.4 诊断性指标（定位失败原因）

- **Latency 隔离**：VideoGameBench Lite 设置——暂停游戏时钟等待模型输出，分离"推理质量"与"推理速度"两个变量；实时版 0.48% vs Lite 版 1.6% 的落差本身就是诊断指标。（来源：01e-game-benchmarks-latest.md:50, 64-65）
- **模态解耦**：GVGAI-LLM 用 ASCII 表征把 spatial reasoning 从视觉感知中解耦单测；Orak 做 text vs vision 输入模态消融。（来源：01e-game-benchmarks-latest.md:152, 160, 98）
- **Observation-behavior gap（FlashAdventure）**：形式化"观测到信息 ≠ 行为上利用信息"，是长程 agent 的统一瓶颈候选；可通过"给 clue 后性能增量"间接测量（TextQuests 的对照设计）。（来源：01e-game-benchmarks-latest.md:186, 190, 261）

### 2.5 训练信号即评估指标（RL 环境侧）

- **Verifiable reward 谱系**：终局胜负（SPIRAL）、code executor 校验（Absolute Zero）、算法验证器（RLVE）、游戏规则（GEM 环境自带）——共同点是 anti-hacking、程序化可验证。（来源：01e-rl-games-envs-latest.md:23, 302）
- **RAE（SPIRAL）**：role-conditioned advantage，按 (game, role) 维护独立 baseline $b_{G,p}$，advantage = 实际回报 − 角色条件 baseline，吸收先手优势等结构性偏差。（来源：01e-rl-games-envs-latest.md:50, 54）
- **Environment-level advantage（AutoForge）**：同环境内多条轨迹聚合估计优势，等价于按环境去均值——与 RAE 同属"对混淆因子做条件化 baseline"的分层建模思想。（来源：01e-rl-games-envs-latest.md:240, 245）
- **Edge-of-learnability（R-Zero）/ 自适应难度（RLVE）**：任务通过率居中（~50%）时 reward/信息量最大；RLVE 按策略当前通过率调整环境生成参数，保持难度在可学习区间。（来源：01e-rl-games-envs-latest.md:113, 124, 176, 180）

---

## 3. 评测协议设计

### 3.1 多任务套件与规模

- **套件规模范式**：10 款（VideoGameBench）→ 12 款全 genre（Orak）→ 25 款（TextQuests）→ 34 款（FlashAdventure）→ 118 款（GVGAI-LLM）→ 400 环境（RLVE-Gym）。结论：跨任务数量本身就是泛化证据，单一任务高分不可信。（来源：01e-game-benchmarks-latest.md:246-253）
- **Genre/能力覆盖设计**：Orak 按 action/RTS/RPG/sports/puzzle 全 genre 覆盖；GIFT 按能力轴（推理/规划/创造力/社会交互）选游戏组合。（来源：01e-game-benchmarks-latest.md:96；01e-rl-games-envs-latest.md:271, 283）

### 3.2 防污染 / generalization split

三条路线（"藏、标记、造"）：

1. **保密 split（藏）**：VideoGameBench dev/test split + 3 款保密游戏测 generalization、防数据泄漏。
2. **Canary GUID（标记）**：TextQuests 数据集内嵌 canary GUID，可审计是否进入训练语料。
3. **程序化生成（造）**：GVGAI-LLM 用 VGDL 无限生成新游戏规则与关卡，评测集可持续刷新，天然抗 overfitting；RLVE 同样靠程序化生成提供无限题目。注意需"生成-验证"闭环确认可解性。
（来源：01e-game-benchmarks-latest.md:54, 63, 135, 156, 165, 257；01e-rl-games-envs-latest.md:176）

### 3.3 变量隔离协议（ablation-as-protocol）

- **Lite 设置**：暂停时钟隔离 inference latency（VideoGameBench）。
- **禁工具设定**：无搜索/无计算器/无代码执行，隔离 intrinsic reasoning（TextQuests）。
- **Autosave 机制**：可控地研究 trial-and-error 学习；"给 clue + autosave"前后对比用于归因（瓶颈在长上下文状态管理而非知识）。
- **模块消融**：Orak 用 MCP plug-and-play 接口对 memory/planner/self-reflection 模块做即插即用替换消融。
（来源：01e-game-benchmarks-latest.md:62, 64, 125, 131, 133-134, 88, 97）

### 3.4 统计可靠性

- **对战排名方差**：Orak battle arena 的 Elo 式排名对采样方差、随机种子、先手优势敏感；引用排名需看置信区间，先手优势需校准——这正是 SPIRAL RAE 在训练侧解决的问题（按 game×role 去偏），评估侧同样需要 per-role/per-seed 分层统计。（来源：01e-game-benchmarks-latest.md:92, 105；01e-rl-games-envs-latest.md:54）
- **自动裁判的校准**：FlashAdventure CUA-as-a-Judge 免人工标注，但 judge 误差会传递给被测 agent 排名，同源模型可能产生系统性偏置——需要人工抽检校准 judge。（来源：01e-game-benchmarks-latest.md:192）
- **Env-level 聚合**：AutoForge 的按环境聚合去均值思想可直接用于评估侧——同一任务多 seed 多 rollout 聚合报告，而非单条轨迹定胜负。（来源：01e-rl-games-envs-latest.md:240）

### 3.5 RL 环境的 reward 与 done 信号定义

- **Reward**：优先 verifiable（终局胜负 / 规则验证器 / executor 校验），避免 learned reward model 被 hack；dense per-turn reward 与 outcome-level 归一化不兼容（GEM 对 GRPO 的批评），multi-turn 场景需要 per-turn 信号或 ReBN 式 return batch normalization。（来源：01e-rl-games-envs-latest.md:208, 213, 221）
- **Done/课程信号**：难度应跟随策略通过率（RLVE adaptive difficulty / R-Zero edge-of-learnability），太易/太难均无梯度；评估侧的对应物是按当前能力分桶报告成功率，而非单一总成功率。（来源：01e-rl-games-envs-latest.md:26, 113, 180）
- **已知风险**：零数据/程序化环境的共同风险是分布坍缩与 reward hacking（Absolute Zero 的 "uh-oh moment"、AutoForge 环境 bug 被 exploit），V 组件需内置"课程健康监控"与不变量校验。（来源：01e-rl-games-envs-latest.md:96, 244, 310, 317）

---

## 4. 对 harness V 组件的落地建议

现有 `TaskVerifier` 四维（structure/count/efficiency/inventory）本质上是**单任务、单轨迹、静态阈值**的终局检查器。以下是可逐项落地的增强清单：

### 4.1 新增维度（建议在 2D 沙盒中实现）

1. **Meaningful step ratio（新增，高优先级）**：统计每个 turn 是否改变了游戏状态（放置/拆除/合成/移动成功 vs 无效动作）。实现容易——harness 的 environment.step 返回结果即可判定。对应 GVGAI-LLM 指标，可直接作为 efficiency 维度的分子级细化。
2. **Checkpoint/milestone 进度（新增，高优先级）**：把 `TaskSpec.target_blocks` 改造为有序 milestone 序列（如 收集木→合成木板→放置墙），报告 `progress = completed/total`，替代纯终局 0/1 判定。解决 TextQuests 教训：binary success 区分度不足。
3. **Mean Harm / 破坏性操作计数（新增）**：统计误拆目标方块、破坏已有正确结构、无效合成等"负进展"动作次数。2D 沙盒中可直接定义为"拆除 target_blocks 中方块的次数 + extra blocks 数"。与现有 `details["extra_blocks"]` 互补但更显式。
4. **Seed/环境方差报告（新增，协议层）**：同一 TaskSpec 在 N 个随机初始布局（agent 出生点、资源分布）上跑 M 次，报告 mean ± std 与 pass rate（即 pass@1 的多次估计），替代单次 rollout 的 `passed` 布尔值。对应 AutoForge env-level 聚合思想。

### 4.2 增强现有维度

- **efficiency**：现有线性衰减 `1 − turn/max_turns` 可保留，但建议与 meaningful step ratio 联合报告（区分"慢但在推进"与"快但在空转"）。
- **block_count**：并入 Mean Harm 视角——超出 max_blocks 的惩罚即"harm"，建议统一进破坏性操作计数而非独立维度（可选替换）。
- **structure_correctness**：保留，但建议从全量比对改为 milestone 加权（关键结构块权重高），对应 checkpoint 占比思想。

### 4.3 评测协议层（V 组件的外围基础设施）

- **多任务套件**：扩展 TaskSpec 工厂（现有 3 个任务）为按能力轴分组的套件：建造类（structure）、合成类（inventory）、探索类（资源定位）、长程组合类（house = 采集+合成+建造），每类 ≥3 个实例，对齐 Orak/GIFT 的覆盖设计。
- **Generalization split**：train/dev/test 任务参数分离——测试集用未见过的坐标/规模/配方组合；沙盒天然支持程序化生成（改 seed 即可），是"造"路线。
- **Ablation-as-protocol**：对 harness 六组件（E/T/C/S/L/V）做开关消融（如关掉 L 的 learning 模块前后对比 pass rate），复用 Orak 的 MCP 式模块消融思想；这恰好是 harness 架构的天然卖点。
- **难度自适应报告**：按任务难度分桶报告成功率，避免单一总分掩盖"只会做简单题"（RLVE 教训）。

### 4.4 与现有四维的关系总表

| 维度 | 处理方式 | 依据 |
|------|---------|------|
| structure_correctness | 增强（milestone 加权 + 进度占比） | VideoGameBench/TextQuests checkpoint 度量 |
| block_count | 可替换/并入 harm 计数 | TextQuests Mean Harm |
| efficiency | 增强（联合 meaningful step ratio） | GVGAI-LLM |
| inventory_match | 保留 | — |
| meaningful_step_ratio | 新增 | GVGAI-LLM |
| milestone_progress | 新增 | VideoGameBench / FlashAdventure |
| mean_harm | 新增 | TextQuests |
| 多 seed pass rate ± std | 新增（协议层） | AutoForge env-level 聚合 / Orak arena 统计可靠性 |

---

## 5. 引用指针

本地文件（`C:\Git-repo-my\AIResearchVault\document\Routine\01-论文阅读与研究库\`）：

- `01e-game-benchmarks-latest.md:18-29` — benchmark 度量函数形式化与设计矛盾
- `01e-game-benchmarks-latest.md:50, 62-66` — VideoGameBench checkpoint 进度、Lite 设置、保密 split、0.48%/1.6% 结果
- `01e-game-benchmarks-latest.md:88, 92, 96-99, 105` — Orak MCP 消融、battle arena 统计可靠性、genre 覆盖
- `01e-game-benchmarks-latest.md:119, 125, 127, 131-135` — TextQuests Game Progress + Mean Harm、autosave、canary GUID、clue 对照
- `01e-game-benchmarks-latest.md:152, 156, 158, 160, 165-168` — GVGAI-LLM meaningful step ratio、VGDL 程序化生成、ASCII 解耦
- `01e-game-benchmarks-latest.md:186, 190, 192, 198, 200` — FlashAdventure observation-behavior gap、CUA-as-a-Judge、full story arc
- `01e-game-benchmarks-latest.md:246-263` — 六 benchmark 横向对比表与趋势（防污染三路线、诊断转向）
- `01e-rl-games-envs-latest.md:18-30` — verifiable reward 形式化与核心矛盾
- `01e-rl-games-envs-latest.md:50, 54` — SPIRAL RAE 公式化描述
- `01e-rl-games-envs-latest.md:113, 124` — R-Zero edge-of-learnability reward
- `01e-rl-games-envs-latest.md:176, 180, 189` — RLVE 自适应难度、environment scaling 对照实验
- `01e-rl-games-envs-latest.md:208, 213, 221` — GEM ReBN vs GRPO、dense per-turn reward 论证
- `01e-rl-games-envs-latest.md:240, 244-245` — AutoForge environment-level advantage、合成环境正确性验证
- `01e-rl-games-envs-latest.md:296-319` — 横向对比表（verifier/课程机制列）与开放问题
- `verifier.py:77-184` — 现有 V 组件四维实现基线

网络检索（2 次）：

- https://arxiv.org/abs/2508.08501 — GVGAI-LLM 摘要（确认三指标名称；具体公式在论文正文，摘要未含）
- https://arxiv.org/abs/2507.23701 — TextQuests 摘要（确认禁工具设定与 long-horizon 定位）

*创建时间：2026-07-20 · 调研员_基准评测*
