from .shapes.shape import Shape

class Obstacle:
    shape: Shape

    def __init__(self, shape: Shape):
        super().__init__(*args, **kwargs)