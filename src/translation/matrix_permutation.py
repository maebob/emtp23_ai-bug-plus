import numpy as np
from copy import deepcopy
from matrix_to_json import main as matrix_to_json
from src.engine.eval import main as eval


def create_all_permutations(matrix):
    permutations = []
    control_flow = matrix[0]
    data_flow = matrix[1]

    '''
        1, 2, 3
    '''

    permutations.append([deepcopy(control_flow), deepcopy(data_flow)])

    '''
        1, 3, 2 
    '''
    control_flow[[3, 4]] = control_flow[[4, 3]]
    control_flow[:, [3, 5]] = control_flow[:, [5, 3]]
    control_flow[:, [4, 6]] = control_flow[:, [6, 4]]

    data_flow[:, [3, 4]] = data_flow[:, [4, 3]]
    data_flow[[3, 5]] = data_flow[[5, 3]]
    data_flow[[4, 6]] = data_flow[[6, 4]]

    permutations.append([deepcopy(control_flow), deepcopy(data_flow)])

    '''
        2, 3, 1
    '''
    control_flow[[2, 4]] = control_flow[[4, 2]]
    control_flow[:, [1, 5]] = control_flow[:, [5, 1]]
    control_flow[:, [2, 6]] = control_flow[:, [6, 2]]

    data_flow[:, [2, 4]] = data_flow[:, [4, 2]]
    data_flow[[1, 5]] = data_flow[[5, 1]]
    data_flow[[2, 6]] = data_flow[[6, 2]]

    permutations.append([deepcopy(control_flow), deepcopy(data_flow)])

    '''
        2, 1, 3
    '''
    control_flow[[3, 4]] = control_flow[[4, 3]]
    control_flow[:, [3, 5]] = control_flow[:, [5, 3]]
    control_flow[:, [4, 6]] = control_flow[:, [6, 4]]

    data_flow[:, [3, 4]] = data_flow[:, [4, 3]]
    data_flow[[3, 5]] = data_flow[[5, 3]]
    data_flow[[4, 6]] = data_flow[[6, 4]]

    permutations.append([deepcopy(control_flow), deepcopy(data_flow)])

    '''
        3, 1, 2
    '''
    control_flow[[2, 4]] = control_flow[[4, 2]]
    control_flow[:, [1, 5]] = control_flow[:, [5, 1]]
    control_flow[:, [2, 6]] = control_flow[:, [6, 2]]

    data_flow[:, [2, 4]] = data_flow[:, [4, 2]]
    data_flow[[1, 5]] = data_flow[[5, 1]]
    data_flow[[2, 6]] = data_flow[[6, 2]]

    permutations.append([deepcopy(control_flow), deepcopy(data_flow)])

    '''
        3, 2, 1
    '''
    control_flow[[3, 4]] = control_flow[[4, 3]]
    control_flow[:, [3, 5]] = control_flow[:, [5, 3]]
    control_flow[:, [4, 6]] = control_flow[:, [6, 4]]

    data_flow[:, [3, 4]] = data_flow[:, [4, 3]]
    data_flow[[3, 5]] = data_flow[[5, 3]]
    data_flow[[4, 6]] = data_flow[[6, 4]]

    permutations.append([deepcopy(control_flow), deepcopy(data_flow)])

    print("In the list:")
    return permutations


def main():
    matrix = np.array([np.zeros((5, 7), dtype=int), np.zeros((7, 5), dtype=int)], dtype=object)
    matrix[0][0][5] = matrix[0][1][6] = matrix[0][2][0] = matrix[0][3][1] = matrix[0][4][4] = 1
    matrix[1][0][4] = matrix[1][3][2] = matrix[1][5][3] = matrix[1][6][0] = 1
    print("All permutations are:\n")
    all_permutations = create_all_permutations(matrix)
    #print(all_permutations)
    for permutation in all_permutations:
        matrix_in_json = matrix_to_json(control_matrix=permutation[0], data_matrix=permutation[1], data_up=2, data_down=3)

        result = eval(matrix_in_json)
        assert result.get("0_Out") == 3
        print("This permutation is correct")






if __name__ == '__main__':
    main()


