# from ray.tune.integration.wandb import WandbLoggerCallback
import numpy as np
from ray.air.integrations.wandb import WandbLoggerCallback
#from ray.tune.stopper import CombinedStopper, ExperimentPlateauStopper, MaximumIterationStopper
import ray.rllib.algorithms.dqn
import ray.rllib.algorithms.ppo
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

# TODO: test for hyperparameter tuning: config before tune.run with grid_search
# 'parameter_name': tune.grid_search([True, False])


difficulty = 0


tune.run("PPO", 
        config={"env": BugPlus, 
            "seed": 42069,
            "framework": "torch",
            "num_workers": 20, # TODO: anpassen
            "num_gpus": 0,
            "num_envs_per_worker": 10,
            "num_cpus_per_worker": 1,
            "lr": tune.grid_search([0.01, 0.001, 0.0001]), # Specify different learning rates
            "log_level": "DEBUG", # Set the log level to DEBUG
        },
         local_dir="/home/aaron/BugPlusEngine/checkpoint_test",
         verbose=1,
         checkpoint_freq=5,
         checkpoint_at_end=True,
         keep_checkpoints_num=5,
         stop={"episode_reward_mean": 97.1},
         #resume=True,
         )
# Warning message from run:
# Current log_level is WARN.
# For more information, set 'log_level': 'INFO' / 'DEBUG' or use the -v and -vv flags.
callbacks=[
             WandbLoggerCallback(
                 api_key=os.environ.get('WANDB_API_KEY'),
                 project="BugsPlus",
                 group="PPO_all_edges_all_configs_4_edges",
                 job_type="train",
                 entity="bugplus",
             )
         ]