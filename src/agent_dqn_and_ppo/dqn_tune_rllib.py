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
from src.environment.environment_ray import BugPlus
from src.utils.determine_number_of_bugs import number_bugs, array_to_matrices

import ray
from ray import tune
import ray.rllib.algorithms.ppo
import ray.rllib.algorithms.dqn

ray.init()

tune.run("DQN",
         config = {"env": BugPlus
         })