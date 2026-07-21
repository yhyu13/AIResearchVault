# -*- coding: utf-8 -*-
"""
Demo 3: Benchmark Runner — N seeds x M episodes 基准评测

依赖并行开发的 agent_harness_game.evaluation 模块，公开 API：
  - default_suite()        -> TaskSuite
  - BenchmarkRunner(...)   N seeds x M episodes 配置
  - render_markdown(...)   渲染 Markdown 报告
  - save_json(...)         保存 JSON 结果

若 evaluation.py 尚未就绪，本 demo 会给出友好提示并正常退出（exit 0）。

Run: python agent_harness_game/demo/run_benchmark.py
"""
import sys
import os

# Add package root (parent of agent_harness_game/) to path,
# so that `import agent_harness_game` works regardless of cwd.
_PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _PACKAGE_ROOT)

# 输出目录：demo/output/
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

# 小规模套件配置：N seeds x M episodes
N_SEEDS = 2
M_EPISODES = 2


def main():
    print("=" * 60)
    print("Agent Harness x Game AI -- Demo: Benchmark Runner")
    print("=" * 60)

    # ------------------------------------------------------------------
    # 0. 尝试导入并行开发的 evaluation 模块
    # ------------------------------------------------------------------
    try:
        from agent_harness_game.evaluation import (
            TaskSuite, BenchmarkRunner, default_suite,
            render_markdown, save_json,
        )
    except ImportError as e:
        print("\n[SKIP] agent_harness_game.evaluation is not available yet.")
        print(f"       ImportError: {e}")
        print("       The evaluation module is being developed in parallel.")
        print("       Once it lands, this demo will run the benchmark:")
        print(f"         suite     = default_suite()")
        print(f"         runner    = BenchmarkRunner(suite, "
              f"n_seeds={N_SEEDS}, m_episodes={M_EPISODES})")
        print(f"         report    = runner.render_markdown(results)")
        print(f"         json out  -> {OUTPUT_DIR}")
        return 0

    # ------------------------------------------------------------------
    # 1. 构建默认任务套件
    # ------------------------------------------------------------------
    suite = default_suite()
    suite_name = getattr(suite, "name", "default_suite")
    n_tasks = len(getattr(suite, "entries", getattr(suite, "tasks", [])) or [])
    print(f"\nTask suite: {suite_name} ({n_tasks} tasks)")
    print(f"Config: N seeds = {N_SEEDS}, M episodes = {M_EPISODES}")

    # ------------------------------------------------------------------
    # 2. 运行基准（N seeds x M episodes）
    # ------------------------------------------------------------------
    runner = BenchmarkRunner(n_seeds=N_SEEDS, m_episodes=M_EPISODES)

    print("\nRunning benchmark...\n")
    results = runner.run_suite(suite)

    # ------------------------------------------------------------------
    # 3. 打印 Markdown 报告
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("BENCHMARK REPORT (Markdown)")
    print("=" * 60)
    report_md = render_markdown(results)
    print(report_md)

    # ------------------------------------------------------------------
    # 4. 保存 JSON 结果到 demo/output/
    # ------------------------------------------------------------------
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    json_path = os.path.join(OUTPUT_DIR, "benchmark_results.json")
    save_json(results, json_path)
    print(f"\nJSON results saved to: {json_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
