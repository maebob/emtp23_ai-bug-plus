import numpy as np
import sys
#TODO: change path
sys.path.append('/Users/mayte/github/bugplusengine') # Mayte
# sys.path.append('C:/Users/D073576/Documents/GitHub/BugPlusEngine/') # Mae
# sys.path.append('/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/') # Aaron
from src.utils.matrix import number_bugs



def is_valid_matrix(matrix) -> bool:
    """
    First, find position of all non-zero elements in the matrix.
    Then, check if the non-zero elements are in positions that are not allowed.
    If so, return False, meaning the matrix is not valid.
    Otherwise, return True.
    """
    array = matrix.flatten()
    non_zero_positions = np.argwhere(array).flatten() # numpy.ndarray
    forbid_pos = forbidden_positions(array) # numpy.ndarray

    for non_zero_position in non_zero_positions:
        #check if non_zero_position is in forbid_pos
        if np.any(non_zero_position == forbid_pos):
            return False      
    return True


def forbidden_positions(matrix) -> np.ndarray:
    n = number_bugs(matrix)
    forbidden_list = []

    # forbidden positions in control flow matrix:
        # n = number of bugs
        # each row has 2n+1 positions
        # a row starts with position p = row*(2n+1)+1
    for row in range(2): # row 0 and 1 in original controlflow matrix
        forbidden_list.append((2*n+1) * row)

    for row in range(2, n + 2): # all rows >= 2 in original controlflow matrix
        forbidden_list.append((n*2+1)*row + (row-2)*2+1)
        forbidden_list.append((n*2+1)*row + (row-2)*2+2)
 
    forbidden_index = np.asarray(forbidden_list)
    return forbidden_index
