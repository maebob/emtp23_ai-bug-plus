"""
import ray
from ray.rllib.utils import check_env
import environment_ray
# print(type(environment_ray.BugPlus))
check_env(environment_ray.BugPlus())

"""
"""
ValueError: Env must be of one of the following supported types: BaseEnv, gymnasium.Env, gym.Env, MultiAgentEnv, VectorEnv, RemoteBaseEnv, ExternalMultiAgentEnv, ExternalEnv, but instead is of type <class 'list'>.
"""

