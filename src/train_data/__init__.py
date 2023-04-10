""" 
This module contains files with training data for the agent.
Each config contains as the first three positions the input-output pair (x, y) and the result (2x+y). Followed by the flattened
corresponding matrix (first, 35 positions for the control flow matrix, then 35 positions for the data flow matrix).
In each matrix, one or several edges for a minimal solution for the problem have been removed.
Explanation of file names with the following examples: all_edges_5_10_4edges.csv, all_edges_5_10_10steps.csv
    - all edges: each edge in a (solved) matrix has been removed
    - 5_10: minimum and maximum of values for x and y as the input
    - 4edges: exact number of edges that have been removed
    - 10steps: 1 to 10 edges have been removed
"""