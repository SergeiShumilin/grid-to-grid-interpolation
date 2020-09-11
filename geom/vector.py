
from geom.basic import *

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def coords(self):
        return self.x, self.y, self.z

    def norm(self):
        return euclidian_distance(self.point(), Point(0, 0, 0))

    def point(self):
        return Point(self.x, self.y, self.z)

    def sub(self, vector):
        return Vector(self.x - vector.x, self.y - vector.y, self.z - vector.z)