"""
Play environment — study-level decomposition of the Play stage.

Chapter mapping:
- Ch. 2: Core idea
- Ch. 4: Stage 1 — Play pretraining
- Ch. 6: Reward design
- Ch. 7: Success and termination
- Ch. 8: Success-tolerance curriculum
- Ch. 17: Environment architecture
"""

from __future__ import annotations

import torch

from .utils import obs_utils, reward_utils, termination_utils


class PlayEnv:
    """
    Minimal structural model of the Play environment.

    The full project subclasses Isaac Lab's DirectRLEnv. This class keeps the
    learning logic explicit so that each research component can be studied
    independently from simulator boilerplate.
    """

    def __init__(self, num_envs: int, device: str = "cpu"):
        # Ch. 19 — vectorized environments.
        self.num_envs = num_envs
        self.device = torch.device(device)

        self.episode_length = torch.zeros(num_envs, dtype=torch.long, device=self.device)
        self.reward = torch.zeros(num_envs, device=self.device)
        self.successes = torch.zeros(num_envs, device=self.device)

        # Ch. 8 — per-environment success tolerance.
        self.current_tolerance = torch.full(
            (num_envs,), 0.01, device=self.device
        )

        # Ch. 6.2 / 6.3 — best-so-far distances.
        self.best_fingertip_distance = torch.full(
            (num_envs, 5), float("inf"), device=self.device
        )
        self.best_keypoint_distance = torch.full(
            (num_envs,), float("inf"), device=self.device
        )

    def compute_reward(
        self,
        *,
        lift: torch.Tensor,
        fingertip_distance: torch.Tensor,
        keypoint_distance: torch.Tensor,
        action: torch.Tensor,
        success: torch.Tensor,
    ) -> torch.Tensor:
        """
        Ch. 6 — compose dense shaping terms and goal reinforcement.
        """
        fingertip_progress, self.best_fingertip_distance = (
            reward_utils.progress_reward(
                fingertip_distance,
                self.best_fingertip_distance,
                scale=1.0,
            )
        )

        keypoint_progress, self.best_keypoint_distance = (
            reward_utils.progress_reward(
                keypoint_distance,
                self.best_keypoint_distance,
                scale=1.0,
            )
        )

        self.reward = reward_utils.total_reward(
            lift=lift,
            fingertip=fingertip_progress.sum(dim=-1),
            keypoint=keypoint_progress,
            action=action,
            success=success,
            lift_scale=1.0,
            fingertip_scale=1.0,
            keypoint_scale=1.0,
            action_scale=0.01,
            goal_scale=10.0,
        )
        return self.reward

    def compute_done(
        self,
        *,
        fallen: torch.Tensor,
        hand_far: torch.Tensor,
        max_successes_reached: torch.Tensor,
        max_episode_length: int,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """
        Ch. 7 — separate termination from time-limit truncation.
        """
        terminated = termination_utils.termination_mask(
            fallen=fallen,
            hand_far=hand_far,
            max_successes_reached=max_successes_reached,
        )
        truncated = termination_utils.truncation_mask(
            self.episode_length,
            max_episode_length,
        )
        return terminated, truncated

    def curriculum_step(
        self,
        increment: float,
        target: float,
        upper: float,
    ) -> None:
        """
        Ch. 8 — tighten the success tolerance over training.
        """
        self.current_tolerance = termination_utils.update_tolerance(
            self.current_tolerance,
            increment=increment,
            target=target,
            upper=upper,
        )

    def observation_dimension(self, policy_fields, critic_fields) -> tuple[int, int]:
        """
        Ch. 4 / Ch. 15 — actor and privileged critic dimensions.
        """
        return (
            obs_utils.compute_obs_dim(policy_fields),
            obs_utils.compute_obs_dim(critic_fields),
        )

    def reset(self) -> None:
        self.episode_length.zero_()
        self.reward.zero_()
        self.best_fingertip_distance.fill_(float("inf"))
        self.best_keypoint_distance.fill_(float("inf"))
