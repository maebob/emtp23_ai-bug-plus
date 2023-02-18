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

# Create data frame out of configs.csv
df = pd.read_csv("configs_4x+4y.csv", sep=";")

# Create a numpy vector out of a random line in the data frame
vector = np.array(df.iloc[np.random.randint(0, len(df))])
# print("vector: ", vector)
# test_vector = np.array(
#     [3, 5, 32,
#     0, 0, 0, 0, 0, 0, 0,
#     0, 0, 0, 0, 0, 0, 1,
#     1, 0, 0, 0, 0, 0, 0,
#     0, 0, 1, 0, 0, 0, 0,
#     0, 0, 0, 0, 1, 0, 0,

#     0, 0, 0, 0, 1,
#     1, 0, 0, 0, 0,
#     0, 1, 0, 0, 0,
#     0, 0, 1, 0, 0,
#     0, 0, 1, 0, 0,
#     0, 0, 0, 1, 0,
#     0, 0, 0, 1, 0])
    # [3, 5, 4,

    # 0, 0, 0, 0, 0, 0, 0, 
    # 0, 0, 0, 0, 0, 0, 1, 
    # 1, 0, 0, 0, 0, 0, 0, 
    # 0, 1, 0, 0, 0, 0, 0, 
    # 0, 0, 0, 0, 1, 0, 0, 

    # 0, 0, 0, 0, 1, 
    # 0, 0, 0, 0, 0, 
    # 0, 0, 0, 0, 0, 
    # 0, 0, 1, 0, 0, 
    # 0, 0, 0, 0, 0, 
    # 0, 0, 0, 1, 0, 
    # 1, 0, 0, 0, 1,

    # 8])
# vector = test_vector[:73]

print('line 55, vector:\n', vector)

"""
# Reshape the vector to the control flow and data flow matrices
print("****************")
controlflow = vector[3:38].reshape(5,7)
dataflow = vector[38:73].reshape(7,5)
print(controlflow)
print("\n",dataflow)
# missing controlflow (1,6)
# print(vector.shape) # shape is (73,), i.e. no solution appended atm
"""

# Initialize the environment with the vector
env = environment.BugPlus()
env.setVectorAsObservationSpace(vector)
env.setInputAndOutputValuesFromVector(vector) # TODO: change input for learner;  returns NONE atm
print("env.setInputAndOutputValuesFromVector(vector)", env.setInputAndOutputValuesFromVector(vector))



# set up matplotlib
is_ipython = 'inline' in matplotlib.get_backend()
if is_ipython:
    from IPython import display

plt.ion()

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
# GAMMA is the discount factor as mentioned in the previous section
# EPS_START is the starting value of epsilon
# EPS_END is the final value of epsilon
# EPS_DECAY controls the rate of exponential decay of epsilon, higher means a slower decay
# TAU is the update rate of the target network
# LR is the learning rate of the AdamW optimizer
# BATCH_SIZE = 128
BATCH_SIZE = 128
GAMMA = 0.99
EPS_START = 0.9
EPS_END = 0.5
EPS_DECAY = 10000 #controls the rate of exponential decay of epsilon, higher means a slower decay
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


episode_durations = []


def plot_durations(show_result=False):
    plt.figure(1)
    durations_t = torch.tensor(episode_durations, dtype=torch.float)
    if show_result:
        plt.title('Result')
    else:
        plt.clf()
        plt.title('Training...')
    plt.xlabel('Episode')
    plt.ylabel('Duration')
    plt.plot(durations_t.numpy())
    # Take 100 episode averages and plot them too
    if len(durations_t) >= 100:
        means = durations_t.unfold(0, 100, 1).mean(1).view(-1)
        means = torch.cat((torch.zeros(99), means))
        plt.plot(means.numpy())

    plt.pause(0.001)  # pause a bit so that plots are updated
    if is_ipython:
        if not show_result:
            display.display(plt.gcf())
            display.clear_output(wait=True)
        else:
            display.display(plt.gcf())

def optimize_model():
    if len(memory) < BATCH_SIZE:
        return
    transitions = memory.sample(BATCH_SIZE)
    # Transpose the batch (see https://stackoverflow.com/a/19343/3343043 for
    # detailed explanation). This converts batch-array of Transitions
    # to Transition of batch-arrays.
    batch = Transition(*zip(*transitions))
    #print("l. 208  batch:\n", batch)

    # Compute a mask of non-final states and concatenate the batch elements
    # (a final state would've been the one after which simulation ended)
    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                          batch.next_state)), device=device, dtype=torch.bool)

    non_final_next_states = torch.cat([s for s in batch.next_state
                                                if s is not None])
    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    #print("l. 219 batch.reward\n", batch.reward)
    reward_batch = torch.cat(batch.reward)
   # print("reward_batch: ", reward_batch)

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
    num_episodes = 400

print('******************************')
dataflow = vector[3:38].reshape (5,7)
print('dataflow:\n', dataflow)
print('needed positions: 13 (/6), 14, 23, 32\n')
controlflow = vector[38:73].reshape (7,5)
print('dataflow:\n', controlflow)
print('needed positions: 39, 40, 46, 52, 57, 63, 68\n')
print('******************************')


t = 0
count_positive_rewards = 0 # counts how often the reward was positive
count_neg_1 = 0
count_neg_10 = 0
count_neg_100 = 0
sum_rewards = 0 # sum of all rewards
number_of_vectors = 1

# count how often which action was chosen:
action_count = [0] * 70
j = 0

for i_episode in range(num_episodes):
    # print("Episode: ", i_episode)
    #print("\nvector:\n", vector)
    env.reset()
    # vector = test_vector[:73]
    env.setVectorAsObservationSpace(vector)
    env.setInputAndOutputValuesFromVector(vector) 
    
    observation_space = env.observation_space # from documentation (https://www.gymlibrary.dev/api/core/#gym.Env.reset) returns observation space
    state = np.concatenate((observation_space[0].flatten(),observation_space[1].flatten()), axis=0) # flattened matrices concatenated into one array
    # n_observations = state.size ändert sich ja nicht (eigentlich..)
    # print ('l.329: observation_space before action:\n', observation_space)

    state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)

    # The index in the observation space that should be updated

    action = select_action(state)
    action_count[action] += 1


    #print("action: ", action)
    reward, observation, ep_return, done, _ = env.step(action.item())
    #print("reward: ", reward)
    observation_flat = np.concatenate((observation[0].flatten(),observation[1].flatten()), axis=0)

    next_state = torch.tensor(observation_flat, dtype=torch.float32, device=device).unsqueeze(0)
    sum_rewards += reward
    # print('Episode: ', i_episode, '    Action:', action, '    Reward:', reward)
    #print ('l.345: observation_space after action:\n', observation_space, '\n')





    if done:
        vector = np.array(df.iloc[np.random.randint(0, len(df))])
        # vector = test_vector[:73]
        number_of_vectors += 1
        
    if reward > 0:
        count_positive_rewards += 1
        print('positive reward in Episode: ', i_episode, '    Action:', action, '    Reward:', reward)
    if reward == -1:
        count_neg_1 += 1
    if reward == -10:
        count_neg_10 += 1
    if reward == -100:
        count_neg_100 += 1
        # dataflow = vector[3:38].reshape (5,7)
        # #print('dataflow:\n', dataflow)
        # controlflow = vector[38:73].reshape (7,5)
        # #print('dataflow:\n', controlflow)
        # #print('******************************')
    #     # next_state = None
        

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

    # if done:
    #     episode_durations.append(t + 1)
    #     plot_durations()
    #     break

print('Complete')
print("count_positive_rewards: ", count_positive_rewards)
print("count -1 rewards: ", count_neg_1)
print("count -10 rewards: ", count_neg_10)
print("count -100 rewards: ", count_neg_100)
print("sum of rewards: ", sum_rewards)
print("number of vectors: ", number_of_vectors)
for i in range(70):
    print("action ", i, " was chosen ", action_count[i], " times")
# plot_durations(show_result=True)
# plt.ioff()
# plt.show()

