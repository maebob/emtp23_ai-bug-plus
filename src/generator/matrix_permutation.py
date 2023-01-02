from sympy.utilities.iterables import multiset_permutations

import numpy as np
from copy import deepcopy


def permutations(matrix: np.array):
    """
    This function creates all permutations of the given matries.
    Arguments:
        matrix: The matrices to create the permutations from.
    Returns:
        A list of all permutations of the given matrices."""
    all_permutations = []

    nr_columns_control_flow = matrix[0][0].size
    nr_rows_control_flow = (nr_columns_control_flow + 3) // 2

    list_rows_cf = np.arange(2, nr_rows_control_flow, dtype=int)

    for perm in multiset_permutations(list_rows_cf):
        copy_matrix = matrix
        control_flow = matrix[0]
        data_flow = matrix[1]
        swapped = True
        # kind of bubblesort
        while swapped:
            swapped = False
            for i in range(len(perm)-1):
                if perm[i] > perm[i+1]:
                    perm[i], perm[i+1] = perm[i+1], perm[i]
                    swapped = True

                    bugSwapped1 = list_rows_cf[i] - 1
                    bugSwapped2 = list_rows_cf[i+1] - 1

                    control_flow[[bugSwapped1 + 1, bugSwapped2 + 1]] = control_flow[[bugSwapped2 + 1, bugSwapped1 + 1]]
                    control_flow[:, [2*bugSwapped1-1, 2*bugSwapped2-1]] = control_flow[:, [2*bugSwapped2-1, 2*bugSwapped1-1]]
                    control_flow[:, [2*bugSwapped1, 2*bugSwapped2]] = control_flow[:, [2*bugSwapped2, 2*bugSwapped1]]

                    data_flow[:, [bugSwapped1+1, bugSwapped2+1]] = data_flow[:, [bugSwapped2+1, bugSwapped1+1]]
                    data_flow[[2*bugSwapped1-1, 2*bugSwapped2-1]] = data_flow[[2*bugSwapped2-1, 2*bugSwapped1-1]]
                    data_flow[[2 * bugSwapped1, 2 * bugSwapped2]] = data_flow[[2 * bugSwapped2, 2 * bugSwapped1]]
        # create an array that contains the control flow and the data flow
        temp = [deepcopy(control_flow), deepcopy(data_flow)]
        # add temp as a nested array to all_permutations
        all_permutations.append(temp)

    return all_permutations

def main():
    matrix = np.array([np.zeros((5, 7), dtype=int), np.zeros((7, 5), dtype=int)], dtype=object)
    matrix[0][0][5] = matrix[0][1][6] = matrix[0][2][0] = matrix[0][3][1] = matrix[0][4][4] = 1
    matrix[1][0][4] = matrix[1][3][2] = matrix[1][5][3] = matrix[1][6][0] = 1

    print(permutations(matrix))

if __name__ == '__main__': 
    main()