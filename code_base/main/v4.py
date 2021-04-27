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
BATCH_SIZE = 4
NUM_EPISODES = 25_000
MAX_EPISODE_STEPS = 200
CORRECT_MOVE_REWARD = 0.05

# MAIN 

def main():
		
	env = default_warehouse_final_boss() #initiation of warenhouse environment
	
	env.add_agent(3,2,4,9)
	env.add_agent(5,2,2,9)
	env.add_agent(7,2,6,8)
	env.add_agent(9,2,7,9)
	
	env.set_start_state()
	env.show()

	agent = DQN_agent(env.agent_state_count*env.agents, env.num_actions, env.ROWS, env.COLUMNS) #init of agent
	agent2 = DQN_agent(env.agent_state_count*env.agents, env.num_actions, env.ROWS, env.COLUMNS) #init of agent
	agent3 = DQN_agent(env.agent_state_count*env.agents, env.num_actions, env.ROWS, env.COLUMNS) #init of agent
	agent4 = DQN_agent(env.agent_state_count*env.agents, env.num_actions, env.ROWS, env.COLUMNS) #init of agent
	
	rec_moves_to = [
	{
	env.get_state([3,3]):1,
	env.get_state([3,4]):1,
	env.get_state([4,4]):4,
	env.get_state([5,4]):4,
	env.get_state([5,5]):1,
	env.get_state([5,6]):1,
	env.get_state([5,7]):1,
	env.get_state([4,7]):3,
	env.get_state([4,8]):1
	},
	{
	env.get_state([5,3]):1,
	env.get_state([4,3]):3,
	env.get_state([3,3]):3,
	env.get_state([2,3]):3,
	env.get_state([2,4]):1,
	env.get_state([2,5]):1,
	env.get_state([2,6]):1,
	env.get_state([2,7]):1,
	env.get_state([2,8]):1
	},
	{
	env.get_state([7,3]):1,
	env.get_state([7,4]):1,
	env.get_state([6,4]):3,
	env.get_state([6,5]):1,
	env.get_state([6,6]):1,
	env.get_state([6,7]):1
	},
	{
	env.get_state([9,3]):1,
	env.get_state([9,4]):1,
	env.get_state([9,5]):1,
	env.get_state([9,6]):1,
	env.get_state([9,7]):1,
	env.get_state([8,7]):3,
	env.get_state([7,7]):3,
	env.get_state([7,8]):1,
	}
	]

	rec_moves_from = [
	{
	env.get_state([4,8]):2,
	env.get_state([4,7]):2,
	env.get_state([5,7]):4,
	env.get_state([5,6]):2,
	env.get_state([5,5]):2,
	env.get_state([5,4]):2,
	env.get_state([4,4]):3,
	env.get_state([3,4]):3,
	env.get_state([3,3]):2
	},
	{
	env.get_state([2,8]):2,
	env.get_state([2,7]):2,
	env.get_state([2,6]):2,
	env.get_state([2,5]):2,
	env.get_state([2,4]):2,
	env.get_state([2,3]):2,
	env.get_state([3,3]):4,
	env.get_state([4,3]):4,
	env.get_state([5,3]):4
	},
	{
	env.get_state([6,7]):2,
	env.get_state([6,6]):2,
	env.get_state([6,5]):2,
	env.get_state([6,4]):2,
	env.get_state([7,4]):4,
	env.get_state([7,3]):2
	},
	{
	env.get_state([7,8]):2,
	env.get_state([7,7]):2,
	env.get_state([8,7]):4,
	env.get_state([9,7]):4,
	env.get_state([9,6]):2,
	env.get_state([9,5]):2,
	env.get_state([9,4]):2,
	env.get_state([9,3]):2	
	}
	]

	print(rec_moves_to)
	
	agentos = [agent,agent2,agent3,agent4]

	rewards_all_episodes = [0,0,0,0]    # only for human metrics
	rewards_current_episode = [0,0,0,0]  # only for human metrics
	num_of_success = 0
	num_packages = 0

	moving_average_20a = deque(maxlen=400) # only for human metrics
	moving_average_20b = deque(maxlen=400) # only for human metrics
	moving_average_20c = deque(maxlen=400) # only for human metrics
	moving_average_20d = deque(maxlen=400) # only for human metrics
	successes_last_100 = deque(maxlen=100)

	rock = False

	packages_total = []
	file_count = 0


	for episode in range(NUM_EPISODES):
		
		if len(packages_total) % 700 == 0:
			with open('LOGGED_v4,'+str(file_count)+'.csv', mode='w') as the_file:
				writer = csv.writer(the_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				for the_file_elements in range(len(packages_total)):
					writer.writerow([the_file_elements,packages_total[the_file_elements]])
			file_count += 1
		

		done = False
		rewards_current_episode = [0,0,0,0]

		if num_packages > 80:
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

			if (episode > 40000): # to see what is going on (simulation)
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

				if env.current_state[i][2] == 0 and env.get_state(env.current_state[i]) in rec_moves_to[i]:
					if rec_moves_to[i][env.get_state(env.current_state[i])] == action_list[i]:
						rewards_current_episode[i] += CORRECT_MOVE_REWARD

				elif env.current_state[i][2] == 1 and env.get_state(env.current_state[i]) in rec_moves_from[i]:
					if rec_moves_from[i][env.get_state(env.current_state[i])] == action_list[i]:
						rewards_current_episode[i] += CORRECT_MOVE_REWARD

				done = True if event_list[i][2] else done

			if done == True:
				moving_average_20a.append(rewards_current_episode[0])
				moving_average_20b.append(rewards_current_episode[1])
				moving_average_20c.append(rewards_current_episode[2])
				moving_average_20d.append(rewards_current_episode[3])
				
				for i in range(env.agents):
					if event_list[i][1] == 5:
						num_packages += 1
				
			
				successes_last_100.append(0)
				for i in range(env.agents):
					agentos[i].remember(state[i], action_list[i], event_list[i][1],event_list[i][0], event_list[i][2])
					state[i] = event_list[i][0]
			
				if not sum(successes_last_100) > 70 and episode < 14000:
					os.system('clear')
					print("episode: {}/{}, \
						\nMoving average: {} \
						\nMoving average 2: {}\
						\nMoving average 3: {}\
						\nMoving average 4: {}\
						\nnum_packages: {}"\
						.format(episode, NUM_EPISODES, mean(moving_average_20a),mean(moving_average_20b),mean(moving_average_20c),mean(moving_average_20d),num_packages))
				
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