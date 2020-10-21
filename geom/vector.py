from numpy import array
from .point import Point


class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def coords(self):
        return self.x, self.y, self.z

    def coords_np_array(self):
        return array([self.x, self.y, self.z]).reshape((1, 3))

    def norm(self):
        from .basics import euclidian_distance
        return euclidian_distance(self.point(), Point(0, 0, 0))

    def point(self):
        return Point(self.x, self.y, self.z)

    def sum(self, other):
        assert isinstance(other, Vector)
        self.x += other.x
        self.y += other.y
        self.z += other.z

    def sub(self, other):
        assert isinstance(other, Vector)
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z

    def dev(self, k):
        if k == 0:
            raise ZeroDivisionError
        self.mul(1 / k)

    def make_unit(self):
        l = self.norm()
        self.dev(l)

    def mul(self, k):
        self.x *= k
        self.y *= k
        self.z *= k

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ')'

    @staticmethod
    def subtract_vectors(v1, v2):
        return Vector(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)
