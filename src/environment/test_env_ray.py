import ray
from ray.rllib.utils import check_env
import environment_ray_functioning
check_env(environment_ray_functioning.BugPlus()) # checks the custom environment for errors
