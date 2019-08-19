from .node import Node
from .path import Path
from math import floor

CANVAS = "canvas"
GRID = "grid"
SCENE = "scene"

CONVERTION = {
    (SCENE, CANVAS): lambda coor, converter: coor * converter.scene_to_canvas_ratio,
    (CANVAS, SCENE): lambda coor, converter: coor / converter.scene_to_canvas_ratio,
    (GRID, SCENE): lambda coor, converter: coor * converter.grid_precision,
    (SCENE, GRID): lambda coor, converter: floor(coor / converter.grid_precision),
    (GRID, CANVAS): lambda coor, converter: (coor * converter.grid_precision) * converter.scene_to_canvas_ratio,
    (CANVAS, GRID): lambda coor, converter: floor((coor / converter.scene_to_canvas_ratio) / converter.grid_precision)
}

class CoorConverter:
    scene_to_canvas_ratio: float
    grid_precision: float

    def __init__(self, grid_precision: float, scene_to_canvas_ratio: float):
        self.scene_to_canvas_ratio = scene_to_canvas_ratio
        self.grid_precision = grid_precision

    def convert_coor(self, source, target, *coors):
        out_coors = tuple(CONVERTION[(source, target)](coor, self) for coor in coors)
        return out_coors[0] if len(out_coors) == 1 else out_coors

    def convert_node(self, source, target, *nodes):
        out_nodes = tuple(Node(*self.convert_coor(source, target, *node.get_xy())) for node in nodes)

        return out_nodes[0] if len(out_nodes) == 1 else out_nodes

    def convert_path(self, source, target, *paths):
        out_paths = tuple(Path([self.convert_node(source, target, node) for node in path.nodes]) for path in paths)

        return out_paths[0] if len(out_paths) == 1 else out_paths

    def generate_tile(self, source, *tiles):
        # the output is canevas/style
        def generate_single_tile(tile: Node):
            x, y = self.convert_node(source, CANVAS, tile).get_xy()
            tile_width = self.convert_coor(GRID, CANVAS, 1)

            return x, y, x + tile_width, y + tile_width

        out_tiles = tuple(generate_single_tile(tile) for tile in tiles)

        return out_tiles[0] if len(out_tiles) == 1 else out_tiles
