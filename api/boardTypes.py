from enum import Enum
from pydantic import BaseModel


class Port(str, Enum):
    ControlIn = "controlIn"
    ControlOutLeft = "controlOutL"
    ControlOutRight = "controlOutR"
    DataInUP = "dataInUp"
    DataInDown = "dataInDown"
    DataOut = "dataOut"
    ControlInInterface = "mainControlIn"
    ControlOutInterfaceL = "mainControlOutL"
    ControlOutInterfaceR = "mainControlOutR"
    DataInUpInterface = "mainDataInUp"
    DataInDownInterface = "mainDataInDown"
    DataOutInterface = "mainDataOut"


class Node(BaseModel):
    id: int


class Edge(BaseModel):
    fromNode: int
    toNode: int
    fromPort: Port
    toPort: Port


class Board(BaseModel):
    bugs: list[Node]
    edges: list[Edge]
    xValue: int
    yValue: int
