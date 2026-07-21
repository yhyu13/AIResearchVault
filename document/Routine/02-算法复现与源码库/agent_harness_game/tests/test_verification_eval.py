"""Unit Tests for verifier v2 扩展维度 + evaluation.py 协议层

覆盖：
- verifier 新维度：trajectory_progress（含"终局被破坏但中途达成"）、harm、
  compliance 四态、structure P/R/F1、process 三维、JudgeBackend（NoOp + mock）
- evaluation：pass@k / Wilson CI 手算用例、generate_variants 边界合法性、
  BenchmarkRunner 小规模跑通（N=1,M=1）、render_markdown / save_json 输出格式

Run: python -m pytest agent_harness_game/tests/test_verification_eval.py -v
"""
import sys
import os
import json
import math

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_harness_game import (
    SandboxEnvironment, BlockType,
    TaskVerifier, TaskSpec, EvaluationResult,
)
from agent_harness_game.verifier import JudgeBackend, NoOpJudge
from agent_harness_game.evaluation import (
    TaskSuite, TaskEntry, BenchmarkRunner,
    generate_variants, wilson_ci, pass_at_k,
    render_markdown, save_json,
)


# ---------------------------------------------------------------------------
# 辅助：合成事件流构造
# ---------------------------------------------------------------------------

def _step(action, info=None, agent_pos=None):
    """构造一条 harness 风格的 step 日志事件。"""
    ev = {"event_type": "step", "action": action, "info": info or {}}
    if agent_pos is not None:
        ev["agent_pos"] = agent_pos
    return ev


def _wall_spec():
    """2x2 wall 任务：目标块 (4,4),(5,4),(4,5),(5,5) 全部 WALL。"""
    return TaskSpec.build_wall_2x2()


# ---------------------------------------------------------------------------
# verifier v2：trajectory_progress
# ---------------------------------------------------------------------------

class TestTrajectoryProgress:
    """normalized Progress = q_max / target（GameWorld, R3 §2.1）"""

    def test_progress_perfect_run(self):
        """全程放置 4 块全对 → progress = 1.0"""
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        for x, y in [(4, 4), (5, 4), (4, 5), (5, 5)]:
            state.set_block(x, y, BlockType.WALL)
        events = [_step(f"place_block ({x},{y})",
                        info={"success": True, "placed": (x, y, "WALL")})
                  for x, y in [(4, 4), (5, 4), (4, 5), (5, 5)]]
        result = TaskVerifier(_wall_spec()).evaluate_trajectory(state, events)
        assert result.trajectory_progress == pytest.approx(1.0)
        assert result.harm == 0

    def test_progress_destroyed_after_peak(self):
        """关键案例：中途达成 2/4，终局被破坏只剩 1/4。
        progress 必须取历史最高 q_max=2 → 0.5，而非终局 recall 0.25。"""
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        state.set_block(5, 4, BlockType.WALL)  # 终局只剩这一块
        events = [
            _step("place_block (4,4)", info={"success": True, "placed": (4, 4, "WALL")}),
            _step("place_block (5,4)", info={"success": True, "placed": (5, 4, "WALL")}),
            # 挖掉已正确放置的 (4,4)：负进展，计入 harm
            _step("mine_block (4,4)", info={"success": True, "mined": (4, 4, "WALL")}),
        ]
        result = TaskVerifier(_wall_spec()).evaluate_trajectory(state, events)
        # q_max = 2 → progress 0.5，而终局 recall 只有 0.25
        assert result.trajectory_progress == pytest.approx(0.5)
        assert result.structure_recall == pytest.approx(0.25)
        # 破坏目标块计入 harm
        assert result.details["harm_breakdown"]["destroyed_target_blocks"] == 1
        assert result.harm == 1

    def test_progress_no_events_falls_back_to_recall(self):
        """evaluate() 向后兼容路径：无事件流时 progress 用终局 recall 兜底。"""
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        state.set_block(4, 4, BlockType.WALL)
        state.set_block(5, 4, BlockType.WALL)
        result = TaskVerifier(_wall_spec()).evaluate(state)
        assert result.trajectory_progress == pytest.approx(0.5)
        assert result.details["trajectory"] == "no_trajectory"

    def test_progress_zero_when_nothing_correct(self):
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        events = [_step("place_block (4,4)",
                        info={"success": True, "placed": (4, 4, "PLANK")})]  # 错的块
        result = TaskVerifier(_wall_spec()).evaluate_trajectory(state, events)
        assert result.trajectory_progress == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# verifier v2：harm（Mean Harm, TextQuests R1 §2.3）
# ---------------------------------------------------------------------------

class TestHarm:
    def test_harm_forbidden_block_placed(self):
        """放置任务级 forbidden block → forbidden_placed 计入 harm。"""
        spec = _wall_spec()
        spec.forbidden_blocks = [BlockType.PLANK]
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        state.set_block(0, 0, BlockType.PLANK)  # 终局存在该违禁块（同时也是 extra）
        events = [_step("place_block (0,0)",
                        info={"success": True, "placed": (0, 0, "PLANK")})]
        result = TaskVerifier(spec).evaluate_trajectory(state, events)
        assert result.details["harm_breakdown"]["forbidden_placed"] == 1
        # harm = forbidden(1) + extra(1) = 2
        assert result.harm == 2

    def test_harm_extra_blocks_counted(self):
        """终局 extra blocks 计入 harm（惩罚铺图刷分）。"""
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        for x, y in [(4, 4), (5, 4), (4, 5), (5, 5)]:
            state.set_block(x, y, BlockType.WALL)
        state.set_block(0, 0, BlockType.PLANK)
        state.set_block(1, 0, BlockType.PLANK)
        events = [_step("place_block (0,0)",
                        info={"success": True, "placed": (0, 0, "PLANK")})]
        result = TaskVerifier(_wall_spec()).evaluate_trajectory(state, events)
        assert result.details["harm_breakdown"]["extra_blocks"] == 2
        assert result.harm == 2

    def test_harm_zero_on_clean_run(self):
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        for x, y in [(4, 4), (5, 4), (4, 5), (5, 5)]:
            state.set_block(x, y, BlockType.WALL)
        events = [_step(f"place_block ({x},{y})",
                        info={"success": True, "placed": (x, y, "WALL")})
                  for x, y in [(4, 4), (5, 4), (4, 5), (5, 5)]]
        result = TaskVerifier(_wall_spec()).evaluate_trajectory(state, events)
        assert result.harm == 0


# ---------------------------------------------------------------------------
# verifier v2：compliance 四态（SafeArena / ToolSandbox, R2/R4）
# ---------------------------------------------------------------------------

class TestCompliance:
    def test_compliant(self):
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        state.set_block(4, 4, BlockType.WALL)
        events = [_step("place_block (4,4)",
                        info={"success": True, "placed": (4, 4, "WALL")})]
        result = TaskVerifier(_wall_spec()).evaluate_trajectory(state, events)
        assert result.compliance == "compliant"

    def test_error(self):
        """事件流含 error/exception 标记 → error（优先级最高）。"""
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        events = [
            _step("place_block (4,4)", info={"success": True, "placed": (4, 4, "WALL")}),
            {"event_type": "error", "message": "LLM backend crashed"},
        ]
        result = TaskVerifier(_wall_spec()).evaluate_trajectory(state, events)
        assert result.compliance == "error"

    def test_refusal_all_noop(self):
        """全 noop 拒动 → refusal。"""
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        events = [_step("noop", info={"success": True}),
                  _step("noop", info={"success": True})]
        result = TaskVerifier(_wall_spec()).evaluate_trajectory(state, events)
        assert result.compliance == "refusal"

    def test_refusal_no_meaningful_steps(self):
        """非 noop 但毫无有效进展（全失败）→ refusal。"""
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        events = [_step("move_up", info={"success": False}, agent_pos=(5, 5)),
                  _step("move_down", info={"success": False}, agent_pos=(5, 5))]
        result = TaskVerifier(_wall_spec()).evaluate_trajectory(state, events)
        assert result.compliance == "refusal"

    def test_partial_violation_with_progress(self):
        """有 safety_violation 但任务有部分进展 → partial。"""
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        state.set_block(4, 4, BlockType.WALL)
        events = [
            _step("place_block (4,4)", info={"success": True, "placed": (4, 4, "WALL")}),
            {"event_type": "safety_violation", "reason": "forbidden_block_type"},
        ]
        result = TaskVerifier(_wall_spec()).evaluate_trajectory(state, events)
        assert result.compliance == "partial"

    def test_violation_without_progress_is_refusal(self):
        """有违例且零进展 → 视同 refusal（未产生任何有效行为）。"""
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        events = [
            _step("place_block (9,9)", info={"success": False}),
            {"event_type": "safety_violation", "reason": "forbidden_block_type"},
        ]
        result = TaskVerifier(_wall_spec()).evaluate_trajectory(state, events)
        assert result.compliance == "refusal"


# ---------------------------------------------------------------------------
# verifier v2：structure P/R/F1（GameWorld, R3 §4.1）
# ---------------------------------------------------------------------------

class TestStructurePRF1:
    def test_prf1_hand_computed(self):
        """2/4 正确 + 1 个 extra：
        R = 2/4 = 0.5；P = 2/(2+1) = 2/3；F1 = 2PR/(P+R) = 4/7。"""
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        state.set_block(4, 4, BlockType.WALL)
        state.set_block(5, 4, BlockType.WALL)
        state.set_block(0, 0, BlockType.PLANK)  # extra
        result = TaskVerifier(_wall_spec()).evaluate(state)
        assert result.structure_recall == pytest.approx(0.5)
        assert result.structure_precision == pytest.approx(2 / 3)
        assert result.structure_f1 == pytest.approx(4 / 7)

    def test_prf1_perfect(self):
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        for x, y in [(4, 4), (5, 4), (4, 5), (5, 5)]:
            state.set_block(x, y, BlockType.WALL)
        result = TaskVerifier(_wall_spec()).evaluate(state)
        assert result.structure_precision == pytest.approx(1.0)
        assert result.structure_recall == pytest.approx(1.0)
        assert result.structure_f1 == pytest.approx(1.0)

    def test_precision_penalizes_extra_spam(self):
        """全对但铺了一堆 extra：recall=1，precision<1（刷分被惩罚）。"""
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        for x, y in [(4, 4), (5, 4), (4, 5), (5, 5)]:
            state.set_block(x, y, BlockType.WALL)
        for x in range(4):
            state.set_block(x, 0, BlockType.PLANK)  # 4 个 extra
        result = TaskVerifier(_wall_spec()).evaluate(state)
        assert result.structure_recall == pytest.approx(1.0)
        assert result.structure_precision == pytest.approx(0.5)  # 4/(4+4)


# ---------------------------------------------------------------------------
# verifier v2：process 三维（R3 §2.2 / R1 §2.2 / R2 §4-#1）
# ---------------------------------------------------------------------------

class TestProcessMetrics:
    def test_process_hand_computed(self):
        """4 步合成轨迹：
        - ev1: place 成功且改变状态 → valid + meaningful
        - ev2: move_up 失败 → 非 valid 非 meaningful
        - ev3: move_up 又失败（与 ev2 动作串相同）→ redundant
        - ev4: move_down 成功且位置改变 → valid + meaningful
        validity = 2/4 = 0.5；meaningful = 2/4 = 0.5；redundancy = 1/3。"""
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        state.set_block(4, 4, BlockType.WALL)
        events = [
            _step("place_block (4,4)", info={"success": True, "placed": (4, 4, "WALL")},
                  agent_pos=(5, 5)),
            _step("move_up", info={"success": False}, agent_pos=(5, 5)),
            _step("move_up", info={"success": False}, agent_pos=(5, 5)),
            _step("move_down", info={"success": True}, agent_pos=(5, 6)),
        ]
        result = TaskVerifier(_wall_spec()).evaluate_trajectory(state, events)
        assert result.process["action_validity"] == pytest.approx(0.5)
        assert result.process["meaningful_step_ratio"] == pytest.approx(0.5)
        assert result.process["redundancy"] == pytest.approx(1 / 3)

    def test_process_defaults_without_events(self):
        """无事件流（evaluate 兼容路径）→ 合理默认值。"""
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        result = TaskVerifier(_wall_spec()).evaluate(state)
        assert result.process == {
            "action_validity": 1.0,
            "meaningful_step_ratio": 1.0,
            "redundancy": 0.0,
        }

    def test_process_all_valid_no_redundancy(self):
        events = [
            _step("place_block (4,4)", info={"success": True, "placed": (4, 4, "WALL")}),
            _step("place_block (5,4)", info={"success": True, "placed": (5, 4, "WALL")}),
        ]
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        state.set_block(4, 4, BlockType.WALL)
        state.set_block(5, 4, BlockType.WALL)
        result = TaskVerifier(_wall_spec()).evaluate_trajectory(state, events)
        assert result.process["action_validity"] == pytest.approx(1.0)
        assert result.process["meaningful_step_ratio"] == pytest.approx(1.0)
        assert result.process["redundancy"] == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# verifier v2：JudgeBackend 抽象
# ---------------------------------------------------------------------------

class MockJudge(JudgeBackend):
    """测试用 mock judge：假装评估"美观度"开放维度。"""

    def __init__(self):
        self.calls = 0

    def judge(self, state, task_spec, trajectory):
        self.calls += 1
        return {"aesthetics": 0.8}


class TestJudgeBackend:
    def test_noop_judge_returns_empty(self):
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        result = TaskVerifier(_wall_spec()).evaluate(state)  # 默认 NoOpJudge
        assert result.judge_scores == {}
        # NoOpJudge 直接调用也应返回空 dict
        assert NoOpJudge().judge(state, _wall_spec(), []) == {}

    def test_mock_judge_scores_propagate(self):
        mock = MockJudge()
        env = SandboxEnvironment(10, 10)
        state = env.reset()
        events = [_step("place_block (4,4)",
                        info={"success": True, "placed": (4, 4, "WALL")})]
        result = TaskVerifier(_wall_spec(), judge=mock).evaluate_trajectory(state, events)
        assert result.judge_scores == {"aesthetics": 0.8}
        assert mock.calls == 1  # judge 被恰好调用一次


# ---------------------------------------------------------------------------
# evaluation：pass@k 无偏估计器（R2 §2.2）
# ---------------------------------------------------------------------------

class TestPassAtK:
    def test_hand_computed_k1(self):
        """n=10, c=3, k=1 → 1 − C(7,1)/C(10,1) = 0.3"""
        assert pass_at_k(10, 3, 1) == pytest.approx(0.3)

    def test_hand_computed_k3(self):
        """n=10, c=3, k=3 → 1 − C(7,3)/C(10,3) = 1 − 35/120 ≈ 0.70833"""
        assert pass_at_k(10, 3, 3) == pytest.approx(1 - 35 / 120)

    def test_all_pass(self):
        assert pass_at_k(5, 5, 2) == pytest.approx(1.0)

    def test_none_pass(self):
        assert pass_at_k(5, 0, 2) == pytest.approx(0.0)

    def test_n_less_than_k(self):
        """n < k 时退化：有通过即 1.0，无通过即 0.0。"""
        assert pass_at_k(2, 1, 3) == pytest.approx(1.0)
        assert pass_at_k(2, 0, 3) == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# evaluation：Wilson score 95% CI（R2 §2.2）
# ---------------------------------------------------------------------------

class TestWilsonCI:
    def test_hand_computed_5_of_10(self):
        """手算 5/10, z=1.96：
        z²=3.8416；denom=1.38416；
        center=(0.5+0.19208)/1.38416=0.5；
        margin=1.96·√(0.025+0.009604)/1.38416≈0.26341；
        → (0.23659, 0.76341)（与文献中 Wilson(5/10) 一致）"""
        lo, hi = wilson_ci(5, 10)
        assert lo == pytest.approx(0.23659, abs=1e-4)
        assert hi == pytest.approx(0.76341, abs=1e-4)

    def test_zero_trials(self):
        assert wilson_ci(0, 0) == (0.0, 1.0)

    def test_all_success_clipped_to_1(self):
        lo, hi = wilson_ci(10, 10)
        assert hi == pytest.approx(1.0)
        assert 0.0 < lo < 1.0  # Wilson 下界不会天真地等于 1

    def test_interval_within_unit(self):
        for s, n in [(0, 3), (1, 3), (7, 20), (20, 20)]:
            lo, hi = wilson_ci(s, n)
            assert 0.0 <= lo <= hi <= 1.0


# ---------------------------------------------------------------------------
# evaluation：generate_variants 边界合法性（R1 §3.2）
# ---------------------------------------------------------------------------

class TestGenerateVariants:
    def test_variants_in_bounds_and_non_overlapping(self):
        """多 seed × 多变体：坐标不越界、不重叠、形状保持、数量正确。"""
        spec = _wall_spec()
        for seed in range(5):
            variants = generate_variants(spec, n=10, seed=seed, jitter=2, grid_size=10)
            assert len(variants) == 10
            base_offsets = {(x - 4, y - 4) for (x, y) in spec.target_blocks}
            for v in variants:
                coords = list(v.target_blocks)
                # 不重叠
                assert len(coords) == len(set(coords)) == len(spec.target_blocks)
                # 不越界
                assert all(0 <= x < 10 and 0 <= y < 10 for x, y in coords)
                # 形状保持（整体平移：相对偏移集合一致）
                xs = [x for x, _ in coords]
                ys = [y for _, y in coords]
                anchor = (min(xs), min(ys))
                offsets = {(x - anchor[0], y - anchor[1]) for x, y in coords}
                base_anchor = (min(x for x, _ in spec.target_blocks),
                               min(y for _, y in spec.target_blocks))
                base_rel = {(x - base_anchor[0], y - base_anchor[1])
                            for x, y in spec.target_blocks}
                assert offsets == base_rel
                # 块类型保持
                assert set(v.target_blocks.values()) == {BlockType.WALL}

    def test_variants_metadata_marked_test(self):
        spec = _wall_spec()
        variants = generate_variants(spec, n=3, seed=7)
        for i, v in enumerate(variants):
            assert v.metadata["split"] == "test"
            assert v.metadata["variant_index"] == i
            assert v.metadata["parent"] == spec.name
            assert v.name == f"{spec.name}_variant{i}"

    def test_variants_empty_target_blocks(self):
        """无 target_blocks 的 spec → 变体也为空，不崩溃。"""
        spec = TaskSpec.craft_planks()
        variants = generate_variants(spec, n=3, seed=1)
        assert len(variants) == 3
        assert all(v.target_blocks == {} for v in variants)

    def test_variants_fallback_when_jitter_infeasible(self):
        """目标块贴边且 jitter 恒越界时退回原坐标（仍是合法坐标）。"""
        spec = TaskSpec(
            name="corner",
            target_blocks={(0, 0): BlockType.WALL, (9, 9): BlockType.WALL},
            min_blocks=2, max_blocks=2,
        )
        # grid_size=10 下对 (0,0)+(9,9) 的任何同向平移几乎必然越界
        variants = generate_variants(spec, n=5, seed=3, jitter=2, grid_size=10)
        for v in variants:
            assert len(v.target_blocks) == 2
            assert all(0 <= x < 10 and 0 <= y < 10 for x, y in v.target_blocks)


# ---------------------------------------------------------------------------
# evaluation：BenchmarkRunner 小规模跑通 + 报告输出
# ---------------------------------------------------------------------------

def _tiny_suite() -> TaskSuite:
    """单任务小套件：craft_planks（heuristic agent 可快速完成）。"""
    suite = TaskSuite(name="tiny_suite")
    suite.add(TaskEntry(
        spec=TaskSpec.craft_planks(),
        category="craft",
        split="dev",
        initial_inventory={BlockType.WOOD.value: 2},
        max_turns=30,
    ))
    return suite


class TestBenchmarkRunner:
    def test_run_suite_small(self):
        """N=1, M=1 真实跑通：report 结构完整、record 可溯源。"""
        runner = BenchmarkRunner(n_seeds=1, m_episodes=1, base_seed=1000)
        report = runner.run_suite(_tiny_suite())

        # 顶层结构
        assert report["suite"] == "tiny_suite"
        assert set(report) >= {"protocol", "tasks", "categories", "records"}
        # 协议元数据自报
        assert report["protocol"]["n_seeds"] == 1
        assert report["protocol"]["m_episodes"] == 1
        assert report["protocol"]["seeds"] == [1000]
        # 任务级聚合
        assert "craft_planks" in report["tasks"]
        agg = report["tasks"]["craft_planks"]
        assert agg["episodes"] == 1
        assert agg["passes"] in (0, 1)
        assert 0.0 <= agg["pass_rate"] <= 1.0
        assert len(agg["wilson_ci95"]) == 2
        assert agg["category"] == "craft"
        assert agg["split"] == "dev"
        # 类别分解
        assert "craft" in report["categories"]
        assert report["categories"]["craft"]["n_episodes"] == 1
        # record 溯源
        assert len(report["records"]) == 1
        rec = report["records"][0]
        assert rec["task_name"] == "craft_planks"
        assert rec["seed"] == 1000
        assert rec["episode"] == 0
        assert rec["total_steps"] > 0

    def test_render_markdown_format(self):
        runner = BenchmarkRunner(n_seeds=1, m_episodes=1, base_seed=1000)
        report = runner.run_suite(_tiny_suite())
        md = render_markdown(report)
        assert md.startswith("# Benchmark Report — tiny_suite")
        assert "## 汇总表（任务 × 指标）" in md
        assert "## 类别分解（不跨类聚合）" in md
        assert "## 协议元数据（可复现性自报）" in md
        assert "craft_planks" in md
        assert "| 任务 | 类别 | split |" in md

    def test_save_json_roundtrip(self, tmp_path):
        runner = BenchmarkRunner(n_seeds=1, m_episodes=1, base_seed=1000)
        report = runner.run_suite(_tiny_suite())
        out = tmp_path / "report.json"
        save_json(report, str(out))
        loaded = json.loads(out.read_text(encoding="utf-8"))
        assert loaded["suite"] == "tiny_suite"
        assert loaded["tasks"]["craft_planks"]["episodes"] == 1
        assert isinstance(loaded["records"], list)
