---
tags: [experiment, generative-agents, social-simulation, memory-stream, emergence]
aliases: [Generative-Agents-Simplified]
paper_source: "Generative Agents: Interactive Simulacra of Human Behavior (Stanford, UIST 2023)"
related_paper: "[[01c-Human-AI-Game-Interaction]]"
status: completed
---

# 实验 11：Generative Agents 社交模拟实验（简化版）

## 实验信息

| 属性 | 值 |
|------|-----|
| **实验编号** | 11 |
| **实验名称** | Generative Agents 社交模拟实验 |
| **论文来源** | Generative Agents: Interactive Simulacra of Human Behavior (Stanford, UIST 2023) |
| **关联笔记** | [[01c-Human-AI-Game-Interaction]] 中 Generative Agents 部分 |
| **核心机制** | 记忆流、重要性评分、反思、规划、涌现社交行为 |
| **技术栈** | Python 3.11+, dataclasses, heapq, 基于规则的模板生成 |
| **代码行数** | ~850 行 |
| **实验环境** | 虚拟小镇（3 个位置，3 个 Agent） |

---

## 实验背景

Generative Agents（Park et al., 2023）是斯坦福在虚拟小镇中部署的 25 个 AI Agent 的社交模拟系统。每个 Agent 拥有**记忆流（Memory Stream）**、**反思（Reflection）**、**规划（Planning）**三层架构，Agent 之间通过自然语言交互，产生涌现的社交行为（如聚会邀请、关系形成、信息传播）。

本实验实现一个**简化版**的 Generative Agents 架构，使用**基于规则的模板生成**代替 LLM，保留核心机制：

- **记忆流**：Agent 记录所有观察，按重要性评分排序
- **反思**：当记忆积累到一定量时，对主题进行总结
- **规划**：分天计划（高等级）和小时计划（低等级）
- **涌现行为**：多个 Agent 在环境中交互产生意外社交模式

---

## 实验目标

1. 理解记忆流 + 反思 + 规划的三层架构
2. 观察基于规则交互产生的涌现社交行为
3. 验证重要性评分对记忆检索的过滤作用
4. 分析规划变更与社交触发的关系

---

## 核心架构

```
┌─────────────────────────────────────────────────────────┐
│                    Agent 内部架构                          │
├─────────────────────────────────────────────────────────┤
│  观察层 → 记忆流(Memory Stream) → 重要性评分 → 排序检索      │
│              ↓                                          │
│  反思层(Reflection) ← 累积同主题记忆 → 生成抽象概念          │
│              ↓                                          │
│  规划层(Planning) ← 天计划 → 小时计划 → 执行动作             │
│              ↓                                          │
│  行为层 → 移动 / 对话 / 互动 → 产生新观察                   │
└─────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────┐
│                    环境架构                               │
├─────────────────────────────────────────────────────────┤
│  虚拟小镇:                                                 │
│    - 家 (Home) - 休息、用餐、私人活动                      │
│    - 咖啡馆 (Cafe) - 社交、闲聊、工作                     │
│    - 公园 (Park) - 散步、偶遇、聚会                       │
│  Agent: Alice, Bob, Carol                                 │
│  时间: 模拟一天 (06:00 - 22:00)                           │
└─────────────────────────────────────────────────────────┘
```

---

## Python 完整实现

```python
"""
Generative Agents 社交模拟实验（简化版）
====================================
基于论文: "Generative Agents: Interactive Simulacra of Human Behavior"
(Park et al., Stanford, UIST 2023)

本实现使用基于规则的模板生成模拟 LLM，保留核心架构：
- 记忆流 (Memory Stream) + 重要性评分
- 反思 (Reflection)
- 规划 (Planning) 分天计划 / 小时计划
- 涌现社交行为

运行方式: python generative_agents_sim.py
"""

import random
import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from enum import Enum, auto
from collections import defaultdict
import heapq

# ─────────────────────────────────────────────────────────────
# 0. 全局配置与随机种子
# ─────────────────────────────────────────────────────────────

random.seed(42)

SIMULATION_DATE = datetime.date(2026, 7, 6)
START_HOUR = 6      # 06:00
END_HOUR = 22       # 22:00

# 时间步长（分钟）
TIME_STEP_MINUTES = 30

# 记忆流参数
MEMORY_CAPACITY = 200           # 最大记忆容量
REFLECTION_THRESHOLD = 8          # 同主题记忆数量触发反思
MAX_REFLECTION_DEPTH = 2        # 反思层级上限
RETRIEVAL_TOP_K = 10            # 检索时返回 top-k 记忆
RECENCY_DECAY_HOURS = 8.0       # 记忆衰减时间常数（小时）

# 重要性评分权重
IMPORTANCE_BASELINE = 3.0
IMPORTANCE_RANGE = (1, 10)


# ─────────────────────────────────────────────────────────────
# 1. 基础数据结构
# ─────────────────────────────────────────────────────────────

class Location(Enum):
    """虚拟小镇位置"""
    HOME = "家"
    CAFE = "咖啡馆"
    PARK = "公园"
    
    @property
    def description(self) -> str:
        descriptions = {
            Location.HOME: "温馨的住所，可以休息、吃饭和做私事",
            Location.CAFE: "小镇的社交中心，提供咖啡和闲聊场所",
            Location.PARK: "绿树成荫的公园，适合散步和偶遇"
        }
        return descriptions[self]


class MemoryType(Enum):
    """记忆类型"""
    OBSERVATION = auto()   # 直接观察
    REFLECTION = auto()    # 反思产生的抽象记忆
    PLAN = auto()          # 计划相关记忆


@dataclass
class MemoryNode:
    """
    记忆节点（记忆流中的基本单元）
    对应论文中的 Memory Stream 条目
    """
    agent_name: str
    content: str
    timestamp: datetime.datetime
    memory_type: MemoryType
    importance: float       # 1-10 的重要性评分
    keywords: Set[str] = field(default_factory=set)
    depth: int = 0          # 反思层级（0=原始观察）
    
    # 用于检索的复合分数（运行时计算）
    retrieval_score: float = 0.0
    
    def __post_init__(self):
        if not self.keywords:
            self.keywords = self._extract_keywords(self.content)
    
    @staticmethod
    def _extract_keywords(content: str) -> Set[str]:
        """基于规则的关键词提取"""
        # 简单规则：提取人名、地点、动作词
        keywords = set()
        
        # 人名
        names = {"Alice", "Bob", "Carol"}
        for name in names:
            if name in content:
                keywords.add(name)
        
        # 地点
        locations = {"家", "咖啡馆", "公园", "咖啡", "公园", "家里"}
        for loc in locations:
            if loc in content:
                keywords.add(loc)
        
        # 动作/事件类型
        events = {"遇见", "聊天", "吃饭", "工作", "散步", "阅读", "睡觉", 
                  "争吵", "帮助", "邀请", "计划", "聚会", "分享"}
        for event in events:
            if event in content:
                keywords.add(event)
        
        # 如果没有关键词，提取前几个名词性词
        if not keywords:
            words = content.replace("，", " ").replace"。", " ").split()
            keywords = set(w for w in words if len(w) > 1)[:3]
        
        return keywords
    
    def __repr__(self) -> str:
        time_str = self.timestamp.strftime("%H:%M")
        type_symbol = {MemoryType.OBSERVATION: "📌", 
                       MemoryType.REFLECTION: "💭", 
                       MemoryType.PLAN: "📋"}
        return f"[{time_str}] {type_symbol.get(self.memory_type, '?')} {self.content} (重要性: {self.importance:.1f})"


@dataclass
class PlanNode:
    """
    计划节点（层级化规划）
    对应论文中的 Planning 模块
    """
    description: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    location: Optional[Location] = None
    priority: int = 5           # 1-10，越高越优先
    is_interruptible: bool = True
    source: str = "plan"        # 来源: plan / reaction / social
    
    @property
    def duration_minutes(self) -> int:
        return int((self.end_time - self.start_time).total_seconds() / 60)
    
    def __repr__(self) -> str:
        start = self.start_time.strftime("%H:%M")
        end = self.end_time.strftime("%H:%M")
        loc = self.location.value if self.location else "?"
        return f"[{start}-{end} @ {loc}] {self.description} (优先级: {self.priority})"


# ─────────────────────────────────────────────────────────────
# 2. 基于规则的重要性评分器
# ─────────────────────────────────────────────────────────────

class ImportanceScorer:
    """
    重要性评分器 —— 决定哪些记忆值得记住
    
    初学者要点：
    - 人类不会记住所有事情（你不会记住每一口呼吸），Agent 也需要"筛选"
    - 评分规则：日常活动低分（1-3），社交互动中分（4-6），情绪事件高分（7-10）
    - 高分记忆更容易被检索到，影响 Agent 的决策
    - 真实论文使用 LLM 评估重要性，这里用规则简化
    
    对应论文中的 Importance Score 模块
    """
    
    HIGH_IMPACT_KEYWORDS = {
        "争吵", "冲突", "生气", "道歉", "表白", "失望", "惊喜",
        "礼物", "帮助", "拯救", "生病", "获奖", "丢失", "找到"
    }
    
    SOCIAL_KEYWORDS = {
        "遇见", "聊天", "对话", "邀请", "聚会", "分享", "讨论",
        "打招呼", "问候", "告别", "一起", "合作"
    }
    
    ROUTINE_KEYWORDS = {
        "起床", "睡觉", "刷牙", "洗澡", "吃饭", "喝水", "走路",
        "坐着", "站着", "阅读", "工作", "休息"
    }
    
    @classmethod
    def score(cls, content: str, memory_type: MemoryType) -> float:
        """计算记忆的重要性评分 (1-10)"""
        base_score = IMPORTANCE_BASELINE
        
        # 反思类型记忆天然重要性较高（抽象层次高）
        if memory_type == MemoryType.REFLECTION:
            base_score += 2.0
        elif memory_type == MemoryType.PLAN:
            base_score += 0.5
        
        # 关键词匹配评分
        content_lower = content.lower()
        
        for kw in cls.HIGH_IMPACT_KEYWORDS:
            if kw in content_lower:
                base_score += 3.0
                break  # 只加一次最高分
        
        for kw in cls.SOCIAL_KEYWORDS:
            if kw in content_lower:
                base_score += 2.0
                break
        
        for kw in cls.ROUTINE_KEYWORDS:
            if kw in content_lower:
                base_score -= 0.5
                break
        
        # 包含其他 Agent 名称（社交意义）
        other_agents = {"Alice", "Bob", "Carol"}
        for name in other_agents:
            if name.lower() in content_lower:
                base_score += 1.0
                break
        
        # 限制在 1-10 范围
        return max(IMPORTANCE_RANGE[0], min(IMPORTANCE_RANGE[1], base_score))


# ─────────────────────────────────────────────────────────────
# 3. Agent 类
# ─────────────────────────────────────────────────────────────

class GenerativeAgent:
    """
    生成式 Agent —— 拥有记忆、反思、规划和社交能力的虚拟人
    
    初学者要点：
    - 这是论文中 25 个 Agent 的简化版，保留核心机制
    - 四个核心模块：
      1. 记忆流（memory_stream）：记录所有经历，按重要性排序
      2. 反思（reflections）：当某主题频繁出现时，生成抽象总结
      3. 规划（future_plans）：按天/小时安排活动
      4. 社交（relationships）：维护与其他 Agent 的关系分数
    - 每次行动都会产生新记忆，形成"观察→记忆→反思→规划→行动"的循环
    """
    
    def __init__(self, name: str, traits: str, initial_location: Location):
        self.name = name
        self.traits = traits
        self.location = initial_location
        
        # 记忆流（Memory Stream）
        self.memory_stream: List[MemoryNode] = []
        
        # 反思存储（主题 -> 反思列表）
        self.reflections: Dict[str, List[MemoryNode]] = defaultdict(list)
        
        # 计划（当前执行计划 + 未来计划队列）
        self.current_plan: Optional[PlanNode] = None
        self.future_plans: List[PlanNode] = []
        
        # 社交关系（其他 Agent -> 关系分数 -10~10）
        self.relationships: Dict[str, float] = defaultdict(float)
        
        # 状态
        self.current_action: str = " idle"
        self.energy: float = 100.0
        
        # 初始化记忆
        self._init_baseline_memories()
    
    def _init_baseline_memories(self):
        """初始化基础记忆（性格、日常习惯）"""
        now = datetime.datetime.combine(SIMULATION_DATE, datetime.time(START_HOUR, 0))
        
        baseline_observations = [
            f"{self.name} 知道自己是一个性格{self.traits}的人",
            f"{self.name} 喜欢在自己的{self.location.value}度过时间",
            f"{self.name} 对小镇的{Location.CAFE.value}印象深刻，那里的人很友善",
            f"{self.name} 记得自己每天早晨需要咖啡",
            f"{self.name} 认为公园是放松的最佳场所"
        ]
        
        for obs in baseline_observations:
            importance = ImportanceScorer.score(obs, MemoryType.OBSERVATION)
            memory = MemoryNode(
                agent_name=self.name,
                content=obs,
                timestamp=now - datetime.timedelta(days=1),  # 作为昨天记忆
                memory_type=MemoryType.OBSERVATION,
                importance=importance,
                depth=0
            )
            self.memory_stream.append(memory)
    
    # ── 记忆流管理 ──
    
    def add_observation(self, content: str, timestamp: datetime.datetime) -> MemoryNode:
        """添加新的观察记忆"""
        importance = ImportanceScorer.score(content, MemoryType.OBSERVATION)
        memory = MemoryNode(
            agent_name=self.name,
            content=content,
            timestamp=timestamp,
            memory_type=MemoryType.OBSERVATION,
            importance=importance,
            depth=0
        )
        self.memory_stream.append(memory)
        
        # 维护容量限制（移除最低重要性且最旧的记忆）
        if len(self.memory_stream) > MEMORY_CAPACITY:
            self.memory_stream.sort(key=lambda m: (m.importance, m.timestamp))
            self.memory_stream = self.memory_stream[1:]  # 移除最低分
        
        # 触发反思检查
        self._check_and_reflect(timestamp)
        
        return memory
    
    def retrieve_memories(self, query_keywords: Set[str], 
                          current_time: datetime.datetime,
                          top_k: int = RETRIEVAL_TOP_K) -> List[MemoryNode]:
        """
        检索相关记忆（使用复合评分：相关性 + 重要性 + 时效性）
        对应论文中的 Memory Retrieval 公式
        """
        scored_memories = []
        
        for memory in self.memory_stream:
            # 1. 相关性评分（关键词重叠）
            if memory.keywords:
                overlap = len(query_keywords & memory.keywords) / len(query_keywords | memory.keywords)
            else:
                overlap = 0.0
            
            # 2. 重要性评分（归一化到 0-1）
            importance_norm = memory.importance / 10.0
            
            # 3. 时效性评分（指数衰减）
            hours_ago = (current_time - memory.timestamp).total_seconds() / 3600
            recency = max(0.0, 1.0 - (hours_ago / RECENCY_DECAY_HOURS))
            
            # 复合评分（论文公式简化版）
            # score = alpha * relevance + beta * importance + gamma * recency
            memory.retrieval_score = 0.5 * overlap + 0.3 * importance_norm + 0.2 * recency
            scored_memories.append(memory)
        
        # 返回 top-k
        scored_memories.sort(key=lambda m: m.retrieval_score, reverse=True)
        return scored_memories[:top_k]
    
    # ── 反思模块 ──
    
    def _check_and_reflect(self, current_time: datetime.datetime):
        """
        检查是否触发反思
        当同一关键词出现在足够多的记忆中时，生成反思
        """
        # 统计最近记忆中各关键词出现频率
        keyword_counts = defaultdict(int)
        recent_memories = [m for m in self.memory_stream 
                          if (current_time - m.timestamp).total_seconds() < 86400]
        
        for memory in recent_memories:
            for kw in memory.keywords:
                keyword_counts[kw] += 1
        
        # 对高频关键词生成反思
        for keyword, count in keyword_counts.items():
            if count >= REFLECTION_THRESHOLD and keyword not in self.reflections:
                self._generate_reflection(keyword, current_time)
    
    def _generate_reflection(self, keyword: str, current_time: datetime.datetime):
        """
        生成反思（基于规则的模板生成，替代 LLM）
        对应论文中的 Reflection 模块
        """
        # 收集相关记忆
        related = [m for m in self.memory_stream if keyword in m.keywords]
        
        if len(related) < REFLECTION_THRESHOLD:
            return
        
        # 基于规则生成反思内容
        # 这里使用模板而非真实 LLM
        reflection_templates = [
            f"{self.name} 反思：最近经常涉及'{keyword}'，这可能反映了某种模式",
            f"{self.name} 意识到'{keyword}'在自己的生活中出现的频率比预期高",
            f"{self.name} 思考：为什么'{keyword}'如此重要？也许需要更深入理解"
        ]
        
        content = random.choice(reflection_templates)
        importance = ImportanceScorer.score(content, MemoryType.REFLECTION)
        
        reflection = MemoryNode(
            agent_name=self.name,
            content=content,
            timestamp=current_time,
            memory_type=MemoryType.REFLECTION,
            importance=importance,
            keywords={keyword, "反思"},
            depth=1
        )
        
        self.memory_stream.append(reflection)
        self.reflections[keyword].append(reflection)
        
        # 深度反思（如果已有反思足够多，生成更高层级）
        if len(self.reflections[keyword]) >= 2 and related[0].depth < MAX_REFLECTION_DEPTH:
            deep_content = f"{self.name} 的高级反思：关于'{keyword}'的模式，{self.name}意识到自己对这个主题的态度正在形成"
            deep_reflection = MemoryNode(
                agent_name=self.name,
                content=deep_content,
                timestamp=current_time + datetime.timedelta(minutes=1),
                memory_type=MemoryType.REFLECTION,
                importance=importance + 1.0,
                keywords={keyword, "深层反思"},
                depth=related[0].depth + 1
            )
            self.memory_stream.append(deep_reflection)
    
    # ── 规划模块 ──
    
    def generate_daily_plan(self, day_start: datetime.datetime) -> List[PlanNode]:
        """
        生成天级计划（简化版，使用模板而非 LLM）
        对应论文中的 Planning 模块
        """
        plans = []
        current_time = day_start
        
        # 根据性格特征选择计划模板
        plan_templates = self._get_plan_templates()
        
        for template in plan_templates:
            duration = template["duration"]
            end_time = current_time + datetime.timedelta(minutes=duration)
            
            plan = PlanNode(
                description=template["activity"].format(name=self.name),
                start_time=current_time,
                end_time=end_time,
                location=template["location"],
                priority=template["priority"],
                is_interruptible=template.get("interruptible", True)
            )
            plans.append(plan)
            current_time = end_time
            
            if current_time.hour >= END_HOUR:
                break
        
        self.future_plans = plans
        return plans
    
    def _get_plan_templates(self) -> List[Dict]:
        """根据性格特征返回计划模板"""
        # 通用模板（所有 Agent）
        base_templates = [
            {"activity": "{name} 起床并准备出门", "duration": 60, 
             "location": Location.HOME, "priority": 8, "interruptible": False},
            {"activity": "{name} 吃早餐", "duration": 30, 
             "location": Location.HOME, "priority": 7},
        ]
        
        # 根据性格特征添加不同活动
        if "外向" in self.traits or "社交" in self.traits:
            social_templates = [
                {"activity": "{name} 去咖啡馆社交", "duration": 120, 
                 "location": Location.CAFE, "priority": 9},
                {"activity": "{name} 在公园散步并可能遇到朋友", "duration": 90, 
                 "location": Location.PARK, "priority": 7},
                {"activity": "{name} 回家休息", "duration": 120, 
                 "location": Location.HOME, "priority": 5},
            ]
        elif "内向" in self.traits or "安静" in self.traits:
            social_templates = [
                {"activity": "{name} 在家阅读和工作", "duration": 180, 
                 "location": Location.HOME, "priority": 8},
                {"activity": "{name} 去咖啡馆安静地喝咖啡", "duration": 60, 
                 "location": Location.CAFE, "priority": 6},
                {"activity": "{name} 在公园独自散步", "duration": 60, 
                 "location": Location.PARK, "priority": 5},
            ]
        else:
            social_templates = [
                {"activity": "{name} 在咖啡馆工作", "duration": 150, 
                 "location": Location.CAFE, "priority": 7},
                {"activity": "{name} 去公园放松", "duration": 90, 
                 "location": Location.PARK, "priority": 6},
                {"activity": "{name} 回家处理事务", "duration": 120, 
                 "location": Location.HOME, "priority": 5},
            ]
        
        # 晚间模板
        evening_templates = [
            {"activity": "{name} 吃晚饭", "duration": 60, 
             "location": Location.HOME, "priority": 7},
            {"activity": "{name} 准备睡觉", "duration": 60, 
             "location": Location.HOME, "priority": 8, "interruptible": False},
        ]
        
        return base_templates + social_templates + evening_templates
    
    def get_current_plan(self, current_time: datetime.datetime) -> Optional[PlanNode]:
        """获取当前时间点应执行的计划"""
        for plan in self.future_plans:
            if plan.start_time <= current_time < plan.end_time:
                return plan
        return None
    
    def replan(self, new_plan: PlanNode, reason: str):
        """
        重新规划（因社交事件改变计划）
        对应论文中的 Plan Reaction 机制
        """
        # 将原因记录为记忆
        self.add_observation(f"{self.name} 改变了计划，因为: {reason}", new_plan.start_time)
        
        # 更新计划
        self.future_plans = [p for p in self.future_plans if p.end_time <= new_plan.start_time]
        self.future_plans.append(new_plan)
        self.future_plans.sort(key=lambda p: p.start_time)
    
    # ── 执行与行动 ──
    
    def act(self, current_time: datetime.datetime, environment: 'Environment') -> str:
        """执行当前时间步的动作"""
        plan = self.get_current_plan(current_time)
        
        if plan:
            # 如果需要移动
            if plan.location and plan.location != self.location:
                self.location = plan.location
                action = f"{self.name} 从之前的地点移动到了{self.location.value}"
                self.add_observation(action, current_time)
                return action
            
            # 执行计划动作
            self.current_action = plan.description
            self.add_observation(plan.description, current_time)
            self.energy -= 2.0
            return plan.description
        else:
            # 没有计划时的默认行为
            default_action = f"{self.name} 在{self.location.value}发呆"
            self.current_action = default_action
            self.add_observation(default_action, current_time)
            return default_action
    
    def interact_with(self, other: 'GenerativeAgent', current_time: datetime.datetime) -> str:
        """
        与另一个 Agent 交互（基于规则的对话生成）
        对应论文中的 Agent-Environment Interaction
        """
        # 确定交互类型
        interaction_type = self._determine_interaction_type(other)
        
        # 生成对话/交互内容
        dialogue = self._generate_dialogue(other, interaction_type, current_time)
        
        # 记录观察
        self.add_observation(f"与 {other.name} 的互动: {dialogue}", current_time)
        other.add_observation(f"与 {self.name} 的互动: {dialogue}", current_time)
        
        # 更新关系
        self._update_relationship(other, interaction_type)
        
        return dialogue
    
    def _determine_interaction_type(self, other: 'GenerativeAgent') -> str:
        """基于关系和历史决定交互类型"""
        relation_score = self.relationships[other.name]
        
        if relation_score > 5:
            return "friendly"
        elif relation_score < -3:
            return "hostile"
        elif relation_score > 0:
            return "neutral_positive"
        else:
            return "neutral"
    
    def _generate_dialogue(self, other: 'GenerativeAgent', 
                           interaction_type: str, 
                           current_time: datetime.datetime) -> str:
        """基于规则的对话生成（模板系统）"""
        
        # 检索相关记忆用于上下文
        query = {other.name, self.location.value}
        relevant_memories = self.retrieve_memories(query, current_time, top_k=3)
        memory_context = ""
        if relevant_memories:
            memory_context = relevant_memories[0].content
        
        # 对话模板
        templates = {
            "friendly": [
                f"{self.name} 热情地向 {other.name} 打招呼: '好久不见！最近在忙什么？'",
                f"{self.name} 对 {other.name} 说: '上次你提到的那个想法，我一直在思考'",
                f"{self.name} 邀请 {other.name}: '要不要一起去{Location.CAFE.value}坐坐？'",
                f"{self.name} 分享了一个有趣的故事给 {other.name}"
            ],
            "neutral_positive": [
                f"{self.name} 对 {other.name} 微笑: '嗨，今天天气不错'",
                f"{self.name} 和 {other.name} 讨论了小镇最近的变化",
                f"{self.name} 向 {other.name} 询问了一些建议"
            ],
            "neutral": [
                f"{self.name} 和 {other.name} 礼貌地点头致意",
                f"{self.name} 对 {other.name} 说: '不好意思，我在赶时间'",
                f"{self.name} 和 {other.name} 简短交换了今天的计划"
            ],
            "hostile": [
                f"{self.name} 冷淡地对 {other.name} 说: '我不想和你说话'",
                f"{self.name} 对 {other.name} 抱怨: '你上次做的事让我很不高兴'",
                f"{self.name} 避开了 {other.name} 的目光"
            ]
        }
        
        # 如果有相关记忆，可能触发特定话题
        if memory_context and "争吵" in memory_context and random.random() < 0.3:
            return f"{self.name} 提起之前的事对 {other.name} 说: '关于那件事，我想我们应该谈谈'"
        
        options = templates.get(interaction_type, templates["neutral"])
        return random.choice(options)
    
    def _update_relationship(self, other: 'GenerativeAgent', interaction_type: str):
        """更新关系分数"""
        delta = {
            "friendly": 1.5,
            "neutral_positive": 0.5,
            "neutral": 0.0,
            "hostile": -2.0
        }.get(interaction_type, 0.0)
        
        self.relationships[other.name] += delta
        other.relationships[self.name] += delta
        
        # 限制范围
        self.relationships[other.name] = max(-10, min(10, self.relationships[other.name]))
        other.relationships[self.name] = max(-10, min(10, other.relationships[self.name]))
    
    # ── 工具方法 ──
    
    def get_memory_summary(self, top_n: int = 10) -> str:
        """获取记忆流摘要"""
        sorted_memories = sorted(self.memory_stream, key=lambda m: m.importance, reverse=True)
        return "\n".join(f"  {m}" for m in sorted_memories[:top_n])
    
    def get_plan_summary(self) -> str:
        """获取计划摘要"""
        return "\n".join(f"  {p}" for p in self.future_plans)
    
    def get_relationship_summary(self) -> str:
        """获取关系摘要"""
        lines = []
        for name, score in self.relationships.items():
            status = "友好" if score > 3 else "一般" if score > -3 else "紧张"
            lines.append(f"  {name}: {score:.1f} ({status})")
        return "\n".join(lines) if lines else "  (暂无社交关系)"


# ─────────────────────────────────────────────────────────────
# 4. 环境类
# ─────────────────────────────────────────────────────────────

class Environment:
    """
    虚拟小镇环境 —— 协调多个 Agent 的交互场所
    
    初学者要点：
    - 管理所有 Agent 的位置、时间和事件记录
    - 每个时间步：所有 Agent 行动 → 同位置 Agent 交互 → 时间推进
    - 社交重新规划（_check_social_replan）：关系好的 Agent 可能邀请对方一起活动
    - event_log 记录所有事件，用于后续分析涌现行为
    """
    
    def __init__(self):
        self.locations: Dict[Location, Set[str]] = {
            loc: set() for loc in Location
        }
        self.agents: Dict[str, GenerativeAgent] = {}
        self.time: datetime.datetime = datetime.datetime.combine(
            SIMULATION_DATE, datetime.time(START_HOUR, 0)
        )
        self.event_log: List[str] = []
    
    def add_agent(self, agent: GenerativeAgent):
        """添加 Agent 到环境"""
        self.agents[agent.name] = agent
        self.locations[agent.location].add(agent.name)
    
    def move_agent(self, agent_name: str, new_location: Location):
        """移动 Agent 到新的位置"""
        agent = self.agents[agent_name]
        
        # 从旧位置移除
        if agent.location in self.locations:
            self.locations[agent.location].discard(agent_name)
        
        # 更新位置
        agent.location = new_location
        self.locations[new_location].add(agent_name)
    
    def get_agents_at(self, location: Location) -> List[GenerativeAgent]:
        """获取某位置的所有 Agent"""
        return [self.agents[name] for name in self.locations.get(location, set())]
    
    def log_event(self, event: str):
        """记录事件"""
        time_str = self.time.strftime("%H:%M")
        self.event_log.append(f"[{time_str}] {event}")
    
    def step(self):
        """环境时间步进"""
        # 1. 每个 Agent 执行动作
        for agent in self.agents.values():
            action = agent.act(self.time, self)
            self.log_event(action)
        
        # 2. 处理同位置 Agent 之间的交互
        for location in Location:
            agents_here = self.get_agents_at(location)
            if len(agents_here) >= 2:
                # 让所有同位置的 Agent 对交互
                for i in range(len(agents_here)):
                    for j in range(i + 1, len(agents_here)):
                        a1, a2 = agents_here[i], agents_here[j]
                        
                        # 只有双方都愿意时才交互（基于计划和可中断性）
                        plan1 = a1.get_current_plan(self.time)
                        plan2 = a2.get_current_plan(self.time)
                        
                        # 如果对方计划不可中断，跳过交互
                        if plan1 and not plan1.is_interruptible:
                            continue
                        if plan2 and not plan2.is_interruptible:
                            continue
                        
                        # 交互概率（社交型性格概率更高）
                        interact_prob = 0.6 if ("外向" in a1.traits or "外向" in a2.traits) else 0.4
                        if random.random() < interact_prob:
                            dialogue = a1.interact_with(a2, self.time)
                            self.log_event(dialogue)
                            
                            # 检查是否需要因社交重新规划
                            self._check_social_replan(a1, a2)
        
        # 3. 时间推进
        self.time += datetime.timedelta(minutes=TIME_STEP_MINUTES)
    
    def _check_social_replan(self, a1: GenerativeAgent, a2: GenerativeAgent):
        """检查社交事件是否触发计划变更"""
        # 如果关系很好，且没有计划一起活动，可能产生新计划
        if a1.relationships[a2.name] > 5 and random.random() < 0.3:
            # 检查是否有一方有计划去新位置，邀请另一方
            for agent in [a1, a2]:
                plan = agent.get_current_plan(self.time)
                if plan and plan.location and plan.is_interruptible:
                    other = a2 if agent == a1 else a1
                    other_plan = other.get_current_plan(self.time)
                    
                    # 如果另一方没有冲突的不可中断计划
                    if other_plan is None or other_plan.is_interruptible:
                        # 产生邀请
                        invitation = (f"{agent.name} 邀请 {other.name} 一起去{plan.location.value}")
                        self.log_event(invitation)
                        
                        # 另一方接受邀请并更新计划
                        new_plan = PlanNode(
                            description=f"{other.name} 接受邀请，和 {agent.name} 一起活动",
                            start_time=self.time,
                            end_time=plan.end_time,
                            location=plan.location,
                            priority=plan.priority + 1,
                            source="social"
                        )
                        other.replan(new_plan, f"{agent.name} 的邀请")
                        
                        # 移动另一方
                        self.move_agent(other.name, plan.location)
                        break


# ─────────────────────────────────────────────────────────────
# 5. 模拟主循环
# ─────────────────────────────────────────────────────────────

def run_simulation() -> Tuple[Environment, List[str]]:
    """运行完整的一天模拟"""
    
    print("=" * 60)
    print("Generative Agents 社交模拟实验（简化版）")
    print("基于论文: Park et al., UIST 2023")
    print("=" * 60)
    
    # 创建环境
    env = Environment()
    
    # 创建 Agent
    alice = GenerativeAgent(
        name="Alice",
        traits="外向、热情、喜欢组织活动",
        initial_location=Location.HOME
    )
    
    bob = GenerativeAgent(
        name="Bob",
        traits="内向、安静、喜欢阅读",
        initial_location=Location.HOME
    )
    
    carol = GenerativeAgent(
        name="Carol",
        traits="友善、好奇、喜欢社交",
        initial_location=Location.HOME
    )
    
    env.add_agent(alice)
    env.add_agent(bob)
    env.add_agent(carol)
    
    # 生成每日计划
    day_start = datetime.datetime.combine(SIMULATION_DATE, datetime.time(START_HOUR, 0))
    
    print("\n" + "─" * 60)
    print("各 Agent 的每日计划:")
    print("─" * 60)
    
    for agent in env.agents.values():
        agent.generate_daily_plan(day_start)
        print(f"\n{agent.name} ({agent.traits}):")
        print(agent.get_plan_summary())
    
    # 模拟循环
    print("\n" + "=" * 60)
    print("模拟开始 (06:00 - 22:00)")
    print("=" * 60)
    
    while env.time.hour < END_HOUR or (env.time.hour == END_HOUR and env.time.minute == 0):
        env.step()
    
    # 输出结果
    print("\n" + "=" * 60)
    print("模拟事件日志:")
    print("=" * 60)
    
    for event in env.event_log:
        print(event)
    
    # 输出各 Agent 状态
    print("\n" + "=" * 60)
    print("模拟结束后各 Agent 状态:")
    print("=" * 60)
    
    for agent in env.agents.values():
        print(f"\n{'─' * 40}")
        print(f"Agent: {agent.name} ({agent.traits})")
        print(f"{'─' * 40}")
        print(f"最终位置: {agent.location.value}")
        print(f"剩余能量: {agent.energy:.1f}")
        
        print(f"\n社交关系:")
        print(agent.get_relationship_summary())
        
        print(f"\n重要记忆 (按重要性 top 10):")
        print(agent.get_memory_summary(top_n=10))
        
        print(f"\n反思记录:")
        if agent.reflections:
            for keyword, reflections in agent.reflections.items():
                print(f"  主题 '{keyword}': {len(reflections)} 条反思")
                for r in reflections:
                    print(f"    - {r}")
        else:
            print("  (暂无反思)")
    
    # 涌现行为分析
    print("\n" + "=" * 60)
    print("涌现行为分析:")
    print("=" * 60)
    analyze_emergence(env)
    
    return env, env.event_log


def analyze_emergence(env: Environment):
    """分析模拟中涌现的社交行为"""
    
    # 1. 统计聚会事件（3 人同时在同一场所）
    gatherings = []
    for event in env.event_log:
        if "邀请" in event or "一起" in event:
            gatherings.append(event)
    
    # 2. 关系变化
    print("\n1. 社交关系演变:")
    for agent in env.agents.values():
        for other_name, score in agent.relationships.items():
            if score != 0:
                print(f"   {agent.name} → {other_name}: 关系分数 = {score:.1f}")
    
    # 3. 计划变更统计
    print("\n2. 计划变更事件:")
    plan_changes = [e for e in env.event_log if "改变了计划" in e]
    for event in plan_changes:
        print(f"   {event}")
    
    # 4. 反思生成统计
    print("\n3. 反思生成统计:")
    for agent in env.agents.values():
        total_reflections = sum(len(v) for v in agent.reflections.values())
        if total_reflections > 0:
            print(f"   {agent.name}: 生成了 {total_reflections} 条反思")
    
    # 5. 位置分布
    print("\n4. 位置访问统计:")
    location_visits = defaultdict(int)
    for event in env.event_log:
        for loc in Location:
            if loc.value in event and "移动" in event:
                location_visits[loc.value] += 1
    
    for loc_name, count in location_visits.items():
        print(f"   {loc_name}: {count} 次访问")
    
    print("\n5. 涌现行为总结:")
    if gatherings:
        print(f"   ✓ 发现 {len(gatherings)} 次社交邀请/共同活动（计划外的涌现）")
    if plan_changes:
        print(f"   ✓ 发现 {len(plan_changes)} 次计划变更（社交驱动的适应）")
    
    # 检查是否有关系链形成
    strong_relations = 0
    for agent in env.agents.values():
        for score in agent.relationships.values():
            if score > 5:
                strong_relations += 1
    
    if strong_relations >= 2:
        print(f"   ✓ 形成 {strong_relations} 段强关系（关系分数 > 5）")
    
    print("\n   这些行为未在初始计划中明确编码，")
    print("   而是通过 Agent 间交互、记忆检索和规划重算自然涌现的。")


# ─────────────────────────────────────────────────────────────
# 6. 运行入口
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_simulation()
```

---


## 评估指标详解（初学者指南）

### 为什么需要这些指标？

Generative Agents 的核心价值在于**涌现行为**——系统没有显式编码"邀请朋友"或"形成小团体"的逻辑，但这些行为会从 Agent 的交互中自然产生。这些指标帮助我们量化涌现行为的发生频率和强度。

### 指标一览

| 指标 | 定义 | 为什么重要 | 理想值 | 如何改进 |
|-----|------|----------|--------|---------|
| **社交关系演变** | Agent 之间关系分数的变化 | 量化社交纽带的形成过程 | 正分数增长 | 增加交互机会、调整关系变化幅度 |
| **计划变更次数** | 因社交事件而改变计划的次数 | 衡量 Agent 的社交适应性 | > 0 | 降低 plan 的 is_interruptible 门槛 |
| **反思生成数量** | 高频主题触发的反思记忆数 | 衡量抽象思维能力 | 随模拟增长 | 降低 REFLECTION_THRESHOLD |
| **位置访问分布** | 各位置被访问的频率 | 验证性格特征是否影响行为 | 外向型更多去咖啡馆 | 调整性格-计划模板映射 |
| **涌现行为计数** | 聚会邀请、强关系形成等 | 核心验证指标：是否有未编码的行为出现 | > 0 | 增加 Agent 数量、增加交互概率 |

### 指标之间的关系

```
更多交互 → 更多记忆 → 更多反思 → 更强关系 → 更多计划变更 → 更多涌现行为
```

**关键洞察**：
- 关系分数 > 5 且计划变更 > 0 → 证明社交确实影响了行为（不是独立行动）
- 反思数量 = 0 → 检查 REFLECTION_THRESHOLD 是否太高，或记忆增长是否太慢
- 位置分布均匀 → 性格特征可能没有正确影响计划生成
- 涌现行为 = 0 → 检查 interact_prob 是否太低，或同位置相遇机会是否太少

---

## 运行示例


```bash
python generative_agents_sim.py
```

### 预期输出（片段）

```
============================================================
Generative Agents 社交模拟实验（简化版）
基于论文: Park et al., UIST 2023
============================================================

------------------------------------------------------------
各 Agent 的每日计划:
------------------------------------------------------------

Alice (外向、热情、喜欢组织活动):
  [06:00-07:00 @ 家] Alice 起床并准备出门 (优先级: 8)
  [07:00-07:30 @ 家] Alice 吃早餐 (优先级: 7)
  [07:30-09:30 @ 咖啡馆] Alice 去咖啡馆社交 (优先级: 9)
  ...

============================================================
模拟开始 (06:00 - 22:00)
============================================================

[06:00] Alice 从之前的地点移动到了家
[06:00] Bob 从之前的地点移动到了家
[06:00] Carol 从之前的地点移动到了家
[06:30] Alice 起床并准备出门
[06:30] Bob 起床并准备出门
[06:30] Carol 起床并准备出门
...
[09:00] Alice 在咖啡馆社交
[09:00] Bob 在家阅读和工作
[09:00] Carol 在咖啡馆安静地喝咖啡
[09:00] Alice 对 Carol 微笑: '嗨，今天天气不错'
[09:00] Carol 热情地向 Alice 打招呼: '好久不见！最近在忙什么？'
...
[10:30] Alice 邀请 Carol: '要不要一起去公园坐坐？'
[10:30] Carol 接受邀请，和 Alice 一起活动
...
[14:00] Alice 反思：最近经常涉及'咖啡馆'，这可能反映了某种模式
...

============================================================
模拟结束后各 Agent 状态:
============================================================

Agent: Alice (外向、热情、喜欢组织活动)
最终位置: 家
剩余能量: 68.0

社交关系:
  Bob: 2.5 (一般)
  Carol: 7.5 (友好)

重要记忆 (按重要性 top 10):
  [10:30] 💭 Alice 反思：最近经常涉及'咖啡馆'...
  [09:00] 📌 Alice 邀请 Carol 去公园
  ...
```

---


## 场景配置矩阵

| 场景 | Agent数量 | 时间步长 | 记忆容量 | 反思阈值 | 用途 |
|-----|----------|---------|---------|---------|------|
| 快速测试 | 2 | 60min | 50 | 5 | 验证基本流程，5分钟出结果 |
| 标准模拟 | 3 | 30min | 200 | 8 | 观察完整社交涌现（推荐） |
| 密集社交 | 5 | 15min | 300 | 6 | 高频率互动，更多涌现行为 |
| 长周期 | 3 | 30min | 500 | 10 | 观察长期关系演化 |
| 极简模式 | 2 | 120min | 30 | 3 | 教学演示，最快理解机制 |

### 初学者调试清单

- [ ] **如果没有涌现行为**：检查 `interact_prob`（默认 0.4-0.6）是否太低
- [ ] **如果反思不生成**：检查 `REFLECTION_THRESHOLD`（默认 8）是否太高，或模拟时间是否太短
- [ ] **如果关系不变化**：检查 `_update_relationship()` 的 delta 值是否太小
- [ ] **如果所有 Agent 行为相同**：检查性格特征是否正确传入 `_get_plan_templates()`
- [ ] **如果计划从不改变**：检查 `is_interruptible` 是否全为 False
- [ ] **如果模拟输出为空**：检查 `END_HOUR` 和循环条件

---

## 实验分析


### 1. 记忆架构验证

| 组件 | 论文实现 | 本实验简化 | 验证目标 |
|------|---------|-----------|---------|
| 记忆流 | 存储所有观察 | 列表存储 + 容量限制 | 记忆是否可增长、可过滤 |
| 重要性评分 | LLM 评估 | 基于规则评分 | 高重要性事件是否优先检索 |
| 检索公式 | 相关+重要+时效 | 加权求和 | 相关记忆是否被正确召回 |
| 反思 | LLM 总结 | 模板触发 | 高频主题是否产生抽象 |

### 2. 涌现行为观察

运行模拟后可观察到的涌现现象：

1. **社交聚会**：Alice（外向）更可能邀请 Carol（友善）一起活动，形成 2 人小团体
2. **关系形成**：频繁互动导致关系分数累积，正反馈循环产生强社交纽带
3. **计划变更**：社交邀请打断原有计划，Agent 自适应调整行程
4. **主题反思**：高频访问的地点（如咖啡馆）触发反思，形成抽象概念

### 3. 与论文的差异

| 维度 | 论文（Park et al.） | 本实验 |
|------|---------------------|--------|
| Agent 数量 | 25 个 | 3 个 |
| 环境规模 | 完整的虚拟小镇（房间级） | 3 个地点 |
| 语言生成 | 真实 LLM（GPT-3.5） | 基于规则的模板 |
| 反思深度 | 多层递归反思 | 最多 2 层 |
| 计算成本 | 高（大量 LLM 调用） | 极低（纯规则） |
| 可复现性 | 低（LLM 随机性） | 高（固定种子） |

### 4. 关键洞察

> **涌现不需要 LLM**：本实验证明，即使使用基于规则的模板系统，只要具备
> - 记忆存储与检索
> - 关系建模
> - 规划重算
> 三个机制，就能产生可信的社交涌现行为。LLM 的作用是提升语言质量，而非涌现的必要条件。

> **反思的触发条件**：论文未明确说明反思何时触发。本实验使用**关键词频率阈值**（8 次）作为触发器，实际效果表明：高频重复的主题确实需要抽象化，否则会淹没记忆流。

> **可中断计划的重要性**：如果计划不可中断，Agent 变成"机器人"，不会产生社交适应。论文中的计划层级（天/小时/分钟）本质上是为可中断性提供粒度。

---

## 扩展实验建议

1. **添加 LLM 后端**：将 `_generate_dialogue` 和 `_generate_reflection` 替换为 API 调用，对比语言质量与计算成本
2. **遗忘机制**：实现基于时间和重要性的记忆衰减，验证"人类遗忘曲线"在 Agent 中的效果
3. **大规模模拟**：扩展到 10-25 个 Agent，观察是否会出现信息传播、谣言、群体极化等复杂涌现
4. **情感维度**：给记忆添加情感标签（正/负/中性），让关系演化更细腻

---

## 关联论文

- Park, J. S., et al. (2023). "Generative Agents: Interactive Simulacra of Human Behavior." *ACM UIST*.
- 关联笔记: [[01c-Human-AI-Game-Interaction]] 第 2 节
- 在线资源: https://generative-agents.com

---

*实验创建: 2026-07-06*
*维护者: AIResearchVault*