"""
import ray
from ray.rllib.utils import check_env
import environment_ray


check_env(environment_ray.BugPlus()) # checks the custom environment for errors
"""
