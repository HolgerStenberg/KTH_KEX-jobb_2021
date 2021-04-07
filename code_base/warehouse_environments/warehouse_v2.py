# for documentation ,check: wiki/program structure. 
import time
import copy
import random
import numpy as np

class Warehouse:	
	def __init__(self, ROWS = 10, COLUMNS = 10):
		#returns a matrix of 10x10 as default
		self.matrix = []
		self.obstacles_coords = []
		self.ROWS = ROWS
		self.COLUMNS = COLUMNS

		self.agents = 0
		self.agent_state_count = 3

		self.current_state = []
		self.goal_state = []
		self.available_start_states = []

		self.num_actions = 0 
		self.total_possible_states = 0

		for i in range(self.ROWS):
			self.matrix.append(["." for i in range(self.COLUMNS)])

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

		state = (wanted_state[0]-1)*self.COLUMNS + (wanted_state[1]-1)

		return state

	def update_robot_location_graphics(self,robot_id,action,start_move = False):

		
		if start_move == True:
			self.matrix_fill(self.start_state[robot_id][0],\
				self.start_state[robot_id][1],'.')

			self.matrix_fill(self.current_state[robot_id][0],\
				(self.current_state[robot_id][1]),chr(ord('a')+robot_id))

		# stay
		elif (action == 0):
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


	def add_to_available_start_states(self):
		for rows in range(self.ROWS):
			for columns in range(self.COLUMNS):
				if not [rows+1,columns+1] in self.obstacles_coords:
					self.available_start_states.append([rows+1,columns+1])


	#RESETS BACK TO START STATE
	def reset(self, randomised_position = False):

		self.current_state = None
		self.matrix = None
		self.current_state = copy.deepcopy(self.start_state)
		self.matrix = copy.deepcopy(self.start_matrix) 
		"""
		if randomised_position == True: 
			if self.available_start_states == []:
				self.add_to_available_start_states()
			
			self.current_state = copy.deepcopy([random.choice(self.available_start_states)])
			self.update_robot_location_graphics(0,-1,start_move=True)
		"""
		state_list = []
		'''
		for i in range(self.agents):
			np_array = np.array(self.current_state[i])
			np_array = np.reshape(np_array, [1, self.agent_state_count])
			state_list.append(np_array)
		'''
		a_tmp_lst = []
		for cord in self.current_state:
			for st in cord:
				a_tmp_lst.append(st)
		
		np_array = np.array(a_tmp_lst)
		np_array = np.reshape(np_array, [1, self.agent_state_count*self.agents])
		
		for i in range(self.agents):
			state_list.append(np_array)

		return state_list
	#IN SIMULATION
	def sim_step(self, action_requests):

		#parsing of action:
		action_request_list = []
		for i in action_requests:	
			action_request_list.append(i)

		event_list = []
		for i in range(self.agents):
			#updates graphics of matrix
			self.update_robot_location_graphics(i,action_request_list[i])
			
			# stay
			if (action_request_list[i] == 0):
				pass
			
			# go right
			elif (action_request_list[i] == 1):
				self.current_state[i][1]+=1

			# go left
			elif (action_request_list[i] == 2):
				self.current_state[i][1]-=1

			# go up
			elif (action_request_list[i] == 3):
				self.current_state[i][0]-=1

			# go down
			elif (action_request_list[i] == 4):
				self.current_state[i][0]+=1

			else:
				pass

			new_state = self.get_state(self.current_state[i])
			reward,done = self.reward_table[new_state]

			if new_state == self.get_state(self.goal_state[i]) and self.current_state[i][2] == 0:
				self.current_state[i][2] = 1
				reward = 2
			
			if new_state == self.get_state(self.start_state[i]) and self.current_state[i][2] == 1:
				self.current_state[i][2] = 0
				reward = 5
				done = True

			a_tmp_lst = []
			for cord in self.current_state:
				for st in cord:
					a_tmp_lst.append(st)
		
			np_array = np.array(a_tmp_lst)
			#np_array = np.array(self.current_state[i])
			np_array = np.reshape(np_array, [1, self.agent_state_count*self.agents])

			print(np_array)
			s

			event_list.append((np_array, reward, done))

		return event_list

	#CONSTRUCTION OF ENVIRONMENT *********

	#SETS REWARD TABLE
	def populate_reward_table(self):

		self.reward_table = [] # create table to be filled

		#total amount of states:
		self.total_possible_states = (self.COLUMNS*self.ROWS)
		
		#init
		for i in range(self.total_possible_states):
			self.reward_table.append((-0.01,False)) 

		#add forbidden states - obstacle collision:
		for given_obstacle_coord in self.obstacles_coords:
			self.reward_table[self.get_state(given_obstacle_coord)] = (-1,True)


	#SETS A START STATE
	def set_start_state(self):
		
		self.start_state = copy.deepcopy(self.current_state)
		self.num_actions = 5

		self.populate_reward_table()
	
		self.start_matrix = copy.deepcopy(self.matrix)

	def add_agent(self, row, col, target_row, target_col):
		#fills agents as lower case, and add goals as upper case.
		self.matrix_fill(row,col,chr(ord('a')+self.agents))
		self.matrix_fill(target_row,target_col,chr(ord('A')+self.agents))
		self.agents += 1

		self.current_state.append([row, col, 0])
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

		if (row > 0 and row <= self.ROWS):
			if (column > 0 and column <= self.COLUMNS):
				self.matrix[row-1][column-1] = fill_type
				return 0
			else:
				print("FILL ERROR: column does not exist")
		else:
			print("FILL ERROR: row does not exist")
		
		return 1


#only run if this file is executed as only file
def main():

	obj = Warehouse(4,4)
	
	obj.obstacle_line('right',2,1,1)

	obj.add_agent(1,2,3,3)
	obj.add_agent(1,1,3,4)

	obj.set_start_state()

	obj.show()

	print(obj.sim_step([1,4]))

	obj.show()

	print( "reset: {}".format(obj.reset()))


if __name__ == '__main__':
	main()