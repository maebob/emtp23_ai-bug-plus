import numpy as np
import random
import gym
import pandas as pd
import sys
#sys.path.append('/Users/mayte/github/bugplusengine') # Mayte
sys.path.append('C:/Users/D073576/Documents/GitHub/BugPlusEngine/') # Mae
# sys.path.append('/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/') # Aaron
import src.environment.environment as env

def qLearningAgent():
    # Create environment to interact with
    environment = env.BugPlus()

    # Initialize Q-table
    # TODO: Calculate size of possible observations
    Q = np.zeros(70)

    # Set hyperparameters parameters
    learningRate = 0.8
    discountRate = 0.95
    epsilon = 1
    decayRate = 0.005


    # Initialize training parameters
    numEpisodes = 1000
    maxSteps = 1

    # Pick configuration from configs.csv to train on
    df = pd.read_csv("configs.csv", sep=";")
    vector = np.array(df.iloc[np.random.randint(0, len(df))])

    # Train agent
    for episode in range(numEpisodes):
        # Reset environment and get first new observation
        environment.reset()
        initialize(environment)
        training_done = False
        # environment.setVectorAsObservationSpace(vector)
        # environment.setInputAndOutputValuesFromVector(vector)
        
        # if episode == 99:
        #    print(environment.observation_space)

        # The Q-Table learning algorithm
        for step in range(maxSteps):
            # Pick an action based on epsilon-greedy policy
            if random.uniform(0, 1) < epsilon:
                action = environment.action_space.sample()
                # print("Random action: " + str(action))
            else:
                action = np.argmax(Q)
                # print("Q-Table action: " + str(action))

            # Get new state and reward from environment
            step_reward, observation_space, ep_return, done, list = environment.step(action)
            # reward = step_reward
            
            # Debugging catch------------------------------------------------------------------------------------
            if action == 32:
                print("AAAAAAAHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
            # Debugging catch------------------------------------------------------------------------------------

            # Update Q-Table with new knowledge
            Q[action] = Q[action] + learningRate * (
                        step_reward + discountRate * np.max(Q) - Q[action])
            
            if done == True:
                training_done = True
        
        if training_done == True:
            break

        # Reduce epsilon (because we need less and less exploration)
        epsilon = min(1, max(0, epsilon - decayRate))



    print("Training finished over " + str(numEpisodes) +  " episodes.")
    input("Press Enter to see out of 100 tries how often the agent picks the correct edge to add to the matrices...")

    # Test agent
    numCorrect = 0
    reward = 0

    environment.reset()
    # environment.setVectorAsObservationSpace(vector)
    # environment.setInputAndOutputValuesFromVector(vector)
    initialize(environment)
        
    action = np.argmax(Q)
    #print(action)
    #print(np.min(Q))
    #print(np.max(Q))
    step_reward, observation_space, ep_return, done, list = environment.step(action)

    reward += step_reward

    if step_reward == 10:
        numCorrect += 1

    #print(action)
        
    # Print results
    #print("Agent picked the correct edge to add to the matrices " + ((str)numCorrect) + " times out of 100 tries.")
    #print("The average reward gained by the agent was " + ((str)avg_reward) + ".")

    # Print number of correct guesses and average reward
    print("Agent picked the correct edge to add to the matrices " + str(numCorrect) + " times out of 1 tries.")
    print("The average reward gained by the agent was " + str(step_reward) + ". \n")

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
    
if __name__ == "__main__":
    qLearningAgent()