import tkinter as tk

# local imports
from .const import *

from scene.scene import Scene
from scene.node import Node
from scene.path import Path

from math import ceil

class Application(tk.Frame):
    def __init__(self, master=None, scene: Scene=None):
        super().__init__(master)
        self.master = master
        self.scene = scene
        self.pack()
        self.create_widgets()


    def create_widgets(self):
        self['bg']='green'
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side="left")

        # Target
        self.menu = tk.Frame(self)
        self.menu.pack(side="left", fill="both", expand="yes")
        """
        self.hi_there = tk.Button(self.menu)
        self.hi_there["text"] = "Hello World\n(click me)"
        #self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")"""


        coor_frame_kwargs = {"side": "top", "fill": "x", "expand": "yes", "ipadx": 5, "ipady": 5}

        # Current 
        self.frame_current = tk.LabelFrame(self.menu, text="Current")
        self.frame_current.pack(**coor_frame_kwargs)
        self.label_current = tk.Label(self.frame_current)
        self.label_current.pack()
        self.label_current["text"] = COOR_TEXT.format('??', '??')
        self.canvas.bind("<Motion>", self.canevas_hover)

        # Origin point
        self.frame_origin = tk.LabelFrame(self.menu, text="Origin")
        self.frame_origin.pack(**coor_frame_kwargs)
        self.label_origin = tk.Label(self.frame_origin)
        self.label_origin.pack()
        self.label_origin["text"] = COOR_TEXT.format(self.scene.origin.x, self.scene.origin.x) if self.scene and self.scene.origin else COOR_TEXT.format('??', '??')
        self.canvas.bind("<Button-3>", self.canevas_click_origin)

        # Target point
        self.frame_target = tk.LabelFrame(self.menu, text="Target")
        self.frame_target.pack(**coor_frame_kwargs)
        self.label_target = tk.Label(self.frame_target)
        self.label_target.pack()
        self.label_target["text"] = COOR_TEXT.format(self.scene.target.x, self.scene.target.x) if self.scene and self.scene.target else COOR_TEXT.format('??', '??')
        self.canvas.bind("<Button-1>", self.canevas_click_target)

        # Grid
        self.grid_precision_var = tk.StringVar(self, value=self.scene.grid_precision if self.scene else GRID_PRECISIONS[0])
        self.frame_grid = tk.LabelFrame(self.menu, text="Grid precision")
        self.frame_grid.pack(**coor_frame_kwargs)
        self.spinbox_grid = tk.Spinbox(self.frame_grid, values=GRID_PRECISIONS, textvariable=self.grid_precision_var)
        self.spinbox_grid.pack()
        self.button_grid = tk.Button(self.frame_grid, text="Update grid", command=self.update_grid)
        self.button_grid.pack()

        #self.quit = tk.Button(self, text="EXIT", command=self.master.destroy)
        #self.quit.pack(side="bottom")
        
    def update_grid(self):
        self.scene.set_grid_precision(float(self.grid_precision_var.get()))
        self.display()

    def canevas_hover(self, event):
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)

        x_scaled, y_scaled = x / DRAW_SCALE, y / DRAW_SCALE

        self.label_current["text"] = COOR_TEXT.format(x_scaled, y_scaled)

    def canevas_click_origin(self, event):
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)

        x_scaled, y_scaled = x / DRAW_SCALE, y / DRAW_SCALE

        self.label_origin["text"] = COOR_TEXT.format(x_scaled, y_scaled)
        self.scene.set_origin(x_scaled, y_scaled)
        self.display()

    def canevas_click_target(self, event):
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)

        x_scaled, y_scaled = x / DRAW_SCALE, y / DRAW_SCALE

        self.label_target["text"] = COOR_TEXT.format(x_scaled, y_scaled)
        self.scene.set_target(x_scaled, y_scaled)
        self.display()

    def display(self, scene: Scene=None):
        self.scene = scene or self.scene
        self.grid_precision_var.set(self.scene.grid_precision)
        self.canvas.config(scrollregion=(0, 0, self.scene.x_size * DRAW_SCALE, self.scene.y_size * DRAW_SCALE))
        self.canvas.config(width=self.scene.x_size * DRAW_SCALE + 1, height=self.scene.y_size * DRAW_SCALE + 1)
        self.draw_background(self.scene)
        self.draw_grid(self.scene)

        self.draw_astar_path(self.scene.astar_path)
        self.draw_nogrid_path(self.scene.nogrid_path)

        self.draw_origin(self.scene)
        self.draw_target(self.scene)

    def draw_background(self, scene: Scene):
        self.canvas.create_rectangle(
            0, 0,
            scene.x_size * DRAW_SCALE, scene.y_size * DRAW_SCALE,
            fill="white")

    def draw_grid(self, scene: Scene):
        color = "lightgray"
        total_x, total_y = scene.x_size * DRAW_SCALE, scene.y_size * DRAW_SCALE

        # varying X
        for i in range(0, ceil(total_x), ceil(scene.grid_precision * DRAW_SCALE)):
            self.canvas.create_line(i, 0, i, total_y, fill=color)

        # varying Y
        for j in range(0, ceil(total_y), ceil(scene.grid_precision * DRAW_SCALE)):
            self.canvas.create_line(0, j, total_x, j, fill=color)

    def draw_origin(self, scene: Scene):
        self.draw_node(scene.origin, ORIGIN_COLOR, ORIGIN_COLOR)

    def draw_target(self, scene: Scene):
        self.draw_node(scene.target, TARGET_COLOR, TARGET_COLOR)

    def draw_node(self, node: Node, color: str, fill: str=""):
        x, y = node.x * DRAW_SCALE, node.y * DRAW_SCALE
        self.canvas.create_oval(x - NODE_RADIUS, y - NODE_RADIUS, x + NODE_RADIUS, y + NODE_RADIUS, outline=color, width=NODE_WIDTH, fill=fill)

    def draw_tile(self, node: Node, color: str):
        x, y = node.x * DRAW_SCALE, node.y * DRAW_SCALE
        self.canvas.create_rectangle(x + 2, y + 2, x + (self.scene.grid_precision * DRAW_SCALE) - 3, y + (self.scene.grid_precision * DRAW_SCALE) - 3, fill=color)

    def draw_nogrid_path(self, path: Path):
        if path:
            # draw the lines
            for node_start, node_end in zip(path.nodes[:-1], path.nodes[1:]):
                self.canvas.create_line(node_start.x * DRAW_SCALE, node_start.y * DRAW_SCALE, node_end.x * DRAW_SCALE, node_end.y * DRAW_SCALE, fill=NOGRID_COLOR, width=NODE_WIDTH)

            # draw the nodes
            for node in path.nodes:
                self.draw_node(node, NOGRID_COLOR)  

    def draw_astar_path(self, path: Path):  
        if path:
            for node in path.nodes:
                self.draw_tile(node, ASTAR_COLOR)      

def build(scene: Scene):
    root = tk.Tk()
    root.title(APP_TITLE)
    app = Application(master=root, scene=scene)
    app.display(scene)
    app.mainloop()