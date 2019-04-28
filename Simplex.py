import numpy as np


def simplex(matrix, coefficients, b, base, basics, no_basics, lines):

    while True:
        base_inverted = base.I
        print("Base inverted: " + str(base_inverted))
        value_variables = np.matmul(base_inverted, b)
        print("Variables Values: " + str(value_variables))
        cb = []
        for i in basics:
            cb.append(coefficients[i])
        print("cb: " + str(cb))

        value_objective_function = np.matmul(np.matmul(cb, base_inverted), b)
        print("Value of partial objective function: " + str(value_objective_function))
        reduced_cost = []
        for i in no_basics:
            aj = []
            for j in range(lines):
                aj.append(matrix[j, i])
            result = coefficients[i] - np.matmul(np.matmul(cb, base_inverted), aj)
            reduced_cost.append(result[0, 0])
        print("Reduced Coast: " + str(reduced_cost))

        lowest_reduced_cost = min(reduced_cost)
        if lowest_reduced_cost >= 0:
            print()
            print("Objective Function Value: " + str(value_objective_function))
            print("Value of basics variables: " + str(value_variables))
            print("Basics: " + str(basics))
            print("No basics: " + str(no_basics))
            break

        variable_go_base = -1
        for i in range(len(reduced_cost)):
            if reduced_cost[i] == lowest_reduced_cost:
                variable_go_base = i

        direction_vectors = []
        for i in no_basics:
            aj = []
            for j in range(lines):
                aj.append(matrix[j, i])
            print("Vector direction of variable " + str(i) + ": " + str(np.matmul(base_inverted, aj)))
            direction_vectors.append(np.matmul(base_inverted, aj))

        direction_vector_variable_go_base = direction_vectors[variable_go_base]
        variable_out_of_base = 0
        lowest_result = np.inf
        for i in range(lines):
            if direction_vector_variable_go_base[0, i] > 0:
                result = value_variables[0, i] / direction_vector_variable_go_base[0, i]
                if result < lowest_result:
                    lowest_result = result
                    variable_out_of_base = i

        print("Go out to base: " + str(basics[variable_out_of_base]))
        print("Go to the base: " + str(variable_go_base))
        aux = basics[variable_out_of_base]
        basics[variable_out_of_base] = variable_go_base
        no_basics[variable_go_base] = aux

        for i in range(lines):
            base[i, variable_out_of_base] = matrix[i, basics[variable_out_of_base]]
        print()


# simplex(np.matrix([[4, 6, 1, 0, 0], [4, 2, 0, 1, 0], [0, 1, 0, 0, 1]]),
#         [-80, -60, 0, 0, 0], [24, 16, 3], np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
#         [2, 3, 4], [0, 1], 3)


simplex(np.matrix([[1, -2, 1, 0, 0], [-2, 1, 0, 1, 0], [5, 3, 0, 0, 1]]),
        [-1, -3, 0, 0, 0], [0, 4, 15], np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
        [2, 3, 4], [0, 1], 3)
