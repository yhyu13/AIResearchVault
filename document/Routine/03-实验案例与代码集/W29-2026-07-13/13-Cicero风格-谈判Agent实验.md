---
tags: [experiment, cicero, diplomacy, negotiation-agent, game-ai, game-theory]
aliases: [实验13, Cicero谈判Agent实验]
reference: [[01c-Human-AI-Game-Interaction]]
created: 2026-07-13
---

# 实验 13：Cicero 风格——谈判 Agent 实验

> **对应论文**：Cicero — Diplomacy 谈判 AI（Meta, Science 2022）
> **目标**：实现简化版 Cicero 双系统架构，在微型 Diplomacy 中演示谈判与策略的耦合。

---

## 1. 实验背景

### 1.1 Cicero 核心架构

Cicero 是首个在 Diplomacy（外交策略桌游）中达到人类水平的 AI。其核心创新是**双系统架构**：

- **语言模型**：负责理解对话、生成谈判文本、解析玩家意图
- **战略规划模型**：类似 AlphaZero，评估棋局价值、选择最优行动
- **意图过滤**：在生成对话前，检查 AI 是否能兑现承诺，避免"说一套做一套"

### 1.2 本实验简化

由于 Diplomacy 完整规则复杂（7 国、34 领土、多阶段行动），本实验将其简化为：

- **3 个势力**：A（红色）、B（蓝色）、C（绿色）
- **5 个领土**：T1, T2, T3, T4, T5（连接关系固定）
- **单阶段**：谈判 + 行动同时结算（类似简化 Diplomacy）
- **胜利条件**：控制 3 个领土即可获胜，或 10 轮后领土最多者胜

---

## 2. 实验设计

### 2.1 游戏模型

```
领土连接图：
    T1 — T2 — T3
         |     |
         T4 — T5

每个势力初始控制 1 个领土，拥有 1 个单位。
```

### 2.2 行动类型

| 行动 | 描述 | 效果 |
|------|------|------|
| `move target` | 移动到相邻领土 | 若目标无防守方，占领；若有两方以上争夺，则冲突 |
| `hold` | 原地防守 | 防止被占领 |
| `support ally target` | 支持盟友攻击目标 | 攻击方获得 +1 力量 |

### 2.3 双系统架构

> **核心概念：双系统解耦**
> 
> Cicero 的关键创新是将"语言理解/生成"与"战略决策"分离为两个独立模块，中间通过**意图过滤**桥接。这种解耦避免了传统端到端模型"说一套做一套"的问题——语言模型可能为了赢得对话而做出无法兑现的承诺，而战略模块只关心最优行动，两者若不协调会产生矛盾行为。
> 
> 形式化地，设语言模块输出消息 $m$，战略模块输出行动 $a$，意图过滤是一个谓词函数：
> $$
> \text{Filter}(m, a) = \begin{cases} \text{True} & \text{if } m \text{ 的承诺可被 } a \text{ 兑现} \\ \text{False} & \text{otherwise} \end{cases}
> $$

```
┌─────────────────────────────────────────────────────────────┐
│                      Cicero 简化架构                         │
├─────────────────────────────────────────────────────────────┤
│  语言模块 (Language Module)                                   │
│  ├── 提议生成器：根据战略目标生成谈判文本                      │
│  ├── 回应解析器：解析对手消息，提取意图                        │
│  └── 模板引擎：基于规则填充模板                                │
├─────────────────────────────────────────────────────────────┤
│  战略模块 (Strategic Module)                                  │
│  ├── 棋局评估：评估当前局势价值（V(s)）                        │
│  ├── 行动规划：选择最优行动（类似 Minimax）                    │
│  └── 承诺追踪：记录哪些承诺是可兑现的                          │
├─────────────────────────────────────────────────────────────┤
│  意图过滤 (Intent Filter)                                     │
│  ├── 承诺验证：检查提议是否被战略模块支持                      │
│  └── 冲突检测：避免矛盾承诺                                    │
└─────────────────────────────────────────────────────────────┘
```

### 2.4 谈判流程

> **核心概念：同时行动博弈（Simultaneous Move Game）**
> 
> Diplomacy 是**不完美信息、同时行动**的博弈。与象棋（轮流行动、完美信息）不同，所有玩家在每轮同时选择行动，且无法观察他人的选择。这导致了一个经典的博弈论困境：即使达成了口头协议，也无法验证对方是否真的会遵守——这正是意图过滤和信任机制存在的根本原因。
> 
> 从博弈论角度，每轮是一个**标准型博弈（Normal Form Game）**，每个玩家的收益取决于所有玩家的行动组合。求解这类博弈通常需要纳什均衡概念，但 Cicero 采用的是**启发式搜索 + 信念更新**的实用方法。

```
Round 1:
1. 每个 Agent 向其他 Agent 发送谈判消息（可提议结盟、支持、欺骗）
2. 收到消息后，Agent 解析并更新内部信念状态
3. 意图过滤：检查 Agent 自己发的承诺是否可兑现
4. 战略模块根据所有信息（包括谈判结果）选择行动
5. 同时执行所有行动，结算领土变化
6. 检查胜利条件
```

---

## 3. 完整 Python 代码

> **代码阅读指南**：本代码按模块组织，建议按顺序阅读：数据结构 → 游戏引擎 → 语言模块 → 战略模块 → 意图过滤 → Agent整合 → 主循环。每个类和函数都附有中文 docstring 和关键逻辑注释。

```python
#!/usr/bin/env python3
"""
Cicero-Style Negotiation Agent Experiment
简化版 Diplomacy 谈判模拟

架构：
  - 语言模块：基于规则的模板生成 + 简单解析
  - 战略模块：Minimax + 棋局评估
  - 意图过滤：确保承诺与行动一致

作者：实验撰写员_13
"""

from __future__ import annotations
import random
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional
from enum import Enum, auto
from collections import defaultdict
import copy


# ============================================================
# 1. 基础数据结构
# ============================================================

class ActionType(Enum):
    """行动类型枚举
    
    三种基本行动：
      - MOVE: 移动到相邻领土
      - HOLD: 原地防守
      - SUPPORT: 支持盟友攻击
    """
    MOVE = "move"
    HOLD = "hold"
    SUPPORT = "support"


@dataclass
class Action:
    """单个行动
    
    参数:
        power: 执行者（A/B/C），标识哪个势力执行此行动
        action_type: 行动类型（MOVE/HOLD/SUPPORT）
        target: 目标领土（MOVE/HOLD 时使用）
        support_target: 被支持的盟友（SUPPORT 时使用，表示支持哪个势力）
        support_against: 支持攻击的目标（SUPPORT 时使用，表示攻击哪个领土）
    
    注意:
        SUPPORT 行动的特殊语义：support_target 是盟友当前所在的领土，
        support_against 是盟友要攻击的目标领土。这两个字段只在 action_type=SUPPORT 时有效。
    """
    power: str                          # 执行者（A/B/C）
    action_type: ActionType
    target: str                         # 目标领土（MOVE/HOLD）
    support_target: Optional[str] = None  # 支持的盟友（SUPPORT）
    support_against: Optional[str] = None   # 支持攻击的目标（SUPPORT）

    def __repr__(self):
        if self.action_type == ActionType.MOVE:
            return f"{self.power}: MOVE -> {self.target}"
        elif self.action_type == ActionType.HOLD:
            return f"{self.power}: HOLD {self.target}"
        else:
            return (f"{self.power}: SUPPORT {self.support_target} "
                    f"against {self.support_against}")


@dataclass
class Message:
    """谈判消息
    
    参数:
        sender: 发送方势力（A/B/C）
        receiver: 接收方势力（A/B/C）
        msg_type: 消息类型，可选值：
            - propose_alliance: 提议结盟
            - promise_support: 承诺支持
            - propose_attack: 提议共同攻击
            - reject: 拒绝提议
            - accept: 接受提议
            - threat: 威胁
        content: 消息的文本内容（由模板引擎生成）
        territories: 相关领土列表（用于承诺支持或攻击时指定目标）
        target_power: 攻击/支持的目标势力（用于结盟或攻击提议）
    
    设计说明:
        使用 dataclass 自动实现 __init__ 和基本比较方法，content 字段存储人类可读文本，
        其他字段存储结构化信息供 Agent 解析。
    """
    sender: str
    receiver: str
    msg_type: str        # propose_alliance / promise_support / propose_attack / reject / accept
    content: str
    territories: List[str] = field(default_factory=list)  # 相关领土
    target_power: Optional[str] = None  # 攻击/支持的目标势力

    def __repr__(self):
        return f"[{self.sender}->{self.receiver}] {self.msg_type}: {self.content}"


# ============================================================
# 2. 游戏引擎
# ============================================================

class DiplomacyGame:
    """简化版 Diplomacy 游戏引擎
    
    核心职责：
      1. 维护领土连接图、单位位置、领土所有权
      2. 同时结算所有行动（处理冲突、支持、防守）
      3. 检查胜利条件
    
    关键设计：
      - 同时结算：所有行动在 resolve_moves() 中一次性处理，模拟 Diplomacy 的同步机制
      - 力量对比：攻击方力量 vs 防守方力量，大者胜；平局则防守方保留
    """

    # 领土连接图（无向图）
    # T2 是中心节点，连接 T1/T3/T4，战略价值最高
    ADJACENCY = {
        "T1": {"T2"},
        "T2": {"T1", "T3", "T4"},
        "T3": {"T2", "T5"},
        "T4": {"T2", "T5"},
        "T5": {"T3", "T4"},
    }

    def __init__(self, powers: List[str] = None):
        """初始化游戏
        
        参数:
            powers: 参与游戏的势力列表，默认 ["A", "B", "C"]
        """
        self.powers = powers or ["A", "B", "C"]
        self.territories = ["T1", "T2", "T3", "T4", "T5"]
        self.round = 0

        # 初始分配：每个势力 1 个单位，放在不同领土
        self.units: Dict[str, str] = {}  # power -> territory（单位当前位置）
        self.ownership: Dict[str, str] = {}  # territory -> power（领土所有权）
        self._init_positions()

    def _init_positions(self):
        """初始化势力位置（固定分配，确保可复现）"""
        # 固定分配：A->T1, B->T3, C->T5
        # 选择这三个位置是因为它们互不相邻，避免初始冲突
        starts = {"A": "T1", "B": "T3", "C": "T5"}
        for p in self.powers:
            self.units[p] = starts[p]
            self.ownership[starts[p]] = p

    def get_adjacent(self, terr: str) -> Set[str]:
        """获取某个领土的相邻领土"""
        return self.ADJACENCY.get(terr, set())

    def get_occupant(self, terr: str) -> Optional[str]:
        """获取某个领土的当前占领者（单位所在位置）
        
        注意：ownership 和 units 可能不一致（单位移动后所有权可能未更新）
        """
        for p, t in self.units.items():
            if t == terr:
                return p
        return None

    def resolve_moves(self, actions: List[Action]) -> None:
        """同时结算所有行动（简化版 Diplomacy 规则）
        
        结算流程：
          1. 收集所有 MOVE/HOLD/SUPPORT 行动
          2. 应用 SUPPORT（支持方未移动时，被支持的攻击力量 +1）
          3. 结算冲突：对每个目标领土，比较所有攻击方的力量 vs 防守方力量
          4. 更新单位位置和领土所有权
        
        关键规则：
          - 若多方攻击同一目标，力量最大者胜；若平局，均失败
          - 防守方力量 = 1（基础）+ 可能的支持
          - 若防守方 MOVE out，则防守力量为 0
        """
        # 1. 收集所有移动和支持
        moves = {}        # target -> list of (power, strength)
        supports = {}     # (target, against) -> list of power
        holds = {}        # power -> hold_target

        for a in actions:
            if a.action_type == ActionType.MOVE:
                # MOVE 行动：对目标领土发起力量为 1 的攻击
                moves.setdefault(a.target, []).append((a.power, 1))
            elif a.action_type == ActionType.HOLD:
                # HOLD 行动：记录防守位置，同时对所在领土贡献 1 点防守力量
                holds[a.power] = a.target
                moves.setdefault(a.target, []).append((a.power, 1))
            elif a.action_type == ActionType.SUPPORT:
                # SUPPORT 行动：记录支持关系 (被支持的盟友, 盟友攻击的目标) -> 支持者列表
                key = (a.support_target, a.support_against)
                supports.setdefault(key, []).append(a.power)

        # 2. 应用支持（支持方必须在相邻位置且没有移动）
        # 简化规则：只要支持方没有执行 MOVE 行动，支持就有效
        # 真实 Diplomacy 中支持会被"切断"（支持者被攻击），这里简化处理
        supported = defaultdict(int)  # (power, target) -> 额外力量

        for (supp_target, against), supporters in supports.items():
            for sp in supporters:
                # 检查支持者是否执行了 MOVE：若移动，则支持无效
                if any(a.power == sp and a.action_type == ActionType.MOVE for a in actions):
                    continue  # 支持者在移动，支持无效
                # 支持生效：被支持的攻击方在 against 目标上获得 +1 力量
                for idx, (p, s) in enumerate(moves.get(against, [])):
                    if p == supp_target:
                        moves[against][idx] = (p, s + 1)
                        break

        # 3. 结算所有冲突
        # 核心逻辑：遍历每个 MOVE 行动，判断攻击是否成功
        new_units = {}    # 成功移动后的新位置
        processed = set() # 已处理的势力（避免重复结算）

        for a in actions:
            if a.action_type == ActionType.MOVE and a.power not in processed:
                target = a.target
                # 获取该攻击方对 target 的总攻击力量（含支持）
                attack_power = 1
                for idx, (p, s) in enumerate(moves.get(target, [])):
                    if p == a.power:
                        attack_power = s
                        break

                # 检查 target 是否有防守方
                defender = self.get_occupant(target)
                defend_power = 0
                if defender and defender != a.power:
                    # 防守方的基础力量（HOLD 或原地未动）
                    for idx, (p, s) in enumerate(moves.get(target, [])):
                        if p == defender:
                            defend_power = s
                            break
                    # 关键规则：如果防守方也在 MOVE out，则没有防守力量
                    for act in actions:
                        if act.power == defender and act.action_type == ActionType.MOVE:
                            defend_power = 0
                            break

                # 比较力量：攻击方必须严格大于防守方才能占领
                if attack_power > defend_power:
                    # 额外检查：是否有其他攻击方力量相同或更大（冲突）
                    all_attackers = moves.get(target, [])
                    max_power = max((s for _, s in all_attackers), default=0)
                    attackers = [p for p, s in all_attackers if s == max_power]
                    # 成功条件：
                    #   1. 只有唯一最大力量者
                    #   2. 该最大力量者就是当前攻击方
                    #   3. 当前攻击方力量等于最大力量（即自己是最大力量者）
                    if len(attackers) == 1 and attackers[0] == a.power and attack_power == max_power:
                        new_units[a.power] = target
                        processed.add(a.power)

        # 4. 未成功移动的单位保持原位
        for a in actions:
            if a.power not in new_units and a.power not in processed:
                # 简化处理：未移动成功的单位退回原位
                new_units[a.power] = self.units[a.power]

        # 5. 更新游戏状态
        self.units = new_units
        # 更新领土所有权（占领即拥有）
        for p, t in self.units.items():
            self.ownership[t] = p
        # 未占领的领土保持原所有者（简化规则）
        for t in self.territories:
            if t not in self.ownership:
                self.ownership[t] = None

        self.round += 1

    def get_state(self) -> Dict:
        """获取当前游戏状态的深拷贝（用于战略模块评估和模拟）"""
        return {
            "round": self.round,
            "units": copy.deepcopy(self.units),
            "ownership": copy.deepcopy(self.ownership),
        }

    def check_winner(self) -> Optional[str]:
        """检查是否有玩家获胜（控制 >= 3 领土）
        
        返回:
            获胜势力名称，或 None（游戏继续）
        """
        counts = defaultdict(int)
        for t, owner in self.ownership.items():
            if owner:
                counts[owner] += 1
        for p, c in counts.items():
            if c >= 3:
                return p
        return None

    def __repr__(self):
        lines = [f"=== Round {self.round} ==="]
        lines.append(f"Units: {self.units}")
        lines.append(f"Ownership: {self.ownership}")
        return "\n".join(lines)


# ============================================================
# 3. 语言模块（Language Module）
# ============================================================

class LanguageModule:
    """
    基于规则+模板的语言模块
    模拟 Cicero 的语言生成能力（简化版）
    
    设计说明：
      - 使用预定义模板 + 随机选择生成多样化文本
      - 解析器提取结构化信息（信任度变化）供战略模块使用
      - 真实 Cicero 使用 70B 参数 LLM，这里是极简模拟
    """

    # 消息模板库：每种消息类型对应多个模板，随机选择以增加多样性
    TEMPLATES = {
        "propose_alliance": [
            "{me} 提议与 {you} 结盟。我们可以一起对抗 {target}。",
            "{you}，{me} 认为我们联手对抗 {target} 是最优策略。",
        ],
        "promise_support": [
            "{me} 承诺在 {territory} 支持 {you} 的行动。",
            "{you} 可以信任 {me} —— 我会支持你在 {territory} 的进攻。",
        ],
        "propose_attack": [
            "{me} 建议我们共同攻击 {target} 的 {territory}。",
            "如果我们联合进攻 {target} 在 {territory} 的单位，一定能成功。",
        ],
        "accept": [
            "{me} 接受 {you} 的提议。",
            "很好，{me} 同意合作。",
        ],
        "reject": [
            "{me} 无法同意这个提议。",
            "{me} 需要重新考虑 {you} 的提案。",
        ],
        "threat": [
            "{me} 警告 {you}：如果不合作，我将支持 {target} 对抗你。",
        ],
    }

    def __init__(self, power: str):
        """初始化语言模块
        
        参数:
            power: 该模块所属的势力名称
        """
        self.power = power

    def generate_message(self, receiver: str, msg_type: str,
                         target_power: Optional[str] = None,
                         territories: List[str] = None) -> Message:
        """生成谈判消息
        
        参数:
            receiver: 消息接收方
            msg_type: 消息类型（必须在 TEMPLATES 中）
            target_power: 攻击/结盟的目标势力（用于模板填充）
            territories: 相关领土列表（用于模板填充）
        
        返回:
            Message 对象，包含生成的文本和结构化信息
        
        实现说明:
            从模板库中随机选择一个模板，用 format() 填充变量（me, you, target, territory）
        """
        templates = self.TEMPLATES.get(msg_type, ["{me} 发送消息给 {you}"])
        template = random.choice(templates)

        content = template.format(
            me=self.power,
            you=receiver,
            target=target_power or "某势力",
            territory=territories[0] if territories else "某地"
        )

        return Message(
            sender=self.power,
            receiver=receiver,
            msg_type=msg_type,
            content=content,
            territories=territories or [],
            target_power=target_power
        )

    def parse_incoming(self, message: Message) -> Dict:
        """解析收到的消息，提取关键信息并更新信念
        
        参数:
            message: 收到的 Message 对象
        
        返回:
            信念字典，包含：
              - sender: 发送方
              - type: 消息类型
              - target: 目标势力
              - territories: 相关领土
              - trust_delta: 信任度变化（根据消息类型预设）
        
        信任度更新规则：
          - propose_alliance: +0.2（结盟提议增加信任）
          - promise_support: +0.1（承诺支持小幅增加信任）
          - accept: +0.3（接受合作显著增加信任）
          - reject: -0.1（拒绝降低信任）
          - threat: -0.3（威胁大幅降低信任）
        
        注意：这是极度简化的信任模型。真实系统中信任度应基于历史交互动态更新。
        """
        belief = {
            "sender": message.sender,
            "type": message.msg_type,
            "target": message.target_power,
            "territories": message.territories,
            "trust_delta": 0.0,  # 信任度变化
        }

        if message.msg_type == "propose_alliance":
            belief["trust_delta"] = 0.2
        elif message.msg_type == "promise_support":
            belief["trust_delta"] = 0.1
        elif message.msg_type == "accept":
            belief["trust_delta"] = 0.3
        elif message.msg_type == "reject":
            belief["trust_delta"] = -0.1
        elif message.msg_type == "threat":
            belief["trust_delta"] = -0.3

        return belief


# ============================================================
# 4. 战略模块（Strategic Module）
# ============================================================

class StrategicModule:
    """
    基于 Minimax + 棋局评估的战略模块
    模拟 Cicero 的战略规划能力（简化版）
    
    核心组件：
      1. evaluate_state(): 手工设计的棋局评估函数 V(s)
      2. get_possible_actions(): 生成所有合法行动
      3. minimax_plan(): 简化版 Minimax 搜索（depth=2）
    
    与真实 Cicero 的区别：
      - 真实 Cicero 使用类似 AlphaZero 的神经网络评估 + MCTS 搜索
      - 本实验使用手工特征 + 简化 Minimax，用于教学演示
    """

    def __init__(self, power: str, game: DiplomacyGame):
        """初始化战略模块
        
        参数:
            power: 该模块所属的势力名称
            game: DiplomacyGame 实例（用于获取游戏状态）
        """
        self.power = power
        self.game = game
        # 每个领土的价值（中心位置 T2 最值钱，边角 T1/T3 最便宜）
        # 这个权重是手工设计的启发式，反映领土的战略重要性
        self.territory_values = {
            "T1": 1.0, "T2": 2.0, "T3": 1.0,
            "T4": 1.5, "T5": 1.5,
        }

    def evaluate_state(self, state: Dict) -> float:
        """评估给定状态的棋局价值 V(s)
        
        参数:
            state: 游戏状态字典，包含 "units" 和 "ownership"
        
        返回:
            浮点数评分：正值表示对我方有利，负值表示不利
        
        评估函数设计（手工启发式）：
          1. 领土控制：自己控制的领土加分（权重×2），敌方控制的减分（权重×0.5）
          2. 单位位置：靠近中心 T2 更好（距离越近加分越多）
          3. 获胜奖励：控制 >=3 个领土时获得大额奖励 +100
        
        数学形式：
        $$
        V(s) = \sum_{t \in \text{terr}} \left[ \mathbb{1}_{o_t = \text{me}} \cdot v_t \cdot 2 - \mathbb{1}_{o_t \neq \text{me}, o_t \neq \text{None}} \cdot v_t \cdot 0.5 \right] + \sum_{p} \frac{\pm 1}{d_t + 1} + \mathbb{1}_{\text{win}} \cdot 100
        $$
        
        注意：这是极度简化的评估函数。真实 Cicero 的 V(s) 由神经网络拟合，
        从数百万局对弈数据中学习。
        """
        ownership = state.get("ownership", self.game.ownership)
        units = state.get("units", self.game.units)

        score = 0.0
        # 1. 自己控制的领土价值（正向）vs 敌方控制（负向）
        for t, owner in ownership.items():
            if owner == self.power:
                score += self.territory_values.get(t, 1.0) * 2.0
            elif owner is not None:
                score -= self.territory_values.get(t, 1.0) * 0.5

        # 2. 单位位置优势（靠近中心 T2 更好）
        # center_dist: 到 T2 的图距离（T2=1, T1/T3/T4/T5=2）
        center_dist = {
            "T1": 2, "T2": 1, "T3": 2,
            "T4": 1, "T5": 2,
        }
        for p, t in units.items():
            if p == self.power:
                # 己方单位：越靠近中心加分越多（1/(dist+1)）
                score += 1.0 / (center_dist.get(t, 1) + 1)
            else:
                # 敌方单位：越靠近中心对我方越不利（减分）
                score -= 0.3 / (center_dist.get(t, 1) + 1)

        # 3. 获胜倾向奖励（大额正向激励）
        my_count = sum(1 for o in ownership.values() if o == self.power)
        if my_count >= 3:
            score += 100.0

        return score

    def get_possible_actions(self, power: str, state: Dict) -> List[Action]:
        """获取某个势力的所有可能行动
        
        参数:
            power: 要查询的势力
            state: 游戏状态（用于确定单位位置）
        
        返回:
            该势力所有合法行动的列表
        
        行动生成规则：
          1. HOLD：总是合法（原地不动）
          2. MOVE：可以移动到任意相邻领土
          3. SUPPORT：对相邻领土的占领者，支持其攻击该领土的任意邻居
        
        注意：本简化版本不检查"是否支持自己"等边界情况，真实 Diplomacy 规则更复杂。
        """
        units = state.get("units", self.game.units)
        if power not in units:
            return []

        pos = units[power]           # 当前位置
        adjacent = self.game.get_adjacent(pos)  # 相邻领土
        actions = []

        # 1. HOLD：原地防守，总是合法
        actions.append(Action(power, ActionType.HOLD, pos))

        # 2. MOVE：移动到任意相邻领土（包括空领土和敌方领土）
        for adj in adjacent:
            actions.append(Action(power, ActionType.MOVE, adj))

        # 3. SUPPORT：支持相邻领土的占领者攻击其邻居
        # 简化规则：只要相邻，就可以支持该位置的单位攻击任意相邻目标
        for adj in adjacent:
            adj_neighbors = self.game.get_adjacent(adj)
            for n in adj_neighbors:
                if n != pos:  # 不支持攻击自己所在位置（无意义）
                    actions.append(Action(
                        power, ActionType.SUPPORT,
                        target=pos,           # 支持时 target 是己方位置（支持方不动）
                        support_target=adj,   # 被支持的盟友所在位置
                        support_against=n     # 盟友攻击的目标
                    ))

        return actions

    def minimax_plan(self, depth: int = 2) -> Tuple[Action, float]:
        """Minimax 规划（简化版）
        
        参数:
            depth: 搜索深度（本实现中未实际使用，仅保留接口）
        
        返回:
            (best_action, best_value): 最优行动及其评估值
        
        算法说明：
          本实现是"简化版 Minimax"，核心假设是"其他所有势力联合对抗我"。
          这不是标准 Minimax（标准 Minimax 假设零和博弈、双方轮流行动），
          而是针对同时行动博弈的实用近似：
          
          对于我的每个可能行动 a：
            假设每个对手选择对我最不利的行动（最小化我的评估值）
            记录该 a 下的最坏结果 worst_value
          选择使 worst_value 最大的行动（Maximin 策略）
          
        数学形式：
        $$
        a^* = \arg\max_{a \in A_{\text{me}}} \min_{a_{-i} \in A_{-i}} V(s_{\text{next}}(a, a_{-i}))
        $$
        
        其中 $A_{\text{me}}$ 是我的行动集合，$A_{-i}$ 是所有对手的行动组合，
        $s_{\text{next}}$ 是执行行动后的新状态。
        
        注意：真实 Cicero 使用类似 AlphaZero 的 MCTS + 神经网络，搜索深度和广度远超本简化版。
        """
        other_powers = [p for p in self.game.powers if p != self.power]
        current_state = self.game.get_state()

        best_action = None
        best_value = float('-inf')

        my_actions = self.get_possible_actions(self.power, current_state)

        for a in my_actions:
            # 假设其他势力都采取最不利（对抗）的行动
            worst_value = float('inf')

            # 简化：对每个对手，只采样其"最对抗"的单个行动
            # 真实实现应遍历所有对手行动组合（笛卡尔积），但计算量爆炸
            opp_actions_lists = []
            for op in other_powers:
                opp_actions = self.get_possible_actions(op, current_state)
                if opp_actions:
                    # 对手按"对我方最不利"排序，取第一个（最对抗的行动）
                    opp_actions.sort(key=lambda x: self._simulate_and_evaluate(current_state, [a] + [x]))
                    opp_actions_lists.append([opp_actions[0]])  # 只保留最对抗的一个
                else:
                    opp_actions_lists.append([])

            # 评估所有对手最对抗行动的组合
            if opp_actions_lists:
                for combo in self._product_sample(opp_actions_lists):
                    value = self._simulate_and_evaluate(current_state, [a] + list(combo))
                    worst_value = min(worst_value, value)
            else:
                worst_value = self._simulate_and_evaluate(current_state, [a])

            # Maximin：选择"最坏情况下最好"的行动
            if worst_value > best_value:
                best_value = worst_value
                best_action = a

        return best_action, best_value

    def _product_sample(self, lists: List[List[Action]]) -> List[Tuple[Action, ...]]:
        """笛卡尔积采样（简化）
        
        参数:
            lists: 每个对手的行动列表（已筛选为最对抗的少数行动）
        
        返回:
            所有行动组合的列表
        
        说明：
            标准笛卡尔积：若每个对手有 N 个行动，M 个对手共 N^M 种组合。
            本实现中每个对手只保留 1 个最对抗行动，所以组合数 = 1。
            保留此函数是为了支持未来扩展（如保留 top-k 对手行动）。
        """
        if not lists or any(not l for l in lists):
            return [()]
        result = [(a,) for a in lists[0]]
        for lst in lists[1:]:
            new_result = []
            for r in result:
                for a in lst:
                    new_result.append(r + (a,))
            result = new_result
        return result

    def _simulate_and_evaluate(self, state: Dict, actions: List[Action]) -> float:
        """模拟行动并评估结果状态
        
        参数:
            state: 当前游戏状态
            actions: 要模拟执行的行动列表
        
        返回:
            模拟后状态的评估值
        
        说明：
            这是一个"快速模拟"，不调用完整游戏引擎的 resolve_moves()，
            而是直接更新单位位置（假设 MOVE 成功）并评估。
            用于 Minimax 搜索中的快速评估，牺牲准确性换取速度。
        
        注意：此简化模拟不处理冲突（假设所有 MOVE 都成功），
        因此评估值是"乐观估计"，真实结果可能更差。
        """
        # 创建临时状态（深拷贝避免修改原状态）
        sim_ownership = dict(state.get("ownership", {}))
        sim_units = dict(state.get("units", {}))

        # 简化模拟：直接应用 MOVE 行动（假设成功）
        for a in actions:
            if a.action_type == ActionType.MOVE:
                sim_units[a.power] = a.target
                sim_ownership[a.target] = a.power

        sim_state = {"units": sim_units, "ownership": sim_ownership}
        return self.evaluate_state(sim_state)

    def get_best_action(self, commitments: Dict = None) -> Action:
        """获取最佳行动（结合承诺）
        
        参数:
            commitments: {power: territory} 表示承诺支持该势力在该领土
                        本简化版本中未实际使用，保留接口供扩展
        
        返回:
            最优 Action 对象
        
        说明：
            当前实现忽略 commitments，直接返回 minimax_plan 的结果。
            扩展方向：可在 minimax 前检查 commitments，若存在未兑现的承诺，
            强制选择 SUPPORT 行动或调整评估函数。
        """
        action, value = self.minimax_plan(depth=2)
        if action is None:
            # 后备策略：若 minimax 失败（无合法行动），默认 HOLD
            action = Action(self.power, ActionType.HOLD, self.game.units.get(self.power, "T1"))
        return action


# ============================================================
# 5. 意图过滤（Intent Filter）
# ============================================================

class IntentFilter:
    """
    Cicero 的关键创新：确保承诺与行动一致
    防止"说一套做一套"
    
    核心机制：
      - 在消息发送前，检查消息中的承诺是否能被计划行动兑现
      - 若不能兑现，拦截该消息（不发送）
    
    为什么需要意图过滤？
      在 Diplomacy 中，信誉是长期资产。频繁违约会导致其他玩家不再信任你，
      即使短期获利，长期也会因被孤立而失败。意图过滤强制 Agent 保持言行一致，
      维护长期信誉。
    """

    def __init__(self, strategic_module: StrategicModule):
        """初始化意图过滤器
        
        参数:
            strategic_module: 战略模块实例（用于获取游戏状态）
        """
        self.strategic = strategic_module
        self.power = strategic_module.power

    def check_commitment(self, message: Message, planned_action: Action) -> bool:
        """检查消息中的承诺是否与计划行动一致
        
        参数:
            message: 要发送的消息
            planned_action: 战略模块计划执行的行动
        
        返回:
            True = 一致（可以发送），False = 矛盾（应拦截）
        
        检查规则：
          - promise_support: planned_action 必须是 SUPPORT，且支持正确的目标
          - propose_attack: planned_action 必须是 MOVE，且目标在消息指定的领土中
          - accept: 总是允许（接受合作不需要特定行动）
          - 其他类型：默认允许
        """
        if message.msg_type == "promise_support":
            # 检查 planned_action 是否是 SUPPORT 且指向正确的目标
            if planned_action.action_type != ActionType.SUPPORT:
                return False
            # 检查是否支持了正确的攻击目标
            if planned_action.support_against not in message.territories:
                return False
            # 检查是否支持了正确的势力（通过位置推断）
            if message.target_power and planned_action.support_target != self.game.units.get(message.target_power):
                return False
            return True

        elif message.msg_type == "propose_attack":
            # 检查 planned_action 是否包含 MOVE 向目标领土
            if planned_action.action_type != ActionType.MOVE:
                return False
            if planned_action.target not in message.territories:
                return False
            return True

        elif message.msg_type == "accept":
            # 接受不需要行动检查，但更新信念
            return True

        # 其他消息类型（threat, reject 等）默认允许（不涉及具体承诺）
        return True

    def filter_outgoing_messages(self, messages: List[Message],
                                  planned_action: Action) -> List[Message]:
        """过滤掉与计划不一致的承诺
        
        参数:
            messages: 待发送的消息列表
            planned_action: 战略模块计划执行的行动
        
        返回:
            过滤后的消息列表（只保留与计划一致的）
        
        说明：
            这是 Cicero 架构的核心安全阀。没有意图过滤，Agent 可能为了谈判优势
            做出虚假承诺（如承诺支持但实际 MOVE 离开），短期内可能获利，
            但长期会破坏信誉，导致其他玩家不再与其合作。
        """
        filtered = []
        for msg in messages:
            if self.check_commitment(msg, planned_action):
                filtered.append(msg)
            else:
                print(f"  [INTENT FILTER] {self.power}: 过滤矛盾承诺 -> {msg.msg_type}")
        return filtered


# ============================================================
# 6. Cicero Agent（整合）
# ============================================================

class CiceroAgent:
    """
    Cicero 简化版 Agent
    整合语言模块 + 战略模块 + 意图过滤
    
    决策流程（每轮）：
      1. 战略模块计算最优行动（基于当前棋局）
      2. 语言模块生成谈判消息（基于战略目标和信任度）
      3. 意图过滤拦截无法兑现的承诺
      4. 发送过滤后的消息
      5. 执行战略行动
    
    内部状态：
      - trust: {power: float} 对其他势力的信任度（-1.0 到 1.0）
      - beliefs: 收到的消息历史
      - commitments: 我做出的承诺记录
    """

    def __init__(self, power: str, game: DiplomacyGame):
        """初始化 Agent
        
        参数:
            power: Agent 所属的势力
            game: DiplomacyGame 实例
        """
        self.power = power
        self.game = game

        # 初始化三个核心模块
        self.language = LanguageModule(power)
        self.strategic = StrategicModule(power, game)
        self.intent_filter = IntentFilter(self.strategic)
        self.intent_filter.game = game  # 给意图过滤器提供游戏状态引用

        # 内部状态
        self.trust: Dict[str, float] = {p: 0.0 for p in game.powers if p != power}
        self.beliefs: List[Dict] = []  # 收到的消息信念历史
        self.commitments: Dict[str, str] = {}  # 我做出的承诺 {receiver: msg_type}

    def receive_messages(self, messages: List[Message]):
        """接收并解析谈判消息，更新信任度
        
        参数:
            messages: 收到的消息列表
        
        说明：
            只处理 receiver 为自己的消息。解析后更新对应发送方的信任度，
            信任度范围 [-1.0, 1.0]，使用 clamp 防止越界。
        """
        for msg in messages:
            if msg.receiver == self.power:
                belief = self.language.parse_incoming(msg)
                self.beliefs.append(belief)
                # 更新信任度：累加 trust_delta，并限制在 [-1.0, 1.0]
                sender = belief["sender"]
                self.trust[sender] = max(-1.0, min(1.0,
                    self.trust.get(sender, 0.0) + belief["trust_delta"]))
                print(f"  [{self.power}] 收到 {sender} 消息: {msg.msg_type} "
                      f"(信任度: {self.trust[sender]:.1f})")

    def generate_negotiations(self) -> List[Message]:
        """生成谈判消息（策略驱动）
        
        返回:
            要发送的消息列表
        
        策略逻辑：
          - 如果落后（领土 < 最大值）：提议与最弱者结盟，共同攻击最强者
          - 如果领先（领土 >= 最大值）：威胁其他所有势力
        
        这是简化版策略。真实 Cicero 会基于 LLM 生成更复杂的谈判文本，
        并考虑更多因素（如历史关系、长期收益等）。
        """
        messages = []
        other_powers = [p for p in self.game.powers if p != self.power]

        # 计算当前各势力领土数
        my_count = sum(1 for o in self.game.ownership.values() if o == self.power)
        threats = {}
        for p in other_powers:
            threats[p] = sum(1 for o in self.game.ownership.values() if o == p)

        # 策略 1：如果落后，提议结盟攻击最强者（"敌人的敌人是朋友"）
        if my_count < max(threats.values(), default=0):
            strongest = max(threats, key=threats.get)
            weakest = min(threats, key=threats.get)
            if weakest != self.power and weakest != strongest:
                # 向最弱者提议结盟
                msg = self.language.generate_message(
                    weakest, "propose_alliance",
                    target_power=strongest,
                    territories=[self.game.units.get(strongest, "")]
                )
                messages.append(msg)
                # 同时承诺支持（增加结盟吸引力）
                adj = self.game.get_adjacent(self.game.units.get(strongest, ""))
                if adj:
                    msg2 = self.language.generate_message(
                        weakest, "promise_support",
                        territories=[adj.pop()]
                    )
                    messages.append(msg2)
        else:
            # 策略 2：如果领先，威胁所有人（"威慑策略"）
            for p in other_powers:
                msg = self.language.generate_message(
                    p, "threat",
                    target_power=min(other_powers, key=lambda x: threats.get(x, 0))
                )
                messages.append(msg)

        return messages

    def plan_action(self) -> Action:
        """战略模块选择行动"""
        return self.strategic.get_best_action(self.commitments)

    def act(self, round_num: int) -> Action:
        """完整决策流程：谈判 -> 意图过滤 -> 行动
        
        参数:
            round_num: 当前轮数（用于日志输出）
        
        返回:
            最终执行的行动
        
        执行顺序：
          1. 先由战略模块计划行动（"做什么"）
          2. 再由语言模块生成消息（"说什么"）
          3. 意图过滤确保"说做一致"
          4. 记录承诺并输出
        
        关键设计：先计划行动，再生成消息。这确保了意图过滤的有效性——
        如果反过来（先生成消息再计划行动），Agent 可能被自己的承诺绑架。
        """
        print(f"\n--- {self.power} 的回合 ---")

        # 1. 先计划行动（基于战略，不考虑语言）
        planned_action = self.plan_action()
        print(f"  [{self.power}] 战略计划: {planned_action}")

        # 2. 生成谈判消息（基于战略目标）
        negotiations = self.generate_negotiations()

        # 3. 意图过滤：拦截与计划不一致的承诺
        filtered = self.intent_filter.filter_outgoing_messages(negotiations, planned_action)

        # 4. 记录承诺（用于未来回合的信誉追踪）
        for msg in filtered:
            if msg.msg_type in ("promise_support", "propose_attack"):
                self.commitments[msg.receiver] = msg.msg_type

        # 5. 输出（在完整系统中会通过网络发送给其他 Agent）
        for msg in filtered:
            print(f"  [{self.power}] 发送: {msg}")

        return planned_action


# ============================================================
# 7. 模拟主循环
# ============================================================

def run_simulation(max_rounds: int = 10) -> None:
    """运行完整模拟
    
    参数:
        max_rounds: 最大轮数（默认 10 轮）
    
    模拟流程：
      1. 初始化游戏和 Agent
      2. 每轮循环：谈判阶段 → 决策阶段 → 执行阶段
      3. 检查胜利条件（控制 >=3 领土）
      4. 输出最终结果
    """
    print("=" * 60)
    print("Cicero 风格谈判 Agent 实验")
    print("简化版 Diplomacy 模拟")
    print("=" * 60)

    # 初始化游戏
    game = DiplomacyGame(powers=["A", "B", "C"])
    print(f"\n初始状态:\n{game}")

    # 创建三个 Agent
    agents = {
        "A": CiceroAgent("A", game),
        "B": CiceroAgent("B", game),
        "C": CiceroAgent("C", game),
    }

    # 主循环
    for round_num in range(1, max_rounds + 1):
        print(f"\n{'=' * 50}")
        print(f"ROUND {round_num}")
        print(f"{'=' * 50}")

        # --- 谈判阶段 ---
        # 所有 Agent 同时生成谈判消息，然后统一分发
        print("\n[谈判阶段]")
        all_messages = []
        for power, agent in agents.items():
            msgs = agent.generate_negotiations()
            # 注意：这里的消息还未经过意图过滤，过滤在 act() 中进行
            all_messages.extend(msgs)

        # 分发消息给接收方
        for msg in all_messages:
            if msg.receiver in agents:
                agents[msg.receiver].receive_messages([msg])

        # --- 决策阶段 ---
        # 每个 Agent 执行完整决策流程（计划 + 谈判 + 过滤）
        print("\n[决策阶段]")
        actions = []
        for power, agent in agents.items():
            action = agent.act(round_num)
            actions.append(action)

        # --- 执行阶段 ---
        # 同时结算所有行动
        print(f"\n[执行阶段]")
        for a in actions:
            print(f"  {a}")

        game.resolve_moves(actions)
        print(f"\n{game}")

        # 检查胜利条件
        winner = game.check_winner()
        if winner:
            print(f"\n🏆 势力 {winner} 获胜！")
            break

    # 最终结果统计
    print(f"\n{'=' * 50}")
    print("模拟结束")
    print(f"{'=' * 50}")
    final_counts = defaultdict(int)
    for t, owner in game.ownership.items():
        if owner:
            final_counts[owner] += 1
    print(f"最终领土控制: {dict(final_counts)}")
    print(f"总轮数: {game.round}")


# ============================================================
# 8. 运行
# ============================================================

if __name__ == "__main__":
    # 设置随机种子保证可复现（可选）
    # 固定种子后，每次运行结果相同，便于调试和对比实验
    random.seed(42)
    run_simulation(max_rounds=10)
```

---

## 4. 实验运行示例

运行上述代码，预期输出如下结构：

```
============================================================
Cicero 风格谈判 Agent 实验
简化版 Diplomacy 模拟
============================================================

初始状态:
=== Round 0 ===
Units: {'A': 'T1', 'B': 'T3', 'C': 'T5'}
Ownership: {'T1': 'A', 'T3': 'B', 'T5': 'C', ...}

==================================================
ROUND 1
==================================================

[谈判阶段]
  [B] 收到 A 消息: propose_alliance (信任度: 0.2)
  [C] 收到 A 消息: propose_alliance (信任度: 0.2)
  ...

[决策阶段]

--- A 的回合 ---
  [A] 战略计划: A: MOVE -> T2
  [A] 发送: [A->B] propose_alliance: A 提议与 B 结盟...
  [A] 发送: [A->C] propose_alliance: A 提议与 C 结盟...

[执行阶段]
  A: MOVE -> T2
  B: MOVE -> T2
  C: HOLD T5

=== Round 1 ===
Units: {'A': 'T1', 'B': 'T3', 'C': 'T5'}  // 冲突导致都失败
Ownership: ...

... 多轮后 ...

🏆 势力 X 获胜！
```

---

## 5. 评估指标详解

本实验虽然没有传统 ML 实验的"准确率"等指标，但可以从博弈论和 Agent 设计角度定义以下评估维度：

### 5.1 胜率（Win Rate）

- **指标名称**: Agent 在多轮模拟中的获胜比例
  - **定义**: $\text{WinRate} = \frac{\text{获胜次数}}{\text{总模拟次数}}$
  - **示例**: 运行 100 次模拟，A 获胜 35 次 → WinRate(A) = 35%
  - **为什么用**: 衡量 Agent 策略的整体有效性，是博弈 AI 的核心指标
  - **局限性**: 
    - 样本量小时方差大（100 次模拟可能不够）
    - 三方博弈中，胜率受初始位置和随机性影响（A 靠近中心 T2 有地理优势）
    - 无法区分"策略优秀"和"运气成分"

### 5.2 承诺兑现率（Commitment Fulfillment Rate）

- **指标名称**: Agent 做出的承诺中被实际执行的比例
  - **定义**: $\text{FulfillmentRate} = \frac{\text{兑现的承诺数}}{\text{总承诺数}}$
  - **示例**: Agent 发送了 10 条 promise_support，其中 8 条与最终行动一致 → FulfillmentRate = 80%
  - **为什么用**: 直接衡量意图过滤的有效性，是 Cicero 架构的核心创新指标
  - **局限性**: 
    - 100% 兑现不一定是好事——有时战略需要改变，严格兑现可能错过更好机会
    - 本实验强制 100% 兑现（意图过滤拦截所有矛盾承诺），无法测试"策略性违约"的影响
    - 无法衡量"隐性承诺"（如结盟暗示但未明确承诺）

### 5.3 信任度收敛性（Trust Convergence）

- **指标名称**: Agent 间信任度是否随交互趋于稳定
  - **定义**: 测量相邻轮次信任度变化的方差：$\text{TrustStability} = 1 - \frac{\sum_{t} |\text{trust}_t - \text{trust}_{t-1}|}{T}$
  - **示例**: 若 Agent A 对 B 的信任度在 10 轮中从 0.0 → 0.2 → 0.2 → 0.2...，则稳定性高
  - **为什么用**: 信任度剧烈波动表明 Agent 策略不一致或环境过于随机，稳定信任是长期合作的基础
  - **局限性**: 
    - 信任度是内部状态，无法直接观察（需要日志记录）
    - 稳定信任不等于"正确信任"——Agent 可能稳定地错误信任一个背叛者
    - 本实验信任更新规则过于简化（固定 delta），无法反映复杂博弈动态

### 5.4 谈判消息有效率（Message Efficiency）

- **指标名称**: 发送的谈判消息中促成有效合作的比例
  - **定义**: $\text{Efficiency} = \frac{\text{导致联盟形成的提议数}}{\text{总提议数}}$
  - **示例**: Agent 发送 20 条 propose_alliance，其中 5 条被对方接受且实际形成合作 → Efficiency = 25%
  - **为什么用**: 衡量语言模块的"说服力"和策略选择的合理性
  - **局限性**: 
    - "有效合作"难以定义——接受结盟但无实际行动是否算有效？
    - 受对手策略影响大（对手可能随机拒绝）
    - 本实验模板生成过于简单，无法体现真实语言说服力

### 5.5 战略-语言一致性（Strategic-Language Alignment）

- **指标名称**: 战略模块输出与语言模块输出的一致性程度
  - **定义**: 意图过滤拦截率：$\text{Alignment} = 1 - \frac{\text{被拦截消息数}}{\text{总生成消息数}}$
  - **示例**: 生成 50 条消息，5 条被拦截 → Alignment = 90%
  - **为什么用**: 直接量化"说一套做一套"的程度，Alignment 越高说明双系统协同越好
  - **局限性**: 
    - 高 Alignment 可能是"语言模块过于保守"（只说安全的话）而非真正协同
    - 拦截率也受战略模块质量影响——若战略模块总是选择 MOVE，则所有 SUPPORT 承诺都会被拦截
    - 无法捕捉"策略性模糊"（故意不承诺以保留灵活性）

---

## 6. 关键概念验证

### 6.1 意图过滤验证

在代码中，当 Agent 计划了 `MOVE -> T2` 但消息中承诺了 `SUPPORT B 在 T3`，**意图过滤会拦截这条消息**。

```
[INTENT FILTER] A: 过滤矛盾承诺 -> promise_support
```

这体现了 Cicero 的核心设计：不做出无法兑现的承诺。

> **深入理解：为什么意图过滤是 Cicero 的关键创新？**
> 
> 在传统端到端对话系统中，语言模型和策略模型是耦合的。语言模型为了"赢得对话"可能做出任意承诺，而策略模型独立决策行动，两者之间没有协调机制。这导致：
> 
> 1. **信誉崩溃**：频繁违约使其他玩家不再信任该 Agent
> 2. **联盟瓦解**：口头协议无法转化为实际合作
> 3. **长期收益损失**：短期欺骗获利，但长期被孤立
> 
> Cicero 的意图过滤强制"承诺先行"——先确定能做什么，再决定说什么。这类似于人类社交中的"三思而后言"，是维护长期合作关系的基础。
> 
> 形式化地，意图过滤确保：
> $$
> \forall m \in \text{Messages}, \quad \text{Filter}(m, a) = \text{True} \implies \text{Commitment}(m) \subseteq \text{Capability}(a)
> $$
> 
> 即：所有发送的消息中的承诺，必须是计划行动能够兑现的子集。

### 6.2 战略 vs 语言的解耦

| 模块 | 输入 | 输出 | 职责 |
|------|------|------|------|
| 语言模块 | 战略目标、信任度 | 谈判文本 | "说什么" |
| 战略模块 | 棋局状态 | 最优行动 | "做什么" |
| 意图过滤 | 语言输出、战略输出 | 过滤后的消息 | "确保说做一致" |

> **设计权衡：解耦 vs 端到端**
> 
> | 架构 | 优点 | 缺点 | 适用场景 |
> |------|------|------|----------|
> | **解耦（Cicero）** | 可解释性强、承诺可控、易于调试 | 模块间信息损失、需要手动设计接口 | 需要长期信誉的博弈 |
> | **端到端** | 信息传递完整、可能发现新策略 | 黑盒、不可控、容易"说一套做一套" | 短期任务、单轮交互 |
> 
> Cicero 选择解耦的核心原因：Diplomacy 是多轮博弈，信誉是长期资产。一个"诚实但稍弱"的 Agent 可能比"强大但欺骗"的 Agent 走得更远，因为其他玩家更愿意与可信的 Agent 结盟。

### 6.3 与真实 Cicero 的对比

| 维度 | 本实验（简化） | 真实 Cicero |
|------|--------------|-------------|
| 语言模型 | 规则+模板 | 70B 参数 LLM |
| 战略规划 | 手动 Minimax | 类似 AlphaZero 的 RL 模型 |
| 意图过滤 | 硬规则检查 | 基于策略模型的概率验证 |
| 谈判复杂度 | 单轮、3势力 | 多轮、7势力、长上下文 |
| 欺骗能力 | 无（强制诚实） | 可控（受伦理约束） |

> **关键洞察**：本实验的"强制诚实"是一个简化假设。真实 Cicero 允许**策略性欺骗**，但有两个约束：
> 1. **概率验证**：意图过滤不是"全有或全无"，而是计算承诺兑现的概率，低于阈值才拦截
> 2. **伦理约束**：Meta 在设计时加入了"不主动背叛"的偏好，避免 Agent 成为"纯欺骗者"
> 
> 这引出了一个深刻的博弈论问题：**在重复博弈中，最优策略是总是诚实、总是欺骗、还是条件性诚实？**
> 
> 根据"以牙还牙"（Tit-for-Tat）策略的研究，在重复囚徒困境中，条件性合作（先合作，之后模仿对方上一轮行为）通常是最优的。Cicero 的意图过滤可以看作是一种"强制合作"机制，确保 Agent 不会主动背叛。

---

## 7. 扩展实验方向

1. **引入 LLM**：将语言模块替换为调用 GPT 或本地 LLM，观察谈判质量变化
2. **欺骗策略**：移除意图过滤，允许 Agent 做出虚假承诺，评估是否提升胜率
3. **记忆系统**：添加长期记忆（Generative Agents 风格），让 Agent 记住历史背叛
4. **多方博弈**：扩展到 5-7 个势力，观察联盟动态
5. **学习机制**：让 Agent 从对局中学习信任/背叛策略（多智能体强化学习）

---

## 8. 配置矩阵与初学者指南

### 8.1 实验配置推荐

| 场景 | 势力数 | 领土数 | 评估深度 | 信任更新 | 意图过滤 | 说明 |
|------|--------|--------|----------|----------|----------|------|
| **入门演示** | 3 | 5 | depth=1 | 固定 delta | 强制开启 | 最快理解核心机制 |
| **标准实验** | 3 | 5 | depth=2 | 固定 delta | 强制开启 | 本实验默认配置 |
| **欺骗对比** | 3 | 5 | depth=2 | 固定 delta | **关闭** | 对比诚实 vs 欺骗策略 |
| **扩展探索** | 5 | 7 | depth=2 | 动态衰减 | 概率过滤 | 更接近真实 Diplomacy |
| **研究级** | 7 | 12 | depth=3 | 神经网络 | 学习过滤 | 需要大量计算资源 |

### 8.2 初学者调试清单

- [ ] **第一步**：运行默认配置（3 势力、5 领土、seed=42），观察输出是否符合预期
- [ ] **第二步**：修改 `territory_values` 权重，观察 Agent 是否优先争夺高价值领土
- [ ] **第三步**：关闭意图过滤（注释掉 `filter_outgoing_messages`），对比胜率变化
- [ ] **第四步**：修改信任度更新规则（如 threat 的 delta 从 -0.3 改为 -0.5），观察联盟稳定性
- [ ] **第五步**：添加日志记录每轮的信任度矩阵，可视化信任演化

### 8.3 常见陷阱

1. **陷阱**：认为"意图过滤会降低胜率"
   - **事实**：短期看，过滤限制了 Agent 的"谈判灵活性"；但长期看，维护信誉带来的联盟收益远超短期欺骗收益
   
2. **陷阱**：认为"Minimax 深度越深越好"
   - **事实**：Diplomacy 是不完美信息博弈，对手行动不可预测。过深的搜索会过度拟合对对手行动的假设，反而降低鲁棒性
   
3. **陷阱**：忽视"同时行动"的特性
   - **事实**：本代码的 `resolve_moves()` 同时结算所有行动，这是 Diplomacy 的核心机制。若改为轮流行动，博弈性质完全改变

---

## 9. 面试要点

- **30 秒**：这个实验演示了 Cicero 的"双系统+意图过滤"架构：语言模块负责谈判，战略模块负责决策，意图过滤确保承诺可兑现。
- **关键问题**：如果移除意图过滤，Agent 的胜率会提升吗？（暗示欺骗 vs 诚实的博弈论问题）
- **数学直觉**：棋局评估函数 V(s) 是手工设计的，在真实 Cicero 中由神经网络拟合，从大量对局数据中学习。
- **深度问题**：为什么 Cicero 选择解耦架构而非端到端？（答：多轮博弈中信誉是长期资产，解耦确保言行一致）

---

*实验编号：13*
*创建时间：2026-07-13*
*维护者：AIResearchVault*
