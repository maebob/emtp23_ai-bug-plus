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

BUGPORTS = ['dataInUp', 'controlIn', 'dataInDown',
             'controlOutL', 'controlOutR', 'dataOut']


def initialize_port_memory(bug_id: int) -> None:
    """Initialize all port values in memory to None for a given bug id
    
    Arguments:
        bug_id {int} -- the id of the bug to be initialized
    """
    for port in BUGPORTS:
       memory_ports[f"{bug_id}_{port}"] = None


def initialize_child_port_memory(bugs: list) -> None:
    """Initialize all port values in memory to None for a given list of bugs
    
    Arguments:

    """
    for bug in bugs:
        initialize_port_memory(bug["id"])


def initialize_connection_memory(edges: list) -> None:
    """Initialize the connection memory

    Arguments:

    """
    for edge in edges:
        if ("control" in edge["fromPort"].lower()):
            memory_connections[f"{edge['fromNode']}_{edge['fromPort']}"] = (f"{edge['toNode']}_{edge['toPort']}")
            continue
        if (memory_connections.get(f"{edge['fromNode']}_{edge['fromPort']}") is None):
            memory_connections[f"{edge['fromNode']}_{edge['fromPort']}"] = list()
        memory_connections[f"{edge['fromNode']}_{edge['fromPort']}"].append(f"{edge['toNode']}_{edge['toPort']}")


def get_next_bug(fromBug: int, fromPort: str) -> int:
    """Get the next bug in the chain based on the fromPort and fromBug"""
    if (memory_connections.get(f"{fromBug}_{fromPort}") is None):
        #TODO check if this is needed as ports that are not connected should not be
        return None
    return int(memory_connections[f"{fromBug}_{fromPort}"][0].split("_")[0])


def get_next_port(fromBug: int, fromPort: str) -> str:
    """Get the next port in the chain based on the fromPort and fromBug

    Arguments:

    """
    if (memory_connections.get(f"{fromBug}_{fromPort}") is None):
        #TODO check if this is needed as ports that are not connected should not be
        return None
    return memory_connections[f"{fromBug}_{fromPort}"][0].split("_")[1]


def eval_plus_bug(up: int or None, down: int or None) -> int and int:
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


def read_from_memory(bug_id: int, port: string) -> int:
    """Read a value from a port in memory

    Arguments:
        bug_id {int} -- The id of the bug
        port {string} -- The port to read from
    Returns:
        int -- The value of the port
    """
    return memory_ports[f"{bug_id}_{port}"]


def set_control_value(bug: object, control_value: int) -> int:
    """Set the value of the control flow in memory and return the next bug id to evaluate

    Arguments:

    """
    if control_value == 0:
        # bugs left control out port is active
        # Activate the left control out port
        write_to_memory(bug["id"], "controlOutL", 1)
        # Deactivate the right control out port
        write_to_memory(bug["id"], "controlOutR", 0)
        # Get the id of the next bug based on the left control out port
        return get_next_bug(bug.get("id"), "controlOutL")
    elif control_value == 1:
        # bugs right control out port is active
        # Deactivate the left control out port
        write_to_memory(bug["id"], "controlOutL", 0)
        # Activate the right control out port
        write_to_memory(bug["id"], "controlOutR", 1)
        # Get the id of the next bug based on the right control out port
        return get_next_bug(bug.get("id"), "controlOutR")


def eval_bug(bug, up, down) -> None:
    if ("id" not in bug):
        """Initialize memory for main bug"""
        initialize_port_memory(0)
        # Set the data input value of the upper parent bug
        write_to_memory(0, "dataInUp", up)
        # Set the data input value of the lower parent bug
        write_to_memory(0, "dataInDown", down)
        write_to_memory(0, "controlIn", 1)  # Activate the parent bug

        initialize_connection_memory(board_main.get("edges"))

        """Connect the parent bugs data ports to the children"""
        initialize_child_port_memory(
            bug["bugs"])  # Initialize the memory for the child bugs to be able to write to them in the future
        # Get the id of the upper child bug
        upper_data_to_node_id = get_next_bug(0, "mainDataInUp")
        # Get the id of the lower child bug
        lower_data_to_node_id = get_next_bug(0, "mainDataInDown")
        # Get the port of the upper child bug TODO this could have multiple bugs connected to it
        upper_data_to_port = get_next_port(0, "mainDataInUp")
        # Get the port of the lower child bug TODO this could have multiple bugs connected to it
        lower_data_to_port = get_next_port(0, "dataInDown")
        # Write the data to the upper child bug
        write_to_memory(upper_data_to_node_id, upper_data_to_port, up)
        # Write the data to the lower child bug
        write_to_memory(lower_data_to_node_id, lower_data_to_port, down)

    if ("bugs" not in bug):
        """The bug is a leaf node -> Plus bug"""

        # Activate the bugs control port
        write_to_memory(bug["id"], "controlIn", 1)
        data_value, control_value = eval_plus_bug(up, down)  # Evaluate the bug
        # Write the result to the data port of the evaluated bug
        write_to_memory(bug["id"], "dataOut", data_value)

        #Update all connected data in ports
        data_ports_to_update = memory_connections.get(f"{bug.get('id')}_dataOut")
        for data_port in data_ports_to_update:
            write_to_memory(int(data_port.split("_")[0]), data_port.split("_")[1], data_value)

    elif (len(bug["bugs"]) != 0):
        """The bug is a parent node"""
        for child in bug["bugs"]:
            # Evaluate the child bugs
            eval_bug(child, read_from_memory(
                child["id"], "dataInUp"), read_from_memory(child["id"], "dataInDown"))
    else:
        raise Exception("Something went wrong")


def main(board, up, down):
    global board_main
    board_main = board
    eval_bug(board, up, down)
    return read_from_memory(0, "mainDataOut")


if __name__ == "__main__":
    example_file = open("/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/BugsPlusEditor/Configurations/incrementor.json", "r").read()
    print(main(json.loads(example_file), 9, None))
    print(memory_connections)
