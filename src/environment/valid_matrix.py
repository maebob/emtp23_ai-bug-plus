import numpy as np

# number of positions in the arrow before the controlflow matrix;
# for 3: up, down and out
NO_EXTRAS = 3


# for dataflow matrix of flowmatrix, use np.transpose(matrix)

def is_valid_matrix(matrix) -> bool:
    """
    First, find position of all non-zero elements in the matrix.
    Then, check if the non-zero elements are in positions that are not allowed.
    If so, return False, meaning the matrix is not valid.
    Otherwise, return True.
    """
    non_zero_positions = (np.argwhere(matrix)) # numpy.ndarray
    forbid_pos = forbidden_positions(matrix) # numpy.ndarray
    for non_zero_position in non_zero_positions:
        #check if non_zero_position is in forbid_pos
        if np.any(np.all(non_zero_position == forbid_pos, axis=1)):
            return False      
    return True

    

def forbidden_positions(matrix) -> np.ndarray:
    """
    Returns forbidden positions of the control flow matrix:
    No connection between L or R and I.
    """
    number_rows, number_columns = matrix.shape
    forbidden_index = np.ndarray((number_rows*2-2, 2), dtype=int) #except for the first two rows, each row has two forbidden positions (for L and R of itself)
    forbidden_index[0] = np.array([0,0])
    forbidden_index[1] = np.array([1,0])
    column_counter = 1
    for row_index in range(2, number_rows): #start at second row
        forbidden_index[row_index*2-2] = np.array([row_index, column_counter]) 
        forbidden_index[row_index*2-1] = np.array([row_index, column_counter+1])
        column_counter += 2
    return forbidden_index

def forbidden_positions_flat(array, no_bugs) -> list: # or should we do a list?
    """
    Takes in an array consiting of the input pair and output, the controlflow matrix flattened,
    followed by the flattened dataflow matrix and (for now) the number of bugs
    Positions are derived from the rows and columns of the matrices in relation to the number of bugs.
    n = number of bugs
    Controlflow matrix: rows from 0 to n+1, columns from 0 to 2n
    Dataflow matrix: rows from 0 to 2n, columns from 0 to n+1

    # TODO: First, the function checks how many bugs are used by the number of positions.
    #TODO: shape of matrix= (n+2)*(2n+1) = 2n^2+5n+2
    Then, the forbidden positions for the control flow matrix are calculated. These are:
    forb. pos for row 0 an 1: (n*2+1)*row+1
    forb. pos. for 1 < row < n+2: (n*2+1)*row +(row-1)*2 and (n*2+1)*row +(row-1)*2+1

    Forbidden positions for dataflow matrix are the same as for the transposed control flow matrix.

    The index of forbidden positions of the input array are saved in the list forbidden_index and returned.
    """
    #no_bugs = int((array.size-NO_EXTRAS)/2/())

    forbidden_index = []



    # forbidden positions in control flow matrix:
    # (looping through the rows)
    for i in range(NO_EXTRAS, NO_EXTRAS+2):
        print("i: ", i)
        forbidden_index.append((no_bugs*2+1)*(i-NO_EXTRAS)+1+NO_EXTRAS)

    for i in range(NO_EXTRAS+2, no_bugs+NO_EXTRAS+2):
        print("i: ", i)
        forbidden_index.append((no_bugs*2+1)*(i-NO_EXTRAS)+((i-NO_EXTRAS)-1)*2+NO_EXTRAS)
        forbidden_index.append((no_bugs*2+1)*(i-NO_EXTRAS)+((i-NO_EXTRAS)-1)*2+NO_EXTRAS+1)

    return forbidden_index



#"""
# Testing
def main():
    #generate empty matrix of shape (5,7)
    testmatrix = np.zeros((5, 7), dtype=int)
    testmatrix[0][5] = testmatrix[1][6] = testmatrix[2][0] = testmatrix[3][1] = testmatrix[4][4]  = 1 # control flow matrix of incrementer
    print(testmatrix)
    flat_matrix = testmatrix.flatten()
    print(flat_matrix)
    test_array = np.concatenate((np.array([1, 2, 3]), flat_matrix, flat_matrix), axis=0)
    print(forbidden_positions_flat(test_array, 3))


    #print(test_array)
    #print("is_valid_matrix: {}".format(is_valid_matrix(matrix=testmatrix)))
    #print(forbidden_positions(testmatrix))



if __name__ == "__main__":
    main()
#"""