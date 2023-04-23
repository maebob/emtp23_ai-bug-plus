"""
This function checks custom gymnasium environments for errors.
Load changed environments as env and run script.
"""
import ray
from ray.rllib.utils import check_env
import env_action_clipping as env   # name of the environment file;
                                    # change if you want to check an environment for errors
                                    # or if you want to find out whether it is still compatible with the current gymnasium version


check_env(env.BugPlus()) # checks the custom environment for errors

