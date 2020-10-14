"""Module describing triangular_grid's node"""

from geom.point import Point
from geom.vector import Vector

class Node:
    __doc__ = "class describing node"

    def __init__(self, x=None, y=None, z=None, Id=None):
        """
        Construct node.
        :param id: node's id in the triangular_grid.
        """
        self.x = x
        self.y = y
        self.z = z
        self.Id = Id

        self.T = None
        self.Hw = None

        self.faces = list()
        self.edges = list()

        self.fixed = False
        self.component = None

    def coordinates(self) -> tuple:
        return self.x, self.y, self.z

    def as_point(self):
        return Point(self.x, self.y, self.z)

    def move(self, v):
        self.x += v.x
        self.y += v.y
        self.z += v.z
