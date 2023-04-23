"""
This file defines a custom environment for BugPlus.
It is based on environment.py and adapted to be used with a DQN agent (self-built version).
"""
from gym import Env, spaces
import numpy as np
import sys
import torch
import os
from dotenv import load_dotenv

# load the .env file
load_dotenv()
# append the absolute_project_path from .env variable to the sys.path
sys.path.append(os.environ.get('absolute_project_path'))

from src.translation.matrix_to_json import main as matrix_to_json
from src.engine.eval import main as eval_engine


class BugPlus(Env):
    def __init__(self):
        '''Initialize the environment.'''
        super(BugPlus, self).__init__()

        # Number of possible bugs
        self.no_bugs = 3 

        # Obersvation and action space of the environment
        self.observation_space = np.array([np.zeros(((2 + self.no_bugs), (1 + 2 * self.no_bugs)), dtype=int), np.zeros(((1 + 2 * self.no_bugs), (2 + self.no_bugs)), dtype=int) ], dtype=object)
        self.action_space = spaces.Discrete((((2 + self.no_bugs) * (1 + 2 * self.no_bugs)) * 2),)

        # Flag to indicate if the episode is done
        self.done = False

        # Episode return
        self.ep_return = 0

        # Input and expected output of the bug
        self.input_up = None
        self.input_down = None
        self.expected_output = None

    def reset(self):
        '''
        Reset the environment to its original state.
        '''
        self.observation_space = np.array([np.zeros(((2 + self.no_bugs), (1 + 2 * self.no_bugs)), dtype=int), np.zeros(((1 + 2 * self.no_bugs), (2 + self.no_bugs)), dtype=int) ], dtype=object)
        self.done = False
        self.ep_return = 0

        return self.observation_space

    def step(self, action: int):
        """
        Perform an action on the environment and reward/punish said action.
        Each action corresponds to a specific edge between two bugs being added to either
        the control flow matrix or the data flow matrix.

        Arguments:
            action {int} -- The action to be performed on the environment.
        Returns:
            reward {int} -- The reward for the performed action.
            observation {np.array} -- The new state of the environment.
            ep_return {int} -- The return of the episode.
            done {bool} -- Flag to indicate if the episode is done.
        """

        # Decide wether the new edge is added to the control flow or data flow matrix
        flow_matrix = 0 if action < (self.observation_space[0][0].size * self.observation_space[1][0].size) else 1
        
        # Calculate the position of the new edge based on the action
        # If the action is in the first half of all possible actions, the edge is added to the control flow matrix
        edge_from = 0
        edge_to = 0

        # Calculation of the edge indices
        if flow_matrix == 0:
            edge_from = action // self.observation_space[0][0].size
            edge_to = action % self.observation_space[0][0].size
        else:
            adjusted_action = action - (self.observation_space[0][0].size * self.observation_space[1][0].size)
            edge_from = adjusted_action // self.observation_space[1][0].size
            edge_to = adjusted_action % self.observation_space[1][0].size

        # Add the new edge to the corresponding matrix
        if self.observation_space[flow_matrix][edge_from][edge_to] == 1:
            done = True
            reward = torch.tensor([-100])
            self.ep_return += 1
            return reward, self.observation_space, self.ep_return, self.done, {}

        else:
            self.observation_space[flow_matrix][edge_from][edge_to] = 1 
        
        # Inrement the episode return
        self.ep_return += 1

        # Check if the board evalutes correctly, is an invalid configuation or is still incomplete
        # The amount of the reward is definded in the called function
        reward, done = self.check_bug_validity() 
        return reward, self.observation_space, self.ep_return, self.done, {}

    def check_bug_validity(self):
        """
        Check if the bug is valid, i.e. if it is a valid control flow graph and data flow graph.

        Returns:
            reward {int} -- The reward for the performed action.
            done {bool} -- Flag to indicate if the episode is done.
        """
        # Translate the matrix representation to a JSON representation
        matrix_as_json = matrix_to_json(control_matrix=self.observation_space[0], data_matrix=self.observation_space[1], data_up=self.input_up, data_down=self.input_down)

        # Run the bug through the engine and check if it produces the correct output
        try:
            result = eval_engine(matrix_as_json)
        except TimeoutError:
            # The engine timed out, the bug is invalid likely a loop
            reward = torch.tensor([-10])
            done = True

            return reward, done
        except:
            # If the bug is not valid, the engine will throw an error
            reward = torch.tensor([-10])
            done = True
            return reward, done
        
        if result.get("0_Out") == self.expected_output:
            # If the result is correct, the reward is 100
            reward = torch.tensor([100])
            done = True
            return reward, done
        
        # Engine evaluated but result was not correct
        reward = torch.tensor([-1])
        done = False
        return reward, done

    
    def initialize_starting_board_setup(self, bugs):
        '''
        Set the starting state of the environment in order to have control over the
        complexity of the problem class.
        '''
        self.observation_space = bugs

    def initialize_input_values(self, up, down):
        '''
        Set the input values the bug bpard is supposed to process in order to have control over the
        complexity of the problem class.
        '''
        self.input_Up = up
        self.input_Down = down

    def initialize_expected_output(self, expected_out):
        '''
        Set the expected output of the bug board in order to check wether the created board
        evaluates correctly.
        '''
        self.expected_output = expected_out


        
    def set_vector_as_observation_space(self, vector):
        '''
        Change format of the input vector to the format the environment expects and intialize the observation space with the result.

        Vector format: [input_up, input_down, expected_output, control_matrix, data_matrix]
        Target format: [[control_matrix], [data_matrix]]
        '''
        # Remove the input and expected output from the vector
        vector = np.delete(vector, [0, 1, 2])

        # Split the vector into the control and data flow matrix
        control_matrix = vector[:(int)(vector.size/2)].reshape(2 + self.no_bugs, 1 + 2 * self.no_bugs)
        data_matrix = vector[(int)(vector.size/2):].reshape(1 + 2 * self.no_bugs, 2 + self.no_bugs)

        self.observation_space = np.array([control_matrix, data_matrix], dtype=object)

    def set_input_and_output_values_from_vector(self, vector):
        '''
        Set the input and output values of the environment.
        '''
        self.input_up = vector[0]
        self.input_down = vector[1]
        self.expected_output = vector[2]
        
        
        