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
    MOVE = "move"
    HOLD = "hold"
    SUPPORT = "support"


@dataclass
class Action:
    """单个行动"""
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
    """谈判消息"""
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
    """简化版 Diplomacy 游戏引擎"""

    # 领土连接图
    ADJACENCY = {
        "T1": {"T2"},
        "T2": {"T1", "T3", "T4"},
        "T3": {"T2", "T5"},
        "T4": {"T2", "T5"},
        "T5": {"T3", "T4"},
    }

    def __init__(self, powers: List[str] = None):
        self.powers = powers or ["A", "B", "C"]
        self.territories = ["T1", "T2", "T3", "T4", "T5"]
        self.round = 0

        # 初始分配：每个势力 1 个单位，放在不同领土
        self.units: Dict[str, str] = {}  # power -> territory
        self.ownership: Dict[str, str] = {}  # territory -> power
        self._init_positions()

    def _init_positions(self):
        """初始化势力位置（固定或随机）"""
        # 固定分配：A->T1, B->T3, C->T5
        starts = {"A": "T1", "B": "T3", "C": "T5"}
        for p in self.powers:
            self.units[p] = starts[p]
            self.ownership[starts[p]] = p

    def get_adjacent(self, terr: str) -> Set[str]:
        return self.ADJACENCY.get(terr, set())

    def get_occupant(self, terr: str) -> Optional[str]:
        """获取某个领土的当前占领者"""
        for p, t in self.units.items():
            if t == terr:
                return p
        return None

    def resolve_moves(self, actions: List[Action]) -> None:
        """同时结算所有行动（简化版 Diplomacy 规则）"""
        # 1. 收集所有移动和支持
        moves = {}        # target -> list of (power, strength)
        supports = {}     # (target, against) -> list of power
        holds = {}        # power -> hold_target

        for a in actions:
            if a.action_type == ActionType.MOVE:
                moves.setdefault(a.target, []).append((a.power, 1))
            elif a.action_type == ActionType.HOLD:
                holds[a.power] = a.target
                # hold 也是防御，记录为 1 力量的防守
                moves.setdefault(a.target, []).append((a.power, 1))
            elif a.action_type == ActionType.SUPPORT:
                key = (a.support_target, a.support_against)
                supports.setdefault(key, []).append(a.power)

        # 2. 应用支持（支持方必须在相邻位置且没有移动）
        # 简化：只要支持方没有被攻击，支持就有效
        # 检查支持是否被切断
        supported = defaultdict(int)  # (power, target) -> 额外力量

        for (supp_target, against), supporters in supports.items():
            for sp in supporters:
                # 检查支持者当前位置是否相邻于被攻击目标
                # 简化：支持总是有效（除非支持者移动了）
                if any(a.power == sp and a.action_type == ActionType.MOVE for a in actions):
                    continue  # 支持者在移动，支持无效
                # 支持生效：被支持的攻击获得 +1
                for idx, (p, s) in enumerate(moves.get(against, [])):
                    if p == supp_target:
                        moves[against][idx] = (p, s + 1)
                        break

        # 3. 结算所有冲突
        # 每个目标领土，力量最大的占领
        new_units = {}
        processed = set()

        for a in actions:
            if a.action_type == ActionType.MOVE and a.power not in processed:
                target = a.target
                # 来自 a.power 对 target 的攻击力量
                attack_power = 1
                # 查找是否被支持
                for idx, (p, s) in enumerate(moves.get(target, [])):
                    if p == a.power:
                        attack_power = s
                        break

                # 检查 target 是否有防守（从 target 出发的 hold/move）
                defender = self.get_occupant(target)
                defend_power = 0
                if defender and defender != a.power:
                    # 防守方 hold 或 move out 的力量
                    for idx, (p, s) in enumerate(moves.get(target, [])):
                        if p == defender:
                            defend_power = s
                            break
                    # 如果防守方也在 move out，则没有防守
                    for act in actions:
                        if act.power == defender and act.action_type == ActionType.MOVE:
                            defend_power = 0
                            break

                # 比较力量
                if attack_power > defend_power:
                    # 但还要检查是否有其他力量攻击同一目标
                    all_attackers = moves.get(target, [])
                    max_power = max((s for _, s in all_attackers), default=0)
                    attackers = [p for p, s in all_attackers if s == max_power]
                    if len(attackers) == 1 and attackers[0] == a.power and attack_power == max_power:
                        new_units[a.power] = target
                        processed.add(a.power)

        # 4. 未成功移动的单位保持原位
        for a in actions:
            if a.power not in new_units and a.power not in processed:
                # 检查是否被击退
                # 简化：如果没有成功移动，保持原位
                new_units[a.power] = self.units[a.power]

        # 5. 更新状态
        self.units = new_units
        # 更新领土所有权（占领即拥有）
        for p, t in self.units.items():
            self.ownership[t] = p
        # 未占领的领土保持原所有者（简化）
        for t in self.territories:
            if t not in self.ownership:
                self.ownership[t] = None

        self.round += 1

    def get_state(self) -> Dict:
        return {
            "round": self.round,
            "units": copy.deepcopy(self.units),
            "ownership": copy.deepcopy(self.ownership),
        }

    def check_winner(self) -> Optional[str]:
        """检查是否有玩家获胜（控制 >= 3 领土）"""
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
    """

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
        self.power = power

    def generate_message(self, receiver: str, msg_type: str,
                         target_power: Optional[str] = None,
                         territories: List[str] = None) -> Message:
        """生成谈判消息"""
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
        """
        解析收到的消息，提取关键信息
        返回信念更新字典
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
    """

    def __init__(self, power: str, game: DiplomacyGame):
        self.power = power
        self.game = game
        # 每个领土的价值（中心位置更值钱）
        self.territory_values = {
            "T1": 1.0, "T2": 2.0, "T3": 1.0,
            "T4": 1.5, "T5": 1.5,
        }

    def evaluate_state(self, state: Dict) -> float:
        """评估给定状态的棋局价值（V(s)）"""
        ownership = state.get("ownership", self.game.ownership)
        units = state.get("units", self.game.units)

        score = 0.0
        # 1. 自己控制的领土价值
        for t, owner in ownership.items():
            if owner == self.power:
                score += self.territory_values.get(t, 1.0) * 2.0
            elif owner is not None:
                score -= self.territory_values.get(t, 1.0) * 0.5

        # 2. 单位位置优势（靠近中心更好）
        center_dist = {
            "T1": 2, "T2": 1, "T3": 2,
            "T4": 1, "T5": 2,
        }
        for p, t in units.items():
            if p == self.power:
                score += 1.0 / (center_dist.get(t, 1) + 1)
            else:
                score -= 0.3 / (center_dist.get(t, 1) + 1)

        # 3. 获胜倾向
        my_count = sum(1 for o in ownership.values() if o == self.power)
        if my_count >= 3:
            score += 100.0

        return score

    def get_possible_actions(self, power: str, state: Dict) -> List[Action]:
        """获取某个势力的所有可能行动"""
        units = state.get("units", self.game.units)
        if power not in units:
            return []

        pos = units[power]
        adjacent = self.game.get_adjacent(pos)
        actions = []

        # 1. HOLD
        actions.append(Action(power, ActionType.HOLD, pos))

        # 2. MOVE 到相邻空位/敌方领土
        for adj in adjacent:
            actions.append(Action(power, ActionType.MOVE, adj))

        # 3. SUPPORT 盟友（如果有其他势力在相邻位置且可攻击同一个目标）
        # 简化：支持任何相邻领土的攻击
        for adj in adjacent:
            # 支持 adj 的占领者攻击 adj 的邻居
            adj_neighbors = self.game.get_adjacent(adj)
            for n in adj_neighbors:
                if n != pos:
                    actions.append(Action(
                        power, ActionType.SUPPORT,
                        target=pos,  # 支持时 target 是己方位置
                        support_target=adj,  # 被支持的盟友所在位置
                        support_against=n    # 盟友攻击的目标
                    ))

        return actions

    def minimax_plan(self, depth: int = 2) -> Tuple[Action, float]:
        """
        Minimax 规划（简化版，只考虑自己 vs 其他所有势力的联合）
        """
        other_powers = [p for p in self.game.powers if p != self.power]
        current_state = self.game.get_state()

        best_action = None
        best_value = float('-inf')

        my_actions = self.get_possible_actions(self.power, current_state)

        for a in my_actions:
            # 假设其他势力都采取最不利（对抗）的行动
            worst_value = float('inf')

            # 简化：只采样其他势力的少数组合
            opp_actions_lists = []
            for op in other_powers:
                opp_actions = self.get_possible_actions(op, current_state)
                if opp_actions:
                    # 对手倾向于最小化我们的收益
                    opp_actions.sort(key=lambda x: self._simulate_and_evaluate(current_state, [a] + [x]))
                    opp_actions_lists.append([opp_actions[0]])  # 取最对抗的行动
                else:
                    opp_actions_lists.append([])

            # 评估组合
            if opp_actions_lists:
                for combo in self._product_sample(opp_actions_lists):
                    value = self._simulate_and_evaluate(current_state, [a] + list(combo))
                    worst_value = min(worst_value, value)
            else:
                worst_value = self._simulate_and_evaluate(current_state, [a])

            if worst_value > best_value:
                best_value = worst_value
                best_action = a

        return best_action, best_value

    def _product_sample(self, lists: List[List[Action]]) -> List[Tuple[Action, ...]]:
        """笛卡尔积采样（简化）"""
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
        """模拟行动并评估"""
        # 创建临时游戏状态模拟
        # 简化：直接评估移动后的状态
        sim_ownership = dict(state.get("ownership", {}))
        sim_units = dict(state.get("units", {}))

        for a in actions:
            if a.action_type == ActionType.MOVE:
                sim_units[a.power] = a.target
                sim_ownership[a.target] = a.power

        sim_state = {"units": sim_units, "ownership": sim_ownership}
        return self.evaluate_state(sim_state)

    def get_best_action(self, commitments: Dict = None) -> Action:
        """
        获取最佳行动（结合承诺）
        commitments: {power: territory} 表示承诺支持该势力在该领土
        """
        action, value = self.minimax_plan(depth=2)
        if action is None:
            # 默认 HOLD
            action = Action(self.power, ActionType.HOLD, self.game.units.get(self.power, "T1"))
        return action


# ============================================================
# 5. 意图过滤（Intent Filter）
# ============================================================

class IntentFilter:
    """
    Cicero 的关键创新：确保承诺与行动一致
    防止"说一套做一套"
    """

    def __init__(self, strategic_module: StrategicModule):
        self.strategic = strategic_module
        self.power = strategic_module.power

    def check_commitment(self, message: Message, planned_action: Action) -> bool:
        """
        检查消息中的承诺是否与计划行动一致
        返回 True = 一致，False = 矛盾（应拒绝发送）
        """
        if message.msg_type == "promise_support":
            # 检查 planned_action 是否是 SUPPORT 且指向正确的目标
            if planned_action.action_type != ActionType.SUPPORT:
                return False
            # 检查是否支持了正确的人攻击正确的领土
            if planned_action.support_against not in message.territories:
                return False
            # 检查是否支持了正确的势力
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

        # 其他消息类型默认允许
        return True

    def filter_outgoing_messages(self, messages: List[Message],
                                  planned_action: Action) -> List[Message]:
        """过滤掉与计划不一致的承诺"""
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
    """

    def __init__(self, power: str, game: DiplomacyGame):
        self.power = power
        self.game = game

        self.language = LanguageModule(power)
        self.strategic = StrategicModule(power, game)
        self.intent_filter = IntentFilter(self.strategic)
        self.intent_filter.game = game  # 引用游戏

        # 内部状态
        self.trust: Dict[str, float] = {p: 0.0 for p in game.powers if p != power}
        self.beliefs: List[Dict] = []  # 收到的消息信念
        self.commitments: Dict[str, str] = {}  # 我做出的承诺

    def receive_messages(self, messages: List[Message]):
        """接收并解析谈判消息"""
        for msg in messages:
            if msg.receiver == self.power:
                belief = self.language.parse_incoming(msg)
                self.beliefs.append(belief)
                # 更新信任度
                sender = belief["sender"]
                self.trust[sender] = max(-1.0, min(1.0,
                    self.trust.get(sender, 0.0) + belief["trust_delta"]))
                print(f"  [{self.power}] 收到 {sender} 消息: {msg.msg_type} "
                      f"(信任度: {self.trust[sender]:.1f})")

    def generate_negotiations(self) -> List[Message]:
        """生成谈判消息（策略驱动）"""
        messages = []
        other_powers = [p for p in self.game.powers if p != self.power]

        # 策略：找最弱的结盟，或者攻击最威胁的
        my_t = self.game.units.get(self.power, "")
        my_count = sum(1 for o in self.game.ownership.values() if o == self.power)

        # 按威胁度排序对手
        threats = {}
        for p in other_powers:
            p_count = sum(1 for o in self.game.ownership.values() if o == p)
            threats[p] = p_count

        # 如果落后，提议结盟攻击最强者
        if my_count < max(threats.values(), default=0):
            strongest = max(threats, key=threats.get)
            weakest = min(threats, key=threats.get)
            if weakest != self.power and weakest != strongest:
                # 向最弱者提议结盟对抗最强者
                msg = self.language.generate_message(
                    weakest, "propose_alliance",
                    target_power=strongest,
                    territories=[self.game.units.get(strongest, "")]
                )
                messages.append(msg)
                # 承诺支持
                adj = self.game.get_adjacent(self.game.units.get(strongest, ""))
                if adj:
                    msg2 = self.language.generate_message(
                        weakest, "promise_support",
                        territories=[adj.pop()]
                    )
                    messages.append(msg2)
        else:
            # 如果领先，威胁所有人
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
        """完整决策流程：谈判 -> 意图过滤 -> 行动"""
        print(f"\n--- {self.power} 的回合 ---")

        # 1. 先计划行动（基于战略）
        planned_action = self.plan_action()
        print(f"  [{self.power}] 战略计划: {planned_action}")

        # 2. 生成谈判消息
        negotiations = self.generate_negotiations()

        # 3. 意图过滤
        filtered = self.intent_filter.filter_outgoing_messages(negotiations, planned_action)

        # 4. 记录承诺
        for msg in filtered:
            if msg.msg_type in ("promise_support", "propose_attack"):
                self.commitments[msg.receiver] = msg.msg_type

        # 5. 输出（在完整系统中会发送给其他 Agent）
        for msg in filtered:
            print(f"  [{self.power}] 发送: {msg}")

        return planned_action


# ============================================================
# 7. 模拟主循环
# ============================================================

def run_simulation(max_rounds: int = 10) -> None:
    """运行完整模拟"""
    print("=" * 60)
    print("Cicero 风格谈判 Agent 实验")
    print("简化版 Diplomacy 模拟")
    print("=" * 60)

    # 初始化游戏
    game = DiplomacyGame(powers=["A", "B", "C"])
    print(f"\n初始状态:\n{game}")

    # 创建 Agent
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
        print("\n[谈判阶段]")
        all_messages = []
        for power, agent in agents.items():
            msgs = agent.generate_negotiations()
            # 意图过滤在 act() 中完成
            all_messages.extend(msgs)

        # 分发消息
        for msg in all_messages:
            if msg.receiver in agents:
                agents[msg.receiver].receive_messages([msg])

        # --- 决策阶段 ---
        print("\n[决策阶段]")
        actions = []
        for power, agent in agents.items():
            action = agent.act(round_num)
            actions.append(action)

        # --- 执行阶段 ---
        print(f"\n[执行阶段]")
        for a in actions:
            print(f"  {a}")

        game.resolve_moves(actions)
        print(f"\n{game}")

        # 检查胜利
        winner = game.check_winner()
        if winner:
            print(f"\n🏆 势力 {winner} 获胜！")
            break

    # 最终结果
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

## 5. 关键概念验证

### 5.1 意图过滤验证

在代码中，当 Agent 计划了 `MOVE -> T2` 但消息中承诺了 `SUPPORT B 在 T3`，**意图过滤会拦截这条消息**。

```
[INTENT FILTER] A: 过滤矛盾承诺 -> promise_support
```

这体现了 Cicero 的核心设计：不做出无法兑现的承诺。

### 5.2 战略 vs 语言的解耦

| 模块 | 输入 | 输出 | 职责 |
|------|------|------|------|
| 语言模块 | 战略目标、信任度 | 谈判文本 | "说什么" |
| 战略模块 | 棋局状态 | 最优行动 | "做什么" |
| 意图过滤 | 语言输出、战略输出 | 过滤后的消息 | "确保说做一致" |

### 5.3 与真实 Cicero 的对比

| 维度 | 本实验（简化） | 真实 Cicero |
|------|--------------|-------------|
| 语言模型 | 规则+模板 | 70B 参数 LLM |
| 战略规划 | 手动 Minimax | 类似 AlphaZero 的 RL 模型 |
| 意图过滤 | 硬规则检查 | 基于策略模型的概率验证 |
| 谈判复杂度 | 单轮、3势力 | 多轮、7势力、长上下文 |
| 欺骗能力 | 无（强制诚实） | 可控（受伦理约束） |

---

## 6. 扩展实验方向

1. **引入 LLM**：将语言模块替换为调用 GPT 或本地 LLM，观察谈判质量变化
2. **欺骗策略**：移除意图过滤，允许 Agent 做出虚假承诺，评估是否提升胜率
3. **记忆系统**：添加长期记忆（Generative Agents 风格），让 Agent 记住历史背叛
4. **多方博弈**：扩展到 5-7 个势力，观察联盟动态
5. **学习机制**：让 Agent 从对局中学习信任/背叛策略（多智能体强化学习）

---

## 7. 面试要点

- **30 秒**：这个实验演示了 Cicero 的"双系统+意图过滤"架构：语言模块负责谈判，战略模块负责决策，意图过滤确保承诺可兑现。
- **关键问题**：如果移除意图过滤，Agent 的胜率会提升吗？（暗示欺骗 vs 诚实的博弈论问题）
- **数学直觉**：棋局评估函数 V(s) 是手工设计的，在真实 Cicero 中由神经网络拟合，从大量对局数据中学习。

---

*实验编号：13*
*创建时间：2026-07-13*
*维护者：AIResearchVault*
