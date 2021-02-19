# for documentation ,check: wiki/program structure. 
import time
import copy

class Warehouse:	
	def __init__(self, __ROWS = 10, __COLUMNS = 10):
		#returns a matrix of 10x10 as default
		self.matrix = []
		self.__ROWS = __ROWS
		self.__COLUMNS = __COLUMNS

		self.agents = 0
		self.current_state = []
		self.start_state = None

		for i in range(self.__ROWS):
			self.matrix.append(["." for i in range(self.__COLUMNS)])

		print("Warehouse object initiated")	


	#RESETS BACK TO START STATE
	def reset(self): 

		print("Reseting")
		self.current_state = copy.deepcopy(self.start_state)
		self.matrix = copy.deepcopy(self.start_matrix)

		return self.start_state


	#SHOW CURRENT STATE
	def show(self):
	#shows the matrix 
		print("\n")
		for i in self.matrix:
			print(' '.join(str(i) for i in i))
		print("\n")


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

	def get_new_state(self):
		pass



	#IN SIMULATION
	def step(self, action):

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


		new_state = self.get_new_state()
		reward = 1
		done=True
		return (new_state, reward, done)

	#CONSTRUCTION OF ENVIRONMENT *********


	#SETS REWARD TABLE
	#def reward_table(self):
	#	for i in 


	#SETS A START STATE
	def set_start_state(self):
		
		self.start_state = copy.deepcopy(self.current_state)
		
		print("num of robots: {}".format(self.agents))

		self.start_matrix = copy.deepcopy(self.matrix)


	def add_agent(self, row, col, target_row, target_col):
		#fills agents as lower case, and add goals as upper case.
		self.matrix_fill(row,col,chr(ord('a')+self.agents))
		self.matrix_fill(target_row,target_col,chr(ord('A')+self.agents))
		self.agents += 1

		self.current_state.append([row, col])


	def obstacle_line(self,direction,row,column,length):

		for i in range(length):
			self.matrix_fill(row, column)

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

	obj = Warehouse(7,7)
	obj.show()	
	obj.add_agent(3,2,5,5)
	obj.add_agent(2,4,4,5)
	obj.add_agent(6,2,4,5)
	obj.show()
	obj.set_start_state()

	for i in range(5*5*5):
		obj.step(i)
		obj.show()
		time.sleep(0.2)
		obj.reset()

	


	
	

	


if __name__ == '__main__':
	main()