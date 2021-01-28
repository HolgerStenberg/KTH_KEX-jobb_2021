import numpy


# Defining warehouse environment and available actions.
warehouse_rows = 3
warehouse_columns = 4
actions = ['left', 'right', 'up', 'down']

# Representation of the warehouse.
warehouse = numpy.full((warehouse_rows, warehouse_columns), "_")
warehouse[2, 0] = "S"
warehouse[0, 2] = "G"
warehouse[1, 1:3] = "X"

# Initiating empty Q-table.
q_value_table = numpy.zeros((warehouse_rows, warehouse_columns, len(actions)))

# Mapping environment rewards.
reward_table = numpy.full((warehouse_rows, warehouse_columns), -1.)
reward_table[0, 2] = 100
reward_table[1, 1:3] = -100


def terminal_state(current_row, current_column):
    # The simulation is ended when the agent reaches a terminal state.
    if reward_table[current_row, current_column] == -1:
        return False
    else:
        return True


def next_action(current_row, current_column, epsilon):
    # numpy.random.random() generates a value between 0-1. If this value is less than epsilon,
    if numpy.random.random() < epsilon:
        # numpy.argmax returns index of the greatest Q-value at the given point (1 of 4 actions).
        return numpy.argmax(q_value_table[current_row, current_column])
    else:
        # If else, the next action is random and is seen as an exploration move.
        return numpy.random.randint(4)


def next_location(current_row, current_column, action):
    new_row = current_row
    new_column = current_column
    # The agent can only move up if it is not currently on the top row.
    if actions[action] == 'up' and current_row > 0:
        new_row -= 1
    # The agent can only move right if it is not currently on the last column to the right.
    elif actions[action] == 'right' and current_column < warehouse_columns - 1:
        new_column += 1
    # The agent can only move down if it is not currently on the bottom row.
    elif actions[action] == 'down' and current_row < warehouse_rows - 1:
        new_row += 1
    # The agent can only move left if it is not currently on the last column to the left.
    elif actions[action] == 'left' and current_column > 0:
        new_column -= 1
    return new_row, new_column


def show_shortest_path(current_row=2, current_column=0):
    shortest_path = []
    shortest_path.append([current_row, current_column])
    while not terminal_state(current_row, current_column):
        # The best action to take, as calculated from the Q-table. Note that epsilon=1.
        action = next_action(current_row, current_column, 1)
        # Moves to the next location, and appends the new location to the list.
        current_row, current_column = next_location(current_row, current_column, action)
        shortest_path.append([current_row, current_column])
    return shortest_path


def training():
    # define training parameters
    epsilon = 0.9  # the percentage of time when we should take the best action (instead of a random action)
    discount_factor = 0.9  # discount factor for future rewards
    learning_rate = 0.9  # the rate at which the AI agent should learn

    # run through 1000 training episodes
    for episode in range(1000):
        # get the starting location for this episode
        row_index, column_index = 2, 0

        # continue taking actions (i.e., moving) until we reach a terminal state
        # (i.e., until we reach the item packaging area or crash into an item storage location)
        while not terminal_state(row_index, column_index):
            # choose which action to take (i.e., where to move next)
            action_index = next_action(row_index, column_index, epsilon)

            # perform the chosen action, and transition to the next state (i.e., move to the next location)
            old_row_index, old_column_index = row_index, column_index  # store the old row and column indexes
            row_index, column_index = next_location(row_index, column_index, action_index)

            # receive the reward for moving to the new state, and calculate the temporal difference
            reward = reward_table[row_index, column_index]
            old_q_value = q_value_table[old_row_index, old_column_index, action_index]
            temp_diff = reward + (discount_factor * numpy.max(q_value_table[row_index, column_index])) - old_q_value

            # update the Q-value for the previous state and action pair
            new_q_value = old_q_value + (learning_rate * temp_diff)
            q_value_table[old_row_index, old_column_index, action_index] = new_q_value


def main():
    print("\nBelow is a representation of the warehouse.")
    print("\n", warehouse[0, :], "\n", warehouse[1, :],"\n", warehouse[2, :])
    print("\n\nBelow is a representation of the reward table.\n\n", reward_table)
    training()
    print("\n\nThe shortest path is: ", show_shortest_path())
    print("\n\nQ-table after training (1000 simulations):\n\n", q_value_table)


main()
