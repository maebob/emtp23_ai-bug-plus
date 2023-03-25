import os
import json
import random
import re

import sys
import os
from dotenv import load_dotenv

# load the .env file
load_dotenv()
# append the absolute_project_path from .env variable to the sys.path
sys.path.append(os.environ.get('absolute_project_path'))

from typing import List
from src.engine.eval import main as eval_engine


def read_config(file: str) -> dict:
    """Read a config file."""
    with open(file, "r") as f:
        return json.load(f)


def read_all_configs(folder: str) -> List[dict]:
    """Read all configs in a folder."""
    configs = []
    for file in os.listdir(folder):
        if file.endswith(".json"):
            filename = os.fsdecode(file).replace(".json", "")
            configs.append(
                {
                    "filename": filename,
                    "config": read_config(folder + "/" + file)
                })
    return configs

def calculate_result(formula: str, x, y) -> int:
    """Calculate the result of a formula.
    
    Arguments:
        formula {str} -- The formula to calculate.
        x {int} -- The x value.
        y {int} -- The y value.
    """
    formula = formula.replace("_", "+")
    
    # convert the formula to a python expression
    search_result = re.search("\dx", formula)
    if search_result:
        search_result = search_result.group()
        formula = formula.replace(search_result, f"{search_result.replace('x', '')}*x")
    
    search_result = re.search("\dy", formula)
    if search_result:
        search_result = search_result.group()
        formula = formula.replace(search_result, f"{search_result.replace('y', '')}*y")

    # calculate the result
    return formula, eval(formula)



def test_config(formula: str, config: dict) -> bool:
    """Test a config."""

    # Test with 5 diffrent inputs
    for i in range(5):
        # generate random inputs
        x = random.randint(3, 8)
        y = random.randint(3, 8)

        # calculate the result with the formula
        formula, result = calculate_result(formula, x, y)

        # replace the inputs in the config
        config["xValue"] = x
        config["yValue"] = y

        try:
            engine_result = eval_engine(config).get("0_Out")
        except:
            print("*** ERROR ***")
            print("Failed: " + formula)
            print(f"Inputs: x={x}, y={y}")
            print(f"Result: {result}")
            print("Engine Result: None")
            print("\n"*3)
            raise Exception("Config does not run")

        # check if the result is incorrect
        if result != engine_result:
            print("*** FAILED ***")
            print("Failed: " + formula)
            print(f"Inputs: x={x}, y={y}")
            print(f"Result: {result}")
            print(f"Engine Result: {engine_result}")
            print("\n"*3)
            raise Exception("Config gives wrong result")


if __name__ == "__main__":
    configs = read_all_configs("heuristics/Configs_3_bugs")

    for config in configs:
        test_config(config.get("filename"), config.get("config"))
