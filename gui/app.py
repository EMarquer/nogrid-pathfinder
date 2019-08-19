import tkinter as tk

# local imports
from .const import *
from .scene_display import *
from .coor_frame import CoorFrame

from scene.scene import Scene
from scene.node import Node
from scene.path import Path
from scene.coor_converter import *

from math import ceil
from pathfinding.astar import *

from time import time

class Application(tk.Frame):
    scene: Scene

    converter: CoorConverter

    draw_scale: int

    def __init__(self, master=None, scene: Scene=None, draw_scale: int=DRAW_SCALE):
        super().__init__(master)
        self.master = master
        self.scene = scene
        self.draw_scale = draw_scale
        self.converter = CoorConverter(self.scene.grid_precision, self.draw_scale)
        self.astar_engine = AStar(self.scene, self.converter)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Pathfinding
        self.menu_pathfinding = tk.Frame(self)
        self.menu_pathfinding.pack(side="left", fill="both", expand="yes")

        # Stats

        # Recompute
        self.button_pathfinding = tk.Button(self.menu_pathfinding, text="Recompute pathfinding", command=self.recompute_pathfinding)
        self.button_pathfinding.pack()

        # Scene
        self.scene_display = SceneDisplay(self, converter=self.converter)
        self.scene_display.pack(side="left")

        # Positions
        self.menu = tk.Frame(self)
        self.menu.pack(side="left", fill="both", expand="yes")

        # Current 
        self.coor_frame_current = CoorFrame(self.menu, text="Current", converter=self.converter)
        self.coor_frame_current.pack(**LABEL_FRAME_KWARGS)

        # Origin point
        self.coor_frame_origin = CoorFrame(self.menu, text="Origin", converter=self.converter)
        self.coor_frame_origin.pack(**LABEL_FRAME_KWARGS)

        # Target point
        self.coor_frame_target = CoorFrame(self.menu, text="Target", converter=self.converter)
        self.coor_frame_target.pack(**LABEL_FRAME_KWARGS)

        # Grid
        self.grid_precision_var = tk.StringVar(self, value=self.scene.grid_precision if self.scene else GRID_PRECISIONS[0])
        self.frame_grid = tk.LabelFrame(self.menu, text="Grid precision")
        self.frame_grid.pack(**LABEL_FRAME_KWARGS)
        self.spinbox_grid = tk.Spinbox(self.frame_grid, values=GRID_PRECISIONS, textvariable=self.grid_precision_var)
        self.spinbox_grid.pack()
        self.button_grid = tk.Button(self.frame_grid, text="Update grid", command=self.update_grid)
        self.button_grid.pack()

        #self.quit = tk.Button(self, text="EXIT", command=self.master.destroy)
        #self.quit.pack(side="bottom")

        self.scene_display.setup(self.scene,
            self.coor_frame_current,
            self.coor_frame_origin,
            self.coor_frame_target)

    def update_grid(self):
        self.scene.set_grid_precision(float(self.grid_precision_var.get()))
        self.converter.grid_precision = self.scene.grid_precision
        self.update_coors()
        self.recompute_pathfinding()
        self.display()

    def update_coors(self):
        self.coor_frame_target.update(*self.converter.convert_coor(SCENE, CANVAS, *self.scene.target.get_xy()))
        self.coor_frame_origin.update(*self.converter.convert_coor(SCENE, CANVAS, *self.scene.origin.get_xy()))

    def update_scene(self, scene: Scene):
        self.scene_display.update_scene(scene)
        self.scene = scene
        self.astar_engine.scene = self.scene

        # update precision selector
        self.grid_precision_var.set(self.scene.grid_precision)
        self.converter.grid_precision = self.scene.grid_precision
        self.update_coors()
        
    def display(self, scene: Scene=None):
        if scene: 
            self.update_scene(scene)
        self.scene_display.display(scene)

    def recompute_pathfinding(self):
        self.scene.set_astar_path(self.astar_engine.compute())

        self.display()

def build(scene: Scene):
    root = tk.Tk()
    root.title(APP_TITLE)
    app = Application(master=root, scene=scene)
    app.display(scene)
    app.mainloop()