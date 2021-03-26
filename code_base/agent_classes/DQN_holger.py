import random
import numpy as np
from collections import deque
import os

import sys
sys.path.append('../')
from neural_nets.neural_nets import *


class DQN_agent:
	
	def __init__(self, state_size, action_size,rows,columns):

		self.state_size = state_size   # used for input  nodes in NN
		self.action_size = action_size # used for output nodes in NN
		self.__COLUMNS = columns
		self.__ROWS = rows

		self.exploration_memory = {} #lookup table for dynamic exploration
		self.visited_memory = {}
	
		self.memory = deque(maxlen=50_000) # for training later on


		#parameter setup (can be changed for tuning behavior)
		self.gamma = 0.9              # learning rate 
		self.epsilon = 1.0 				# exploration rate
		self.epsilon_min = 0.07		    # mimimum possible exploration rate
		self.epsilon_decay_rate = 0.997  # decay of exploration

		self.learning_rate = 0.0005      # this is learning rate for adam in NN

		self.model = self._build_model()# initiates the model NN 

	def _build_model(self):

		model = neural_n_1(self.state_size,self.action_size,self.learning_rate)

		return model

	def remember(self, state, action, reward, new_state, done):

		#save event as a memory in the deque
		self.memory.append( (state, action, reward, new_state, done) )



	def state_number_rep(self,wanted_state):
	#needs to be affected by num of cols and rows and number of robots.
		
		state = 0
		robot_counter = 0
		matrix_size = self.__COLUMNS * self.__ROWS

		for i in wanted_state:
						
			multiplier = matrix_size ** robot_counter
			robot_counter+= 1

			state += ((i[0]-1)*self.__COLUMNS + (i[1]-1))*multiplier

		return state


	def act(self, state):

		state_as_number = self.state_number_rep(state) #converting from coordinates to number 

		if state_as_number not in self.exploration_memory:
			self.exploration_memory[state_as_number] = 1

		if np.random.rand() <= self.exploration_memory[state_as_number]:
			
			if self.exploration_memory[state_as_number] > self.epsilon_min:
				self.exploration_memory[state_as_number] -= 0.03
			
			return random.randrange(self.action_size)

		act_values = self.model.predict(state) # return np array(s) of predictions
		return np.argmax(act_values) # return index of highest valued element


	def replay (self, batch_size):

		mini_batch = random.sample(self.memory, batch_size)

		for state, action, reward, new_state, done in mini_batch:
			target = reward
			if not done:
				target = (reward + (self.gamma * np.max(self.model.predict(new_state),axis=1)))
			target_f = self.model.predict(state)
			
			target_f[0][action] = target
			
			self.model.fit(state, target_f, verbose=0)


		if self.epsilon > self.epsilon_min:
			self.epsilon*=self.epsilon_decay_rate
















