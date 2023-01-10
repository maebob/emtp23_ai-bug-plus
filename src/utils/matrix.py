import numpy as np

"""
Define how many positions are taken up in the matrix/array for the learner
at the beginning and end.
In order to count the number of positions in the matrix correctly, we need to count from 1 and not from zero.
Therefore, use for EXTRAS_START the number of positions minus 1. 
"""
# TODO: discuss!
EXTRAS_START = 2 # The first three positions (0, 1, and 2) are taken for up, down, out
EXTRAS_END = 1 # The last position is taken for one deleted edge. Change if we want higher (but fixed) number of reserved positions for the solution.

def number_bugs(matrix_or_array) -> int:
    # TODO: Should we take the number of extra positions as an input or rather keep them as fixed variables?
    """
    Given the matrix or flattened matrix of control- and dataflow, returns the number of bugs.

    In more detail:

    Takes in an matrix or array consiting of the input pair and output, the controlflow matrix flattened,
    the dataflow matrix flattened and lastly, the position of the deleted edge.
    1) Flattens the matrix. If the input is an array already, nothing changes -> array
    2) Calculates the number of elements in each matrix -> no_fields
    3) Calculates the number of bugs by solving the quadratic equation, see explanation below.

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
    no_fields = int((array.size - EXTRAS_START - EXTRAS_END)/2) # number of fields in each matrix
    no_bugs = int((-5 + (25-8*(2 - no_fields))**(0.5))/4) # number of bugs used 
    print('no_bugs: ', no_bugs)

    return no_bugs


def array_to_matrix(array) -> np.array:
    """
    reshape the array into controlflow and dataflow matrices.
    n = number of bugs, #X = number of X
    dataflow: 
        [Wdh LA: (m x n)-matrix mit m Zeilen und n Spalten]
        #rows = n+2
        #columns = 2n+1
        shape: (n+2, 2n+1)
        start position: EXTRAS_START
        end position: EXTRAS_START + ((n+2)*(2n+1))
    controlflow:
        #rows = 2n+1
        #columns = n+2
        shape: (2n+1, n+2)
        start position: EXTRAS_START + ((n+2)*(2n+1))
        end position:  EXTRAS_START + 2* ((n+2)*(2n+1))
    """
    no_bugs = number_bugs(array)
    controlflow = array[EXTRAS_START : EXTRAS_START +(no_bugs + 2) * (2 * no_bugs + 1)].reshape(no_bugs + 2, 2 * no_bugs + 1)
    dataflow = array[EXTRAS_START +(no_bugs + 2) * (2 * no_bugs + 1) : EXTRAS_START + 2 * ((no_bugs + 2) * (2 * no_bugs + 1))].reshape(2 * no_bugs + 1, no_bugs + 2)
    learner_input = array[0:EXTRAS_START]
    missing_positions = array[-EXTRAS_END:]
    # TODO: includes up, down, out, missing positions; okay or do we want to change it?
    # TODO: discuss shape of "input" matrix for environment; does not work as is atm
    matrix = np.array([learner_input, controlflow, dataflow, missing_positions])
    print('matrix: ', matrix)
    print('learner_input: ', learner_input)
    print('missing_positions', missing_positions)
    print('controlflow: ', controlflow)
    print('dataflow: ', dataflow)
    return matrix

# """
def main():
    test_array = np.array([3, 5, 8,
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

    #array_to_matrix(test_array)
    number_bugs(test_array)
    #number_bugs(array_to_matrix(test_array))


if __name__ == "__main__":
    main()


 # """

"""
# Taken from env.observation_space

 array([array([[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0]]), array([[0, 0, 0, 0, 0],
                                              [0, 0, 0, 0, 0],
                                              [0, 0, 0, 0, 0],
                                              [0, 0, 0, 0, 0],
                                              [0, 0, 0, 0, 0],
                                              [0, 0, 0, 0, 0],
                                              [0, 0, 0, 0, 0]])],
      dtype=object)
"""
