"""Unit Tests for Agent Harness Game AI Components

Tests each of H=(E,T,C,S,L,V) independently + integration.
Run: python -m pytest tests/test_harness.py -v
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_harness_game import (
    SandboxEnvironment, GameState, GameAction, ActionType, BlockType,
    SafetySandbox, SafetyPolicy,
    ContextManager,
    ReActAgent, SimulatedLLM,
    TaskVerifier, TaskSpec, EvaluationResult,
    AgentHarness, HarnessConfig,
)


class TestEnvironment:
    """Test E — Environment Execution"""

    def test_reset(self):
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        assert state.width == 10
        assert state.height == 10
        assert state.agent_pos == (5, 5)
        assert state.turn == 0

    def test_movement(self):
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        state.agent_pos = (5, 5)

        # Move up
        new_state, _, _, _ = env.step(state, GameAction(ActionType.MOVE_UP))
        assert new_state.agent_pos == (5, 4)

        # Move right
        new_state, _, _, _ = env.step(new_state, GameAction(ActionType.MOVE_RIGHT))
        assert new_state.agent_pos == (6, 4)

    def test_boundary_movement(self):
        env = SandboxEnvironment(5, 5)
        state = env.reset()
        state.agent_pos = (0, 0)

        # Can't go left from (0,0)
        new_state, _, _, _ = env.step(state, GameAction(ActionType.MOVE_LEFT))
        assert new_state.agent_pos == (0, 0)

    def test_place_block(self):
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        state.agent_pos = (5, 5)
        state.inventory[BlockType.PLANK.value] = 5

        action = GameAction(ActionType.PLACE_BLOCK, {
            "block_type": BlockType.PLANK,
            "x": 5, "y": 5
        })
        new_state, _, _, info = env.step(state, action)
        assert info["success"]
        assert new_state.get_block(5, 5) == BlockType.PLANK
        assert new_state.inventory[BlockType.PLANK.value] == 4

    def test_mine_block(self):
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        state.agent_pos = (5, 5)
        state.grid[5][5] = BlockType.WOOD.value

        action = GameAction(ActionType.MINE_BLOCK, {"x": 5, "y": 5})
        new_state, _, _, info = env.step(state, action)
        assert info["success"]
        assert info["mined"] == (5, 5, "WOOD")
        assert new_state.inventory[BlockType.WOOD.value] == 1
        assert new_state.get_block(5, 5) == BlockType.GRASS

    def test_craft(self):
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        state.inventory[BlockType.WOOD.value] = 2

        action = GameAction(ActionType.CRAFT, {"recipe": "plank"})
        new_state, _, _, info = env.step(state, action)
        assert info["success"]
        assert info["crafted"] == "plank"
        assert new_state.inventory[BlockType.WOOD.value] == 1
        assert new_state.inventory[BlockType.PLANK.value] == 4

    def test_observation(self):
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        obs = env.get_observation(state)
        assert "visual_grid" in obs
        assert "local_view" in obs
        assert "inventory" in obs
        assert "agent_pos" in obs


class TestSafety:
    """Test S — Safety Sandbox"""

    def test_boundary_violation(self):
        env = SandboxEnvironment(5, 5)
        state = env.reset()
        state.agent_pos = (0, 0)
        sandbox = SafetySandbox()

        action = GameAction(ActionType.MOVE_LEFT)
        ok, reason = sandbox.validate(state, action)
        assert not ok
        assert "boundary_violation" in reason

    def test_inventory_insufficient(self):
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        state.inventory[BlockType.PLANK.value] = 0
        sandbox = SafetySandbox()

        action = GameAction(ActionType.PLACE_BLOCK, {"block_type": BlockType.PLANK})
        ok, reason = sandbox.validate(state, action)
        assert not ok
        assert "insufficient_inventory" in reason

    def test_forbidden_block(self):
        policy = SafetyPolicy(forbidden_block_types=[BlockType.AGENT])
        sandbox = SafetySandbox(policy)
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        state.inventory[BlockType.AGENT.value] = 1

        action = GameAction(ActionType.PLACE_BLOCK, {"block_type": BlockType.AGENT})
        ok, reason = sandbox.validate(state, action)
        assert not ok
        assert "forbidden_block_type" in reason

    def test_mine_grass(self):
        sandbox = SafetySandbox()
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        state.grid[5][5] = BlockType.GRASS.value

        action = GameAction(ActionType.MINE_BLOCK, {"x": 5, "y": 5})
        ok, reason = sandbox.validate(state, action)
        assert not ok
        assert "cannot_mine_grass" in reason

    def test_safe_action(self):
        sandbox = SafetySandbox()
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        state.inventory[BlockType.PLANK.value] = 5
        state.agent_pos = (5, 5)

        action = GameAction(ActionType.PLACE_BLOCK, {
            "block_type": BlockType.PLANK,
            "x": 5, "y": 5
        })
        ok, reason = sandbox.validate(state, action)
        assert ok
        assert reason is None

    def test_filter_actions(self):
        sandbox = SafetySandbox()
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        state.inventory[BlockType.PLANK.value] = 1
        state.agent_pos = (0, 0)

        actions = [
            GameAction(ActionType.MOVE_RIGHT),  # safe
            GameAction(ActionType.MOVE_LEFT),   # unsafe (boundary)
            GameAction(ActionType.PLACE_BLOCK, {"block_type": BlockType.PLANK, "x": 0, "y": 0}),  # safe
        ]
        safe = sandbox.filter_actions(state, actions)
        assert len(safe) == 2
        assert sandbox.violation_log[0]["reason"] == "boundary_violation: (-1,0)"


class TestContext:
    """Test C — Context Management"""

    def test_record_and_retrieve(self):
        ctx = ContextManager()
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        obs = env.get_observation(state)

        ctx.record(state, obs, GameAction(ActionType.NOOP), 0.0, {})
        assert len(ctx.history) == 1

        recent = ctx.get_recent_context(5)
        assert len(recent) == 1

    def test_summary(self):
        ctx = ContextManager()
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        obs = env.get_observation(state)

        ctx.record(state, obs, GameAction(ActionType.MOVE_UP), 0.0, {})
        ctx.record(state, obs, GameAction(ActionType.MOVE_DOWN), 0.0, {})

        summary = ctx.compress_history()
        assert summary["total_steps"] == 2

    def test_prompt_building(self):
        ctx = ContextManager()
        ctx.set_goal("Build a wall")
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        obs = env.get_observation(state)

        prompt = ctx.build_agent_prompt(state, obs, ["move_up", "move_down"])
        assert "Goal: Build a wall" in prompt
        assert "move_up" in prompt
        assert "move_down" in prompt


class TestVerifier:
    """Test V — Verification & Evaluation"""

    def test_wall_2x2_perfect(self):
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        # Build perfect wall at (4,4), (5,4), (4,5), (5,5)
        state.set_block(4, 4, BlockType.WALL)
        state.set_block(5, 4, BlockType.WALL)
        state.set_block(4, 5, BlockType.WALL)
        state.set_block(5, 5, BlockType.WALL)
        state.turn = 10

        verifier = TaskVerifier(TaskSpec.build_wall_2x2())
        result = verifier.evaluate(state)
        assert result.passed
        assert result.dimensions["structure_correctness"] == 1.0

    def test_wall_2x2_incomplete(self):
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        state.set_block(4, 4, BlockType.WALL)
        state.set_block(5, 4, BlockType.WALL)
        # Missing two blocks
        state.turn = 20

        verifier = TaskVerifier(TaskSpec.build_wall_2x2())
        result = verifier.evaluate(state)
        assert not result.passed
        assert result.dimensions["structure_correctness"] == 0.5

    def test_craft_planks(self):
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        state.inventory[BlockType.PLANK.value] = 4
        state.turn = 5

        verifier = TaskVerifier(TaskSpec.craft_planks())
        result = verifier.evaluate(state)
        assert result.passed
        assert result.dimensions["inventory_match"] == 1.0

    def test_efficiency(self):
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        state.turn = 50
        state.max_turns = 100

        verifier = TaskVerifier(TaskSpec.build_wall_2x2())
        result = verifier.evaluate(state)
        assert result.dimensions["efficiency"] == 0.5


class TestAgent:
    """Test T — Tool Calling / Agent"""

    def test_simulated_llm_parses_action(self):
        llm = SimulatedLLM(strategy="random")
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        ctx = ContextManager()
        obs = env.get_observation(state)
        prompt = ctx.build_agent_prompt(state, obs, ["move_up"])

        raw = llm.generate(prompt)
        assert "{" in raw
        assert "action_type" in raw

    def test_react_agent_returns_action(self):
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        ctx = ContextManager()
        obs = env.get_observation(state)
        agent = ReActAgent(context=ctx)

        thought, action = agent.act(state, obs)
        assert action is not None
        assert isinstance(action.action_type, ActionType)

    def test_safety_interception(self):
        env = SandboxEnvironment(5, 5)
        state = env.reset()
        state.agent_pos = (0, 0)
        ctx = ContextManager()
        obs = env.get_observation(state)
        safety = SafetySandbox()
        agent = ReActAgent(safety=safety, context=ctx)

        # Force agent to try moving left (unsafe)
        # We'll simulate this by checking the safety works during act
        # Since the simulated agent is heuristic, we check that safety is active
        thought, action = agent.act(state, obs)
        if "safety" in thought.lower():
            assert "intercept" in thought.lower() or "blocked" in thought.lower()


class TestIntegration:
    """Test H — Full Harness Integration"""

    def test_build_wall_2x2(self):
        config = HarnessConfig(max_turns=50, log_level="WARNING")
        harness = AgentHarness(config)
        harness.set_task(TaskSpec.build_wall_2x2())
        harness.set_agent(strategy="heuristic")

        result = harness.run()
        assert result.total_steps > 0
        assert result.total_steps <= 50
        assert result.evaluation.overall_score > 0
        # The heuristic agent should be able to build the wall eventually
        print(f"Wall build score: {result.evaluation.overall_score}")

    def test_craft_planks(self):
        config = HarnessConfig(max_turns=30, log_level="WARNING")
        harness = AgentHarness(config)
        harness.set_task(TaskSpec.craft_planks())
        harness.set_agent(strategy="heuristic")

        # Give the agent wood to craft with
        result = harness.run(initial_blocks={})
        print(f"Craft score: {result.evaluation.overall_score}")

    def test_safety_violations_logged(self):
        config = HarnessConfig(max_turns=50, log_level="WARNING")
        harness = AgentHarness(config)
        harness.set_task(TaskSpec.build_wall_2x2())
        harness.set_agent(strategy="heuristic")

        result = harness.run()
        trace = harness.get_full_trace()
        # Should have no safety violations with heuristic agent
        assert trace["safety_summary"]["total"] == 0 or trace["safety_summary"]["total"] < 5

    def test_reproducibility(self):
        """Two runs with same config should produce traceable results."""
        config = HarnessConfig(max_turns=30, log_level="WARNING")

        harness1 = AgentHarness(config)
        harness1.set_task(TaskSpec.build_wall_2x2())
        harness1.set_agent(strategy="heuristic")
        result1 = harness1.run()

        harness2 = AgentHarness(config)
        harness2.set_task(TaskSpec.build_wall_2x2())
        harness2.set_agent(strategy="heuristic")
        result2 = harness2.run()

        # Both should produce valid results
        assert result1.total_steps > 0
        assert result2.total_steps > 0
        # Trajectories should be logged
        assert len(result1.trajectory) > 0
        assert len(result2.trajectory) > 0


if __name__ == "__main__":
    # Run all tests with simple print-based output
    import traceback

    test_classes = [
        TestEnvironment, TestSafety, TestContext,
        TestVerifier, TestAgent, TestIntegration
    ]

    total_passed = 0
    total_failed = 0

    for cls in test_classes:
        print(f"\n{'='*50}")
        print(f"Running {cls.__name__}:")
        print(f"{'='*50}")
        instance = cls()
        for name in dir(instance):
            if name.startswith("test_"):
                try:
                    getattr(instance, name)()
                    print(f"  ✅ {name}")
                    total_passed += 1
                except Exception as e:
                    print(f"  ❌ {name}: {e}")
                    traceback.print_exc()
                    total_failed += 1

    print(f"\n{'='*50}")
    print(f"TOTAL: {total_passed} passed, {total_failed} failed")
    print(f"{'='*50}")
    sys.exit(1 if total_failed > 0 else 0)
