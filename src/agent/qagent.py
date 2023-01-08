import numpy as np
import random
import gym
import pandas as pd
import environment as env

def qLearningAgent():
    # Create environment to interact with
    environment = env.BugPlus()

    # Initialize Q-table
    # TODO: Calculate size of possible observations
    Q = np.zeros((environment.observation_space.n, 70))

    # Set hyperparameters parameters
    learningRate = 0.8
    discountRate = 0.95
    epsilon = 1
    decayRate = 0.005

    # Initialize training parameters
    numEpisodes = 10000
    maxSteps = 1

    # Pick configuration from configs.csv to train on
    df = pd.read_csv("configs.csv", sep=";")
    vector = np.array(df.iloc[np.random.randint(0, len(df))])

    # Train agent
    for episode in range(numEpisodes):
        # Reset environment and get first new observation
        environment.reset()
        environment.setVectorAsObservationSpace(vector)
        environment.setInputAndOutputValuesFromVector(vector)

        # The Q-Table learning algorithm
        for step in range(maxSteps):
            # Pick an action based on epsilon-greedy policy
            if random.uniform(0, 1) < epsilon:
                action = environment.action_space.sample()
            else:
                action = np.argmax(Q[environment.observation_space, :])

            # Get new state and reward from environment
            step_reward, observation_space, ep_return, done, list = environment.step(action)
            reward = step_reward

            # Update Q-Table with new knowledge
            Q[environment.observation_space, action] = Q[environment.observation_space, action] + learningRate * (
                        reward + discountRate * np.max(Q[observation_space, :]) - Q[environment.observation_space, action])

        # Reduce epsilon (because we need less and less exploration)
        epsilon = min(1, max(0, epsilon - decayRate))

    print("Training finished over {numEpisodes} episodes.")
    input("Press Enter to see out of 100 tries how often the agent picks the correct edge to add to the matrices...")

    # Test agent
    numCorrect = 0
    reward = 0
    for i in range(100):
        environment.reset()
        environment.setVectorAsObservationSpace(vector)
        environment.setInputAndOutputValuesFromVector(vector)
        
        action = np.argmax(Q[environment.observation_space, :])
        step_reward, observation_space, ep_return, done, list = environment.step(action)
        reward = step_reward

        if step_reward == 1:
            numCorrect += 1
    avg_reward = reward / 100
        
    # Print results
    print("Agent picked the correct edge to add to the matrices {numCorrect} times out of 100 tries.")
    print("The average reward gained by the agent was {avg_rewward}.")

if __name__ == "__main__":
    qLearningAgent()