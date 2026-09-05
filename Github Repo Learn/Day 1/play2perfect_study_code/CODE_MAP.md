Kiến trúc khi map với readme.md học thuật của Day 1.


```
train.py
   │
   ▼
PlayEnv
   │
   ├── obs_utils
   │      └── Observation representation
   │
   ├── reward_utils
   │      └── Reward shaping
   │
   └── termination_utils
          └── Success / curriculum
   │
   ▼
PreciseAssemblyEnv
   │
   └── Assembly goals
   │
   ▼
PPO + SAPG
   │
   ▼
LSTM Actor-Critic
```