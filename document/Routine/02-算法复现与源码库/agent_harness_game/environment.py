"""
E — Environment Execution: Simplified 2D Sandbox Environment

Maps the paper's Environment Execution component to a simplified Game AI setting.
State: S = (grid, agent_pos, inventory)
Action: A = {move, place, mine, craft, noop}
Transition: P(s'|s,a) — deterministic for simplicity
Reward: R(s,a) — sparse task-based
"""
from dataclasses import dataclass, field
from typing import Tuple, List, Dict, Optional, Set
from enum import Enum
import copy


class BlockType(Enum):
    EMPTY = 0
    GRASS = 1
    WOOD = 2
    STONE = 3
    PLANK = 4
    WALL = 5
    AGENT = 9


class ActionType(Enum):
    MOVE_UP = "move_up"
    MOVE_DOWN = "move_down"
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"
    PLACE_BLOCK = "place_block"
    MINE_BLOCK = "mine_block"
    CRAFT = "craft"
    NOOP = "noop"


@dataclass
class GameAction:
    action_type: ActionType
    params: Dict = field(default_factory=dict)

    def __repr__(self):
        p = f"({self.params})" if self.params else ""
        return f"{self.action_type.value}{p}"


@dataclass
class GameState:
    """S = (grid, agent_pos, inventory, turn)"""
    grid: List[List[int]]
    agent_pos: Tuple[int, int]
    inventory: Dict[int, int] = field(default_factory=lambda: {b.value: 0 for b in BlockType})
    turn: int = 0
    max_turns: int = 100

    @property
    def width(self) -> int:
        return len(self.grid[0]) if self.grid else 0

    @property
    def height(self) -> int:
        return len(self.grid)

    def get_block(self, x: int, y: int) -> BlockType:
        if 0 <= y < self.height and 0 <= x < self.width:
            return BlockType(self.grid[y][x])
        return BlockType.EMPTY

    def set_block(self, x: int, y: int, block: BlockType):
        if 0 <= y < self.height and 0 <= x < self.width:
            self.grid[y][x] = block.value

    def clone(self) -> "GameState":
        return GameState(
            grid=[row[:] for row in self.grid],
            agent_pos=self.agent_pos,
            inventory=copy.deepcopy(self.inventory),
            turn=self.turn,
            max_turns=self.max_turns,
        )

    def render(self) -> str:
        """ASCII render for debugging"""
        chars = {
            BlockType.EMPTY: "·",
            BlockType.GRASS: "░",
            BlockType.WOOD: "T",
            BlockType.STONE: "#",
            BlockType.PLANK: "=",
            BlockType.WALL: "█",
            BlockType.AGENT: "A",
        }
        lines = []
        for y, row in enumerate(self.grid):
            line = ""
            for x, cell in enumerate(row):
                if (x, y) == self.agent_pos:
                    line += "A"
                else:
                    line += chars.get(BlockType(cell), "?")
            lines.append(line)
        return "\n".join(lines)


class SandboxEnvironment:
    """
    Simplified 2D Minecraft-like environment.
    
    State transition: s' = P(s, a)  (deterministic)
    Reward: task-completion sparse reward
    """

    def __init__(self, width: int = 10, height: int = 10):
        self.width = width
        self.height = height

    def reset(self, initial_blocks: Optional[Dict[Tuple[int, int], BlockType]] = None) -> GameState:
        grid = [[BlockType.GRASS.value for _ in range(self.width)] for _ in range(self.height)]
        if initial_blocks:
            for (x, y), block in initial_blocks.items():
                if 0 <= x < self.width and 0 <= y < self.height:
                    grid[y][x] = block.value
        # Place agent at center
        agent_pos = (self.width // 2, self.height // 2)
        return GameState(
            grid=grid,
            agent_pos=agent_pos,
            inventory={b.value: 0 for b in BlockType},
            turn=0,
            max_turns=100,
        )

    def step(self, state: GameState, action: GameAction) -> Tuple[GameState, float, bool, Dict]:
        """
        Execute one step.
        Returns: (new_state, reward, done, info)
        """
        if state.turn >= state.max_turns:
            return state, 0.0, True, {"reason": "max_turns_reached"}

        new_state = state.clone()
        new_state.turn += 1
        reward = 0.0
        done = False
        info = {"action": action.action_type.value, "success": True}

        x, y = new_state.agent_pos

        if action.action_type == ActionType.MOVE_UP:
            new_state.agent_pos = (x, max(0, y - 1))
        elif action.action_type == ActionType.MOVE_DOWN:
            new_state.agent_pos = (x, min(self.height - 1, y + 1))
        elif action.action_type == ActionType.MOVE_LEFT:
            new_state.agent_pos = (max(0, x - 1), y)
        elif action.action_type == ActionType.MOVE_RIGHT:
            new_state.agent_pos = (min(self.width - 1, x + 1), y)

        elif action.action_type == ActionType.PLACE_BLOCK:
            block_type = action.params.get("block_type", BlockType.PLANK)
            if new_state.inventory.get(block_type.value, 0) > 0:
                tx = action.params.get("x", x)
                ty = action.params.get("y", y)
                if 0 <= tx < self.width and 0 <= ty < self.height:
                    new_state.set_block(tx, ty, block_type)
                    new_state.inventory[block_type.value] -= 1
                    info["placed"] = (tx, ty, block_type.name)
            else:
                info["success"] = False
                info["reason"] = "insufficient_inventory"

        elif action.action_type == ActionType.MINE_BLOCK:
            tx = action.params.get("x", x)
            ty = action.params.get("y", y)
            if 0 <= tx < self.width and 0 <= ty < self.height:
                block = new_state.get_block(tx, ty)
                if block != BlockType.EMPTY and block != BlockType.GRASS:
                    new_state.set_block(tx, ty, BlockType.GRASS)
                    new_state.inventory[block.value] += 1
                    info["mined"] = (tx, ty, block.name)
                else:
                    info["success"] = False
                    info["reason"] = "nothing_to_mine"
            else:
                info["success"] = False
                info["reason"] = "out_of_bounds"

        elif action.action_type == ActionType.CRAFT:
            recipe = action.params.get("recipe", "plank")
            if recipe == "plank" and new_state.inventory.get(BlockType.WOOD.value, 0) >= 1:
                new_state.inventory[BlockType.WOOD.value] -= 1
                new_state.inventory[BlockType.PLANK.value] += 4
                info["crafted"] = "plank"
            else:
                info["success"] = False
                info["reason"] = "recipe_not_available"

        elif action.action_type == ActionType.NOOP:
            pass

        return new_state, reward, done, info

    def get_observation(self, state: GameState) -> Dict:
        """
        Multi-modal observation: (visual grid, structured state, text inventory)
        Maps to paper's "multi-modal state representation" challenge.
        """
        x, y = state.agent_pos
        # Local view: 5x5 window around agent
        view = []
        for dy in range(-2, 3):
            row = []
            for dx in range(-2, 3):
                vx, vy = x + dx, y + dy
                if 0 <= vx < state.width and 0 <= vy < state.height:
                    row.append(state.get_block(vx, vy).name)
                else:
                    row.append("VOID")
            view.append(row)

        return {
            "visual_grid": state.render(),
            "local_view": view,
            "agent_pos": state.agent_pos,
            "inventory": {BlockType(k).name: v for k, v in state.inventory.items() if v > 0},
            "turn": state.turn,
            "max_turns": state.max_turns,
        }

    def get_valid_actions(self, state: GameState) -> List[ActionType]:
        """Return all action types (safety filtering is done by Safety Sandbox S)."""
        return list(ActionType)
