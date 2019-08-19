from abc import abstractmethod
from tkinter import Canvas
from ..coor_converter import *
from ..node import Node

class Shape:
    @abstractmethod
    def contains_coor(self, x, y) -> bool:
        return False

    @abstractmethod
    def draw(self, canvas: Canvas, coor_converter: CoorConverter, **kwargs) -> None:
        pass
