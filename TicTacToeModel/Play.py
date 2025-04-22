from Board_Creation import TicTacToeEnv, user
from rl_agent import Q_Agent
import numpy as np
from Train_Agent import Train_Agent

# Initialize the environment and agents
env = TicTacToeEnv()
agent = Q_Agent(env, alpha=0.1, gamma=0.9, epsilon=0.1)
human_player = user(env)
train_agent = Train_Agent(env, agent, human_player)


# Train the agent against the human player
train_agent.train_against_human(episodes=10)


# Print the training statistics
print("Training Statistics:")
print(f"Wins: {train_agent.stats['wins']}")
print(f"Losses: {train_agent.stats['losses']}")
