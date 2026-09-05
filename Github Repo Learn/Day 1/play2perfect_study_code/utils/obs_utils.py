"""
Observation construction for the Play stage.

Chapter mapping:
- Ch. 4: Stage 1 — Play pretraining
- Ch. 4.2: Observation representation
- Ch. 4.3: Coordinate representation
- Ch. 4.4: Object keypoints
- Ch. 5: Observation noise and delay
"""

from __future__ import annotations

import math
import torch


NUM_JOINTS = 29
NUM_FINGERTIPS = 5
NUM_KEYPOINTS = 4

# Ch. 4.2 — observation fields used by the policy representation.
OBS_FIELD_SIZES = {
    "joint_pos": NUM_JOINTS,
    "joint_vel": NUM_JOINTS,
    "prev_action_targets": NUM_JOINTS,
    "palm_pos": 3,
    "palm_rot": 4,
    "palm_vel": 6,
    "object_rot": 4,
    "object_vel": 6,
    "fingertip_pos_rel_palm": 3 * NUM_FINGERTIPS,
    "keypoints_rel_palm": 3 * NUM_KEYPOINTS,
    "keypoints_rel_goal": 3 * NUM_KEYPOINTS,
    "object_scales": 3,
    "closest_keypoint_max_dist": 1,
    "closest_fingertip_dist": NUM_FINGERTIPS,
    "lifted_object": 1,
    "progress": 1,
    "successes": 1,
    "reward": 1,
}


def compute_obs_dim(fields) -> int:
    """Compute the flattened policy/state dimension."""
    return sum(OBS_FIELD_SIZES[name] for name in fields)


# Ch. 4.4 — object keypoint representation.
KEYPOINT_CORNERS = (
    (1, 1, 1),
    (1, 1, -1),
    (-1, -1, 1),
    (-1, -1, -1),
)


def quaternion_to_matrix(q: torch.Tensor) -> torch.Tensor:
    """Convert normalized quaternion q=(w,x,y,z) to rotation matrices."""
    q = torch.nn.functional.normalize(q, dim=-1)
    w, x, y, z = q.unbind(-1)

    return torch.stack(
        (
            1 - 2 * (y*y + z*z), 2 * (x*y - z*w),     2 * (x*z + y*w),
            2 * (x*y + z*w),     1 - 2 * (x*x + z*z), 2 * (y*z - x*w),
            2 * (x*z - y*w),     2 * (y*z + x*w),     1 - 2 * (x*x + y*y),
        ),
        dim=-1,
    ).reshape(q.shape[:-1] + (3, 3))


def keypoints_world(
    center_pos: torch.Tensor,
    center_rot_wxyz: torch.Tensor,
    offsets_local: torch.Tensor,
) -> torch.Tensor:
    """
    Ch. 4.4:
        k_world = p_world + R_world @ k_local
    """
    R = quaternion_to_matrix(center_rot_wxyz)
    rotated = torch.matmul(offsets_local, R.transpose(-1, -2))
    return center_pos.unsqueeze(-2) + rotated


def stack_observation_dict(obs: dict[str, torch.Tensor], fields) -> torch.Tensor:
    """Flatten fields in the exact configured order."""
    return torch.cat(
        [obs[name].reshape(obs[name].shape[0], -1) for name in fields],
        dim=-1,
    )


def add_object_pose_noise(
    position: torch.Tensor,
    rotation: torch.Tensor,
    position_std: float,
) -> tuple[torch.Tensor, torch.Tensor]:
    # Ch. 5.1 — observation-side domain randomization.
    noisy_position = position + torch.randn_like(position) * position_std
    return noisy_position, rotation


def build_observations(
    *,
    clean: dict[str, torch.Tensor],
    policy_fields,
    critic_fields,
    position_noise_std: float = 0.0,
) -> dict[str, torch.Tensor]:
    """
    Construct actor and critic tensors.

    Ch. 15 — asymmetric actor-critic:
    actor receives policy observations, while the critic may receive the
    privileged state representation.
    """
    policy_obs = dict(clean)

    if position_noise_std > 0.0 and "palm_pos" in policy_obs:
        policy_obs["palm_pos"] = (
            policy_obs["palm_pos"]
            + torch.randn_like(policy_obs["palm_pos"]) * position_noise_std
        )

    return {
        "policy": stack_observation_dict(policy_obs, policy_fields),
        "critic": stack_observation_dict(clean, critic_fields),
    }
