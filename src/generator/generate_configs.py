import numpy as np
from itertools import combinations
import sys
import os
from dotenv import load_dotenv
import json
from typing import List

# load the .env file
load_dotenv()
# append the absolute_project_path from .env variable to the sys.path
sys.path.append(os.environ.get('absolute_project_path'))
from src.engine.test_configs import test_config, calculate_result
from src.translation.json_to_matrix import create_matrices

def delete_edges(array: np.ndarray, num_edges: int) -> np.ndarray:
    """
    Create all permutations of an array with a the exact number and less deleted edges.

    Args:
    array (np.ndarray): A flat numpy array.
    num_edges (int): The number of edges to delete.

    Returns:
    A numpy array of shape (n, m), where n is the number of permutations and m is the length of the input array.

    """
    if num_edges > len(array):
        num_edges = len(array)

    # Create all possible combinations of edge indices to delete
    edge_indices = list(combinations(range(len(array)), num_edges))

    # Create all possible permutations of the array with the specified edges set to 0
    permutations = []
    for indices in edge_indices:
        perm = np.copy(array)
        for index in indices:
            perm[index] = 0
        
        # Check the number of 1 in perm
        if np.count_nonzero(perm) != np.count_nonzero(array):
            permutations.append(perm)

    # Remove duplicates
    unique_permutations = np.unique(permutations, axis=0)

    return unique_permutations

def delete_exact_edges(array: np.ndarray, num_edges: int) -> np.ndarray:
    """
    Create all permutations of an array with a specified number of edges deleted.

    Args:
    array (np.ndarray): A flat numpy array.
    num_edges (int): The number of edges to delete.

    Returns:
    A numpy array of shape (n, m), where n is the number of permutations and m is the length of the input array.

    Raises:
    ValueError: If num_edges is greater than the number of edges in the input array.
    """
    edges = np.where(array == 1)[0]
    if num_edges > len(edges):
        num_edges = len(array)

    # Create all possible combinations of edge indices to delete
    edge_indices = list(combinations(edges, num_edges))

    # Create all possible permutations of the array with the specified edges set to 0
    permutations = []
    for indices in edge_indices:
        perm = np.copy(array)
        for index in indices:
            perm[index] = 0
        # Check the number of 1 in perm
        if np.count_nonzero(perm) == np.count_nonzero(array) - num_edges:
            permutations.append(perm)

    # Remove duplicates
    unique_permutations = np.unique(permutations, axis=0)

    return unique_permutations


def generate(directory: str, num_edges: int, low: int, high: int, all_permutations: bool, output: str) -> None:
    """
    Generate a list of configurations for a set of JSON files.

    Args:
    directory (str): The directory containing the JSON files.
    num_edges (int): The number of edges to delete from each matrix.
    low (int): The lower bound of the range of values for x and y.
    high (int): The upper bound of the range of values for x and y.
    all_permutations (bool): If True, generate all possible permutations of the matrices with the specified number of edges deleted. If False, generate only permutations with exactly the specified number of edges deleted.
    output (str): The filename of the output CSV file.

    Returns:
    None

    Raises:
    None
    """

    result: List[List[int]] = []
    
    # Iterate over all JSON files in the specified directory
    for file in os.listdir(directory):
        if not file.endswith(".json"):
            continue

        with open(f"{directory}/{file}", "r") as f:
            data = json.load(f)

        formula = file.replace(".json", "")

        # Test the configuration
        try:
            test_config(formula=formula, config=data)
        except:
            print(f"Error in {file}")
            continue

        # Create control and data flow matrices
        control, data = create_matrices(data)
        
        # Flatten the matrices
        control = control.flatten()
        data = data.flatten()

        # Append the matrices to each other
        combined = np.concatenate((control, data), axis=0)

        # Create all possible permutations of the matrices with the specified number of edges deleted
        if all_permutations:
            permutations = delete_edges(combined, num_edges)
        else:
            permutations = delete_exact_edges(combined, num_edges)
        
        # Create a list of all the possible configurations
        for config in permutations:
            for x in range(low, high):
                for y in range(low, high):
                    config_result = calculate_result(formula=formula, x=x, y=y)[1]
                    if config_result < 1:
                        continue
                    # Add x, y, and the result in front of the config
                    result.append([x, y, config_result, *config])

    # shuffle the result
    np.random.shuffle(result)
    
    # if the result is longer than 50_000, only take the first 50_000
    if len(result) > 50_000:
        result = result[:50_000]

    # Save the result to a CSV file as integers 
    np.savetxt(output, result, delimiter=";", fmt="%d")
    print(f"Saved {len(result)} configurations to {output}")
    print(f"Length of each configuration: {len(result[0])}")



if (__name__ == "__main__"):
    generate(directory="src/configs", num_edges=4, low=5, high=10, all_permutations=False, output="src/train_data/all_edges_5_10_4edges.csv")
