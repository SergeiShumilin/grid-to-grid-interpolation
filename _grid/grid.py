"""Module describes triangular _grid."""
from .node import Node
from .face import Face
from .zone import Zone
import numpy as np
from algorithms.avl_tree import AVLTree


class Grid:
    __doc__ = "Class describing triangular _grid"

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
        Init zone 1 of _grid.

        Makes all elements of the _grid belong to zone 1.
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
        assert len(f.nodes) < 3, 'There are already 3 nodes incident to the face'
        n.faces.append(f)
        f.nodes.append(n)

    @staticmethod
    def link_node_and_edge(n, e):
        """
        Link node and edge.
        :param n: node.
        :param e: edge.
        """
        assert len(e.nodes) < 2, 'There are already 2 nodes incident to the edge'
        n.edges.append(e)
        e.nodes.append(n)

    @staticmethod
    def link_face_and_edge(f, e):
        """
        Link face and edge.
        :param f: face.
        :param e: edge.
        """
        assert len(f.edges) < 3, 'There are already 3 edges incident to the face'
        assert len(e.faces) < 2, 'There are already 2 faces incident to the edge'
        if e not in f.edges:
            f.edges.append(e)
        if f not in e.faces:
            e.faces.append(f)

    @staticmethod
    def is_edge_present(n1, n2):
        """
        Whether the `_grid.Edges` contains the edge connecting nodes n1 and n2.
        :param n1: node 1.
        :param n2: node 2.
        :return: id of the edge if present and None if not.
        """

        for edge in n1.edges:
            if n2 in edge.nodes:
                return edge

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
            self.link_face_and_node(f, self.Nodes[nids[2]])
            self.link_face_and_node(f, self.Nodes[nids[1]])
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

    def return_aux_nodes_as_a_ndim_array(self) -> np.array:
        """Return (n_points, 3) array of coordinates of nodes."""
        x, y, z = list(), list(), list()

        for f in self.Faces:
            x.append(f.aux_node.x)
            y.append(f.aux_node.y)
            z.append(f.aux_node.z)

        return np.array([x, y, z]).T

    def make_avl(self):
        """Compose an avl tree that contains references to nodes and allows to logn search."""
        for n in self.Nodes:
            self.avl.insert(n)

    def is_isomprphic_to(self, grid) -> bool:
        """
        Check whether the _grid is isomorphic to another _grid.

        We make a simple two-steps check:
        1. Whether the number of nodes is equal.
        2. Whether the sorted arrays of nodes' degrees (number of connected nodes) of the grids are equal.

        It means that the result is not hundred percent correct, but this heuristics are useful and easy.

        :param grid: Grid (obj)
        :return: bool
        """
        if len(self.Nodes) == len(grid.Nodes):
            degrees_old = []
            degrees_new = []

            for n in self.Nodes:
                degrees_old.append(len(n.edges))
            for n in grid.Nodes:
                degrees_new.append(len(n.edges))

            sorted(degrees_new)
            sorted(degrees_old)

            if degrees_new == degrees_old:
                return True

        return False

    def relocate_values_from_isomorphic_grid(self, grid):
        for i in range(len(self.Faces)):
            self.Faces[i].T = grid.Faces[i].T
            self.Faces[i].Hw = grid.Faces[i].Hw

    def compute_aux_nodes(self):
        """Calculate the points which are the point of medians' intersection."""
        for f in self.Faces:
            n1, n2, n3 = f.nodes[0], f.nodes[1], f.nodes[2]
            f.aux_node.x = (n1.x + n2.x + n3.x) / 3
            f.aux_node.y = (n1.y + n2.y + n3.y) / 3
            f.aux_node.z = (n1.z + n2.z + n3.z) / 3

    def return_paramenter_as_ndarray(self, parameter):
        values_in_auxes = list()
        for f in self.Faces:
            if parameter == 'T':
                values_in_auxes.append(f.T)
            if parameter == 'Hw':
                values_in_auxes.append(f.Hw)
        return np.array(values_in_auxes).reshape((len(values_in_auxes), 1))

    def set_aux_nodes_parameters(self, interpolated_parameters, parameter='T'):
        assert interpolated_parameters.shape[0] == 1, 'Wrong array dimensions'
        for i, f in enumerate(self.Faces):
            if parameter == 'T':
                f.T = interpolated_parameters[0, i]
            if parameter == 'Hw':
                f.Hw = interpolated_parameters[0, i]
