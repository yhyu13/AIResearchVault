"""
V — Verification & Evaluation: Task Completion Assessment

Implements the paper's Verification component V(H_T) → R^k.
Supports multi-dimensional evaluation for game tasks.
"""
from typing import Tuple, List, Dict, Optional, Callable
from dataclasses import dataclass, field
from .environment import GameState, BlockType


@dataclass
class TaskSpec:
    """Task specification: what needs to be built/achieved."""
    name: str
    target_blocks: Dict[Tuple[int, int], BlockType] = field(default_factory=dict)
    min_blocks: int = 0
    max_blocks: int = 1000
    required_inventory: Dict[BlockType, int] = field(default_factory=dict)
    max_turns: int = 100
    description: str = ""

    @classmethod
    def build_wall_2x2(cls) -> "TaskSpec":
        return cls(
            name="build_wall_2x2",
            description="Build a 2x2 wall at positions (4,4), (5,4), (4,5), (5,5)",
            target_blocks={
                (4, 4): BlockType.WALL,
                (5, 4): BlockType.WALL,
                (4, 5): BlockType.WALL,
                (5, 5): BlockType.WALL,
            },
            min_blocks=4,
            max_blocks=4,
            max_turns=50,
        )

    @classmethod
    def build_house_outline(cls) -> "TaskSpec":
        return cls(
            name="build_house_outline",
            description="Build a 3x3 house outline with 8 wall blocks",
            target_blocks={
                (3, 3): BlockType.WALL,
                (4, 3): BlockType.WALL,
                (5, 3): BlockType.WALL,
                (3, 4): BlockType.WALL,
                (5, 4): BlockType.WALL,
                (3, 5): BlockType.WALL,
                (4, 5): BlockType.WALL,
                (5, 5): BlockType.WALL,
            },
            min_blocks=8,
            max_turns=80,
        )

    @classmethod
    def craft_planks(cls) -> "TaskSpec":
        return cls(
            name="craft_planks",
            description="Craft at least 4 planks from wood",
            required_inventory={BlockType.PLANK: 4},
            max_turns=30,
        )


@dataclass
class EvaluationResult:
    """Multi-dimensional evaluation result."""
    overall_score: float  # 0.0 to 1.0
    dimensions: Dict[str, float]
    passed: bool
    details: Dict = field(default_factory=dict)


class TaskVerifier:
    """
    V(H_T) → R^k: evaluates task completion on multiple dimensions.
    
    Dimensions for game tasks:
    - structure_correctness: target blocks match exactly
    - block_count: total blocks within bounds
    - efficiency: turns used / max_turns
    - inventory_match: required inventory achieved
    """

    def __init__(self, task_spec: TaskSpec):
        self.task_spec = task_spec

    def evaluate(self, state: GameState) -> EvaluationResult:
        """Full evaluation of current state against task spec."""
        dims = {}
        details = {}

        # Dimension 1: Structure correctness (if target_blocks defined)
        if self.task_spec.target_blocks:
            correct = 0
            total_target = len(self.task_spec.target_blocks)
            extra = 0
            for y, row in enumerate(state.grid):
                for x, cell in enumerate(row):
                    if (x, y) in self.task_spec.target_blocks:
                        expected = self.task_spec.target_blocks[(x, y)]
                        if cell == expected.value:
                            correct += 1
                    elif cell != BlockType.GRASS.value and cell != BlockType.EMPTY.value:
                        # Check if it's an extra block not in target
                        if (x, y) not in self.task_spec.target_blocks:
                            extra += 1
            
            if total_target > 0:
                dims["structure_correctness"] = correct / total_target
            else:
                dims["structure_correctness"] = 1.0
            
            details["correct_blocks"] = correct
            details["target_blocks"] = total_target
            details["extra_blocks"] = extra
        else:
            dims["structure_correctness"] = 1.0
            details["structure_correctness"] = "no_target_blocks_defined"

        # Dimension 2: Block count bounds
        total_blocks = sum(1 for row in state.grid for cell in row 
                           if cell not in (BlockType.GRASS.value, BlockType.EMPTY.value))
        if self.task_spec.min_blocks <= total_blocks <= self.task_spec.max_blocks:
            dims["block_count"] = 1.0
        elif total_blocks < self.task_spec.min_blocks:
            dims["block_count"] = total_blocks / max(self.task_spec.min_blocks, 1)
        else:
            dims["block_count"] = max(0, 1.0 - (total_blocks - self.task_spec.max_blocks) / 10)
        details["total_blocks"] = total_blocks

        # Dimension 3: Efficiency
        dims["efficiency"] = max(0, 1.0 - state.turn / self.task_spec.max_turns)
        details["turns_used"] = state.turn
        details["max_turns"] = self.task_spec.max_turns

        # Dimension 4: Inventory match
        if self.task_spec.required_inventory:
            inv_score = 0.0
            inv_count = 0
            for block, req in self.task_spec.required_inventory.items():
                have = state.inventory.get(block.value, 0)
                inv_count += 1
                if have >= req:
                    inv_score += 1.0
                else:
                    inv_score += have / max(req, 1)
            dims["inventory_match"] = inv_score / max(inv_count, 1)
            details["inventory_check"] = {
                b.name: {"have": state.inventory.get(b.value, 0), "need": n}
                for b, n in self.task_spec.required_inventory.items()
            }
        else:
            dims["inventory_match"] = 1.0

        # Overall score: weighted average
        weights = {
            "structure_correctness": 0.4,
            "block_count": 0.2,
            "efficiency": 0.2,
            "inventory_match": 0.2,
        }
        overall = sum(dims[d] * weights[d] for d in weights if d in dims)

        # Pass threshold: all mandatory dimensions >= 0.8, overall >= 0.75
        passed = overall >= 0.75
        if self.task_spec.target_blocks and dims.get("structure_correctness", 1.0) < 0.75:
            passed = False
        if self.task_spec.required_inventory and dims.get("inventory_match", 1.0) < 0.8:
            passed = False

        return EvaluationResult(
            overall_score=overall,
            dimensions=dims,
            passed=passed,
            details=details,
        )

    def verify(self, state: GameState) -> bool:
        """Quick pass/fail check."""
        return self.evaluate(state).passed
