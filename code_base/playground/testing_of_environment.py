import sys
sys.path.append('../')

from warehouse_environments.warehouse import Warehouse
from warehouse_environments.warehouse_johan import *
from warehouse_environments.default_warehouses import *

def main():

	#get_warehouse(10,10,4)

	env = default_warehouse_1()

	env.show()

if __name__ == '__main__':
	main()