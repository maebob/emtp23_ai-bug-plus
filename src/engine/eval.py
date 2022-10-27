from multiprocessing import connection
import string
import json

"""
my_memory{
    ports{
        port: value
    }
    connections{
        from_port: [to_ports]
    }
}
"""

memory_ports = {}
memory_connections = {}
memory_bug_types = {}

BUGPORTS = ['dataInUp', 'controlIn', 'dataInDown',
            'controlOutL', 'controlOutR', 'dataOut']


def initialize_port_memory(bug_id: int) -> None:
    """Initialize all port values in memory to None for a given bug id

    Arguments:
        bug_id {int} -- the id of the bug to be initialized
    """
    for port in BUGPORTS:
        memory_ports[f"{bug_id}_{port}"] = None


def initialize_connection_memory(edges: list) -> None:
    """Initialize the connection memory

    Arguments:

    """
    for edge in edges:
        if ("control" in edge["fromPort"].lower()):
            memory_connections[f"{edge['fromNode']}_{edge['fromPort']}"] = (
                f"{edge['toNode']}_{edge['toPort']}")
            continue
        if (memory_connections.get(f"{edge['fromNode']}_{edge['fromPort']}") is None):
            memory_connections[f"{edge['fromNode']}_{edge['fromPort']}"] = list(
            )
        memory_connections[f"{edge['fromNode']}_{edge['fromPort']}"].append(
            f"{edge['toNode']}_{edge['toPort']}")


def get_next_bug(fromBug: int, fromPort: str) -> int:
    """Get the next bug in the chain based on the fromPort and fromBug"""
    if (memory_connections.get(f"{fromBug}_{fromPort}") is None):
        # TODO check if this is needed as ports that are not connected should not be
        return None
    return int(memory_connections[f"{fromBug}_{fromPort}"][0].split("_")[0])


def get_next_bug_to_evaluate(bug_id: int) -> int:
    """Get the next bug to evaluate based on the control port value

    Arguments:
        bug_id {int} -- The id of the bug to evaluate
    Returns:
        int -- The id of the next bug to evaluate
    """
    if (memory_ports.get(f"{bug_id}_controlOutL") is None and memory_ports.get(f"{bug_id}_controlOutR") is None):
        # This is a nested bug that has not been evaluated yet -> return the first bug in the nested bug
        return int(memory_connections[f"{bug_id}_controlIn"].split("_")[0])

    if (read_from_memory(bug_id, "controlOutL") == 1):
        return int(memory_connections[f"{bug_id}_controlOutL"].split("_")[0])
    return int(memory_connections[f"{bug_id}_controlOutR"].split("_")[0])


def calculate_plus_bug(up: int or None, down: int or None) -> int and int:
    """Evaluate the plus bug using the rules of bugsplus

    Arguments:
        up {int or None} -- The value of the upper input data port
        down {int or None} -- The value of the lower input data port
    Returns:
        int and int -- The value of the data port and the value of the control port
    Raises:
        ValueError: If the value of the upper input data port is not None and not an integer
    """
    if (up is None and down is None):
        return 0, 0
    elif (up is None and down is not None):
        return -1, 1
    elif (up is not None and down is None):
        return 1, 1
    elif (up is not None and down is not None):
        if (up + down == 0):
            return 0, 0
        return up + down, 1
    else:
        raise Exception("Something went wrong")


def write_to_memory(bug_id: int, port: string, value: int) -> None:
    """Write a value to a port in memory

    Arguments:
        bug_id {int} -- The id of the bug
        port {string} -- The port to write to
        value {int} -- The value to write to the port
    """
    memory_ports[f"{bug_id}_{port}"] = value


def wirte_data_to_memory(ports: list, data_value: int) -> None:
    """Write the data value to the data ports in memory

    Arguments:
        ports {list} -- The list of ports to write to
        data_value {int} -- The value to write to the ports
    """
    if (ports is None):
        return
    for port in ports:
        write_to_memory(port.split("_")[0], port.split("_")[1], data_value)


def read_from_memory(bug_id: int, port: string) -> int:
    """Read a value from a port in memory

    Arguments:
        bug_id {int} -- The id of the bug
        port {string} -- The port to read from
    Returns:
        int -- The value of the port
    """
    return memory_ports[f"{bug_id}_{port}"]


def set_control_value(bug_id: int, control_value: int) -> int:
    """Set the value of the control flow in memory and return the next port to evaluate

    Arguments:

    """
    if control_value == 0:
        # bugs left control out port is active
        # Activate the left control out port
        write_to_memory(bug_id, "controlOutL", 1)
        # Deactivate the right control out port
        write_to_memory(bug_id, "controlOutR", 0)
        # Get the id of the next bug based on the left control out port
        return get_next_bug(bug_id, "controlOutL")
    elif control_value == 1:
        # bugs right control out port is active
        # Deactivate the left control out port
        write_to_memory(bug_id, "controlOutL", 0)
        # Activate the right control out port
        write_to_memory(bug_id, "controlOutR", 1)
        # Get the id of the next bug based on the right control out port
        return get_next_bug(bug_id, "controlOutR")


def initialize_bug_memory(bug) -> None:
    """Initialize a bug"""
    if "edges" in bug:
        initialize_connection_memory(bug.get("edges"))
        initialize_port_memory(bug.get("id"))
        memory_bug_types[bug.get("id")] = "nested"
        for bug in bug.get("bugs"):
            initialize_bug_memory(bug)
        return
    else:
        memory_bug_types[bug.get("id")] = "plus"
    initialize_port_memory(bug.get("id"))


def initialize_board_memory(board) -> int:
    """Initialize the memory of the board

    Arguments:
        board {object} -- The board to initialize the memory for
    """
    initialize_port_memory(board.get("id"))
    # Set the data input value of the upper parent bug
    write_to_memory(board.get("id"), "dataInUp", board.get("xValue"))
    # Set the data input value of the lower parent bug
    write_to_memory(board.get("id"), "dataInDown", board.get("yValue"))
    write_to_memory(board.get("id"), "controlIn", 1)  # Activate the parent bug

    initialize_connection_memory(board.get("edges"))

    memory_bug_types[board.get("id")] = "root"

    for bug in board.get("bugs"):
        initialize_bug_memory(bug)

    # Set initial values to data ports
    # Write the data to the upper child bug
    if (memory_connections.get(f"{board.get('id')}_dataInUp") is not None):
        wirte_data_to_memory(memory_connections.get(
            f"{board.get('id')}_dataInUp"), board.get("xValue"))
    #write_to_memory(upper_data_to_node_id, upper_data_to_port, up)
    # Write the data to the lower child bug
    if (memory_connections.get(f"{board.get('id')}_dataInDown") is not None):
        wirte_data_to_memory(memory_connections.get(
            f"{board.get('id')}_dataInDown"), board.get("yValue"))

    return get_next_bug(board.get("id"), "controlIn")


def write_control_to_parent_bug(bug_id: int) -> None:
    """Write the control value to the parent bug

    Arguments:
        bug_id {int} -- The id of the bug to write the control value to
    """

    if (memory_connections.get(f"{bug_id}_controlOutL") is not None):
        memory_ports[memory_connections.get(
            f"{bug_id}_controlOutL")] = memory_ports[f"{bug_id}_controlOutL"]
    if (memory_connections.get(f"{bug_id}_controlOutR") is not None):
        memory_ports[memory_connections.get(
            f"{bug_id}_controlOutR")] = memory_ports[f"{bug_id}_controlOutR"]


def evaluate_plus_bug(bug_id: int) -> int:
    """Evaluate a plus bug

    Arguments:
        bug_id {int} -- The id of the bug to evaluate
    Returns:
        int -- The id of the next bug to evaluate
    """
    # Activate bug
    write_to_memory(bug_id, "controlIn", 1)
    # Evaluate the plus bug
    up = read_from_memory(bug_id, "dataInUp")
    down = read_from_memory(bug_id, "dataInDown")
    data_value, control_value = calculate_plus_bug(up, down)

    # Write the results to the port itself
    write_to_memory(bug_id, "dataOut", data_value)
    set_control_value(bug_id, control_value)

    # Write the results to the connected ports
    if (memory_connections.get(f"{bug_id}_dataOut") is not None):
        wirte_data_to_memory(memory_connections.get(
            f"{bug_id}_dataOut"), data_value)

    # If the next bug is not a plus bug, set the control value
    if (control_value == 0 and memory_bug_types.get(get_next_bug(bug_id, "controlOutL")) != "plus"):
        write_control_to_parent_bug(bug_id)
    elif (control_value == 1 and memory_bug_types.get(get_next_bug(bug_id, "controlOutR")) != "plus"):
        write_control_to_parent_bug(bug_id)

    return get_next_bug_to_evaluate(bug_id)


def evaluate_nested_bug(bug_id: int) -> None:
    # Check if we have a nested bug

    # Write data to the nested bug ports
    if (memory_ports.get(f"{bug_id}_dataInUp") is not None):
        wirte_data_to_memory(memory_connections.get(
            f"{bug_id}_dataInUp"), read_from_memory(bug_id, "dataInUp"))
    if (memory_ports.get(f"{bug_id}_dataInDown") is not None):
        wirte_data_to_memory(memory_connections.get(
            f"{bug_id}_dataInDown"), read_from_memory(bug_id, "dataInDown"))

    if (memory_ports.get(f"{bug_id}_controlIn") == 0 or memory_ports.get(f"{bug_id}_controlIn") is None):
        write_to_memory(bug_id, "controlIn", 1)
        # Evaluate the nested bug
        next_bug_id = get_next_bug_to_evaluate(bug_id)
        eval_bug(next_bug_id)

    # Set the control value of the nested bug
    if (memory_ports.get(f"{bug_id}_dataOut") != 0):
        write_to_memory(bug_id, "controlOutL", 0)
        write_to_memory(bug_id, "controlOutR", 1)
    else:
        write_to_memory(bug_id, "controlOutL", 1)
        write_to_memory(bug_id, "controlOutR", 0)

    # Go to the next bug
    if (memory_connections.get(f"{bug_id}_controlOutL") == 1):
        next_bug_id = get_next_bug(bug_id, "controlOutL")
        eval_bug(next_bug_id)
    else:
        next_bug_id = get_next_bug(bug_id, "controlOutR")
        eval_bug(next_bug_id)

    # deactivate the control port of the nested bug
    write_to_memory(bug_id, "controlIn", 0)

    wirte_data_to_memory(memory_connections.get(
        f"{bug_id}_dataOut"), read_from_memory(bug_id, "dataOut"))


def eval_bug(bug_id) -> None:
    if (memory_bug_types.get(bug_id) == "root"):
        return
    elif (memory_bug_types.get(bug_id) == "nested"):
        evaluate_nested_bug(bug_id)
        if (memory_ports.get(f"{bug_id}_controlOutL") == 1 and memory_bug_types.get(get_next_bug(bug_id, "controlOutL")) != "plus"):
            write_control_to_parent_bug(bug_id)
        elif (memory_ports.get(f"{bug_id}_controlOutR") == 1 and memory_bug_types.get(get_next_bug(bug_id, "controlOutR")) != "plus"):
            write_control_to_parent_bug(bug_id)
        return
    elif (memory_bug_types.get(bug_id) == "plus"):
        eval_bug(evaluate_plus_bug(bug_id))

    """Idea deactivate control port after evaluation if a control in port is active at arival we can terminate the evaluation"""


def main(board):
    #global board_main

    first_bug_id = initialize_board_memory(board)
    eval_bug(first_bug_id)

    return memory_ports


if __name__ == "__main__":
    """example_file = open(
        "/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/BugsPlusEditor/Configurations/nestedIncrementor.json", "r").read()
    main(json.loads(example_file))
    # print(memory_connections)
    print(memory_ports)
    print(memory_ports.get("0_dataOut"))
    # print(memory_bug_types)"""
    example_file = open("/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/BugsPlusEditor/Configurations/isZero.json", "r").read()
    example = json.loads(example_file)
    print(example)
    assert main(example).get("0_dataOut") == 11
