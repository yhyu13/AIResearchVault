---
tags: [implementation, agent-harness, game-ai, 六组件架构]
aliases: [Agent-Harness-Game-AI-Tuesday]
created: 2026-07-01
source: [[Agent-Harness-Game-AI-2026-06-29]]
---

# 算法复现：Agent Harness 六组件架构 × Game AI

- **来源论文**：[[Agent-Harness-Game-AI-2026-06-29]]
- **核心论文**：Agent Harness for Large Language Model Agents: A Survey (Preprints, 2026-04-07)
- **参考实现**：自研（基于论文架构推导）
- **主题**：[[LLM Agent]] × [[Game AI]] × [[Reinforcement Learning]]
- **复现日期**：2026-07-01（周二）
- **测试状态**：✅ 全部通过（24/24）
- **v2 状态**：✅ Verification/Evaluation v2 扩展完成（2026-07-20，见"八、v2 扩展"）

---

## 一、算法推导

### 1.1 核心定义：Harness 六组件

来自 Survey 论文的形式化定义：

$$
H = (E, T, C, S, L, V)
$$

| 组件 | 符号 | 论文定义 | 游戏 AI 映射 |
|------|------|----------|-------------|
| **E** | Environment Execution | 环境执行器，管理状态转移 | 2D 沙盒网格，支持移动/放置/挖掘/合成 |
| **T** | Tool Calling | LLM Agent 的工具调用接口 | ReAct 循环：观察 → 推理 → 动作生成 |
| **C** | Context Management | 上下文管理与状态压缩 | 观察-动作-奖励轨迹 + 滑动窗口 |
| **S** | Safety Sandbox | 安全沙箱与动作校验 | 边界检查、库存校验、禁止块类型过滤 |
| **L** | Logging/Tracing | 日志追踪与可复现 | 结构化事件流、完整轨迹回溯 |
| **V** | Verification/Evaluation | 验证与多维度评估 | 结构正确性、块数量、效率、库存匹配 |

### 1.2 状态空间定义

**游戏状态**：$S = (G, p, I, t)$
- $G \in \mathbb{Z}^{H \times W}$: 网格（每个 cell 一个 BlockType）
- $p \in \mathbb{Z}^2$: 智能体位置 $(x, y)$
- $I \in \mathbb{N}^{|B|}$: 库存向量（每种方块的数量）
- $t \in \mathbb{N}$: 当前回合数

**动作空间**：$A = \{a_{\text{move}}, a_{\text{place}}, a_{\text{mine}}, a_{\text{craft}}, a_{\text{noop}}\}$

**状态转移函数**（确定性）：
$$
s' = \mathcal{P}(s, a) =
\begin{cases}
(p + \Delta_d, I, t+1) & a = \text{move}_d \\
(G[b \leftarrow \tau], I[\tau] - 1, t+1) & a = \text{place}(b, \tau) \\
(G[b \leftarrow \text{grass}], I[\text{type}(b)] + 1, t+1) & a = \text{mine}(b) \\
(s, I[\text{wood}] - 1, I[\text{plank}] + 4, t+1) & a = \text{craft}(\text{plank}) \\
(s, t+1) & a = \text{noop}
\end{cases}
$$

### 1.3 安全沙箱形式化

安全函数：$S: S \times A \to \{0, 1\} \times \text{Reason}$

$$
S(s, a) = \bigwedge_{r \in \mathcal{R}} r(s, a)
$$

其中规则集合 $\mathcal{R}$ 包括：
1. **边界规则**：$r_{\text{bound}}(s, a) = \mathbb{1}[p' \in [0, W) \times [0, H)]$
2. **库存规则**：$r_{\text{inv}}(s, a) = \mathbb{1}[I[\tau] > 0]$ for place actions
3. **禁止规则**：$r_{\text{forbid}}(s, a) = \mathbb{1}[\tau \notin \mathcal{F}]$ where $\mathcal{F}$ is forbidden set
4. **挖掘规则**：$r_{\text{mine}}(s, a) = \mathbb{1}[G[x,y] \notin \{\text{empty}, \text{grass}\}]$

### 1.4 验证评估多维度框架

论文提出的 Harness 可靠性评估，映射到游戏任务：

$$
V(s_T) = \sum_{k=1}^{K} w_k \cdot v_k(s_T)
$$

其中维度 $k \in \{\text{structure}, \text{count}, \text{efficiency}, \text{inventory}\}$：

- **结构正确性**：$v_{\text{struct}} = \frac{|\{b \in \text{target} : G[b] = \text{target}(b)\}|}{|\text{target}|}$
- **块数量**：$v_{\text{count}} = \mathbb{1}[n_{\text{min}} \leq n_{\text{blocks}} \leq n_{\text{max}}]$
- **效率**：$v_{\text{eff}} = 1 - \frac{t}{t_{\text{max}}}$
- **库存匹配**：$v_{\text{inv}} = \frac{1}{|R|} \sum_{(b, q) \in R} \min(1, \frac{I[b]}{q})$

通过条件：$V(s_T) \geq 0.75$ 且所有强制维度 $\geq 0.8$

---

## 二、代码实现

### 2.1 项目结构

```
agent_harness_game/
├── __init__.py          # 包导出
├── environment.py       # E: 2D 沙盒环境（~260行）
├── agent.py             # T: ReAct Agent + 模拟 LLM（~280行）
├── context.py           # C: 上下文管理（~170行）
├── safety.py            # S: 安全沙箱（~190行）
├── verifier.py          # V: 多维度验证（~230行）
├── harness.py           # H: 六组件组装器（~200行）
├── demo/
│   └── build_house.py   # 案例：建造 2×2 墙
├── tests/
│   └── test_harness.py  # 24 个单元测试 + 集成测试
├── 02-Agent-Harness-Game-AI-2026-07-01.md  # 复现主文档
└── plan.md                                 # 实现计划
```

### 2.2 关键技术决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 环境维度 | 2D 网格（10×10） | 保留核心概念，避免真实 Minecraft 依赖 |
| LLM 后端 | 模拟规则基 + 抽象接口 | 无需 API key，可替换为 GPT-4/Claude |
| 动作空间 | 8 个离散动作 | 覆盖移动、放置、挖掘、合成、空操作 |
| 状态表示 | 多模态：ASCII + 局部视图 + 结构化 | 模拟论文中的多模态挑战 |
| 安全策略 | 白名单 + 边界检查 | 基础版，可扩展为多维度沙箱 |
| 日志格式 | 结构化 JSON 事件流 | 支持完整回溯和可复现性 |

### 2.3 核心类图

```
AgentHarness (H)
  ├── SandboxEnvironment (E)
  │     └── GameState (grid, pos, inventory, turn)
  ├── ReActAgent (T)
  │     ├── LLMBackend (abstract)
  │     │     └── SimulatedLLM (heuristic/random)
  │     └── SafetySandbox (S) [双重校验]
  ├── ContextManager (C)
  │     └── ContextEntry[] (history)
  ├── SafetySandbox (S)
  │     └── SafetyPolicy (rules)
  ├── TaskVerifier (V)
  │     └── TaskSpec (target definition)
  └── Logger (L) [内置在 Harness 中]
```

### 2.4 执行流程（Pipeline）

```
初始化: E.reset() → S.setup() → C.set_goal() → T.set_agent() → V.set_task()

循环（直到 done）:
  1. E.get_observation(state) → 多模态观察
  2. C.build_agent_prompt(obs, history) → LLM 提示
  3. T.generate(prompt) → (thought, action)
  4. S.validate(state, action) → safe?
     ├─ Yes → 继续
     └─ No  → fallback to NOOP, log violation
  5. E.step(state, action) → (next_state, reward, done, info)
  6. C.record(state, obs, action, reward, info)
  7. V.evaluate(next_state) → passed? → done = True
  8. L.log(event)

结束: V.evaluate(final_state) → HarnessResult
```

---

## 三、与参考实现对比

由于 Survey 论文是综述性质，没有官方代码实现。我们基于论文定义推导了完整的可运行代码。

| 维度     | Survey 论文           | 本实现             | 差距分析                    |
| ------ | ------------------- | --------------- | ----------------------- |
| 架构覆盖   | 六组件完整定义             | ✅ 六组件完整实现       | 对齐                      |
| 环境复杂度  | 真实 3D 游戏（Minecraft） | ⚠️ 简化 2D 网格     | 保留核心状态转移概念，降低运行门槛       |
| LLM 集成 | 真实 GPT-4/Claude     | ✅ 模拟 + 抽象接口     | `LLMBackend` 可替换为真实 API |
| 安全性    | 多维度沙箱（论文提及）         | ✅ 白名单 + 边界 + 库存 | 基础版，可扩展规则引擎             |
| 可复现性   | 强调日志但未给出格式          | ✅ 结构化 JSON 轨迹   | 增强：支持完整回溯               |
| 评估     | 概念性讨论               | ✅ 四维量化评估        | 从定性到定量                  |
| 代码量    | 无                   | ~1,500 行 Python | 完整可运行                   |

---

## 四、调试记录

### 4.1 问题 1：放置方块库存不匹配

**现象**：`test_place_block` 失败，`info["success"]` 为 False
**原因**：测试用例中放置 `BlockType.WALL`，但库存中只有 `BlockType.PLANK`
**修复**：将测试中的动作改为放置 `BlockType.PLANK`，与库存一致
**代码**：`agent_harness_game/tests/test_harness.py:85-92`

### 4.2 问题 2：模拟 Agent 策略不够智能

**现象**：集成测试得分偏低（wall 0.200, craft 0.600）
**原因**：`SimulatedLLM` 的 heuristic 策略是简单的目标追踪，没有资源获取规划
**分析**：这是预期行为——模拟 LLM 仅用于验证架构流程，真实场景应接入 GPT-4
**后续优化方向**：
1. 添加预规划模块（Plan → Execute）
2. 实现库存感知的目标分解
3. 接入真实 LLM API 验证策略质量

### 4.3 问题 3：编码问题

**现象**：Windows 终端输出中 Unicode 符号（✅❌）显示为乱码
**原因**：Git Bash 默认使用 UTF-8，但 Windows console 可能使用 GBK
**修复**：使用 ASCII 替代符号（✅→PASS, ❌→FAIL）或在支持 UTF-8 的终端运行
**影响**：纯显示问题，不影响代码功能

---

## 五、测试验证

### 5.1 测试覆盖矩阵

| 组件 | 测试数 | 覆盖功能 | 结果 |
|------|--------|----------|------|
| E (Environment) | 7 | reset, movement, boundary, place, mine, craft, observation | ✅ 7/7 |
| S (Safety) | 6 | boundary, inventory, forbidden, mine_grass, safe, filter | ✅ 6/6 |
| C (Context) | 3 | record, summary, prompt_building | ✅ 3/3 |
| V (Verifier) | 4 | perfect, incomplete, craft, efficiency | ✅ 4/4 |
| T (Agent) | 2 | llm_generate, react_returns_action | ✅ 2/2 |
| H (Integration) | 3 | wall_build, craft, trace | ✅ 3/3 |
| **总计** | **24** | | **✅ 24/24** |

### 5.2 运行方式

```bash
# 方式 1：运行全部测试（通过 PythonRun）
python agent_harness_game/tests/test_harness.py

# 方式 2：运行 Demo
python agent_harness_game/demo/build_house.py

# 方式 3：作为模块导入
from agent_harness_game import AgentHarness, HarnessConfig, TaskSpec

config = HarnessConfig(max_turns=50)
harness = AgentHarness(config)
harness.set_task(TaskSpec.build_wall_2x2())
harness.set_agent(strategy="heuristic")
result = harness.run()
print(f"Score: {result.evaluation.overall_score}")
```

---

## 六、经验教训

### 6.1 设计层面

1. **抽象接口的重要性**：`LLMBackend` 抽象层使得我们可以在没有 API key 的情况下完成全部开发和测试。这是论文 "Tool Calling" 组件的精髓——接口标准化比具体实现更重要。

2. **安全沙箱的防御深度**：在 `agent.act()` 中做一次安全检查，在 `harness.run()` 中做二次检查。这符合论文强调的 "Harness 可靠性"——关键路径上需要冗余校验。

3. **多维度评估优于单一指标**：游戏 AI 的创造性任务（如"建造房屋"）很难用单一标准评判。四维评估（结构、数量、效率、库存）比二元 pass/fail 更有信息量。

### 6.2 工程层面

1. **简化环境是明智的选择**：使用 2D 网格而非真实 Minecraft，使得测试可以在 1 秒内完成，快速迭代。所有核心概念（状态转移、多模态观察、异构动作空间）都得以保留。

2. **日志是调试的第一手段**：`HarnessResult` 中的 `logs` 和 `trajectory` 字段在调试测试失败时至关重要。L 组件不是"锦上添花"，而是工程必需。

3. **类型注解和 dataclass 提升可读性**：`GameState`、`GameAction`、`SafetyPolicy` 等 dataclass 让代码自文档化，降低了从论文公式到代码的翻译成本。

### 6.3 待改进项

| 优先级 | 改进项 | 说明 |
|--------|--------|------|
| P1 | 接入真实 LLM | 实现 `OpenAIBackend(LLMBackend)` |
| P1 | 预规划模块 | 将任务分解为子目标序列（Plan → Execute） |
| P2 | 更丰富的合成配方 | 当前仅支持 wood → plank |
| P2 | 安全策略扩展 | 支持动态规则加载、规则冲突检测 |
| P3 | 3D 环境扩展 | 使用 MineDojo 或类似框架 |
| P3 | 并行 Agent 评估 | 同时评估多个 Agent 策略 |

---

## 七、与周一论文的关联

```
周一论文预读 → 周二算法复现

├── 六组件架构 H=(E,T,C,S,L,V)
│   └── 从概念定义 → 完整 Python 实现
├── 游戏环境映射
│   └── 从 Minecraft 讨论 → 2D 可运行沙盒
├── ReAct 推理循环
│   └── 从论文引用 → 可执行的 Thought-Action-Observation
├── 多维度评估
│   └── 从 "评估不可靠性" 讨论 → 四维量化框架
└── 可复现性
    └── 从 "日志追踪" 概念 → 结构化 JSON 轨迹 + 回溯
```

**人类执行建议**：
1. 阅读 `agent_harness_game/harness.py` 理解组装流程
2. 修改 `agent_harness_game/agent.py` 中的 `SimulatedLLM` 策略，尝试不同的 heuristics
3. 在 `agent_harness_game/demo/build_house.py` 中接入真实 OpenAI API（替换 `SimulatedLLM`）
4. 在 Monday 论文笔记中链接到本文件：`[[02-Agent-Harness-Game-AI-2026-07-01]]`

---

## 八、v2 扩展：Verification/Evaluation 深化（2026-07-20）

> 依据：项目内 `research/R1-benchmarks.md`、`R2-harness-verification.md`、`R3-execution-interaction.md`、`R4-supporting-evals.md` 四份调研 brief 与 `plan-v2-verification-eval.md`；综合笔记见 [[01e-agent-verification-eval-latest]]（约 58 条引用）。

### 8.1 扩展动机

v1 的 V 组件是"单任务、单轨迹、静态阈值的终局检查器"（四维加权 `V(s_T) = Σ w_k·v_k`，阈值 0.75）。R1–R4 调研得出的一致结论：V 组件必须升级为**四维指标体系 + 统计化评测协议 + harness 自评（net benefit）**的组合——粗粒度 binary 指标在 TextQuests / VisEscape 上区分度为 0，需要细粒度进度与过程指标（GameWorld 案例：agent 达 ~90% progress 但 SR=0）。

### 8.2 verifier.py 新增维度总表

| 新维度 | 公式 / 定义 | 文献来源 |
|--------|-------------|----------|
| structure P/R/F1（goal-state diff） | 终态 world state 与目标 state 逐格比对：`precision = correct/(correct+extra)`、`recall = correct/(correct+missing)`、F1；precision 防"铺满全图"刷分 | ToolSandbox 有状态终态比对思想（R4）；R3 建议 recall+precision 配对 |
| mean_harm | 危险/破坏性操作计数（误拆目标方块、破坏已有正确结构、无效合成） | TextQuests（arXiv:2507.23701）（R1） |
| trajectory_progress（normalized progress） | `progress = clip_[0,1]((q_max − b)/(τ − b))`，q_max 取运行中历史最高值，防止终局恰好被破坏而低估能力 | GameWorld（arXiv:2604.07429）（R3） |
| action_validity | 无效动作数 / 总动作数（非法位置、材料不足的 craft、解析失败指令） | GameWorld action-validity diagnostics（R3） |
| meaningful_step_ratio | 真正推进游戏状态的步数占比，区分"慢但在推进"与"快但在空转" | GVGAI-LLM（arXiv:2508.08501）（R1） |
| redundancy（冗余动作率） | 无净效果动作对占比（放置后立即挖除等），等价于 over-tooling rate | Harness Engineering Survey §3.7（R2）/ When2Tool（R4） |
| compliance 四态 | 违例任务集报告 Compliant / Partial / Refusal / Error 四级分布，分类别报告而非聚合 | SafeArena（ICML 2025）（R4） |
| JudgeBackend / NoOpJudge | LLM-as-judge 抽象接口；NoOpJudge 为默认空实现——可状态化的判断一律走断言，judge 仅兜底无 ground-truth 维度 | FlashAdventure CUA-as-a-Judge（R1/R3）；ODYSSEY critic 降级（R3） |

v1 四维处置：structure_correctness 增强（recall→P/R/F1 配对、q_max 历史取值）；block_count 降为诊断 details；efficiency 由 normalized progress 增强；inventory_match 保留。

### 8.3 evaluation.py API 摘要（新建，~650 行）

| API | 说明 |
|-----|------|
| `TaskEntry` | 任务条目：TaskSpec + category（build/craft/adversarial）+ split（dev/test） |
| `TaskSuite` | 任务集合（默认 10 任务），`by_category()` / `by_split()` 分组，`default_suite(seed=42)` 工厂 |
| `generate_variants(spec, n, seed)` | 从 held-out 分布程序化生成任务变体（平移目标位置、换方块类型），dev/test 防过拟合核心 |
| `BenchmarkRunner(n_seeds, m_episodes)` | N seeds × M episodes 批量评测，`run_suite(suite)` → 报告 dict |
| `EpisodeRecord` | 单 episode 记录（seed、episode、passed、各维度得分），`to_dict()` 序列化 |
| `pass_at_k(n, c, k)` | 无偏估计器 `pass@k = 1 − C(n−c,k)/C(n,k)`，k=1 即 Resolve@1 |
| `wilson_ci(successes, n, z=1.96)` | Wilson 95% CI，小 n 下比裸比例更稳 |
| `render_markdown(report)` / `save_json(report, path)` | 分类别分解报告输出（Markdown / JSON） |
| `run_ablation(suite, configs, ...)` / `render_ablation_markdown(...)` | 多 harness 配置受控对比（ablation-as-protocol） |

### 8.4 协议设计

1. **dev/test split + 变体生成**：TaskSpec 增加 split 字段；dev 坐标固定，test 由 `generate_variants` 从 held-out 分布采样（seed 固定可复现）——对应 R1 三条防污染路线中的"造（程序化生成）"与 R2 的 hold-out 验证。
2. **多 seed × 多 episode**：同一任务在 N 个随机初始布局上跑 M 次，报告 mean ± std 与 pass rate，而非单次 rollout 布尔值（每任务 n ≥ 10 episode 的 R2/R3 建议的可调实现）。
3. **pass@k**：报 pass@1 为主、pass@k（k=3,5）为辅（SWE-bench Resolve@1 惯例，R2）。
4. **Wilson CI**：成功率一律报 Wilson 95% CI；两组对比可用配对 McNemar 检验（pass/fail 二值）。
5. **分类别分解报告**：按 build / craft / adversarial 三类分别聚合，避免单一总分掩盖弱点（SafeArena 分类别报告、RLVE 难度分桶思想）。
6. **run_ablation（三臂消融）**：native（V 不参与反馈）vs full-V vs 去单维，报 Δscore / Δcost / net benefit——harness 自评核心（Harness Engineering Survey §6 两层评估逻辑：native capability-gap diagnosis + compensation effectiveness）。

### 8.5 文件变更清单

| 文件 | 变更 |
|------|------|
| `verifier.py` | 扩展（~230 行 → ~524 行）：structure P/R/F1、mean_harm、trajectory_progress、process 三维（action_validity / meaningful_step_ratio / redundancy）、compliance 四态、JudgeBackend/NoOpJudge |
| `evaluation.py` | 新建（~648 行）：TaskSuite / generate_variants / BenchmarkRunner / EpisodeRecord / pass_at_k / wilson_ci / render_markdown / save_json / run_ablation |
| `demo/craft_item.py` | 新建：合成任务演示 |
| `demo/run_benchmark.py` | 新建：BenchmarkRunner 端到端演示 |
| `research/R1-benchmarks.md` ~ `R4-supporting-evals.md` | 新建：4 份调研 brief（基准评测 / Harness 验证 / 执行与交互评估 / 支撑组件评估） |
| `plan-v2-verification-eval.md` | 新建：v2 实现计划 |
| `01e-agent-verification-eval-latest.md` | 新建（研究库）：综合调研笔记，约 58 条引用 |

---

*AI 执行时间：约 30 分钟（代码生成 + 测试）*
*人类验证时间：约 30 分钟（阅读代码 + 运行测试）*
*日期：2026-07-01 周二*
*状态：✅ 复现完成，24/24 测试通过*
*v2 更新：2026-07-20 · Verification/Evaluation 深化完成（见第八节）*
