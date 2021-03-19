import numpy as np
import string

actions = ['left', 'right', 'up', 'down', 'stay']


class Robot:
    def __init__(self, identity, current_position, target_position, environment, actions):
        self.starting_position = [int(current_position[0]), int(current_position[1])]
        self.current_position = self.starting_position
        self.target_position = [int(target_position[0]), int(target_position[1])]
        self.Q_table = np.zeros(shape=(len(environment.flatten()), len(actions)))
        self.disengaged = False
        self.ID = identity


def place_robots(number_of_robots, environment):
    robot_vector = []

    for i in range(number_of_robots):
        prompt1 = "Input starting position for robot"
        prompt2 = "(x *space* y): "
        prompt3 = "Input target position for robot"
        starting_position = input('{} {} {}'.format(prompt1, string.ascii_lowercase[i], prompt2)).split()
        target_position = input('{} {} {}'.format(prompt3, string.ascii_lowercase[i], prompt2)).split()

        environment[1][int(starting_position[0]), int(starting_position[1])] = string.ascii_lowercase[i]
        environment[1][int(target_position[0]), int(target_position[1])] = string.ascii_uppercase[i]
        environment[0][int(target_position[0]), int(target_position[1])] = 1

        robot = Robot(string.ascii_lowercase[i], starting_position, target_position, environment[0], actions)
        robot_vector.append(robot)

    return robot_vector, environment
