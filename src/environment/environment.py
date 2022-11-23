from gym import Env, spaces
import numpy as np

class BugPlus(Env):
    def __init__(self):
        super(BugPlus, self).__init__()

        # Number of possible bugs
        self.no_bugs = 3

        self.observation_space = np.array([np.zeros(((2 + self.no_bugs), (1 + 2 * self.no_bugs)), dtype=int), np.zeros(((1 + 2 * self.no_bugs), (2 + self.no_bugs)), dtype=int) ])
        self.action_space = spaces.Discrete((((2 + self.no_bugs) * (1 + 2 * self.no_bugs)) * 2),)

        self.done = False

    def reset(self):
        self.observation_space = np.array([np.zeros(((2 + self.no_bugs), (1 + 2 * self.no_bugs)), dtype=int), np.zeros(((1 + 2 * self.no_bugs), (2 + self.no_bugs)), dtype=int) ])
        self.done = False
        self.ep_return = 0

    def step(self, action):
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

    # Create predefined environment state
    def updateBugs(self, bugs):
        '''Set the starting state of the environment in order to have control over the
         complexity of the problem class.'''
        self.observation_space = bugs

    def checkBugValidity(self):
        '''Check if the bug is valid, i.e. if it is a valid control flow graph and data flow graph.'''
        # TODO: Tranlate matrix representation to JSON representation, use eval function of engine to check validity

        return False