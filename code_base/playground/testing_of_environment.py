import random
import os
import time
import numpy as np

import sys
sys.path.append('../')

from warehouse_environments.warehouse import Warehouse
from warehouse_environments.default_warehouses import *

def main():

	#input data
	num_episodes = 10000
	max_steps_per_episode = 100
	learning_rate = 0.1
	discount_rate = 0.99

	exploration_rate = 1
	max_exploration_rate = 1
	min_exploration_rate = 0.1
	exploration_decay_rate = 0.01


	#reward list, for performance check
	rewards_all_episodes = []


	env = default_warehouse_1()
	action_space_size = env.action_space
	state_space_size = env.obervation_space
	env.show()

	# Q-Learning algorithm
	for episode in range(num_episodes):
		
		state = env.reset()

		done = False
		rewards_current_episode = 0

		for step in range (max_steps_per_episode):

			#Exploration-exploitation trade-off
			exploration_rate_threshold = random.uniform(0,1)
			if exploration_rate_threshold > exploration_rate:
				action = np.argmax(q_table[state,:])
			else:
				action = env.action_space.sample()

			new_state, reward, done, info = env.step(action)

			# Update Q-table for Q(s,a)
			q_table[state, action] = q_table[state, action] * (1 - learning_rate) + \
			learning_rate * (reward+discount_rate*np.max(q_table[new_state, :]))

			state = new_state
			rewards_current_episode += reward

			if done == True:
				break

		# Exploration rate decay
		exploration_rate = min_exploration_rate + \
		(max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate*episode)
	
		rewards_all_episodes.append(rewards_current_episode)



if __name__ == '__main__':
	main()