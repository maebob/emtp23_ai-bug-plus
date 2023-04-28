## Language Specifications for BugPlus:

- Possible bug ports:
    - 1 control in
    - 2 control out
    - 2 data in
    - 1 data out

- Predefined constant bugs are possible:
    - 1 control in
    - 1 control out
    - 1 data out
    - no data in

- Nodes can have the following attributes:
    - nodeID
    - objectType

- A board consists of:
    - nodes[]
    - links[]

- All bug ports must have memory.

- A single control in port can receive multiple inputs.

- A single control out port can have only one link.

- A single data in port can have only one link.

- A single data out port can have multiple links.

- The activated control out port is denoted by 1, while the inactive one is denoted by 0.

- Possible Bugs: +Bug, Board, Constant

- Calculation is object-based.

- On evaluation, a node returns the control link to the next node/output, as well as the data out value.
