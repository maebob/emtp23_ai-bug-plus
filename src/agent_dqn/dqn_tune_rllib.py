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
from src.environment.env_complex_observation import BugPlus


# clear the terminal
os.system('clear')
ray.init()


tune.run("DQN",
         config={"env": BugPlus,
                 "seed": 42069,
                 "framework": "torch",
                 "num_workers": 1,
                 "num_gpus": 0,
                 "num_envs_per_worker": 1,
                 "num_cpus_per_worker": 1,
                 },
         local_dir="result_data/",
         callbacks=[
             # adjust the entries here to conform to your wandb environment
             # cf. https://docs.wandb.ai/ and https://docs.ray.io/en/master/tune/examples/tune-wandb.html
             WandbLoggerCallback(
                 api_key=os.environ.get('WANDB_API_KEY'),
                 project="bugplus",
                 group="dqn",
                 job_type="train",
                 info={"env": "BugPlus", "seed": 42069, "algorithm": "DQN",
                       "config": os.environ.get('config_path')},
             ),
         ],
         verbose=0,
         )
