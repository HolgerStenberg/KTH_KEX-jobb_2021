import numpy
from code_base.warehouse_environments.default_warehouses import default_warehouse_2, default_warehouse_1


def get_environment():
    number_of_robots = int(input("Input number of robots (1-4): "))
    if number_of_robots == 1:
        environment = default_warehouse_1()
        environment = numpy.array(environment.matrix)
        return environment, number_of_robots
    if number_of_robots == 2:
        environment = default_warehouse_2()
        environment = numpy.array(environment.matrix)
        return environment, number_of_robots
    else:
        print("Not implemented yet.")


def get_reward_table(environment, number_of_robots):
    flat_env = environment.flatten()

    if number_of_robots == 1:
        print("")
        reward_table = numpy.full((len(flat_env), 1), -1.)
        for a in range(len(flat_env)):
            if flat_env[a] == 'H':
                print("Env Col.", a)
                reward_table[a] = -100
            elif flat_env[a] == 'A':
                print("GOAL!", a)
                reward_table[a] = 100
        return reward_table

    if number_of_robots == 2:
        print("")
        reward_table = numpy.full((len(flat_env), len(flat_env)), -1.)
        for a in range(len(flat_env)):
            for b in range(len(flat_env)):
                if a == b:
                    # print("Rob Col.", a, b)
                    reward_table[a, b] = -100
                elif flat_env[a] == 'H' or flat_env[b] == 'H':
                    # print("Env Col.", a, b)
                    reward_table[a, b] = -100
                elif flat_env[a] == "A" and flat_env[b] == "B":
                    # print("GOAL!", a, b)
                    reward_table[a, b] = 100
        return reward_table

    else:
        pass


def main():
    environment, number_of_robots = get_environment()
    print("\n", environment)

    flat_env = environment.flatten()
    print("\n", flat_env)

    reward_table = get_reward_table(flat_env, number_of_robots)
    print("\n", reward_table)


main()
