import sys
sys.path.append('../')

from warehouse_environments.warehouse import Warehouse
def main():
	obj = Warehouse()

	obj.make()
	obj.show()

	try:
		obj.fill()
	except:
		print("not yet implemented")
		

	

if __name__ == '__main__':
	main()