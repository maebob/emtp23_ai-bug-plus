import numpy as np

from src.utils.matrix import number_of_bugs


# For matrices with input and output values as well as the position of the removed edge
"""
# positions in the arrow before the controlflow matrix
NO_EXTRAS_BEGINNING = 2 # positions 0, 1, 2 are reserved for up, down, out
# positions in the arrow after the dataflow matrix
NO_EXTRAS_END = 1 # last position is reserved for solution of the removed edge
"""
# For matrices consiting of dataflow and controlflow matrix without any additional information, set the following:
# TODO: change to imported values from utils (?)
NO_EXTRAS_BEGINNING = -1 # to account for the fact that the first position is 0 and not 1
NO_EXTRAS_END = 0

# For input arrays delete the "translation" into array and change input of definition to 'matrix'

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
    n = number_of_bugs(matrix)
    forbidden_list = []


    # forbidden positions in control flow matrix:
        # n = number of bugs
        # each row has 2n+1 positions
        # a row starts with position p = row*(2n+1)+1
    for i in range(2): # row 0 and 1 in original controlflow matrix
        forbidden_list.append((no_bugs * 2 + 1) * (i - NO_EXTRAS_BEGINNING) + 1 + NO_EXTRAS_BEGINNING)
    
    for i in range(NO_EXTRAS_BEGINNING + 2, no_bugs + NO_EXTRAS_BEGINNING + 2): # rows 2 to (n+1) in original controlflow matrix
        forbidden_list.append((no_bugs * 2 + 1) * (i - NO_EXTRAS_BEGINNING)+((i - NO_EXTRAS_BEGINNING) - 1) * 2 + NO_EXTRAS_BEGINNING)
        forbidden_list.append((no_bugs * 2 + 1) * (i - NO_EXTRAS_BEGINNING)+((i - NO_EXTRAS_BEGINNING)-1) * 2 + NO_EXTRAS_BEGINNING + 1)
    forbidden_index = np.asarray(forbidden_list)
    return forbidden_index



    """
def forbidden_positions(matrix) -> np.ndarray:
    #TODO: use util function to get number of bugs and kick out what is not needed

    # Takes in an array consiting of the input pair and output, the controlflow matrix flattened,
    # followed by the flattened dataflow matrix
    # Positions are derived from the rows and columns of the matrices in relation to the number of bugs.
    # n = number of bugs
    # Controlflow matrix: rows from 0 to n+1, columns from 0 to 2n
    # Dataflow matrix: rows from 0 to 2n, columns from 0 to n+1

    # First, the function checks how many bugs are used by the number of positions.
    # shape of matrix= (n+2)*(2n+1) = 2n^2+5n+2
    # using the "Mitternachtsformel" to solve for the number of bugs:
    # no_fields = (n+2)*(2n+1) = 2n**2+5n+2
    # <=> 0 = 2n**2+5n+(2-no_fields)

    # Then, the forbidden positions for the control flow matrix are calculated, i.e. no control flow connection of a bug to itself.
    # These are:
    # forb. pos for row 0 an 1: (n*2+1)*row+1
    # forb. pos. for 1 < row < n+2: (n*2+1)*row +(row-1)*2 and (n*2+1)*row +(row-1)*2+1

    # Forbidden positions for dataflow matrix are the same as for the transposed control flow matrix.

    # The index of forbidden positions of the input array are saved in the list forbidden_index and returned.
    
    array = matrix.flatten()
    no_fields = int((array.size - NO_EXTRAS_BEGINNING - NO_EXTRAS_END)/2) # number of fields in each matrix
    no_bugs = int((-5 + (25 - 8 *(2 - no_fields))**(0.5))/4) # number of bugs used 

    forbidden_list = []


    # forbidden positions in control flow matrix:
    for i in range(NO_EXTRAS_BEGINNING, NO_EXTRAS_BEGINNING + 2): # row 0 and 1 in original controlflow matrix
        forbidden_list.append((no_bugs * 2 + 1) * (i - NO_EXTRAS_BEGINNING) + 1 + NO_EXTRAS_BEGINNING)
    
    for i in range(NO_EXTRAS_BEGINNING + 2, no_bugs + NO_EXTRAS_BEGINNING + 2): # rows 2 to (n+1) in original controlflow matrix
        forbidden_list.append((no_bugs * 2 + 1) * (i - NO_EXTRAS_BEGINNING)+((i - NO_EXTRAS_BEGINNING) - 1) * 2 + NO_EXTRAS_BEGINNING)
        forbidden_list.append((no_bugs * 2 + 1) * (i - NO_EXTRAS_BEGINNING)+((i - NO_EXTRAS_BEGINNING)-1) * 2 + NO_EXTRAS_BEGINNING + 1)
    forbidden_index = np.asarray(forbidden_list)
    return forbidden_index
    """






"""
# Testing
def main():
    controlflow = np.zeros((5, 7), dtype=int)
    controlflow[0][5] = controlflow[1][6] = controlflow[2][0] = controlflow[3][1] = controlflow[4][4]  = 1

    dataflow = np.zeros((7,5), dtype= int)
    dataflow[0][4] = dataflow[3][2] = dataflow[5][3] = dataflow[6][0] = 1

    validmatrix = np.concatenate((controlflow.flatten(), dataflow.flatten()), axis=0)
    # use for tests with array as input
    # validarray = np.concatenate((np.array([1, 2, 3]), validmatrix.flatten(), validmatrix.flatten()), axis=0)
    print("valid matrix is valid matrix: {}".format(is_valid_matrix(validmatrix)))
    print(forbidden_positions(validmatrix))
    print("expected output: [0, 7, 15, 16, 24, 25, 33, 34]")
    #print(forbidden_positions(validarray))
    # expected output for array when first 3 postions are reserved for up, down, out
    # print("expected output: [3, 10, 18, 19, 27, 28, 36, 37]")


    invalidcontrolflow = controlflow.copy()
    invalidcontrolflow[0][0] =invalidcontrolflow[1][6] = invalidcontrolflow[2][0] = invalidcontrolflow[3][1] = invalidcontrolflow[4][4]  = 1
    invalidmatrix = np.concatenate((invalidcontrolflow.flatten(), dataflow.flatten()), axis=0)
    print("invalid matrix is valid matrix: {}".format(is_valid_matrix(invalidmatrix)))

    # use for tests with array as input
    #invalidarray = np.concatenate((np.array([1, 2, 3]), invalidmatrix.flatten(), validmatrix.flatten()), axis=0)
    #print("invalid matrix is valid matrix: {}".format(is_valid_matrix(invalidarray)))








if __name__ == "__main__":
    main()
"""