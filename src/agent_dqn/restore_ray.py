import numpy as np
from ray.air.integrations.wandb import WandbLoggerCallback
from ray.rllib.agents import ppo
import ray
from ray import tune

import sys
import os
from dotenv import load_dotenv

# load the .env file
load_dotenv()
# append the absolute_project_path from .env variable to the sys.path
sys.path.append(os.environ.get('absolute_project_path'))

from src.environment.env_complex_observation import BugPlus
# clear the terminal
os.system('clear')
ray.init()

difficulty = 0

checkpoint_path = "/result_data_coriculumn/PPO/PPO_BugPlus_d7dfb_00000_0_2023-03-25_18-02-36"  # Replace with your actual checkpoint path

trainer = ppo.PPOTrainer(config={"env": BugPlus, 
                                  "seed": 42069,
                                  "framework": "torch",
                                  "num_workers": 20,  # TODO: anpassen
                                  "num_gpus": 0,
                                  "num_envs_per_worker": 10,
                                  "num_cpus_per_worker": 1,
                                  })

trainer.restore(checkpoint_path)
target_mean_reward = 97.1
mean_reward = None

while mean_reward is None or mean_reward < target_mean_reward:
    result = trainer.train()
    mean_reward = result['episode_reward_mean']
    print(f"Iteration: {result['training_iteration']}, Mean Reward: {mean_reward}")

    if result['training_iteration'] % 50 == 0:
        checkpoint = trainer.save()
        print(f"Checkpoint saved at {checkpoint}")
