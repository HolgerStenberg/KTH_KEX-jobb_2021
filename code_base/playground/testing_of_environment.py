import random
import os
import time
import numpy as np

import sys

from code_base.warehouse_environments.default_warehouses import default_warehouse_2, default_warehouse_1

sys.path.append('../')


def main():

	#input data

	num_episodes = 500000
	max_steps_per_episode = 100
	learning_rate = 0.5
	discount_rate = 0.99999


	num_episodes = 300000
	max_steps_per_episode = 200
	learning_rate = 0.3
	discount_rate = 0.9999

	exploration_rate = 1
	max_exploration_rate = 1
	min_exploration_rate = 0.1
	exploration_decay_rate = 0.00001


	#reward list, for performance check
	rewards_all_episodes = []

	env = default_warehouse_1()
	action_space_size = env.num_actions
	state_space_size = env.total_states
	q_table = np.zeros((state_space_size, action_space_size))
	env.show()
	# Q-Learning algorithm
	for episode in range(num_episodes):
		state = env.reset()

		done = False
		rewards_current_episode = 0

		for step in range(max_steps_per_episode):

			#Exploration-exploitation trade-off
			exploration_rate_threshold = random.uniform(0,1)
			if exploration_rate_threshold > exploration_rate:
				action = np.argmax(q_table[state,:])
			else:
				action = env.sample_action()
			
			if episode > (num_episodes-100):
				os.system('clear')
				print("\033[1;41m" + "simulation run: {}".format(episode) + "\033[1;m")
				print("exploration_rate: {}".format(exploration_rate))
				print("most recent reward: {}".format(rewards_all_episodes[-1]))
				env.show()
				time.sleep(1)

			new_state, reward, done = env.step(action)

			if reward == 100 and episode > (num_episodes-100):
				os.system('clear')
				env.show()
				print("YAY")
				time.sleep(1.5)

			

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