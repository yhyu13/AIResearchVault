# -*- coding: utf-8 -*-
"""
Demo 2: Craft Planks — ReAct Loop + Safety Sandbox (非法 craft 拦截)

演示 H=(E,T,C,S,L,V) 在合成任务上的完整流程：
  Phase 1: 正常流程 —— Agent 通过 ReAct 循环把 WOOD 合成为 PLANK，
           由 V (TaskVerifier) 校验 required_inventory。
  Phase 2: 安全演示 —— 在零库存下直接尝试 craft / place_block，
           展示 E (Environment) 的 recipe 校验与 S (SafetySandbox) 的拦截。

Run: python agent_harness_game/demo/craft_item.py
"""
import sys
import os

# Add package root (parent of agent_harness_game/) to path,
# so that `import agent_harness_game` works regardless of cwd.
_PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _PACKAGE_ROOT)

from agent_harness_game import (
    AgentHarness, HarnessConfig,
    TaskSpec, BlockType, GameAction, ActionType,
)


def print_inventory(state):
    """以 ASCII 文本打印当前库存（避免 Windows/Git Bash 下 Unicode 乱码）。"""
    items = {BlockType(k).name: v for k, v in state.inventory.items() if v > 0}
    if not items:
        print("  Inventory: (empty)")
    else:
        for name, count in sorted(items.items()):
            print(f"  Inventory: {name} x{count}")


def main():
    print("=" * 60)
    print("Agent Harness x Game AI -- Demo: Craft Planks")
    print("=" * 60)

    # ------------------------------------------------------------------
    # Phase 1: 正常合成流程（ReAct loop 完整跑通 H=(E,T,C,S,L,V)）
    # ------------------------------------------------------------------
    print("\n[Phase 1] Normal crafting run (ReAct loop)")
    print("-" * 60)

    # 1. Configure harness：初始发放 2 个 WOOD，供 agent 合成
    config = HarnessConfig(
        env_width=10,
        env_height=10,
        max_turns=30,
        context_window=10,
        log_level="DEBUG",  # 逐步打印 [L] 日志
        initial_inventory={BlockType.WOOD.value: 2},
    )
    harness = AgentHarness(config)

    # 2. Set task：craft_planks 要求库存中至少有 4 个 PLANK
    task = TaskSpec.craft_planks()
    harness.set_task(task)

    print(f"\nTask: {task.description}")
    print(f"Required inventory: {{PLANK: 4}}")
    print(f"Initial inventory: {{WOOD: 2}}  (1 WOOD -> 4 PLANK)")
    print("\nRunning harness...\n")

    result = harness.run(agent_strategy="heuristic")

    # 3. 逐步日志回放（来自 L 组件的结构化 logs）
    print("\n" + "-" * 60)
    print("Step-by-step trace (from L component):")
    print("-" * 60)
    for entry in result.logs:
        if entry.get("event_type") == "step":
            info = entry.get("info", {})
            note = ""
            if info.get("crafted"):
                note = f"  -> crafted: {info['crafted']}"
            elif not info.get("success", True):
                note = f"  -> FAILED: {info.get('reason', 'unknown')}"
            print(f"  step {entry['step']:>2}: {entry['action']}{note}")

    # 4. Report
    print("\n" + "=" * 60)
    print("RESULT (Phase 1)")
    print("=" * 60)
    print(f"Success: {result.success}")
    print(f"Total Steps: {result.total_steps}")
    print(f"Overall Score: {result.evaluation.overall_score:.3f}")
    print(f"Safety Violations: {result.safety_violations}")
    print(f"\nDimension Scores:")
    for dim, score in result.evaluation.dimensions.items():
        print(f"  {dim}: {score:.3f}")
    print(f"\nDetails: {result.evaluation.details}")
    print(f"\nFinal inventory:")
    print_inventory(result.final_state)
    print(f"\nFinal State:\n{result.final_state.render()}")

    # ------------------------------------------------------------------
    # Phase 2: 安全演示 —— 非法 craft 与非法放置的拦截
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("[Phase 2] Safety sandbox: illegal action interception")
    print("-" * 60)

    # 直接复用 harness 的 E 与 S 组件，构造一个零库存状态
    state = harness.environment.reset()
    print("\nInitial state: empty inventory (no WOOD, no PLANK)")

    # Case A: 零 WOOD 下尝试 craft —— S 不拦截 craft，但 E 的 recipe 校验拒绝执行
    craft_action = GameAction(ActionType.CRAFT, {"recipe": "plank"})
    ok, reason = harness.safety.validate(state, craft_action)
    print(f"\n[Case A] craft('plank') with 0 WOOD")
    print(f"  S (SafetySandbox) validate: ok={ok}, reason={reason}")
    next_state, reward, done, info = harness.environment.step(state, craft_action)
    print(f"  E (Environment) step: success={info['success']}, "
          f"reason={info.get('reason', '-')}")
    print(f"  Inventory after: PLANK={next_state.inventory.get(BlockType.PLANK.value, 0)}"
          f" (unchanged, illegal craft rejected)")

    # Case B: 零 PLANK 下尝试 place_block —— S 直接拦截，动作不会进入 E
    place_action = GameAction(ActionType.PLACE_BLOCK, {"block_type": BlockType.PLANK})
    ok, reason = harness.safety.validate(state, place_action)
    print(f"\n[Case B] place_block(PLANK) with 0 PLANK")
    print(f"  S (SafetySandbox) validate: ok={ok}, reason={reason}")
    if not ok:
        print(f"  -> action BLOCKED by S before reaching E "
              f"(agent falls back to NOOP)")
        # 与 harness.py 主循环一致：被拦截的动作替换为 NOOP
        blocked = GameAction(ActionType.NOOP, {"safety_blocked": reason})
        next_state, reward, done, info = harness.environment.step(state, blocked)
        print(f"  E executed fallback: {blocked.action_type.value}")

    # Case C: 未知 recipe —— E 的 recipe 校验拒绝
    bad_recipe = GameAction(ActionType.CRAFT, {"recipe": "diamond_sword"})
    ok, reason = harness.safety.validate(state, bad_recipe)
    next_state, reward, done, info = harness.environment.step(state, bad_recipe)
    print(f"\n[Case C] craft('diamond_sword') unknown recipe")
    print(f"  E (Environment) step: success={info['success']}, "
          f"reason={info.get('reason', '-')}")

    print("\nDone. Phase 1 exit code drives the process exit status.")
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
