# from ray.tune.integration.wandb import WandbLoggerCallback
from ray.air.integrations.wandb import WandbLoggerCallback
from ray.tune.stopper import CombinedStopper, ExperimentPlateauStopper, MaximumIterationStopper
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
# from src.environment import environment_ray as environment


# clear the terminal
os.system('clear')
ray.init()

# implement erarly stopping based on the mean reward
stop = {
    "episode_reward_mean": 100,
    "timesteps_total": 100000,
}
# tune.stopper = CombinedStopper(
#     MaximumIterationStopper(max_iter=10),
#     ExperimentPlateauStopper(
#         metric="episode_reward_mean",
#         std=1.0,
#         top=100,
#         mode="max",
#         patience=10
#     )
# )

from src.environment.env_complex_observation import BugPlus

tune.run("PPO", 
         # test for hyperparameter tuning: config before tune.run with grid_search
         #  'parameter_name': tune.grid_search([True, False])
        config={"env": BugPlus, 
            "seed": 42069,
            "framework": "torch",
            "num_workers": 2, # TODO: anpassen
            "num_gpus": 0,
            "num_envs_per_worker": 1,
            "num_cpus_per_worker": 1,
        },
         local_dir="result_data/",
         callbacks=[
             WandbLoggerCallback(
                 api_key=os.environ.get('WANDB_API_KEY'),
                 project="BugsPlus",
                 group="ppo_remove_edge",
                 job_type="train",
                 entity="bugplus",
             ),
            #  wandb.log() # would need wandb.init() before in order to log code as well
],
    verbose=0,
    checkpoint_freq=10,
    checkpoint_at_end=True,
    keep_checkpoints_num=5,
)
# Current log_level is WARN.
# For more information, set 'log_level': 'INFO' / 'DEBUG' or use the -v and -vv flags.