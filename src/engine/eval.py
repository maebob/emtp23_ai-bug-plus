from itertools import count
import json
import sys
import os

from dotenv import load_dotenv

# load the .env file
load_dotenv()
# append the absolute_project_path from .env variable to the sys.path
sys.path.append(os.environ.get('absolute_project_path'))

# sys.path.append('/Users/mayte/github/bugplusengine') # Mayte
# sys.path.append('/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/') # Mae
# sys.path.append('/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/') # Aaron

from src.engine.boardTypes import EdgeType, PortType, Bug, Edge

memory_ports = {}
memory_connections = {}
memory_bug_types = {}
ITERATIONS = 0 # The number of iterations the engine has run
MAX_ITERATIONS = 10 # The maximum number of iterations the engine is allowed to run

def stack_size2a(size=2):
    """
    Get stack size for caller's frame.
    This is used to analyse the stack size of the caller's frame. (recursion depth)
    """
    frame = sys._getframe(size)

    for size in count(size):
        frame = frame.f_back
        if not frame:
            return size


def print_memory():
    """Print the memory"""
    print("Ports")
    print(json.dumps(memory_ports, indent=4))
    print("Connections")
    print(json.dumps(memory_connections, indent=4))
    print("Bug Types")
    print(json.dumps(memory_bug_types, indent=4))


def print_memory_of_bug(bug_id: int) -> None:
    """
    Print the memory of a bug

    Arguments:
        bug_id {int} -- The id of the bug to print the memory of
    """
    print(f"Ports of bug {bug_id}")
    print(json.dumps({k: v for k, v in memory_ports.items()
          if k.startswith(f"{bug_id}_")}, indent=4))
    print(f"Connections of bug {bug_id}")
    print(json.dumps({k: v for k, v in memory_connections.items()
          if k.startswith(f"{bug_id}_")}, indent=4))


def initialize_port_memory(bug_id: int) -> None:
    """
    Initialize all port values in memory to None for a given bug id

    Arguments:
        bug_id {int} -- the id of the bug to be initialized
    """
    for port in PortType:
        memory_ports[f"{bug_id}_{port.value}"] = None


def initialize_connection_memory(edges: Edge) -> None:
    """
    Initialize the connection memory

    Arguments:
        edges {list} -- The edges of the board or nested bug

    """
    for edge in edges:
        # Get the Info where the edge is coming from
        try:
            from_bugId = edge.get("from_").get("bugId")
            from_port = edge.get("from_").get("port")
        except AttributeError:
            raise AttributeError(
                "The edge does not have a from_ attribute please check the config schema")

        # Get the Info where the edge is going to
        try:
            to_bugId = edge.get("to").get("bugId")
            to_port = edge.get("to").get("port")
        except AttributeError:
            raise AttributeError(
                "The edge does not have a to attribute please check the config schema")

        # Write the connection to memory and check for the type of the edge as control edges are a string and data edges are a list
        if edge.get("Type") == EdgeType.Control.value:
            # If it is a control edge we can just write the connection to memory as only one connection is allowed
            memory_connections[f"{from_bugId}_{from_port}"] = (
                f"{to_bugId}_{to_port}")
            continue

        # If it is a data edge we need to check if there is already a connection as multiple connections are allowed
        if memory_connections.get(f"{from_bugId}_{from_port}") is None:
            # If there is no connection yet we create a new list. This could be optimized in the future if only one connection is needed
            memory_connections[f"{from_bugId}_{from_port}"] = list()
        # Add the connection to the list
        memory_connections[f"{from_bugId}_{from_port}"].append(
            f"{to_bugId}_{to_port}")


def get_next_bug(fromBug: int, fromPort: str) -> int:
    """
    Get the next bug in the chain based on the fromPort and fromBug
    Arguments:
        fromBug {int} -- The id of the bug to get the next bug from
        fromPort {str} -- The port to get the next bug from
    Returns:
        int -- The id of the next bug
    """
    if (memory_connections.get(f"{fromBug}_{fromPort}") is None):
        raise ValueError(
            f"Port {fromPort} of bug {fromBug} is not connected to anything")
    return int(memory_connections[f"{fromBug}_{fromPort}"].split("_")[0])


def get_next_bug_to_evaluate(bug_id: int) -> int:
    """Get the next bug to evaluate based on the control port value

    Arguments:
        bug_id {int} -- The id of the bug to evaluate
    Returns:
        int -- The id of the next bug to evaluate
    """
    if memory_bug_types.get(bug_id) != "plus" and memory_ports.get(f"{bug_id}_{PortType.Left.value}") is None and memory_ports.get(f"{bug_id}_{PortType.Right.value}") is None:
        # This is a nested bug that has not been evaluated yet -> return the first bug in the nested bug
        return int(memory_connections[f"{bug_id}_{PortType.In.value}"].split("_")[0])

    if memory_ports.get(f"{bug_id}_{PortType.Left.value}") == 1:
        # The left control out port is active
        next_bug_id = int(memory_connections.get(
            f"{bug_id}_{PortType.Left.value}").split("_")[0])
        # If the next bug is a plus bug we can return the next bug
        if memory_bug_types.get(next_bug_id) == "plus":
            return next_bug_id
        # If the next bug is nested and we are currently inside it (Conected to a control out port) jump to the next bug
        if memory_bug_types.get(next_bug_id) != "plus" and "Out" in memory_connections.get(f"{bug_id}_{PortType.Left.value}"):
            return get_next_bug_to_evaluate(next_bug_id)
        # If the next bug is nested and we are currently outside it (Conected to a control in port) jump to nested bug
        return next_bug_id
    elif memory_ports.get(f"{bug_id}_{PortType.Right.value}") == 1:
        # The right control out port is active
        next_bug_id = int(memory_connections.get(
            f"{bug_id}_{PortType.Right.value}").split("_")[0])
        # If the next bug is a plus bug we can return the next bug
        if memory_bug_types.get(next_bug_id) == "plus":
            return next_bug_id
        # If the next bug is nested and we are currently inside it (Conected to a control out port) jump to the next bug
        if memory_bug_types.get(next_bug_id) != "plus" and "Out" in memory_connections.get(f"{bug_id}_{PortType.Right.value}"):
            return get_next_bug_to_evaluate(next_bug_id)
        # If the next bug is nested and we are currently outside it (Conected to a control in port) jump to nested bug
        return next_bug_id
    else:
        raise Exception("Something went wrong", memory_ports.get(
            f"{bug_id}_{PortType.Left.value}"), memory_ports.get(f"{bug_id}_{PortType.Right.value}"))


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
        if up + down == 0:
            return 0, 0
        return up + down, 1
    else:
        raise Exception(
            f"Something went wrong while evaluating the plus bug whith the following values up:{up} and down:{down}")


def write_to_memory(bug_id: int, port: str, value: int) -> None:
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
    if ports is None:
        return
    for port in ports:
        write_to_memory(port.split("_")[0], port.split("_")[1], data_value)


def read_from_memory(bug_id: int, port: str) -> int:
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
        bug_id {int} -- The id of the bug
        control_value {int} -- The value to set the control flow to 0 is left and 1 is right
    Returns:
        int -- The id of the next bug to evaluate

    """
    if control_value == 0:
        # bugs left control out port is active
        # Activate the left control out port
        write_to_memory(bug_id, PortType.Left.value, 1)
        # Deactivate the right control out port
        write_to_memory(bug_id, PortType.Right.value, 0)
        # Get the id of the next bug based on the left control out port
        return get_next_bug(bug_id, PortType.Left.value)
    elif control_value == 1:
        # bugs right control out port is active
        # Deactivate the left control out port
        write_to_memory(bug_id, PortType.Left.value, 0)
        # Activate the right control out port
        write_to_memory(bug_id, PortType.Right.value, 1)
        # Get the id of the next bug based on the right control out port
        return get_next_bug(bug_id, PortType.Right.value)


def initialize_bug_memory(bug: Bug) -> None:
    """
    Initialize a bug in all the memory structures
    Arguments:
        bug {Bug} -- The bug to initialize
    """
    # Set the bug type
    memory_bug_types[bug.get("id")] = bug.get("Type")
    if bug.get("Type") != "plus":
        initialize_connection_memory(bug.get("edges"))
        initialize_port_memory(bug.get("id"))
        for bug in bug.get("bugs"):
            initialize_bug_memory(bug)
        return

    initialize_port_memory(bug.get("id"))


def initialize_board_memory(board: Bug) -> int:
    """Initialize the memory of the board

    Arguments:
        board {Bug} -- The board to initialize the memory for
    Returns:
        int -- The id of the first bug to evaluate
    """
    initialize_port_memory(board.get("id"))
    # Set the data input value of the upper parent bug
    write_to_memory(board.get("id"), PortType.Up.value, board.get("xValue"))
    # Set the data input value of the lower parent bug
    write_to_memory(board.get("id"), PortType.Down.value, board.get("yValue"))
    write_to_memory(board.get("id"), PortType.In.value,
                    1)  # Activate the parent bug

    initialize_connection_memory(board.get("edges"))

    memory_bug_types[board.get("id")] = "root"

    for bug in board.get("bugs"):
        initialize_bug_memory(bug)

    # Set all concected Data ports to 0 otherwise they will be None
    for key, value in memory_connections.items():
        # if value is a list (only data ports are lists)
        if not isinstance(value, list):
            continue
        for data_port in value:
            write_to_memory(data_port.split(
                "_")[0], data_port.split("_")[1], 0)

    # Set initial values to data ports
    # Write the data to the upper child bug
    if (memory_connections.get(f"{board.get('id')}_{PortType.Up.value}") is not None):
        wirte_data_to_memory(memory_connections.get(
            f"{board.get('id')}_{PortType.Up.value}"), board.get("xValue"))
    #write_to_memory(upper_data_to_node_id, upper_data_to_port, up)
    # Write the data to the lower child bug
    if (memory_connections.get(f"{board.get('id')}_{PortType.Down.value}") is not None):
        wirte_data_to_memory(memory_connections.get(
            f"{board.get('id')}_{PortType.Down.value}"), board.get("yValue"))

    return get_next_bug(board.get("id"), PortType.In.value)


def write_control_to_parent_bug(bug_id: int) -> None:
    """Write the control value to the parent bug

    Arguments:
        bug_id {int} -- The id of the bug to write the control value to
    """

    if memory_connections.get(f"{bug_id}_{PortType.Left.value}") is not None:
        memory_ports[memory_connections.get(
            f"{bug_id}_{PortType.Left.value}")] = memory_ports[f"{bug_id}_{PortType.Left.value}"]
    if (memory_ports[f"{bug_id}_{PortType.Left.value}"] == 1 and memory_connections.get(f"{bug_id}_{PortType.Right.value}") is not None and memory_connections.get(f"{bug_id}_{PortType.Left.value}") == memory_connections.get(f"{bug_id}_{PortType.Right.value}")):
        # If the left control out port is active and the left and right control out ports are connected to the same port dont write the value to the port again as otherwise the one will be overwritten
        return
    if (memory_connections.get(f"{bug_id}_{PortType.Right.value}") is not None):
        memory_ports[memory_connections.get(
            f"{bug_id}_{PortType.Right.value}")] = memory_ports[f"{bug_id}_{PortType.Right.value}"]


def evaluate_plus_bug(bug_id: int) -> int:
    """Evaluate a plus bug

    Arguments:
        bug_id {int} -- The id of the bug to evaluate
    Returns:
        int -- The id of the next bug to evaluate
    """
    # Activate bug
    write_to_memory(bug_id, PortType.In.value, 1)
    # Evaluate the plus bug
    up = read_from_memory(bug_id, PortType.Up.value)
    down = read_from_memory(bug_id, PortType.Down.value)

    data_value, control_value = calculate_plus_bug(up, down)

    # Write the results to the port itself
    write_to_memory(bug_id, PortType.Out.value, data_value)
    set_control_value(bug_id, control_value)

    # Write the results to the connected ports
    if memory_connections.get(f"{bug_id}_{PortType.Out.value}") is not None:
        wirte_data_to_memory(memory_connections.get(
            f"{bug_id}_{PortType.Out.value}"), data_value)

    # If the next bug is not a plus bug, set the control value
    if (control_value == 0 and memory_bug_types.get(get_next_bug(bug_id, PortType.Left.value)) != "plus"):
        write_control_to_parent_bug(bug_id)
    elif (control_value == 1 and memory_bug_types.get(get_next_bug(bug_id, PortType.Right.value)) != "plus"):
        write_control_to_parent_bug(bug_id)

    return get_next_bug_to_evaluate(bug_id)


def evaluate_nested_bug(bug_id: int, parent_bug_id: int = None) -> None:
    """Evaluate a nested bug
    Arguments:
        bug_id {int} -- The id of the bug to evaluate
        parent_bug_id {int} -- The id of the parent bug
    """
    #print(stack_size2a(), bug_id, parent_bug_id)
    # Write data to the nested bug ports
    if (memory_ports.get(f"{bug_id}_{PortType.Up.value}") is not None):
        wirte_data_to_memory(memory_connections.get(
            f"{bug_id}_{PortType.Up.value}"), read_from_memory(bug_id, PortType.Up.value))
    if (memory_ports.get(f"{bug_id}_{PortType.Down.value}") is not None):
        wirte_data_to_memory(memory_connections.get(
            f"{bug_id}_{PortType.Down.value}"), read_from_memory(bug_id, PortType.Down.value))

    if (memory_ports.get(f"{bug_id}_{PortType.In.value}") == 0 or memory_ports.get(f"{bug_id}_{PortType.In.value}") is None):
        pass
    write_to_memory(bug_id, PortType.In.value, 1)

    # Evaluate the nested bug
    next_bug_id = get_next_bug_to_evaluate(bug_id)
    while next_bug_id != bug_id:
        if (memory_bug_types.get(next_bug_id) == "plus"):
            next_bug_id = evaluate_plus_bug(next_bug_id)
        elif (memory_bug_types.get(next_bug_id) != "plus"):
            next_bug_id = evaluate_nested_bug(next_bug_id, bug_id)
        else:
            raise Exception("Unknown bug type")

    wirte_data_to_memory(memory_connections.get(
        f"{bug_id}_{PortType.Out.value}"), read_from_memory(bug_id, PortType.Out.value))

    # Go to the next bug
    if (memory_ports.get(f"{bug_id}_{PortType.Left.value}") == 1):
        next_bug_id = get_next_bug(bug_id, PortType.Left.value)
    elif (memory_ports.get(f"{bug_id}_{PortType.Right.value}") == 1):
        next_bug_id = get_next_bug(bug_id, PortType.Right.value)
    else:
        raise Exception(
            f"Control port not set => Bug ({bug_id}) is not connected to the next bug")

    if next_bug_id == None:
        # Print the memory of the current bug
        print_memory_of_bug(bug_id)
        raise Exception("No next bug found")

    if parent_bug_id == next_bug_id or memory_bug_types.get(next_bug_id) == "root":
        # if we sep out of a nested bug or if we are at the root bug we need to set the control value
        write_control_to_parent_bug(bug_id)
        write_to_memory(bug_id, PortType.Left.value, None)
        write_to_memory(bug_id, PortType.Right.value, None)
        return next_bug_id

    # Reset the control ports of the nested bug
    write_to_memory(bug_id, PortType.Left.value, None)
    write_to_memory(bug_id, PortType.Right.value, None)

    return next_bug_id


def eval_bug(bug_id: int) -> None:
    """Evaluate the main bug that was selected by the user
    Arguments:
        bug_id {int} -- The id of the bug to evaluate
    """
    if bug_id is None:
        raise Exception(
            "No bug selected therefore no evaluation possible -> Problem in configuration")
    
    # Increment the global iteration counter
    global ITERATIONS
    
    while memory_bug_types.get(bug_id) != "root" and ITERATIONS < MAX_ITERATIONS:
        ITERATIONS = ITERATIONS + 1
        if memory_bug_types.get(bug_id) == "plus":
            bug_id = evaluate_plus_bug(bug_id)
        elif memory_bug_types.get(bug_id) != "plus":
            bug_id = evaluate_nested_bug(bug_id)
        else:
            raise Exception("Unknown bug type")
    
    # Stop the evaluation if it took # too long
    if ITERATIONS >= MAX_ITERATIONS:
        raise TimeoutError("Evaluation took too long")

def main(board: Bug) -> dict:
    """The main function of the program
    Arguments:
        board {Bug} -- The root bug with all the nested bugs
    Returns:
        dict -- The memory of the root bug
    """
    # To avoid having data stored in the memory of the previous run we reset the memory
    memory_connections.clear()
    memory_ports.clear()
    memory_bug_types.clear()
    ITERATIONS = 0

    # Initialize the memory of the root bug and get the first bug to evaluate
    first_bug_id = initialize_board_memory(board)
    
    eval_bug(first_bug_id)

    return memory_ports


if __name__ == "__main__":
    """This function is only used for testing purposes"""
    # TODO pseudo parallel only works on first itreation
    example_file = open(
        "Configurations/multiply.json", "r").read()
    example_board = json.loads(example_file)
    example_board["xValue"] = 10
    example_board["yValue"] = 1
    main(example_board)
    # print(memory_connections)
    print(memory_ports)
    print("Data out:", memory_ports.get("0_Out"), "Control Left:", memory_ports.get(
        "0_Left"), "Control Right:", memory_ports.get("0_Right"))
    # print(memory_bug_types)
