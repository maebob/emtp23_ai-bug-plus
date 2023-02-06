import os
import json
import random
import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TableRow:
    """A table row."""
    formula: str
    src: int
    dst: int
    edge_type: str
    src_port: str
    dst_port: str
    src_value: Optional[int] = None
    dst_value: Optional[int] = None


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

def format_formula(formula: str) -> int:
    """Format the formula to a python expression.
    
    Arguments:
        formula {str} -- The formula to calculate.
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

    # return the formatted formula
    return formula

def calculate_result(formula: str, x, y) -> int:
    """Calculate the result of a formula.

    Arguments:
        formula {str} -- The formula to calculate.
        x {int} -- The x value.
        y {int} -- The y value.
    """
    # replace the inputs in the formula
    formula = formula.replace("x", str(x))
    formula = formula.replace("y", str(y))
    return eval(formula)


def get_all_bugs(config: dict) -> List[int]:
    """Get all bugs from a config.
    
    Arguments:
        config {dict} -- The config to get the bugs from.
    """
    bugs = []
    # Add the root bug
    bugs.append(0)
    for bug in config.get("bugs"):
        bugs.append(bug.get("id"))
    return bugs

def translate_bug_ids(bugs: List[int]) -> dict[int]:
    """Translate the bug ids to the correct bug ids.
    For the graphs we need the ids to start at 0 and count up.
    
    Arguments:
        bugs {List[int]} -- The bugs to translate.
    """
    bug_ids = {}
    for i, bug in enumerate(bugs):
        bug_ids[bug] = i
    return bug_ids

def json_to_graph(json: dict, formula: str, up: int, down: int) -> List[List[int]]:
    """Convert a json to a graph.
    
    Arguments:
        json {dict} -- The json to convert.
        formula {str} -- The formula to calculate.
        up {int} -- The up value.
        down {int} -- The down value.
    """
    all_bugs = get_all_bugs(json)
    bug_ids = translate_bug_ids(all_bugs)

    # calculate the result of the root bug
    result = calculate_result(formula, up, down)

    graph = []
    # Loop over the edges
    for edge in json.get("edges"):
        #get source and destination
        source_id = bug_ids.get(edge.get("from_").get("bugId"))
        source_port = edge.get("from_").get("port")
        destination_id = bug_ids.get(edge.get("to").get("bugId"))
        destination_port = edge.get("to").get("port")

        # Get the type of the edge
        edge_type = edge.get("Type")

        # if source is the root bug
        if source_id == 0 and edge_type == "Data":
            if source_port == "Up":
                source_value = up
            elif source_port == "Down":
                source_value = down
            else:
                # should not happen
                raise Exception("Unknown source")
            graph.append(TableRow(formula, source_id, destination_id, edge_type, source_port, destination_port, source_value))
        # if destination is the root bug
        if destination_id == 0 and edge_type == "Data":
            print("Destination is root bug")
            destination_value = result
            graph.append(TableRow(formula, source_id, destination_id, edge_type, source_port, destination_port, None, destination_value))

        graph.append(TableRow(formula, source_id, destination_id, edge_type, source_port, destination_port))
    return graph

def generate_graph(formula: str, config: dict) -> bool:
    """Test a config."""

    x = random.randint(-10, 10)
    y = random.randint(-10, 10)

    # Format the formula
    formula = format_formula(formula)

    return json_to_graph(config, formula, x, y)



if __name__ == "__main__":
    configs = read_all_configs("heuristics/Configs_3_bugs")

    graphs = []
    for config in configs:
        graph = generate_graph(config.get("filename"), config.get("config"))
        graphs.append(graph)
    
    # Write the graphs to a csv file with ; as seperator
    with open("graphs.csv", "w") as f:
        # Write the header
        f.write("formula;src;dst;edge_type;src_port;dst_port;src_value;dst_value")

        # Write the graphs
        for graph in graphs:
            for row in graph:
                f.write(f"\n{row.formula};{row.src};{row.dst};{row.edge_type};{row.src_port};{row.dst_port};{row.src_value};{row.dst_value}")
            break


