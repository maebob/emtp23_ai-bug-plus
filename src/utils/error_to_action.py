import numpy as np

def translate(error, no_bugs):
    actions = np.array()
    index_col = 0
    indices_missing_edges = []

    # Check wether the passed error concerns the control flow or the data flow
    if error['port'] == 'Up' or error['port'] == 'Down' or error['port'] == 'Out':
        # DATA FLOW
        pass
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
            actions.append(index_pair[1] + (2 * no_bugs) + index_pair[0])

    return actions