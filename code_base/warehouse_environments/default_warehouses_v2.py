from warehouse_environments import *
from warehouse_environments.warehouse_v2 import Warehouse


def default_warehouse_0():


	obj = Warehouse(5,5)

	obj.obstacle_line("right",1,1,5)
	obj.obstacle_line("right",5,1,5)
	obj.obstacle_line("down",2,1,3)
	obj.obstacle_line("down",2,5,3)

	return obj



def default_warehouse_1():


	obj = Warehouse(5,7)

	obj.obstacle_line("right",1,1,7)
	obj.obstacle_line("right",5,1,7)
	obj.obstacle_line("down",2,1,3)
	obj.obstacle_line("down",2,4,3)
	obj.obstacle_line("down",2,7,3)

	return obj



def default_warehouse_2():


	obj = Warehouse(5,6)

	obj.obstacle_line("right",1,1,6)
	obj.obstacle_line("right",5,1,6)
	obj.obstacle_line("down",2,1,3)
	obj.obstacle_line("down",2,6,3)

	return obj

def default_warehouse_3():


	obj = Warehouse(5,5)

	obj.obstacle_line("right",1,1,5)
	obj.obstacle_line("right",2,2,2)
	obj.obstacle_line("right",4,2,2)
	obj.obstacle_line("right",5,1,5)
	obj.obstacle_line("down",2,1,3)
	obj.obstacle_line("down",2,5,3)

	return obj

def default_warehouse_4():


	obj = Warehouse(7,8)

	obj.obstacle_line("right",1,1,8)
	obj.obstacle_line("right",7,1,8)
	obj.obstacle_line("left",3,7,2)
	obj.obstacle_line("left",5,7,2)
	obj.obstacle_line("down",2,1,5)
	obj.obstacle_line("down",2,8,5)

	return obj


def main():
	obj = default_warehouse_3
	obj.show()
if __name__ == '__main__':
	main()
