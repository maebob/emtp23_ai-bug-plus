import pickle
import numpy as np

from engine import eval_main
from translation import matrix_to_json


def read_file(file_name):
    # Load the data from the pickle file
    with open(file_name, 'rb') as f:
        return pickle.load(f)


def split_data_element(data_element: list, matrix_size: int):
    up_port = data_element[0]
    down_port = data_element[1]
    result = data_element[2]
    control_matrix = data_element[3:3 + matrix_size]
    data_matrix = data_element[3 + matrix_size:3 + matrix_size + matrix_size]
    fix_bit = int(data_element[3 + matrix_size + matrix_size])
    return up_port, down_port, result, control_matrix, data_matrix, fix_bit


def fix_config(control_matrix: list, data_matrix: list, fix_bit: int):
    if fix_bit > len(control_matrix):
        data_matrix[fix_bit - len(control_matrix)] = 1
    else:
        control_matrix[fix_bit] = 1
    return control_matrix, data_matrix


def validate_config(up_port: int, down_port: int, result: int, control_matrix: list, data_matrix: list, fix_bit: int):
    """
    Validate the configuration by checking if the result is correct.

    Arguments:
        up_port {int} -- The up port
        down_port {int} -- The down port
        result {int} -- The expected result
        control_matrix {list} -- The control matrix
        data_matrix {list} -- The data matrix
        fix_bit {int} -- The fix bit
    Raises:
        Exception: If the result is not correct
    """
    fixed_control_matrix, fixed_data_matrix = fix_config(
        control_matrix, data_matrix, fix_bit)

    # Reshape the matrices
    # TODO: make this dependent on the matrix size
    fixed_control_matrix = np.array(fixed_control_matrix).reshape(5, 7)
    fixed_data_matrix = np.array(fixed_data_matrix).reshape(7, 5)

    # Convert the matrices to ints
    fixed_control_matrix = fixed_control_matrix.astype(int)
    fixed_data_matrix = fixed_data_matrix.astype(int)

    # Translate the matrix to a json
    json = matrix_to_json(control_matrix=fixed_control_matrix,
                          data_matrix=fixed_data_matrix, data_up=up_port, data_down=down_port)

    print(f"Starting validation: {json}")

    # Evaluate the json
    eval_result = eval_main(json)
    if eval_result.get("0_Out") != result:
        raise Exception(
            f'Validation failed: {up_port} {down_port} {result} {control_matrix} {data_matrix} {fix_bit}')


def run_validation(files: list):

    for file in files:
        file = read_file(file)
        length = len(file)
        for index, element in enumerate(file):
            up_port, down_port, result, control_matrix, data_matrix, fix_bit = split_data_element(
                element, 35)
            # change the fix bit to the correct index -3 for up, down, result 
            fix_bit = int(fix_bit) - 3

            validate_config(up_port, down_port, result, control_matrix,
                            data_matrix, fix_bit)
            
            if index % 100 == 0:
                print(f'Finished {index}/{length}')


if __name__ == '__main__':
    run_validation(['training_set.pkl', 'test_set.pkl'])
