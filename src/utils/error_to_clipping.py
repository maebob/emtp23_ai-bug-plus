import numpy as np

def find_error_columns(error: dict, no_bugs: int) -> int and int:
    """
    This function takes an error and the number of bugs as input parameters and returns the matrix,
    where the error occurred (0: control flow, 1: dataflow matrix), and the row where an edge is missing.
    Args:
        error {dict} -- A dictionary containing information about the error. It has the following keys:
                        - port {str} -- The port where the error occurred (Up, Down, Out, Left, or Right).
                        - bug {int or str} -- The id of the bug where the error occurred.
        no_bugs {int} -- The number of bugs on the board.
    Returns:
        int and int: The part of the matrix (0: control flow, 1: dataflow matrix) and the row of the missing edge.
    """
    index_col = None
    # Check whether the passed error concerns the control flow or the data flow
    if error['port'] == 'Up' or error['port'] == 'Down' or error['port'] == 'Out':
        # DATA FLOW
        # errors or missing edges for board 0 are not caught, therefore we only need to take care of errors for bugs 1 to no_bugs
        control_or_data_matrix = 1
        index_col = 1 + int(error['bug'])
    else:
        # CONTROL FLOW
        control_or_data_matrix = 0
        # Calculate column index
        if error['bug'] == 0:
            index_col = 0
        else:
            index_col = 1 + ((int(error['bug']) - 1) * 2)
            if error['port'] == 'Right':
                index_col += 1
    return control_or_data_matrix, index_col



def column_to_range_transposed_matrix(control_or_data_matrix: int, no_bugs: int, index_col: int) -> np.array:
    """
    Given the column index and the the part of a matrix (0 for controlflow, 1 for dataflow),
    this function calculates the range of positions of the transposed matrix of our environment.
    Example: Controlflow matrix (control_or_data_matrix=0), index_col=0, no_bugs = 3: returns [0,5]
    Args:
        control_or_data_matrix {int} -- 0: controlflow matrix , 1 dataflow matrix
        no_bugs {int} -- The number of bugs on the board.
        index_col {int} -- The column index of the positions to be calculated.
    Returns:
        np.array -- The range of corresponding positions in the transposed matrix, i.e. min (inclusive) and max (not inclusive).
    """
    size_matrix = (no_bugs * 2 + 1) * (no_bugs + 2)
    range_from = 0
    range_to = 2 * size_matrix
    if index_col == None: # if none of the defined errors were caught, the action space should not be clipped
        return [range_from, range_to]
    elif control_or_data_matrix == 0:
        # CONTROL FLOW
        range_from = index_col * (no_bugs + 2)
        range_to = range_from + (no_bugs + 2)
    elif control_or_data_matrix == 1:
        # DATA FLOW
        range_from = index_col * (2 * no_bugs + 1) + size_matrix
        range_to = range_from + (2 * no_bugs + 1)
    return [range_from, range_to]


def translate_to_range(error: dict, no_bugs: int) -> np.ndarray:
    """ 
    Given an error, this function returns the range to which the action space should be clipped to.
    Example: error = {'port': 'Left', 'bug': 1}, no_bugs = 3: returns [5, 9]
    Args:
        error {dict} -- A dictionary containing information about the error. It has the following keys:
                        - port {str} -- The port where the error occurred (Up, Down, Out, Left, or Right).
                        - bug {int or str} -- The id of the bug where the error occurred.
        no_bugs {int} -- The number of bugs on the board.
            np.array -- The range, i.e. min (inclus.) and max (not inclusive), of positions of the transposed
        matrix of our environment.
   Returns:
        np.array -- The range of positions to which the action space should be clipped to.
        First element is inclusive, second element is not inclusive. (see example above).
    """
    control_or_data_matrix, index_col = find_error_columns(error, no_bugs)
    range_for_clipping = column_to_range_transposed_matrix(control_or_data_matrix, no_bugs, index_col)
    return range_for_clipping