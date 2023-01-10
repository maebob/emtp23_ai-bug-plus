"""
Define how many positions are taken up in the matrix/array for the learner
at the beginning and end.
In order to count the number of positions in the matrix correctly, we need to count from 1 and not from zero.
Therefore, use for EXTRAS_START the number of positions minus 1. 
"""
EXTRAS_START = 2 # The first three positions (0, 1, and 2) are taken for up, down, out
EXTRAS_END = 1 # The last position is taken for one deleted edge. Change if we want higher (but fixed) number of reserved positions for the solution.

def number_bugs(matrix_or_array) -> int:
    # TODO: Should we take the number of extra positions as an input or rather keep them as fixed variables?
    """
    Given the matrix or flattened matrix of control- and dataflow, returns the number of bugs.

    In more detail:
    Flattens the matrix. If the input is an array already, nothing changes.
    Takes in an array consiting of the input pair and output, the controlflow matrix flattened,
    the dataflow matrix flattened and lastly, the position of the deleted edge.
    Positions are derived from the rows and columns of the matrices in relation to the number of bugs.
    n = number of bugs
    Controlflow matrix: rows from 0 to n+1, columns from 0 to 2n
    Dataflow matrix: rows from 0 to 2n, columns from 0 to n+1

    The function checks how many bugs are used by the number of positions.
    shape of matrix= (n+2)*(2n+1) = 2n^2+5n+2
    using the quadratic formula ("Mitternachtsformel") to solve for the number of bugs:
    no_fields = (n+2)*(2n+1) = 2n^2+5n+2
    <=> 0 = 2n^2+5n+(2-no_fields)
    """
    array = matrix_or_array.flatten()
    no_fields = int((array.size - EXTRAS_START - EXTRAS_END)/2) # number of fields in each matrix
    no_bugs = int((-5 + (25-8*(2 - no_fields))**(0.5))/4) # number of bugs used 

    return no_bugs