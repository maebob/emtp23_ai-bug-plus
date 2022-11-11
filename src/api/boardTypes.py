from __future__ import annotations

from typing import Optional
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
    from_: PortAdress
    to: PortAdress
    Type: EdgeType


class Bug(BaseModel):
    id: int
    bugs: list[Bug]
    edges: list[Edge]
    Type: str
    xValue: Optional[int] = None
    yValue: Optional[int] = None

