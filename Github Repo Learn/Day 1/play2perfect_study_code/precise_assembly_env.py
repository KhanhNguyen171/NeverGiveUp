"""
Precise assembly environment — study-level structural implementation.

Chapter mapping:
- Ch. 9: Stage 2 — Precise assembly
- Ch. 10: Assembly goal sequence
- Ch. 11: Four assembly tasks
- Ch. 15: Asymmetric actor-critic
- Ch. 17: Environment architecture
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AssemblyGoal:
    """One waypoint in the assembly state machine."""

    name: str
    position_tolerance: float
    orientation_tolerance: float


class PreciseAssemblyEnv:
    """
    Stage-2 wrapper/conceptual environment.

    The research idea is to retain the Play manipulation prior and change the
    task objective to contact-rich assembly. The concrete simulator objects,
    robot articulation, and Isaac Lab lifecycle belong to the full repository.
    """

    TASKS = (
        "tight_insertion",
        "beam_assembly_step1",
        "beam_assembly_step2",
        "screwing",
    )

    def __init__(self, task_name: str, play_env, *, final_goal_only: bool = True):
        # Ch. 9.1 — Stage 2 reuses the Play environment machinery.
        if task_name not in self.TASKS:
            raise ValueError(f"Unknown assembly task: {task_name}")

        self.task_name = task_name
        self.play_env = play_env
        self.final_goal_only = final_goal_only
        self.goal_index = 0
        self.goals: list[AssemblyGoal] = self._build_goal_sequence()

    def _build_goal_sequence(self) -> list[AssemblyGoal]:
        # Ch. 10.1 — assembly is naturally represented as a sequence of
        # geometric sub-goals rather than one undifferentiated objective.
        if self.final_goal_only:
            return [AssemblyGoal("final", 0.0005, 0.05)]

        return [
            AssemblyGoal("transport", 0.01, 0.15),
            AssemblyGoal("pre_insert", 0.003, 0.10),
            AssemblyGoal("final", 0.0005, 0.05),
        ]

    @property
    def current_goal(self) -> AssemblyGoal:
        return self.goals[min(self.goal_index, len(self.goals) - 1)]

    def step_goal(self, position_error: float, orientation_error: float) -> bool:
        """Advance the goal state when the current geometric criterion is met."""
        goal = self.current_goal

        if (
            position_error <= goal.position_tolerance
            and orientation_error <= goal.orientation_tolerance
        ):
            if self.goal_index < len(self.goals) - 1:
                self.goal_index += 1
            return True

        return False

    def reset(self) -> None:
        self.goal_index = 0
