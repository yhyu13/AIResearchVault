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
import json
import random
from .environment import GameState, GameAction, ActionType, BlockType
from .context import ContextManager
from .safety import SafetySandbox


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

    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Parse prompt and return a simulated action."""
        if self.strategy == "random":
            return self._random_action()

        # Extract goal and state from prompt
        goal = self._extract_goal(prompt)
        pos = self._extract_position(prompt)
        inventory = self._extract_inventory(prompt)

        if "build wall" in goal.lower() or "build house" in goal.lower():
            return self._building_strategy(goal, pos, inventory)
        elif "craft" in goal.lower():
            return self._crafting_strategy(inventory)
        else:
            return self._random_action()

    def _random_action(self) -> str:
        actions = [a.value for a in ActionType]
        a = random.choice(actions)
        if a == "place_block":
            return json.dumps({"action_type": a, "params": {"block_type": "PLANK"}})
        return json.dumps({"action_type": a, "params": {}})

    def _building_strategy(self, goal: str, pos: Tuple, inventory: Dict) -> str:
        """Simple building: move toward target and place blocks."""
        # Extract target positions from goal if available
        if "wall_2x2" in goal.lower():
            targets = [(4, 4), (5, 4), (4, 5), (5, 5)]
        elif "house_outline" in goal.lower():
            targets = [(3, 3), (4, 3), (5, 3), (3, 4), (5, 4), (3, 5), (4, 5), (5, 5)]
        else:
            return self._random_action()

        x, y = pos
        # Find nearest target that needs a block
        for tx, ty in targets:
            if (x, y) == (tx, ty):
                if inventory.get(BlockType.PLANK.value, 0) > 0 or inventory.get(BlockType.WALL.value, 0) > 0:
                    block = "WALL" if inventory.get(BlockType.WALL.value, 0) > 0 else "PLANK"
                    return json.dumps({"action_type": "place_block", "params": {"block_type": block, "x": x, "y": y}})
            else:
                # Move toward target
                if x < tx:
                    return json.dumps({"action_type": "move_right", "params": {}})
                elif x > tx:
                    return json.dumps({"action_type": "move_left", "params": {}})
                elif y < ty:
                    return json.dumps({"action_type": "move_down", "params": {}})
                elif y > ty:
                    return json.dumps({"action_type": "move_up", "params": {}})

        return self._random_action()

    def _crafting_strategy(self, inventory: Dict) -> str:
        if inventory.get(BlockType.WOOD.value, 0) > 0:
            return json.dumps({"action_type": "craft", "params": {"recipe": "plank"}})
        return json.dumps({"action_type": "noop", "params": {}})

    def _extract_goal(self, prompt: str) -> str:
        for line in prompt.split("\n"):
            if line.startswith("Goal:"):
                return line[5:].strip()
        return ""

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
