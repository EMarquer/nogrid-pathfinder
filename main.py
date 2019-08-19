from gui.app import build
from scene.scene import Scene
from scene.scene import Path, Node
from scene.shapes import *

obstacles = {Circle(Node(7, 2), 2)}
scene = Scene(10, 5, obstacles=obstacles)

scene.nogrid_path = Path([Node(.5, .5), Node(2, 3), Node(4, 5), Node(4.5, 3.5)])

from pathfinding.astar import *
from scene.coor_converter import *

converter = CoorConverter(scene.grid_precision, 1)

scene.grid[3][3] = 1
build(scene)