# from ray.tune.integration.wandb import WandbLoggerCallback
from ray.air.integrations.wandb import WandbLoggerCallback
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
from src.environment.env_complex_observation import BugPlus 
# alternative environments:
# from src.environment.env_remove_edge import BugPlus # allows agent to remove edges
# from src.environment.env_empty_board import BugPlus # starts with empty board, independently from config file


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
            "num_cpus_per_worker": 1,
            # "evaluation_num_workers": 10,
        },
        #  local_dir="result_data_no_curriculum/", # choose the directory where the results are saved, otherwise the results are saved in a default directory
         callbacks=[
             WandbLoggerCallback(
                 api_key=os.environ.get('WANDB_API_KEY'),
                 project="BugsPlus",
                 group="PPO_all_edges_all_configs_4_edges", # choose name of the run according to the agent, the config file and the environment
                 job_type="train",
                 entity="bugplus",
             ),
],
    verbose=0,
    checkpoint_freq=50,
    checkpoint_at_end=True,
    keep_checkpoints_num=5,
    stop={"episode_reward_mean": 97},
)

