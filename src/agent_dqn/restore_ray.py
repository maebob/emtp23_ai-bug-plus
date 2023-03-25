# from ray.tune.integration.wandb import WandbLoggerCallback
from ray.air.integrations.wandb import WandbLoggerCallback
from ray.tune.stopper import CombinedStopper, ExperimentPlateauStopper, MaximumIterationStopper
import ray.rllib.algorithms.dqn
from ray.rllib.agents import ppo
import pandas as pd
import ray
from ray import tune
from ray.tune.registry import register_env

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

#checkpoint path 
checkpoint_path = "/home/aaron/BugPlusEngine/result_data/PPO/PPO_BugPlus_5319c_00000_0_2023-03-10_22-48-42/checkpoint_000317"

# Define the environment you're using
def env_creator(env_config):
    return BugPlus(env_config)

register_env("my_env", env_creator)


# Define the configuration for Tune
config = {
    "env": "my_env",
    "seed": 42069,
    "framework": "torch",
    "num_workers": 20,
    "num_gpus": 0,
    "num_envs_per_worker": 10,
    "num_cpus_per_worker": 1,
    "evaluation_num_workers": 10,
    "callbacks": WandbLoggerCallback(
        api_key=os.environ.get('WANDB_API_KEY'),
        project="BugsPlus",
        group="PPO_3_edges_all_configs",
        job_type="train",
        entity="bugplus",
    ),
    "checkpoint_path": checkpoint_path,  # Load the checkpoint
}

# Create a PPOTrainer and restore the checkpoint
trainer = ppo.PPOTrainer(config=config)
trainer.restore(checkpoint_path)

# Train the agent for additional iterations
for i in range(300):
    result = trainer.train()
    print(result)

    # Checkpoint the agent every 50 iterations
    if i % 50 == 0:
        checkpoint = trainer.save()
        print("Checkpoint saved at", checkpoint)
# Warning message from run:
# Current log_level is WARN.
# For more information, set 'log_level': 'INFO' / 'DEBUG' or use the -v and -vv flags.