from __future__ import annotations
"""From https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2"""

from typing import Union, Tuple, Optional
from scene.node import Node
from scene.scene import Scene
from scene.path import Path

from sortedcollections import SortedList, SortedSet
from scene.coor_converter import *

MOVE_DIRECTIONS = SortedSet(
    (Node(x, y) for x in {-1, 0, 1} for y in {-1, 0, 1} if (x, y) != (0, 0)),
    key=lambda node: node.get_xy())

class AStarNode(Node):
    """A node class for A* Pathfinding"""
    parent: AStarNode

    def __init__(self,
            position: Union[Node, Tuple[int, int]],
            parent: Optional[AStarNode]=None):
        # either we already have a node object or we have to create it
        super(AStarNode, self).__init__(*(position.get_xy() if isinstance(position, Node) else position))
        self.parent = parent

        self.distance_to_start = 0 # distance to start
        self.heuristic_cost = 0 # heuristic
        self.total_cost = 0 # total cost

    def set_cost(self, target_node: Optional[AStarNode]=None) -> None:
        self.distance_to_start = self.parent.distance_to_start + 1 if self.parent else 0
        #heuristic: squared euclidian distance
        self.heuristic_cost = ((self.x - target_node.x) ** 2) + ((self.y - target_node.y) ** 2) if target_node else 0

        self.total_cost = self.distance_to_start + self.heuristic_cost

    def generate_path(self) -> Path:
        if self.parent: 
            return self.parent.generate_path() + self
        else:
            return Path([self])

    def __str__(self):
        return "AStarNode {}x{}".format(self.x, self.y)
        
class AStar:
    origin_node: AStarNode
    target_node: AStarNode

    scene: Scene

    def __init__(self, scene: Scene, converter: CoorConverter):
        self.scene = scene
        self.converter = converter
    
    def compute(self) -> Optional[Path]:
        # grab origin and target
        self.origin_node = AStarNode(self.converter.convert_node(SCENE, GRID, self.scene.origin))
        self.target_node = AStarNode(self.converter.convert_node(SCENE, GRID, self.scene.target))
        self.origin_node.set_cost(self.target_node)
        self.target_node.set_cost(self.target_node)

        # Initialize both open (with the start node) and closed list
        closed_nodes_set = set()
        open_nodes_sorted_set = SortedSet([self.origin_node], key=lambda x: x.total_cost)

        # Loop until you find the end
        while open_nodes_sorted_set:
            # Get the current node (less costly item)
            # Pop current off open list, add to closed list
            current_node = open_nodes_sorted_set.pop(0)
            closed_nodes_set.add(current_node)

            # Found the goal
            if current_node == self.target_node: 
                return current_node.generate_path()

            # Generate children
            for move_direction in MOVE_DIRECTIONS: # Adjacent squares
                # Get node position
                new_node = current_node + move_direction

                # Make sure within range
                if (
                        (new_node.x in range(len(self.scene.grid)) and new_node.y in range(len(self.scene.grid[0]))) and 
                        self.scene.grid[new_node.x][new_node.y] == 0 and # Make sure walkable terrain
                        new_node not in closed_nodes_set): # Child is on the closed list
                    # Create new node
                    new_astar_node = AStarNode(new_node, current_node)
                    new_astar_node.set_cost(self.target_node)

                    # Child is already in the open list, replace the previous value if the cost of the current one is lower
                    if new_astar_node in open_nodes_sorted_set:
                        for open_node in open_nodes_sorted_set:
                            if (new_astar_node == open_node and
                                    new_astar_node.distance_to_start > open_node.distance_to_start):
                                open_nodes_sorted_set.discard(open_node)
                                open_nodes_sorted_set.add(new_astar_node)

                    # Add the child to the open list
                    open_nodes_sorted_set.add(new_astar_node)

        return None