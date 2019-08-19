from __future__ import annotations
from typing import Tuple

class Node:
    x: float
    y: float
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def get_xy(self) -> Tuple[float, float]:
        return self.x, self.y

    def __sub__(self, other: Node) -> Node:
        return Node(self.x - other.x, self.y - other.y)

    def __add__(self, other: Node) -> Node:
        return Node(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return "Node {}x{}".format(self.x, self.y)