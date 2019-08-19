from __future__ import annotations
from __future__ import annotations
from typing import List, Union
from .node import Node

class Path:
    nodes: List[Node]
    
    def __init__(self, nodes: List[Node]=[]):
        self.nodes = nodes

    def __add__(self, path_or_node: Union[Path, Node]) -> Path:
        if isinstance(path_or_node, Path):
            return Path(self.nodes + path_or_node.nodes)
        else:
            return Path(self.nodes + [path_or_node])

    def __len__(self):
        return len(self.nodes)