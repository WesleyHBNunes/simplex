import numpy as np


def simplex(matrix, coefficients, b, base, basics, no_basics, lines):
    iteration = 0
    solved = False

    while not solved:
        iteration += 1
        print(str(iteration) + "ª iteration")
        base_inverted = base.I
        print("Base inverted:\n " + str(base_inverted))
        value_variables = np.matmul(base_inverted, b)
        print("Variables Values (b): " + str(value_variables))
        cb = create_cb(basics, coefficients)
        print("Coefficients basics (cb): " + str(cb))

        value_objective_function = np.matmul(np.matmul(cb, base_inverted), b)
        print("Value of partial objective function: " + str(value_objective_function))

        variable_go_base, lowest_reduced_cost, index_variable_go_base = calculate_reduced_coasts(
            matrix, no_basics, coefficients, cb, base_inverted, lines)

        if lowest_reduced_cost >= 0:
            print()
            print("Objective Function Value: " + str(value_objective_function))
            print("Value of basics variables (b): " + str(value_variables))
            print("Basics: " + str(basics))
            print("No basics: " + str(no_basics))
            solved = True
            continue

        direction_vectors = calculate_direction_vectors(matrix, base_inverted, no_basics, lines)

        direction_vector_variable_go_base = direction_vectors[index_variable_go_base]

        variable_out_of_base = calculate_the_lowest_theta(direction_vector_variable_go_base, value_variables,
                                                          basics, lines)

        print("Go out to base: (x" + str(basics[variable_out_of_base]) + ")")
        print("Go to the base: (x" + str(variable_go_base) + ")")
        base, basics, no_basics = updated_base_basics_no_basics(matrix, base, basics, no_basics, variable_go_base,
                                                                index_variable_go_base, variable_out_of_base, lines)

        print("New base: \n" + str(base))
        print("New basics variables: " + str(basics))
        print("New no basics variables: " + str(no_basics))
        print()


def create_cb(basics, coefficients):
    cb = []
    for i in basics:
        cb.append(coefficients[i])
    return cb


def calculate_reduced_coasts(matrix, no_basics, coefficients, cb, base_inverted, lines):
    reduced_cost = []
    lowest_reduced_cost = (np.inf, -1)
    variable_go_base = -1,
    iteration = -1
    index_variable_go_base = iteration
    for i in no_basics:
        iteration += 1
        aj = return_aj(matrix, lines, i)
        result = coefficients[i] - np.matmul(np.matmul(cb, base_inverted), aj)
        print("Reduced Coast (x" + str(i) + "): " + str(result))
        reduced_cost.append(result[0, 0])
        if result < lowest_reduced_cost[0]:
            lowest_reduced_cost = result
            variable_go_base = i
            index_variable_go_base = iteration
    return variable_go_base, lowest_reduced_cost, index_variable_go_base


def calculate_direction_vectors(matrix, base_inverted, no_basics, lines):
    direction_vectors = []

    for i in no_basics:
        aj = return_aj(matrix, lines, i)
        print("Vector direction of variable (x" + str(i) + "): " + str(np.matmul(base_inverted, aj)))
        direction_vectors.append(np.matmul(base_inverted, aj))
    return direction_vectors


def calculate_the_lowest_theta(direction_vector_variable_go_base, value_variables, basics, lines):
    variable_out_of_base = 0
    lowest_result = np.inf

    for i in range(lines):
        if direction_vector_variable_go_base[0, i] > 0:
            result = value_variables[0, i] / direction_vector_variable_go_base[0, i]

            print("Theta x(" + str(basics[i]) + "): " + str(value_variables[0, i]) + "/" +
                  str(direction_vector_variable_go_base[0, i]) + " -> " + str(result))
            if result < lowest_result:
                lowest_result = result
                variable_out_of_base = i
        else:
            print("Theta x(" + str(basics[i]) + "): " + str(value_variables[0, i]) + "/" +
                  str(direction_vector_variable_go_base[0, i]) + " -> " + "Infinity")
    return variable_out_of_base


def updated_base_basics_no_basics(matrix, base, basics, no_basics, variable_go_base, index_variable_go_base,
                                  variable_out_of_base, lines):
    aux = basics[variable_out_of_base]
    basics[variable_out_of_base] = variable_go_base
    no_basics[index_variable_go_base] = aux

    for i in range(lines):
        base[i, variable_out_of_base] = matrix[i, basics[variable_out_of_base]]
    return base, basics, no_basics


def return_aj(matrix, lines, variable):
    aj = []
    for j in range(lines):
        aj.append(matrix[j, variable])
    return aj


if __name__ == '__main__':

    # simplex(np.matrix([[4, 6, 1, 0, 0], [4, 2, 0, 1, 0], [0, 1, 0, 0, 1]]),
    #         [-80, -60, 0, 0, 0], [24, 16, 3], np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
    #         [2, 3, 4], [0, 1], 3)

    # simplex(np.matrix([[1, -2, 1, 0, 0], [-2, 1, 0, 1, 0], [5, 3, 0, 0, 1]]),
    #         [-1, -3, 0, 0, 0], [0, 4, 15], np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
    #         [2, 3, 4], [0, 1], 3)

    # simplex(np.matrix([[1, 1, 1, 0], [3, 2, 0, 1]]),
    #         [-2, -4, 0, 0], [3, 14], np.matrix([[1, 0], [0, 1]]),
    #         [2, 3], [0, 1], 2)

    # simplex(np.matrix([[1.5, 4, 1, 0, 0], [3, 1.5, 0, 1, 0], [1, 1, 0, 0, 1]]),
    #         [-6, -6, 0, 0, 0], [24, 21, 8], np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
    #        [2, 3, 4], [0, 1], 3)

    # simplex(np.matrix([[1, 1, 1, 0, 0], [1, -1, 0, 1, 0], [-1, 1, 0, 0, 1]]),
    #         [-1, -1, 0, 0, 0], [6, 4, 4], np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
    #         [2, 3, 4], [0, 1], 3)

    simplex(np.matrix([[1, -4, 1, 0, 0, 0], [-2, 1, 0, 1, 0, 0], [-3, 4, 0, 0, 1, 0], [2, 1, 0, 0, 0, 1]]),
            [-1, -2, 0, 0, 0, 0], [4, 2, 12, 8], np.matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]),
            [2, 3, 4, 5], [0, 1], 4)