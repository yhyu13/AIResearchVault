"""
C — Context Management: Observation, History, and State Compression

Implements the paper's Context Management component.
Manages: (1) observation history, (2) inventory state, (3) goal tracking, (4) state compression.
"""
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from .environment import GameState, GameAction, BlockType


@dataclass
class ContextEntry:
    """Single entry in context history: (turn, observation, action, reward, info)"""
    turn: int
    observation: Dict
    action: Optional[GameAction]
    reward: float
    info: Dict
    state_snapshot: Optional[GameState] = None


class ContextManager:
    """
    C: Context management with sliding window + state summarization.
    
    Key features:
    1. Full history logging (for reproducibility)
    2. Sliding window context (for LLM prompt limits)
    3. State compression (grid → key facts)
    4. Goal tracking
    """

    def __init__(self, max_history: int = 100, context_window: int = 10):
        self.max_history = max_history
        self.context_window = context_window
        self.history: List[ContextEntry] = []
        self.goal: Optional[str] = None
        self.metadata: Dict = {}

    def set_goal(self, goal: str):
        self.goal = goal

    def record(self, state: GameState, observation: Dict, action: GameAction,
               reward: float, info: Dict, save_snapshot: bool = False):
        """Record one interaction step."""
        entry = ContextEntry(
            turn=state.turn,
            observation=observation,
            action=action,
            reward=reward,
            info=info,
            state_snapshot=state.clone() if save_snapshot else None,
        )
        self.history.append(entry)
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get_recent_context(self, n: Optional[int] = None) -> List[ContextEntry]:
        """Get last n entries (or context_window entries)."""
        k = n or self.context_window
        return self.history[-k:]

    def summarize_state(self, state: GameState) -> str:
        """Compress full state into a text summary for LLM context."""
        x, y = state.agent_pos
        lines = [
            f"Turn {state.turn}/{state.max_turns}",
            f"Position: ({x}, {y})",
            "Inventory:",
        ]
        for block_type, count in state.inventory.items():
            if count > 0:
                name = BlockType(block_type).name
                lines.append(f"  - {name}: {count}")
        lines.append("Grid snapshot:")
        lines.append(state.render())
        return "\n".join(lines)

    def build_agent_prompt(self, state: GameState, observation: Dict,
                           available_actions: List[str]) -> str:
        """
        Build LLM prompt from current context.
        This is the key bridge from game state → natural language for LLM.
        """
        lines = []
        if self.goal:
            lines.append(f"Goal: {self.goal}")
        lines.append("")
        lines.append("Current State:")
        lines.append(self.summarize_state(state))
        lines.append("")
        lines.append("Recent Actions:")
        for entry in self.get_recent_context(5):
            act_str = str(entry.action) if entry.action else "None"
            lines.append(f"  T{entry.turn}: {act_str} → {entry.info}")
        lines.append("")
        lines.append("Available Actions:")
        for act in available_actions:
            lines.append(f"  - {act}")
        lines.append("")
        lines.append("What action do you choose? Respond with a JSON object:")
        lines.append('{"action_type": "move_up|move_down|move_left|move_right|place_block|mine_block|craft|noop", "params": {...}}')
        return "\n".join(lines)

    def compress_history(self) -> Dict:
        """Compress full history into a compact summary for logging."""
        if not self.history:
            return {}
        total_reward = sum(e.reward for e in self.history)
        action_counts = {}
        for e in self.history:
            if e.action:
                k = e.action.action_type.value
                action_counts[k] = action_counts.get(k, 0) + 1
        return {
            "total_steps": len(self.history),
            "total_reward": total_reward,
            "action_distribution": action_counts,
            "goal": self.goal,
            "metadata": self.metadata,
        }

    def get_trajectory_for_verification(self) -> List[Dict]:
        """Export clean trajectory for verifier V."""
        return [
            {
                "turn": e.turn,
                "action": str(e.action) if e.action else None,
                "reward": e.reward,
                "info": e.info,
            }
            for e in self.history
        ]

    def reset(self):
        self.history = []
        self.goal = None
        self.metadata = {}
