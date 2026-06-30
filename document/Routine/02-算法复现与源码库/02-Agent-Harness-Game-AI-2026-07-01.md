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
└── harness.py           # H: 六组件组装器（~200行）

demo/
└── build_house.py       # 案例：建造 2×2 墙

tests/
└── test_harness.py      # 24 个单元测试 + 集成测试
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

| 维度 | Survey 论文 | 本实现 | 差距分析 |
|------|------------|--------|----------|
| 架构覆盖 | 六组件完整定义 | ✅ 六组件完整实现 | 对齐 |
| 环境复杂度 | 真实 3D 游戏（Minecraft） | ⚠️ 简化 2D 网格 | 保留核心状态转移概念，降低运行门槛 |
| LLM 集成 | 真实 GPT-4/Claude | ✅ 模拟 + 抽象接口 | `LLMBackend` 可替换为真实 API |
| 安全性 | 多维度沙箱（论文提及） | ✅ 白名单 + 边界 + 库存 | 基础版，可扩展规则引擎 |
| 可复现性 | 强调日志但未给出格式 | ✅ 结构化 JSON 轨迹 | 增强：支持完整回溯 |
| 评估 | 概念性讨论 | ✅ 四维量化评估 | 从定性到定量 |
| 代码量 | 无 | ~1,500 行 Python | 完整可运行 |

---

## 四、调试记录

### 4.1 问题 1：放置方块库存不匹配

**现象**：`test_place_block` 失败，`info["success"]` 为 False
**原因**：测试用例中放置 `BlockType.WALL`，但库存中只有 `BlockType.PLANK`
**修复**：将测试中的动作改为放置 `BlockType.PLANK`，与库存一致
**代码**：`tests/test_harness.py:85-92`

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
python tests/test_harness.py

# 方式 2：运行 Demo
python demo/build_house.py

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
3. 在 `demo/build_house.py` 中接入真实 OpenAI API（替换 `SimulatedLLM`）
4. 在 Monday 论文笔记中链接到本文件：`[[02-Agent-Harness-Game-AI-2026-07-01]]`

---

*AI 执行时间：约 30 分钟（代码生成 + 测试）*
*人类验证时间：约 30 分钟（阅读代码 + 运行测试）*
*日期：2026-07-01 周二*
*状态：✅ 复现完成，24/24 测试通过*
