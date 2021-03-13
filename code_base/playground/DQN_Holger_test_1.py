
#Dependencies import

import random
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
NUM_EPISODES = 2_000
MAX_EPISODE_STEPS = 100


STATES = 2



def main():
	
	
	env = default_warehouse_6() #initiation of warenhouse environment
	action_space_size = env.num_actions #get number of possible actions
	state_space_size = env.total_states #get number of state parameters

	agent = DQN_agent(STATES,action_space_size) #init of agent

	rewards_all_episodes = []    # only for human metrics
	rewards_current_episode = 0  # only for human metrics


	moving_average_20 = deque(maxlen=20) # only for human metrics


	for episode in range(NUM_EPISODES):

		#environment setup	
		state = env.reset(DQN=True) # resets environment for new simulation
		state = np.reshape(state, [1, STATES])

		done = False
		rewards_current_episode = 0

		#iteration process
		for step in range (MAX_EPISODE_STEPS):

			#let agent take action
			action = agent.act(state)
			
			"""
			if (episode % 10 == 0): # to see what is going on (simulation)
				os.system('clear')
				print("\033[1;41m" + "simulation run: {}".format(episode) + "\033[1;m")
				#print("most recent reward: {}".format(rewards_all_episodes[-1]))
				env.show()
				time.sleep(0.5)
			"""

			new_state, reward, done = env.step(action,DQN=True)
			new_state = np.reshape(new_state, [1, STATES])

			agent.remember(state, action, reward, new_state, done)
			
			state = new_state

			rewards_current_episode += reward

			if done == True:
				moving_average_20.append(rewards_current_episode)
				print("episode: {}/{}, score: {}, epsilon: {}, Moving average: {}".format(episode, NUM_EPISODES, rewards_current_episode,agent.epsilon,mean(moving_average_20)))
			
				break

		if len(agent.memory) > BATCH_SIZE:
			agent.replay(BATCH_SIZE)

		rewards_all_episodes.append(rewards_current_episode)
	
main()