import sys
sys.path.append('C:/Users/D073576/Documents/GitHub/BugPlusEngine/') # Mae

import src.environment.env_complex_observation_engine_feedback as env
import src.utils.error_to_action as error_to_action
from src.translation.matrix_to_json import main as matrix_to_json
import pandas as pd
import numpy as np

# Import configs from csv
configs = pd.read_csv('C:/Users/D073576/Documents/GitHub/BugPlusEngine/configs_4x+4y_data_control.csv', header=None)

# Create environment
env = env.BugPlus()

# Initialzie environment with random config
env.reset()

env.step(39)
env.step(13)