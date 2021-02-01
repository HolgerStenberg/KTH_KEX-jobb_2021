import sys
sys.path.append('../')

from warehouse_environments.warehouse import Warehouse
from warehouse_environments.default_warehouses import *

def main():


	env = Warehouse(5,5)

	env.matrix_fill(5,5)
	env.obstacle_line("right",1,1,6)

	env.show()

if __name__ == '__main__':
	main()