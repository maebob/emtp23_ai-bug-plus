import numpy as np
import sys
import os
from dotenv import load_dotenv

# load the .env file
load_dotenv()
# append the absolute_project_path from .env variable to the sys.path
sys.path.append(os.environ.get('absolute_project_path'))

from src.utils.determine_number_of_bugs import number_bugs



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
