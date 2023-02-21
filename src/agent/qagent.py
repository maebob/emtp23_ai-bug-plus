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

''' Current Expermient:
    - Goal try to learn to restore configs for 4x + 4y 
    - Agent is restricted to one step per episode
    - As long as the config has not been solved the agent will be trained on the same config
    - If the config has been solved the agent will be trained on a new randomly chosen config'''

def qLearningAgent():
    # Create variables needed to store information about the learning progress
    count_solved_problems = 0 # count the number of solved problems
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
    # state = np.concatenate((observation_space[0].flatten(),observation_space[1].flatten()), axis=0) # flattened matrices concatenated into one array
    # n_observations = state.size

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

    # Initialize Q-table
    Q = np.zeros((len(df), n_actions))
    state = np.random.randint(0, len(df))
    vector = np.array(df.iloc[state])

    # Marker to check wether or not a configuration was solved
    config_solved = False

    # Train agent
    for episode in range(numEpisodes):
        # Reset environment and get first new observation
        #state = environment.reset()
        environment.reset()
        # Initialize matrices with config from configs_4x+4y.csv
        if config_solved == False:
            environment.setVectorAsObservationSpace(vector)
            environment.setInputAndOutputValuesFromVector(vector)
        else:
            # Choose new random config from configs_4x+4y.csv
            state = np.random.randint(0, len(df))
            vector = np.array(df.iloc[state])
            environment.setVectorAsObservationSpace(vector)
            environment.setInputAndOutputValuesFromVector(vector)
            config_solved = False

        # Upodate state of the environment
        # state = np.concatenate((observation_space[0].flatten(),observation_space[1].flatten()), axis=0)
        training_done = False
        # environment.setVectorAsObservationSpace(vector)
        # environment.setInputAndOutputValuesFromVector(vector)
        
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
            # reward = step_reward         
            #state = np.concatenate((observation_space[0].flatten(),observation_space[1].flatten()), axis=0)

            # Update Q-Table with new knowledge
            Q[state, action] = Q[state, action] + learningRate * (step_reward + discountRate * np.max(Q[state, :]) - Q[state, action])
            
            if done == True:
                config_solved = True
                count_solved_problems += 1
            else:
                config_solved = False

        # Reduce epsilon (because we need less and less exploration)
        epsilon = min(1, max(0, epsilon - decayRate))

        # Update the plotting information
        if (episode > 0) & (episode % 5000 == 0):
        
            proportion_new = count_solved_problems / 50  # = count_solved_problems / 5000 * 100
            no_episodes.append(episode/1000)
            tot_prblems_solved.append(count_solved_problems)
            prop_problems_solved.append(100 * count_solved_problems / episode)
            prop_problems_solved_lastX.append(proportion_new)
            improvement_lastX.append(proportion_new - proportion_old)

            # Reset and update the counters for the last 5,000 episodes
            count_pos_epsisodes = 0
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
    
if __name__ == "__main__":
    qLearningAgent()