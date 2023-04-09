
import ray
from ray.rllib.utils import check_env
import env_action_clipping as env


check_env(env.BugPlus()) # checks the custom environment for errors

