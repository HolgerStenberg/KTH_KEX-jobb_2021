from code_base.warehouse_environments import *
from code_base.warehouse_environments.warehouse import Warehouse


def default_warehouse_1():


	obj = Warehouse(5,5)
	obj.add_agent(2,2,4,4)
	obj.add_agent(2,4,4,2)

	obj.obstacle_line("down",3,3,1)
	obj.obstacle_line("right",1,1,5)
	obj.obstacle_line("right",5,1,5)
	obj.obstacle_line("down",2,1,3)
	obj.obstacle_line("down",2,5,3)

	obj.set_start_state()
	
	return obj

def default_warehouse_2():

	obj = Warehouse(7,7)
	obj.add_agent(2,2,2,4)
	obj.add_agent(6,2,6,4)
	obj.add_agent(2,6,5,4)

	obj.obstacle_line("down",4,5,3)
	obj.obstacle_line("right",1,1,7)
	obj.obstacle_line("right",7,1,7)
	obj.obstacle_line("down",2,1,5)
	obj.obstacle_line("down",2,7,5)

	obj.set_start_state()
	
	return obj

def default_warehouse_3():

	row_q = 8
	col_q = 8
	env = Warehouse(row_q,col_q)

	env.obstacle_line("up",8,3,4)
	env.obstacle_line("up",8,6,2)
	env.obstacle_line("down",1,5,2)
	env.obstacle_line("down",1,8,3)
	env.matrix_fill(1,2)
	env.matrix_fill(4,6)


	env.add_agent(7,2,8,8)
	env.add_agent(8,5,1,1)
	env.add_agent(1,4,1,7)

	env.set_start_state()
	
	return env

def default_warehouse_4():

	row_q = 10
	col_q = 10
	env = Warehouse(row_q,col_q)

	env.obstacle_line("right",1,1,3)
	env.obstacle_line("right",4,1,3)
	env.obstacle_line("right",8,1,3)

	env.matrix_fill(6,5)

	env.obstacle_line("left",3,10,4)
	env.obstacle_line("left",6,10,4)
	env.obstacle_line("left",10,10,4)


	env.add_agent(1,10,7,1)
	env.add_agent(1,5,5,10)
	env.add_agent(10,2,4,9)
	env.add_agent(2,1,8,8)
	
	return env

			

