"""
This script demonstrates the usage of the 'permutations' function, which generates
all possible permutations of a given matrix based on the control flow. The main
function creates a matrix with specific values, calls the 'permutations' function,
and then prints the result.

To execute the script, simply run it from the command line:
python matrix_permutations.py

The script will print the permutations of the matrix as a list of lists.

Functions included in this script:

permutations: Generate all possible permutations of the matrix based on the control flow.
main: Main function to demonstrate the permutations of the given matrix.
"""

from sympy.utilities.iterables import multiset_permutations

import numpy as np
from copy import deepcopy


def permutations(matrix):
    """
    Generate all possible permutations of the matrix based on the control flow.

    This function takes a matrix as input and generates all possible permutations
    of the matrix by sorting the control flow and data flow elements based on
    the row indices.

    Argumments:
        matrix (list): A list containing two elements: control_flow (matrix[0])
                    and data_flow (matrix[1]).

    Returns:
        list: A list of all possible permutations of the matrix.

    Example:
        matrix = [        [[1, 2], [3, 4]],
            [[5, 6], [7, 8]],
        ]
        result = permutations(matrix)
        print(result)  # Output: [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
    """
    all_permutations = []

    nr_columns_control_flow = matrix[0][0].size
    nr_rows_control_flow = (nr_columns_control_flow + 3) // 2

    list_rows_cf = np.arange(2, nr_rows_control_flow, dtype=int)

    for perm in multiset_permutations(list_rows_cf):
        copy_matrix = matrix
        control_flow = matrix[0]
        data_flow = matrix[1]
        swapped = True

        # Perform bubble sort to generate permutations
        while swapped:
            swapped = False
            for i in range(len(perm) - 1):
                if perm[i] > perm[i + 1]:
                    perm[i], perm[i + 1] = perm[i + 1], perm[i]
                    swapped = True

                    bugSwapped1 = list_rows_cf[i] - 1
                    bugSwapped2 = list_rows_cf[i + 1] - 1

                    # Swap the control_flow rows and columns
                    control_flow[[bugSwapped1 + 1, bugSwapped2 + 1]
                                 ] = control_flow[[bugSwapped2 + 1, bugSwapped1 + 1]]
                    control_flow[:, [2 * bugSwapped1 - 1, 2 * bugSwapped2 - 1]
                                 ] = control_flow[:, [2 * bugSwapped2 - 1, 2 * bugSwapped1 - 1]]
                    control_flow[:, [2 * bugSwapped1, 2 * bugSwapped2]
                                 ] = control_flow[:, [2 * bugSwapped2, 2 * bugSwapped1]]

                    # Swap the data_flow rows and columns
                    data_flow[:, [bugSwapped1 + 1, bugSwapped2 + 1]
                              ] = data_flow[:, [bugSwapped2 + 1, bugSwapped1 + 1]]
                    data_flow[[2 * bugSwapped1 - 1, 2 * bugSwapped2 - 1]
                              ] = data_flow[[2 * bugSwapped2 - 1, 2 * bugSwapped1 - 1]]
                    data_flow[[2 * bugSwapped1, 2 * bugSwapped2]
                              ] = data_flow[[2 * bugSwapped2, 2 * bugSwapped1]]

        all_permutations.append([deepcopy(control_flow), deepcopy(data_flow)])

    return all_permutations  # Return the list of permutations


def main():
    """
    Main function to demonstrate the permutations of the given matrix.
    This function creates a matrix with specific values, calls the 'permutations'
    function to generate all possible permutations of the matrix, and then prints
    the result.
    """
    # Create a matrix with specific values
    matrix = np.array([np.zeros((5, 7), dtype=int),
                      np.zeros((7, 5), dtype=int)], dtype=object)
    matrix[0][0][5] = matrix[0][1][6] = matrix[0][2][0] = matrix[0][3][1] = matrix[0][4][4] = 1
    matrix[1][0][4] = matrix[1][3][2] = matrix[1][5][3] = matrix[1][6][0] = 1

    # Generate all possible permutations of the matrix
    result = permutations(matrix)

    # Print the permutations
    print(result)


if __name__ == '__main__':
    main()
