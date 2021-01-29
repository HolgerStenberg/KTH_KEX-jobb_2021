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

	def show(self):
		print("\n")
		for i in self.matrix:
			print(' '.join(str(i) for i in i))
		print("\n")

	def obstacle_line(self,direction,row,col,length):

		try:
			for i in range(length):
				self.matrix[row][col] = 1

				if direction == "up":
					row -= 1;

				elif direction == "down":
					row += 1;

				elif direction == "left":
					col -= 1;

				elif direction == "right":
					col += 1;

		except:
			print("out of bounds")
	
def main():

	obj = Warehouse(5,2)

 	
 	obj.show()
 	print("teest")

if __name__ == '__main__':
	main()