from _grid.vector import *

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def coords(self):
        return self.x, self.y, self.z

    def as_vector(self):
        return Vector(self.x, self.y, self.z)

