from warehouse import Warehouse

def default_warehouse_1():

	row_q = 6
	col_q = 6

	env = Warehouse(row_q,col_q)

	for i in range(row_q):
		if i%3 == 0:
			env.obstacle_line("right",i+1, 1, 3)
			#env.obstacle_line("left",i,-1,4)
	env.matrix_fill(1,6,"a")
	env.matrix_fill(5,6,"b")


	env.matrix_fill(5,1,"A")
	env.matrix_fill(2,1,"B")


	return env

def default_warehouse_2():

	row_q = 5
	col_q = 5

	env = Warehouse(row_q,col_q)

	for i in range(row_q):
		if i%4 == 0:
			env.obstacle_line("right",i, 0, 6)
			env.obstacle_line("left",i,-1,4)

	return env

