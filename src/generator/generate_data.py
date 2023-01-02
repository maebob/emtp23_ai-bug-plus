import numpy as np
from copy import deepcopy
import pickle

import matrix_permutation as mp


def create_bitvector(up: int, down: int, out: int, control_matrix: np.array, data_matrix: np.array) -> np.array:
    """
    This function creates a bitvector from the given input pairs and the given matrices.
    Arguments:
        up: The up value
        down: The down value
        out: The output value
        control_matrix: The control matrix to translate
        data_matrix: The data matrix to translate
    Returns:
        A bitvector with the given input pairs and the given matrices.
    """
    # create the bitvector
    bitvector = np.array([up, down, out])
    # flatten the matrices
    control_matrix = control_matrix.flatten()
    data_matrix = data_matrix.flatten()
    # concatenate the matrices with the bitvector
    bitvector = np.concatenate((bitvector, control_matrix, data_matrix))
    return bitvector

def delete_position_bitvector(bitvector: np.array, position: int) -> np.array:
    """
    This function deletes (sets to 0) a given position from a given bitvector.
    Arguments:
        bitvector: The bitvector to delete the position from.
        position: The position to delete.
    Returns:
        The given bitvector with the given position deleted.
    """
    bitvector[position] = 0
    return bitvector

def delete_positions_bitvector(bitvector: np.array, positions: np.array) -> np.array:
    """
    This function deletes (sets to 0) a given positions from a given bitvector and appends the position.
    Arguments:
        bitvector: The bitvector to delete the positions from.
        positions: The positions to delete.
    Returns:
        The given bitvector with the given positions deleted.
    """
    return_vectors = np.array([])
    original_bitvector = deepcopy(bitvector)

    for position in positions:
        # delete the position from the bitvector
        bitvector = delete_position_bitvector(original_bitvector, position)
        # append the position to the bitvector to know which position was deleted
        bitvector = np.append(bitvector, position)
        return_vectors = np.append(return_vectors, bitvector)
    return return_vectors

def create_bitvector_with_deleted_positions(up: int, down: int, out: int, control_matrix: np.array, data_matrix: np.array) -> np.array:
    """
    This function creates a bitvector from the given input pairs and the given matrices.
    Arguments:
        up: The up value
        down: The down value
        out: The output value
        control_matrix: The control matrix to translate
        data_matrix: The data matrix to translate
    Returns:
        A bitvector with the given input pairs and the given matrices.
    """
    # create the bitvector
    bitvector = create_bitvector(up, down, out, control_matrix, data_matrix)
    # get all positions where the bitvector has a 1
    positions = np.argwhere(bitvector == 1)
    # delete the positions
    bitvector = delete_positions_bitvector(bitvector, positions)
    return bitvector

def create_data_for_config(min: int, max: int, control_matrix: np.array, data_matrix: np.array, calculation: callable) -> np.array:
    """
    This function creates a data set for a given configuration.
    Arguments:
        min: The minimum value for the up and down values.
        max: The maximum value for the up and down values.
        control_matrix: The control matrix to translate.
        data_matrix: The data matrix to translate.
        calculation: The calculation to perform.
    Returns:
            A data set with the given configuration.
    """

    # create an empty data set
    data_set = np.array([])
    # create all possible input pairs
    for up in range(min, max):
        for down in range(min, max):
            # create the output value
            out = calculation(up, down)
            # create the bitvector
            bitvector = create_bitvector_with_deleted_positions(up, down, out, control_matrix, data_matrix)
            # append the bitvector to the data set
            data_set = np.append(data_set, bitvector)
    return data_set

def main():
    # create the control matrix
    control_matrix = np.array([
        [0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0]
    ])
    # create the data matrix
    data_matrix = np.array([
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0]
    ])
    matries = [control_matrix, data_matrix]
    all_permutations = mp.permutations(matrix=matries)


    print("Generating data set...")
    total_permutations = len(all_permutations) 
    # create the data set
    data_set = np.array([])
    
    for index, permutation in enumerate(all_permutations):
        permutation_control_matrix = permutation[0]
        permutation_data_matrix = permutation[1]
        data_set = np.append(data_set, create_data_for_config(0, 20, permutation_control_matrix, permutation_data_matrix, lambda x, y: x + 1))
        print(f"Generated {((index / total_permutations)) * 100}% of data set.")
    # reshape the data set to save a bitvector per row
    bits_per_vector = 3 + control_matrix.size + data_matrix.size + 1
    data_set = data_set.reshape(-1, bits_per_vector)
    
    print("Saving data set...")
    # shuffle the data set
    np.random.shuffle(data_set)

    print("{} rows in data set.".format(data_set.shape[0]))

    # split the data set into a training and a test set
    training_set = data_set[:int(data_set.shape[0] * 0.8)]
    test_set = data_set[int(data_set.shape[0] * 0.8):]

    # save the training set
    with open('training_set.pkl', 'wb') as file:
        pickle.dump(training_set, file)
    print("Training set saved.")
    # save the test set
    with open('test_set.pkl', 'wb') as file:
        pickle.dump(test_set, file)
    print("Test set saved.")

if __name__ == '__main__':
    main()