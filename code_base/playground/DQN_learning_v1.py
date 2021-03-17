
#Dependencies import

import random
import math
import time
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import os

from statistics import mean

import sys
sys.path.append('../')

from warehouse_environments.warehouse import Warehouse
from warehouse_environments.default_warehouses import *

from agent_classes.DQN_holger import DQN_agent



# HYPER PARAMETERS
BATCH_SIZE = 4
NUM_EPISODES = 3_000
MAX_EPISODE_STEPS = 20

STATES = 2



def main():
	
	
	env = default_warehouse_7() #initiation of warenhouse environment
	action_space_size = env.num_actions #get number of possible actions
	state_space_size = env.total_states #get number of state parameters

	agent = DQN_agent(STATES, action_space_size, env.ROWS, env.COLUMNS) #init of agent
	
	rewards_all_episodes = []    # only for human metrics
	rewards_current_episode = 0  # only for human metrics


	moving_average_20 = deque(maxlen=80) # only for human metrics
	state = np.array([])

	for episode in range(NUM_EPISODES):

		#environment setup	
		state = env.reset(DQN=True,randomised_position=False) # resets environment for new simulation
		
		#state = np.concatenate((state, np.array(env.goal_state[0])))

		state = np.reshape(state, [1, STATES])
	
		done = False
		rewards_current_episode = 0
		reward = 0

		#iteration process
		for step in range (MAX_EPISODE_STEPS):

			#let agent take action
			action = agent.act(state)

			
			
			if (episode > 2000): # to see what is going on (simulation)
				os.system('clear')
				print("\033[1;41m" + "simulation run: {}".format(episode) + "\033[1;m")
				print(f"reward: {reward}")
				print(f"exploration state value: {agent.exploration_memory[agent.state_number_rep(state)]}")
				#print("most recent reward: {}".format(rewards_all_episodes[-1]))
				env.show()
				time.sleep(0.5)
			

			new_state, reward, done = env.step(action+1,DQN=True)
			
			
			#new_state = np.concatenate((new_state, np.array(env.goal_state[0])))

			#if not done:
				#distance_sq = (new_state[0]-env.goal_state[0][0])**2 + (new_state[1]-env.goal_state[0][1])**2
				#reward += (  (0.1)/((0.012*distance_sq)-(0.02*math.sqrt(distance_sq))+0.08)  ) - 0.4


			new_state = np.reshape(new_state, [1, STATES])

			agent.remember(state, action, reward, new_state, done)
			
			state = new_state

			rewards_current_episode += reward 

			if done == True:
				moving_average_20.append(rewards_current_episode)
				if state[0][0] == env.goal_state[0][0] and state[0][1] == env.goal_state[0][1]:
					print("SUCCESS")
				print("episode: {}/{}, score: {}, Moving average: {}, state: {}".format(episode, NUM_EPISODES, rewards_current_episode,mean(moving_average_20),state))
			
				break

		if len(agent.memory) > BATCH_SIZE:
			agent.replay(BATCH_SIZE)

		rewards_all_episodes.append(rewards_current_episode)
	
main()