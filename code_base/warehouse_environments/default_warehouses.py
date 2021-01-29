from warehouse import Warehouse



def default_warehouse_1():

	row_q = 15
	col_q = 15

	env = Warehouse(row_q,col_q)

	for i in range(row_q):
		if i%4 == 0:
			env.obstacle_line("right",i, 0, 4)
			env.obstacle_line("left",i,-1,4)


	return env

def default_warehouse_2():

	row_q = 10
	col_q = 10

	env = Warehouse(row_q,col_q)

	for i in range(row_q):
		if i%4 == 0:
			env.obstacle_line("right",i, 0, 4)
			env.obstacle_line("left",i,-1,4)



	return env

