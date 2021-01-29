# for documentation ,check: wiki/program structure. 

class Warehouse:
	
	def __init__(self, __DEFAULT_SIZE = 10):
		self.matrix = []
		self.__DEFAULT_SIZE = __DEFAULT_SIZE

		print("Warehouse object initiated")		

	def make(self,default=None):
	#returns a matrix of 10x10 as default
		for i in range(self.__DEFAULT_SIZE):
			self.matrix.append([0 for i in range(self.__DEFAULT_SIZE)])

	def show(self):
		print("\n")
		for i in self.matrix:
			print(' '.join(str(i) for i in i))
		print("\n")

	def fill(self):
		pass
	
def main():

	obj = Warehouse()
	obj.make()
 	
 	obj.show()
 	print("teest")

if __name__ == '__main__':
	main()