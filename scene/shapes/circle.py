from .shape import *

class Circle(Shape):
    center: Node
    radius: float

    def __init__(self, center: Node, radius: float):
        self.center = center
        self.radius = radius
    
    def contains_node(self, node: Node) -> bool:
        delta_x, delta_y = (node - self.center).get_xy()
        return (delta_x ** 2) + (delta_y ** 2) <= self.radius ** 2

    def draw(self, canvas: Canvas, coor_converter: CoorConverter, **kwargs) -> None:
        canvas.create_oval(
            *coor_converter.convert_coor(SCENE, CANVAS,
                self.center.x - self.radius,
                self.center.y - self.radius,
                self.center.x + self.radius,
                self.center.y + self.radius),
            **kwargs)