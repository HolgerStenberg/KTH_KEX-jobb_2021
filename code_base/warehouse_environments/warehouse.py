# for documentation ,check: wiki/program structure. 

class Warehouse:	
	def __init__(self, __ROWS = 10, __COLUMNS = 10):
		#returns a matrix of 10x10 as default
		self.matrix = []
		self.__ROWS = __ROWS
		self.__COLUMNS = __COLUMNS

		for i in range(self.__ROWS):
			self.matrix.append([0 for i in range(self.__COLUMNS)])

		print("Warehouse object initiated")		

	def matrix_fill(self, row, column, fill_type = 1):

		if (row > 0 and row <= self.__ROWS):
			if (column > 0 and column <= self.__COLUMNS):
				self.matrix[row-1][column-1] = fill_type
				return 0
			else:
				print("FILL ERROR: column does not exist")
		else:
			print("FILL ERROR: row does not exist")
		
		return 1

	def show(self):
		#shows the matrix 
		print("\n")
		for i in self.matrix:
			print(' '.join(str(i) for i in i))
		print("\n")


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
	

#only run if this file is executed as only file
def main():

	obj = Warehouse(5,5)
	obj.show()

 	obj.obstacle_line("right", 1, 1, 3)
 	obj.show()
 	#print("teest")

if __name__ == '__main__':
	main()