from typing import Set, List

from math import ceil, floor

from .node import Node
from .path import Path
from .obstacle import Obstacle

class Scene:
    x_size: float
    y_size: float

    grid_precision: float

    grid: List[List[float]] # a star cost : 0 to 1

    obstacles: Set[Obstacle]

    origin: Node
    target: Node

    astar_path: Path
    nogrid_path: Path

    def __init__(self,
            x_size: float=10,
            y_size: float=10,
            grid_precision: float=0.5,
            obstacles: Set[Obstacle]={},
            origin: Node=Node(.5, .5),
            target: Node=Node(4.5, 3.5)
            ):
        self.x_size = x_size
        self.y_size = y_size

        self.grid_precision = grid_precision
        self.prepare_grid()
    
        self.obstacles = obstacles

        self.origin = origin
        self.target = target

        self.astar_path = None
        self.nogrid_path = None

    def set_origin(self, x: float, y: float):
        self.origin = Node(x, y)

    def set_target(self, x: float, y: float):
        self.target = Node(x, y)

    def prepare_grid(self):
        self.grid = [
            [0 for j in range(ceil(self.y_size/self.grid_precision))]
            for i in range(ceil(self.x_size/self.grid_precision))
        ]

    def get_tile(self, x: float, y: float):
        return self.grid[floor(x)][floor(y)]
    def set_tile(self, x: float, y: float, value: float):
        self.grid[floor(x)][floor(y)] = value

    def set_grid_precision(self, grid_precision: float):
        self.grid_precision = grid_precision
        self.prepare_grid()

    def __str__(self):
        return "\n".join([
            "Scene {}:".format(self.__repr__()),
            "\tScene dimensions: {}x{}".format(self.x_size, self.y_size),
            "\tGrid:",
            "\t\tdimensions: {}x{}".format(len(self.grid), len(self.grid[0])),
            "\t\tprecision: {}""".format(self.grid_precision)
        ])