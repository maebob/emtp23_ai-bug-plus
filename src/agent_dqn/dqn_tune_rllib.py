from ray.tune.integration.wandb import WandbLoggerCallback
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
tune.stopper.ExperimentPlateauStopper(
    metric="episode_reward_mean",
    std=1.0,
    top=100,
    mode="max",
    patience=10,
)
from src.environment.env_complex_observation import BugPlus

tune.run("DQN", 
        config={"env": BugPlus,
            "seed": 42069,
            "framework": "torch",
            "num_workers": 20, # TODO: anpassen! 2,
            "num_gpus": 0,
            "num_envs_per_worker": 1,
            "num_cpus_per_worker": 1,
        },
         local_dir="result_data/",
         callbacks=[
             WandbLoggerCallback(
                 api_key=os.environ.get('WANDB_API_KEY'),
                 project="BugsPlus",
                 group="dqn",
                 job_type="train",
                 entity="bugplus",
             ),
],
    verbose=0,
    checkpoint_freq=10,
    checkpoint_at_end=True,
    keep_checkpoints_num=5,
)
