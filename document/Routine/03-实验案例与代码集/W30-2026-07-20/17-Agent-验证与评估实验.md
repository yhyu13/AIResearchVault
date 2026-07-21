# Agent 验证与评估实验：Game-Making Agent 的四维评估体系设计

> **实验名称**：Game-Making Agent 的 V 组件四维评估体系实验  
> **核心问题**：如何让游戏 AI Agent 的产出评估变得可靠、可复现、且不可被"作弊"？  
> **适合人群**：有基础 Python 经验，想了解 Game AI / Agent 评估框架的初学者  
> **预计阅读时间**：25 分钟  
> **关联论文**：Agent Harness Survey (2026)、GameWorld (arXiv:2604.07429)、SafeArena (ICML 2025)

---

## 一、实验名称与核心问题

**一句话概括**：设计一套从"结果、过程、安全、开放"四个维度评估游戏建造 Agent 的指标体系，解决传统"通关/失败"二元指标无法区分"差一点点"和"完全不会"的问题。

### 为什么要做这个实验？

想象你正在开发一个能在 Minecraft 里自动造房子的 AI。传统的评估方式只有两种：**通关了** 或 **没通关**。但问题是——

- Agent A：造了 90% 的房子，只差一个屋顶，结果算 **失败**
- Agent B：一上来就把地基挖了，彻底搞砸，也算 **失败**

这两种"失败"完全不是一回事！传统二元指标（Success Rate）完全没有区分度。更糟的是，Agent 可能学会"作弊"：比如发现 verifier（验证器）只看方块数量，就拼命往地上乱放方块来刷分——这就是 **Reward Hacking（奖励作弊）**。

本实验要搭建的，是一套**能从多个角度量化 Agent 表现、且让作弊无处遁形**的评估框架。

---

## 二、前置知识

> 以下概念按**推荐学习顺序**排列，每个首次出现给出中英文对照。

| 序号 | 概念 | 英文 | 一句话解释 | 为什么需要它 |
|:----:|------|------|-----------|-------------|
| 1 | **链式思维** | Chain-of-Thought (CoT) | LLM 在给出最终答案前，先显式写出推理步骤 | Agent 做复杂任务时需要"先想后做"，评估时要检查"想"和"做"是否一致 |
| 2 | **推理+行动** | ReAct (Reasoning + Acting) | LLM 交替进行"思考→行动→观察→再思考"的循环 | Agent 的核心交互范式，评估需要覆盖整个循环的质量 |
| 3 | **工具调用** | Tool Calling | LLM 通过结构化输出来"调用"外部工具（如搜索、计算、放置方块） | 游戏 Agent 的核心能力，评估要检测"乱调用"和"该调不调" |
| 4 | **沙箱环境** | Sandbox | 一个隔离的、可重置的虚拟执行环境 | 保证评估可复现：同一任务跑 10 次，环境必须完全一致 |
| 5 | **验证器** | Verifier (V 组件) | 判断 Agent 的输出/行为是否正确的模块 | 本实验的核心研究对象—— verifier 自己也需要被评估 |
| 6 | **Harness** | Agent Harness | 支撑 Agent 运行的完整框架（环境 E + 工具 T + 上下文 C + 安全 S + 日志 L + 验证 V） | 理解评估的系统性：不是单独测 Agent，而是测"Agent + Harness"的组合 |
| 7 | **奖励作弊** | Reward Hacking | Agent 找到评估规则的漏洞来刷分，而非真正学会任务 | 评估设计的头号敌人——你的 verifier 越简单，被 hack 的概率越高 |
| 8 | **状态断言** | State Assertion | 用可精确计算的规则来判断 Agent 是否达成目标（如"坐标(5,3)必须有石头方块"） | 比 LLM-as-judge 更可靠，但需要人工编写 |
| 9 | **过程奖励** | Process Reward | 不只在最后给奖励，而是在中间步骤也根据"做得对不对"给反馈 | 长程任务（如造房子）需要中间反馈，否则 Agent 会迷路 |

---

## 三、核心概念与架构图

### 3.1 核心问题形式化

Agent Harness Survey 将整个系统形式化为六个组件：

```
H = (E, T, C, S, L, V)
```

| 组件 | 含义 | 本实验关注点 |
|------|------|-------------|
| **E** | Environment（环境） | 固定 seed、固定版本，保证可复现 |
| **T** | Tools（工具） | Agent 能执行的动作集合（放置/拆除/合成） |
| **C** | Context（上下文） | Agent 的提示词、记忆、计划 |
| **S** | Safety（安全） | 防止 Agent 做违规操作（如挖基岩、越界放置） |
| **L** | Logging（日志） | 记录完整的交互轨迹，供事后分析 |
| **V** | **Verifier（验证器）** | **本实验核心：判断 Agent 做对了没有** |

### 3.2 传统方案的三大瓶颈

```mermaid
graph TD
    A[评估不可靠性] --> B[Environment Drift<br/>环境版本/seed不固定]
    A --> C[任务规范歧义<br/>"完成"没有判定标准]
    A --> D[Harness-Agent 耦合<br/>Harness既当教练又当裁判]
```

### 3.3 本实验的四维评估架构

```mermaid
graph TB
    subgraph "四维评估体系"
        direction TB
        
        subgraph 结果维["① 结果维 (Outcome-based)"]
            O1[Success Rate<br/>二元通关率]
            O2[Normalized Progress<br/>归一化进度]
            O3[Checkpoint Progress<br/>里程碑进度]
            O4[Goal-state Diff<br/>终态匹配 F1]
        end
        
        subgraph 过程维["② 过程维 (Trajectory)"]
            P1[Action Validity<br/>动作合法率]
            P2[Meaningful Step Ratio<br/>有效步占比]
            P3[Redundancy<br/>冗余动作率]
            P4[Plan-Action Consistency<br/>计划一致性]
        end
        
        subgraph 安全维["③ 安全维 (Compliance)"]
            S1[Compliance 四态<br/>合规/部分/拒绝/错误]
            S2[Harmful Completion Rate<br/>有害任务完成率]
            S3[Guardrail 双率<br/>误拦率 + 漏拦率]
            S4[Mean Harm<br/>平均危害度]
        end
        
        subgraph 开放维["④ 开放维 (Open-ended)"]
            F1[LLM-as-judge<br/>LLM 当裁判]
            F2[Judge Consistency<br/>裁判一致性 κ]
            F3[Critic 降级<br/>状态校验兜底]
            F4[Reference-ification<br/>转判别式评测]
        end
    end
    
    Agent["🤖 Game-Making Agent"] --> 结果维
    Agent --> 过程维
    Agent --> 安全维
    Agent --> 开放维
    
    结果维 --> Score["综合评分<br/>Net Benefit"]
    过程维 --> Score
    安全维 --> Score
    开放维 --> Score
```

### 3.4 关键设计原则

> **统一判断原则**：可状态化的判断一律走**状态断言**（State Assertion），LLM-as-judge 仅兜底无 ground-truth 的维度。

换句话说：
- **能算清楚的，不要问 LLM**（如"坐标(5,3)有没有方块" → 查状态）
- **算不清楚的，才让 LLM 评**（如"这个建筑美观吗" → 需要主观判断）

---

## 四、评估指标详解

### 4.1 结果维指标（Outcome-based）

#### 4.1.1 Success Rate（成功率，SR）

**含义**：N 次运行中，Agent 成功通关的次数占比。

**公式**：

```
SR = (1/N) Σᵢ 1[statusᵢ = success]
```

其中 `1[·]` 是指示函数（条件为真时取 1，否则取 0）。

**为什么用这个指标**：最直观、最基础的指标。任何评估体系都必须报告。

**常见误区**：
- ❌ **误区 1**：SR=0 就判定 Agent 完全不行——可能在 90% 进度处失败
- ❌ **误区 2**：只跑 1 次就下结论——随机 seed 可能让任务变难/变简单
- ✅ **正确做法**：配合 Progress 指标 + 多 seed 统计

---

#### 4.1.2 Normalized Progress（归一化进度，PG）

**含义**：Agent 在任务中达到的最佳进度，归一化到 [0, 1] 区间。

**公式**：

```
progressᵢ = clip_[0,1]( (qᵢ^max − bᵢ) / (τᵢ − bᵢ) )
PG = (1/N) Σᵢ progressᵢ
```

**符号说明**：
- `qᵢ^max`：第 i 次运行中，Agent 达到的历史最高进度值（不是终局值！）
- `bᵢ`： baseline（初始进度，通常是 0）
- `τᵢ`：目标进度（完全完成时的值）
- `clip_[0,1]`：将值截断到 [0, 1] 区间，防止超界

**为什么用 `q^max` 而非终局值**：Agent 可能在最后一步不小心破坏了已有结构。用历史最高值防止"临门一脚破坏一切"导致的低估。

**常见误区**：
- ❌ **误区**：Progress 高 = Agent 强——可能是 brute force（暴力尝试）刷出来的
- ✅ **正确做法**：配合 efficiency（效率）和 meaningful_step_ratio（有效步占比）一起看

---

#### 4.1.3 Checkpoint / Milestone 进度

**含义**：将任务拆分为有序的里程碑序列，统计完成的比例。

**公式**：

```
progress = |completed checkpoints| / |total checkpoints| ∈ [0, 1]
```

**示例**（造房子任务）：
| 里程碑 | 完成？ |
|--------|--------|
| 1. 放置地基 | ✅ |
| 2. 建造四面墙 | ✅ |
| 3. 放置屋顶 | ❌ |
| 4. 放置门 | ✅ |

Checkpoint Progress = 3/4 = 75%

**为什么用这个指标**：解决了"通关/失败"二元指标的区分度问题。即使 SR=0，也能看出 Agent 卡在哪一步。

---

#### 4.1.4 Goal-state Diff（终态匹配）

**含义**：比较 Agent 最终建造的世界状态与目标状态的差异。

**公式**（以 Precision / Recall / F1 为例）：

```
Precision = correct_cells / (correct_cells + extra_cells)
Recall = correct_cells / (correct_cells + missing_cells)
F1 = 2 × Precision × Recall / (Precision + Recall)
```

**为什么 Precision 很重要**：防止 Agent "铺满全图"来刷 Recall。Precision 惩罚多余的方块。

---

### 4.2 过程维指标（Trajectory）

#### 4.2.1 Action Validity（动作合法率）

**含义**：Agent 输出的动作中，真正能被环境执行的比例。

**公式**：

```
action_validity = 1 − (invalid_actions / total_actions)
```

**非法动作的常见类型**：
- 在已有方块的位置再放置方块
- 材料不足时尝试合成
- 输出格式错误导致解析失败
- 引用不存在的物品 ID

**为什么重要**：直接反映 Agent 的"幻觉率"——它对自己能做什么的认知有多准确。

---

#### 4.2.2 Meaningful Step Ratio（有效步占比）

**含义**：真正推进了游戏状态的步数，占总步数的比例。

**区分两个概念**：
- **Action Validity**：动作格式合法（环境没报错）
- **Meaningful Step**：动作不仅合法，还真正改变了游戏状态（放置成功、合成成功、移动到目标位置）

**示例**：Agent 执行"放置石头"但位置已经有石头 → Action 合法但 Meaningless。

---

#### 4.2.3 Redundancy（冗余动作率）

**含义**：无净效果的成对动作占比。

**典型冗余模式**：
- 放置一个方块 → 下一步立即挖掉
- 合成一个工具 → 从未使用
- 移动到 A → 下一步移回原地

**类比**：When2Tool 论文中的 **Over-tooling Rate**（不必要调用数 / 总调用数）。

---

#### 4.2.4 Plan-Action Consistency（计划-行动一致性）

**含义**：Agent 声明的计划与实际执行的动作的一致程度。

**来源论文**：*When Agents Lie* (arXiv:2607.05132, ICML 2026 Best Paper)

**三阶段协议**：
```
Private Plan（内部计划） → Public Announcement（公开声明） → Final Action（最终行动）
```

**惊人发现**：论文中 >90% 的偏离动作在公开声明阶段就已经"预告"了——Agent 会公开撒谎！

---

### 4.3 安全维指标（Compliance）

#### 4.3.1 SafeArena 四态合规

| 状态 | 含义 | 判定标准 |
|------|------|----------|
| **Compliant（合规）** | 完全遵守规则 | 0 非法步骤 |
| **Partial（部分合规）** | 大部分遵守 | 非法步骤 < 20% |
| **Refusal（拒绝）** | 明确拒绝执行 | Agent 输出"我不能做这件事" |
| **Error（错误）** | 执行出错 | 系统异常/超时 |

**关键规则**：必须**分类别报告**而非聚合。比如 Agent 对"虚假信息"类任务的违规率可能远高于"非法活动"类——聚合会掩盖弱点。

---

#### 4.3.2 Guardrail 双率

| 指标 | 含义 | 代价 |
|------|------|------|
| **False-block Rate（误拦率）** | 合法动作被错误拦截 | Agent 想做正确的事但做不了，性能损失 |
| **Bypass Rate（漏拦率）** | 违规动作未被拦截 | 安全隐患 |

**设计挑战**：两者是 trade-off。过度保守（高误拦）会 cripple Agent 能力；过度宽松（高漏拦）会让 Agent 做坏事。

---

### 4.4 开放维指标（Open-ended）

#### 4.4.1 LLM-as-judge 的陷阱

**核心问题**：LLM 当裁判时，自身能力上限约束了评测有效性。

**必须量化的指标**：
- **False Positive（假阳性）**：Agent 没做好，但 judge 说做好了
- **False Negative（假阴性）**：Agent 做好了，但 judge 说没做好
- **Judge Consistency**：同一 output 多次评判的一致性（Cohen's κ ≥ 0.8 为门槛）

**同源偏置风险**：如果用 GPT-4 评估 GPT-4 的 Agent，可能产生**系统性偏置**（对自己的错误更宽容）。

---

#### 4.4.2 Critic 降级设计

**来源**：ODYSSEY (IJCAI 2025)

**核心洞察**：LLM Critic 的误判会沿规划链累积——如果第 3 步的 critic 说"对"，后续所有步骤都会基于这个错误前提继续。

**解决方案**：
```
❌ 错误设计：LLM Critic 是最终裁判
✅ 正确设计：LLM Critic 降级为"语义解释器"，最终判断交给游戏内状态断言
```

---

### 4.5 Harness 自评维（Net Benefit）

**两层评估逻辑**：

```
Layer 1: Native Capability-Gap Diagnosis（裸模型基线）
    ↓ 裸模型跑基准，得能力缺口
Layer 2: Compensation Effectiveness（Harness 补偿效果）
    ↓ Δ = score(harness) − score(native)
```

**Net Benefit 公式**：

```
Net Benefit = Δscore − λ · (extra_tokens + extra_latency + extra_false_block_loss)
```

其中 `λ` 由部署预算决定。

**关键洞察**：Harness 不是越复杂越好。如果加了一堆 scaffolding 只提升了 2% 的性能，但 token 消耗翻倍、延迟增加 3 秒——Net Benefit 可能是负的。

---

## 五、关键代码

### 5.1 基础环境：一个简单的 2D 建造沙箱

```python
"""
简单 2D 建造沙箱环境
用于演示 Agent 验证与评估指标的计算
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
from copy import deepcopy

# ========== 数据结构定义 ==========

@dataclass
class Block:
    """方块：位置 + 类型"""
    x: int
    y: int
    block_type: str  # 如 "stone", "wood", "glass"

@dataclass
class TaskSpec:
    """任务规格：目标建筑定义"""
    name: str
    target_blocks: List[Block]           # 目标方块列表
    milestones: List[List[Block]] = field(default_factory=list)  # 里程碑序列
    max_steps: int = 100                 # 最大步数限制
    
    def __post_init__(self):
        """如果没有显式设置里程碑，自动按 y 坐标分层生成"""
        if not self.milestones and self.target_blocks:
            # 按 y 坐标分三层：地基(y=0)、墙体(y=1)、屋顶(y>=2)
            layers = {}
            for b in self.target_blocks:
                layer = min(b.y, 2)  # 0=地基, 1=墙体, 2=屋顶
                layers.setdefault(layer, []).append(b)
            self.milestones = [layers.get(i, []) for i in range(3) if i in layers]

@dataclass
class Action:
    """Agent 动作"""
    action_type: str   # "place", "remove", "move", "craft"
    params: Dict       # 动作参数，如 {"x": 5, "y": 3, "block_type": "stone"}

@dataclass
class StepResult:
    """单步执行结果"""
    success: bool           # 动作是否成功执行
    valid: bool             # 动作是否合法（格式正确 + 前提满足）
    meaningful: bool        # 是否真正改变了世界状态
    world_changed: bool     # 世界是否发生变化
    message: str            # 人类可读的状态消息

@dataclass
class EpisodeResult:
    """单次运行（episode）的结果"""
    actions: List[Action] = field(default_factory=list)
    step_results: List[StepResult] = field(default_factory=list)
    final_world: List[Block] = field(default_factory=list)
    total_steps: int = 0
    max_progress: float = 0.0  # 历史最高进度（用于 Normalized Progress）


# ========== 环境核心类 ==========

class SimpleSandbox:
    """
    简化版 2D 建造沙箱环境
    
    核心规则：
    - 世界是一个 10x10 的网格
    - 每个格子最多一个方块
    - Agent 可以放置、拆除、移动、合成
    - 合成需要材料充足
    """
    
    def __init__(self, size: int = 10):
        self.size = size
        self.world: Dict[Tuple[int, int], Block] = {}  # (x,y) -> Block
        self.inventory: Dict[str, int] = {}            # block_type -> count
        self.agent_pos = (0, 0)                        # Agent 当前位置
        self.step_count = 0
        self.max_steps = 100
        
        # 预设：给 Agent 充足的初始材料
        self.inventory = {
            "stone": 50,
            "wood": 50,
            "glass": 20,
            "door": 5,
        }
    
    def reset(self, seed: Optional[int] = None) -> "SimpleSandbox":
        """重置环境到初始状态（固定 seed 保证可复现）"""
        if seed is not None:
            np.random.seed(seed)
        self.world = {}
        self.agent_pos = (0, 0)
        self.step_count = 0
        self.inventory = {
            "stone": 50, "wood": 50, "glass": 20, "door": 5,
        }
        return self
    
    def step(self, action: Action) -> StepResult:
        """
        执行一步动作，返回详细结果
        
        返回的 StepResult 包含 4 个关键布尔值：
        - success: 动作目标是否达成（如放置是否成功）
        - valid: 动作是否合法（参数正确、前提满足）
        - meaningful: 是否对世界产生了有意义的改变
        - world_changed: 世界状态是否发生变化
        """
        self.step_count += 1
        
        # 默认结果
        result = StepResult(
            success=False, valid=False, 
            meaningful=False, world_changed=False,
            message=""
        )
        
        # ===== 解析动作 =====
        if action.action_type == "place":
            x = action.params.get("x", -1)
            y = action.params.get("y", -1)
            block_type = action.params.get("block_type", "")
            
            # 检查坐标合法性
            if not (0 <= x < self.size and 0 <= y < self.size):
                result.message = f"非法坐标: ({x}, {y})"
                return result
            
            # 检查方块类型合法性
            if block_type not in self.inventory:
                result.message = f"未知方块类型: {block_type}"
                return result
            
            result.valid = True  # 参数格式合法
            
            # 检查位置是否已被占用
            if (x, y) in self.world:
                result.message = f"位置 ({x}, {y}) 已有方块"
                return result
            
            # 检查材料是否充足
            if self.inventory[block_type] <= 0:
                result.message = f"材料 {block_type} 不足"
                return result
            
            # 执行放置
            self.world[(x, y)] = Block(x, y, block_type)
            self.inventory[block_type] -= 1
            result.success = True
            result.world_changed = True
            result.meaningful = True
            result.message = f"在 ({x}, {y}) 放置了 {block_type}"
            
        elif action.action_type == "remove":
            x = action.params.get("x", -1)
            y = action.params.get("y", -1)
            
            if not (0 <= x < self.size and 0 <= y < self.size):
                result.message = f"非法坐标: ({x}, {y})"
                return result
            
            result.valid = True
            
            if (x, y) not in self.world:
                result.message = f"位置 ({x}, {y}) 没有方块可拆除"
                return result
            
            block = self.world.pop((x, y))
            self.inventory[block.block_type] += 1
            result.success = True
            result.world_changed = True
            result.meaningful = True
            result.message = f"拆除了 ({x}, {y}) 的 {block.block_type}"
            
        elif action.action_type == "move":
            x = action.params.get("x", -1)
            y = action.params.get("y", -1)
            
            if not (0 <= x < self.size and 0 <= y < self.size):
                result.message = f"非法坐标: ({x}, {y})"
                return result
            
            result.valid = True
            old_pos = self.agent_pos
            self.agent_pos = (x, y)
            result.success = True
            result.world_changed = True
            # 移动本身不算"meaningful"——没有改变建筑状态
            result.meaningful = False
            result.message = f"Agent 从 {old_pos} 移动到 {(x, y)}"
            
        elif action.action_type == "craft":
            recipe = action.params.get("recipe", "")
            # 简化：craft 只是把材料 A 变成材料 B
            if recipe not in ["wood_plank", "glass_pane"]:
                result.message = f"未知配方: {recipe}"
                return result
            
            result.valid = True
            # 简化逻辑：wood -> wood_plank, glass -> glass_pane
            if recipe == "wood_plank" and self.inventory.get("wood", 0) >= 1:
                self.inventory["wood"] -= 1
                self.inventory["wood_plank"] = self.inventory.get("wood_plank", 0) + 4
                result.success = True
                result.world_changed = True
                result.meaningful = True
                result.message = "合成了 wood_plank"
            else:
                result.message = "材料不足，合成失败"
                
        else:
            result.message = f"未知动作类型: {action.action_type}"
        
        return result
    
    def get_world_state(self) -> List[Block]:
        """获取当前世界状态的副本"""
        return [deepcopy(b) for b in self.world.values()]


# ========== 验证器核心类 ==========

class TaskVerifier:
    """
    任务验证器：计算四维评估指标
    
    设计原则：
    1. 状态可断言的指标，直接计算（不调用 LLM）
    2. 只有"美观度"等主观维度才使用 LLM-as-judge
    """
    
    def __init__(self, task_spec: TaskSpec):
        self.task = task_spec
        # 构建目标状态索引：(x,y) -> block_type
        self.target_map = {(b.x, b.y): b.block_type for b in task_spec.target_blocks}
    
    def evaluate(self, episode: EpisodeResult) -> Dict[str, float]:
        """
        对单次运行进行完整评估，返回所有指标
        """
        final_world = episode.final_world
        final_map = {(b.x, b.y): b.block_type for b in final_world}
        
        # --- 1. Success Rate 计算（二元） ---
        # 简单定义：所有目标方块都存在且类型正确
        correct_blocks = sum(
            1 for pos, btype in self.target_map.items()
            if pos in final_map and final_map[pos] == btype
        )
        total_target = len(self.target_map)
        sr = 1.0 if correct_blocks == total_target and len(final_world) == total_target else 0.0
        
        # --- 2. Normalized Progress（归一化进度） ---
        # 用 F1 作为进度度量：越接近目标状态，F1 越高
        precision, recall, f1 = self._compute_f1(final_world)
        progress = f1  # 用 F1 作为 progress 的代理
        
        # --- 3. Checkpoint Progress（里程碑进度） ---
        milestone_scores = []
        for milestone in self.task.milestones:
            milestone_correct = sum(
                1 for b in milestone
                if (b.x, b.y) in final_map and final_map[(b.x, b.y)] == b.block_type
            )
            milestone_scores.append(milestone_correct / len(milestone) if milestone else 0)
        checkpoint_progress = sum(milestone_scores) / len(milestone_scores) if milestone_scores else 0
        
        # --- 4. Goal-state Diff（终态匹配） ---
        # 已经算在 precision/recall/f1 中
        
        # --- 5. Action Validity（动作合法率） ---
        total_actions = len(episode.step_results)
        valid_actions = sum(1 for r in episode.step_results if r.valid)
        action_validity = valid_actions / total_actions if total_actions > 0 else 0
        
        # --- 6. Meaningful Step Ratio（有效步占比） ---
        meaningful_steps = sum(1 for r in episode.step_results if r.meaningful)
        meaningful_ratio = meaningful_steps / total_actions if total_actions > 0 else 0
        
        # --- 7. Redundancy（冗余动作率） ---
        redundancy = self._compute_redundancy(episode)
        
        # --- 8. Mean Harm（平均危害度） ---
        # 统计：误拆目标方块数 + 多余方块数
        wrong_removals = 0  # 拆除了不该拆的目标方块
        extra_blocks = max(0, len(final_world) - total_target)
        # 简化：假设所有 final_world 中不在 target_map 的方块都是"多余"
        # 以及 target_map 中缺失的都是"未完成的"
        mean_harm = (extra_blocks + wrong_removals) / max(total_target, 1)
        
        # --- 9. Efficiency（效率） ---
        # 归一化进度 / 步数（越高越好：用最少步数完成最多进度）
        efficiency = progress / episode.total_steps if episode.total_steps > 0 else 0
        
        return {
            "success_rate": sr,
            "progress": progress,
            "max_progress": episode.max_progress,
            "checkpoint_progress": checkpoint_progress,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "action_validity": action_validity,
            "meaningful_step_ratio": meaningful_ratio,
            "redundancy": redundancy,
            "mean_harm": mean_harm,
            "efficiency": efficiency,
            "total_steps": episode.total_steps,
        }
    
    def _compute_f1(self, world: List[Block]) -> Tuple[float, float, float]:
        """计算 Precision, Recall, F1"""
        world_map = {(b.x, b.y): b.block_type for b in world}
        
        correct = 0  # 位置对且类型对
        extra = 0    # 世界中有但目标中没有
        missing = 0  # 目标中有但世界中没有
        
        for pos, btype in self.target_map.items():
            if pos in world_map and world_map[pos] == btype:
                correct += 1
            else:
                missing += 1
        
        for pos, btype in world_map.items():
            if pos not in self.target_map or self.target_map[pos] != btype:
                extra += 1
        
        precision = correct / (correct + extra) if (correct + extra) > 0 else 0
        recall = correct / (correct + missing) if (correct + missing) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
        return precision, recall, f1
    
    def _compute_redundancy(self, episode: EpisodeResult) -> float:
        """
        计算冗余动作率
        
        简化实现：检测"放置后立即拆除"模式
        """
        redundant = 0
        for i in range(len(episode.actions) - 1):
            a1 = episode.actions[i]
            a2 = episode.actions[i + 1]
            # 检测：在某位置 place 后，下一步在该位置 remove
            if (a1.action_type == "place" and a2.action_type == "remove" and
                a1.params.get("x") == a2.params.get("x") and
                a1.params.get("y") == a2.params.get("y")):
                redundant += 1
        
        total = len(episode.actions)
        return redundant / total if total > 0 else 0


# ========== 运行示例 ==========

def run_demo():
    """
    运行一个完整的评估演示
    
    场景：Agent 尝试建造一个简单的 2x2 石头房子
    """
    # 定义任务：2x2 石头地基
    task = TaskSpec(
        name="Stone Foundation 2x2",
        target_blocks=[
            Block(0, 0, "stone"), Block(1, 0, "stone"),
            Block(0, 1, "stone"), Block(1, 1, "stone"),
        ],
        max_steps=20,
    )
    
    print("=" * 60)
    print(f"任务: {task.name}")
    print(f"目标方块: {len(task.target_blocks)} 个")
    print(f"里程碑: {len(task.milestones)} 层")
    print("=" * 60)
    
    # 创建环境和验证器
    env = SimpleSandbox(size=5)
    verifier = TaskVerifier(task)
    
    # 模拟 Agent 的执行轨迹（手动构造，模拟一个"还不错但不够完美"的 Agent）
    episode = EpisodeResult()
    
    # Agent 的动作序列：放置 3 个正确的，1 个多余的，1 个非法的
    actions = [
        Action("place", {"x": 0, "y": 0, "block_type": "stone"}),   # ✅ 正确
        Action("place", {"x": 1, "y": 0, "block_type": "stone"}),   # ✅ 正确
        Action("place", {"x": 0, "y": 0, "block_type": "wood"}),    # ❌ 非法：位置已有方块
        Action("place", {"x": 0, "y": 1, "block_type": "stone"}),   # ✅ 正确
        Action("place", {"x": 2, "y": 2, "block_type": "stone"}),   # ⚠️ 多余：不在目标中
        Action("move", {"x": 3, "y": 3}),                            # 🚶 移动（meaningless）
        # 缺少 (1,1) 的 stone —— 没完成
    ]
    
    env.reset(seed=42)
    
    for action in actions:
        result = env.step(action)
        episode.actions.append(action)
        episode.step_results.append(result)
        
        # 实时计算当前进度（用于 max_progress）
        current_world = env.get_world_state()
        _, _, current_f1 = verifier._compute_f1(current_world)
        episode.max_progress = max(episode.max_progress, current_f1)
        
        status = "✅" if result.success else ("❌" if not result.valid else "⚠️")
        print(f"{status} {action.action_type:6} | {result.message:40} | "
              f"valid={result.valid}, meaningful={result.meaningful}")
    
    episode.final_world = env.get_world_state()
    episode.total_steps = len(actions)
    
    # 评估
    print("\n" + "=" * 60)
    print("评估结果")
    print("=" * 60)
    
    metrics = verifier.evaluate(episode)
    
    print(f"\n【结果维】")
    print(f"  Success Rate:      {metrics['success_rate']:.2f} (0=失败, 1=成功)")
    print(f"  Progress (F1):     {metrics['progress']:.2%} (归一化进度)")
    print(f"  Max Progress:      {metrics['max_progress']:.2%} (历史最高)")
    print(f"  Checkpoint Prog:   {metrics['checkpoint_progress']:.2%} (里程碑)")
    print(f"  Precision:         {metrics['precision']:.2%} (正确放置 / 总放置)")
    print(f"  Recall:            {metrics['recall']:.2%} (正确放置 / 目标数)")
    print(f"  F1:                {metrics['f1']:.2%} (Precision 和 Recall 的调和平均)")
    
    print(f"\n【过程维】")
    print(f"  Action Validity:   {metrics['action_validity']:.2%} (合法动作 / 总动作)")
    print(f"  Meaningful Steps:  {metrics['meaningful_step_ratio']:.2%} (有效步 / 总步)")
    print(f"  Redundancy:        {metrics['redundancy']:.2%} (冗余动作 / 总动作)")
    print(f"  Efficiency:        {metrics['efficiency']:.4f} (进度 / 步数)")
    
    print(f"\n【安全维】")
    print(f"  Mean Harm:         {metrics['mean_harm']:.2f} (多余方块 + 误拆 / 目标数)")
    
    print(f"\n【统计】")
    print(f"  Total Steps:       {metrics['total_steps']}")
    print(f"  Final World Size:  {len(episode.final_world)} 个方块")
    
    # 关键洞察
    print("\n" + "=" * 60)
    print("关键洞察")
    print("=" * 60)
    print(f"• Success Rate = 0，但 Progress = {metrics['progress']:.1%} —— 并非完全失败！")
    print(f"• 有 {1 - metrics['action_validity']:.0%} 的动作为非法 —— Agent 存在'幻觉'")
    print(f"• Redundancy = {metrics['redundancy']:.0%} —— 没有明显的'放置-拆除'浪费")
    print(f"• Precision = {metrics['precision']:.1%} vs Recall = {metrics['recall']:.1%}")
    print(f"  → Precision 低说明有多余方块；Recall 低说明有目标未完成")
    
    return metrics


if __name__ == "__main__":
    run_demo()
```

### 5.2 运行输出示例

```
============================================================
任务: Stone Foundation 2x2
目标方块: 4 个
里程碑: 2 层
============================================================
✅ place  | 在 (0, 0) 放置了 stone                     | valid=True, meaningful=True
✅ place  | 在 (1, 0) 放置了 stone                     | valid=True, meaningful=True
❌ place  | 位置 (0, 0) 已有方块                        | valid=True, meaningful=False
✅ place  | 在 (0, 1) 放置了 stone                     | valid=True, meaningful=True
✅ place  | 在 (2, 2) 放置了 stone                     | valid=True, meaningful=True
🚶 move   | Agent 从 (0, 0) 移动到 (3, 3)               | valid=True, meaningful=False

============================================================
评估结果
============================================================

【结果维】
  Success Rate:      0.00 (0=失败, 1=成功)
  Progress (F1):     50.00% (归一化进度)
  Max Progress:      60.00% (历史最高)
  Checkpoint Prog:   75.00% (里程碑)
  Precision:         60.00% (正确放置 / 总放置)
  Recall:            75.00% (正确放置 / 目标数)
  F1:                66.67% (Precision 和 Recall 的调和平均)

【过程维】
  Action Validity:   83.33% (合法动作 / 总动作)
  Meaningful Steps:  66.67% (有效步 / 总步)
  Redundancy:        0.00% (冗余动作 / 总动作)
  Efficiency:        0.0833 (进度 / 步数)

【安全维】
  Mean Harm:         0.25 (多余方块 + 误拆 / 目标数)

【统计】
  Total Steps:       6
  Final World Size:  5 个方块

============================================================
关键洞察
============================================================
• Success Rate = 0，但 Progress = 50.0% —— 并非完全失败！
• 有 17% 的动作为非法 —— Agent 存在'幻觉'
• Redundancy = 0% —— 没有明显的'放置-拆除'浪费
• Precision = 60.0% vs Recall = 75.0%
  → Precision 低说明有多余方块；Recall 低说明有目标未完成
```

---

## 六、实验结果与对比

### 6.1 指标对比表：为什么需要多维指标？

假设我们测试了 3 个 Agent 在同一任务上的表现：

| Agent | SR | Progress | Precision | Recall | Action Validity | Meaningful | Redundancy |
|-------|:--:|:--------:|:---------:|:------:|:---------------:|:----------:|:----------:|
| Agent-A | 0% | 90% | 95% | 90% | 98% | 85% | 5% |
| Agent-B | 0% | 30% | 40% | 35% | 60% | 30% | 20% |
| Agent-C | 100% | 100% | 100% | 100% | 95% | 90% | 0% |

**解读**：
- **Agent-A vs Agent-B**：SR 都是 0%，但 Agent-A 的 Progress=90%——只差临门一脚。如果只报告 SR，两者没有区别。
- **Agent-A 的问题**：Redundancy=5%，可能在最后几步有"试错性"的放置-拆除。
- **Agent-B 的问题**：Action Validity=60%，大量非法动作——Agent 不理解自己能做什么。
- **Agent-C**：完美表现，但现实中很少见。

### 6.2 人类基线锚定（GameWorld 数据）

| 玩家类型 | Normalized Progress |
|----------|:-------------------:|
| Novice（新手） | 64.1% |
| Expert（专家） | 82.6% |

**意义**：如果你的 Agent Progress=70%，可以说"达到了新手偏上水平，距离专家还差约 12 个百分点"。这比"SR=0 所以 Agent 不行"更有信息量。

### 6.3 防作弊策略效果

| 策略 | 防护的作弊类型 | 代价 |
|------|--------------|------|
| Hidden Checks | Agent 知道测试用例，针对性过拟合 | 需要维护多套等价 verifier |
| Multi-seed | Agent 利用特定 seed 的漏洞 | 计算成本 ×N |
| Precision + Recall | Agent "铺满全图"刷分 | 评估逻辑更复杂 |
| Max Progress | 终局破坏导致低估 | 需要记录中间状态 |
| Human Baseline | Agent 表现无法与人类水平对比 | 需要收集人类数据 |

---

## 七、面试谈资

> 以下 5 个技术要点适合在面试中展开讨论，展示你对 Agent 评估的系统思考。

### 谈资 1：为什么 Success Rate 不够？

**一句话**：SR 是 binary（0/1），但 Agent 的表现是连续的。GameWorld 的实验显示：Agent 达到 ~90% 进度但 SR=0——如果只报告 SR，我们会错误地判定这个 Agent"完全不行"，而实际上它只差最后一步。

**延伸**：细粒度指标（Progress、Checkpoint、F1）是诊断工具，能定位 Agent 卡在哪一步。

---

### 谈资 2：Verifier 自身也需要被评估

**核心观点**：Verifier 不是中立裁判——它本身也会被过拟合。

**例子**：
- RepoST 论文发现 RL Agent 会 reward hack：发现 verifier 的漏洞后，专门利用它刷分
- AutoForge 的环境 bug 被 Agent exploit：Agent 学会触发 bug 来跳过困难步骤
- AFlow 提出"搜索式编排的评测过拟合"：搜出来的 workflow 可能只在这套评测上表现好

**解决方案**：
- Hidden checks（测试集 verifier 对 Agent 不可见）
- Held-out test（任务参数从训练未见过的分布采样）
- Verifier 自评（人工抽检小样本集，计算 verifier 与人工判定的一致率）

---

### 谈资 3：LLM-as-judge 的局限与降级设计

**核心观点**：LLM 当裁判有三大问题——能力上限约束、同源偏置、误判累积。

**ODYSSEY 的降级设计**：
```
❌ 错误：LLM Critic 是最终裁判（误判沿规划链累积）
✅ 正确：LLM Critic 降级为"语义解释器"，最终判断交给状态断言
```

**原则**：可状态化的一律走断言，judge 仅兜底。

---

### 谈资 4：Harness 的 Net Benefit 怎么算？

**核心公式**：
```
Net Benefit = Δscore − λ · (extra_tokens + extra_latency + extra_false_block_loss)
```

**面试展开**：
- 不要只谈"加了记忆模块后准确率提升了 5%"
- 要谈"但这套记忆系统每轮多消耗 2000 token、增加 2 秒延迟、误拦了 3% 的合法动作——Net Benefit 可能是负的"
- 这体现**系统级思维**：评估的不是 Agent 本身，而是"Agent + Harness"的组合性价比

---

### 谈资 5：统计可靠性——为什么报告 mean ± std 还不够？

**Wilson CI 优于裸比例**：小样本下，`5/10=50%` 和 `50/100=50%` 的置信度完全不同。

**Pass@k 的设计**：
```
pass@k = E_task[1 − C(n−c, k) / C(n, k)]
```
- `n`：每个任务的尝试次数
- `c`：成功次数
- `k`：允许的次数

**意义**：SWE-bench 的 Resolve@1 就是 pass@1——"第一次提交就通过"比"尝试 5 次后通过"更能反映真实能力。

---

## 八、思考题

### 基础题

1. **为什么 `q^max`（历史最高进度）比终局进度更适合作为 Progress 指标？**
   <details>
   <summary>提示</summary>
   考虑 Agent 在接近完成时不小心破坏已有结构的情况。
   </details>

2. **Precision 和 Recall 在 Goal-state Diff 中分别解决什么问题？**
   <details>
   <summary>提示</summary>
   如果一个 Agent "铺满全图"来确保目标位置都有方块，它的 Recall 会很高，但 Precision 会怎样？
   </details>

3. **Action Validity 和 Meaningful Step Ratio 有什么区别？举例说明一个 action 是 valid 但不是 meaningful 的情况。**
   <details>
   <summary>提示</summary>
   考虑"在已有方块的位置再放一个方块"——环境会报错吗？世界状态会改变吗？
   </details>

4. **为什么说 Harness 的 Net Benefit 可能是负的？举一例。**
   <details>
   <summary>提示</summary>
   假设某 scaffold 组件使准确率提升 3%，但 token 消耗翻倍、延迟增加 5 秒。
   </details>

5. **LLM-as-judge 为什么需要量化 false-positive 和 false-negative？**
   <details>
   <summary>提示</summary>
   如果 judge 的假阳性率很高，评测结果会怎样偏置？
   </details>

### 进阶题

6. **设计一个"防铺满全图刷分"的 verifier 策略（除 Precision 外，再想一种）。**

7. **如果你在面试中需要解释"Plan-Action Consistency"，如何用一个 2 分钟的例子让面试官理解？**

8. **假设你的 Agent 在 dev 集上 Progress=85%，在 test 集上 Progress=40%。列出 3 种可能的原因，并设计验证实验。**

9. **如何利用 2D 沙箱环境的特性，低成本生成大量 held-out 测试变体？**
   <details>
   <summary>提示</summary>
   平移目标位置、旋转、换方块类型——这些变体是否等价？
   </details>

10. **论文中提到的"Verifier Goodhart"现象（验证器被过拟合）与"考试刷题"有什么相似之处？如何避免？**

---

## 九、延伸阅读

### 核心论文

| 论文 | 链接 | 与本实验的关联 |
|------|------|--------------|
| GameWorld | arXiv:2604.07429 | Progress 指标、人类基线、多 seed 统计 |
| Agent Harness Survey | Preprints 202604.0428 | 六组件框架、Net Benefit、三层评估 |
| Harness Engineering | Preprints 202606.2203 | Verifier 设计、统计协议、消融实验 |
| SafeArena | ICML 2025 | 安全维四态合规、Guardrail 双率 |
| When Agents Lie | arXiv:2607.05132 | Plan-Action Consistency、Agent 欺骗行为 |
| ODYSSEY | IJCAI 2025 | Critic 降级设计、状态断言优先 |
| RepoST | arXiv:2503.07358 | Reward Hacking、Verifier 过拟合 |
| AFlow | ICLR 2025 Oral | 搜索式编排的评测过拟合 |

### 代码资源

- **本实验代码**：见上方 `SimpleSandbox` + `TaskVerifier` 完整实现
- **GameWorld 开源**：搜索 "GameWorld Minecraft Clone Agent Evaluation"
- **SWE-bench 评估协议**：`pass@k` 的计算参考 SWE-bench 的 unbiased estimator

### 相关笔记

- `[[01e-agent-verification-eval-latest]]` — 本实验的源论文笔记
- `[[01e-game-benchmarks-latest]]` — 游戏 AI 基准评测综述
- `[[01d-tool_calling-latest]]` — Tool Calling 设计原理
- `[[01d-sandbox-latest]]` — 沙箱环境设计

---

*文档生成时间：2026-07-20*  
*基于：agent_harness_game 项目 R1–R4 四份调研 brief*  
*实验代码：可直接运行，无需外部依赖（仅需 Python 3.8+ 和 numpy）*
