import environment

env = environment.BugPlus()

env.reset()

for i in range (10):
    action = env.action_space.sample()
    print(action)
    env.step(action)

print("Control Flow Matrix after step:")
print(env.observation_space[0])

print("Data Flow Matrix after step:")
print(env.observation_space[1])