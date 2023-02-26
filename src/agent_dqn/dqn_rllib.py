import gym
import math
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from collections import namedtuple, deque
from itertools import count

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F


import pandas as pd

import sys
import os
from dotenv import load_dotenv

# load the .env file
load_dotenv()
# append the absolute_project_path from .env variable to the sys.path
sys.path.append(os.environ.get('absolute_project_path'))
from src.environment import environment_ray as environment
from src.utils.matrix import number_bugs, array_to_matrices


import ray
from ray import tune
from ray.rllib.algorithms.dqn import DQNConfig


ray.init()
config = (  # 1. Configure the algorithm,
    DQNConfig()
    .environment(environment.BugPlus)
    .rollouts(num_rollout_workers=2)
    .framework("tf2")
    .training(model={"fcnet_hiddens": [64, 64]})
    .evaluation(evaluation_num_workers=1)
)

algo = config.build()  # 2. build the algorithm,

for _ in range(5):
    print(algo.train())  # 3. train it,

algo.evaluate()  # 4. and evaluate it.

