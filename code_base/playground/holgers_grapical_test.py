import sys
import os
import time
import numpy as np

from code_base.warehouse_environments.default_warehouses import default_warehouse_3, default_warehouse_4

sys.path.append('../')


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