
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
from src.engine.eval import main as eval_engine
from src.utils.translate_action import translate_action # translate actions into the format of a transposed matrix
from src.utils.error_to_clipping import translate_to_range # translate the error into a range for clipping

SPACE_SIZE = 1_000
INDEX = 0

# Create Train- and Test-Data


# load config file and do some simple preprocessing
config_path = os.environ.get('config_path')
df = pd.read_csv(config_path, sep=";", header=None)
# add a column with index to train data
df = df.rename_axis('index1').reset_index()


#>Use this part for training:
####################################################
# Split into train and test data
train_data = df.sample(frac=0.9, random_state=42069)
test_data = df.drop(train_data.index)
# write test data to file
train_data.to_csv("/Users/mayte/GitHub/BugPlusEngine/src/train_data/train_all_edges_5_10_4edges.csv", sep=";", header=None, index=False)
test_data.to_csv("/Users/mayte/GitHub/BugPlusEngine/src/train_data/test_all_edges_5_10_4edges.csv", sep=";", header=None, index=False)
# add a column with index to train data
DF = train_data
####################################################
#<

#> Use this part for testing:
###################################################
# load test as df; change in .env file!
# DF = df(frac=1, random_state=42069).reset_index() # shuffle rows, keep index
# counter = 0
####################################################
#<



def load_config(load_new: bool = False):
    """
    This function loads a random configuration from the config file. If load_new is set to True, a new random configuration is loaded.
    Otherwise, the last loaded configuration is returned.

    Arugments:
        load_new {bool} -- If True, a new random configuration is loaded. Otherwise, the last loaded configuration is returned. (default: {False})
    Returns:
        vector {np.array} -- The vector containing the configuration.
    """
    #### TRAINING
    if load_new:
        global INDEX
        INDEX = np.random.randint(0, len(DF))        
    
    ###### TESTING
    # counter =+ 1
    # INDEX = counter % len(DF)

    config_for_vector = np.array(DF.iloc[INDEX])
    vector = config_for_vector[1:]
    # define global varibles for logging:
    global LOG_INDEX, CONFIG
    LOG_INDEX = config_for_vector[0]
    CONFIG = config_for_vector[1:]

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
        '''
        Reset the environment to its original state.
        '''      
        self.done = False
        self.ep_return = 0
        vector = load_config(True) # changed
        self.set_input_output_state(vector)
        self.set_matrix_state(vector)
        self.epsiode_length = 0

        return self.state, {}

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
        reward_action_clipping = 0
        self.epsiode_length += 1
        # if maximum episode length is reached, end the episode
        if self.epsiode_length > 15:
            self.done = True
            truncated = True
            reward = -1
            loop_string = str(LOG_INDEX) + ";" + str(reward) + ";"+str(CONFIG)+"\n"
            f = open("/Users/mayte/GitHub/BugPlusEngine/result_logging/test_log.csv", "a")
            f.write(loop_string)
            f.close()
            
            return self.state, reward, self.done, truncated, {'ep_return': self.ep_return}
        
        # enforce action clipping:
        clip_from, clip_to, control_or_data_matrix, next_action = find_action_space(self) # find range for clipping
        if action_original in range(clip_from, clip_to): # selected action is within the suggested range by the engine's feedback
            reward_action_clipping = 0.1    # reward the agent for choosing an action within the range
                                            # makes reward 0 if agent picks a position where there previously was no edge and which does not lead to a loop
        else: # action is outside the clipped range
            if control_or_data_matrix == 0: # error is in controlflow matrix:
                action_original = next_action 
            else: # error is in dataflow matrix:      
                if action_original < clip_from: # if action chosen by agent is too low, use minimum action in action space
                    action_original = clip_from
                else:
                    action_original = clip_to - 1  # this would be the default case when using gymnasium.wrapper.ClipActionWrapper
                                                # if action chosen by agent is too high, use maximum action in action space
            
        # translate action to the position corresponding in the transposed matrix
        action = translate_action(self.no_bugs, action_original) # translate action to the position corresponding in transposed matrix



        if self.state.get("matrix")[action] == 1:
            # The action was already performed, punish the agent
            reward = -0.2
            self.done = False
            truncated = False
            reward = reward + reward_action_clipping # add reward for choosing an action within the the clipped range (+0.1), otherwise additional reward is 0
            return self.state, reward, self.done, truncated, {'ep_return': self.ep_return}
        
        self.state["matrix"][action] = 1
        reward, self.done = self.check_bug_validity()
        if self.done:
            truncated = True
        else:
            truncated = False

        if reward <= 0 and self.done:
            error_string = str(LOG_INDEX) + ";" + str(reward) + ";"+str(CONFIG)+"\n"
            f = open("/Users/mayte/GitHub/BugPlusEngine/result_logging/test_log.csv", "a")
            f.write(error_string)
            f.close()
            self.load_new_config = True #changed;  #TODO: check what happens there!
        elif reward > 0 and self.done:
            self.load_new_config = True
        reward = reward + reward_action_clipping # add reward for choosing an action within the the clipped range (+0.1), otherwise additional reward is 0
        return self.state, reward, self.done, truncated, {'ep_return': self.ep_return}

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


def find_action_space(self) -> int and int:
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
    range_min = 0 # default is full action space
    range_max = 2 * (self.no_bugs + 2) * (2 * self.no_bugs + 1)
    control_or_data_matrix = None # dummy values which could be returned if no error is caught
    next_action = None # dummy values which could be returned if no error is caught

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
        # for time out error, the action space is not clipped, the step function takes care of it (e.g. by ending the episode)
        return range_min, range_max, None, None
    except ValueError as e:
        # If the bug is not valid, the engine will throw an error
        # something in the control flow is not connected (but not a loop), execution cannot terminate
        # The engine feedback is translated and fed into the current state of the environment
        e = dict(e.args[0])
        error = {'port': e['fromPort'],
                    'bug': e['fromBug']}
        try:
            range_min, range_max, control_or_data_matrix, next_action = translate_to_range(error, self.no_bugs)
        except:
            # any other errors: return full action space
            return range_min, range_max, None
    except: # catch everythin else?
        # any other errors: return full action space
        return range_min, range_max, None, None
    return range_min, range_max, control_or_data_matrix, next_action