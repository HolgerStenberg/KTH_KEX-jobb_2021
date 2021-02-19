import sys
import os
import time
import numpy as np

sys.path.append('../')
from warehouse_environments.warehouse import Warehouse
from warehouse_environments.default_warehouses import *


def main():

	#get_warehouse(10,10,4)


	



	

	for i in range(10):
		print("\033[1;41m" + "simulation run: {}".format(i) + "\033[1;m")

		env = default_warehouse_3()
		env.show()
		time.sleep(0.5)
		os.system('clear')
		print("\033[1;41m" + "simulation run: {}".format(i) + "\033[1;m")
		env = default_warehouse_4()
		env.show()
		
		time.sleep(0.5)
		os.system('clear')
	

if __name__ == '__main__':
	main()