import ray
from ray.rllib.utils import check_env
import env_complex_observation

import sys
import os
from dotenv import load_dotenv

# load the .env file
load_dotenv()
# append the absolute_project_path from .env variable to the sys.path
sys.path.append(os.environ.get('absolute_project_path'))

check_env(env_complex_observation.BugPlus()) # checks the custom environment for errors
