import numpy as np

def find_error_columns(error: dict, no_bugs: int) -> int and int and int:
    """
    This function takes an error and the number of bugs as input parameters and returns the matrix,
    where the error occurred (0: control flow, 1: dataflow matrix), and the row where an edge is missing.
    Args:
        error {dict} -- A dictionary containing information about the error. It has the following keys:
                        - port {str} -- The port where the error occurred (Up, Down, Out, Left, or Right).
                        - bug {int or str} -- The id of the bug where the error occurred.
        no_bugs {int} -- The number of bugs on the board.
    Returns:
        int and int and int: The part of the matrix (0: control flow, 1: dataflow matrix), the row of the missing edge and the Bug ID where the error occured.
    """
    index_col = None
    bug_id = int(error['bug'])
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
    return control_or_data_matrix, index_col, bug_id



def column_to_range_transposed_matrix(control_or_data_matrix: int, no_bugs: int, index_col: int) -> int and int:
    """
    Given the column index and the the part of a matrix (0 for controlflow, 1 for dataflow),
    this function calculates the range of positions of the transposed matrix of our environment.
    Example: Controlflow matrix (control_or_data_matrix=0), index_col=0, no_bugs = 3: returns [0,5]
    Args:
        control_or_data_matrix {int} -- 0: controlflow matrix , 1 dataflow matrix
        no_bugs {int} -- The number of bugs on the board.
        index_col {int} -- The column index of the positions to be calculated.
    Returns:
        int and int -- The range of corresponding positions in the transposed matrix, i.e. min (inclusive) and max (not inclusive).
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
    return range_from, range_to

def connecting_row(control_or_data_matrix: int, index_col: int, bug_id:int, no_bugs ) -> int:
    """ 
    Given the part of a matrix (0 for controlflow, 1 for dataflow), the column index and the bug id,
    find the row where an edge is missing. This can then be used to determine the exact position, the next edge should be placed.
    Args:
        control_or_data_matrix {int} -- 0: controlflow matrix , 1 dataflow matrix
        index_col {int} -- The column index of the positions to be calculated.
        bug_id {int} -- The id of the bug where the error occurred.
    Returns:
        int -- The row where an edge is missing.
    """
    if control_or_data_matrix == 0:
        # CONTROL FLOW
        next_row = (bug_id + 2) % (no_bugs+1) # the next row is the bug id + 2; for the last bug, the next row is 0 (note: could also be 1 or depend on L /R; adjust if needed)
    elif control_or_data_matrix == 1:
        next_row = None
    return next_row

def select_new_position(control_or_data_matrix: int, range_from: int, bug_id:int, no_bugs ) -> int:
    """ 
   If the error occurs in the control flow, find the position in the matrix where the next edge should be placed.
   Connects a bug to the next bug or respectively the last bug to the mother board.
    Args:
        control_or_data_matrix {int} -- 0: controlflow matrix , 1: dataflow matrix
        range_from {int} -- The first position of the row where an edge is missing.
        bug_id {int} -- The id of the bug where the error occurred.
    Returns:
        int -- The position where a new edge should be placed.
    """
    if control_or_data_matrix == 0: # error is in the control flow
        next_row = (bug_id + 2) % (no_bugs+2) # connect the control flow to the next bug or the last bug to the mother board
        next_position = range_from + next_row # the next position is the range from + the next row
    else:
        next_position = None
    return next_position

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
    control_or_data_matrix, index_col, bug_id = find_error_columns(error, no_bugs)
    range_from, range_to = column_to_range_transposed_matrix(control_or_data_matrix, no_bugs, index_col)
    next_action = select_new_position(control_or_data_matrix, range_from, bug_id, no_bugs)
    return range_from, range_to, next_action