import string

addition = {
    "bugs": [
        {
            "id": 1,
        },
        {
            "id": 2,
        },
        {
            "id": 3,
        }

    ],
    "edges": [
        {
            "fromNode": 0,
            "toNode": 1,
            "fromPort": "mainControlIn",
            "toPort": "controlIn"
        },
        {
            "fromNode": 1,
            "toNode": 2,
            "fromPort": "controlOutL",
            "toPort": "controlIn"
        },
        {
            "fromNode": 1,
            "toNode": 2,
            "fromPort": "controlOutR",
            "toPort": "controlIn"
        },
        {
            "fromNode": 2,
            "toNode": 3,
            "fromPort": "controlOutL",
            "toPort": "controlIn"
        },
        {
            "fromNode": 2,
            "toNode": 3,
            "fromPort": "controlOutR",
            "toPort": "controlIn"
        },
        {
            "fromNode": 1,
            "toNode": 2,
            "fromPort": "dataOut",
            "toPort": "dataInDown"
        },
        {
            "fromNode": 0,
            "toNode": 3,
            "fromPort": "mainDataInUp",
            "toPort": "dataInDown"
        },
        {
            "fromNode": 2,
            "toNode": 3,
            "fromPort": "dataOut",
            "toPort": "dataInUp"
        },
        {
            "fromNode": 3,
            "toNode": 0,
            "fromPort": "dataOut",
            "toPort": "mainDataOut"
        },
        {
            "fromNode": 3,
            "toNode": 0,
            "fromPort": "controlOutL",
            "toPort": "mainControlOutL"
        },
        {
            "fromNode": 3,
            "toNode": 0,
            "fromPort": "controlOutR",
            "toPort": "mainControlOutR"
        }
    ],
    "x": 0,
    "y": 0,


}


my_memory = {
}


bugsPorts = ['dataInUp', 'controlIn', 'dataInDown',
             'controlOutL', 'controlOutR', 'dataOut']


def initialize_memory(bug_id: int) -> None:
    """Initialize all port values in memory to None for a given bug id"""
    for port in bugsPorts:
        my_memory[f"{bug_id}_{port}"] = None


def initialize_child_memory(bugs: list) -> None:
    for bug in bugs:
        initialize_memory(bug["id"])


def get_next_bug(edges, fromPort, fromBug) -> int:
    for edge in edges:
        if edge["fromPort"] == fromPort and edge["fromNode"] == fromBug:
            return edge["toNode"]


def get_next_port(edges, fromPort, fromBug) -> int:
    for edge in edges:
        if edge["fromPort"] == fromPort and edge["fromNode"] == fromBug:
            return edge["toPort"]

#print(get_next_bug(addition["edges"], "controlOutL", 1))


def eval_plus_bug(up: int or None, down: int or None) -> int:
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
    my_memory[f"{bug_id}_{port}"] = value


def read_from_memory(bug_id: int, port: string) -> int:
    return my_memory[f"{bug_id}_{port}"]


def eval_bug(bug, up, down) -> None:
    if ("id" not in bug):
        """Initialize memory for main bug"""
        initialize_memory(0)
        # Set the data input value of the upper parent bug
        write_to_memory(0, "dataInUp", up)
        # Set the data input value of the lower parent bug
        write_to_memory(0, "dataInDown", down)
        write_to_memory(0, "controlIn", 1)  # Activate the parent bug

        """Connect the parent bugs data ports to the children"""
        initialize_child_memory(
            bug["bugs"])  # Initialize the memory for the child bugs to be able to write to them in the future
        # Get the id of the upper child bug
        upper_data_to_node_id =  (bug["edges"], "mainDataInUp", 0)
        # Get the id of the lower child bug
        lower_data_to_node_id = get_next_bug(bug["edges"], "mainDataInDown", 0)
        # Get the port of the upper child bug TODO this could have multiple bugs connected to it
        upper_data_to_port = get_next_port(bug["edges"], "mainDataInUp", 0)
        # Get the port of the lower child bug TODO this could have multiple bugs connected to it
        lower_data_to_port = get_next_port(bug["edges"], "dataInDown", 0)
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

        if control_value == 0:
            # bugs left control out port is active
            # Activate the left control out port
            write_to_memory(bug["id"], "controlOutL", 1)
            # Deactivate the right control out port
            write_to_memory(bug["id"], "controlOutR", 0)
            # Get the id of the next bug based on the left control out port
            next_bug_id = get_next_bug(
                addition["edges"], "controlOutL", bug["id"])
        elif control_value == 1:
            # bugs right control out port is active
            # Deactivate the left control out port
            write_to_memory(bug["id"], "controlOutL", 0)
            # Activate the right control out port
            write_to_memory(bug["id"], "controlOutR", 1)
            # Get the id of the next bug based on the right control out port
            next_bug_id = get_next_bug(
                addition["edges"], "controlOutR", bug["id"])

        # Get the data port of the next bug where the data should be written to
        next_data_port = get_next_port(addition["edges"], "dataOut", bug["id"])
        # Write the data to the next bugs data port
        write_to_memory(next_bug_id, next_data_port, data_value)

    elif (len(bug["bugs"]) != 0):
        """The bug is a parent node"""
        for child in bug["bugs"]:
            # Evaluate the child bugs
            eval_bug(child, read_from_memory(
                child["id"], "dataInUp"), read_from_memory(child["id"], "dataInDown"))
    else:
        raise Exception("Something went wrong")


eval_bug(addition, 8, 5)
print(my_memory)
