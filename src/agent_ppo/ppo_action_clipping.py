"""
This file contains the script to run the PPO agent with the action restriction environment.
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
from src.environment.env_action_clipping import BugPlus


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
         local_dir="/Users/mayte/GitHub/BugPlusEngine/result_PPO_4_edges_action_clipping",
         callbacks=[
             WandbLoggerCallback(
                 api_key=os.environ.get('WANDB_API_KEY'),
                 project="BugsPlus",
                 group="logging_action_clipping",
                 job_type="train",
                 entity="bugplus",
             ),
],
    verbose=0,
    checkpoint_freq=10,
    checkpoint_at_end=True,
    keep_checkpoints_num=5,
    # stop = {
    # "episode_reward_mean": 40,},
    # resume=True
)
