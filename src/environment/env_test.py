import environment
import numpy as np
import pandas as pd

''' 
env = environment.BugPlus()

env.reset()
env.initializeInputValues(2, 3)
env.initializeExpectedOutput(3)

reward = 0

for i in range (10):
    action = env.action_space.sample()
    print(action)
    step_reward, observation_space, ep_return, done, list = env.step(action)
    reward += step_reward

print("Control Flow Matrix after step:")
print(env.observation_space[0])

print("\nData Flow Matrix after step:")
print(env.observation_space[1])

print(" \nReward: " + str(reward))'''

# Create data frame out of configs.csv
df = pd.read_csv("configs.csv", sep=";")

# Create a numpy vector out of a random line in the data frame
vector = np.array(df.iloc[np.random.randint(0, len(df))])

# Initialize the environment with the vector
env = environment.BugPlus()
env.setVectorAsObservationSpace(vector)
env.setInputAndOutputValuesFromVector(vector)

print("Control Flow Matrix before step:")
print(env.observation_space[0])

print("\nData Flow Matrix before step:")
print(env.observation_space[1])

step_reward, observation_space, ep_return, done, list = env.step(35)
reward = step_reward
print("\nControl Flow Matrix after step:")
print(env.observation_space[0])

print("\nData Flow Matrix after step:")
print(env.observation_space[1])

print(" \nReward: " + str(reward))
