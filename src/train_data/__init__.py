""" 
This module contains files with training data for the agent.
Each config contains several rows of data.
Each row corresponds to a problem the agent should solve.
A problem consists  of the following parts:
    - the first three positions are the input-output pair (x, y) and the result (2x+y)
    - corresponding matrix flattened to array (35 positions for the control flow matrix, then 35 positions for the data flow matrix).

In each matrix, one or several edges for a minimal solution for the problem have been removed.

Explanation of file names with the following examples: all_edges_5_10_4edges.csv, all_edges_5_10_10steps.csv
    - all edges: each edge in a (solved) matrix has been removed
    - 5_10: minimum and maximum values for x and y as the input
    - 4edges: exact number of edges that have been removed in each problem
    - 10steps: maximum number of removed edges; the file contains problems with 1 to 10 removed edges
"""