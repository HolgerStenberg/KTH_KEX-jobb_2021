import numpy
from code_base.warehouse_environments.default_warehouses import *

action_possibles = ['left', 'right', 'up', 'down', 'stay']
actions = ['left', 'right', 'up', 'down', 'stay']
for i in action_possibles:
    for j in action_possibles:
        actions.append(i+j)


def get_environment():
    number_of_robots = int(input("Input number of robots (1-4): "))
    if number_of_robots == 1:
        environment = default_warehouse_1()
        number_of_columns = len(environment.matrix[0])
        environment = numpy.array(environment.matrix)
        return environment, number_of_robots, number_of_columns
    if number_of_robots == 2:
        environment = default_warehouse_2()
        number_of_columns = len(environment.matrix[0])
        environment = numpy.array(environment.matrix)
        return environment, number_of_robots, number_of_columns
    else:
        print("Not implemented yet.")


def get_reward_table(environment, number_of_robots):
    flat_env = environment.flatten()
    terminal_states=[]
    if number_of_robots == 1:
        print("")
        reward_table = numpy.full((len(flat_env), 1), -1.)
        start_state = [None]
        for a in range(len(flat_env)):
            if flat_env[a] == 'a':
                start_state[0] = a
            if flat_env[a] == 'H':
                # print("Env Col.", a)
                reward_table[a] = -100
                terminal_states.append([a])
            elif flat_env[a] == 'A':
                # print("GOAL!", a)
                reward_table[a] = 100
                terminal_states.append([a])
        return reward_table, start_state, terminal_states

    if number_of_robots == 2:
        print("")
        reward_table = numpy.full((len(flat_env), len(flat_env)), -1.)
        start_state = [None, None]
        for a in range(len(flat_env)):
            for b in range(len(flat_env)):
                if flat_env[a] == 'a':
                    start_state[0] = a
                if flat_env[b] == 'b':
                    start_state[1] = b
                if a == b:
                    # print("Rob Col.", a, b)
                    reward_table[a, b] = -100
                    terminal_states.append([a, b])
                elif flat_env[a] == 'H' or flat_env[b] == 'H':
                    # print("Env Col.", a, b)
                    reward_table[a, b] = -100
                    terminal_states.append([a, b])
                elif flat_env[a] == "A" and flat_env[b] == "B":
                    # print("GOAL!", a, b)
                    reward_table[a, b] = 100
                    terminal_states.append([a, b])
        return reward_table, start_state, terminal_states

    else:
        pass


def get_q_table(reward_table, number_of_robots):
    flat_rew = reward_table.flatten()
    actions = 5**number_of_robots
    q_table = numpy.full((len(flat_rew), actions), 0)
    return q_table


def next_action(current_state, epsilon, q_table):
    # numpy.random.random() generates a value between 0-1. If this value is less than epsilon,
    if numpy.random.random() < epsilon:
        # numpy.argmax returns index of the greatest Q-value at the given point (1 of 4 actions).
        return numpy.argmax(q_table[current_state])
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


def training(current_state, terminal_states, q_table, reward_table):
    # define training parameters
    epsilon = 0.9  # the percentage of time when we should take the best action (instead of a random action)
    discount_factor = 0.9  # discount factor for future rewards
    learning_rate = 0.9  # the rate at which the AI agent should learn

    # run through 1000 training episodes
    for simulation in range(1000):

        # continue taking actions (i.e., moving) until we reach a terminal state
        # (i.e., until we reach the item packaging area or crash into an item storage location)
        while current_state not in terminal_states:
            # choose which action to take (i.e., where to move next)
            action_index = next_action(current_state, epsilon, q_table)

            # perform the chosen action, and transition to the next state (i.e., move to the next location)
            old_state = current_state  # store the old row and column indexes
            current_state = next_location(current_state, action_index)

            # receive the reward for moving to the new state, and calculate the temporal difference
            reward = reward_table[current_state]
            old_q_value = q_table[old_state, action_index]
            temp_diff = reward + (discount_factor * numpy.max(q_table[current_state])) - old_q_value

            # update the Q-value for the previous state and action pair
            new_q_value = old_q_value + (learning_rate * temp_diff)
            q_table[old_state, action_index] = new_q_value


def main():
    environment, number_of_robots, number_of_columns = get_environment()
    print("\n", environment)

    # flat_env = environment.flatten()
    # print("\n", flat_env)

    reward_table, start_state, terminal_states = get_reward_table(environment, number_of_robots)
    print("\n", reward_table)

    # Each row in the Q-table is a state, each column a set och actions [(0,0), (0,1), ...]
    q_table = get_q_table(reward_table, number_of_robots)
    print("\n", q_table)

    print(start_state)
    print(terminal_states)


main()
