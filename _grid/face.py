"""Module describing _grid's face."""
from .node import Node
from geom.basic import cross_product, point_to_vector
from geom.vector import Vector
from geom.vector import Point


class Face:
    __doc__ = "Module describing _grid's face."

    def __init__(self, Id=None):
        """
        Construct a face.
        :param id: face's id.
        """
        self.Id = Id

        # Nodes and edges set clockwise.
        self.nodes = list()
        self.nodes_ids = list()
        self.edges = list()

        self.T = None
        self.Hw = None
        self.Hi = None
        self.HTC = None
        self.Beta = None
        self.TauX = None
        self.TauY = None
        self.TauZ = None
        self.aux_node = Node()

    def normal(self):
        assert len(self.nodes) == 3, 'Wrong number of nodes in the face'
        p1 = self.nodes[0].as_point()
        p2 = self.nodes[1].as_point()
        p3 = self.nodes[2].as_point()
        v1 = Vector(p1.x, p1.y, p1.z)
        v2 = Vector(p2.x, p2.y, p2.z)
        v3 = Vector(p3.x, p3.y, p3.z)
        vf = Vector.subtract_vectors(v1, v2)
        vs = Vector.subtract_vectors(v1, v3)
        vr = cross_product(vf, vs)
        vr.make_unit()
        assert isinstance(vr, Vector)
        return vr

    def area(self):
        """Calculate the area of the face."""
        assert len(self.nodes) == 3, "Wrong number of nodes in the face"
        n1, n2, n3 = self.nodes[0], self.nodes[1], self.nodes[2]
        p1, p2, p3 = n1.as_point(), n2.as_point(), n3.as_point()
        v1 = Vector.subtract_vectors(point_to_vector(p1), (point_to_vector(p2)))
        v2 = Vector.subtract_vectors(point_to_vector(p1), (point_to_vector(p3)))
        res = cross_product(v1, v2).norm() / 2
        assert isinstance(res, float), print('Wrong area', res)
        return res

    def centroid(self):
        n1 = self.nodes[0]
        n2 = self.nodes[1]
        n3 = self.nodes[2]
        x = (n1.x + n2.x + n3.x) / 3
        y = (n1.y + n2.y + n3.y) / 3
        z = (n1.z + n2.z + n3.z) / 3

        return Point(x, y, z)
