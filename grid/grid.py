"""Module describes triangular grid."""
from .node import Node
from .face import Face
from .zone import Zone
import numpy as np
from algorithms.avl_tree import AVLTree


class Grid:
    __doc__ = "Class describing triangular grid"

    def __init__(self):
        """
        Grid constructor.
        """
        self.Faces = list()
        self.Edges = list()
        self.Nodes = list()
        self.Zones = list()
        self.avl = AVLTree()

    def init_zone(self):
        """
        Init zone 1 of grid.

        Makes all elements of the grid belong to zone 1.
        """
        z = Zone()
        z.Nodes = self.Nodes
        z.Faces = self.Faces
        self.Zones.append(z)

    @staticmethod
    def link_face_and_node(f, n):
        """
        Link node and face.
        :param n: node.
        :param f: face.
        """
        n.faces.append(f)
        f.nodes.append(n)

    @staticmethod
    def link_node_and_edge(n, e):
        """
        Link node and edge.
        :param n: node.
        :param e: edge.
        """
        n.edges.append(e)
        e.nodes.append(n)

    @staticmethod
    def link_face_and_edge(f, e):
        """
        Link face and edge.
        :param f: face.
        :param e: edge.
        """
        f.edges.append(e)
        e.faces.append(f)

    @staticmethod
    def is_edge_present(n1, n2):
        """
        Whether the `grid.Edges` contains the edge connecting nodes n1 and n2.
        :param n1: node 1.
        :param n2: node 2.
        :return: id of the edge if present and None if not.
        """
        for edge in n1.edges:
            if edge.nodes[0] == n2 or edge.nodes[1] == n2:
                return edge
            else:
                return None

    def set_nodes_and_faces(self, x, y, z, triangles):
        """
        Create Grid's nodes from the x, y, z co-ordinates.
        :param x, y, z: arrays of coordinates
        :param triangles: array (n_tri, 3) with indexes of corresponding nodes.

        Fills all faces' values with face's id.
        """
        for x, y, z in zip(x, y, z):
            self.Nodes.append(Node(x, y, z))

        i = 0
        for nids in triangles:
            f = Face(i)
            i += 1
            f.nodes_ids = nids + 1
            self.link_face_and_node(f, self.Nodes[nids[0]])
            self.link_face_and_node(f, self.Nodes[nids[1]])
            self.link_face_and_node(f, self.Nodes[nids[2]])
            self.Faces.append(f)

        self.init_zone()

    def relocate_values_from_faces_to_nodes(self):
        """First use the simplest algrithm.
        The value in the node is a mean of values in the adjacent faces."""
        for n in self.Nodes:
            n_faces = len(n.faces)
            t = 0
            hw = 0
            for f in n.faces:
                t += f.T
                hw += f.Hw
            n.T = t / n_faces
            n.Hw = hw / n_faces

    def relocate_values_from_nodes_to_faces(self):
        """Set values in faces as mean of the neighbour nodes."""
        for f in self.Faces:
            f.T = (f.nodes[0].T + f.nodes[1].T + f.nodes[2].T) / 3.0
            f.Hw = (f.nodes[0].Hw + f.nodes[1].Hw + f.nodes[2].Hw) / 3.0

    def values_from_nodes_to_array(self) -> np.array:
        """Return nodes' values as an array."""
        res = list()
        for n in self.Nodes:
            res.append(n.value)

        return np.array(res)

    def return_coordinates_as_a_ndim_array(self) -> np.array:
        """Return (n_points, 3) array of coordinates of nodes."""
        x, y, z = list(), list(), list()

        for n in self.Nodes:
            x.append(n.x)
            y.append(n.y)
            z.append(n.z)

        return np.array([x, y, z]).T

    def make_avl(self):
        """Compose an avl tree that contains references to nodes and allows to logn search."""
        for n in self.Nodes:
            self.avl.insert(n)
