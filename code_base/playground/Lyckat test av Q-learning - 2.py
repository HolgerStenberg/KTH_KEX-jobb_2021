import numpy


# Defining warehouse environment and available actions.
warehouse_rows = 3
warehouse_columns = 4
actions = ['left', 'right', 'up', 'down']

# Representation of the warehouse.
warehouse = numpy.full((warehouse_rows, warehouse_columns), "_")
warehouse[2, 0] = "a"
warehouse[0, 2] = "A"

warehouse[2, 2] = "b"
warehouse[0, 1] = "B"
warehouse[1, 2] = "X"

number_of_robots = 2

# Initiating empty Q-table.
q_value_table = numpy.zeros((warehouse_rows, warehouse_columns, len(actions)**number_of_robots))

# Mapping environment rewards.
reward_table_a = numpy.full((warehouse_rows, warehouse_columns), -1.)
reward_table_a[0, 2] = 100
reward_table_a[1, 2] = -100

reward_table_b = numpy.full((warehouse_rows, warehouse_columns), -1.)
reward_table_b[0, 1] = 100
reward_table_b[1, 2] = -100


def terminal_state(location_a, location_b):
    # The simulation is ended when the agent reaches a terminal state.
    X = reward_table_a[location_a[0], location_a[1]]
    Y = reward_table_b[location_b[0], location_b[1]]
    if X == -1 and Y == -1:
        return False
    else:
        return True


def collision(location_a, location_b):
    if location_a == location_b:
        return True
    else:
        return False


def next_action(location_a, location_b, epsilon):
    # numpy.random.random() generates a value between 0-1. If this value is greater than epsilon,
    if numpy.random.random() < epsilon:
        # numpy.argmax returns index of the greatest Q-value at the given point (1 of 4 actions).
        action_a = numpy.nanargmax(q_value_table_a[location_a[0], location_a[1]])
        action_b = numpy.nanargmax(q_value_table_b[location_b[0], location_b[1]])
        return action_a, action_b
    else:
        # If else, the next action is random and is seen as an exploration move.
        action_a = numpy.random.randint(4)
        action_b = numpy.random.randint(4)
        return action_a, action_b


def next_location(location, action):
    next_location = location
    # The agent can only move up if it is not currently on the top row.
    if actions[action] == 'up' and location[0] > 0:
        next_location[0] -= 1
    # The agent can only move right if it is not currently on the last column to the right.
    elif actions[action] == 'right' and location[1] < warehouse_columns - 1:
        next_location[1] += 1
    # The agent can only move down if it is not currently on the bottom row.
    elif actions[action] == 'down' and location[0] < warehouse_rows - 1:
        next_location[0] += 1
    # The agent can only move left if it is not currently on the last column to the left.
    elif actions[action] == 'left' and location[1] > 0:
        next_location[1] -= 1

    return next_location


def show_shortest_path():
    location_a = [2, 0]
    location_b = [2, 2]
    shortest_path_a = []
    shortest_path_b = []
    shortest_path_a.append(location_a)
    shortest_path_b.append(location_b)
    while not terminal_state(location_a, location_b) and not collision(location_a, location_b):
        # The best action to take, as calculated from the Q-table. Note that epsilon=1.
        [action_index_a, action_index_b] = next_action(location_a, location_b, 1)
        # Moves to the next location, and appends the new location to the list.
        location_a = next_location(location_a, action_index_a)
        location_b = next_location(location_b, action_index_b)
        shortest_path_a.append(location_a)
        shortest_path_b.append(location_b)
    return shortest_path_a, shortest_path_b


def training():
    # define training parameters
    epsilon = 0.9  # the percentage of time when we should take the best action (instead of a random action)
    discount_factor = 0.9  # discount factor for future rewards
    learning_rate = 0.9  # the rate at which the AI agent should learn

    # run through 1000 training episodes
    for episode in range(1000):
        # get the starting location for this episode
        location_a = [2, 0]
        location_b = [2, 2]
        # continue taking actions (i.e., moving) until we reach a terminal state
        # (i.e., until we reach the item packaging area or crash into an item storage location)
        while not terminal_state(location_a, location_b):
            # choose which action to take (i.e., where to move next)
            collided = collision(location_a, location_b)
            [action_index_a, action_index_b] = next_action(location_a, location_b, epsilon)

            # perform the chosen action, and transition to the next state (i.e., move to the next location)
            old_location_a = location_a  # store the old row and column indexes
            old_location_b = location_b
            location_a = next_location(location_a, action_index_a)
            location_b = next_location(location_b, action_index_b)

            # receive the reward for moving to the new state, and calculate the temporal difference
            if collided:
                reward_a = -100
                reward_b = -100
            else:
                reward_a = reward_table_a[location_a[0], location_a[1]]
                reward_b = reward_table_b[location_b[0], location_b[1]]

            old_q_value_a = q_value_table_a[old_location_a[0], old_location_a[1], action_index_a]
            old_q_value_b = q_value_table_b[old_location_b[0], old_location_b[1], action_index_b]
            temp_diff_a = reward_a + (discount_factor * numpy.max(q_value_table_a[location_a[0], location_a[1]])) - old_q_value_a
            temp_diff_b = reward_b + (discount_factor * numpy.max(q_value_table_b[location_b[0], location_b[1]])) - old_q_value_b

            # update the Q-value for the previous state and action pair
            new_q_value_a = old_q_value_a + (learning_rate * temp_diff_a)
            new_q_value_b = old_q_value_b + (learning_rate * temp_diff_b)
            q_value_table_a[old_location_a[0], old_location_a[1], action_index_a] = new_q_value_a
            q_value_table_b[old_location_b[0], old_location_b[1], action_index_b] = new_q_value_b


def main():
    print("\nBelow is a representation of the warehouse.")
    print("\n", warehouse[0, :], "\n", warehouse[1, :],"\n", warehouse[2, :])
    print("\n\nBelow is a representation of the reward table.\n\n", reward_table_a, "\n\n", reward_table_b)
    training()
    paths = show_shortest_path()
    print("\n\nThe shortest path for robot a  is: ", paths[0])
    print("\n\nThe shortest path for robot b  is: ", paths[1])
    print("\n\nQ-table (robot a) after training (1000 simulations):\n\n", q_value_table_a)
    print("\n\nQ-table (robot b) after training (1000 simulations):\n\n", q_value_table_b)


main()
