import numpy as np
import sys
import os
from dotenv import load_dotenv

# load the .env file
load_dotenv()
# append the absolute_project_path from .env variable to the sys.path
sys.path.append(os.environ.get('absolute_project_path'))

from src.utils.determine_number_of_bugs import number_bugs

def translate_action(n: int, action: int) -> int:
    """Returns the translated action that would correspond to the matrix being in transposed form.
    Arguments:
        n {int} -- The number of bugs in the matrix.
        action {int} -- The action that should be translated to the position in the transposed matrix.
    Returns:
        int
    """
    size_matrix = (n * 2+1) * (n + 2)
    if action < size_matrix: # CONTROLFLOW
        row = action % (n + 2)
        column= action // (n + 2)
        new_action = row * (2 * n + 1) + column
    else: # DATAFLOW
        action = action - size_matrix
        row = action % (n * 2 + 1)
        column = action // (n * 2 + 1)
        new_action = row * (n + 2) + column + size_matrix
    return new_action


# Testing:
"""
# if __name__ == '__main__':
#     n = 3
#     action = 66
#     print(translate_action(n, action))
"""
