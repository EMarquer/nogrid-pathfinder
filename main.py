from gui.app import build
from scene.scene import Scene
from scene.scene import Path, Node

scene = Scene(10, 5)
print(scene)

scene.nogrid_path = Path([Node(.5, .5), Node(2, 3), Node(4, 5), Node(4.5, 3.5)])
scene.astar_path = Path([Node(.5, .5), Node(1, 1), Node(1.5, 1.5), Node(2, 2), Node(2.5, 2.5), Node(3, 3), Node(3.5, 3.5), Node(4, 3.5), Node(4.5, 3.5)])

build(scene)
print(scene)