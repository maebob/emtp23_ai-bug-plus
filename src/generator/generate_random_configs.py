"""
This file takes a given valid matrix and deletes n random edges from it.
"""
import numpy as np
from copy import deepcopy


def delete_edges_in_matrix(matrix: np.array, n: int, edges_to_delete: np.array) -> list[np.array]:
    """
    This function takes a given valid matrix and deletes n given edges from it.
    Arguments:
        matrix: A valid matrix.
        n: The number of edges to delete.
    Returns:
        A list of matrices with n deleted edges.
    """
    for i in range(n):
        # delete a random edge from the matrix the matrix will have a 1 at that position
        # get all positions where the matrix has a 1
        positions = np.argwhere(matrix == 1)
        # get position to delete
        position_to_delte = positions[edges_to_delete[i]]
        # delete the edge
        matrix[position_to_delte[0], position_to_delte[1]] = 0
    return matrix

def generate_config_with_input_pairs(control_matrix: np.array, data_matrix: np.array, data_range: range, output_function) -> list[np.array]:
    """
    This function generates a config with the given input pairs.
    Arguments:
        control_matrix: The control matrix to translate
        data_matrix: The data matrix to translate
        data_range: The range of data bugs to use
        output_function: The function to use to generate the output
    Returns:
        A config with the given input pairs.
    """
    # get all possible input pairs and save them in a numpy array
    input_pairs = np.array([[data_up, data_down, output_function(data_up, data_down)] for data_up in data_range for data_down in data_range])
    
    # flatten the matrices
    control_matrix = control_matrix.flatten()
    data_matrix = data_matrix.flatten()
    # concatenate the matrices with every input pair
    configs = np.array([np.concatenate((input_pair, control_matrix, data_matrix)) for input_pair in input_pairs])
    
    return configs

if __name__ == "__main__":
    # generate a random matrix
    control_matrix_incrementor = np.array([
        [0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0]
        ])
    data_matrix_incrementor = np.array([
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0]
    ])

    # Get the count of ones in the control matrix
    control_matrix_ones = np.count_nonzero(control_matrix_incrementor == 1)
    configs = np.array([])
    for i in range(0, control_matrix_ones):
        # get a copy of the control matrix
        control_matrix = deepcopy(control_matrix_incrementor)
        # get a copy of the data matrix
        data_matrix = deepcopy(data_matrix_incrementor)
        # delete i edges from the control matrix
        deleted_control_matrices = delete_edges_in_matrix(control_matrix, 1, np.array([i]))
        # generate a config with the input pairs
        config = generate_config_with_input_pairs(control_matrix, data_matrix, range(0, 10), lambda x, y: x + y)
        
        # add the config to the configs
        if configs.size == 0:
            configs = config
        else:
            configs = np.concatenate((configs, config))

    # save the configs to a file
    np.savetxt("configs.csv", configs, delimiter=";", fmt="%d")
