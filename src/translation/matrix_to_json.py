import math
import json
import numpy as np
import sys
import os
from dotenv import load_dotenv

# load the .env file
load_dotenv()
# append the absolute_project_path from .env variable to the sys.path
sys.path.append(os.environ.get('absolute_project_path'))
from src.api.boardTypes import EdgeType, Edge, PortAdress, PortType


def translate_matrix(matrix_to_translate: np.array, type: EdgeType) -> tuple[list[Edge], list[int]]:
    """
    Translate the matrix to a json.
    Arguments:
        matrix_to_translate {np.Array} -- The matrix to translate
        type {EdgeType} -- The type of the port
    Returns:
        tuple[dict, list[int]] -- The json and the ids of the bugs that are used in the matrix
    """
    return_edges = []
    
    # get coordinates from the matrix where the value is 1
    coordinates = np.argwhere(matrix_to_translate == 1)
    if type == EdgeType.Control:
        # if the coloum number is odd it is the left port if it is even it is the right port unless it is the 0th column
        for coordinate in coordinates:
            # Get the from and to coordinates
            from_coordinate = coordinate[1] # row
            to_coordinate = coordinate[0] # coloum

            # Special case for the 0th column
            if from_coordinate == 0:
                from_port = {
                "bugId": 0,
                "port": PortType.In.value
            }
            else:
                # Bug id for from is allways the column index / 2 and rounded up
                # Create the from Port Adress
                from_port = {
                    "bugId": math.ceil(from_coordinate / 2),
                    "port": PortType.Left.value if from_coordinate % 2 == 1 else PortType.Right.value
                }

            # special case for the 0th and 1st row
            if to_coordinate == 0 or to_coordinate == 1:
                to_port = {
                    "bugId": 0,
                    "port": PortType.Left.value if to_coordinate == 0 else PortType.Right.value
                }
            else:
                # Create the to Port Adress
                to_port = {
                    "bugId": int(to_coordinate-1),
                    "port": PortType.In.value
                }

            # Add the edge to the list
            return_edges.append({"from_": from_port, "to": to_port, "Type": type.value})
    else:
        for coordinate in coordinates:
            # Get the from and to coordinates
            from_coordinate = coordinate[1]
            to_coordinate = coordinate[0]

            # Special case for the 0th and 1st column
            if from_coordinate == 0 or from_coordinate == 1:
                from_port = {
                    "bugId": 0,
                    "port": PortType.Up.value if from_coordinate == 0 else PortType.Down.value
                }
            else:
                # Create the from Port Adress
                from_port = {
                    "bugId": int(from_coordinate-1),
                    "port": PortType.Out.value
                }

            # special case for the 0th row
            if to_coordinate == 0:
                to_port = {
                    "bugId": 0,
                    "port": PortType.Out.value
                }
            else:
                # Create the to Port Adress
                to_port = {
                    "bugId": math.ceil(to_coordinate / 2),
                    "port": PortType.Up.value if to_coordinate % 2 == 1 else PortType.Down.value
                }

            # Add the edge to the list
            return_edges.append({"from_": from_port, "to": to_port, "Type": type.value})

    return return_edges

def main(control_matrix: np.array, data_matrix: np.array, data_up: int, data_down: int) -> dict:
    """
    Translate the matrix to a json.
    Arguments:
        control_matrix {np.Array} -- The control matrix to translate
        data_matrix {np.Array} -- The data matrix to translate
        data_up {int} -- The number of data bugs on the up side
        data_down {int} -- The number of data bugs on the down side
    Returns:
        dict -- The json
    """
    # Check if the control matrix less more columns than the data matrix
    if control_matrix.shape[1] < data_matrix.shape[1]:
        # This should never happen -> raise error
        raise ValueError("The control matrix has less columns than the data matrix")
    
    # Get all bugs used in the matrix
    bugs = list(set(np.argwhere(control_matrix == 1).flatten().tolist() + np.argwhere(data_matrix == 1).flatten().tolist()))
    bugs = [math.ceil(bug / 2) for bug in bugs]
    bugs = list(set(bugs))
    # delete the 0th bug
    if 0 in bugs:
        bugs.remove(0)
    json_bugs = [{"id": bug, "bugs": [], "edges": [], "Type": "plus"} for bug in bugs]
        

    # Get the edges from the matrices
    control_edges = translate_matrix(control_matrix, EdgeType.Control)
    data_edges = translate_matrix(data_matrix, EdgeType.Data)

    # Create the json
    json = {
        "id": 0,
        "xValue": data_up,
        "yValue": data_down,
        "Type": "root",
        "bugs": json_bugs,
        "edges": control_edges + data_edges
    }

    return json

if __name__ == "__main__":
    control_matrix_incrementor = np.array([
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
        ])
    data_matrix_incrementor = np.array([
        [0, 0, 1, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ])
    matrix = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0])

    config = main(control_matrix=matrix[:35].reshape(3 + 2, 2 * 3 + 1), data_matrix=matrix[35:].reshape(2 * 3 + 1, 3 + 2), data_up=1, data_down=1)
    # write config to json file
    with open('config_test2.json', 'w') as outfile:
        json.dump(config, outfile, indent=4)
    