import tkinter as tk

# local imports
from .const import *
from scene.coor_converter import *

class CoorFrame(tk.LabelFrame):
    def __init__(self, master, text: str, converter: CoorConverter):
        super().__init__(master, text=text)
        self.master = master
        self.converter = converter

        self.frame_scene = tk.LabelFrame(self, text="Scene")
        self.frame_scene.pack(**COOR_INNER_FRAME_KWARGS)

        self.label_scene = tk.Label(self.frame_scene)
        self.label_scene.pack()
        self.label_scene["text"] = COOR_TEXT.format('??', '??')

        self.frame_grid = tk.LabelFrame(self, text="Grid")
        self.frame_grid.pack(**COOR_INNER_FRAME_KWARGS)

        self.label_grid = tk.Label(self.frame_grid)
        self.label_grid.pack()
        self.label_grid["text"] = COOR_TEXT.format('??', '??')

    def update(self, x: float, y: float):
        self.label_scene["text"] = COOR_TEXT.format(*self.converter.convert_coor(CANVAS, SCENE, x, y))
        self.label_grid["text"] = COOR_TEXT.format(*self.converter.convert_coor(CANVAS, GRID, x, y))
        
