# from ray.tune.integration.wandb import WandbLoggerCallback
import numpy as np
from ray.rllib.agents.callbacks import DefaultCallbacks
from src.environment.env_complex_observation import BugPlus
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


# clear the terminal
os.system('clear')
ray.init()

# TODO: test for hyperparameter tuning: config before tune.run with grid_search
# 'parameter_name': tune.grid_search([True, False])


difficulty = 0


class SetDifficulty(DefaultCallbacks):
    def on_episode_end(self, worker, base_env, policies, episode, **kwargs):
        super().on_episode_end(worker, base_env, policies, episode, **kwargs)
        episode_mean_reward = np.mean(
            episode.batch_builder.policy_batches['default_policy'].data['rewards'])
        for env in base_env.envs:
            if episode_mean_reward > 80:
                difficulty += 1
            env.set_difficulty(difficulty)


tune.run("PPO",
         config={"env": BugPlus,
                 "seed": 42069,
                 "framework": "torch",
                 "num_workers": 20,  # TODO: anpassen
                 "num_gpus": 0,
                 "num_envs_per_worker": 10,
                 "num_cpus_per_worker": 1,
                 "evaluation_num_workers": 10,
                 },
         local_dir="result_data/",
         callbacks=[
             WandbLoggerCallback(
                 api_key=os.environ.get('WANDB_API_KEY'),
                 project="BugsPlus",
                 group="PPO_3_edges_all_configs",
                 job_type="train",
                 entity="bugplus",
             ),
             SetDifficulty(),
         ],
         verbose=0,
         checkpoint_freq=50,
         checkpoint_at_end=True,
         keep_checkpoints_num=5,
         stop={"episode_reward_mean": 97.1},
         )
# Warning message from run:
# Current log_level is WARN.
# For more information, set 'log_level': 'INFO' / 'DEBUG' or use the -v and -vv flags.
