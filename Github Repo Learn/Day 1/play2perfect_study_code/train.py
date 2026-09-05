"""
Play2Perfect — study implementation of the training entry point.

Chapter mapping in the research .md:
- Ch. 17: Environment architecture
- Ch. 18: Training pipeline
- Ch. 19: Vectorized environment
- Ch. 20: Domain randomization
"""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    # Ch. 18.2 — Configuration flow:
    # CLI arguments select the task/agent; the actual environment and RL
    # configuration are loaded by the surrounding Isaac Lab / Hydra stack.
    parser = argparse.ArgumentParser("Play2Perfect training")
    parser.add_argument("--task", required=True)
    parser.add_argument("--agent", default="rl_games_cfg_entry_point")
    parser.add_argument("--checkpoint", default=None)
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--rl_device", default="cuda:0")
    parser.add_argument("--sim_device", default="cuda:0")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    # Ch. 17.1 — Isaac Lab DirectRLEnv is the simulation-side environment.
    #
    # Ch. 18.1 — The intended data path is:
    # Isaac Sim/Lab -> Gym environment -> RL-games wrapper -> PPO/SAPG runner.
    #
    # This study file deliberately keeps framework bootstrapping out of the
    # core learning logic. The real repository wires these components through
    # Hydra and rl_games.
    try:
        from isaaclab.app import AppLauncher
    except ImportError as exc:
        raise RuntimeError(
            "Isaac Lab is required to execute this entry point."
        ) from exc

    launcher = AppLauncher({"headless": args.headless})
    app = launcher.app

    try:
        import gymnasium as gym
        import isaacsimenvs  # noqa: F401
        from rl_games.torch_runner import Runner

        # Ch. 18.2 — task configuration is resolved before environment creation.
        env = gym.make(args.task)

        # Ch. 19 — the vectorized wrapper bridges Gym/Isaac Lab tensors to
        # rl_games and handles device/observation/action conventions.
        from isaaclab_rl import RlGamesVecEnvWrapper
        env = RlGamesVecEnvWrapper(
            env,
            rl_device=args.rl_device,
            clip_obs=float("inf"),
            clip_actions=float("inf"),
        )

        # Ch. 12–13 — PPO/SAPG is the optimization layer; this file does not
        # reimplement the optimizer.
        runner = Runner()
        # The concrete agent YAML is supplied by the repository configuration.
        # runner.load(agent_cfg)
        # runner.run({"train": not args.test, "play": args.test,
        #             "checkpoint": args.checkpoint})
        raise NotImplementedError(
            "Connect the repository's Hydra agent configuration here."
        )
    finally:
        del app


if __name__ == "__main__":
    main()
