import numpy as np

def translate(error: dict, no_bugs: int) -> np.ndarray:
    """
    This function takes an error and the number of bugs as input parameters and returns an array of actions.
    The actions are used to place edges in a graph based on the error and number of bugs.

    Args:
    error (dict): A dictionary containing information about the error. It has the following keys:
                    - port (str): The port where the error occurred (Up, Down, Out, Left, or Right).
                    - bug (int or str): The id of the bug where the error occurred.
    no_bugs (int): The number of bugs allowed on the board.

    Returns:
    np.ndarray: An array containing actions used to place edges in the graph.

    """

    actions = []
    index_col = 0
    indices_missing_edges = []

    # Check whether the passed error concerns the control flow or the data flow
    if error['port'] == 'Out':
        # DATA FLOW
        # Calculate column index
        index_col = 1 + int(error['bug'])

        index_row = 0
        while index_row <= (no_bugs * 2 + 1):
            indices_missing_edges.append([index_col, index_row])
            index_row += 1
        
        # Translate indices into the corresponding actions used to place the edges
        for index_pair in indices_missing_edges:

            # TRANSLATION:
            # für 3 bugs:
            # (Zeile * 5) + Spalte + 35

            # für n bugs:
            # (Zeile * (no_bugs + 2 )) + Spalte + size_matrix((no_bugs + 2) * (no_bugs + 2))
            # index_row * (no_bugs + 2) + index_col + ((no_bugs + 2) * (no_bugs + 2))
            # (index_pair[1] * (no_bugs + 2) + index_pair[0] + ((no_bugs + 2) * (no_bugs + 2))
            # !!!! (Spalte, Zeile) !!!!  -> Konvention für Position in Matrizen: (Zeile, Spalte)

            actions.append(index_pair[1] * (2 * no_bugs) + index_pair[0] + 35)

    else:
        # CONTROL FLOW
        # Calculate column index
        if error['bug'] == 0:
            index_col = 0
        else:
            index_col = 1 + ((int(error['bug']) - 1) * 2)
            if error['port'] == 'Right':
                index_col += 1

        index_row = 0
        while index_row <= (no_bugs + 1):
            indices_missing_edges.append([index_col, index_row])
            index_row += 1

        # Translate indices into the corresponding actions used to place the edges
        for index_pair in indices_missing_edges:
            actions.append(index_pair[1] * (2 * no_bugs + 1) + index_pair[0])

    return actions

if __name__ == '__main__':
    print("error = {'port': 'Left', 'bug': 1}")
    error = {'port': 'Left', 'bug': 1}
    no_bugs = 3
    actions = translate(error, no_bugs)
    print(actions)

    print("\nerror_4 = {'port': 'Up', 'bug': 1}")
    error_4 = {'port': 'Up', 'bug': 1}
    actions_4 = translate(error_4, no_bugs)
    print(actions_4)

    print("\nerror_5 = {'port': 'Out', 'bug': 1}")
    error_5 = {'port': 'Out', 'bug': 1}
    actions_5 = translate(error_5, no_bugs)
    print(actions_5)

    print("\nerror_6 = {'port': 'Out', 'bug': 0}")
    error_6 = {'port': 'Out', 'bug': 0}
    actions_6 = translate(error_6, no_bugs)
    print(actions_6)

    print("\nerror_7 = {'port': 'Up', 'bug': 0}")
    error_7 = {'port': 'Up', 'bug': 0}
    actions_7 = translate(error_7, no_bugs)
    print(actions_7)