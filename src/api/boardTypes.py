from enum import Enum
from pydantic import BaseModel


class PortType(str, Enum):
    In = "In"
    Out = "Out"
    Up = "Up"
    Down = "Down"
    Left = "Left"
    Right = "Right"

class EdgeType(str, Enum):
    Control = "Control"
    Data = "Data"


class PortAdress(BaseModel):
    bugId: int
    port: PortType


class Edge(BaseModel):
    From: PortAdress
    to: PortAdress
    Type: EdgeType


class Bug(BaseModel):
    id: int
    bugs: list[Bug]
    edges: list[Edge]
    xValue: int
    yValue: int
