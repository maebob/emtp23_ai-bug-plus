import numpy as np

def number_bugs(matrix_or_array) -> int:

    """
    Given the matrix or flattened matrix of the controlflow matrix (or dataflow matrix), returns the number of bugs.

    n = number of bugs
    Controlflow matrix: rows from 0 to n+1, columns from 0 to 2n
    Dataflow matrix: rows from 0 to 2n, columns from 0 to n+1

    
    shape of matrix(controlflow)= ((n+2), (2n+1)), or transposed for dataflow; number of fields in each matrix is the same.
    no_fields = (n+2)*(2n+1) = 2n^2+5n+2
    using the quadratic formula ("Mitternachtsformel") to solve for the number of bugs:
    no_fields = (n+2)*(2n+1) = 2n^2+5n+2
    <=> 0 = 2n^2+5n+(2-no_fields)
    """
    array = matrix_or_array.flatten()
    no_bugs = int((-5 + (25-8*(2 - array.size))**(0.5))/4) # number of bugs used to form the matrix

    return no_bugs




# Change if needed:
# Define how many positions are taken up in the matrix/array for the learner
# at the beginning and end.

EXTRAS_START = 3
EXTRAS_END = 1

def array_to_matrices(array) -> tuple:
    
    #reshape the array into controlflow and dataflow matrices in the shape as needed for the environment
    #n = number of bugs, #X = number of X
    #dataflow: 
    #    [Wdh LA: (m x n)-matrix mit m Zeilen und n Spalten]
    #    #rows = n+2
    #    #columns = 2n+1
    #    shape: (n+2, 2n+1)
    #    start position: EXTRAS_START
    #    end position: EXTRAS_START + ((n+2)*(2n+1))
    #controlflow:
    #    #rows = 2n+1
    #    #columns = n+2
    #    shape: (2n+1, n+2)
    #    start position: EXTRAS_START + ((n+2)*(2n+1))
    #    end position:  EXTRAS_START + 2* ((n+2)*(2n+1))
    
    # workaround to determine the number of bugs by finding the first matrix:
    no_extra_array = np.array(array[EXTRAS_START : -EXTRAS_END])
    no_fields = no_extra_array.size
    first_matrix_flatten = no_extra_array[0 : int(no_fields/2)]

    no_bugs = number_bugs(first_matrix_flatten)

    controlflow = array[EXTRAS_START : EXTRAS_START +(no_bugs + 2) * (2 * no_bugs + 1)].reshape(no_bugs + 2, 2 * no_bugs + 1)
    dataflow = array[EXTRAS_START +(no_bugs + 2) * (2 * no_bugs + 1) : EXTRAS_START + 2 * ((no_bugs + 2) * (2 * no_bugs + 1))].reshape(2 * no_bugs + 1, no_bugs + 2)
    learner_input = array[0:EXTRAS_START]
    missing_positions = array[-EXTRAS_END:]
    tuple = np.array([controlflow, dataflow], dtype=object)
    return tuple

"""
def main():
    test_array_with_extras = np.array(
    [3, 5, 8,

    0, 1, 0, 0, 1, 0, 1, 
    0, 0, 0, 0, 0, 0, 0, 
    0, 0, 0, 0, 0, 0, 0, 
    0, 0, 0, 0, 0, 0, 0, 
    0, 1, 0, 0, 0, 0, 1, 

    0, 0, 0, 1, 0, 
    0, 0, 0, 1, 0, 
    0, 0, 0, 0, 0, 
    0, 1, 0, 0, 0, 
    0, 0, 0, 1, 0, 
    0, 0, 0, 0, 0, 
    0, 0, 0, 0, 1,

    12])

    array_to_tuple = array_to_matrices(test_array_with_extras)
    print(array_to_tuple)




if __name__ == "__main__":
    main()
"""
