import random
import csv
import os
import time
import numpy as np

import sys

sys.path.append('../')
from warehouse_environments.default_warehouses import default_warehouse_DQN, default_warehouse_1

def main():

	#input data

	num_episodes = 20_000
	max_steps_per_episode = 200
	learning_rate = 0.9
	discount_rate = 0.9999

	exploration_rate = 1
	max_exploration_rate = 1
	min_exploration_rate = 0.1
	exploration_decay_rate = 0.00001


	#reward list, for performance check
	rewards_all_episodes = []

	env = default_warehouse_DQN()
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
			
			"""
			if episode > (num_episodes-100):
				os.system('clear')
				print("\033[1;41m" + "simulation run: {}".format(episode) + "\033[1;m")
				print("exploration_rate: {}".format(exploration_rate))
				print("most recent reward: {}".format(rewards_all_episodes[-1]))
				env.show()
				time.sleep(1)
			"""
			new_state, reward, done = env.step(action)



			
			if reward == 2 and episode > (num_episodes-100):
				os.system('clear')
				print(rewards_current_episode)
				print(done)
				time.sleep(2.5)
			

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


	
	with open('LOGGED_Q'+'.csv', mode='w') as the_file:
		writer = csv.writer(the_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for the_file_elements in range(len(rewards_all_episodes)):
			writer.writerow([the_file_elements,rewards_all_episodes[the_file_elements]])
	




if __name__ == '__main__':
	main()