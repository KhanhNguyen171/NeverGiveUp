"""
Success and termination logic.

Chapter mapping:
- Ch. 7: Success and termination
- Ch. 8: Success-tolerance curriculum
"""

from __future__ import annotations

import torch


def update_tolerance(
    current: torch.Tensor,
    increment: float,
    target: float,
    upper: float,
) -> torch.Tensor:
    """
    Ch. 8.1 — gradually tighten the success criterion.

    tau_{k+1} = clamp(tau_k + Δtau, tau_target, tau_initial)
    """
    return torch.clamp(current + increment, min=target, max=upper)


def success_from_keypoints(
    max_keypoint_distance: torch.Tensor,
    tolerance: torch.Tensor | float,
) -> torch.Tensor:
    # Ch. 7.1 — success is defined geometrically from object/goal keypoints.
    return max_keypoint_distance <= tolerance


def termination_mask(
    *,
    fallen: torch.Tensor,
    hand_far: torch.Tensor,
    max_successes_reached: torch.Tensor,
) -> torch.Tensor:
    # Ch. 7.2 — early episode termination.
    return fallen | hand_far | max_successes_reached


def truncation_mask(
    episode_length: torch.Tensor,
    max_episode_length: int,
) -> torch.Tensor:
    # Ch. 7.2 — time-limit truncation is distinct from failure termination.
    return episode_length >= max_episode_length
