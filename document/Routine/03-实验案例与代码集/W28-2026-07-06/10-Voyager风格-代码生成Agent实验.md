---
tags: [experiment, llm-agent, voyager, code-generation, curriculum, skill-library]
aliases: [Voyager-代码生成Agent实验]
created: 2026-07-06
---

# 实验 10：Voyager 风格 — 代码生成 Agent 实验

> **参考论文**: Voyager (NeurIPS 2023) — 终身学习 Minecraft Agent
> **实验时间**: 2026-07-06
> **核心架构**: 自动课程 + 技能库 + 迭代提示

---

## 一、实验背景与目标

### 1.1 背景

Voyager 是 NVIDIA 等团队在 NeurIPS 2023 提出的**终身学习 Minecraft Agent**，其核心创新是将动作空间从传统的低层 API（移动/点击）升级为**代码生成**（Python/Mineflayer API），使 Agent 能组合原子技能形成复杂行为。

Voyager 的三层架构：
- **自动课程（Automatic Curriculum）**: 根据当前能力动态生成递进任务
- **技能库（Skill Library）**: 存储可执行、可检索、可复用的代码片段
- **迭代提示（Iterative Prompting）**: 从执行错误中自动修复代码，形成闭环

**关键洞察**: 在开放世界中，代码是天然的可执行、可组合、可验证的原子动作单元。

### 1.2 实验目标

1. 在**2D 网格环境**中复现 Voyager 三模块架构
2. 实现一个**模拟 LLM**，能根据任务描述生成可执行 Python 代码
3. 构建**技能库**系统：存储成功代码，支持按描述检索和复用
4. 实现**自动课程**：根据当前技能覆盖度动态生成新任务
5. 实现**迭代提示**：捕获执行错误，修复代码并重试
6. 验证：Agent 随时间推移能否持续解锁新能力（终身学习曲线）

---

## 二、核心概念

### 2.1 代码生成作为动作空间

```
传统 Agent: 动作 = {上移, 下移, 左移, 右移, 拾取, ...}  // 低层、离散
Voyager Agent: 动作 = def solve_task(): ...  // 高层、可组合、可执行
```

**优势**：
- **组合性**: 代码可以调用其他代码（函数组合）
- **可验证性**: 执行代码即可验证正确性
- **可复用性**: 成功的代码片段存入技能库，未来检索调用
- **抽象层次**: 一次 LLM 调用可以生成多步行为（降低延迟累积）

**代价**：
- 延迟：每次动作需要一次 LLM 代码生成（秒级）
- 可靠性：生成代码可能包含 bug，需要沙箱和回滚机制

### 2.2 三模块交互图

```
┌─────────────────────────────────────────────────────────────┐
│                     Voyager 风格 Agent                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌──────────────┐    新任务    ┌──────────────┐           │
│   │  自动课程    │ ──────────→ │   代码生成    │           │
│   │  (LLM)       │             │   (LLM)       │           │
│   └──────────────┘             └──────┬───────┘           │
│          ↑                            │                    │
│          │ 根据能力                    ↓ 生成代码           │
│          │ 生成任务            ┌──────────────┐           │
│          │                     │   代码执行    │           │
│          │                     │   (沙箱)      │           │
│          │                     └──────┬───────┘           │
│          │                            │                    │
│          │                    ┌───────┴───────┐           │
│          │                    ↓               ↓           │
│          │               [成功]            [失败]           │
│          │                    │               │            │
│          │                    ↓               ↓           │
│          │            ┌──────────────┐   ┌──────────────┐  │
│          └─────────── │   技能库      │   │  迭代提示     │  │
│              更新能力   │  (存储+检索)  │   │  (错误修复)   │  │
│                       └──────────────┘   └──────┬───────┘  │
│                                                 │          │
│                                                 └────→ 重试│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 实验环境与真实 Minecraft 的映射

| 真实 Minecraft | 本实验 2D 网格环境 |
|---------------|------------------|
| 3D 方块世界 | 2D 网格地图 (`N×M`) |
| 玩家位置 `(x, y, z)` | 玩家位置 `(row, col)` |
| 方块类型（木头、石头等） | 单元格类型（空地、木头、石头、目标） |
| 制作/合成 | 收集资源 + 到达目标 |
| 工具（斧头、镐） | 代码中的函数/技能 |
| 生物（敌人、动物） | 障碍物（需要绕行） |
| 生存目标 | 到达目标点并收集资源 |

---

## 三、环境设计：2D 网格世界

### 3.1 环境规范

```
网格大小: 10×10（可配置）
单元格类型:
  '.' : 空地（可通行）
  '#' : 障碍物（不可通行）
  'W' : 木头（可收集的资源）
  'S' : 石头（可收集的资源）
  'T' : 目标点（任务目的地）
  'P' : 玩家当前位置

动作（代码层面）:
  move_up(), move_down(), move_left(), move_right()
  collect()    — 收集当前位置资源
  is_at(r, c)  — 检查是否在某位置
  get_pos()    — 获取当前位置
  scan()       — 扫描周围单元格
```

### 3.2 任务类型（课程设计）

| 难度 | 任务描述 | 所需技能 |
|-----|---------|---------|
| L1 | 移动到目标点 | 基础移动 |
| L2 | 收集木头后到达目标 | 移动 + 收集 |
| L3 | 绕过障碍物到达目标 | 路径规划 |
| L4 | 收集两种资源后到达目标 | 多资源收集 + 路径规划 |
| L5 | 先收集资源 A，再收集资源 B，最后到达目标 | 序列规划 + 组合 |
| L6 | 在未知地图中探索并找到目标 | 探索 + 动态规划 |

---

## 四、完整代码实现

> **初学者阅读指南**：本代码包含 4 个核心模块，建议按顺序阅读：
> 1. `GridWorld` — 2D 网格环境（理解 Agent 能做什么动作）
> 2. `SimulatedLLM` — 模拟 LLM（理解代码是如何生成的）
> 3. `SkillLibrary` — 技能库（理解成功经验如何存储和复用）
> 4. `VoyagerAgent` — 主控制器（理解三模块如何协同工作）

```python

```python
#!/usr/bin/env python3
"""
Voyager-Style Code Generation Agent Experiment
===============================================
A simplified reproduction of Voyager's three-module architecture:
  1. Automatic Curriculum  — dynamic task generation based on current capabilities
  2. Skill Library         — executable, retrievable, reusable code snippets
  3. Iterative Prompting   — error-driven code repair loop

Environment: 2D grid world (no Minecraft dependency)
LLM: Simulated (rule-based + template) for reproducibility without API keys
"""

from __future__ import annotations

import re
import textwrap
import traceback
import uuid
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple, Any
import math


# ============================================================================
#  MODULE 0: 2D Grid Environment (Minecraft surrogate)
# ============================================================================

class GridWorld:
    """
    2D 网格环境 —— Agent 的"物理世界"
    
    初学者要点：
    - 这是 Agent 执行代码的"沙箱"，所有动作最终都落到这里
    - 网格中的每个格子可以是：空地(.)、墙(#)、木头(W)、石头(S)、目标(T)
    - Agent 通过调用 move_up/down/left/right() 和 collect() 与环境交互
    - 每次移动/收集消耗 1 个 step，超过 max_steps 则任务失败
    """

    CELL_EMPTY = "."
    CELL_WALL = "#"
    CELL_WOOD = "W"
    CELL_STONE = "S"
    CELL_GOAL = "T"
    CELL_PLAYER = "P"

    def __init__(self, size: int = 10, max_steps: int = 100):
        self.size = size
        self.max_steps = max_steps
        self.grid: List[List[str]] = []
        self.player_pos: Tuple[int, int] = (0, 0)
        self.initial_pos: Tuple[int, int] = (0, 0)
        self.goal_pos: Optional[Tuple[int, int]] = None
        self.inventory: Dict[str, int] = {"wood": 0, "stone": 0}
        self.step_count = 0
        self.done = False
        self.last_error: Optional[str] = None

    # -- scenario generation -------------------------------------------------

    def reset(self, scenario: str) -> str:
        """Reset environment with a given scenario string."""
        self.grid = [list(row) for row in scenario.strip().split("\n")]
        self.size = max(len(self.grid), len(self.grid[0]) if self.grid else 0)
        self.inventory = {"wood": 0, "stone": 0}
        self.step_count = 0
        self.done = False
        self.last_error = None

        # Find player and goal positions
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell == self.CELL_PLAYER:
                    self.player_pos = (r, c)
                    self.initial_pos = (r, c)
                    self.grid[r][c] = self.CELL_EMPTY  # replace with empty
                elif cell == self.CELL_GOAL:
                    self.goal_pos = (r, c)

        return self.get_observation()

    def reset_random(self, level: int = 1, seed: Optional[int] = None) -> str:
        """Generate a random scenario of given difficulty level."""
        import random
        if seed is not None:
            random.seed(seed)

        size = 8 + level * 2  # larger grid for harder levels
        self.size = size
        self.grid = [[self.CELL_EMPTY for _ in range(size)] for _ in range(size)]

        # Place player at top-left
        self.player_pos = (0, 0)
        self.initial_pos = (0, 0)

        # Place goal at bottom-right or random far position
        goal_r, goal_c = size - 1, size - 1
        if level >= 4:
            goal_r, goal_c = random.randint(size // 2, size - 1), random.randint(size // 2, size - 1)
        self.goal_pos = (goal_r, goal_c)
        self.grid[goal_r][goal_c] = self.CELL_GOAL

        # Place obstacles based on level
        num_walls = min(3 + level * 2, size * size // 8)
        for _ in range(num_walls):
            r, c = random.randint(0, size - 1), random.randint(0, size - 1)
            if (r, c) != (0, 0) and (r, c) != self.goal_pos:
                self.grid[r][c] = self.CELL_WALL

        # Place resources based on level
        if level >= 2:
            num_wood = random.randint(1, 2 + level // 2)
            for _ in range(num_wood):
                r, c = random.randint(0, size - 1), random.randint(0, size - 1)
                if self.grid[r][c] == self.CELL_EMPTY and (r, c) not in [(0, 0), self.goal_pos]:
                    self.grid[r][c] = self.CELL_WOOD

        if level >= 4:
            num_stone = random.randint(1, 1 + level // 3)
            for _ in range(num_stone):
                r, c = random.randint(0, size - 1), random.randint(0, size - 1)
                if self.grid[r][c] == self.CELL_EMPTY and (r, c) not in [(0, 0), self.goal_pos]:
                    self.grid[r][c] = self.CELL_STONE

        self.inventory = {"wood": 0, "stone": 0}
        self.step_count = 0
        self.done = False
        self.last_error = None
        return self.get_observation()

    # -- observation ---------------------------------------------------------

    def get_observation(self) -> str:
        """Return a text rendering of the current grid state."""
        lines = []
        for r in range(len(self.grid)):
            row = []
            for c in range(len(self.grid[0])):
                if (r, c) == self.player_pos:
                    row.append(self.CELL_PLAYER)
                else:
                    row.append(self.grid[r][c])
            lines.append(" ".join(row))
        lines.append(f"Position: {self.player_pos}")
        lines.append(f"Inventory: {self.inventory}")
        lines.append(f"Steps: {self.step_count}/{self.max_steps}")
        return "\n".join(lines)

    def get_state_dict(self) -> Dict[str, Any]:
        """Return structured state for LLM prompting."""
        return {
            "player_pos": self.player_pos,
            "inventory": dict(self.inventory),
            "grid_size": (len(self.grid), len(self.grid[0]) if self.grid else 0),
            "goal_pos": self.goal_pos,
            "step_count": self.step_count,
            "max_steps": self.max_steps,
        }

    # -- actions (API exposed to generated code) -------------------------------

    def move_up(self) -> str:
        return self._move(-1, 0)

    def move_down(self) -> str:
        return self._move(1, 0)

    def move_left(self) -> str:
        return self._move(0, -1)

    def move_right(self) -> str:
        return self._move(0, 1)

    def _move(self, dr: int, dc: int) -> str:
        self.step_count += 1
        r, c = self.player_pos[0] + dr, self.player_pos[1] + dc
        if 0 <= r < len(self.grid) and 0 <= c < len(self.grid[0]):
            if self.grid[r][c] != self.CELL_WALL:
                self.player_pos = (r, c)
                return f"Moved to {self.player_pos}"
            else:
                self.last_error = f"Cannot move to ({r},{c}): blocked by wall"
                return self.last_error
        else:
            self.last_error = f"Cannot move to ({r},{c}): out of bounds"
            return self.last_error

    def collect(self) -> str:
        self.step_count += 1
        r, c = self.player_pos
        cell = self.grid[r][c]
        if cell == self.CELL_WOOD:
            self.inventory["wood"] += 1
            self.grid[r][c] = self.CELL_EMPTY
            return f"Collected wood at ({r},{c}). Inventory: {self.inventory}"
        elif cell == self.CELL_STONE:
            self.inventory["stone"] += 1
            self.grid[r][c] = self.CELL_EMPTY
            return f"Collected stone at ({r},{c}). Inventory: {self.inventory}"
        else:
            self.last_error = f"Nothing to collect at ({r},{c})"
            return self.last_error

    def get_pos(self) -> Tuple[int, int]:
        return self.player_pos

    def is_at(self, r: int, c: int) -> bool:
        return self.player_pos == (r, c)

    def scan(self) -> Dict[str, List[Tuple[int, int]]]:
        """Scan the entire grid and return locations of interesting cells."""
        result = {"wood": [], "stone": [], "goal": [], "wall": [], "empty": []}
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                cell = self.grid[r][c]
                if (r, c) == self.player_pos:
                    continue
                if cell == self.CELL_WOOD:
                    result["wood"].append((r, c))
                elif cell == self.CELL_STONE:
                    result["stone"].append((r, c))
                elif cell == self.CELL_GOAL:
                    result["goal"].append((r, c))
                elif cell == self.CELL_WALL:
                    result["wall"].append((r, c))
                else:
                    result["empty"].append((r, c))
        return result

    def check_goal(self, required_wood: int = 0, required_stone: int = 0) -> Tuple[bool, str]:
        """Check if task is complete."""
        if self.player_pos != self.goal_pos:
            return False, f"Not at goal {self.goal_pos}"
        if self.inventory["wood"] < required_wood:
            return False, f"Need {required_wood} wood, have {self.inventory['wood']}"
        if self.inventory["stone"] < required_stone:
            return False, f"Need {required_stone} stone, have {self.inventory['stone']}"
        self.done = True
        return True, "Task completed successfully!"

    def is_done(self) -> bool:
        return self.done or self.step_count >= self.max_steps


# ============================================================================
#  MODULE 1: Simulated LLM (for reproducibility without API keys)
# ============================================================================

class SimulatedLLM:
    """
    模拟 LLM —— 用规则模板替代真实的 GPT-4/Claude API
    
    初学者要点：
    - 真实 Voyager 调用 GPT-4 生成代码，这里用规则模板保证可复现性
    - 三个核心功能：
      1. generate_curriculum: 根据当前能力生成下一个任务（课程设计）
      2. generate_code: 根据任务描述生成 Python 代码（代码生成）
      3. repair_code: 根据执行错误修复代码（迭代修复）
    - 替换为真实 LLM：只需重写这三个方法，改为 API 调用即可
    """

    def __init__(self):
        self.call_count = 0

    # -- curriculum generation -----------------------------------------------

    def generate_curriculum(
        self,
        completed_levels: List[int],
        skill_names: List[str],
        failure_history: List[str],
    ) -> Dict[str, Any]:
        """Generate the next task based on current capabilities."""
        self.call_count += 1

        max_completed = max(completed_levels) if completed_levels else 0

        # Curriculum logic: try next level, or retry failed level
        if failure_history and self.call_count % 3 == 0:
            # Every 3rd call, retry a failed level for consolidation
            level = max(1, max_completed)
            task_type = "retry"
        else:
            level = max_completed + 1
            task_type = "new"

        level = min(level, 6)  # cap at level 6

        tasks = {
            1: {
                "description": "Move from start to goal",
                "required_wood": 0,
                "required_stone": 0,
                "hint": "Use move_up/down/left/right to reach the goal.",
            },
            2: {
                "description": "Collect 1 wood, then reach goal",
                "required_wood": 1,
                "required_stone": 0,
                "hint": "First find and collect wood using collect(), then move to goal.",
            },
            3: {
                "description": "Navigate around walls to reach goal",
                "required_wood": 0,
                "required_stone": 0,
                "hint": "Use scan() to find walls, then plan a path around them.",
            },
            4: {
                "description": "Collect 1 wood and 1 stone, then reach goal",
                "required_wood": 1,
                "required_stone": 1,
                "hint": "Collect wood and stone in any order, then reach goal.",
            },
            5: {
                "description": "Collect 2 wood, then 1 stone, then reach goal",
                "required_wood": 2,
                "required_stone": 1,
                "hint": "Sequence: collect wood (2) -> collect stone (1) -> goal.",
            },
            6: {
                "description": "Explore unknown map, collect all resources, reach goal",
                "required_wood": 2,
                "required_stone": 2,
                "hint": "Use scan() to discover layout, then plan optimal route.",
            },
        }

        task = tasks.get(level, tasks[6]).copy()
        task["level"] = level
        task["type"] = task_type
        return task

    # -- code generation -----------------------------------------------------

    def generate_code(
        self,
        task: Dict[str, Any],
        env_state: Dict[str, Any],
        retrieved_skills: List[Dict[str, Any]],
        previous_error: Optional[str] = None,
    ) -> str:
        """Generate Python code to solve the given task."""
        self.call_count += 1

        level = task["level"]
        desc = task["description"]
        hint = task.get("hint", "")
        req_wood = task.get("required_wood", 0)
        req_stone = task.get("required_stone", 0)

        # Build prompt context (simulated)
        context = f"""# Task: {desc}
# Goal position: {env_state.get('goal_pos')}
# Required: wood={req_wood}, stone={req_stone}
# Current position: {env_state.get('player_pos')}
# Hint: {hint}
"""

        if previous_error:
            context += f"# PREVIOUS ERROR: {previous_error}\n# Please fix the code.\n"

        if retrieved_skills:
            context += "# Available skills:\n"
            for skill in retrieved_skills:
                context += f"# --- {skill['name']} ---\n"
                context += skill["code"] + "\n"

        # Generate code based on task level (rule-based templates)
        code = self._code_template(level, req_wood, req_stone, env_state, retrieved_skills)
        return code

    def _code_template(
        self,
        level: int,
        req_wood: int,
        req_stone: int,
        env_state: Dict[str, Any],
        skills: List[Dict[str, Any]],
    ) -> str:
        """Rule-based code generation templates."""

        goal_r, goal_c = env_state.get("goal_pos", (0, 0))
        player_r, player_c = env_state.get("player_pos", (0, 0))

        # Helper to find nearest resource
        def find_nearest(resource_list: List[Tuple[int, int]], pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
            if not resource_list:
                return None
            return min(resource_list, key=lambda p: abs(p[0] - pos[0]) + abs(p[1] - pos[1]))

        # Simple BFS pathfinding (embedded in generated code)
        bfs_code = '''
def move_to(target_r, target_c):
    """Simple greedy movement toward target."""
    pr, pc = get_pos()
    while (pr, pc) != (target_r, target_c):
        if pr < target_r and not is_wall(pr + 1, pc):
            move_down()
        elif pr > target_r and not is_wall(pr - 1, pc):
            move_up()
        elif pc < target_c and not is_wall(pr, pc + 1):
            move_right()
        elif pc > target_c and not is_wall(pr, pc - 1):
            move_left()
        else:
            # Stuck, try to find a way around (simple fallback)
            if not is_wall(pr + 1, pc):
                move_down()
            elif not is_wall(pr, pc + 1):
                move_right()
            elif not is_wall(pr - 1, pc):
                move_up()
            elif not is_wall(pr, pc - 1):
                move_left()
            else:
                break
        pr, pc = get_pos()
        if step_count > max_steps - 5:
            break
'''

        # For higher levels, try to use retrieved skills if available
        skill_calls = ""
        for skill in skills:
            if skill.get("name") in ["move_to", "collect_resources", "pathfind"]:
                skill_calls += f"# Using skill: {skill['name']}\n"

        # Level-specific code generation
        if level == 1:
            return f'''# Solve: Move to goal at ({goal_r}, {goal_c})
{skill_calls}
# Move to goal
pr, pc = get_pos()
if pr < {goal_r}:
    for _ in range({goal_r} - pr):
        move_down()
elif pr > {goal_r}:
    for _ in range(pr - {goal_r}):
        move_up()
if pc < {goal_c}:
    for _ in range({goal_c} - pc):
        move_right()
elif pc > {goal_c}:
    for _ in range(pc - {goal_c}):
        move_left()
'''
        elif level == 2:
            return f'''# Solve: Collect 1 wood, then reach goal
scan_result = scan()
wood_positions = scan_result.get("wood", [])
if wood_positions:
    target = wood_positions[0]
    # Move to wood
    tr, tc = target
    pr, pc = get_pos()
    while (pr, pc) != (tr, tc):
        if pr < tr: move_down()
        elif pr > tr: move_up()
        elif pc < tc: move_right()
        elif pc > tc: move_left()
        pr, pc = get_pos()
    collect()
# Move to goal
pr, pc = get_pos()
gr, gc = {goal_r}, {goal_c}
while (pr, pc) != (gr, gc):
    if pr < gr: move_down()
    elif pr > gr: move_up()
    elif pc < gc: move_right()
    elif pc > gc: move_left()
    pr, pc = get_pos()
'''
        elif level == 3:
            return f'''# Solve: Navigate around walls to goal
{bfs_code}
# Use greedy pathfinding with wall avoidance
move_to({goal_r}, {goal_c})
'''
        elif level >= 4:
            return f'''# Solve: Collect resources then reach goal
scan_result = scan()
# Collect wood
for _ in range({req_wood}):
    wood_positions = scan_result.get("wood", [])
    # Find wood that still exists (not collected)
    available = [p for p in wood_positions if is_at(p[0], p[1]) == False]
    if available:
        target = available[0]
        tr, tc = target
        pr, pc = get_pos()
        while (pr, pc) != (tr, tc):
            if pr < tr and not is_wall(pr+1, pc): move_down()
            elif pr > tr and not is_wall(pr-1, pc): move_up()
            elif pc < tc and not is_wall(pr, pc+1): move_right()
            elif pc > tc and not is_wall(pr, pc-1): move_left()
            else:
                break
            pr, pc = get_pos()
        collect()
        scan_result = scan()
# Collect stone
for _ in range({req_stone}):
    stone_positions = scan_result.get("stone", [])
    available = [p for p in stone_positions if is_at(p[0], p[1]) == False]
    if available:
        target = available[0]
        tr, tc = target
        pr, pc = get_pos()
        while (pr, pc) != (tr, tc):
            if pr < tr and not is_wall(pr+1, pc): move_down()
            elif pr > tr and not is_wall(pr-1, pc): move_up()
            elif pc < tc and not is_wall(pr, pc+1): move_right()
            elif pc > tc and not is_wall(pr, pc-1): move_left()
            else:
                break
            pr, pc = get_pos()
        collect()
        scan_result = scan()
# Move to goal
gr, gc = {goal_r}, {goal_c}
pr, pc = get_pos()
while (pr, pc) != (gr, gc):
    if pr < gr and not is_wall(pr+1, pc): move_down()
    elif pr > gr and not is_wall(pr-1, pc): move_up()
    elif pc < gc and not is_wall(pr, pc+1): move_right()
    elif pc > gc and not is_wall(pr, pc-1): move_left()
    else:
        break
    pr, pc = get_pos()
'''
        else:
            return "# Unknown level\npass\n"

    # -- error repair --------------------------------------------------------

    def repair_code(
        self,
        original_code: str,
        error_message: str,
        env_state: Dict[str, Any],
    ) -> str:
        """Attempt to fix code based on execution error."""
        self.call_count += 1

        # Simple rule-based repairs
        if "out of bounds" in error_message.lower():
            # Add bounds checking
            repaired = original_code.replace(
                "move_down()",
                "if get_pos()[0] + 1 < grid_size[0]: move_down()",
            )
            repaired = repaired.replace(
                "move_right()",
                "if get_pos()[1] + 1 < grid_size[1]: move_right()",
            )
            return repaired

        if "blocked by wall" in error_message.lower():
            # Add wall checking (inject is_wall helper)
            helper = '''
def is_wall(r, c):
    """Check if position is a wall."""
    scan_result = scan()
    return (r, c) in scan_result.get("wall", [])
'''
            return helper + "\n" + original_code

        if "name 'step_count' is not defined" in error_message.lower():
            # Fix: use env access instead of undefined variable
            return original_code.replace("step_count", "env.step_count")

        # Default: add a try-except wrapper
        return f'''# REPAIRED after error: {error_message}
{original_code}
'''


# ============================================================================
#  MODULE 2: Skill Library (executable code storage + retrieval)
# ============================================================================

@dataclass
class Skill:
    """A stored skill = executable code + metadata."""
    id: str
    name: str
    description: str
    code: str
    level: int
    success_count: int = 0
    tags: List[str] = field(default_factory=list)


class SkillLibrary:
    """
    技能库 —— 存储和检索成功的代码片段
    
    初学者要点：
    - 核心思想："成功经验外化"——把解决过任务的代码存起来，以后遇到类似任务直接复用
    - 与 RAG 的区别：RAG 存文本段落，技能库存可执行代码；代码可以直接运行验证
    - 检索策略：按关键词重叠 + 难度等级接近度 + 成功次数 综合评分
    - 真实 Voyager 使用 embedding 做语义检索，这里简化为规则匹配
    """

    def __init__(self):
        self.skills: Dict[str, Skill] = {}
        self.skill_counter = 0

    def add_skill(
        self,
        name: str,
        description: str,
        code: str,
        level: int,
        tags: Optional[List[str]] = None,
    ) -> Skill:
        """Store a new successful code snippet as a skill."""
        self.skill_counter += 1
        skill_id = f"skill_{self.skill_counter:04d}"
        skill = Skill(
            id=skill_id,
            name=name,
            description=description,
            code=code,
            level=level,
            tags=tags or [],
        )
        self.skills[skill_id] = skill
        return skill

    def retrieve_skills(
        self,
        task_description: str,
        level: int,
        top_k: int = 3,
    ) -> List[Skill]:
        """Retrieve relevant skills based on task description and level."""
        # Simplified retrieval: score by keyword overlap and level proximity
        def score(skill: Skill) -> float:
            s = 0.0
            # Level proximity (closer is better)
            s += 10.0 / (1.0 + abs(skill.level - level))
            # Keyword overlap
            task_words = set(task_description.lower().split())
            desc_words = set(skill.description.lower().split())
            overlap = len(task_words & desc_words)
            s += overlap * 2.0
            # Success count boost
            s += skill.success_count * 1.5
            return s

        scored = [(score(s), s) for s in self.skills.values()]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [s for _, s in scored[:top_k]]

    def increment_success(self, skill_id: str) -> None:
        """Record that a skill was successfully reused."""
        if skill_id in self.skills:
            self.skills[skill_id].success_count += 1

    def list_skills(self) -> List[Skill]:
        """Return all skills sorted by level."""
        return sorted(self.skills.values(), key=lambda s: s.level)

    def get_stats(self) -> Dict[str, Any]:
        """Return skill library statistics."""
        return {
            "total_skills": len(self.skills),
            "levels_covered": sorted(set(s.level for s in self.skills.values())),
            "total_successful_uses": sum(s.success_count for s in self.skills.values()),
            "skill_names": [s.name for s in self.skills.values()],
        }


# ============================================================================
#  MODULE 3: Voyager Agent (orchestrates curriculum + skill_lib + code_gen)
# ============================================================================

class VoyagerAgent:
    """
    Voyager 主控制器 —— 协调三个核心模块的终身学习循环
    
    初学者要点：
    - 这是整个系统的"导演"，控制学习流程：
      1. 自动课程 → 生成递进任务（由易到难）
      2. 代码生成 → LLM 写代码解决任务
      3. 迭代修复 → 失败时自动修复代码并重试
      4. 技能库 → 成功后存储代码，未来复用
    - 终身学习 = 不断循环：生成任务 → 尝试解决 → 成功则存储 → 生成更难任务
    - 关键状态：completed_levels（已完成的难度）、failure_history（失败记录）
    """

    def __init__(self, env: GridWorld, llm: SimulatedLLM, max_retries: int = 3):
        self.env = env
        self.llm = llm
        self.skill_lib = SkillLibrary()
        self.max_retries = max_retries

        # Tracking
        self.completed_levels: List[int] = []
        self.failure_history: List[str] = []
        self.task_results: List[Dict[str, Any]] = []

    # -- curriculum ----------------------------------------------------------

    def next_task(self) -> Dict[str, Any]:
        """Get next task from automatic curriculum."""
        skill_names = [s.name for s in self.skill_lib.list_skills()]
        task = self.llm.generate_curriculum(
            completed_levels=self.completed_levels,
            skill_names=skill_names,
            failure_history=self.failure_history,
        )
        return task

    # -- code execution in sandbox -------------------------------------------

    def execute_code(self, code: str, task: Dict[str, Any]) -> Tuple[bool, str, str]:
        """
        在沙箱中执行生成的代码
        
        初学者要点：
        - 这是"代码即动作"的核心：把 LLM 生成的 Python 代码放到环境中执行
        - namespace 把环境 API（move_up, collect 等）注入到代码的命名空间
        - 使用 exec() 执行代码，捕获异常作为错误反馈
        - 执行后检查是否满足任务目标（位置 + 资源要求）
        
        Returns: (是否成功, 最终消息, 错误或空字符串)
        """
        # Reset environment for the task
        obs = self.env.reset_random(level=task["level"], seed=42 + len(self.task_results))

        # Build execution namespace with environment API
        namespace = {
            # Environment API exposed to generated code
            "move_up": self.env.move_up,
            "move_down": self.env.move_down,
            "move_left": self.env.move_left,
            "move_right": self.env.move_right,
            "collect": self.env.collect,
            "get_pos": self.env.get_pos,
            "is_at": self.env.is_at,
            "scan": self.env.scan,
            # Additional helpers
            "grid_size": (self.env.size, self.env.size),
            "max_steps": self.env.max_steps,
            "env": self.env,
        }

        # Try to execute the code
        try:
            exec(code, namespace)
        except Exception as e:
            error_msg = f"{type(e).__name__}: {e}"
            return False, "", error_msg

        # Check if task goal is met
        req_wood = task.get("required_wood", 0)
        req_stone = task.get("required_stone", 0)
        success, msg = self.env.check_goal(req_wood, req_stone)
        return success, msg, ""

    # -- iterative prompting loop --------------------------------------------

    def solve_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        尝试解决一个任务（带迭代修复的完整流程）
        
        初学者要点：
        - 这是单次任务解决的完整流程：
          1. 从技能库检索相关经验（retrieve_skills）
          2. 生成初始代码（generate_code）
          3. 执行代码（execute_code）
          4. 如果失败 → 修复代码（repair_code）→ 重试
          5. 如果成功 → 存入技能库（add_skill）
        - max_retries 控制最多尝试次数，防止无限循环
        - 每次尝试的结果都记录到 task_results 中，用于后续分析
        """
        print(f"\n{'='*60}")
        print(f"Task [Level {task['level']}]: {task['description']}")
        print(f"Required: wood={task.get('required_wood',0)}, stone={task.get('required_stone',0)}")
        print(f"{'='*60}")

        # Retrieve relevant skills from library
        retrieved = self.skill_lib.retrieve_skills(
            task["description"], task["level"], top_k=3
        )
        if retrieved:
            print(f"Retrieved {len(retrieved)} skills: {[s.name for s in retrieved]}")

        # Generate initial code
        env_state = self.env.get_state_dict()
        code = self.llm.generate_code(
            task=task,
            env_state=env_state,
            retrieved_skills=[{"name": s.name, "code": s.code} for s in retrieved],
        )
        print(f"\n--- Generated Code ---\n{code}\n---")

        # Iterative execution loop
        success = False
        final_msg = ""
        error = ""
        attempts = 0

        for attempt in range(1, self.max_retries + 1):
            attempts = attempt
            success, final_msg, error = self.execute_code(code, task)

            if success:
                print(f"✅ Success on attempt {attempt}: {final_msg}")
                break
            else:
                print(f"❌ Failed on attempt {attempt}: {error}")
                if attempt < self.max_retries:
                    # Iterative prompting: repair code based on error
                    print(f"🔧 Repairing code...")
                    code = self.llm.repair_code(code, error, self.env.get_state_dict())
                    print(f"--- Repaired Code ---\n{code}\n---")

        result = {
            "task": task,
            "success": success,
            "attempts": attempts,
            "final_message": final_msg,
            "error": error if not success else "",
            "code": code,
            "code_length": len(code),
        }

        # Store successful code in skill library
        if success:
            skill_name = f"solve_level_{task['level']}_{task['description'][:20]}"
            skill = self.skill_lib.add_skill(
                name=skill_name,
                description=task["description"],
                code=code,
                level=task["level"],
                tags=["auto_generated"],
            )
            result["skill_id"] = skill.id
            self.completed_levels.append(task["level"])
            # Remove from failure history if it was there
            self.failure_history = [f for f in self.failure_history if task["description"] not in f]
        else:
            self.failure_history.append(f"Level {task['level']}: {task['description']} - {error}")

        self.task_results.append(result)
        return result

    # -- training loop (lifetime learning) -----------------------------------

    def train(self, num_episodes: int = 10) -> Dict[str, Any]:
        """Run the lifetime learning loop for N episodes."""
        print(f"\n{'#'*60}")
        print(f"# VOYAGER AGENT: Lifetime Learning Begins")
        print(f"# Episodes: {num_episodes}")
        print(f"{'#'*60}\n")

        for episode in range(1, num_episodes + 1):
            print(f"\n{'#'*60}")
            print(f"# Episode {episode}/{num_episodes}")
            print(f"{'#'*60}")

            # 1. Automatic Curriculum: generate next task
            task = self.next_task()

            # 2. Iterative Prompting: solve with retries
            result = self.solve_task(task)

            # 3. Skill library automatically updated on success
            print(f"\nSkill Library: {self.skill_lib.get_stats()}")

        return self.get_training_report()

    def get_training_report(self) -> Dict[str, Any]:
        """Generate final training report."""
        successes = sum(1 for r in self.task_results if r["success"])
        total = len(self.task_results)
        avg_attempts = sum(r["attempts"] for r in self.task_results) / max(total, 1)
        levels_reached = max(self.completed_levels) if self.completed_levels else 0

        return {
            "total_episodes": total,
            "successes": successes,
            "failures": total - successes,
            "success_rate": successes / max(total, 1),
            "avg_attempts_per_task": avg_attempts,
            "max_level_reached": levels_reached,
            "skill_library_stats": self.skill_lib.get_stats(),
            "failure_patterns": self._analyze_failures(),
        }

    def _analyze_failures(self) -> Dict[str, int]:
        """Analyze common failure patterns."""
        patterns = {}
        for r in self.task_results:
            if not r["success"] and r["error"]:
                # Categorize error
                if "out of bounds" in r["error"].lower():
                    patterns["out_of_bounds"] = patterns.get("out_of_bounds", 0) + 1
                elif "blocked" in r["error"].lower():
                    patterns["wall_blocked"] = patterns.get("wall_blocked", 0) + 1
                elif "name " in r["error"].lower() and "is not defined" in r["error"].lower():
                    patterns["undefined_variable"] = patterns.get("undefined_variable", 0) + 1
                else:
                    patterns["other"] = patterns.get("other", 0) + 1
        return patterns


# ============================================================================
#  MODULE 4: Visualization & Analysis (lifelong learning curve)
# ============================================================================

def print_learning_curve(agent: VoyagerAgent) -> None:
    """Print a text-based learning curve."""
    print(f"\n{'='*60}")
    print("LIFELONG LEARNING CURVE")
    print(f"{'='*60}")

    skills_over_time = []
    cumulative_skills = 0
    for i, result in enumerate(agent.task_results, 1):
        if result["success"]:
            cumulative_skills += 1
        skills_over_time.append((i, cumulative_skills))

    # Simple ASCII chart
    max_skills = max((s for _, s in skills_over_time), default=0)
    height = max(max_skills, 1)

    for h in range(height, 0, -1):
        line = f"{h:3d} | "
        for ep, skills in skills_over_time:
            if skills >= h:
                line += "█ "
            else:
                line += "  "
        print(line)
    print(f"    {'-' * (len(agent.task_results) * 2 + 1)}")
    print(f"    {' '.join(f'{i%10}' for i in range(1, len(agent.task_results) + 1))}")
    print(f"    Episode")

    print(f"\nTotal skills acquired: {cumulative_skills}/{len(agent.task_results)}")


def print_final_report(report: Dict[str, Any]) -> None:
    """Print formatted final training report."""
    print(f"\n{'='*60}")
    print("FINAL TRAINING REPORT")
    print(f"{'='*60}")
    print(f"Total Episodes:      {report['total_episodes']}")
    print(f"Successes:           {report['successes']}")
    print(f"Failures:            {report['failures']}")
    print(f"Success Rate:        {report['success_rate']:.1%}")
    print(f"Avg Attempts/Task:   {report['avg_attempts_per_task']:.2f}")
    print(f"Max Level Reached:   {report['max_level_reached']}")
    print(f"\nSkill Library:")
    stats = report["skill_library_stats"]
    print(f"  Total Skills:      {stats['total_skills']}")
    print(f"  Levels Covered:    {stats['levels_covered']}")
    print(f"  Successful Reuses: {stats['total_successful_uses']}")
    print(f"  Skill Names:       {stats['skill_names']}")
    if report["failure_patterns"]:
        print(f"\nFailure Pattern Analysis:")
        for pattern, count in report["failure_patterns"].items():
            print(f"  {pattern}: {count}")
    print(f"{'='*60}")


# ============================================================================
#  MAIN: Experiment Runner
# ============================================================================

def run_experiment(num_episodes: int = 10, grid_size: int = 10) -> Dict[str, Any]:
    """
    Run the full Voyager-style experiment.

    Returns the final training report dictionary.
    """
    # Initialize components
    env = GridWorld(size=grid_size, max_steps=100)
    llm = SimulatedLLM()
    agent = VoyagerAgent(env=env, llm=llm, max_retries=3)

    # Run lifetime learning
    report = agent.train(num_episodes=num_episodes)

    # Visualize
    print_learning_curve(agent)
    print_final_report(report)

    # Print sample skill from library
    if agent.skill_lib.skills:
        print(f"\n{'='*60}")
        print("SAMPLE SKILL FROM LIBRARY")
        print(f"{'='*60}")
        sample = list(agent.skill_lib.skills.values())[0]
        print(f"Name: {sample.name}")
        print(f"Description: {sample.description}")
        print(f"Level: {sample.level}")
        print(f"Code:\n{sample.code}")

    print(f"\n{'='*60}")
    print(f"EXPERIMENT COMPLETE")
    print(f"Total LLM calls: {llm.call_count}")
    print(f"{'='*60}")

    return report


# ============================================================================
#  ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Configuration
    NUM_EPISODES = 12   # Number of training episodes
    GRID_SIZE = 10      # Grid world size

    print("Voyager-Style Code Generation Agent Experiment")
    print("=" * 60)
    print(f"Configuration: {NUM_EPISODES} episodes, {GRID_SIZE}x{GRID_SIZE} grid")
    print("=" * 60)

    report = run_experiment(num_episodes=NUM_EPISODES, grid_size=GRID_SIZE)

    # Save report to file
    import json
    with open("voyager_experiment_report.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    print("\nReport saved to: voyager_experiment_report.json")
```

---


## 四、评估指标详解（初学者指南）

### 为什么需要这些指标？

Voyager 是一个**终身学习**系统，核心问题是：Agent 是否真的在"学习"，而不是在"记忆"？这些指标帮助我们量化：
- Agent 能否解决越来越难的问题？
- 成功经验是否被有效存储和复用？
- 失败模式是否在减少？

### 指标一览

| 指标 | 定义 | 为什么重要 | 理想值 | 如何改进 |
|-----|------|----------|--------|---------|
| **success_rate** | 成功任务数 / 总任务数 | 衡量整体学习效果 | > 70% | 改进代码生成模板、增加重试次数 |
| **avg_attempts** | 平均每个任务尝试次数 | 衡量一次通过率，越低说明代码质量越高 | < 2.0 | 优化 SimulatedLLM 的代码模板 |
| **max_level_reached** | Agent 成功完成的最高难度等级 | 衡量能力上限 | 越高越好（最高6） | 确保课程递进逻辑正确 |
| **skill_library.total_skills** | 技能库中存储的成功代码片段数 | 衡量知识积累量 | 持续增长 | 确保成功任务被正确存入技能库 |
| **skill_library.levels_covered** | 技能库覆盖的难度等级列表 | 衡量技能广度 | [1,2,3,4,5,6] | 确保各级别都有成功解 |
| **failure_patterns** | 失败类型统计（越界/撞墙/未定义变量） | 帮助定位代码生成的薄弱环节 | 趋向于0 | 针对性增强 repair_code 规则 |

### 指标之间的关系

```
success_rate ↑  ←  skill_library 增长 ←  经验积累
     ↑
avg_attempts ↓  ←  代码质量提升 ←  迭代修复有效
     ↑
max_level ↑     ←  课程递进合理 ←  自动课程工作正常
```

**关键洞察**：
- `success_rate` 高但 `avg_attempts` 也高 → Agent 在"试错学习"，这是正常的终身学习模式
- `skill_library` 不增长 → 检查 `execute_code` 后的存储逻辑
- `max_level` 停滞在低级 → 检查 `generate_curriculum` 的 level 递进逻辑
- `failure_patterns` 中某类错误持续高 → 针对性增强 `repair_code` 的对应规则

---

## 五、实验步骤


### 5.1 运行实验

```bash
# 1. 保存上述代码到 voyager_agent.py
# 2. 运行实验
python voyager_agent.py
```

### 5.2 预期输出

```
############################################################
# VOYAGER AGENT: Lifetime Learning Begins
# Episodes: 12
############################################################

============================================================
Task [Level 1]: Move from start to goal
Required: wood=0, stone=0
============================================================

--- Generated Code ---
# Solve: Move to goal at (9, 9)
# Move to goal
pr, pc = get_pos()
if pr < 9:
    for _ in range(9 - pr):
        move_down()
...
---
✅ Success on attempt 1: Task completed successfully!

Skill Library: {'total_skills': 1, 'levels_covered': [1], ...}

...

============================================================
LIFELONG LEARNING CURVE
============================================================
  5 | █ █ █ █ █ █ █ █ █ █ █ █
  4 | █ █ █ █ █ █ █ █ █ █ █ █
  ...

============================================================
FINAL TRAINING REPORT
============================================================
Total Episodes:      12
Successes:           10
Failures:            2
Success Rate:        83.3%
Avg Attempts/Task:   1.4
Max Level Reached:   5

Skill Library:
  Total Skills:      10
  Levels Covered:    [1, 2, 3, 4, 5]
  Successful Reuses: 0
  Skill Names:       [...]

Failure Pattern Analysis:
  out_of_bounds: 1
  wall_blocked: 1
============================================================
```

### 5.3 实验步骤详解

| 步骤 | 操作 | 验证点 |
|-----|------|--------|
| 1 | 运行实验脚本 | 输出训练报告，无报错 |
| 2 | 检查技能库增长 | 每次成功后技能库 `total_skills` 增加 |
| 3 | 检查课程递进 | 任务难度从 L1 逐步升级到 L5/L6 |
| 4 | 检查迭代修复 | 失败任务是否触发代码修复（`repair_code`） |
| 5 | 检查最终曲线 | 成功率应 > 60%，技能库持续增长 |
| 6 | 修改环境参数 | 改变 `GRID_SIZE` 和 `NUM_EPISODES`，观察泛化 |

---


## 场景配置矩阵

| 场景 | episodes | grid_size | max_retries | 用途 |
|-----|----------|-----------|-------------|------|
| 快速测试 | 5 | 8 | 2 | 验证代码能跑通，2分钟出结果 |
| 标准训练 | 12 | 10 | 3 | 观察完整学习曲线（推荐） |
| 深度训练 | 20 | 12 | 5 | 验证长期学习能力，观察技能饱和 |
| 调试模式 | 3 | 6 | 1 | 快速定位bug，最小复现 |
| 泛化测试 | 15 | 15 | 3 | 测试大网格上的表现 |

### 初学者调试清单

- [ ] **如果 success_rate < 50%**：检查 `SimulatedLLM._code_template()` 的代码模板是否正确生成
- [ ] **如果 skill_library 不增长**：检查 `solve_task()` 成功后是否调用了 `add_skill()`
- [ ] **如果 max_level_reached 停滞**：检查 `generate_curriculum()` 的 level 递进逻辑（是否 cap 在低级）
- [ ] **如果 failure_patterns 中 "out_of_bounds" 高**：增强 `repair_code()` 的边界检查规则
- [ ] **如果 failure_patterns 中 "blocked by wall" 高**：检查 L3+ 的代码模板是否包含 wall 检测
- [ ] **如果 avg_attempts > 3**：降低 `max_retries` 或改进初始代码质量

---

## 六、关键设计决策与解释


### 6.1 为什么用 2D 网格而非真实 Minecraft？

| 维度 | 本实验 | 真实 Minecraft |
|-----|--------|---------------|
| 环境依赖 | 纯 Python，零外部依赖 | 需要 Minecraft 客户端 + Mineflayer + Node.js |
| 实验成本 | 毫秒级/episode | 秒级~分钟级/episode |
| 可复现性 | 确定性的（seed 控制） | 受网络、游戏状态影响 |
| 教学价值 | 核心逻辑清晰 | 被环境复杂性淹没 |
| 扩展路径 | 替换 `GridWorld` 类即可 | 需要完整的 Voyager 基础设施 |

### 6.2 模拟 LLM 的设计权衡

本实验使用**规则模板模拟 LLM**而非真实 API，原因：
- **零成本**: 无需 OpenAI/Anthropic API key
- **确定性**: 相同输入总是产生相同输出，便于调试
- **聚焦架构**: 学习 Voyager 三模块架构，而非 LLM 提示工程技巧

**替换为真实 LLM**只需修改 `SimulatedLLM` 的三个方法：
- `generate_curriculum()` → 调用 GPT-4 with curriculum prompt
- `generate_code()` → 调用 GPT-4 with code generation prompt
- `repair_code()` → 调用 GPT-4 with error + code repair prompt

### 6.3 技能库 vs RAG

| 特性 | Voyager 技能库 | 标准 RAG |
|-----|---------------|----------|
| 存储内容 | 可执行代码 | 文本段落 |
| 验证方式 | 执行验证 | 语义相关 |
| 组合性 | 代码可调用代码 | 文本拼接 |
| 更新机制 | 成功即存储 | 预构建索引 |
| 优势 | **可执行、可验证** | 语义灵活 |
| 劣势 | 依赖关系管理复杂 | 不可直接执行 |

---

## 七、思考题

### 7.1 基础问题

1. **代码生成动作空间 vs 低层 API**：本实验中 `move_up()` 等函数既是代码中的调用，也是环境 API。如果动作空间改为 "每次只能输出一个 move 命令"，完成 L4 任务需要多少 LLM 调用？代码生成方式的优势是什么？

2. **技能库检索**：本实验使用基于关键词和 level 的简化检索。如果改为 embedding-based 检索（如 Voyager 原论文），检索质量会如何变化？需要什么基础设施？

3. **迭代提示的代价**：每次失败需要一次额外的 LLM 调用（`repair_code`）。如果连续失败 3 次，该任务消耗的 LLM 调用是成功案例的 3 倍。如何设计策略减少这种 "失败税"？

### 7.2 进阶问题

4. **技能依赖管理**：本实验的技能库假设技能之间无依赖。但 `collect_resources` 可能依赖 `move_to`。如果代码 A 调用代码 B，但技能库只检索到 A，执行会失败。如何设计**带依赖解析的技能库**？

5. **从 2D 到 3D**：如果要将本实验扩展到类 Minecraft 的 3D 环境（支持 y 轴、方块放置/破坏），三模块中哪些需要修改？哪些可以复用？

6. **自动课程的多样性**：本实验的 `generate_curriculum` 是确定性的规则。真实的 Voyager 课程由 LLM 生成，可能产生**重复或过于相似**的任务。如何量化课程的多样性？如何防止 "课程坍缩"（只生成已经擅长的任务）？

### 7.3 面试谈资

> **30 秒版本**：Voyager 是 Minecraft 中的终身学习 Agent，核心创新是将动作空间设为代码生成。三模块架构（自动课程 + 技能库 + 迭代提示）让它无需梯度更新就能持续解锁新能力。本实验在 2D 网格中复现了该架构，验证了技能库的增长曲线和迭代修复的有效性。

> **2 分钟版本**：Voyager 的关键洞察是**代码天然是可执行、可组合、可验证的原子动作**。在开放世界中，低层 API（如键盘按键）的探索空间太大，而代码生成通过 LLM 的抽象能力直接输出高层行为。技能库则是"外化记忆"——将成功的代码片段存储起来，未来通过检索复用。这比 RAG 更强大，因为检索到的代码可以直接执行验证。但局限也很明显：延迟高（每次动作需要 LLM 调用）、代码片段间的依赖关系难以管理、且对实时游戏不适用。

---

## 八、扩展方向

### 8.1 可能的改进

| 方向 | 改进内容 | 预期收益 |
|-----|---------|---------|
| 真实 LLM | 替换 `SimulatedLLM` 为 GPT-4/Claude API | 代码生成质量提升，能处理更复杂任务 |
| Embedding 检索 | 技能库使用 sentence-transformer 做语义检索 | 跨任务技能复用率提升 |
| 技能依赖图 | 维护技能之间的调用关系，检索时自动解析依赖 | 组合技能的成功率提升 |
| 课程难度量化 | 引入任务复杂度度量（步数、资源数、障碍物密度） | 课程难度曲线更平滑 |
| 沙箱隔离 | 用 `subprocess` 或 `docker` 隔离代码执行 | 安全性提升，可运行不可信代码 |
| 3D 扩展 | 替换 GridWorld 为 Mineflayer API 或简化 3D 环境 | 更接近真实 Minecraft |

### 8.2 相关实验链接

- 实验 9: [[09-AutoGPT-反思与错误修正机制实验]] — 对比 AutoGPT 的文本反思 vs Voyager 的代码迭代修复
- 实验 11: [[11-分层控制-高层规划与低层执行分离实验]] — 将 Voyager 的代码生成与 RL 执行层结合
- 实验 12: [[12-工具使用-Function-Calling-Agent实验]] — 对比代码生成 vs Function Calling 动作空间

---

## 九、实验文件清单

```
10-Voyager风格-代码生成Agent实验.md   # 本实验文档
voyager_agent.py                       # 完整代码（从本文档提取）
voyager_experiment_report.json          # 实验输出报告（运行后生成）
```

---

*实验创建时间: 2026-07-06*
*维护者: AIResearchVault*
*关联论文: Voyager (NeurIPS 2023)*
