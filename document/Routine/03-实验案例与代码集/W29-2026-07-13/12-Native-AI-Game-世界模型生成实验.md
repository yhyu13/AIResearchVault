# 实验 12：Native AI Game — 世界模型生成实验

---

## 实验信息

| 属性 | 值 |
|------|-----|
| **实验编号** | 12 |
| **实验名称** | Native AI Game — 世界模型生成实验 |
| **关联论文** | Genie (DeepMind), Infinigen (Meta), AI Dungeon |
| **实验类型** | 程序化生成 + 世界模型 + 交互模拟 |
| **技术栈** | Python, NumPy, Matplotlib |
| **预估耗时** | 60-90 分钟 |
| **难度等级** | ★★★★☆ |

---

## 实验背景

### 核心概念

**Native AI Game** 是围绕 AI 原生能力重新设计的游戏范式——不是将 AI 作为外挂工具，而是让 AI 生成世界、驱动叙事、创造玩法。本实验聚焦两个关键技术路径：

1. **程序化生成路径（Infinigen）**：用算法和规则系统生成无限多样化的世界内容。每个元素都有确定性生成逻辑和可编辑属性，不依赖训练数据。

2. **世界模型路径（Genie）**：用神经网络从数据中学习环境动力学，生成可交互的物理一致世界。核心思想是"世界模型即游戏引擎"。

### 实验目标

将两条路径融合到一个简化原型中：
- 使用 **程序化生成**（Infinigen 思路）构建基础地形、植被、建筑
- 使用 **世界模型**（Genie 思路）管理环境状态和预测交互后果
- 实现一个可探索的 2D 世界，包含地形、物体、NPC 和基本交互
- 提供 **移动、采集、建造** 三种核心交互

---

## 理论基础

### 程序化生成（Procedural Generation）

程序化生成使用算法而非手工制作来创建内容。核心数学工具包括：

**Perlin 噪声**：通过叠加多个频率的噪声（Fractional Brownian Motion, fBm）生成自然地形：

$$h(x,y) = \sum_{i=0}^{n-1} \frac{1}{2^i} \cdot noise(2^i x, 2^i y)$$

其中 $noise$ 是平滑的伪随机函数，通过多八度叠加产生自相似的分形地形。

**地形分类**：基于高度阈值将连续地形映射到离散类型：

| 高度范围 | 地形类型 | 特征 |
|---------|---------|------|
| $h < 0.3$ | 水域 | 不可通行，提供鱼类资源 |
| $0.3 \leq h < 0.4$ | 沙滩 | 过渡区域，稀有资源 |
| $0.4 \leq h < 0.6$ | 平原 | 适合建造，有植被 |
| $0.6 \leq h < 0.8$ | 森林 | 木材资源丰富，NPC 出没 |
| $h \geq 0.8$ | 山地 | 石材资源，难以通行 |

### 世界模型（World Model）

世界模型 $M$ 将当前状态 $s_t$ 和动作 $a_t$ 映射到下一状态 $s_{t+1}$：

$$s_{t+1} = M(s_t, a_t)$$

在本实验中，世界模型简化为确定性状态转移规则：
- 移动：$s_{t+1} = s_t + \Delta_{direction}$，若目标位置可通行
- 采集：若资源存在，$inventory \leftarrow inventory + resource$，$world[resource] \leftarrow 0$
- 建造：若资源足够且位置可建造，$world[building] \leftarrow type$

### 简单 NPC AI（Agent Model）

每个 NPC 有目标驱动行为：
- 状态：位置、能量、目标、记忆
- 感知：观察周围 7×7 区域
- 行动：向目标移动、采集、休息
- 世界模型：NPC 内部维护简化的世界状态预测，用于路径规划

---

## 实验架构

```
┌─────────────────────────────────────────────────────┐
│                   Game Engine                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │  World Gen  │  │ World Model │  │  Renderer   │  │
│  │ (Infinigen) │  │  (Genie)    │  │(Matplotlib) │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
│         │                │                │          │
│         ▼                ▼                ▼          │
│  ┌─────────────────────────────────────────────┐   │
│  │              World State (64×64)              │   │
│  │  terrain[64,64]  ·  objects[64,64]  ·  NPCs  │   │
│  └─────────────────────────────────────────────┘   │
│         ▲                ▲                ▲        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐│
│  │   Player    │  │    NPCs     │  │  Buildings  ││
│  │  Controller │  │    AI       │  │   System    ││
│  └─────────────┘  └─────────────┘  └─────────────┘│
└─────────────────────────────────────────────────────┘
```

---

## 完整代码

### 文件：`native_ai_world_game.py`

```python
"""
Native AI Game - 世界模型生成实验
融合 Infinigen 程序化生成 + Genie 世界模型思路

技术栈：Python + NumPy + Matplotlib（纯标准库实现，无外部依赖）

作者: AIResearchVault
日期: 2026-07-13
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.collections import PatchCollection
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Set
import random
import math
from collections import deque


# ═══════════════════════════════════════════════════════════
# 1. 核心枚举与数据类
# ═══════════════════════════════════════════════════════════

class TerrainType(Enum):
    """地形类型枚举"""
    WATER = 0
    SAND = 1
    PLAIN = 2
    FOREST = 3
    MOUNTAIN = 4
    
    @property
    def color(self) -> str:
        return {
            TerrainType.WATER: '#1E90FF',
            TerrainType.SAND: '#F0E68C',
            TerrainType.PLAIN: '#228B22',
            TerrainType.FOREST: '#006400',
            TerrainType.MOUNTAIN: '#696969',
        }[self]
    
    @property
    def walkable(self) -> bool:
        return self != TerrainType.WATER and self != TerrainType.MOUNTAIN


class ResourceType(Enum):
    """资源类型"""
    NONE = 0
    WOOD = 1
    STONE = 2
    FOOD = 3
    GOLD = 4
    
    @property
    def color(self) -> str:
        return {
            ResourceType.NONE: 'none',
            ResourceType.WOOD: '#8B4513',
            ResourceType.STONE: '#A9A9A9',
            ResourceType.FOOD: '#FF6347',
            ResourceType.GOLD: '#FFD700',
        }[self]


class BuildingType(Enum):
    """建筑类型"""
    NONE = 0
    HOUSE = 1
    WORKSHOP = 2
    FARM = 3
    TOWER = 4
    
    @property
    def cost(self) -> Dict[ResourceType, int]:
        return {
            BuildingType.NONE: {},
            BuildingType.HOUSE: {ResourceType.WOOD: 5, ResourceType.STONE: 2},
            BuildingType.WORKSHOP: {ResourceType.WOOD: 8, ResourceType.STONE: 4},
            BuildingType.FARM: {ResourceType.WOOD: 3, ResourceType.FOOD: 2},
            BuildingType.TOWER: {ResourceType.STONE: 10, ResourceType.WOOD: 5, ResourceType.GOLD: 2},
        }[self]
    
    @property
    def color(self) -> str:
        return {
            BuildingType.NONE: 'none',
            BuildingType.HOUSE: '#CD853F',
            BuildingType.WORKSHOP: '#4682B4',
            BuildingType.FARM: '#9ACD32',
            BuildingType.TOWER: '#DC143C',
        }[self]


class NPCRole(Enum):
    """NPC 角色类型"""
    VILLAGER = auto()
    MERCHANT = auto()
    GUARD = auto()
    EXPLORER = auto()


@dataclass
class Position:
    """2D 位置"""
    x: int
    y: int
    
    def __add__(self, other: Tuple[int, int]) -> 'Position':
        return Position(self.x + other[0], self.y + other[1])
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def distance_to(self, other: 'Position') -> float:
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)


@dataclass
class Inventory:
    """玩家/NPC 背包"""
    items: Dict[ResourceType, int] = field(default_factory=lambda: {
        ResourceType.WOOD: 0,
        ResourceType.STONE: 0,
        ResourceType.FOOD: 0,
        ResourceType.GOLD: 0,
    })
    
    def add(self, resource: ResourceType, amount: int) -> None:
        self.items[resource] += amount
    
    def has(self, resource: ResourceType, amount: int) -> bool:
        return self.items.get(resource, 0) >= amount
    
    def can_afford(self, cost: Dict[ResourceType, int]) -> bool:
        return all(self.has(r, a) for r, a in cost.items())
    
    def pay(self, cost: Dict[ResourceType, int]) -> bool:
        if not self.can_afford(cost):
            return False
        for r, a in cost.items():
            self.items[r] -= a
        return True
    
    def total_value(self) -> int:
        values = {ResourceType.WOOD: 1, ResourceType.STONE: 2, 
                  ResourceType.FOOD: 1, ResourceType.GOLD: 10}
        return sum(self.items[r] * values[r] for r in ResourceType if r != ResourceType.NONE)


# ═══════════════════════════════════════════════════════════
# 2. 程序化世界生成器（Infinigen 思路）
# ═══════════════════════════════════════════════════════════

class ProceduralWorldGenerator:
    """
    程序化世界生成器
    
    使用纯算法（不依赖神经网络）生成地形、资源、建筑、NPC。
    核心：多层噪声叠加 + 基于规则的元素放置。
    """
    
    def __init__(self, width: int = 64, height: int = 64, seed: Optional[int] = None):
        self.width = width
        self.height = height
        self.seed = seed or random.randint(0, 100000)
        random.seed(self.seed)
        np.random.seed(self.seed)
        
        # 预计算噪声
        self._noise_cache = {}
        
    def _hash(self, x: int, y: int, octave: int) -> float:
        """伪随机哈希函数（替代 Perlin 噪声，零外部依赖）"""
        key = (x * 374761393 + y * 668265263 + octave * 1274126177 + self.seed) & 0xFFFFFFFF
        key = (key ^ (key >> 13)) * 1274126177
        key = key ^ (key >> 16)
        return (key / 4294967295.0) * 2 - 1  # 映射到 [-1, 1]
    
    def _smooth_noise(self, x: float, y: float, octave: int) -> float:
        """平滑插值噪声"""
        x0, y0 = int(x), int(y)
        xf, yf = x - x0, y - y0
        
        # 四个角
        n00 = self._hash(x0, y0, octave)
        n10 = self._hash(x0 + 1, y0, octave)
        n01 = self._hash(x0, y0 + 1, octave)
        n11 = self._hash(x0 + 1, y0 + 1, octave)
        
        # 双线性插值（使用 smoothstep 曲线）
        u = xf * xf * (3 - 2 * xf)
        v = yf * yf * (3 - 2 * yf)
        
        nx0 = n00 * (1 - u) + n10 * u
        nx1 = n01 * (1 - u) + n11 * u
        
        return nx0 * (1 - v) + nx1 * v
    
    def _fbm(self, x: float, y: float, octaves: int = 6, lacunarity: float = 2.0, 
             persistence: float = 0.5) -> float:
        """分形布朗运动（Fractional Brownian Motion）"""
        value = 0.0
        amplitude = 1.0
        frequency = 1.0
        max_value = 0.0
        
        for _ in range(octaves):
            value += amplitude * self._smooth_noise(x * frequency, y * frequency, _)
            max_value += amplitude
            amplitude *= persistence
            frequency *= lacunarity
        
        return value / max_value  # 归一化到 [-1, 1]
    
    def generate_terrain(self) -> np.ndarray:
        """生成地形高度图并分类为离散地形类型"""
        terrain = np.zeros((self.height, self.width), dtype=np.int32)
        
        for y in range(self.height):
            for x in range(self.width):
                # 基础地形噪声
                h = self._fbm(x / 20.0, y / 20.0, octaves=6)
                
                # 添加大尺度趋势（让水域和山脉分布更自然）
                large_scale = self._fbm(x / 60.0, y / 60.0, octaves=3) * 0.3
                h = h * 0.7 + large_scale
                
                # 映射到 [0, 1]
                h = (h + 1) / 2
                h = np.clip(h, 0, 1)
                
                # 阈值分类
                if h < 0.30:
                    terrain[y, x] = TerrainType.WATER.value
                elif h < 0.40:
                    terrain[y, x] = TerrainType.SAND.value
                elif h < 0.60:
                    terrain[y, x] = TerrainType.PLAIN.value
                elif h < 0.80:
                    terrain[y, x] = TerrainType.FOREST.value
                else:
                    terrain[y, x] = TerrainType.MOUNTAIN.value
        
        return terrain
    
    def generate_resources(self, terrain: np.ndarray) -> np.ndarray:
        """基于地形规则生成资源"""
        resources = np.zeros((self.height, self.width), dtype=np.int32)
        
        for y in range(self.height):
            for x in range(self.width):
                t = terrain[y, x]
                
                # 资源生成概率（基于地形类型）
                if t == TerrainType.FOREST.value:
                    if random.random() < 0.4:
                        resources[y, x] = ResourceType.WOOD.value
                elif t == TerrainType.MOUNTAIN.value:
                    if random.random() < 0.5:
                        resources[y, x] = ResourceType.STONE.value
                elif t == TerrainType.PLAIN.value:
                    if random.random() < 0.2:
                        resources[y, x] = ResourceType.FOOD.value
                elif t == TerrainType.SAND.value:
                    if random.random() < 0.05:
                        resources[y, x] = ResourceType.GOLD.value
        
        return resources
    
    def generate_buildings(self, terrain: np.ndarray) -> np.ndarray:
        """程序化生成建筑（基于聚落规则）"""
        buildings = np.zeros((self.height, self.width), dtype=np.int32)
        
        # 寻找适合建聚落的区域（平原邻接水域）
        settlement_centers = []
        for y in range(2, self.height - 2):
            for x in range(2, self.width - 2):
                if terrain[y, x] == TerrainType.PLAIN.value:
                    # 检查邻接水域
                    has_water = False
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if terrain[y + dy, x + dx] == TerrainType.WATER.value:
                                has_water = True
                    if has_water and random.random() < 0.02:
                        settlement_centers.append((x, y))
        
        # 在聚落中心放置建筑
        for cx, cy in settlement_centers[:8]:  # 最多 8 个聚落
            # 放置中心建筑
            buildings[cy, cx] = BuildingType.HOUSE.value
            
            # 放置附属建筑
            for _ in range(random.randint(2, 5)):
                dx = random.randint(-2, 2)
                dy = random.randint(-2, 2)
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if terrain[ny, nx] == TerrainType.PLAIN.value:
                        btype = random.choice([
                            BuildingType.HOUSE.value,
                            BuildingType.WORKSHOP.value,
                            BuildingType.FARM.value
                        ])
                        buildings[ny, nx] = btype
        
        return buildings
    
    def generate_npcs(self, terrain: np.ndarray, buildings: np.ndarray) -> List['NPC']:
        """在聚落周围生成 NPC"""
        npcs = []
        
        # 找到所有建筑位置
        building_positions = []
        for y in range(self.height):
            for x in range(self.width):
                if buildings[y, x] != BuildingType.NONE.value:
                    building_positions.append(Position(x, y))
        
        # 在建筑附近生成 NPC
        for bp in building_positions:
            if random.random() < 0.6:
                role = random.choice(list(NPCRole))
                # 在附近找可行走位置
                for _ in range(20):
                    dx = random.randint(-3, 3)
                    dy = random.randint(-3, 3)
                    nx, ny = bp.x + dx, bp.y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        t = TerrainType(terrain[ny, nx])
                        if t.walkable:
                            npc = NPC(
                                pos=Position(nx, ny),
                                role=role,
                                name=f"NPC_{len(npcs)}"
                            )
                            npcs.append(npc)
                            break
        
        # 额外生成一些探索者
        for _ in range(5):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            t = TerrainType(terrain[y, x])
            if t.walkable and t != TerrainType.SAND:
                npcs.append(NPC(
                    pos=Position(x, y),
                    role=NPCRole.EXPLORER,
                    name=f"Explorer_{_}"
                ))
        
        return npcs


# ═══════════════════════════════════════════════════════════
# 3. 世界模型（Genie 思路简化版）
# ═══════════════════════════════════════════════════════════

class WorldModel:
    """
    简化世界模型
    
    核心思想：维护世界状态，预测动作后果。
    类似于 Genie 的底层动力学模型，但用规则系统实现。
    """
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        
        # 世界状态层
        self.terrain: np.ndarray = None
        self.resources: np.ndarray = None
        self.buildings: np.ndarray = None
        
        # 动态实体
        self.npcs: List['NPC'] = []
        self.player: Optional['Player'] = None
        
        # 生成器
        self.generator = ProceduralWorldGenerator(width, height)
        
        # 时间步
        self.time_step = 0
        
        # 历史记录（用于一致性检查）
        self.history: deque = deque(maxlen=100)
    
    def generate_world(self, seed: Optional[int] = None) -> None:
        """生成完整世界"""
        if seed is not None:
            self.generator.seed = seed
            self.generator = ProceduralWorldGenerator(self.width, self.height, seed)
        
        # 分层生成（程序化生成的典型管线）
        self.terrain = self.generator.generate_terrain()
        self.resources = self.generator.generate_resources(self.terrain)
        self.buildings = self.generator.generate_buildings(self.terrain)
        self.npcs = self.generator.generate_npcs(self.terrain, self.buildings)
        
        # 记录初始状态
        self._snapshot("init")
    
    def _snapshot(self, event: str) -> None:
        """记录世界快照"""
        self.history.append({
            'time': self.time_step,
            'event': event,
            'resource_count': int(np.sum(self.resources != 0)),
            'npc_count': len(self.npcs),
        })
    
    def is_valid_position(self, pos: Position) -> bool:
        """检查位置是否在世界范围内且可行走"""
        if not (0 <= pos.x < self.width and 0 <= pos.y < self.height):
            return False
        t = TerrainType(self.terrain[pos.y, pos.x])
        if not t.walkable:
            return False
        if self.buildings[pos.y, pos.x] != BuildingType.NONE.value:
            return False
        return True
    
    def predict_move(self, pos: Position, direction: Tuple[int, int]) -> Position:
        """预测移动结果（世界模型的核心函数）"""
        new_pos = pos + direction
        if self.is_valid_position(new_pos):
            return new_pos
        return pos
    
    def predict_gather(self, pos: Position) -> Optional[ResourceType]:
        """预测采集结果"""
        r = self.resources[pos.y, pos.x]
        if r != ResourceType.NONE.value:
            return ResourceType(r)
        return None
    
    def predict_build(self, pos: Position, building: BuildingType) -> bool:
        """预测建造可行性"""
        if not self.is_valid_position(pos):
            return False
        if self.resources[pos.y, pos.x] != ResourceType.NONE.value:
            return False
        # 检查是否在已有建筑旁边（聚落规则）
        has_neighbor = False
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                nx, ny = pos.x + dx, pos.y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.buildings[ny, nx] != BuildingType.NONE.value:
                        has_neighbor = True
        return has_neighbor
    
    def apply_action(self, entity: 'Entity', action: str, **kwargs) -> Dict:
        """
        执行动作并更新世界状态
        返回动作结果字典
        """
        result = {'success': False, 'message': ''}
        
        if action == 'move':
            direction = kwargs['direction']
            new_pos = self.predict_move(entity.pos, direction)
            if new_pos != entity.pos:
                entity.pos = new_pos
                result['success'] = True
                result['message'] = f"Moved to ({new_pos.x}, {new_pos.y})"
            else:
                result['message'] = "Cannot move there!"
        
        elif action == 'gather':
            resource = self.predict_gather(entity.pos)
            if resource and isinstance(entity, Player):
                entity.inventory.add(resource, 1)
                self.resources[entity.pos.y, entity.pos.x] = ResourceType.NONE.value
                result['success'] = True
                result['message'] = f"Gathered {resource.name}"
            else:
                result['message'] = "Nothing to gather here."
        
        elif action == 'build':
            building = kwargs['building']
            if self.predict_build(entity.pos, building):
                if isinstance(entity, Player) and entity.inventory.pay(building.cost):
                    self.buildings[entity.pos.y, entity.pos.x] = building.value
                    result['success'] = True
                    result['message'] = f"Built {building.name}"
                else:
                    result['message'] = "Not enough resources!"
            else:
                result['message'] = "Cannot build here!"
        
        self._snapshot(action)
        return result
    
    def tick(self) -> None:
        """推进世界时间（NPC 更新）"""
        self.time_step += 1
        for npc in self.npcs:
            npc.update(self)
        self._snapshot("tick")


# ═══════════════════════════════════════════════════════════
# 4. 实体系统
# ═══════════════════════════════════════════════════════════

@dataclass
class Entity:
    """基础实体"""
    pos: Position
    name: str
    symbol: str = 'E'
    color: str = '#FFFFFF'


@dataclass
class Player(Entity):
    """玩家实体"""
    pos: Position
    name: str = "Player"
    symbol: str = 'P'
    color: str = '#FF00FF'
    inventory: Inventory = field(default_factory=Inventory)
    vision_range: int = 8
    
    def get_visible_area(self, world: WorldModel) -> List[Position]:
        """获取玩家可见区域（视线系统）"""
        visible = []
        for dy in range(-self.vision_range, self.vision_range + 1):
            for dx in range(-self.vision_range, self.vision_range + 1):
                nx, ny = self.pos.x + dx, self.pos.y + dy
                if 0 <= nx < world.width and 0 <= ny < world.height:
                    if math.sqrt(dx*dx + dy*dy) <= self.vision_range:
                        visible.append(Position(nx, ny))
        return visible


@dataclass
class NPC(Entity):
    """NPC 实体"""
    pos: Position
    role: NPCRole
    name: str
    symbol: str = 'N'
    color: str = '#00FFFF'
    energy: int = 100
    target: Optional[Position] = None
    
    def __post_init__(self):
        self.color = {
            NPCRole.VILLAGER: '#FFD700',
            NPCRole.MERCHANT: '#9370DB',
            NPCRole.GUARD: '#DC143C',
            NPCRole.EXPLORER: '#00FA9A',
        }.get(self.role, '#00FFFF')
        self.symbol = {
            NPCRole.VILLAGER: 'V',
            NPCRole.MERCHANT: 'M',
            NPCRole.GUARD: 'G',
            NPCRole.EXPLORER: 'E',
        }.get(self.role, 'N')
    
    def update(self, world: WorldModel) -> None:
        """NPC 更新（简单 AI）"""
        if self.energy <= 0:
            self.energy = 100
            return
        
        # 选择目标
        if self.target is None or random.random() < 0.1:
            self._choose_target(world)
        
        # 向目标移动
        if self.target:
            dx = 0
            if self.target.x > self.pos.x:
                dx = 1
            elif self.target.x < self.pos.x:
                dx = -1
            
            dy = 0
            if self.target.y > self.pos.y:
                dy = 1
            elif self.target.y < self.pos.y:
                dy = -1
            
            # 尝试移动
            new_pos = world.predict_move(self.pos, (dx, dy))
            if new_pos != self.pos:
                self.pos = new_pos
                self.energy -= 1
            else:
                self.target = None  # 目标不可达
    
    def _choose_target(self, world: WorldModel) -> None:
        """选择新目标（基于角色）"""
        if self.role == NPCRole.VILLAGER:
            # 村民在附近徘徊
            self.target = Position(
                self.pos.x + random.randint(-5, 5),
                self.pos.y + random.randint(-5, 5)
            )
        elif self.role == NPCRole.EXPLORER:
            # 探索者向远处走
            self.target = Position(
                random.randint(0, world.width - 1),
                random.randint(0, world.height - 1)
            )
        elif self.role == NPCRole.GUARD:
            # 守卫在建筑附近巡逻
            buildings = []
            for y in range(world.height):
                for x in range(world.width):
                    if world.buildings[y, x] != BuildingType.NONE.value:
                        buildings.append(Position(x, y))
            if buildings:
                base = random.choice(buildings)
                self.target = Position(
                    base.x + random.randint(-3, 3),
                    base.y + random.randint(-3, 3)
                )
        elif self.role == NPCRole.MERCHANT:
            # 商人在聚落间移动
            self.target = Position(
                self.pos.x + random.randint(-10, 10),
                self.pos.y + random.randint(-10, 10)
            )


# ═══════════════════════════════════════════════════════════
# 5. 渲染系统
# ═══════════════════════════════════════════════════════════

class WorldRenderer:
    """Matplotlib 2D 渲染器"""
    
    def __init__(self, world: WorldModel, figsize: Tuple[int, int] = (14, 12)):
        self.world = world
        self.figsize = figsize
        self.fig = None
        self.ax = None
        self._init_display()
    
    def _init_display(self) -> None:
        """初始化显示窗口"""
        self.fig, self.ax = plt.subplots(figsize=self.figsize)
        self.ax.set_xlim(0, self.world.width)
        self.ax.set_ylim(0, self.world.height)
        self.ax.set_aspect('equal')
        self.ax.invert_yaxis()
        self.ax.set_title('Native AI Game - World Model', fontsize=14, fontweight='bold')
    
    def render(self, show_player_vision: bool = True) -> None:
        """渲染完整世界"""
        self.ax.clear()
        self.ax.set_xlim(0, self.world.width)
        self.ax.set_ylim(0, self.world.height)
        self.ax.set_aspect('equal')
        self.ax.invert_yaxis()
        self.ax.set_title(
            f'Native AI Game - World Model | Time: {self.world.time_step} | '
            f'NPCs: {len(self.world.npcs)}',
            fontsize=14, fontweight='bold'
        )
        
        # 1. 渲染地形（使用网格）
        for y in range(self.world.height):
            for x in range(self.world.width):
                t = TerrainType(self.world.terrain[y, x])
                rect = Rectangle((x, y), 1, 1, facecolor=t.color, edgecolor='none')
                self.ax.add_patch(rect)
        
        # 2. 渲染资源
        for y in range(self.world.height):
            for x in range(self.world.width):
                r = ResourceType(self.world.resources[y, x])
                if r != ResourceType.NONE:
                    circle = plt.Circle((x + 0.5, y + 0.5), 0.2, color=r.color, zorder=5)
                    self.ax.add_patch(circle)
        
        # 3. 渲染建筑
        for y in range(self.world.height):
            for x in range(self.world.width):
                b = BuildingType(self.world.buildings[y, x])
                if b != BuildingType.NONE:
                    fancy = FancyBboxPatch(
                        (x + 0.1, y + 0.1), 0.8, 0.8,
                        boxstyle="square,pad=0.02",
                        facecolor=b.color, edgecolor='black', linewidth=1.5, zorder=6
                    )
                    self.ax.add_patch(fancy)
        
        # 4. 渲染 NPC
        for npc in self.world.npcs:
            self.ax.text(
                npc.pos.x + 0.5, npc.pos.y + 0.5, npc.symbol,
                ha='center', va='center', fontsize=10, color='white',
                fontweight='bold', zorder=10,
                bbox=dict(boxstyle='circle', facecolor=npc.color, edgecolor='black')
            )
        
        # 5. 渲染玩家
        if self.world.player:
            # 视野范围
            if show_player_vision:
                visible = self.world.player.get_visible_area(self.world)
                for pos in visible:
                    rect = Rectangle(
                        (pos.x, pos.y), 1, 1,
                        facecolor='none', edgecolor='yellow', linewidth=0.5, alpha=0.3, zorder=2
                    )
                    self.ax.add_patch(rect)
            
            # 玩家标记
            self.ax.text(
                self.world.player.pos.x + 0.5, self.world.player.pos.y + 0.5,
                self.world.player.symbol,
                ha='center', va='center', fontsize=14, color='white',
                fontweight='bold', zorder=11,
                bbox=dict(boxstyle='circle', facecolor=self.world.player.color, 
                         edgecolor='black', linewidth=2)
            )
        
        # 6. 图例
        legend_elements = [
            plt.Rectangle((0,0),1,1, facecolor=TerrainType.WATER.color, label='Water'),
            plt.Rectangle((0,0),1,1, facecolor=TerrainType.SAND.color, label='Sand'),
            plt.Rectangle((0,0),1,1, facecolor=TerrainType.PLAIN.color, label='Plain'),
            plt.Rectangle((0,0),1,1, facecolor=TerrainType.FOREST.color, label='Forest'),
            plt.Rectangle((0,0),1,1, facecolor=TerrainType.MOUNTAIN.color, label='Mountain'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=ResourceType.WOOD.color, 
                      markersize=8, label='Wood'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=ResourceType.STONE.color, 
                      markersize=8, label='Stone'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=ResourceType.FOOD.color, 
                      markersize=8, label='Food'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=ResourceType.GOLD.color, 
                      markersize=8, label='Gold'),
        ]
        self.ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.02, 1), 
                      fontsize=9, title='Legend')
        
        plt.tight_layout()
    
    def render_ascii(self, viewport_size: int = 20) -> str:
        """ASCII 渲染（用于终端显示）"""
        if not self.world.player:
            return "No player!"
        
        px, py = self.world.player.pos.x, self.world.player.pos.y
        half = viewport_size // 2
        
        lines = []
        lines.append(f"{'═' * (viewport_size + 2)}")
        
        for dy in range(-half, half + 1):
            row = []
            for dx in range(-half, half + 1):
                nx, ny = px + dx, py + dy
                if 0 <= nx < self.world.width and 0 <= ny < self.world.height:
                    # 检查是否有玩家
                    if self.world.player and nx == px and ny == py:
                        row.append('P')
                        continue
                    
                    # 检查是否有 NPC
                    npc_here = False
                    for npc in self.world.npcs:
                        if npc.pos.x == nx and npc.pos.y == ny:
                            row.append(npc.symbol)
                            npc_here = True
                            break
                    if npc_here:
                        continue
                    
                    # 检查建筑
                    b = self.world.buildings[ny, nx]
                    if b != BuildingType.NONE.value:
                        row.append('B')
                        continue
                    
                    # 检查资源
                    r = self.world.resources[ny, nx]
                    if r != ResourceType.NONE.value:
                        row.append({
                            ResourceType.WOOD.value: 'w',
                            ResourceType.STONE.value: 's',
                            ResourceType.FOOD.value: 'f',
                            ResourceType.GOLD.value: 'g',
                        }.get(r, '?'))
                        continue
                    
                    # 地形
                    t = self.world.terrain[ny, nx]
                    row.append({
                        TerrainType.WATER.value: '~',
                        TerrainType.SAND.value: '.',
                        TerrainType.PLAIN.value: ',',
                        TerrainType.FOREST.value: 'T',
                        TerrainType.MOUNTAIN.value: '^',
                    }.get(t, '?'))
                else:
                    row.append(' ')
            
            lines.append('║' + ''.join(row) + '║')
        
        lines.append(f"{'═' * (viewport_size + 2)}")
        
        # 添加信息栏
        lines.append(f"  Player: ({px},{py}) | Resources: {self.world.player.inventory.items}")
        lines.append(f"  Time: {self.world.time_step} | NPCs: {len(self.world.npcs)}")
        lines.append("  Controls: w/a/s/d=move, g=gather, b=build house, q=quit")
        
        return '\n'.join(lines)
    
    def show(self) -> None:
        """显示当前帧"""
        self.fig.canvas.draw()
        plt.pause(0.001)
    
    def save(self, filename: str) -> None:
        """保存当前帧"""
        self.fig.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Saved to {filename}")


# ═══════════════════════════════════════════════════════════
# 6. 游戏引擎与主循环
# ═══════════════════════════════════════════════════════════

class GameEngine:
    """游戏引擎"""
    
    def __init__(self, world_size: int = 64, seed: Optional[int] = None):
        self.world = WorldModel(world_size, world_size)
        self.world.generate_world(seed)
        
        # 初始化玩家（放在可行走位置）
        self._spawn_player()
        
        self.renderer = WorldRenderer(self.world)
        self.running = False
    
    def _spawn_player(self) -> None:
        """在安全位置生成玩家"""
        for _ in range(1000):
            x = random.randint(0, self.world.width - 1)
            y = random.randint(0, self.world.height - 1)
            if self.world.is_valid_position(Position(x, y)):
                self.world.player = Player(pos=Position(x, y))
                return
        raise RuntimeError("Could not find valid spawn position!")
    
    def handle_input(self, key: str) -> Dict:
        """处理输入"""
        directions = {
            'w': (0, -1), 'W': (0, -1),
            's': (0, 1), 'S': (0, 1),
            'a': (-1, 0), 'A': (-1, 0),
            'd': (1, 0), 'D': (1, 0),
        }
        
        if key in directions:
            return self.world.apply_action(
                self.world.player, 'move', direction=directions[key]
            )
        
        elif key in ['g', 'G']:
            return self.world.apply_action(self.world.player, 'gather')
        
        elif key in ['b', 'B']:
            return self.world.apply_action(
                self.world.player, 'build', building=BuildingType.HOUSE
            )
        
        elif key in ['1', '2', '3', '4']:
            building = {
                '1': BuildingType.HOUSE,
                '2': BuildingType.WORKSHOP,
                '3': BuildingType.FARM,
                '4': BuildingType.TOWER,
            }.get(key)
            return self.world.apply_action(
                self.world.player, 'build', building=building
            )
        
        elif key in ['q', 'Q']:
            self.running = False
            return {'success': True, 'message': 'Quit'}
        
        elif key in ['t', 'T']:
            # 推进时间
            self.world.tick()
            return {'success': True, 'message': 'Time advanced'}
        
        elif key in ['h', 'H']:
            return {
                'success': True,
                'message': (
                    "Controls:\n"
                    "  w/a/s/d - Move\n"
                    "  g - Gather resource\n"
                    "  b/1 - Build House\n"
                    "  2 - Build Workshop\n"
                    "  3 - Build Farm\n"
                    "  4 - Build Tower\n"
                    "  t - Advance time (NPCs move)\n"
                    "  q - Quit\n"
                    "  h - Help"
                )
            }
        
        return {'success': False, 'message': f"Unknown command: {key}"}
    
    def run_interactive(self, mode: str = 'matplotlib') -> None:
        """运行交互式游戏"""
        self.running = True
        
        if mode == 'matplotlib':
            self._run_matplotlib_mode()
        else:
            self._run_ascii_mode()
    
    def _run_matplotlib_mode(self) -> None:
        """Matplotlib 交互模式"""
        print("=" * 60)
        print("  Native AI Game - World Model")
        print("  Controls: w/a/s/d=move, g=gather, b/1-4=build")
        print("  t=advance time, h=help, q=quit")
        print("  Click on the plot window and press keys")
        print("=" * 60)
        
        self.renderer.render()
        self.renderer.show()
        
        # 使用 matplotlib 的 key press 事件
        def on_key(event):
            if not self.running:
                return
            result = self.handle_input(event.key)
            print(f"[{event.key}] {result['message']}")
            
            # 自动推进 NPC
            self.world.tick()
            
            self.renderer.render()
            self.renderer.show()
        
        self.renderer.fig.canvas.mpl_connect('key_press_event', on_key)
        plt.show()
    
    def _run_ascii_mode(self) -> None:
        """ASCII 终端模式"""
        print("=" * 60)
        print("  Native AI Game - ASCII Mode")
        print("  Controls: w/a/s/d=move, g=gather, b=build, t=time, q=quit")
        print("=" * 60)
        
        while self.running:
            print('\n' + self.renderer.render_ascii())
            key = input("Command: ").strip()
            
            if not key:
                continue
            
            result = self.handle_input(key[0])
            print(f">>> {result['message']}")
            
            # 自动推进 NPC
            if key[0] in 'wasdWASDgGbB123':
                self.world.tick()
    
    def run_simulation(self, steps: int = 50, save_frames: bool = False) -> None:
        """运行自动模拟（用于观察世界演化）"""
        self.running = True
        
        for step in range(steps):
            self.world.tick()
            
            if step % 10 == 0:
                self.renderer.render()
                self.renderer.show()
                if save_frames:
                    self.renderer.save(f"frame_{step:04d}.png")
                print(f"Step {step}: {len(self.world.npcs)} NPCs, "
                      f"resources={np.sum(self.world.resources != 0)}")
        
        # 最终状态
        self.renderer.render()
        self.renderer.show()
        if save_frames:
            self.renderer.save("frame_final.png")
        
        print("\nSimulation complete!")
        print(f"Final state: time={self.world.time_step}, NPCs={len(self.world.npcs)}")


# ═══════════════════════════════════════════════════════════
# 7. 主入口
# ═══════════════════════════════════════════════════════════

def main():
    """主函数"""
    import sys
    
    # 解析命令行参数
    mode = 'matplotlib'
    size = 64
    seed = None
    
    for arg in sys.argv[1:]:
        if arg == '--ascii':
            mode = 'ascii'
        elif arg.startswith('--size='):
            size = int(arg.split('=')[1])
        elif arg.startswith('--seed='):
            seed = int(arg.split('=')[1])
    
    # 创建并运行游戏
    engine = GameEngine(world_size=size, seed=seed)
    
    if mode == 'matplotlib':
        engine.run_interactive('matplotlib')
    else:
        engine.run_interactive('ascii')


if __name__ == '__main__':
    main()
```

---

## 实验运行指南

### 环境要求

```
Python >= 3.8
NumPy >= 1.20
Matplotlib >= 3.3
```

### 安装依赖

```bash
pip install numpy matplotlib
```

### 运行方式

**方式一：Matplotlib 交互模式（推荐）**

```bash
python native_ai_world_game.py
```

点击图形窗口，按以下键控制：

| 按键 | 动作 | 说明 |
|------|------|------|
| `w/a/s/d` | 移动 | 上下左右移动玩家 |
| `g` | 采集 | 收集当前位置资源 |
| `b` / `1` | 建造房屋 | 消耗 5 木材 + 2 石材 |
| `2` | 建造工坊 | 消耗 8 木材 + 4 石材 |
| `3` | 建造农场 | 消耗 3 木材 + 2 食物 |
| `4` | 建造塔楼 | 消耗 10 石材 + 5 木材 + 2 黄金 |
| `t` | 推进时间 | NPC 自动行动 |
| `h` | 帮助 | 显示操作说明 |
| `q` | 退出 | 关闭游戏 |

**方式二：ASCII 终端模式**

```bash
python native_ai_world_game.py --ascii
```

**方式三：自动模拟模式**

修改 `main()` 函数调用 `engine.run_simulation(steps=100, save_frames=True)`。

### 可选参数

```bash
python native_ai_world_game.py --size=32 --seed=42      # 小世界 + 固定种子
python native_ai_world_game.py --ascii --size=48         # ASCII 模式 + 中等地图
```

---

## 实验分析

### 1. 程序化生成 vs 世界模型的对比

| 维度 | 本实验（融合） | 纯程序化（Infinigen） | 纯世界模型（Genie） |
|------|---------------|---------------------|-------------------|
| **世界生成** | 算法规则（噪声+阈值） | 几何节点 + 物理仿真 | 神经网络从视频学习 |
| **可预测性** | 高（确定性规则） | 高（参数驱动） | 低（概率生成） |
| **可编辑性** | 中（修改阈值即可） | 高（节点可视化编辑） | 低（黑箱） |
| **交互性** | 规则驱动状态转移 | 静态（无交互） | 高（物理一致） |
| **计算成本** | 低（CPU 即可） | 中（需要 Blender） | 高（GPU 推理） |
| **内容多样性** | 中（噪声参数变化） | 高（无限参数组合） | 高（数据驱动） |

### 2. 关键设计决策分析

**决策一：为什么用伪随机哈希而非标准 Perlin 噪声？**

- 原因：零外部依赖，便于理解底层数学。
- 实现：用线性同余哈希 + 双线性插值模拟平滑噪声。
- 局限：频谱不如 Perlin 噪声理想，但对演示目的足够。

**决策二：为什么 NPC 用规则 AI 而非神经网络？**

- 原因：本实验聚焦"世界生成"而非"智能体学习"。
- 对应：Genie 的底层世界模型也不负责 NPC 高层行为，只负责环境动力学。
- 扩展：可叠加 RL 智能体（参见实验 11 的 RL 模块）。

**决策三：为什么建筑需要邻接已有建筑？**

- 原因：模拟真实聚落形成（程序化生成为什么看起来"自然"）。
- 对应：Infinigen 使用物理和生态规则约束元素放置。

### 3. 扩展方向

1. **神经网络世界模型**：将 `WorldModel.predict_*` 替换为训练好的神经网络，从数据中学习状态转移。
2. **LLM 叙事层**：叠加 AI Dungeon 思路，用 LLM 生成 NPC 对话和动态任务。
3. **多智能体社会**：引入 Generative Agents 思路，让 NPC 有记忆、目标和社交关系。
4. **3D 升级**：将 2D 渲染替换为 PyTorch3D 或 Three.js，实现真正的 Infinigen 式 3D 生成。

---

## 实验检查清单

- [ ] 运行代码，观察地形生成（水域、平原、森林、山地的分布）
- [ ] 测试移动（w/a/s/d），确认碰撞检测和地形约束
- [ ] 测试采集（g），收集木材、石材、食物，观察背包变化
- [ ] 测试建造（b/1-4），在已有建筑旁边建造新建筑，确认资源扣除
- [ ] 推进时间（t），观察 NPC 移动和行为模式
- [ ] 修改 `seed` 参数，观察不同种子生成的世界差异
- [ ] 修改 `ProceduralWorldGenerator._fbm` 的 `octaves` 参数，观察地形细节变化
- [ ] 尝试将 `TerrainType` 的阈值改为不同值，观察地形分布变化
- [ ] 思考：如果要让这个世界"真正可玩"，还缺少哪些设计元素？
- [ ] 思考：如果加入神经网络世界模型，需要哪些训练数据？

---

## 面试谈资

### 30 秒版本

> 这个实验将 Infinigen 的程序化生成和 Genie 的世界模型融合到一个 2D 原型中。程序化生成用分形噪声+规则创建地形和资源，世界模型管理状态转移和交互预测。核心观察：程序化生成提供确定性和可编辑性，世界模型提供动态交互——两者结合是 Native AI Game 的可行路径。

### 2 分钟版本

> Native AI Game 有两个关键技术路径：程序化生成（Infinigen）和世界模型（Genie）。
> 
> 本实验展示了融合路径：
> 1. **地形层**用 fBm 噪声生成，通过阈值分类为离散地形。这体现了程序化生成的核心——用参数化规则生成无限内容。
> 2. **资源层**基于地形规则放置（森林产木材、山地产石材），模拟 Infinigen 的"生态约束"思路。
> 3. **建筑层**使用聚落规则——建筑必须邻接已有建筑，形成自然的聚落分布。
> 4. **交互层**用 WorldModel 类封装状态转移，这是 Genie"世界模型即引擎"的简化版。
> 5. **NPC 层**用目标驱动 AI，每个 NPC 有角色和目标选择逻辑。
> 
> 关键设计洞见：程序化生成和世界模型不是互斥的。程序化生成提供**基础内容的确定性和可编辑性**，世界模型提供**动态交互的涌现性**。在真实游戏中，可以用程序化生成创建基础世界，再用神经网络添加动态内容（如 NPC 行为、叙事事件），这是 Native AI Game 的实用架构。

---

## 相关资源

| 资源 | 类型 | 链接 | 备注 |
|------|------|------|------|
| Genie | 项目 | DeepMind | 生成式交互环境 |
| Infinigen | 项目 | https://infinigen.org | 程序化 3D 场景 |
| AI Dungeon | 产品 | https://aidungeon.io | 文本 LLM 驱动游戏 |
| Perlin Noise | 教程 | https://en.wikipedia.org/wiki/Perlin_noise | 噪声生成基础 |
| fBm | 教程 | https://en.wikipedia.org/wiki/Fractional_Brownian_motion | 分形布朗运动 |

---

*实验文件版本: 1.0*  
*创建日期: 2026-07-13*  
*维护者: AIResearchVault*
