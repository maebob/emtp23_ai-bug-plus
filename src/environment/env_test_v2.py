# Test wether the environment`s reward assignment works for correct results
import sys
#sys.path.append('/Users/mayte/github/bugplusengine') # Mayte
sys.path.append('C:/Users/D073576/Documents/GitHub/BugPlusEngine/') # Mae
# sys.path.append('/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/') # Aaron
import src.environment.environment as env
import numpy as np

# Create incrementor matrces with one edge removed
control_flow = np.zeros((5, 7), dtype=int)
data_flow = np.zeros((7, 5), dtype=int)

# Create the environment
environment = env.BugPlus()
acc_reward = 0

for i in range(10):
    environment.reset()
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

    # Replace missing edge
    reward, observation_space, ep_return, done, list = environment.step(32)
    acc_reward += reward
    print(i)


print("\n Average Reward: ")
print(acc_reward/10)