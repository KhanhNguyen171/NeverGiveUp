"""
Reward terms for Play2Perfect study.

Chapter mapping:
- Ch. 6: Reward design
- Ch. 6.1: Lifting reward
- Ch. 6.2: Fingertip distance progress
- Ch. 6.3: Keypoint progress
- Ch. 6.4: Action/motion penalty
- Ch. 6.5: Goal bonus
"""

from __future__ import annotations

import torch


def progress_reward(
    current_distance: torch.Tensor,
    best_distance: torch.Tensor,
    scale: float,
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Ch. 6.2 / 6.3 — best-so-far progress.

    Δd_t = d_best,t-1 - d_t
    """
    improvement = torch.clamp(best_distance - current_distance, min=0.0)
    new_best = torch.minimum(best_distance, current_distance)
    return scale * improvement, new_best


def lifting_reward(
    object_height: torch.Tensor,
    reference_height: torch.Tensor,
    scale: float,
) -> torch.Tensor:
    # Ch. 6.1 — encourage the object to leave its initial support region.
    return scale * torch.clamp(object_height - reference_height, min=0.0)


def action_penalty(action: torch.Tensor, scale: float) -> torch.Tensor:
    # Ch. 6.4 — regularize large control commands.
    return -scale * torch.sum(action.square(), dim=-1)


def goal_bonus(success: torch.Tensor, scale: float) -> torch.Tensor:
    # Ch. 6.5 — sparse terminal/goal reinforcement.
    return scale * success.float()


def total_reward(
    *,
    lift: torch.Tensor,
    fingertip: torch.Tensor,
    keypoint: torch.Tensor,
    action: torch.Tensor,
    success: torch.Tensor,
    lift_scale: float,
    fingertip_scale: float,
    keypoint_scale: float,
    action_scale: float,
    goal_scale: float,
) -> torch.Tensor:
    """
    Ch. 6 — reward decomposition.

    r_t =
        r_lift
        + r_fingertip
        + r_keypoint
        + r_goal
        + r_action
    """
    return (
        lift_scale * lift
        + fingertip_scale * fingertip
        + keypoint_scale * keypoint
        + goal_scale * success.float()
        - action_scale * torch.sum(action.square(), dim=-1)
    )
