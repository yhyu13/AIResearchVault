"""
H — Harness: 六组件组装器 (E, T, C, S, L, V)

Orchestrates the full Agent Harness pipeline:
  Environment → Safety → Agent → Context → Execution → Verification → Logging

This is the main entry point: H = (E, T, C, S, L, V)
"""
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from .environment import SandboxEnvironment, GameState, GameAction, ActionType
from .safety import SafetySandbox, SafetyPolicy
from .context import ContextManager
from .agent import ReActAgent, LLMBackend, SimulatedLLM
from .verifier import TaskVerifier, TaskSpec, EvaluationResult


@dataclass
class HarnessConfig:
    """Configuration for the game harness."""
    env_width: int = 10
    env_height: int = 10
    max_turns: int = 100
    context_window: int = 10
    safety_policy: Optional[SafetyPolicy] = None
    save_state_snapshots: bool = False
    log_level: str = "INFO"
    initial_inventory: Optional[Dict[int, int]] = None


@dataclass
class HarnessResult:
    """Result of a full harness run."""
    success: bool
    final_state: GameState
    evaluation: EvaluationResult
    total_steps: int
    total_reward: float
    safety_violations: int
    logs: List[Dict] = field(default_factory=list)
    trajectory: List[Dict] = field(default_factory=list)


class AgentHarness:
    """
    H = (E, T, C, S, L, V): Full harness assembly for game AI.

    Pipeline:
    1. Initialize E (environment) with task
    2. Initialize S (safety) with policy
    3. Initialize C (context) with goal
    4. Initialize T (agent) with LLM
    5. Initialize V (verifier) with task spec
    6. Loop: observe → C.build_prompt → T.generate → S.validate → E.step → L.record → V.check
    7. Return HarnessResult with logs, trajectory, and evaluation
    """

    def __init__(self, config: Optional[HarnessConfig] = None):
        self.config = config or HarnessConfig()
        self.environment = SandboxEnvironment(
            self.config.env_width, self.config.env_height
        )
        self.safety = SafetySandbox(self.config.safety_policy or SafetyPolicy.default_game_policy())
        self.context = ContextManager(context_window=self.config.context_window)
        self.verifier: Optional[TaskVerifier] = None
        self.agent: Optional[ReActAgent] = None
        self.logs: List[Dict] = []

    def set_agent(self, agent: Optional[ReActAgent] = None, llm: Optional[LLMBackend] = None,
                  strategy: str = "heuristic"):
        """Set or create the agent."""
        if agent:
            self.agent = agent
        else:
            llm = llm or SimulatedLLM(strategy=strategy)
            self.agent = ReActAgent(llm=llm, safety=self.safety, context=self.context)

    def set_task(self, task_spec: TaskSpec):
        """Set the task and initialize verifier."""
        self.verifier = TaskVerifier(task_spec)
        self.context.set_goal(f"{task_spec.name}: {task_spec.description}")

    def run(self, initial_blocks: Optional[Dict] = None,
            agent_strategy: str = "heuristic") -> HarnessResult:
        """
        Execute full harness episode.
        """
        # Initialize agent if not set
        if not self.agent:
            self.set_agent(strategy=agent_strategy)

        # Initialize environment
        state = self.environment.reset(initial_blocks=initial_blocks)
        state.max_turns = self.config.max_turns
        if self.config.initial_inventory:
            state.inventory.update(self.config.initial_inventory)
        total_reward = 0.0
        done = False
        step = 0

        self._log("harness_start", {
            "task": self.verifier.task_spec.name if self.verifier else "unknown",
            "initial_state": state.render(),
        })

        while not done and step < self.config.max_turns:
            # 1. Observe
            observation = self.environment.get_observation(state)

            # 2. Agent thinks and acts (ReAct)
            thought, action = self.agent.act(state, observation)

            # 3. Safety check (already done in agent, but double-check)
            ok, reason = self.safety.validate(state, action)
            if not ok:
                self._log("safety_violation", {"step": step, "reason": reason, "action": str(action)})
                action = GameAction(ActionType.NOOP, {"safety_blocked": reason})

            # 4. Execute in environment
            next_state, reward, done_env, info = self.environment.step(state, action)

            # 5. Record context
            self.context.record(state, observation, action, reward, info,
                                save_snapshot=self.config.save_state_snapshots)

            # 6. Verify (optional mid-episode check)
            if self.verifier and step % 10 == 0 and step > 0:
                eval_result = self.verifier.evaluate(next_state)
                if eval_result.passed:
                    done = True
                    self._log("task_completed_early", {"step": step, "score": eval_result.overall_score})

            # 7. Transition
            total_reward += reward
            state = next_state
            step += 1
            done = done or done_env

            self._log("step", {
                "step": step,
                "action": str(action),
                "reward": reward,
                "agent_pos": state.agent_pos,
                "info": info,
            })

        # Final verification
        final_eval = EvaluationResult(
            overall_score=0.0,
            dimensions={},
            passed=False,
        )
        if self.verifier:
            final_eval = self.verifier.evaluate(state)

        self._log("harness_end", {
            "total_steps": step,
            "total_reward": total_reward,
            "passed": final_eval.passed,
            "score": final_eval.overall_score,
            "final_state": state.render(),
        })

        return HarnessResult(
            success=final_eval.passed,
            final_state=state,
            evaluation=final_eval,
            total_steps=step,
            total_reward=total_reward,
            safety_violations=len(self.safety.violation_log),
            logs=self.logs,
            trajectory=self.context.get_trajectory_for_verification(),
        )

    def _log(self, event_type: str, data: Dict):
        """Structured logging for L component."""
        entry = {"event_type": event_type, **data}
        self.logs.append(entry)
        if self.config.log_level == "DEBUG":
            print(f"[L] {event_type}: {data}")

    def reset(self):
        """Reset all components for a new episode."""
        self.context.reset()
        self.safety.violation_log = []
        self.logs = []
        if self.agent:
            self.agent.reset()

    def get_full_trace(self) -> Dict:
        """Export full trace for reproducibility (L component)."""
        return {
            "logs": self.logs,
            "context_summary": self.context.compress_history(),
            "safety_summary": self.safety.get_violation_summary(),
            "trajectory": self.context.get_trajectory_for_verification(),
        }
