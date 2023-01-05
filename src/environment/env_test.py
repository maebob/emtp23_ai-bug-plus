import environment

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

print(" \nReward: " + str(reward))