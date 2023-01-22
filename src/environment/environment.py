from gym import Env, spaces
import numpy as np
import sys
sys.path.append('/Users/mayte/github/bugplusengine') # Mayte
# sys.path.append('C:/Users/D073576/Documents/GitHub/BugPlusEngine/') # Mae
# sys.path.append('/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/') # Aaron
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
        '''Reset the environment to its original state.'''
        self.observation_space = np.array([np.zeros(((2 + self.no_bugs), (1 + 2 * self.no_bugs)), dtype=int), np.zeros(((1 + 2 * self.no_bugs), (2 + self.no_bugs)), dtype=int) ], dtype=object)
        self.done = False
        self.ep_return = 0

        return self.observation_space

    def step(self, action):
        '''Perform an action on the environment and reward/punish said action.
        Each action corresponds to a specific edge between two bugs being added to either
        the control flow matrix or the data flow matrix.'''
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
        self.observation_space[flow_matrix][edge_from][edge_to] = 1

        # Inrement the episode return
        self.ep_return += 1

        # Check if the board contains valid bugs only and set the reward accordingly
        reward = 1 if self.checkBugValidity() else -1

        # Close the episode if the board contains a valid bug
        self.done = True if reward == 1 else False


        return reward, self.observation_space, self.ep_return, self.done, {}

    def checkBugValidity(self):
        '''Check if the bug is valid, i.e. if it is a valid control flow graph and data flow graph.'''
        # Translate the matrix representation to a JSON representation
        matrix_as_json = matrix_to_json(control_matrix=self.observation_space[0], data_matrix=self.observation_space[1], data_up=self.input_up, data_down=self.input_down)
        
        # TODO:Check if the bug is valid, i.e. if it adheres to the rules of the BugPlus language

        # Run the bug through the engine and check if it produces the correct output
        try:
            result = eval_engine(matrix_as_json)
        except:
            return False
        if result.get("0_Out") == self.expected_output:
            return True
        return False

    def initializeStartingBoardSetup(self, bugs):
        '''Set the starting state of the environment in order to have control over the
         complexity of the problem class.'''
        self.observation_space = bugs

    def initializeInputValues(self, up, down):
        '''Set the input values the bug bpard is supposed to process in order to have control over the
         complexity of the problem class.'''
        self.input_Up = up
        self.input_Down = down

    def initializeExpectedOutput(self, expected_out):
        '''Set the expected output of the bug board in order to check wether the created board
        evaluates correctly.'''
        self.expected_output = expected_out

    def createStartingBoardSetup(self):
        '''Create an incrementor with on edge removed'''
        # Create the control flow matrix
        control_matrix = np.zeros((5, 7), dtype=int)
        control_matrix[0][5] = control_matrix[1][6] = control_matrix[2][0] = control_matrix[3][1] = control_matrix[4][4]  = 1

        # Create the data flow matrix
        data_matrix = np.zeros((7, 5), dtype=int)
        data_matrix[0][4] = data_matrix[3][2] = data_matrix[5][3] = data_matrix[6][0] = 1

        # Delete random 1 from either the control flow or data flow matrix
        if np.random.randint(0, 2) == 1:
            control_matrix[np.random.randint(0, 5)][np.random.randint(0, 7)] = 0
        else:
            data_matrix[np.random.randint(0, 7)][np.random.randint(0, 5)] = 0
        
    def setVectorAsObservationSpace(self, vector):
        '''Change format of the input vector to the format the environment expects and intialize the observation space with the result.

        Vector format: [input_up, input_down, expected_output, control_matrix, data_matrix]
        Target format: [[control_matrix], [data_matrix]]'''

        # Remove the input and expected output from the vector
        vector = np.delete(vector, [0, 1, 2])

        # Split the vector into the control and data flow matrix
        control_matrix = vector[:(int)(vector.size/2)].reshape(2 + self.no_bugs, 1 + 2 * self.no_bugs)
        data_matrix = vector[(int)(vector.size/2):].reshape(1 + 2 * self.no_bugs, 2 + self.no_bugs)

        self.observation_space = np.array([control_matrix, data_matrix], dtype=object)

    def setInputAndOutputValuesFromVector(self, vector):
        '''Set the input and output values of the environment.'''

        self.input_up = vector[0]
        self.input_down = vector[1]
        self.expected_output = vector[2]
        
        
        