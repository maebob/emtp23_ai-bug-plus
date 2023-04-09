from gymnasium import Env, spaces
import numpy as np
import pandas as pd
import sys
import torch
import os
from dotenv import load_dotenv
from copy import deepcopy

# load the .env file
load_dotenv()
# append the absolute_project_path from .env variable to the sys.path
sys.path.append(os.environ.get('absolute_project_path'))
from src.engine.eval import main as eval_engine
from src.utils.valid_matrix import is_valid_matrix
from src.translation.matrix_to_json import main as matrix_to_json



def load_config() -> np.array:
    """
    Load a random configuration from the csv file.
    """
    df = pd.read_csv("configs_4x+4y.csv", sep=';') # TODO: check if this works for everyone
    index = np.random.randint(0, len(df))
    vector = np.array(df.iloc[index])
    return vector


class BugPlus(Env):
    def __init__(self, render_mode=None):
        """
        Initialize the environment.
        """

        # Number of possible bugs
        self.n_bugs = 3

        self.observation_space = spaces.Dict(
            {
            "matrix": spaces.MultiBinary((((2 + self.n_bugs) * (1 + 2 * self.n_bugs)) * 2)),
            "sample_input": spaces.MultiDiscrete( 
                np.array([1,2]), dtype=np.int64),
            "sample_output": spaces.Box(
                low = np.NINF,
                high = np.inf,
                shape = (1,),
                dtype = np.int64),
            "error_info": spaces.MultiBinary((((2 + self.n_bugs) * (1 + 2 * self.n_bugs)) * 2))
            })
        # Action space of the environment
        self.action_space = spaces.Discrete(((2 + self.n_bugs) * (1 + 2 * self.n_bugs)) * 2)
        
        # State of the environment; initially array of zeros
        self.state = np.zeros((((2 + self.n_bugs) * (1 + 2 * self.n_bugs)) * 2))

        # Flag to indicate if the episode is done
        self.done = False

        # Episode return
        self.ep_return = 0


    def reset(self, *, seed=None, options=None):
        """
        Resets the environment to the initial state given by the vector.
        """ 
        vector = load_config() # load config
        self.state ={
            "matrix": self.set_vector_as_state(vector),
            "sample_input": self.set_vector_as_input(vector),
            "sample_output": self.set_vector_as_output(vector)
            }
        self.done = False
        self.ep_return = 0
        return self.state, {}
    

    def step(self, action: int):
        """
        Perform an action on the environment and reward/punish said action.
        Each action corresponds to a specific edge between two bugs being added to either
        the control flow matrix or the data flow matrix.

        Arguments:
            action {int} -- The action to be performed on the environment.
        Returns:
            state {dict} -- The new state of the environment. 
            reward {int} -- The reward for the performed action.
            done {bool} -- Flag to indicate if the episode is done.
            truncated {bool} -- Flag to indicate if the episode was truncated.
            info {dict} -- Additional information about the episode:
            ep_return {int} -- The return of the episode.
        """
        #TODO: discuss if we need a step counter?

        update_matrix = deepcopy(self.state["matrix"])
        update_matrix[action] = 1 # if matrix[action] == 0 else 0 # TODO for later: think about flipping the value (code copied from previous project)

        self.state = {
            "matrix": update_matrix,
            "sample_input": self.state["sample_input"],
            "sample_output": self.state["sample_output"]
        }
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
        input_pair = self.state["sample_input"] # get input pair from state
        matrix_as_json = matrix_to_json(
            control_matrix=self.state[:split_index].reshape(2 * self.n_bugs + 1, self.n_bugs + 2),    # controlflow shape (2n+1, n+2)
            data_matrix = self.state[split_index:].reshape(self.n_bugs + 2, 2 * self.n_bugs + 1),     # dataflow shape: (n+2, 2n+1)v
            data_up = input_pair[0],
            data_down = input_pair[1])

        # # Check if the bug is valid, i.e. if it adheres to the rules of the BugPlus language 
        # #TODO (Aaron/engine): put as extra function (is this still a todo or can we delete/ignore this step with the updated evaluation process of the engine?)
        # if is_valid_matrix(self.observation_space[0]) == False:
        #     reward = -100, True
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
        """
        Set the state of the environment using the vector representation.
        """
        vector[3:]  #TODO: muss das returnen, wenn wir nicht mehr direkt self.state setzen?

    def set_vector_as_input(self, vector):
        """
        Set the input and output values of the environment.
        """
        np.array(vector[0], vector[1]) #TODO: type: list or array?

    def set_vector_as_output(self, vector):
        """
        Set the output value of the environment.
        """
        vector[2] #TODO


