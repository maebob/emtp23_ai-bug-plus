"""
This file contains the script to run the PPO agent within the environment with sparse rewards.
"""
from ray.air.integrations.wandb import WandbLoggerCallback
import ray.rllib.algorithms.dqn
import ray.rllib.algorithms.ppo
import pandas as pd
import ray
from ray import tune


import sys
import os
from dotenv import load_dotenv


# load the .env file
load_dotenv()
# append the absolute_project_path from .env variable to the sys.path
sys.path.append(os.environ.get('absolute_project_path'))
from src.environment.env_sparse_rewards import BugPlus


# clear the terminal
os.system('clear')
ray.init()


tune.run("PPO", 
        config={"env": BugPlus, 
            "seed": 42069,
            "framework": "torch",
            "num_workers": 2, 
            "num_gpus": 0,
            "num_envs_per_worker": 10,
            # "num_cpus_per_worker": 1,
        }, 
         local_dir="result_data/",
         callbacks=[
             WandbLoggerCallback(
                 api_key=os.environ.get('WANDB_API_KEY'),
                 project="BugsPlus",
                 group="PPO_all_edges_all_configs_4_edges_sparse_rewards",
                 job_type="train",
                 entity="bugplus",
             ),
],
    verbose=0,
    checkpoint_freq=10,
    checkpoint_at_end=True,
    keep_checkpoints_num=5,
    stop = {
    "episode_reward_mean": 99.8,},
    # resume=True
)