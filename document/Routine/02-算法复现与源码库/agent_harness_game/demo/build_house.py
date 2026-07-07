"""
Demo 1: Build a 2×2 Wall — Full Harness Pipeline

Demonstrates H=(E,T,C,S,L,V) working together to complete a building task.
Run: python agent_harness_game/demo/build_house.py
"""
import sys
import os

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_harness_game import (
    AgentHarness, HarnessConfig,
    TaskSpec, BlockType,
)


def main():
    print("=" * 60)
    print("Agent Harness × Game AI — Demo: Build 2×2 Wall")
    print("=" * 60)

    # 1. Configure harness
    config = HarnessConfig(
        env_width=10,
        env_height=10,
        max_turns=50,
        context_window=10,
        log_level="INFO",
    )
    harness = AgentHarness(config)

    # 2. Set task
    task = TaskSpec.build_wall_2x2()
    harness.set_task(task)

    # 3. Give agent initial resources (for demo purposes)
    initial_blocks = {
        # Pre-place some wood for the agent to mine
    }

    # 4. Run with heuristic agent
    print(f"\nTask: {task.description}")
    print(f"Target blocks: {len(task.target_blocks)}")
    print("\nRunning harness...\n")

    result = harness.run(initial_blocks=initial_blocks, agent_strategy="heuristic")

    # 5. Report
    print("\n" + "=" * 60)
    print("RESULT")
    print("=" * 60)
    print(f"Success: {result.success}")
    print(f"Total Steps: {result.total_steps}")
    print(f"Overall Score: {result.evaluation.overall_score:.3f}")
    print(f"Safety Violations: {result.safety_violations}")
    print(f"\nDimension Scores:")
    for dim, score in result.evaluation.dimensions.items():
        print(f"  {dim}: {score:.3f}")
    print(f"\nDetails: {result.evaluation.details}")
    print(f"\nFinal State:\n{result.final_state.render()}")

    # 6. Full trace export
    trace = harness.get_full_trace()
    print(f"\nTrajectory length: {len(trace['trajectory'])} steps")
    print(f"Total safety violations: {trace['safety_summary']['total']}")

    if trace['safety_summary']['total'] > 0:
        print("Violation breakdown:")
        for reason, count in trace['safety_summary']['by_reason'].items():
            print(f"  {reason}: {count}")

    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
