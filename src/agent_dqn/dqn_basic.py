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


from src.environment import environment_tensor as environment

from src.utils.matrix import number_bugs, array_to_matrices

#TODO: implement method to apply the strategies
# choose between two modi:
# config_strategy = 'priority' # 'random' or 'priority'
# problem_solving_strategy = 'reload' # 'reload' or 'new'
#TODO MD: priority_new


# Create data frame out of configs.csv
config_name = '/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/configs_4x+4y'
config = f"{config_name}.csv"
df_full = pd.read_csv(config, sep=";")
df  = df_full[:]

# set up a way to select the configurations which have been solved the least

# count how often a specific configuration was solved successfully:
config_count = [0] * len(df) # intialize with 0, meaning, a configuration that has not been used yet gets a count of 0

# give values to each configuration, based on how often it was solved successfully / how long it took to be solved:
config_priority = [-1] * len(df) # intialize with -1, meaning, a configuration that has not been used yet gets a count of -1

# keep track when a configuration was first loaded:
config_first_loaded = [-1] * len(df)

# keep track when a configuration was first solved:
config_first_solved = [-1] * len(df)

# keep track which action solved the problem:
config_solution = [-1] * len(df)


EPS_CONFIGS = 0.3 # probability to choose a random configuration

def select_config(index):
    """
    selects index of the configuration dataframe with the lowest count
    """
    old_index = index
    #index = np.random.randint(0, len(config_priority))

    sample = random.random()
    if sample > EPS_CONFIGS:
        index = config_priority.index(min(config_priority))
        if index == old_index: # if same index is chosen, choose a random one
            index = np.random.randint(0, len(config_priority)) 
    else:
        index = np.random.randint(0, len(config_priority))
    return index


# Create a numpy vector out of any config in the data frame
index = 0
config_first_loaded[index] = 0 # first configuration is always loaded first
vector = np.array(df.iloc[index]) # first vector is initialized with any of the configuration (in order to set up the environment)

# set seed
torch.manual_seed(42)

# Initialize the environment with the vector
env = environment.BugPlus()
env.setVectorAsObservationSpace(vector)
env.setInputAndOutputValuesFromVector(vector) # TODO: change input for learner;  returns NONE atm; OR: ignore and delete this line? (also subsequent occurences)


# if gpu is to be used
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))


class ReplayMemory(object):

    def __init__(self, capacity):
        self.memory = deque([],maxlen=capacity)

    def push(self, *args):
       #Save a transition
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

class DQN(nn.Module):

    def __init__(self, n_observations, n_actions):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(n_observations, 128)
        self.layer2 = nn.Linear(128, 128)
        self.layer3 = nn.Linear(128, n_actions)

    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).
    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return self.layer3(x)

# BATCH_SIZE is the number of transitions sampled from the replay buffer
# GAMMA is the discount factor
# EPS_START is the starting value of epsilon
# EPS_END is the final value of epsilon
# EPS_DECAY controls the rate of exponential decay of epsilon, higher means a slower decay
# TAU is the update rate of the target network
# LR is the learning rate of the AdamW optimizer
BATCH_SIZE = 128
GAMMA = 0.99
EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 1000
TAU = 0.005
LR = 1e-4

# Get number of actions from gym action space
n_actions = env.action_space.n

observation_space = env.observation_space # from documentation (https://www.gymlibrary.dev/api/core/#gym.Env.reset) returns observation space
state = np.concatenate((observation_space[0].flatten(),observation_space[1].flatten()), axis=0) # flattened matrices concatenated into one array
n_observations = state.size



policy_net = DQN(n_observations, n_actions).to(device)
target_net = DQN(n_observations, n_actions).to(device)
target_net.load_state_dict(policy_net.state_dict())

optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)
memory = ReplayMemory(10000)


steps_done = 0


def select_action(state):
    global steps_done
    sample = random.random()
    eps_threshold = EPS_END + (EPS_START - EPS_END) * \
        math.exp(-1. * steps_done / EPS_DECAY)
    steps_done += 1
    if sample > eps_threshold:
        with torch.no_grad():
            # t.max(1) will return largest column value of each row.
            # second column on max result is index of where max element was
            # found, so we pick action with the larger expected reward.
            return policy_net(state).max(1)[1].view(1, 1)
    else:
        return torch.tensor([[env.action_space.sample()]], device=device, dtype=torch.long)



def optimize_model():
    if len(memory) < BATCH_SIZE:
        return
    transitions = memory.sample(BATCH_SIZE)
    # Transpose the batch (see https://stackoverflow.com/a/19343/3343043 for
    # detailed explanation). This converts batch-array of Transitions
    # to Transition of batch-arrays.
    batch = Transition(*zip(*transitions))

    # Compute a mask of non-final states and concatenate the batch elements
    # (a final state would've been the one after which simulation ended)
    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                          batch.next_state)), device=device, dtype=torch.bool)

    non_final_next_states = torch.cat([s for s in batch.next_state
                                                if s is not None])
    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)


    # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
    # columns of actions taken. These are the actions which would've been taken
    # for each batch state according to policy_net
    state_action_values = policy_net(state_batch).gather(1, action_batch)

    # Compute V(s_{t+1}) for all next states.
    # Expected values of actions for non_final_next_states are computed based
    # on the "older" target_net; selecting their best reward with max(1)[0].
    # This is merged based on the mask, such that we'll have either the expected
    # state value or 0 in case the state was final.
    next_state_values = torch.zeros(BATCH_SIZE, device=device)
    with torch.no_grad():
        next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0]
    # Compute the expected Q values
    expected_state_action_values = (next_state_values * GAMMA) + reward_batch

    # Compute Huber loss
    criterion = nn.SmoothL1Loss()
    loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

    # Optimize the model
    optimizer.zero_grad()
    loss.backward()
    # In-place gradient clipping
    torch.nn.utils.clip_grad_value_(policy_net.parameters(), 100)
    optimizer.step()




if torch.cuda.is_available():
    num_episodes = 600
else:
    num_episodes = 5
 




count_positive_rewards = 0 # counts how often the reward was positive
count_pos_epsisodes = 0 # counts how often the reward was positive within 1,000 episodes
sum_rewards = 0 # sum of all rewards
number_of_vectors = 1
proportion_old = 0

# count how often which action was chosen:
# action_count = [0] * 70
# j = 0


# in order to visualize the leaning process, we set up the following lists:
x = [] # number of episodes
y1 = [] # total number of solved problems
y2 = [] # proportion of solved problems at each time point
y3 = [] # proportion of solved problems within the last 5,000 episodes
y4 = [] # compare if the learner improves in comparison to previous 5,000 episodes

for i_episode in range(num_episodes):

    # if i_episode == 0:
    #     index = 0
    #     old_index = 0
    #     vector = np.array(df.iloc[index])

    env.reset()
    env.setVectorAsObservationSpace(vector)
    env.setInputAndOutputValuesFromVector(vector) 
    
    observation_space = env.observation_space # from documentation (https://www.gymlibrary.dev/api/core/#gym.Env.reset) returns observation space
    state = np.concatenate((observation_space[0].flatten(),observation_space[1].flatten()), axis=0) # flattened matrices concatenated into one array


    state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)

    # The index in the observation space that should be updated
    action = select_action(state)
    # action_count[action] += 1



    reward, observation, ep_return, done, _ = env.step(action.item())
    observation_flat = np.concatenate((observation[0].flatten(),observation[1].flatten()), axis=0)

    next_state = torch.tensor(observation_flat, dtype=torch.float32, device=device).unsqueeze(0)
    sum_rewards += reward
    config_count[index] += 1 # each time a configuration is used the count is increased by 1
        
    if reward > 0:
        count_positive_rewards += 1
        count_pos_epsisodes += 1
        config_priority[index] += 1 # each time a configuration is solved successfully, the count is increased by 1
        config_solution[index] = action.item() # action that solved the configuration is stored as integer
        number_of_vectors += 1
        """
        this loads new problems only when the current problem is solved successfully
        """
        # index = select_config(index) # select new configuration by first  finding index of lowest count
        # vector = np.array(df.iloc[index]) # set new vector with freshly selected configuration 


        if config_first_solved[index] == -1: # write episode of first successful solution
            config_first_solved[index] = i_episode

        if config_first_loaded[index] == -1: # write episode of first loading of configuration
            config_first_loaded[index] = i_episode+1 # new problem is loaded in the next episode

    
    if reward <= 0:
        config_priority[index] -= 1 # each time a configuration is not solved successfully, the count of the action that solved it is decreased by 1 to make it more likely to be picked again

    """
    This loads a new problem every episode
    """
    index = select_config(index) # select new configuration by first  finding index of lowest count
    vector = np.array(df.iloc[index]) # set new vector with freshly selected configuration 


    if (i_episode > 0) & (i_episode % 5000 == 0):
        print(i_episode, 'Episodes done', number_of_vectors, 'vectors done')

        proportion_new = count_pos_epsisodes / 50  # = count_pos_episodes / 5000 * 100
        x.append(i_episode/1000)
        y1.append(count_positive_rewards)
        y2.append(100 * count_positive_rewards / i_episode)
        y3.append(proportion_new)
        y4.append(proportion_new - proportion_old)

        # resetting and updating the counters for the last 5,000 episodes
        count_pos_epsisodes = 0
        proportion_old = proportion_new


    # Store the transition in memory
    memory.push(state, action, next_state, reward)

    # Move to the next state
    state = next_state

    # Perform one step of the optimization (on the policy network)
    optimize_model() 


    # Soft update of the target network's weights
    # θ′ ← τ θ + (1 −τ )θ′
    target_net_state_dict = target_net.state_dict()
    policy_net_state_dict = policy_net.state_dict()
    for key in policy_net_state_dict:
        target_net_state_dict[key] = policy_net_state_dict[key]*TAU + target_net_state_dict[key]*(1-TAU)
    target_net.load_state_dict(target_net_state_dict)


print('Complete after ', num_episodes, ' episodes')
print("count_positive_rewards: ", count_positive_rewards)
print("sum of rewards: ", sum_rewards)
print("proportion of correct steps: ", count_positive_rewards/num_episodes*100, "%")


# creating dataframe with information about the configs for analysis
config_summary = []
config_summary.append(config_count)
config_summary.append(config_priority)
config_summary.append(config_first_loaded)
config_summary.append(config_first_solved)
config_summary.append(config_solution)
# ugly workaround: configs to list, then add, then convert the whole new list to df
configs_list = df.values.tolist()
config_summary.append(configs_list)


df_config_summary = pd.DataFrame(config_summary).transpose()
df_config_summary.columns=['count', 'priority', 'first_loaded', 'first_solved', 'solution', 'original_config']

# saving the data in a csv file
file_name = f"summary_{config_name}_{num_episodes}_priority_new.csv"
df_config_summary.to_csv(file_name, sep =';')


# plotting the learning rate of DQN learner in two subplots:
fig, ax = plt.subplots(2, 2)


# plotting the absolute number of correctly solved configurations
ax[0][0].plot(x, y1)
ax[0][0].set_xlabel('number of episodes (in 1,000)', fontsize=8)
ax[0][0].set_ylabel('number of correctly solved problems', fontsize=8)


# plotting the proportion of correctly solved configurations
ax[0][1].plot(x, y2)
ax[0][1].set_xlabel('number of episodes (in 1,000)', fontsize=8)
ax[0][1].set_ylabel('proportion of correctly solved (in %)', fontsize=8)



# plotting the proportion of correctly solved configurations within the last 1,000 episodes
ax[1][0].plot(x, y3)
ax[1][0].set_xlabel('number of episodes (in 1000)', fontsize=6)
ax[1][0].set_ylabel('proportion correctly solved within 5,000 episodes (in %)', fontsize=8)

ax[1][1].plot(x, y4)
ax[1][1].set_xlabel('number of episodes (in 1,000)', fontsize=6)
ax[1][1].set_ylabel('trend in comparison to previous 5,000 episodes', fontsize=8)

fig.tight_layout(pad=3.0)
fig.suptitle('Learning progress of DQN learner', fontsize=16)
plot_name = f"plot_{config_name}_{num_episodes}_priority_new.png"
plt.savefig(plot_name)
plt.show()
