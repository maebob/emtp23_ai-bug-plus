
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

from src.translation.matrix_to_json import main as matrix_to_json
from src.engine.eval_aus_error_translation import main as eval_engine
from src.utils.translate_action import translate_action # translate actions into the format of a transposed matrix
from src.utils.error_to_clipping import translate_to_range # translate the error into a range for clipping

SPACE_SIZE = 1_000
INDEX = 0


# load config file and do some simple preprocessing
config_path = os.environ.get('config_path')
df = pd.read_csv(config_path, sep=";", header=None)
df = df.dropna(axis=0, how='all') # drop empty rows
DF = df.sample(frac=1, random_state=42069).reset_index() # shuffle rows, keep index

wrong_counter = 0
episode_counter = 0

def load_config(load_new: bool = False):
    """
    This function loads a random configuration from the config file. If load_new is set to True, a new random configuration is loaded.
    Otherwise, the last loaded configuration is returned.

    Arugments:
        load_new {bool} -- If True, a new random configuration is loaded. Otherwise, the last loaded configuration is returned. (default: {False})
    Returns:
        vector {np.array} -- The vector containing the configuration.
    """
    if load_new:
        global INDEX
        INDEX = np.random.randint(0, len(DF))
    
    vector = np.array(DF.iloc[INDEX][1:]) # get the vector without the index from the configs in the DF
    return vector


class BugPlus(Env):
    def __init__(self, render_mode=None):
        '''Initialize the environment.'''
        # Number of possible bugs
        self.no_bugs = 3

        # Observation and action space of the environment
        self.observation_space = spaces.Dict({
            "matrix": spaces.MultiBinary(
            (((2 + self.no_bugs) * (1 + 2 * self.no_bugs)) * 2)),
            "up": spaces.Discrete(SPACE_SIZE),
            "down": spaces.Discrete(SPACE_SIZE),
            "output": spaces.Discrete(10 * SPACE_SIZE),
            })
        
        self.action_space = spaces.Box(low=0, high=70, shape=(1,), dtype=np.int32)
        
        self.state = {
            "matrix": np.zeros(
            (((2 + self.no_bugs) * (1 + 2 * self.no_bugs)) * 2)),
            "up": 0,
            "down": 0,
            "output": 0,
        }


        # Flag to indicate if the episode is done
        self.done = False
        # Episode return
        self.ep_return = 0
        self.load_new_config = True
        self.epsiode_length = 0

    def reset(self, *, seed=None, options=None):
        '''Reset the environment to its original state.'''      
        self.done = False
        self.ep_return = 0
        vector = load_config(self.load_new_config)
        self.set_input_output_state(vector)
        self.set_matrix_state(vector)
        self.epsiode_length = 0
        #restrict action space before returning the state
        # clip = find_action_space(self) # find range for clipping
        # self.action_space = spaces.Box(low=clip[0], high=clip[1], shape=(1,), dtype=np.int32) # restricting the action space

        return self.state, {} # TODO: return action_space here?

    def step(self, action_original: torch):
        """
        Perform an action on the environment and reward/punish said action.
        Each action corresponds to a specific edge between two bugs being added to either
        the control flow matrix or the data flow matrix.
        Arguments:
            action {int} -- The action to be performed on the environment.
        Returns:
            state{dict} -- The new state of the environment.
            reward {int} -- The reward for the performed action.
            done {bool} -- Flag to indicate if the episode is done.
            truncated {bool} -- Flag to indicate if the episode was truncated.
            info {dict}
                ep_return {int} -- The return of the episode.
        """
        self.epsiode_length += 1
        # if maximum episode length is reached, end the episode
        if self.epsiode_length > 15:
            self.done = True
            truncated = True
            return self.state, -1, self.done, truncated, {'ep_return': self.ep_return}
        
        print("\n", self.action_space, "\naction before action clipping:", action_original)
        # enforce action clipping:
        if action_original not in self.action_space:           
            if action_original < self.action_space.low: # if action chosen by agent is too low, use minimum action in action space
                action_original = self.action_space.low
            else:
                action_original = self.action_space.high # if action chosen by agent is too high, use maximum action in action space
        
        # translate action to the position corresponding in the transposed matrix
        action = translate_action(self.no_bugs, action_original) # translate action to the position corresponding in transposed matrix
        print("action after clipping:", action_original, "translated action:", action, "\n", self.state.get("matrix"), "\n")


        if self.state.get("matrix")[action] == 1:
            # The action was already performed, punish the agent
            reward = -0.2
            done = False
            truncated = False
            return self.state, reward, done, truncated, {'ep_return': self.ep_return}
        
        self.state["matrix"][action] = 1
        reward, done = self.check_bug_validity()
        if done:
            truncated = True
        else:
            truncated = False

        if reward <= 0 and done:
            self.load_new_config = False
        elif reward > 0 and done:
            self.load_new_config = True

        # restrict action space for next step
        clip = find_action_space(self) # find range for clipping
        self.action_space = spaces.Box(low=clip[0], high=clip[1], shape=(1,), dtype=np.int32) # restricting the action space
        
        #TODO: think about if this could be done at the beginning of each step instead
        # if this is only then used to change the action

        return self.state, reward, done, truncated, {'ep_return': self.ep_return}

    def check_bug_validity(self):
        """
        Check if the bug is valid, i.e. if it is a valid control flow graph and data flow graph.
        Returns:
            reward {int} -- The reward for the performed action.
            done {bool} -- Flag to indicate if the episode is done.
        """
        # Translate the matrix representation to a JSON representation
        matrix = deepcopy(self.state.get("matrix"))
        split_index = int(len(matrix) / 2)

        control_matrix = matrix[:split_index].reshape(self.no_bugs + 2, 2 * self.no_bugs + 1)
        data_matrix = matrix[split_index:].reshape(2 * self.no_bugs + 1, self.no_bugs + 2)
       

        matrix_as_json = matrix_to_json(
            control_matrix=control_matrix,    # controlflow shape (2n+1, n+2)
            data_matrix=data_matrix,     # dataflow shape: (n+2, 2n+1)v
            data_up=self.state.get("up"), data_down=self.state.get("down"))
        
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
            reward = -0.1
            done = False          
            return reward, done
        if result.get("0_Out") == self.state.get("output"):
            # If the result is correct, the reward is 100
            reward = 100
            done = True
            return reward, done
        # Engine evaluated but result was not correct
        reward = -0.1
        done = False
        return reward, done

    def set_matrix_state(self, vector):
        '''Set matrix state of the environment as given by the vector (position 3 onwards).'''
        self.state["matrix"] = vector[3:]
 
    def set_input_output_state(self, vector):
        '''Set the input and output values of the environment.'''
        self.state["up"] = vector[0]
        self.state["down"] = vector[1]
        self.state["output"] = vector[2]


def find_action_space(self) -> np.array:
    """ Given the current state, restrict the action space for the agent.
    Missing edges are determined by the engine's evalutation of the current state..
    Possible caught errors that trigger a restriction of the action space are:
        - missing edges in the control flow
        - missing edges in the data flow (for bugs 1 to no_bugs)
    All other errors are handled elsewhere and do promt a change in the action space.
    Returns:
        np.array -- The range of positions to which the action space should be clipped to.
        First element is inclusive, second element is not inclusive. (see example above).  
    """
    range_for_clipping = [0, 2 * (self.no_bugs + 2) * (2 * self.no_bugs + 1)] # default is full action space
    # get current state and evaluate the matrix; catch errors and turn this into clipped state
    matrix = deepcopy(self.state.get("matrix"))
    split_index = int(len(matrix) / 2)

    control_matrix = matrix[:split_index].reshape(self.no_bugs + 2, 2 * self.no_bugs + 1)
    data_matrix = matrix[split_index:].reshape(2 * self.no_bugs + 1, self.no_bugs + 2)
    

    matrix_as_json = matrix_to_json(
        control_matrix=control_matrix,    # controlflow shape (2n+1, n+2)
        data_matrix=data_matrix,     # dataflow shape: (n+2, 2n+1)
        data_up=self.state.get("up"), data_down=self.state.get("down"))
    try:
        result = eval_engine(matrix_as_json)
    except TimeoutError:
        range_for_clipping = range_for_clipping # for time out error, the action space is not clipped, the step function takes care of it (e.g. by ending the episode)

    except ValueError as e:
        # If the bug is not valid, the engine will throw an error
        # something in the control flow is not connected (but not a loop), execution cannot terminate
        # The engine feedback is translated and fed into the current state of the environment
        e = dict(e.args[0])
        error = {'port': e['fromPort'],
                    'bug': e['fromBug']}
        try:
            range_for_clipping = translate_to_range(error, self.no_bugs)
        except:
             # any other errors: return full action space
            range_for_clipping = range_for_clipping # use default
    except: # catch everythin else?
        range_for_clipping = range_for_clipping
        wrong_counter += 1
        print('something else went wrong: ', wrong_counter)
    return range_for_clipping