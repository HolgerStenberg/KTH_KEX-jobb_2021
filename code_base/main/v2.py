'''
V1 - Decentralised DQN with single and multiple robot compatability

Holger Stenberg
Johan Wahréus

'''

#Dependencies import
import csv
import random
import time
import os
import numpy as np
from collections import deque
from statistics import mean

# Import of written classes and functions, found in the code base directory
import sys
sys.path.append('../')

from warehouse_environments.warehouse_v2 import Warehouse
from warehouse_environments.default_warehouses_v2 import *
from agent_classes.DQN_v2 import DQN_agent


# HYPER PARAMETERS
BATCH_SIZE = 16
NUM_EPISODES = 25_000
MAX_EPISODE_STEPS = 200

# MAIN 

def main():
		
	env = default_warehouse_4() #initiation of warenhouse environment
	env.add_agent(3,2,4,7)
	env.add_agent(4,2,6,7)
	env.add_agent(5,2,2,7)
	env.set_start_state()
	env.show()

	agent = DQN_agent(env.agent_state_count*env.agents, env.num_actions, env.ROWS, env.COLUMNS) #init of agent
	agent2 = DQN_agent(env.agent_state_count*env.agents, env.num_actions, env.ROWS, env.COLUMNS) #init of agent
	agent3 = DQN_agent(env.agent_state_count*env.agents, env.num_actions, env.ROWS, env.COLUMNS) #init of agent
	agentos = [agent, agent2, agent3]

	rewards_all_episodes = []    # only for human metrics
	rewards_current_episode = [0,0,0]  # only for human metrics
	num_of_success = 0
	num_packages = 0

	moving_average_20a = deque(maxlen=400) # only for human metrics
	moving_average_20b = deque(maxlen=400) # only for human metrics
	moving_average_20c = deque(maxlen=400) # only for human metrics
	successes_last_100 = deque(maxlen=100)

	rock = False

	packages_total = []
	file_count = 0


	for episode in range(NUM_EPISODES):

		if len(packages_total) % 300 == 0:
			with open('LOGGED'+str(file_count)+'.csv', mode='w') as the_file:
				writer = csv.writer(the_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				for the_file_elements in range(len(packages_total)):
					writer.writerow([the_file_elements,packages_total[the_file_elements]])
			file_count += 1


		done = False
		rewards_current_episode = [0,0,0]

		if num_packages > 10:
			for ag in agentos:
				ag.epsilon_min = 0.01

		num_packages = 0
		#environment setup	
		state = env.reset(randomised_position=False) # resets environment for new simulation
		if sum(successes_last_100) > 60:
			agent.epsilon_min = 0

		#iteration process
		for step in range (1,MAX_EPISODE_STEPS):


			#let agent make action suggestions
			action_list = []
			for i in range(env.agents):
				action_list.append(agentos[i].act(state[i]))

			if (episode > 20000): # to see what is going on (simulation)
				if not rock: 
					input("rock and roll!")
					rock = True

				os.system('clear')
				print("\033[1;41m" + "simulation run: {}".format(episode) + "\033[1;m")
				#print(f"state_space_size already visited: {agent.visited_memory}")
				print("state:{}".format(state))
				print("delivered packages: {}".format(num_packages))
				#print("most recent reward: {}".format(rewards_all_episodes[-1]))
				env.show()
				time.sleep(0.3)

			event_list = env.sim_step(action_list)
			
			for i in range(env.agents):
				rewards_current_episode[i] += event_list[i][1]
				done = True if event_list[i][2] else done

			if done == True:
				moving_average_20a.append(rewards_current_episode[0])
				moving_average_20b.append(rewards_current_episode[1])
				moving_average_20c.append(rewards_current_episode[2])
				
				for i in range(env.agents):
					if event_list[i][1] == 5:
						num_packages += 1
				
			
				successes_last_100.append(0)
				for i in range(env.agents):
					agentos[i].remember(state[i], action_list[i], event_list[i][1], event_list[i][0], event_list[i][2])
					state[i] = event_list[i][0]
			
				if not sum(successes_last_100) > 70 and episode < 14000:
					os.system('clear')
					print("episode: {}/{}, \
						\nMoving average: {} \
						\nMoving average 2: {}\
						\nMoving average 3: {}\
						\nnum_packages: {}" \
						.format(episode, NUM_EPISODES, mean(moving_average_20a),mean(moving_average_20b),mean(moving_average_20c),num_packages))
				
				breakit = False
				for ev in event_list:
					if ev[1] == -1:
						breakit = True
				if breakit == True:
					packages_total.append(num_packages)
					break
				
			else:
				for i in range(env.agents):
					agentos[i].remember(state[i], action_list[i], event_list[i][1], event_list[i][0], event_list[i][2])
					state[i] = event_list[i][0]

			for i in range(env.agents):
				if len(agentos[i].memory) > BATCH_SIZE and sum(successes_last_100) < 50 and step%10 == 0:
					agentos[i].replay(BATCH_SIZE)

		for i in range(env.agents):
			if len(agentos[i].memory) > BATCH_SIZE and sum(successes_last_100) < 50:
				agentos[i].replay(BATCH_SIZE)

	
main()