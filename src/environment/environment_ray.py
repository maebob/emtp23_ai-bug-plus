from gymnasium import Env, spaces
import numpy as np
import pandas as pd
import sys
import torch
import os
from dotenv import load_dotenv

# load the .env file
load_dotenv()
# append the absolute_project_path from .env variable to the sys.path
sys.path.append(os.environ.get('absolute_project_path'))
from src.engine.eval import main as eval_engine
from src.utils.valid_matrix import is_valid_matrix
from src.translation.matrix_to_json import main as matrix_to_json


def load_config():
    config_name = 'configs_4x+4y'
    config = f"{config_name}.csv"
    df = pd.read_csv(config, sep=';')
    index = np.random.randint(0, len(df))
    vector = np.array(df.iloc[index])
    return vector


class BugPlus(Env):
    def __init__(self, render_mode=None):
        '''Initialize the environment.'''

        # Number of possible bugs
        self.no_bugs = 3

        # Observation and action space of the environment
        self.observation_space = spaces.MultiBinary(
            (((2 + self.no_bugs) * (1 + 2 * self.no_bugs)) * 2))
        self.action_space = spaces.Discrete(
            (((2 + self.no_bugs) * (1 + 2 * self.no_bugs)) * 2))
        # = spaces.MultiBinary(70) for 3 bugs

        # create array with zeroes
        self.state = np.zeros((((2 + self.no_bugs) * (1 + 2 * self.no_bugs)) * 2))

        # Flag to indicate if the episode is done
        self.done = False

        # Episode return
        self.ep_return = 0

        # Input and expected output of the bug
        self.input_up = None
        self.input_down = None
        self.expected_output = None

    def reset(self, *, seed=None, options=None):
        '''Reset the environment to its original state.'''
        self.observation_space = spaces.MultiBinary(
            (((2 + self.no_bugs) * (1 + 2 * self.no_bugs)) * 2))
        # self.action_space = spaces.Discrete(
        #     (((2 + self.no_bugs) * (1 + 2 * self.no_bugs)) * 2))
        self.done = False
        self.ep_return = 0
        vector = load_config()
        self.setInputAndOutputValuesFromVector(vector)
        self.setVectorAsObservationSpace(vector) # returns self.state now
        return self.state, {} # self.observation_space -> self.state geändert nach Ende des Calls

    def step(self, action: torch):
        """
        #TODO: rewrite documentation
        Perform an action on the environment and reward/punish said action.
        Each action corresponds to a specific edge between two bugs being added to either
        the control flow matrix or the data flow matrix.

        Arguments:
            action {int} -- The action to be performed on the environment.
        Returns:
            reward {int} -- The reward for the performed action.
            observation {Env.space} -- The new state of the environment. # TODO: check for correct type
            ep_return {int} -- The return of the episode.
            done {bool} -- Flag to indicate if the episode is done.
        """
        self.state[action] = 1  # TODO: later: think about flipping the value
        reward, done = self.checkBugValidity()
        truncated = True
        return self.state, reward, done, truncated, {'ep_return': self.ep_return} # geändert nach Call: self.observation_space -> self.state

    def checkBugValidity(self):
        """
        Check if the bug is valid, i.e. if it is a valid control flow graph and data flow graph.

        Returns:
            reward {int} -- The reward for the performed action.
            done {bool} -- Flag to indicate if the episode is done.
        """

        # Translate the matrix representation to a JSON representation
        split_index = int(len(self.state) / 2)
        matrix_as_json = matrix_to_json(
            control_matrix=self.state[:split_index].reshape(2 * self.no_bugs + 1, self.no_bugs + 2),    # controlflow shape (2n+1, n+2)
            data_matrix = self.state[split_index:].reshape(self.no_bugs + 2, 2 * self.no_bugs + 1),     # dataflow shape: (n+2, 2n+1)v
            data_up=self.input_up, data_down=self.input_down)

        # # Check if the bug is valid, i.e. if it adheres to the rules of the BugPlus language #TODO: put as extra function
        # if is_valid_matrix(self.observation_space[0]) == False:
        #     reward = torch.tensor([-100]), True
        #     return reward

        # Run the bug through the engine and check if it produces the correct output
        try:
            result = eval_engine(matrix_as_json)
        except TimeoutError:
            # The engine timed out, the bug is invalid likely a loop
            # reward = torch.tensor([-10])
            reward = -10
            done = True

            return reward, done
        except:
            # If the bug is not valid, the engine will throw an error
            # something in the control flow is not connected (but not a loop), execution cannot terminate
            # reward = torch.tensor([-1])
            reward = -1
            done = True  # TODO: think about in the future; EIGENTLICH hier auch nicht done, weil er es noch retten könnte
            return reward, done

        if result.get("0_Out") == self.expected_output:
            # If the result is correct, the reward is 100
            # reward = torch.tensor([100])
            reward = 100
            done = True
            return reward, done

        # Engine evaluated but result was not correct
        # reward = torch.tensor([-1])
        reward = -1
        done = False
        return reward, done

    def setVectorAsObservationSpace(self, vector): #TODO: rename
        '''
        TODO: write documentation
        '''
        self.state = vector[3:]

    def setInputAndOutputValuesFromVector(self, vector):
        '''Set the input and output values of the environment.'''
        self.input_up = vector[0]
        self.input_down = vector[1]
        self.expected_output = vector[2]
