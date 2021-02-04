import numpy
import random
from warehouse import Warehouse


def get_warehouse(rows, columns, number_of_agents):
    # Defining warehouse environment.
    # 0 = floor
    # 1 = shelves
    # n + 1 = starting point for robot n. (n > 0)
    # n + 2 = ending point for robot n.

    #environment = numpy.full((rows, columns), 0)
    environment = Warehouse(10,10)
    # Generate starting points.
    occupied_states = []
    for n in range(number_of_agents):

        row_start = random.randint(0, rows - 1)
        col_start = random.randint(0, columns - 1)
        row_end = random.randint(0, rows - 1)
        col_end = random.randint(0, columns - 1)

      #  while [[row_start, col_start]] or [[row_end, col_end]] in occupied_states:

           # [row_start, col_start] = [random.randint(0, rows - 1), random.randint(0, columns - 1)]
           # [row_end, col_end] = [random.randint(0, rows - 1), random.randint(0, columns - 1)]

        environment[row_start, col_start] = 2*n+2
        environment[row_end, col_end] = 2*n+3
       # occupied_states.append([row_start, col_start])
       # occupied_states.append([row_end, col_end])

    return environment
