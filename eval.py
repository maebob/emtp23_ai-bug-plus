import string

addition = {
    "id": 0,
    "bugs": [
        {
            "id": 1
        },
        {
            "id": 2
        },
        {
            "id": 3
        }

    ],
    "edges": [
        {
            "from": "0_controlIn",
            "to": "1_controlIn"
        },
        {
            "from": "1_controlOutL",
            "to": "2_controlIn"
        },
        {
            "from": "1_controlOutR",
            "to": "2_controlIn"
        },
        {
            "from": "2_controlOutL",
            "to": "3_controlIn"
        },
        {
            "from": "2_controlOutR",
            "to": "3_controlIn"
        },
        {
            "from": "1_dataOut",
            "to": "2_dataInDown"
        },
        {
            "from": "0_dataInUp",
            "to": "3_dataInDown"
        },
        {
            "from": "2_dataOut",
            "to": "3_dataInUp"
        },
        {
            "from": "3_dataOut",
            "to": "0_dataOut"
        },
        {
            "from": "3_controlOutL",
            "to": "0_controlOutL"
        },
        {
            "from": "3_controlOutR",
            "to": "0_controlOutR"
        }
    ],
    "x": 0,
    "y": 0,


}


my_memory = {
}


BUGS_PORTS = ['dataInUp', 'controlIn', 'dataInDown',
             'controlOutL', 'controlOutR', 'dataOut']


def get_next_bug(edges, from_port:string) -> int:
    for edge in edges:
        if edge["from"] == from_port:
            return edge["to"]

def get_next_port(edges, current_port) -> int:
    for edge in edges:
        if edge["from"] == current_port:
            return edge["to"]

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


def write_bug_to_memory(port: string, value: int) -> None:
    my_memory[port] = value


def read_from_memory(bug_id: int, port: string) -> int:
    return my_memory[f"{bug_id}_{port}"]


def set_control_out_ports(bug_id: int, active_port: int) -> None:
    if active_port == 0:
        # bugs left control out port is active
        # Activate the left control out port
        write_bug_to_memory(f"{bug_id}_controlOutL", 1)
        # Deactivate the right control out port
        write_bug_to_memory(f"{bug_id}_controlOutR", 0)
    elif active_port == 1:
        # bugs right control out port is active
        # Deactivate the left control out port
        write_bug_to_memory(f"{bug_id}_controlOutL", 0)
        # Activate the right control out port
        write_bug_to_memory(f"{bug_id}_controlOutR", 1)



def initialize_memory_main(bug)->None:
    """Initialize all port values in memory to None for a given bug id"""
    if ("bugs" not in bug):
        for port in BUGS_PORTS:
            my_memory[f"{bug['id']}_{port}"] = None
    else:
        for child in bug["bugs"]:
            initialize_memory_main(child)

def initialize_global_memory():
    for port in BUGS_PORTS:
        my_memory[f"0_{port}"] = None

def set_global_ports(up, down):
    write_bug_to_memory("0_controlIn", 1)
    write_bug_to_memory("0_dataInUp", up)
    write_bug_to_memory("0_dataInDown", down)
    

def write_data_out(edges, bug_id):
    data_ports = []
    for edge in edges:
        if edge["from"] == f"{bug_id}_dataOut":
            data_ports.append(edge["to"])
    
    for port in data_ports:
        write_bug_to_memory(port, read_from_memory(bug_id, "dataOut"))
    


def compile(bug):
    current_port = str(bug["id"]) + "_controlIn"
    while (current_port is not None):
        next_port = get_next_port(bug["edges"], current_port)
        
        write_bug_to_memory(next_port, 1)
        next_bug_id = int(next_port.split("_")[0])
        next_bug = None
        for child in bug["bugs"]:
            if child["id"] == next_bug_id:
                next_bug = child
                break
        if next_bug is None:
            break

        if("bugs" not in next_bug):
            up = read_from_memory(next_bug["id"], "dataInUp")
            down = read_from_memory(next_bug["id"], "dataInDown")
            data_result, control_result = eval_plus_bug(up, down)
            write_bug_to_memory(f"{next_bug_id}_dataOut", data_result)
            set_control_out_ports(next_bug["id"], control_result)
            if control_result == 0:
                current_port = f"{next_bug_id}_controlOutL"
            elif control_result == 1:
                current_port = f"{next_bug_id}_controlOutR"
        else:
            compile(next_bug)
        write_data_out(bug["edges"], next_bug_id)




def main(bug, up, down) -> None:
    initialize_global_memory()
    initialize_memory_main(bug)
    set_global_ports(up, down)
    compile(bug)
    print(my_memory)

if __name__ == "__main__":
    main(addition, 3, 2)
    #print(addition["bugs"].keys(1))