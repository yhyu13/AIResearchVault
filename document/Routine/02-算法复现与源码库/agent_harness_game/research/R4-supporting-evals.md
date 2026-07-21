# R4 — 支撑组件评估调研 Brief（tool calling / sandbox / memory / world model → V 组件）

> 角色：调研员_支撑组件评估
> 输入：01d-tool_calling-latest.md、01d-sandbox-latest.md、01d-memory-latest.md、01e-world-models-latest.md
> 目标：为 Agent Harness H=(E,T,C,S,L,V) 的 **V（Verification/Evaluation）组件** 提炼可落地的评估维度与协议
> 说明：本 brief 全部基于本地四个文件的实际内容整理；未额外做网络检索（文件已包含指标定义与协议要点）。

---

## 1. 相关论文/实现清单

### Tool Calling 方向（01d-tool_calling-latest.md）

| 名称 | 来源 | 年份 | 一句话定位 |
|---|---|---|---|
| When2Tool / Probe&Prefill | arXiv 2605.09252 | 2026 | 18 环境工具必要性基准；用 hidden-state 线性探针（AUROC 0.89–0.96）量化 over-tooling |
| Atomix | arXiv 2602.14849 | 2026 | 工具调用的事务语义（Execute→Seal→Frontier Check→Settle），并发/不可逆效果的一致性 |
| PASTE / SPORK / B-PASTE | arXiv 2603.18897 等 | 2026 | 推测执行加速；量化工具延迟占比（16–37% / 35–61%）与推测正确率 |
| ReTool | arXiv 2504.11536 | 2025 | RL 工具策略；outcome reward、AIME 67.0%、400 步训练效率 |
| ToolACE-R | AAAI 2026 | 2026 | 模型感知迭代训练 + 自适应自精炼；在 BFCL / API-Bank 上评估 |
| 综述（Wang et al.）+ BFCL / API-Bank / ToolSandbox / τ-Bench | ACM Computing Surveys | 2026 | Pre-call/On-call/Post-call 三阶段框架与 10+ 评估基准对比 |

### Sandbox / 安全方向（01d-sandbox-latest.md）

| 名称 | 来源 | 年份 | 一句话定位 |
|---|---|---|---|
| SafeArena | ICML 2025 (PMLR 267) | 2025 | 250 safe + 250 harmful Web Agent 任务；Agent Risk Assessment 四风险等级 |
| ceLLMate | arXiv 2512.12594 | 2025 | 浏览器级沙箱；ambient authority 限制与 blast radius 度量 |
| Crab | arXiv 2604.28138 | 2026 | 语义感知 C/R；恢复正确率（8%→100%）、checkpoint 流量、RL rollout 分支节约 |
| LLM-in-Sandbox | arXiv 2601.16206 | 2026 | 沙箱激发通用智能；token 消耗 8× 降低 |
| EnvSimBench | arXiv 2605.07247 | 2026 | LLM 环境模拟器 fidelity 基准；fidelity 随步数衰减曲线 |
| Agent-World | arXiv 2604.18292 | 2026 | 真实 MCP 锚定环境合成；程序化可验证 reward |

### Memory 方向（01d-memory-latest.md）

| 名称 | 来源 | 年份 | 一句话定位 |
|---|---|---|---|
| Mem0 | arXiv 2504.19413 | 2025 | 生产级记忆层；LOCOMO 上超 OpenAI 26%，P95 延迟 -91%，token -90% |
| Zep / Graphiti | arXiv 2501.13956 | 2025 | 双时间戳时序知识图谱；DMR 94.8%，LongMemEval 63.8% |
| A-MEM | NeurIPS 2025 / arXiv 2502.12110 | 2025 | Zettelkasten 记忆网络；LoCoMo 多跳 ROUGE-L 约 5.8× 提升 |
| Memory-R1 | arXiv 2508.19828 | 2025 | RL 记忆管理（ADD/UPDATE/DELETE/NOOP）；LOCOMO F1 +48%，152 样本收敛 |
| HiMem | arXiv 2601.06377 | 2026 | 分层 Episode→Note 记忆 + 冲突感知再巩固 |
| MemP / LEGOMem | arXiv 2508.06433 / 2510.04851 | 2025 | 程序记忆（目标-轨迹-反馈三元组）；LEGOMem 任务完成时间 -34%，错误恢复率 +28% |
| LoCoMo / LongMemEval 基准 | arXiv 2402.17753 / 2410.10813 | 2024 | 长程对话记忆标准评估（单跳/时序/多跳/开放域） |

### World Model 方向（01e-world-models-latest.md）

| 名称 | 来源 | 年份 | 一句话定位 |
|---|---|---|---|
| MineWorld | arXiv 2504.08388 | 2025 | Minecraft 开源交互世界模型；提出**动作跟随精度 + 视觉保真度**双轨评测协议 |
| Matrix-Game 2.0 | arXiv 2508.13009 | 2025 | Self-Forcing 蒸馏 720p/25fps；与 Oasis/MineWorld 的质量-实时性双指标对比 |
| Vid2World | arXiv 2505.14357 (ICLR 2026) | 2025 | 视频扩散改世界模型；用**下游 planning/policy 收益**做 value-aware 评估 |
| WorldPlay | arXiv 2512.14614 | 2025 | 显式 3D 几何记忆；定义 **revisit consistency（场景重访一致性）** 指标 |
| WBench / WorldMark | arXiv 2605.25874 等 | 2026 | 多轮交互世界模型专用 benchmark 层（一致性排名） |
| EnvSimBench（交叉引用） | arXiv 2605.07247 | 2026 | "幻觉环境"警告：模拟器 fidelity 衰减 → agent 学到错误策略 |

---

## 2. 评估维度与指标

### 2.1 Tool calling 正确性评估（→ 映射 harness 的 T 组件验证）

| 维度 | 指标 | 定义/公式 | 出处 |
|---|---|---|---|
| 工具必要性 | Over-tooling rate | 不必要工具调用数 / 总调用数；When2Tool 报告 Probe&Prefill 减少 48% 调用、准确率仅降 1.7% | 01d-tool_calling-latest.md:47, 63 |
| 必要性可解码性 | Hidden-state AUROC | 线性探针从 hidden states 解码"是否需要工具"，AUROC 0.89–0.96 | 01d-tool_calling-latest.md:47, 61 |
| 参数/选择正确性 | AST match / 工具选择准确率 | BFCL、API-Bank 标准协议：工具名 + 参数的结构化匹配 | 01d-tool_calling-latest.md:182, 216 |
| 有状态多步正确性 | ToolSandbox 状态匹配 | 对话式、有状态工具调用序列的最终世界状态比对 | 01d-tool_calling-latest.md:216, 276 |
| 事务一致性 | 事务成功率 / 延迟开销 / 并发度 | Atomix 四阶段结算下的 commit/abort 比例与协调开销 | 01d-tool_calling-latest.md:96 |
| 延迟结构 | 工具时间占比 | 工具执行时间 / 总任务时间（PASTE 测得 16–37%，另一处 35–61%）；推测执行后任务完成时间 -43.5% | 01d-tool_calling-latest.md:114, 126 |
| 结果验证门控 | V(r,q)→{pass,retry,abort} | 执行后验证三态决策，错误级联（错误传播放大）计数 | 01d-tool_calling-latest.md:23, 31 |

### 2.2 Sandbox 安全违例度量（→ 映射 harness 的 E/S 边界验证）

| 维度 | 指标 | 定义/公式 | 出处 |
|---|---|---|---|
| 有害任务合规率 | Harmful completion rate | 完成的有害任务数 / 有害任务总数；GPT-4o 34.7%、Qwen-2 27.3%、Claude-3.5 22.8% | 01d-sandbox-latest.md:118, 139 |
| 风险分级 | Agent Risk Assessment | 四级：Compliant / Partial / Refusal / Error（Partial 边界需自定义，如完成 80% 步骤） | 01d-sandbox-latest.md:118, 124, 130 |
| 权限泄漏面 | Ambient authority / blast radius | Agent 自动获得的敏感操作空间大小（如单次购买金额上限、跨站 Cookie 携带）；ceLLMate 的 blast radius 对比实验 | 01d-sandbox-latest.md:152, 158, 168 |
| 恢复正确性 | Restore accuracy | C/R 后状态一致率：chat-only 8–13% → Crab 100%；checkpoint 流量 -87% | 01d-sandbox-latest.md:84, 96 |
| 环境保真度 | Simulator fidelity 衰减曲线 | 模拟状态 vs 真实状态的偏差随交互步数的增长（EnvSimBench：10 步后显著偏离）；状态转移准确性、奖励一致性、长期稳定性三轴 | 01d-sandbox-latest.md:185, 199-201 |
| 对抗鲁棒性 | LLM 生成有害任务的拒绝率差 | Agent 对 LLM 生成任务的拒绝率低于人类编写任务 → 对抗性任务生成攻击面 | 01d-sandbox-latest.md:126, 132 |

### 2.3 Memory 利用评估（→ 映射 harness 的 L 组件验证）

| 维度 | 指标 | 定义/公式 | 出处 |
|---|---|---|---|
| 记忆操作正确性 | ADD/UPDATE/DELETE/NOOP 决策准确率 | 每条新信息应采取的记忆操作 vs LLM 实际操作（Mem0 四类操作；Memory-R1 用 RL 学该决策） | 01d-memory-latest.md:53, 66, 155 |
| 长程检索质量 | F1 / BLEU-1 / LLM-as-a-Judge | LOCOMO 标准三指标；Memory-R1: F1 +48%, BLEU-1 +69%, Judge +37% | 01d-memory-latest.md:155, 170 |
| 时序推理 | Temporal QA accuracy | "当时是什么状态"类问题正确率；Zep 双时间戳（valid time + ingestion time），LongMemEval 63.8% vs Mem0 49.0% | 01d-memory-latest.md:88, 94, 102 |
| 多跳推理 | Multi-hop ROUGE-L | A-MEM 在 LoCoMo 多跳任务上比向量基线提升约 5.8× | 01d-memory-latest.md:122, 138 |
| 记忆效率 | P95 延迟 / token 消耗 | Mem0: P95 延迟 -91%，token -90%；"记忆过载临界点"（检索开销 > 记忆收益） | 01d-memory-latest.md:53, 69, 338 |
| 记忆一致性/篡改 | 冲突处理正确率 | 新旧信息冲突时是否正确更新（HiMem 再巩固 vs Zep 失效标记两种哲学的误判率） | 01d-memory-latest.md:195, 332 |
| 程序记忆复用 | 技能复用带来的探索节约 | MemP 三元组（目标, 轨迹, 反馈）；LEGOMem: 任务完成时间 -34%，错误恢复率 +28% | 01d-memory-latest.md:222, 238, 255 |

### 2.4 World model 辅助验证（→ 用模型预测校验结果，V 组件的"软验证器"）

| 维度 | 指标 | 定义/公式 | 出处 |
|---|---|---|---|
| 动作跟随精度 | Action-following accuracy | 给定动作序列后生成帧与真实帧的动作一致性；可借鉴 inverse dynamics：从相邻帧反推动作与输入动作比对 | 01e-world-models-latest.md:83, 91, 98 |
| 重访一致性 | Revisit consistency | 场景离开再返回时结构不漂移的度量（WorldPlay 核心指标；Genie 3 分钟级 vs Genie 2 10–20 秒） | 01e-world-models-latest.md:49, 251, 265 |
| 视觉保真度 | FVD 等 | 与真实 rollout 的分布距离；注意 FVD 与动作一致性的相关性弱，需双轨 | 01e-world-models-latest.md:91, 166, 232 |
| 下游决策价值 | Value-aware eval | 用世界模型 rollout 做 planning/policy，度量对真实环境决策的收益（Vid2World）；警惕"视觉好但动态不准"的模型误导 policy | 01e-world-models-latest.md:193, 200 |
| 模拟可信度 | Fidelity 衰减 + 可验证子集 | EnvSimBench：多步后 fidelity 指数衰减；缓解=混合模拟（LLM 管开放域、规则引擎管确定性部分）+ 定期真实校准 | 01e-world-models-latest.md:307；01d-sandbox-latest.md:185, 206 |
| Goodhart 风险 | 对抗性交互评测 | 模型可能对 benchmark 的"过场动画式一致性"过拟合，长尾交互（极端动作）仍崩坏 → 需要对抗性交互协议 | 01e-world-models-latest.md:311 |

---

## 3. 评测协议设计

从四个文件提炼的协议要素：

1. **任务配比协议（SafeArena 式）**：safe : harmful = 1:1（250:250），harmful 分类别（虚假信息/非法活动/骚扰/网络犯罪/偏见五类）；每类单独报告 completion rate，避免聚合掩盖弱点（misinformation 最高 28–30%）。（01d-sandbox-latest.md:118, 133）
2. **三态/四态判定而非二值**：SafeArena 的 Compliant/Partial/Refusal/Error；tool calling 的 V(r,q)→{pass,retry,abort}。Partial 需操作化定义（如完成 ≥80% 有害步骤）。（01d-sandbox-latest.md:124；01d-tool_calling-latest.md:23）
3. **多轨评估而非单指标**：Hunyuan-GameCraft 的"FVD + 动作一致性 + 人工评测"三轨；MineWorld 的"视觉保真度 × 动作跟随精度"双轨。（01e-world-models-latest.md:166, 83）
4. **过程指标 + 结果指标**：tool 时间占比、checkpoint 流量、token 消耗、P95 延迟等效率过程指标，与最终任务成功率并列报告。（01d-tool_calling-latest.md:126；01d-sandbox-latest.md:84；01d-memory-latest.md:53）
5. **有状态最终状态比对**：ToolSandbox 比对多步调用后的世界终态而非单步输出 → 直接适用于沙盒游戏的 world state diff。（01d-tool_calling-latest.md:216）
6. **seed / 重置与分支**：Crab 的 RL rollout 从中间 checkpoint 分支（省 40–64% token），评测应固定初始 seed 并支持确定性重放；非确定性 agent 需 fast-forward 合成响应保证一致。（01d-sandbox-latest.md:90, 92, 100）
7. **长程衰减曲线**：fidelity / 一致性随交互步数作图（EnvSimBench、WorldPlay 的分钟级/重访测试），而非只在固定 horizon 报一个点估计。（01d-sandbox-latest.md:201；01e-world-models-latest.md:265）
8. **训练效率作为协议元数据**：ReTool 的"400 步 vs 1000+ 步"、Memory-R1 的"152 QA 对收敛"——报告达到某性能所需样本/步数。（01d-tool_calling-latest.md:163；01d-memory-latest.md:169）
9. **基线对照 + 消融**：PASTE-Tool-Only vs PASTE-LLM-Only 消融；Zep 报 Mem0/MemGPT 同期数字。新维度需保留旧四维作对照组。（01d-tool_calling-latest.md:130；01d-memory-latest.md:88）

注：pass@k 与 generalization split 在所读四个文件中未被显式定义（仅 BFCL/ToolSandbox 等资源指针提及），如需公式需另查 BFCL-v4 / τ-bench 原文——标注为待补充。

---

## 4. 对 harness V 组件的落地建议

现有 verifier.py 四维：**structure / count / efficiency / inventory**（2D 沙盒 Minecraft-like，game-making agent）。建议如下：

### 4.1 新增维度（最高优先级，2D 沙盒可直接实现）

1. **工具必要性率（tool-necessity rate）—— 新增**
   - 度量：不必要的动作/工具调用数 ÷ 总调用数（When2Tool 思路的白盒版）。在 2D 沙盒中可程序化判定：如对已满足条件的方块重复 place、对不存在的资源 attempt mine、空手 attack 无目标格。
   - 与现有四维关系：**增强 efficiency**——efficiency 目前大概率只看步数/时间，over-tooling 率是其正交细化（"有效步占比 = 1 − over-tooling rate"）。
2. **安全/规则违例分级（SafeArena 四态移植）—— 新增第五维 "compliance"**
   - 在沙盒中定义违例任务集（如"挖掉基岩""生成非法物品 ID""越界放置"），报告 Compliant / Partial（完成部分非法步骤）/ Refusal / Error 四级分布，而非单一违规计数。类别化报告（仿 SafeArena 五类有害任务）。
3. **终态匹配精度（ToolSandbox state-match）—— 替换/强化 count**
   - count 目前应是"造了几个结构"的计数；升级为 **goal-state diff**：episode 结束 world state 与目标 world state 的逐格匹配率（precision/recall/F1 over cells），同时报结构级（连通区域级）匹配。这是有状态终态验证，比纯计数严格。
4. **动作跟随校验（MineWorld action-following 的逆向使用）—— 新增 "world-model consistency"**
   - 用转移模型 P（哪怕是规则化 ground-truth 引擎）预测执行动作后的状态，与实际状态比对；不一致计数 → 检测 agent 对环境的错误心智模型（如以为沙子会悬空）。这正是 EnvSimBench 警告的"幻觉环境"问题的内部度量。长期可训练一个轻量 world model 作为软验证器，用 **fidelity 衰减曲线**（预测误差随 rollout 步数）评估它本身。

### 4.2 增强现有维度

5. **efficiency → 双轨：过程效率 + 结果效率**
   - 过程：每 episode 的 action 数、无效动作率（4.1.1）、工具/动作时间占比（PASTE 式）；结果：达到 goal-state F1 ≥ τ 所需最小步数 vs 实际步数之比。
6. **inventory → 时序化 inventory tracking**
   - 借鉴 Zep 双时间戳：记录资源的"获得/消耗/失效"事件流，验证 agent 在 t 时刻的决策是否使用了 t 时刻实际持有的物品（时序一致性校验，抓"用了还没有的资源"这类幻觉动作）。
7. **structure → 结构 + 可逆性检查**
   - 增加 Partial-credit：结构完成度按连通组件比例给分（对应 SafeArena 的 Partial 思路），避免 0/1 判定的信息损失。

### 4.3 协议层建议

- **Episode 设计**：safe : adversarial = 1:1 配比；adversarial 类包含规则违例诱导任务；固定 seed、固定初始 world state，支持 checkpoint 重放（Crab 式）以复现失败点。
- **统计方法**：每个维度报均值 + 分类别分解（不按类别聚合）；至少 N episodes/seed，多 seed 报方差；长程任务画"成功率/一致性随步数衰减曲线"。
- **验证器自评**：V 组件本身也要被评估——用人工标注的小样本集计算 verifier 判定与人工判定的一致率（类似 LLM-as-a-Judge 与人工的相关性协议），防止 verifier 自身 Goodhart。

### 4.4 待补充（本 brief 未覆盖）

- pass@k / pass^k 的确切公式与 generalization split 设计（需查 BFCL-v4、τ-bench 原文）。
- When2Tool 的三类必要性（计算规模/知识边界/执行可靠性）在沙盒中的具体映射实例。

---

## 5. 引用指针

本地文件（C:\Git-repo-my\AIResearchVault\document\Routine\01-论文阅读与研究库\）：

- `01d-tool_calling-latest.md:23` — V(r,q)→{pass,retry,abort} 验证门控
- `01d-tool_calling-latest.md:47,61,63` — When2Tool over-tooling、AUROC 0.89–0.96、48% 调用减少
- `01d-tool_calling-latest.md:96` — Atomix 事务成功率/延迟/并发度评估
- `01d-tool_calling-latest.md:114,126,130` — PASTE 工具时间占比 16–37%/35–61%、-43.5%、消融
- `01d-tool_calling-latest.md:182,216,276` — ToolACE-R 在 BFCL/API-Bank 评估；综述三阶段框架；ToolSandbox 指针
- `01d-sandbox-latest.md:84,90,96,100` — Crab 恢复正确率 8%→100%、流量 -87%、fast-forward、RL 分支省 40–64%
- `01d-sandbox-latest.md:118,124,130,133,139` — SafeArena 250:250、四风险等级、类别化 completion rate、各模型合规率
- `01d-sandbox-latest.md:152,158,168` — ceLLMate ambient authority / blast radius
- `01d-sandbox-latest.md:185,199,201,206` — EnvSimBench fidelity 三轴、衰减曲线、混合模拟缓解
- `01d-memory-latest.md:53,66,69` — Mem0 四操作、LOCOMO +26%、P95 -91%
- `01d-memory-latest.md:88,94,102` — Zep 双时间戳、LongMemEval 63.8% vs 49.0%
- `01d-memory-latest.md:122,138` — A-MEM 多跳 ROUGE-L 5.8×
- `01d-memory-latest.md:155,169,170` — Memory-R1 F1 +48%、152 QA 对收敛
- `01d-memory-latest.md:195,332` — 再巩固 vs 失效标记、记忆篡改风险
- `01d-memory-latest.md:222,238,255` — MemP 三元组；LEGOMem -34% 时间 / +28% 错误恢复
- `01e-world-models-latest.md:83,91,98` — MineWorld 动作跟随精度 + inverse dynamics 思路
- `01e-world-models-latest.md:166,232` — GameCraft 三轨评估、FVD/动作一致性/人评
- `01e-world-models-latest.md:193,200` — Vid2World value-aware 下游决策评估
- `01e-world-models-latest.md:251,265,297,311` — WorldPlay revisit consistency；WBench/WorldMark；Goodhart 风险
- `01e-world-models-latest.md:307` — world-model 幻觉环境 vs EnvSimBench 警告

论文 URL（均转录自上述文件，未另行访问）：
- https://arxiv.org/abs/2605.09252 (When2Tool) · https://arxiv.org/abs/2602.14849 (Atomix) · https://arxiv.org/abs/2504.11536 (ReTool)
- https://proceedings.mlr.press/v267/tur25a.html (SafeArena) · https://arxiv.org/abs/2512.12594 (ceLLMate) · https://arxiv.org/abs/2604.28138 (Crab) · https://arxiv.org/abs/2605.07247 (EnvSimBench)
- https://arxiv.org/abs/2504.19413 (Mem0) · https://arxiv.org/abs/2501.13956 (Zep) · https://arxiv.org/abs/2502.12110 (A-MEM) · https://arxiv.org/abs/2508.19828 (Memory-R1)
- https://arxiv.org/abs/2402.17753 (LoCoMo) · https://arxiv.org/abs/2410.10813 (LongMemEval)
- https://arxiv.org/abs/2504.08388 (MineWorld) · https://arxiv.org/abs/2508.13009 (Matrix-Game 2.0) · https://arxiv.org/abs/2505.14357 (Vid2World) · https://arxiv.org/abs/2512.14614 (WorldPlay) · https://arxiv.org/abs/2605.25874 (WBench)
