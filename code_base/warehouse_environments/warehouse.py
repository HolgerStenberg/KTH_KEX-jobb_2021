# for documentation ,check: wiki/program structure. 
import time
import copy
import random
import numpy as np


class Warehouse:	
	def __init__(self, __ROWS = 10, __COLUMNS = 10):
		#returns a matrix of 10x10 as default
		self.matrix = []
		self.__ROWS = __ROWS
		self.__COLUMNS = __COLUMNS

		self.agents = 0
		self.current_state = []
		self.goal_state = []
		self.obstacles_coords = []


		self.num_actions = 0 
		self.total_states = 0

		for i in range(self.__ROWS):
			self.matrix.append(["." for i in range(self.__COLUMNS)])

		print("Warehouse object initiated")	


	#SHOW CURRENT STATE
	def show(self):
	#shows the matrix 
		print("\n")
		for i in self.matrix:
			print(' '.join(str(i) for i in i))
		print("\n")


	def get_state(self,wanted_state):
	#needs to be affected by num of cols and rows and number of robots.

		state = 0
		robot_counter = 0
		matrix_size = self.__COLUMNS * self.__ROWS

		for i in wanted_state:
			
			multiplier = matrix_size ** robot_counter
			robot_counter+= 1

			state += ((i[0]-1)*self.__COLUMNS + (i[1]-1))*multiplier

		return state

	def get_state_lst(self,state,mtrx = True):

		the_list = []

		for i in range(self.agents):
			action_modulus = (self.__ROWS*self.__COLUMNS)**(self.agents-i-1)
			action_counter = 0
			while state >= action_modulus:

				state -= action_modulus
				action_counter += 1 
			
			if mtrx == True:

				tmp_list = [0,0]
				
				while action_counter >= self.__COLUMNS:
					tmp_list[0] += 1
					action_counter -= self.__COLUMNS

				tmp_list[1] = action_counter+1
				tmp_list[0] += 1

				the_list.insert(0,tmp_list)
			else:
				the_list.insert(0,action_counter)

		return the_list


	#RESETS BACK TO START STATE
	def reset(self, DQN = False): 

		#print("Reseting")
		self.current_state = copy.deepcopy(self.start_state)
		self.matrix = copy.deepcopy(self.start_matrix)

		if DQN == False:
			return self.get_state(self.start_state)

		else:
			np_array = []
			for i in self.start_state:
				for j in i:
					np_array.append(j)
			
			return np.array(np_array)


	def sample_action(self):
		return random.randint(0, self.num_actions-1)


	def update_robot_location_graphics(self,robot_id,action):

		# stay
		if (action == 0):
			pass
		
		# go right
		elif (action == 1):

			self.matrix_fill(self.current_state[robot_id][0],\
				self.current_state[robot_id][1],'.')

			self.matrix_fill(self.current_state[robot_id][0],\
				(self.current_state[robot_id][1])+1,chr(ord('a')+robot_id))

		# go left
		elif (action == 2):
			self.matrix_fill(self.current_state[robot_id][0],\
				self.current_state[robot_id][1],'.')

			self.matrix_fill(self.current_state[robot_id][0],\
				self.current_state[robot_id][1]-1,chr(ord('a')+robot_id))

		# go up
		elif (action == 3):
			self.matrix_fill(self.current_state[robot_id][0],\
				self.current_state[robot_id][1],'.')

			self.matrix_fill(self.current_state[robot_id][0]-1,\
				self.current_state[robot_id][1],chr(ord('a')+robot_id))
			

		# go down
		elif (action == 4):
			self.matrix_fill(self.current_state[robot_id][0],\
				self.current_state[robot_id][1],'.')

			self.matrix_fill(self.current_state[robot_id][0]+1,\
				self.current_state[robot_id][1],chr(ord('a')+robot_id))

		else:
			pass


	#IN SIMULATION
	def step(self, action, DQN = False):

		#parsing of action:
		action_list = []
		
		for i in range(self.agents):
			action_modulus = 5**(self.agents-i-1)
			action_counter = 0
		
			while action >= action_modulus:

				action -= action_modulus
				action_counter += 1 
				
			action_list.insert(0,action_counter)


		for i in range(self.agents):
			#updates graphics of matrix
			self.update_robot_location_graphics(i,action_list[i])
			
			# stay
			if (action_list[i] == 0):
				pass
			
			# go right
			elif (action_list[i] == 1):
				self.current_state[i][1]+=1

			# go left
			elif (action_list[i] == 2):
				self.current_state[i][1]-=1

			# go up
			elif (action_list[i] == 3):
				self.current_state[i][0]-=1

			# go down
			elif (action_list[i] == 4):
				self.current_state[i][0]+=1

			else:
				pass

		new_state = self.get_state(self.current_state)
		reward,done = self.reward_table[new_state]
		
		if DQN == True:
			np_array = []
			for i in self.current_state:
				for j in i:
					np_array.append(j)

			return(np.array(np_array), reward, done)
		else:
			return (new_state, reward, done)

	#CONSTRUCTION OF ENVIRONMENT *********


	#SETS REWARD TABLE
	def populate_reward_table(self):

		self.reward_table = []
		#total amount of states:
		self.total_states = ((self.__COLUMNS*self.__ROWS)**self.agents) 
		print("total states: {}".format(self.total_states))

		#init
		for i in range(self.total_states):
			self.reward_table.append((-1,False)) 
		
		#find combo of goals, that should get 100 points:
		stated = self.get_state(self.goal_state)
		self.reward_table[stated] = (100,True)


		#add forbidden states - robot collision:
		if (self.agents > 1):
			for i in range(self.total_states):
				if len(self.get_state_lst(i,False)) != len(set(self.get_state_lst(i,False))):
					self.reward_table[i] = (-100,True)


		#add forbidden states - obstacle collision:
		for given_obstacle_coord in self.obstacles_coords:
			#print("forbidden: {}".format(given_obstacle_coord))
		
			for state in range(self.total_states):
				coord_state = self.get_state_lst(state)
				if given_obstacle_coord in coord_state:
					self.reward_table[state] = (-100,True)


	#SETS A START STATE
	def set_start_state(self):
		
		self.start_state = copy.deepcopy(self.current_state)
		
		print("start_state generated!")
		print("num of robots: {}".format(self.agents))

		self.num_actions = 5**self.agents
		print("num of actions: {}".format(self.num_actions))

		self.populate_reward_table()
		print("Reward table generated..")

		self.start_matrix = copy.deepcopy(self.matrix)


	def add_agent(self, row, col, target_row, target_col):
		#fills agents as lower case, and add goals as upper case.
		self.matrix_fill(row,col,chr(ord('a')+self.agents))
		self.matrix_fill(target_row,target_col,chr(ord('A')+self.agents))
		self.agents += 1

		self.current_state.append([row, col])
		self.goal_state.append([target_row, target_col])


	def obstacle_line(self,direction,row,column,length):

		for i in range(length):
			self.matrix_fill(row, column)
			self.obstacles_coords.append([row,column])

			if direction == "up":
				row -= 1;

			elif direction == "down":
				row += 1;

			elif direction == "left":
				column -= 1;

			elif direction == "right":
				column += 1;
	
	def matrix_fill(self, row, column, fill_type = "H"):

		if (row > 0 and row <= self.__ROWS):
			if (column > 0 and column <= self.__COLUMNS):
				self.matrix[row-1][column-1] = fill_type
				return 0
			else:
				print("FILL ERROR: column does not exist")
		else:
			print("FILL ERROR: row does not exist")
		
		return 1




#only run if this file is executed as only file
def main():

	obj = Warehouse(3,3)
	obj.add_agent(1,1,3,3)
	obj.add_agent(1,2,2,3)
	obj.set_start_state()
	
	print(obj.step(0,DQN=True))

	print(obj.reset(DQN=True))


if __name__ == '__main__':
	main()