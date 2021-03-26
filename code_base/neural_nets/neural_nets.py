
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import Adam


def neural_n_1(state_size,action_size,learning_rate):

	model = Sequential([

			Dense(24,input_dim = state_size),
			Activation('relu'),
			Dense(24),
			Activation('relu'),
			Dense(24),
			Activation('relu'),
			Dense(action_size)

			])

	model.compile(loss='mse', optimizer=Adam(learning_rate=learning_rate))

	return model


