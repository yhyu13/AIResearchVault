"""
S — Safety Sandbox: Action Validation & Constraints

Implements the paper's Safety component S(a) → {0,1}.
Filters: boundary, inventory, block destruction, rate limiting.
"""
from typing import Tuple, List, Dict, Optional
from enum import Enum
from dataclasses import dataclass, field
from .environment import GameState, GameAction, ActionType, BlockType


@dataclass
class SafetyPolicy:
    """Configurable safety rules for the game harness."""
    allow_boundary_violation: bool = False
    allow_inventory_negative: bool = False
    allow_destroy_unmineable: bool = False
    max_actions_per_turn: int = 10
    forbidden_block_types: List[BlockType] = field(default_factory=list)
    required_tools: Dict[BlockType, str] = field(default_factory=dict)

    @classmethod
    def default_game_policy(cls) -> "SafetyPolicy":
        return cls(
            allow_boundary_violation=False,
            allow_inventory_negative=False,
            allow_destroy_unmineable=False,
            max_actions_per_turn=10,
            forbidden_block_types=[BlockType.AGENT],
            required_tools={
                BlockType.STONE: "pickaxe",
                BlockType.WALL: "pickaxe",
            },
        )


class SafetySandbox:
    """
    S(a) ∈ {0,1}: validates every action before execution.
    
    Safety pipeline:
    1. Parse action type
    2. Check boundary constraints
    3. Check inventory/resource constraints
    4. Check destruction constraints
    5. Check rate limits
    """

    def __init__(self, policy: Optional[SafetyPolicy] = None):
        self.policy = policy or SafetyPolicy.default_game_policy()
        self.violation_log: List[Dict] = []

    def validate(self, state: GameState, action: GameAction) -> Tuple[bool, Optional[str]]:
        """
        Returns (is_safe, violation_reason).
        If safe, returns (True, None).
        If unsafe, returns (False, "reason_string").
        """
        x, y = state.agent_pos

        # 1. Boundary check for movement
        if action.action_type in {ActionType.MOVE_UP, ActionType.MOVE_DOWN,
                                  ActionType.MOVE_LEFT, ActionType.MOVE_RIGHT}:
            nx, ny = x, y
            if action.action_type == ActionType.MOVE_UP:
                ny -= 1
            elif action.action_type == ActionType.MOVE_DOWN:
                ny += 1
            elif action.action_type == ActionType.MOVE_LEFT:
                nx -= 1
            elif action.action_type == ActionType.MOVE_RIGHT:
                nx += 1

            if not (0 <= nx < state.width and 0 <= ny < state.height):
                if not self.policy.allow_boundary_violation:
                    return False, f"boundary_violation: ({nx},{ny})"

        # 2. Boundary check for place/mine target
        target_pos = None
        if action.action_type in {ActionType.PLACE_BLOCK, ActionType.MINE_BLOCK}:
            tx = action.params.get("x", x)
            ty = action.params.get("y", y)
            target_pos = (tx, ty)
            if not (0 <= tx < state.width and 0 <= ty < state.height):
                return False, f"boundary_violation_target: ({tx},{ty})"

        # 3. Inventory check for placement
        if action.action_type == ActionType.PLACE_BLOCK:
            block_type = action.params.get("block_type", BlockType.PLANK)
            if state.inventory.get(block_type.value, 0) <= 0:
                return False, f"insufficient_inventory: {block_type.name}"

        # 4. Check forbidden block types
        if action.action_type == ActionType.PLACE_BLOCK:
            block_type = action.params.get("block_type", BlockType.PLANK)
            if block_type in self.policy.forbidden_block_types:
                return False, f"forbidden_block_type: {block_type.name}"

        # 5. Check destruction constraints (can't mine unmineable blocks)
        if action.action_type == ActionType.MINE_BLOCK and target_pos:
            tx, ty = target_pos
            block = state.get_block(tx, ty)
            if block in self.policy.forbidden_block_types:
                return False, f"forbidden_destruction: {block.name}"
            if block == BlockType.GRASS or block == BlockType.EMPTY:
                return False, "cannot_mine_grass_or_empty"

        # 6. Rate limiting (turn-based, not action-based in this simplified version)
        if state.turn >= state.max_turns:
            return False, "max_turns_exceeded"

        return True, None

    def filter_actions(self, state: GameState, actions: List[GameAction]) -> List[GameAction]:
        """Batch filter: keep only safe actions."""
        safe = []
        for action in actions:
            ok, reason = self.validate(state, action)
            if ok:
                safe.append(action)
            else:
                self.violation_log.append({
                    "turn": state.turn,
                    "action": str(action),
                    "reason": reason,
                })
        return safe

    def get_violation_summary(self) -> Dict:
        """Summary of safety violations for logging."""
        if not self.violation_log:
            return {"total": 0, "by_reason": {}}
        by_reason = {}
        for v in self.violation_log:
            r = v["reason"]
            by_reason[r] = by_reason.get(r, 0) + 1
        return {
            "total": len(self.violation_log),
            "by_reason": by_reason,
            "violations": self.violation_log,
        }
