

from .const import *
import tkinter as tk
from scene.scene import Scene
from scene.node import Node
from scene.path import Path
from .coor_frame import CoorFrame
from scene.coor_converter import *
from math import ceil

class SceneDisplay(tk.Canvas):
    def __init__(self, master=None, converter: CoorConverter=None, **kwargs):
        super().__init__(master=master, **kwargs)
        self.converter = converter

    def setup(self,
            scene: Scene,
            coor_frame_current: CoorFrame,
            coor_frame_origin: CoorFrame,
            coor_frame_target: CoorFrame):
        self.coor_frame_current = coor_frame_current
        self.coor_frame_origin = coor_frame_origin
        self.coor_frame_target = coor_frame_target
        self.scene = scene
        
        self.bind("<Motion>", self.canvas_hover)
        self.bind("<Button-3>", self.canvas_click_origin)
        self.bind("<Button-1>", self.canvas_click_target)

    def update_scene(self, scene: Scene):
        self.scene = scene
        self.converter.grid_precision = self.scene.grid_precision
        self.display()

    def canvas_hover(self, event):
        # grab the mouse cordinates and get the corresponding scene coordinates
        self.coor_frame_current.update(
            self.canvasx(event.x),
            self.canvasy(event.y))

    def canvas_click_origin(self, event):
        # grab the mouse cordinates and get the corresponding scene coordinates
        x, y = self.canvasx(event.x), self.canvasy(event.y)
        
        self.coor_frame_origin.update(x, y)

        self.scene.set_origin(*self.converter.convert_coor(CANVAS, SCENE, x, y))
        self.display()

    def canvas_click_target(self, event):
        # grab the mouse cordinates and get the corresponding scene coordinates
        x, y = self.canvasx(event.x), self.canvasy(event.y)
        
        self.coor_frame_target.update(x, y)

        self.scene.set_target(*self.converter.convert_coor(CANVAS, SCENE, x, y))
        self.display()

    def display(self, scene: Scene=None):
        if scene: self.update_scene(scene)

        if self.scene:
            # update canevas size
            self.config(
                width= self.converter.convert_coor(SCENE, CANVAS, self.scene.x_size) + 1,
                height=self.converter.convert_coor(SCENE, CANVAS, self.scene.y_size) + 1)

            # draw background
            #self.draw_background(self.scene)
            self.draw_grid()
            self.draw_obstacles()

            self.draw_astar_path(self.scene.astar_path)
            self.draw_nogrid_path(self.scene.nogrid_path)

            self.draw_origin()
            self.draw_target()

    def draw_background(self, scene: Scene):
        self.create_rectangle(
            0, 0, *self.converter.convert_coor(SCENE, CANVAS, scene.x_size, scene.y_size),
            fill="white")

    def draw_obstacles(self):
        for obstacle in self.scene.obstacles:
            obstacle.draw(self, self.converter, outline=OBSTACLE_BORDER_COLOR, width=NODE_WIDTH)

    def draw_grid(self):
        for x, line in enumerate(self.scene.grid):
            for y, cell in enumerate(line):
                self.draw_tile(Node(x, y), OBSTACLE_COLOR_GETTER(cell))
    
        # draw grid
        total_x, total_y = self.converter.convert_coor(SCENE, CANVAS, self.scene.x_size, self.scene.y_size)

        # varying X
        for i in range(0, ceil(total_x), ceil(self.scene.grid_precision * DRAW_SCALE)):
            self.create_line(i, 0, i, total_y, fill=GRID_COLOR)

        # varying Y
        for j in range(0, ceil(total_y), ceil(self.scene.grid_precision * DRAW_SCALE)):
            self.create_line(0, j, total_x, j, fill=GRID_COLOR)

    def draw_origin(self):
        self.draw_node(self.scene.origin, ORIGIN_COLOR, ORIGIN_COLOR)

    def draw_target(self):
        self.draw_node(self.scene.target, TARGET_COLOR, TARGET_COLOR)

    def draw_node(self, node: Node, color: str, fill: str=""):
        x, y = self.converter.convert_node(SCENE, CANVAS, node).get_xy()
        self.create_oval(x - NODE_RADIUS, y - NODE_RADIUS, x + NODE_RADIUS, y + NODE_RADIUS, outline=color, width=NODE_WIDTH, fill=fill)

    def draw_tile(self, tile: Node, color: str):
        self.create_rectangle(*self.converter.generate_tile(GRID, tile), fill=color, outline='')

    def draw_nogrid_path(self, path: Path):
        if path:
            # draw the lines
            for node_start, node_end in zip(path.nodes[:-1], path.nodes[1:]):
                self.create_line(
                    self.converter.convert_node(SCENE, CANVAS, node_start).get_xy(),
                    self.converter.convert_node(SCENE, CANVAS, node_end).get_xy(),
                    fill=NOGRID_COLOR, width=NODE_WIDTH)

            # draw the nodes
            for node in path.nodes:
                self.draw_node(node, NOGRID_COLOR)  

    def draw_astar_path(self, path: Path):  
        if path:
            for node in path.nodes:
                self.draw_tile(node, ASTAR_COLOR)