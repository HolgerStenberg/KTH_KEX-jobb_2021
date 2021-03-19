import decentralized_robots
import decentralized_environments
import numpy
import string

actions = ['left', 'right', 'up', 'down', "stay"]


def coord_to_ind(x, y, env_size):
    return env_size * x + y


def next_action(robot, epsilon, env_size):
    # numpy.random.random() generates a value between 0-1. If this value is less than epsilon,
    x = robot.current_position[0]
    y = robot.current_position[1]
    index = coord_to_ind(x, y, env_size)
    if numpy.random.random() < epsilon:
        # numpy.argmax returns index of the greatest Q-value at the given point (1 of 4 actions).
        return numpy.argmax(robot.Q_table[index])
    else:
        # If else, the next action is random and is seen as an exploration move.
        return numpy.random.randint(5)


def next_location(robot, action, environment_size):
    x = robot.current_position[0]
    y = robot.current_position[1]
    wall_collision = False

    # The agent can only move up if it is not currently on the top row.
    if actions[action] == 'up' and x > 0:
        x -= 1
    # The agent can only move right if it is not currently on the last column to the right.
    elif actions[action] == 'right' and y < environment_size - 1:
        y += 1
    # The agent can only move down if it is not currently on the bottom row.
    elif actions[action] == 'down' and x < environment_size - 1:
        x += 1
    # The agent can only move left if it is not currently on the last column to the left.
    elif actions[action] == 'left' and y > 0:
        y -= 1

    elif actions[action] != 'stay':
        wall_collision = True

    return x, y, wall_collision


def update_table(robot, x, y, old_x, old_y, action_index, env_size, reward, learning_rate, discount_factor):
    old_index = coord_to_ind(old_x, old_y, env_size)
    old_q = robot.Q_table[old_index, action_index]

    new_index = coord_to_ind(x, y, env_size)
    temp_diff = reward + (discount_factor * numpy.max(robot.Q_table[new_index])) - old_q

    new_q = old_q + (learning_rate * temp_diff)
    robot.Q_table[old_index, action_index] = new_q

    return


def training(robot_vector, environment, env_size):
    epsilon = 0.7  # the percentage of time when we should take the best action (instead of a random action)
    discount_factor = 0.9  # discount factor for future rewards
    learning_rate = 0.5  # the rate at which the AI agent should learn

    # run through 1000 training episodes

    for episode in range(10000):
        disengaged_robots = []
        temp_env = environment
        for robot in robot_vector:
            robot.current_position = robot.starting_position
            robot.disengaged = False

        while len(disengaged_robots) < len(robot_vector):
            for robot in robot_vector:

                if robot.disengaged:
                    if robot.ID not in disengaged_robots:
                        disengaged_robots.append(robot.ID)
                    continue
                action_index = next_action(robot, epsilon, env_size)

                # perform the chosen action, and transition to the next state (i.e., move to the next location)
                old_x, old_y = robot.current_position[0], robot.current_position[1]
                # store the old row and column indexes
                x, y, wall_collision = next_location(robot, action_index, env_size)

                if wall_collision:
                    robot.disengaged = True
                    reward = -1
                    update_table(robot, x, y, old_x, old_y, action_index, env_size, reward, learning_rate,
                                 discount_factor)
                    continue

                temp_state = temp_env[1][x, y]

                if temp_state.islower():
                    robot.disengaged = True
                    reward = -1
                    update_table(robot, x, y, old_x, old_y, action_index, env_size, reward, learning_rate,
                                 discount_factor)
                    break

                robot.current_position[0], robot.current_position[1] = x, y

                if temp_env[1][x, y] == "X":
                    robot.disengaged = True
                    reward = temp_env[0][x, y]
                # receive the reward for moving to the new state, and calculate the temporal difference
                elif robot.current_position == robot.target_position:
                    reward = 1
                    robot.disengaged = True
                elif wall_collision:
                    reward = -1
                    robot.disengaged = True
                else:
                    reward = temp_env[0][x, y]

                update_table(robot, x, y, old_x, old_y, action_index, env_size, reward, learning_rate, discount_factor)

                temp_env[1][old_x, old_y] = "."
                temp_env[1][x, y] = robot.ID

                # print(temp_env[1], "   [", robot.current_position[0], ",", robot.current_position[1], "]", "\n")
    return robot_vector


def show_shortest_path(robot, env_size):
    shortest_path = []
    robot.current_position = robot.starting_position
    shortest_path.append(robot.current_position)
    while not robot.current_position != robot.target_position:
        # The best action to take, as calculated from the Q-table. Note that epsilon=1.
        action = next_action(robot, 1, env_size)
        # Moves to the next location, and appends the new location to the list.
        robot.current_position = next_location(robot, action, env_size)
        shortest_path.append(robot.current_position)

    return shortest_path


def main():
    environment_size = int(input("Input grid size (n in nxn, 4/6/8/10): "))
    environment = decentralized_environments.choose_environment(environment_size)
    print("\n", environment[1], "\n")

    number_of_robots = int(input("Input number of robots: "))
    robot_vector, environment = decentralized_robots.place_robots(number_of_robots, environment)
    print("\n", environment[1], "\n")

    robot_vector = training(robot_vector, environment, environment_size)

    inp = input("Input ID of robot and print Q-table: ")
    index = ord(inp)-97

    print("\n", robot_vector[index].Q_table)

    print("\n", "Shortest path for robot "+inp+":")
    print("\n", show_shortest_path(robot_vector[index], environment_size))


main()
