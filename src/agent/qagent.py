import numpy as np
import random
import gym
import environment.environment as env

def qLearningAgent():
    # Create environment to interact with
    environment = env.Environment()

    # Initialize Q-table
    Q = np.zeros((environment.observation_space.n, environment.action_space.n))

    # Set hyperparameters parameters
    learningRate = 0.8
    discountRate = 0.95
    epsilon = 1
    decayRate = 0.005

    # Initialize training parameters
    numEpisodes = 10000
    maxSteps = 1

    # Train agent
