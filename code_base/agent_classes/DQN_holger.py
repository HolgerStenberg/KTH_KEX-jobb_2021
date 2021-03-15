import random
import time
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import os


class DQN_agent:
	
	def __init__(self, state_size, action_size):

		self.state_size = state_size   # used for input  nodes in NN
		self.action_size = action_size # used for output nodes in NN
	
		self.memory = deque(maxlen=5_000) # for training later on


		#parameter setup (can be changed for tuning behavior)
		self.gamma = 0.9              # learning rate 
		self.epsilon = 1.0 				# exploration rate
		self.epsilon_decay_rate = 0.998 # decay of exploration
		self.epsilon_min = 0.01		    # mimimum possible exploration rate

		self.learning_rate = 0.010      # this is learning rate for adam in NN

		self.model = self._build_model()# initiates the model NN 

	def _build_model(self):

		model = Sequential()

		model.add(Dense(8,
			            input_dim = self.state_size,
			            activation = 'relu'))
		
		model.add(Dense(5, activation = 'relu')) #hidden layer
		model.add(Dense(5, activation = 'relu')) #hidden layer
		model.add(Dense(5, activation = 'relu')) #hidden layer
		model.add(Dense(5, activation = 'relu')) #hidden layer
		model.add(Dense(5, activation = 'relu')) #hidden layer
		model.add(Dense(5, activation = 'relu')) #hidden layer
		model.add(Dense(5, activation = 'relu')) #hidden layer

		
		model.add(Dense(self.action_size, activation = 'linear'))

		model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))

		return model

	def remember(self, state, action, reward, new_state, done):

		#save event as a memory in the deque
		self.memory.append( (state, action, reward, new_state, done) )


	def act(self, state):

		if np.random.rand() <= self.epsilon:
			return random.randrange(self.action_size)

		act_values = self.model.predict(state) # return np array(s) of predictions
		return np.argmax(act_values[0]) # return index of highest valued element


	def replay (self, batch_size):

		mini_batch = random.sample(self.memory, batch_size)

		for state, action, reward, new_state, done in mini_batch:
			target = reward
			if not done:
				target = (reward + self.gamma * np.argmax(self.model.predict(new_state)[0]))
			target_f = self.model.predict(state)
			target_f[0][action] = target

			self.model.fit(state, target_f, epochs=10, verbose=0)


		if self.epsilon > self.epsilon_min:
			self.epsilon*=self.epsilon_decay_rate
















