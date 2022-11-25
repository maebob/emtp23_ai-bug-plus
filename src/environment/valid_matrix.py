import numpy as np

# for dataflow matrix of flowmatrix, use np.transpose(matrix)

def is_valid_matrix(matrix) -> bool:
    """
    First, find position of all non-zero elements in the matrix.
    Then, check if the non-zero elements are in positions that are allowed.
    Otherwise, return True.
    """
    non_zero_positions = (np.argwhere(matrix)) # numpy.ndarray

    forbid_pos = forbidden_positions(matrix)

    for non_zero_position in non_zero_positions:
        #check if non_zero_position is in forbid_pos
        if np.any(np.all(non_zero_position == forbid_pos, axis=1)):
            return False
        
    return True

    

def forbidden_positions(matrix) -> np.ndarray: # returns all forbidden positions of the matrix
    number_rows, number_columns = matrix.shape
    forbidden_index = np.ndarray((number_rows*2-2, 2), dtype=int) #except for the first two rows, each row has two forbidden positions (for L and R of itself)
    forbidden_index[0] = np.array([0,0])
    forbidden_index[1] = np.array([1,0])
    column_counter = 1 #TODO: Können wir das noch mehr verallgemeinern?
    for row_index in range(2, number_rows): #start at second row
        forbidden_index[row_index*2-2] = np.array([row_index, column_counter]) 
        column_counter += 1 #TODO: more elegant way to do this?
        forbidden_index[row_index*2-1] = np.array([row_index,column_counter])
        column_counter += 1
    return forbidden_index


"""
This loops through all forbidden positions
"""
def check_forbidden_positions(matrix) -> bool: # checks if any edges are in forbidden positions (hardcoded)
    for i in forbidden_positions(matrix):
        if matrix[i[0]][i[1]] != 0:
            return False
        else:
            return True


def main():
    #generate empty matrix of shape (5,7)
    testmatrix = np.zeros((5, 7), dtype=int)
    testmatrix [0][5]=testmatrix [1][6] =testmatrix [2][0] =testmatrix [3][1] =testmatrix [4][4]  = 1 # control flow matrix of incrementer
    print(testmatrix)
    print("check forbidden positions: \n", check_forbidden_positions(matrix=testmatrix))
    print("***********************************")
    print("is valid matrix: \n", is_valid_matrix(matrix=testmatrix))




if __name__ == "__main__":
    main()