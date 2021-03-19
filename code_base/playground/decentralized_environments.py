import numpy as np


def environment_4x4():
    environment_rewards = np.full((4, 4), -0.1)
    environment_rewards[1, 1:4],  environment_rewards[3, 2] = -1, -1

    environment = np.full((4, 4), ".")
    environment[1, 1:4], environment[3, 2] = "X", "X"
    return environment_rewards, environment


def environment_6x6():
    environment_rewards = np.full((6, 6), -0.1)
    environment_rewards[1, 0:2] = -1
    environment_rewards[4:7, 2] = -1
    environment_rewards[2, 4:7] = -1

    environment = np.full((6, 6), ".")
    environment[1, 0:2] = "X"
    environment[4:7, 2] = "X"
    environment[2, 4:7] = "X"
    return environment_rewards, environment


def environment_8x8():
    environment_rewards = np.full((8, 8), -0.1)
    environment_rewards[2, 4:8], environment_rewards[2:6, 4] = -1, -1
    environment_rewards[1, 1:3], environment_rewards[4:7, 1] = -1, -1

    environment = np.full((8, 8), ".")
    environment[2, 4:8], environment[2:6, 4] = "X", "X"
    environment[1, 1:3], environment[4:7, 1] = "X", "X"
    return environment_rewards, environment


def environment_10x10():
    environment_rewards = np.full((10, 10), -0.1)
    environment_rewards[1:3, 3:7], environment_rewards[6:8, 7:9] = -1, -1
    environment_rewards[3:6, 1], environment_rewards[6:10, 4] = -1, -1

    environment = np.full((10, 10), ".")
    environment[1:3, 3:7], environment[6:8, 7:9] = "X", "X"
    environment[3:6, 1], environment[6:10, 4] = "X", "X"
    return environment_rewards, environment


def choose_environment(choice):
    if choice == 4:
        return environment_4x4()

    if choice == 6:
        return environment_6x6()

    if choice == 8:
        return environment_8x8()

    if choice == 10:
        return environment_10x10()
