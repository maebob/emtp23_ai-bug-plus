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
    df = pd.read_csv("configs_4x+4y.csv", sep=';') # TODO: check if this works for everyone
    index = np.random.randint(0, len(df))
    vector = np.array(df.iloc[index])
    return vector


class BugPlus(Env):
    def __init__(self, render_mode=None):
        '''Initialize the environment.'''

        # Number of possible bugs
        self.no_bugs = 3
        # Observation and action space of the environment
        self.observation_space = spaces.Dict(
            {
            "matrix": spaces.MultiBinary((((2 + self.no_bugs) * (1 + 2 * self.no_bugs)) * 2)),
             "sample_input": spaces.MultiDiscrete( # TODO https://gymnasium.farama.org/api/spaces/fundamental/#multidiscrete
                    shape=([1,2]),
                    dtype=np.int64
                ),
                "sample_output": spaces.Discrete()
            })
        
        # discrete space from 0 to inf:
        # spaces.Box(np.array([0]), np.array([inf]),dtype = np.int64 ) 
        # source: https://stackoverflow.com/questions/55787460/openai-gym-box-space-configuration

        # Documentation Gymnasium Fundamental Spaces: https://gymnasium.farama.org/api/spaces/fundamental/

        # create array with zeroes
        self.state = np.zeros((((2 + self.no_bugs) * (1 + 2 * self.no_bugs)) * 2))

        # Flag to indicate if the episode is done
        self.done = False

        # Episode return
        self.ep_return = 0

        # TODO: reorganize; this should be now part of the observation space, right?
        # Input and expected output of the bug
        self.input_up = None # # TODO: do we need to change this? (see also the def of set_vector_as_input_output)
        self.input_down = None
        self.expected_output = None

    def reset(self, *, seed=None, options=None):
        '''Reset the environment to its original state.'''
        #TODO: adjust to all changes in init
        
        
        self.state = spaces.Dict( #TODO: change if necessary, i.e. if init is changed
            {
            "matrix": spaces.MultiBinary((((2 + self.n_bugs) * (1 + 2 * self.n_bugs)) * 2)),
             "sample_input": spaces.MultiDiscrete( 
                    shape=([1,2]),
                    dtype=np.int64
                ),
                "sample_output": spaces.Discrete()
            })

        self.done = False
        self.ep_return = 0
        vector = load_config()
        self.set_vector_as_input_output(vector)
        self.set_vector_as_state(vector) 
        return self.state, {}
    
        # example for resetting from previous project:
    # def reset(self) -> Dict[str, Any]:
    #     """
    #     Resets the environment and returns the reset state.
    #     :return:
    #     """

    #     self.done = False
    #     self.reward = 0
    #     self.info = dict()
    #     self.step_counter = 0

    #     row = self._sample_from_training_set()

    #     self.state = {
    #         "control_flow_matrix": row["modified_control_flow_matrix"].values[0],
    #         "sample_input_pairs": row["input_samples"].values[0],
    #         "sample_output_pairs": row["output_samples"].values[0]
    #     }

    #     return self.state

    def step(self, action: torch):
        """
        Perform an action on the environment and reward/punish said action.
        Each action corresponds to a specific edge between two bugs being added to either
        the control flow matrix or the data flow matrix.

        Arguments:
            action {int} -- The action to be performed on the environment.
        Returns:
            state {Env.space} -- The new state of the environment. # TODO: check for correct type
            reward {int} -- The reward for the performed action.
            done {bool} -- Flag to indicate if the episode is done.
            truncated {bool} -- Flag to indicate if the episode was truncated.
            info {dict} -- Additional information about the episode:
                ep_return {int} -- The return of the episode.
        """
        self.state[action] = 1  # TODO: later: think about flipping the value
        reward, done = self.checkBugValidity()
        truncated = True
        return self.state, reward, done, truncated, {'ep_return': self.ep_return}

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

        # # Check if the bug is valid, i.e. if it adheres to the rules of the BugPlus language 
        # #TODO: put as extra function (is this still a todo or can we delete/ignore this step with the updated evaluation process of the engine?)
        # if is_valid_matrix(self.observation_space[0]) == False:
        #     reward = torch.tensor([-100]), True
        #     return reward

        # Run the bug through the engine and check if it produces the correct output
        try:
            result = eval_engine(matrix_as_json)
        except TimeoutError:
            # The engine timed out, the bug is invalid likely a loop
            reward = -10
            done = True

            return reward, done
        except:
            # If the bug is not valid, the engine will throw an error
            # something in the control flow is not connected (but not a loop), execution cannot terminate
            reward = -1
            done = True  # TODO: think about in the future; EIGENTLICH hier auch nicht done, weil er es noch retten könnte
            return reward, done

        if result.get("0_Out") == self.expected_output:
            # If the result is correct, the reward is 100
            reward = 100
            done = True
            return reward, done

        # Engine evaluated but result was not correct
        reward = -1
        done = False
        return reward, done

    def set_vector_as_state(self, vector):
        '''
        Set the state of the environment using the vector representation.
        '''
        self.state = vector[3:]

    def set_vector_as_input_output(self, vector):   # TODO: do we need to change this? (see reset)
                                                    # input up-down together as one vector?
                                                    # also, check if we need to make this coherent with the gym space
                                                    # does the output need its own method if it does have its own space?
        '''
        Set the input and output values of the environment.
        '''
        self.input_up = vector[0]
        self.input_down = vector[1]
        self.expected_output = vector[2]
