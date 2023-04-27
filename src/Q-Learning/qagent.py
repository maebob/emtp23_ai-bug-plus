'''This file contains a Q-Learning agent that interacts with a simple BugPlus environment.
The agent is trained on a set of configurations and tries to learn to solve them, however it is restricted to one step per episode,
and thus can only be used to solve configurations missing one edge.'''

import numpy as np
import random
import gym
import pandas as pd
import sys
#sys.path.append('/Users/mayte/github/bugplusengine') # Mayte
sys.path.append('C:/Users/D073576/Documents/GitHub/BugPlusEngine/') # Mae
# sys.path.append('/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/') # Aaron
import src.environment.environment as env

import matplotlib
import matplotlib.pyplot as plt
import wandb

''' Current Expermient:
    - Goal try to learn to restore configs for 4x + 4y 
    - Agent is restricted to one step per episode
    - As long as the config has not been solved the agent will be trained on the same config
    - If the config has been solved the agent will be trained on a new randomly chosen config'''

def qLearningAgent():
    # Create variables needed to store information about the learning progress
    count_solved_problems = 0 # count the number of solved problems
    count_solved_problems_total = 0 # count the number of solved problems in total
    proportion_new = 0 # proportion of solved problems at current time point
    proportion_old = 0 # proportion of solved problems at preceeding time point

    no_episodes = [] # number of episodes
    tot_prblems_solved = [] # total number of solved problems
    prop_problems_solved = [] # proportion of solved problems at each time point
    prop_problems_solved_lastX = [] # proportion of solved problems within the last 5,000 episodes
    improvement_lastX = [] # compare if the learner improves in comparison to previous 5,000 episodes

    # Create environment to interact with
    environment = env.BugPlus()

    # Initialize Q-table
    observation_space = environment.observation_space # from documentation (https://www.gymlibrary.dev/api/core/#gym.Env.reset) returns observation space
    

    # Size of action space
    n_actions = environment.action_space.n

    # Set hyperparameters parameters
    learningRate = 0.8
    discountRate = 0.95
    epsilon = 1
    decayRate = 0.0005

    # Initialize training parameters
    numEpisodes = 100000
    maxSteps = 1

    # Import configurations from configs_4x+4y.csv to train on
    df = pd.read_csv("C:/Users/D073576/Documents/GitHub/BugPlusEngine/src/agent/configs_4x+4y.csv", sep=";")

    # Create vector that stores the difficulty of each configuration
    difficulty = np.zeros(len(df))

    # Create index for configurtation location in df and vector
    index = 0

    # Initialize Q-table
    Q = np.zeros((len(df), n_actions))
    state = np.random.randint(0, len(df))
    vector = chooseNewConfig(df, 2, difficulty)

    # Marker to check wether or not a configuration was solved
    config_solved = False

    # Train agent
    for episode in range(numEpisodes):
        # Reset environment and get first new observation
        environment.reset()

        vector, index = chooseNewConfig(df, 2, difficulty)
        environment.setVectorAsObservationSpace(vector)
        environment.setInputAndOutputValuesFromVector(vector)

        # Upodate state of the environment
        training_done = False
        
        # The Q-Table learning algorithm
        for step in range(maxSteps):
            # Pick an action based on epsilon-greedy policy
            if random.uniform(0, 1) < epsilon:
                action = environment.action_space.sample()
                print("Random action: " + str(action))
            else:
                # Select action with highest Q-value
                action = np.argmax(Q[state, :])
                print("Q-Table action: " + str(action))

            # Get new state and reward from environment
            step_reward, new_state, ep_return, done, list = environment.step(action)

            # Update Q-Table with new knowledge
            Q[state, action] = Q[state, action] + learningRate * (step_reward + discountRate * np.max(Q[state, :]) - Q[state, action])
            
            if done == True:
                config_solved = True
                updateDifficulty(difficulty, index, True)
                count_solved_problems += 1
                count_solved_problems_total += 1
            else:
                config_solved = False
                updateDifficulty(difficulty, index, False)

        # Reduce epsilon (because we need less and less exploration)
        epsilon = min(1, max(0, epsilon - decayRate))

        # Update the plotting information
        if (episode > 0) & (episode % 5000 == 0):
        
            proportion_new = count_solved_problems / 50  # = count_solved_problems / 5000 * 100
            no_episodes.append(episode/1000)
            tot_prblems_solved.append(count_solved_problems_total)
            prop_problems_solved.append(100 * count_solved_problems_total / episode)
            prop_problems_solved_lastX.append(proportion_new)
            improvement_lastX.append(proportion_new - proportion_old)

            # Reset and update the counters for the last 5,000 episodes
            count_solved_problems = 0
            proportion_old = proportion_new
    # Plot the results
    plotResults(no_episodes, tot_prblems_solved, prop_problems_solved, prop_problems_solved_lastX, improvement_lastX, 'Q-Learning_Progress_over_100,000_Episodes')

    # Test the agent on 100 random configurations from configs_4x+4y.csv
    testAgent(df, Q)

def testAgent(df, Q):
    # Test agent on 100 random configurations from configs_4x+4y.csv

    # Create environment to interact with
    environment = env.BugPlus()
    numCorrect = 0
    reward = 0

    state = np.random.randint(0, len(df))

    for i in range(100):
        environment.reset()
        environment.setVectorAsObservationSpace(np.array(df.iloc[state]))
        environment.setInputAndOutputValuesFromVector(np.array(df.iloc[state]))
        
        action = np.argmax(Q[state, :])
        step_reward, observation_space, ep_return, done, list = environment.step(action)
        reward += step_reward

        if step_reward == 50:
            numCorrect += 1
        
        # Prepare next random config
        state = np.random.randint(0, len(df))

    # Calculate average reward    
    avg_reward = reward / 100

    # Print number of correct guesses and average reward
    print("Agent picked the correct edge to add to the matrices " + str(numCorrect) + " times out of 100 tries.")
    print("The average reward gained by the agent was " + str(avg_reward) + ". \n")

    
def initialize(environment):
    environment.reset()
    # Create incrementor matrces with one edge removed
    control_flow = np.zeros((5, 7), dtype=int)
    data_flow = np.zeros((7, 5), dtype=int)

    # Missing edge in control flow matrix: [4][4] or 33
    control_flow[0][5] = control_flow[1][6] = control_flow[2][0] = control_flow[3][1]  = 1
    data_flow[0][4] = data_flow[3][2] = data_flow[5][3] = data_flow[6][0] = 1

    # Set the environment`s observation space
    environment.observation_space[0] = control_flow
    environment.observation_space[1] = data_flow

    # Set input and expected output
    environment.input_up = 4
    environment.input_down = 2
    environment.expected_output = 5

def plotResults(x, y1, y2, y3, y4, name):
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
    fig.suptitle('Learning progress of the Q-Learning Agent', fontsize=16)
    plt.show()

    plt.savefig(name + '.png')

def updateDifficulty(difs, index, solved):
    # Decreasde the difficulty of the problem by 100 if it was solved, increase it by 1 if it was not solved
    if solved == True:
        difs[index] += -1
    else:
        difs[index] -= 100

def chooseNewConfig(df, strategy, difs):
    '''Get a new vector from the dataframe based on the strategy chosen
    The strategies are:
    - random: choose a random vector from the dataframe (1)
    - most difficult: choose the vector with the highest difficulty value (2)'''

    if strategy == 1:
        # Choose a random vector from the dataframe
        candidate = np.random.randint(0, len(df))
    elif strategy == 2:
        # Choose the vector with the highest difficulty value
        maxId = np.argmax(difs)
        candidate = np.array(df.iloc[maxId])

    # Return the first column of the dataframe (the vector)
    return candidate, maxId
    
if __name__ == "__main__":
    qLearningAgent()