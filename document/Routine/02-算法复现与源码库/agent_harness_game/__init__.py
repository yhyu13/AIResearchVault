"""Agent Harness for Game AI - 六组件架构实现"""
from .environment import SandboxEnvironment, GameState, GameAction, ActionType, BlockType
from .safety import SafetySandbox, SafetyPolicy
from .context import ContextManager, ContextEntry
from .agent import ReActAgent, LLMBackend, SimulatedLLM, AgentResponse, AgentMode
from .verifier import TaskVerifier, TaskSpec, EvaluationResult, JudgeBackend, NoOpJudge
from .harness import AgentHarness, HarnessConfig, HarnessResult
from .evaluation import (
    TaskSuite, TaskEntry, BenchmarkRunner, EpisodeRecord,
    default_suite, generate_variants,
    wilson_ci, pass_at_k, render_markdown, save_json,
    run_ablation, render_ablation_markdown,
)

__version__ = "0.1.0"
__all__ = [
    # E — Environment
    "SandboxEnvironment", "GameState", "GameAction", "ActionType", "BlockType",
    # S — Safety
    "SafetySandbox", "SafetyPolicy",
    # C — Context
    "ContextManager", "ContextEntry",
    # T — Tool/Agent
    "ReActAgent", "LLMBackend", "SimulatedLLM", "AgentResponse", "AgentMode",
    # V — Verification
    "TaskVerifier", "TaskSpec", "EvaluationResult", "JudgeBackend", "NoOpJudge",
    # H — Harness
    "AgentHarness", "HarnessConfig", "HarnessResult",
    # Evaluation — Benchmark 协议层
    "TaskSuite", "TaskEntry", "BenchmarkRunner", "EpisodeRecord",
    "default_suite", "generate_variants",
    "wilson_ci", "pass_at_k", "render_markdown", "save_json",
    "run_ablation", "render_ablation_markdown",
]
