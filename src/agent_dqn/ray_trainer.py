from ray.rllib.agents.ppo import PPOTrainer
from src.environment.env_complex_observation import BugPlus

# Initialize the trainer
trainer = PPOTrainer(config={
    "env": BugPlus,
    "seed": 42069,
    "framework": "torch",
    "num_workers": 20,
    "num_gpus": 0,
    "num_envs_per_worker": 10,
    "num_cpus_per_worker": 1,
    "lr": 0.001,  # Specify the learning rate here
})

# Restore from the checkpoint
checkpoint_path = "result_data_coriculumn/PPO/PPO_BugPlus_1a19a_00000_0_2023-03-25_18-04-28/checkpoint_50/checkpoint-50"
trainer.restore(checkpoint_path)

# Train for a certain number of iterations
num_iterations = 100
stop_reward = 97.1
for i in range(num_iterations):
    result = trainer.train()
    print("Iteration {}: episode_reward_mean={}".format(i, result["episode_reward_mean"]))
    
    # Save a checkpoint every 5 iterations
    if i % 5 == 0:
        checkpoint = trainer.save()
        print("Checkpoint saved at", checkpoint)
    
    # Stop training if the mean reward is above the stop_reward
    if result["episode_reward_mean"] >= stop_reward:
        print("Stopping training as the mean reward reached", stop_reward)
        break
