from warehouse_environments.warehouse import Warehouse

def default_warehouse_1():

	row_q = 4
	col_q = 4
	env = Warehouse(row_q,col_q)

	env.obstacle_line("right",3, 2, 2)
	env.add_agent(1,4,4,1)
	
	return env

def default_warehouse_2():

	row_q = 6
	col_q = 6
	env = Warehouse(row_q,col_q)

	env.obstacle_line("right",4,1,3)
	env.obstacle_line("left",1,6,3)

	env.add_agent(1,1,6,1)
	env.add_agent(6,6,1,2)

	return env

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

			

