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


import ray
from ray import tune
import ray.rllib.algorithms.ppo
import ray.rllib.algorithms.dqn

# clear the terminal
os.system('clear')
ray.init()

tune.run("DQN",
         config = {"env": BugPlus
         })