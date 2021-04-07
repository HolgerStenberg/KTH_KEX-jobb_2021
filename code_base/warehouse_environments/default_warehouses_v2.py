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

