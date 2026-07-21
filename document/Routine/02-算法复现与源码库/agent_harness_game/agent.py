"""
T — Tool Calling: LLM Agent Interface + ReAct Loop

Implements the paper's Tool Calling component.
Agent: ReAct pattern (Reasoning + Action)
- Thought: internal reasoning about current state
- Action: tool call (game action)
- Observation: result from environment
"""
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import functools
import json
import random
from .environment import GameState, GameAction, ActionType, BlockType
from .context import ContextManager
from .safety import SafetySandbox
from .verifier import TaskSpec


# ---------------------------------------------------------------------------
# 任务知识库（仅供 SimulatedLLM 使用）
#
# 现状：AgentHarness.set_task 只把 "name: description" 文本经 ContextManager
# 传给 agent，结构化 TaskSpec（target_blocks 坐标/块类型）并不暴露给 T 组件；
# 且 evaluation.generate_variants 会对 held-out 变体抖动坐标，导致目标文本中
# 的坐标过期。真实 LLM 部署时会由调用方提供完整任务规格，为了让模拟后端在
# 不修改 harness.py 的前提下获得同等信息，这里在 TaskSpec 构造时按 name 注册
# 一份知识库。若 name 未命中（如外部临时构造的任务），规划器退化为从目标
# 文本中解析 "(x, y)" 坐标。
# ---------------------------------------------------------------------------
TASK_KNOWLEDGE: Dict[str, TaskSpec] = {}


def _register_task_spec(init):
    """包装 TaskSpec.__init__，把每个构造出的任务规格按 name 登记进知识库。"""

    @functools.wraps(init)
    def wrapper(self, *args, **kwargs):
        init(self, *args, **kwargs)
        TASK_KNOWLEDGE[self.name] = self

    return wrapper


TaskSpec.__init__ = _register_task_spec(TaskSpec.__init__)


class AgentMode(Enum):
    REACT = "react"
    DIRECT = "direct"
    PLANNING = "planning"


@dataclass
class AgentResponse:
    thought: str
    action: GameAction


class LLMBackend:
    """
    Abstract LLM backend interface.
    Can be replaced with real GPT-4/Claude API.
    """

    def __init__(self, model_name: str = "simulated"):
        self.model_name = model_name

    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Return raw text response from LLM."""
        raise NotImplementedError


class SimulatedLLM(LLMBackend):
    """
    Rule-based simulated LLM for testing without API keys.
    Implements simple heuristics for game actions.
    """

    def __init__(self, strategy: str = "random"):
        super().__init__("simulated")
        self.strategy = strategy
        # 已确认放置的目标格记忆：agent 站立格在 grid 快照中被渲染为 'A'，
        # 遮住其下方方块，无法从 prompt 判断该格是否已放对，故需要记忆。
        self._placed_confirmed: set = set()
        self._last_turn: int = -1

    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Parse prompt and return a simulated action."""
        if self.strategy == "random":
            return self._random_action()

        # Extract goal and state from prompt
        goal = self._extract_goal(prompt)
        pos = self._extract_position(prompt)
        inventory = self._extract_inventory(prompt)
        grid = self._extract_grid(prompt)

        # 检测新 episode（turn 回退）→ 清空放置记忆
        turn = self._extract_turn(prompt)
        if turn <= self._last_turn:
            self._placed_confirmed.clear()
        self._last_turn = turn

        # heuristic / planner 均走目标导向贪心规划器（planner 为显式策略名，
        # heuristic 保持向后兼容，其建造/合成行为由规划器修复）
        return self._plan(goal, pos, inventory, grid)

    def _random_action(self) -> str:
        actions = [a.value for a in ActionType]
        a = random.choice(actions)
        if a == "place_block":
            return json.dumps({"action_type": a, "params": {"block_type": "PLANK"}})
        return json.dumps({"action_type": a, "params": {}})

    # ------------------------------------------------------------------
    # 目标导向贪心规划器
    # ------------------------------------------------------------------

    def _plan(self, goal: str, pos: Tuple[int, int],
              inventory: Dict[int, int], grid: Dict[Tuple[int, int], BlockType]) -> str:
        """顶层分派：建造目标 → build 规划；合成目标 → craft 规划；否则随机。"""
        targets = self._resolve_targets(goal)
        if targets:
            return self._plan_build(targets, pos, inventory, grid)
        if "craft" in goal.lower():
            return self._plan_craft(pos, inventory, grid)
        return self._random_action()

    def _resolve_targets(self, goal: str) -> Dict[Tuple[int, int], BlockType]:
        """
        从目标文本解析建造目标 {(x, y): BlockType}。
        优先查任务知识库（按 goal 前缀的任务名命中 TaskSpec.target_blocks）；
        未命中时从文本中解析 "(x, y)" 坐标列表，并按关键词推断块类型。
        """
        name = goal.split(":", 1)[0].strip()
        spec = TASK_KNOWLEDGE.get(name)
        if spec is not None and spec.target_blocks:
            return dict(spec.target_blocks)

        # 兜底：解析文本坐标，如 "Build a 2x2 wall at (4,4), (5,4), ..."
        coords = []
        for seg in goal.split("(")[1:]:
            if ")" not in seg:
                continue
            nums = seg[: seg.index(")")].replace(",", " ").split()
            if len(nums) == 2 and all(n.lstrip("-").isdigit() for n in nums):
                coords.append((int(nums[0]), int(nums[1])))
        if not coords:
            return {}
        lower = goal.lower()
        block = BlockType.WALL
        for keyword, bt in (("stone", BlockType.STONE), ("plank", BlockType.PLANK),
                            ("wood", BlockType.WOOD), ("wall", BlockType.WALL)):
            if keyword in lower:
                block = bt
                break
        return {c: block for c in coords}

    def _plan_build(self, targets: Dict[Tuple[int, int], BlockType],
                    pos: Tuple[int, int], inventory: Dict[int, int],
                    grid: Dict[Tuple[int, int], BlockType]) -> str:
        """
        建造贪心规划：
        1. 找出尚未完成的的目标块（grid 当前值 != 期望值）；
        2. 库存足够的最近目标 → 移动至相邻/站上后放置正确类型块；
        3. 库存不足 → 走资源获取子策略（craft / mine）；
        4. 全部完成 → noop。
        """
        remaining = [(p, b) for p, b in targets.items()
                     if grid.get(p) != b and p not in self._placed_confirmed]
        if not remaining:
            return self._noop()

        # 当前库存可直接满足的目标
        doable = [(p, b) for p, b in remaining if inventory.get(b.value, 0) > 0]
        if doable:
            tp, tb = min(doable, key=lambda pb: self._dist(pos, pb[0]))

            def _do_place():
                # 放置后该格可能被 'A' 渲染遮住，记入已确认集合
                self._placed_confirmed.add(tp)
                return self._place(tp, tb)

            return self._move_or_act(pos, tp, _do_place)

        # 库存不足：对最近的未完成目标做资源获取
        tp, tb = min(remaining, key=lambda pb: self._dist(pos, pb[0]))
        return self._acquire(tb, pos, inventory, grid)

    def _plan_craft(self, pos: Tuple[int, int], inventory: Dict[int, int],
                    grid: Dict[Tuple[int, int], BlockType]) -> str:
        """合成规划：有木头就合成木板；没有就去找木头挖。"""
        if inventory.get(BlockType.WOOD.value, 0) > 0:
            return json.dumps({"action_type": "craft", "params": {"recipe": "plank"}})
        return self._acquire(BlockType.WOOD, pos, inventory, grid)

    def _acquire(self, block: BlockType, pos: Tuple[int, int],
                 inventory: Dict[int, int], grid: Dict[Tuple[int, int], BlockType]) -> str:
        """
        资源获取子策略：
        - 需要 PLANK 且有 WOOD → craft；
        - 否则在 grid 上找最近的该类型方块（PLANK 退化为找 WOOD），
          移动到相邻/站上后挖掘；
        - 无获取途径 → noop（不随机，避免安全层误报）。
        """
        if block == BlockType.PLANK and inventory.get(BlockType.WOOD.value, 0) > 0:
            return json.dumps({"action_type": "craft", "params": {"recipe": "plank"}})

        source = BlockType.WOOD if block == BlockType.PLANK else block
        cells = [p for p, b in grid.items() if b == source]
        if not cells:
            return self._noop()
        tp = min(cells, key=lambda p: self._dist(pos, p))
        return self._move_or_act(pos, tp, lambda: self._mine(tp))

    # ------------------------------------------------------------------
    # 规划器原子动作
    # ------------------------------------------------------------------

    @staticmethod
    def _dist(a: Tuple[int, int], b: Tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _move_or_act(self, pos: Tuple[int, int], target: Tuple[int, int],
                     act_when_close) -> str:
        """与目标 Manhattan 距离 ≤1（含站上）时执行 act，否则朝目标走一步。"""
        if self._dist(pos, target) <= 1:
            return act_when_close()
        x, y = pos
        tx, ty = target
        if tx > x:
            move = "move_right"
        elif tx < x:
            move = "move_left"
        elif ty > y:
            move = "move_down"
        else:
            move = "move_up"
        return json.dumps({"action_type": move, "params": {}})

    def _place(self, target: Tuple[int, int], block: BlockType) -> str:
        return json.dumps({"action_type": "place_block",
                           "params": {"block_type": block.name,
                                      "x": target[0], "y": target[1]}})

    def _mine(self, target: Tuple[int, int]) -> str:
        return json.dumps({"action_type": "mine_block",
                           "params": {"x": target[0], "y": target[1]}})

    def _noop(self) -> str:
        return json.dumps({"action_type": "noop", "params": {}})

    def _extract_goal(self, prompt: str) -> str:
        for line in prompt.split("\n"):
            if line.startswith("Goal:"):
                return line[5:].strip()
        return ""

    def _extract_turn(self, prompt: str) -> int:
        """解析 "Turn k/max" 行，用于检测新 episode（turn 回退时清空记忆）。"""
        for line in prompt.split("\n"):
            if line.startswith("Turn "):
                num = line[5:].split("/")[0].strip()
                if num.isdigit():
                    return int(num)
        return 0

    def _extract_position(self, prompt: str) -> Tuple[int, int]:
        for line in prompt.split("\n"):
            if "Position:" in line:
                parts = line.split("Position:")[1].strip()
                # Parse (x, y)
                parts = parts.replace("(", "").replace(")", "").replace(",", " ")
                coords = [int(x) for x in parts.split() if x.strip().lstrip("-").isdigit()]
                if len(coords) >= 2:
                    return (coords[0], coords[1])
        return (5, 5)

    def _extract_inventory(self, prompt: str) -> Dict[int, int]:
        inv = {}
        in_inventory = False
        for line in prompt.split("\n"):
            if "Inventory:" in line:
                in_inventory = True
                continue
            if in_inventory and line.strip().startswith("-"):
                parts = line.replace("-", "").strip().split(":")
                if len(parts) == 2:
                    name = parts[0].strip()
                    count = int(parts[1].strip())
                    for bt in BlockType:
                        if bt.name == name:
                            inv[bt.value] = count
                            break
            elif in_inventory and not line.strip().startswith("-"):
                in_inventory = False
        return inv

    # Grid snapshot 中 ASCII 字符 → BlockType（与 GameState.render 的映射互逆）
    _GRID_CHARS = {
        "·": BlockType.EMPTY,
        "░": BlockType.GRASS,
        "T": BlockType.WOOD,
        "#": BlockType.STONE,
        "=": BlockType.PLANK,
        "█": BlockType.WALL,
        "A": BlockType.AGENT,
    }

    def _extract_grid(self, prompt: str) -> Dict[Tuple[int, int], BlockType]:
        """从 prompt 的 "Grid snapshot:" 段落反解析完整 grid（含 agent 位置格）。"""
        grid: Dict[Tuple[int, int], BlockType] = {}
        lines = prompt.split("\n")
        try:
            start = lines.index("Grid snapshot:") + 1
        except ValueError:
            return grid
        for y, line in enumerate(lines[start:]):
            # grid 段落结束于空行或首个非 grid 字符行
            if not line or any(ch not in self._GRID_CHARS for ch in line):
                break
            for x, ch in enumerate(line):
                grid[(x, y)] = self._GRID_CHARS[ch]
        return grid


class ReActAgent:
    """
    ReAct Agent: Reasoning + Action loop.

    Pattern:
    1. Observe environment → build context
    2. Generate Thought + Action (LLM)
    3. Execute Action → get Observation
    4. Repeat

    Maps to paper's Tool Calling component T with ReAct reasoning.
    """

    def __init__(self, llm: Optional[LLMBackend] = None,
                 safety: Optional[SafetySandbox] = None,
                 context: Optional[ContextManager] = None,
                 mode: AgentMode = AgentMode.REACT):
        self.llm = llm or SimulatedLLM(strategy="heuristic")
        self.safety = safety
        self.context = context or ContextManager()
        self.mode = mode
        self.action_history: List[GameAction] = []

    def act(self, state: GameState, observation: Dict) -> Tuple[str, GameAction]:
        """
        Single ReAct step: observe → think → act.
        Returns: (thought, action)
        """
        # Build prompt from context
        available = [a.value for a in ActionType]
        prompt = self.context.build_agent_prompt(state, observation, available)

        # LLM generates response
        raw_response = self.llm.generate(prompt)

        # Parse response
        thought, action = self._parse_response(raw_response)

        # Safety check if available
        if self.safety:
            ok, reason = self.safety.validate(state, action)
            if not ok:
                # Fallback to noop if unsafe
                action = GameAction(ActionType.NOOP, {"reason": f"safety_fallback: {reason}"})
                thought += f" [Safety intercepted: {reason}]"

        return thought, action

    def _parse_response(self, raw: str) -> Tuple[str, GameAction]:
        """Parse LLM response into thought and action."""
        thought = "Simulated reasoning..."

        try:
            # Try JSON parsing first
            if "{" in raw:
                start = raw.index("{")
                end = raw.rindex("}") + 1
                json_str = raw[start:end]
                data = json.loads(json_str)
                action_type_str = data.get("action_type", "noop")
                params = data.get("params", {})

                # Convert string block_type to enum if needed
                if "block_type" in params and isinstance(params["block_type"], str):
                    try:
                        params["block_type"] = BlockType[params["block_type"].upper()]
                    except KeyError:
                        pass

                action = GameAction(ActionType(action_type_str), params)
            else:
                action = GameAction(ActionType.NOOP, {})
        except (json.JSONDecodeError, ValueError) as e:
            action = GameAction(ActionType.NOOP, {"parse_error": str(e)})

        return thought, action

    def reset(self):
        self.action_history = []
