# Tuesday Plan · Agent Harness × Game AI — 算法复现与实现

> **来源**：[[Agent-Harness-Game-AI-2026-06-29]]（周一论文预读）
> **目标**：将 Agent Harness 六组件架构 $H=(E,T,C,S,L,V)$ 从理论推导到可运行代码
> **场景**：Minecraft-like 沙盒游戏环境

---

## 一、理论推导阶段

### 1.1 数学建模：Harness 六组件

对 Survey 论文定义的六组件做形式化推导，映射到 Game AI 场景：

| 组件 | 符号 | 数学对象 | 游戏映射 |
|------|------|----------|----------|
| Environment Execution | $E$ | $(\mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R})$ | 沙盒状态、动作、转移、奖励 |
| Tool Calling | $T$ | $T: \text{Prompt} \to \text{Action}$ | LLM Agent 的游戏命令接口 |
| Context Management | $C$ | $\mathcal{H}_t = \{(o,a,r)_i\}_{i=1}^t$ | 观察-动作-奖励轨迹 + 库存/目标状态 |
| Safety Sandbox | $S$ | $S(a) \in \{0,1\}$ | 动作合法性校验、边界约束 |
| Logging/Tracing | $L$ | $\mathcal{D} = \{(t, s, a, s', r)\}$ | 完整交互日志，支持可复现 |
| Verification/Evaluation | $V$ | $V(\mathcal{H}_T) \to \mathbb{R}^k$ | 多维度任务完成度评估 |

### 1.2 核心算法推导

1. **环境执行器**（E）：简化版 Gymnasium 接口
2. **工具调用**（T）：ReAct 循环 + 代码生成动作空间
3. **上下文管理**（C）：滑动窗口 + 状态摘要
4. **安全沙箱**（S）：白名单过滤 + 边界检查
5. **日志追踪**（L）：结构化事件流 + 回溯
6. **验证评估**（V）：目标匹配 + 结构完整性检查

---

## 二、代码实现阶段

### 2.1 目录结构

```
02-算法复现与源码库/
├── 00-README.md
├── 02-Agent-Harness-Game-AI-2026-07-01.md      # 复现主文档
├── agent_harness_game/
│   ├── __init__.py
│   ├── environment.py     # E: 简化版沙盒环境
│   ├── agent.py           # T: LLM Agent 接口 + ReAct 循环
│   ├── context.py         # C: 上下文管理
│   ├── safety.py          # S: 安全沙箱
│   ├── logging.py         # L: 日志追踪
│   ├── verifier.py        # V: 验证评估
│   └── harness.py         # H: 六组件组装器
├── demo/
│   ├── build_house.py     # 案例1: 建造房屋任务
│   └── craft_item.py      # 案例2: 合成物品任务
└── tests/
    └── test_harness.py    # 单元测试
```

### 2.2 实现优先级

1. **P0**: `environment.py` + `harness.py`（核心骨架）
2. **P1**: `safety.py` + `verifier.py`（安全与验证）
3. **P2**: `agent.py` + `context.py`（LLM Agent 接口）
4. **P3**: `demo/` 案例 + `tests/` 测试

### 2.3 关键技术决策

- **不依赖真实 Minecraft 环境**：使用简化 2D 网格模拟，确保代码可运行
- **不依赖真实 LLM API**：使用规则基模拟 Agent，降低运行门槛
- **但保留 LLM 接口抽象**：`LLMBackend` 接口可替换为真实 API
- **状态表示**：ASCII 网格 + 结构化属性（坐标、库存、方块类型）

---

## 三、验证与对比阶段

### 3.1 测试矩阵

| 任务 | 动作数 | 验证维度 | 预期通过 |
|------|--------|----------|----------|
| 放置 3 个方块 | 3 | 结构匹配 | ✅ |
| 建造 2×2 墙 | 5 | 结构 + 位置 | ✅ |
| 非法动作越界 | 1 | 安全拦截 | ✅ |
| 非法动作破坏 | 1 | 安全拦截 | ✅ |
| 长程任务（10+ 步） | 15 | 日志回溯 + 目标完成 | ✅ |

### 3.2 与论文对比

| 维度 | Survey 论文 | 本实现 | 差距分析 |
|------|------------|--------|----------|
| 架构覆盖 | 六组件完整 | 六组件完整 | ✅ 对齐 |
| 环境复杂度 | 真实 3D 游戏 | 简化 2D 网格 | ⚠️ 简化但保留核心概念 |
| LLM 集成 | 真实 GPT-4/Claude | 模拟 + 抽象接口 | ⚠️ 可替换 |
| 安全性 | 多维度沙箱 | 白名单 + 边界检查 | ⚠️ 基础版，可扩展 |
| 可复现性 | 有日志但未强调 | 完整日志 + 回溯 | ✅ 增强 |

---

## 四、执行 Checklist

- [ ] 创建 `plan.md`（本文件）
- [ ] 推导环境状态转移方程
- [ ] 实现 `environment.py`
- [ ] 实现 `safety.py`
- [ ] 实现 `verifier.py`
- [ ] 实现 `context.py`
- [ ] 实现 `agent.py`（ReAct 骨架）
- [ ] 实现 `harness.py`（组装器）
- [ ] 实现 `demo/build_house.py`
- [ ] 实现 `tests/test_harness.py`
- [ ] 运行全部测试并记录结果
- [ ] 撰写复现文档 `02-Agent-Harness-Game-AI-2026-07-01.md`
- [ ] 更新 00-README 复现索引

---

*计划创建时间：2026-07-01（周二）*
*预计执行时间：2-3 小时*
*最终交付物：可运行代码 + 完整复现文档*
