import json
import numpy as np
from typing import Tuple
import matrix_to_json

def calculate_matrix_size(number_of_bugs: int, control: bool) -> Tuple[int, int]:
    """Calculate the size of a matrix given the number of bugs and a control flag.

    Args:
    number_of_bugs (int): The number of bugs in the matrix.
    control (bool): A flag indicating whether the matrix is controlled or not.

    Returns:
    A tuple containing the number of rows and columns in the matrix.
    """
    if control:
        # If the matrix is controlled, it has number_of_bugs + 2 rows and
        # 2 * number_of_bugs + 1 columns.
        rows = number_of_bugs + 2
        columns = 2 * number_of_bugs + 1
        return rows, columns
    else:
        # If the matrix is not controlled, it has 2 * number_of_bugs + 1 rows and
        # number_of_bugs + 2 columns.
        rows = 2 * number_of_bugs + 1
        columns = number_of_bugs + 2
        return rows, columns


def translate_position(edge):
    """Translate an edge position into row and column indices in the matrix.

    Args:
    edge (dict): A dictionary containing information about the edge.

    Returns:
    A tuple of two integers representing the row and column indices in the matrix.

    Raises:
    ValueError: If the edge type is not "Control" or "Data".
    """
    # Use variable unpacking and dictionary comprehension to access keys
    edge_type = edge["Type"]
    from_bug = {k:v for k,v in edge["from_"].items()}
    to_bug = {k:v for k,v in edge["to"].items()}
    
    if edge_type == "Control":
        # The column index is the bug id * 2 for the right port and bug id * 2 - 1 for the left port
        col_index = from_bug["bugId"] * 2 - (1 if from_bug["port"] == "Left" else 0)
        
        # Special case 0 bug id
        if from_bug["bugId"] == 0:
            col_index = 0
        
        # The row index is the bug id
        row_index = to_bug["bugId"] + (1 if to_bug["bugId"] == 0 and to_bug["port"] == "Right" else 1)
        
        return row_index, col_index
    
    elif edge_type == "Data":
        #TODO: Fix this
        # The row index is the bug id * 2 for the down port and bug id * 2 - 1 for the up port
        row_index = to_bug["bugId"] * 2 - (1 if to_bug["port"] == "Up" else 0)
        
        # Special case 0 bug id
        if to_bug["bugId"] == 0:
            row_index = 0
        
        # The column index is the bug id
        col_index = from_bug["bugId"] + 1

        if from_bug["bugId"] == 0:
            col_index = 0
            if from_bug["port"] == "Down":
                col_index = 1
        
        return row_index, col_index
    
    else:
        raise ValueError("Edge type is not control or data")



def create_matrices(data: dict) -> Tuple[np.ndarray, np.ndarray]:
    """Create a matrix for each language in the JSON file.

    Args:
    data (dict): A dictionary containing information about the program bugs and edges.

    Returns:
    A tuple of two numpy arrays representing the control flow and data flow matrices.
    """

    # Create the matrices
    control_flow_matrix = np.zeros(calculate_matrix_size(
        number_of_bugs=(len(data["bugs"])), control=True), dtype=int)
    data_flow_matrix = np.zeros(calculate_matrix_size(
        number_of_bugs=(len(data["bugs"])), control=False), dtype=int)
    
    # Fill the matrices
    for edge in data.get("edges"):
        if edge.get("Type") == "Control":
            # Set the value in the control flow matrix to 1 at the given position
            control_flow_matrix[translate_position(edge)] = 1
        else:
            # Set the value in the data flow matrix to 1 at the given position
            data_flow_matrix[translate_position(edge)] = 1

    return control_flow_matrix, data_flow_matrix


if __name__ == "__main__":
    import os
    
    directory = "src/configs"
    import sys
    import os
    from dotenv import load_dotenv

    # load the .env file
    load_dotenv()
    # append the absolute_project_path from .env variable to the sys.path
    sys.path.append(os.environ.get('absolute_project_path'))
    from src.engine.test_configs import test_config

    # get all json files in the configs folder
    for file in os.listdir(directory):
        with open(f"{directory}/{file}", "r") as f:
            data = json.load(f)

        control, data = create_matrices(data)
        # print("control:\n", control)
        # print("data:\n", data)
        config = matrix_to_json.main(control, data, 4, 5)
        formula = file.replace(".json", "")
        test_config(formula, config)

        if formula == "2y-2":
            # Save the json file
            with open(f"{formula}_test.json", "w") as f:
                json.dump(config, f, indent=4)
