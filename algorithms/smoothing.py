from geom.basics import *
from scipy.linalg import eig, det
from numpy import argmax, array, vstack, diag, dot, abs, cumprod, sum, zeros, full, isnan
from geom.vector import Vector
from tecplot import writer
from triangular_grid.grid import Grid
from copy import deepcopy
from collections import deque

DETERMINANT_ACCURACY = 10e-5


class Smoothing:
    __name__ = ''

    def __init__(self, grid, num_interations=20, node_fixation_method=None):
        self.grid = grid
        self.num_iterations = num_interations
        assert node_fixation_method in [None, 'no_move', 'along_edge']
        self.node_fixation_method = node_fixation_method

        if self.node_fixation_method is not None:
            self.mark_all_fixed_nodes()

    @staticmethod
    def name_of_iteration(i):
        iteration_name = str(i)
        zeros = '000'
        return zeros[:-len(iteration_name)] + iteration_name

    def smoothing(self):
        raise NotImplementedError

    @staticmethod
    def is_node_fixed(n):
        border_edges = [e for e in n.edges if e.border]
        assert len(border_edges) == 2, print('Wrong number of border edges', len(border_edges))

        alpha = 0.2
        be1_v = border_edges[0]
        be2_v = border_edges[1]
        # make vectors directed in different sides.
        # represent as (n1) --be1_v-- (n2) --be2_v-- (n3)
        n1 = None
        n2 = n
        n3 = None
        assert len(be1_v.nodes) == 2
        assert len(be2_v.nodes) == 2
        if be1_v.nodes[0] == n:
            n1 = be1_v.nodes[1]
        else:
            n1 = be1_v.nodes[0]
            assert be1_v.nodes[1] == n

        if be2_v.nodes[0] == n:
            n3 = be2_v.nodes[1]
        else:
            n3 = be2_v.nodes[0]
            assert be2_v.nodes[1] == n

        assert n1 is not n2
        assert n2 is not n3
        assert n3 is not n1

        n1_v = Vector(n1.x, n1.y, n1.z)
        n2_v = Vector(n2.x, n2.y, n2.z)
        n3_v = Vector(n3.x, n3.y, n3.z)
        be1 = Vector.subtract_vectors(n1_v, n2_v)
        be2 = Vector.subtract_vectors(n3_v, n2_v)
        be1.make_unit()
        be2.make_unit()
        dot_between_unit_edges = dot_product(be1, be2)
        assert -1 <= dot_between_unit_edges <= 1
        if dot_between_unit_edges > (-1 + alpha):
            return True, border_edges

        return False, border_edges

    def border_edge_to_project_on(self, n, shift_vector):
        is_fixed, border_edges = self.is_node_fixed(n)

        if is_fixed:
            return Vector(0, 0, 0)

        dot_products_between_edges_and_shift = [dot_product(edge_to_vector(e), shift_vector) for e in border_edges]
        edge_to_project_on_number = argmax(dot_products_between_edges_and_shift)
        assert edge_to_project_on_number == 0 or edge_to_project_on_number == 1
        edge_to_project_on = edge_to_vector(border_edges[edge_to_project_on_number])
        edge_to_project_on.make_unit()
        assert isinstance(edge_to_project_on, Vector)
        return edge_to_project_on

    def move_node(self, node, shift: Vector):
        if self.node_fixation_method == 'no_move':
            if node.fixed:
                pass
            else:
                node.move(shift)
        elif self.node_fixation_method == 'along_edge':
            if node.fixed:
                edge_to_project_on_unit = self.border_edge_to_project_on(node, shift)
                projection_of_shift_on_edge = dot_product(edge_to_project_on_unit, shift)
                edge_to_project_on_unit.mul(projection_of_shift_on_edge)
                node.move(edge_to_project_on_unit)
            else:
                node.move(shift)
        else:
            node.move(shift)

    def write_grid_and_print_info(self, iteration):
        print('{}th iteration of {} smoothing'.format(iteration, self.__name__))
        writer.write_tecplot(self.grid, '{}_ORIGsmoothing_{}.dat'.format(self.__name__,
                                                                         self.name_of_iteration(iteration)))

    def mark_all_fixed_nodes(self):
        for e in self.grid.Edges:
            if len(e.faces) == 1:
                e.border = True
                for n in e.nodes:
                    if not n.fixed:
                        n.fixed = True
                        self.grid.number_of_border_nodes += 1

    def apply_laplacians(self, laplacians):
        assert len(self.grid.Nodes) == len(laplacians)
        for n, l in zip(self.grid.Nodes, laplacians):
            self.move_node(n, l)


class LaplacianSmoothing(Smoothing):
    __name__ = 'Laplacian'

    def __init__(self, grid: Grid, num_iterations=20, alpha=0.2, node_fixation_method=None):
        self.alpha = alpha
        Smoothing.__init__(self, grid, num_iterations, node_fixation_method)

    def smoothing(self):
        for i in range(self.num_iterations):
            for n in self.grid.Nodes:
                neighbours = []
                assert len(n.edges) > 1
                for e in n.edges:
                    assert len(e.nodes) == 2
                    n1 = e.nodes[0]
                    n2 = e.nodes[1]
                    if n1 == n:
                        neighbours.append(n2)
                    else:
                        neighbours.append(n1)

                laplacian = Vector()
                for neighbour_node in neighbours:
                    laplacian.sum(point_to_vector(neighbour_node.as_point()))
                laplacian.dev(len(neighbours))
                laplacian.sub(point_to_vector(n.as_point()))
                laplacian.mul(self.alpha)

                Smoothing.move_node(self, n, laplacian)

            Smoothing.write_grid_and_print_info(self, i)


class TaubinSmoothing(Smoothing):
    __name__ = 'Taubin'

    def __init__(self, grid: Grid, num_iterations=20, lamb=0.5, mu=0.52, node_fixation_method=None):
        self.lamb = lamb
        self.mu = mu
        Smoothing.__init__(self, grid, num_iterations, node_fixation_method)

    def smoothing(self):
        for i in range(self.num_iterations):
            for n in self.grid.Nodes:
                neighbours = []
                assert len(n.edges) > 1
                for e in n.edges:
                    assert len(e.nodes) == 2
                    n1 = e.nodes[0]
                    n2 = e.nodes[1]
                    if n1 == n:
                        neighbours.append(n2)
                    else:
                        neighbours.append(n1)

                laplacian = Vector()
                for neighbour_node in neighbours:
                    laplacian.sum(point_to_vector(neighbour_node.as_point()))
                laplacian.dev(len(neighbours))
                laplacian.sub(point_to_vector(n.as_point()))
                backward_laplacian = deepcopy(laplacian)

                laplacian.mul(self.lamb)
                backward_laplacian.mul(self.mu)
                backward_laplacian.mul(-1)

                if i % 2 == 0:
                    Smoothing.move_node(self, n, laplacian)
                else:
                    Smoothing.move_node(self, n, backward_laplacian)

            Smoothing.write_grid_and_print_info(self, i)


class NullSpaceSmoothing(Smoothing):
    __name__ = "NullSpace"

    def __init__(self, grid: Grid, num_iterations=20, st=0.2, epsilon=10e-3, n_neighbours_for_border_nodes=None,
                 node_fixation_method=None):
        assert len(grid.Nodes) > 0, 'the grid is empty'
        assert len(grid.Faces) > 0, 'the grid is empty'
        assert len(grid.Edges) > 0, 'the grid is empty'
        self.st = st
        self.epsilon = epsilon
        self.n_neighbours_for_border_nodes = n_neighbours_for_border_nodes
        Smoothing.__init__(self, grid, num_iterations, node_fixation_method)

    @staticmethod
    def print_info(node, eigenValues, nullspace, k):
        print('Узел', node.x, node.y, node.z)
        if node.fixed:
            print('Boundary node')
        print('k =', k)
        print(eigenValues)
        print(nullspace)
        print('-------------')

    @staticmethod
    def create_matrix_of_normals(node) -> array:
        N = node.faces[0].normal().coords_np_array()
        N = N.reshape((1, 3))
        for f in node.faces[1:]:
            normal = f.normal().coords_np_array()
            assert N.shape[1] == normal.shape[1], print(N.shape, normal.shape)
            N = vstack((N, normal))

        return N

    def find_n_neighbours_faces_of_node(self, node, n_neighbours=None):
        if n_neighbours is None:
            n_neighbours = len(node.faces)

        visited = full(len(self.grid.Faces), False)
        # find n_neighbours with breadth-first search
        neighbours = []
        q = deque()
        assert len(node.faces) > 0

        for neighbour in node.faces[:n_neighbours]:
            neighbours.append(neighbour)
            q.append(neighbour)
            assert isinstance(neighbour.Id, int)
            visited[neighbour.Id] = True

        while len(q) > 0 and len(neighbours) < n_neighbours:
            search_around_face = q.popleft()
            visited[search_around_face.Id] = True
            for adjacent_face in search_around_face.adjacent_faces():
                if not visited[adjacent_face.Id]:
                    q.append(adjacent_face)
                    neighbours.append(adjacent_face)

        # assert len(neighbours) == n_neighbours, 'unable to find n neighbours for local interpolation for border nodes'

        return neighbours

    def set_weight_for_face(self, node, face, centroid):
        if not node.fixed:
            return 1.0
        is_fixed, border_edges = Smoothing.is_node_fixed(node)
        assert len(border_edges) == 2
        if is_fixed:
            # any of border edges
            edge_to_compare_with = border_edges[0]
            edge_to_compare_with = edge_to_vector(edge_to_compare_with)
            edge_to_compare_with.make_unit()
            centroid_ = deepcopy(centroid)
            centroid_.make_unit()
            assert edge_to_compare_with.norm() - 1.0 < 10e-6
            assert centroid_.norm() - 1.0 < 10e-6
            return 1.0 - abs(dot_product(edge_to_compare_with, centroid_))
        else:
            return 1.0

    def vector_to_avg_of_centroids(self, node, n_neighbours=None):
        dv = Vector()
        p = point_to_vector(node.as_point())
        weights = 0

        # turn off condition len(node.faces) % 2 != 0 for a second
        if node.fixed:
            neighbours = self.find_n_neighbours_faces_of_node(node, n_neighbours)
        else:
            neighbours = node.faces

        assert len(neighbours) > 0
        assert isinstance(node.Id, int)

        for f in neighbours:
            self.grid.adj_list_for_border_nodes[node.Id - 1, f.Id] = 1

        for f in neighbours:
            c = point_to_vector(f.centroid())
            c.sub(p)
            weight = self.set_weight_for_face(node, f, c)
            assert isinstance(c, Vector)
            assert isinstance(weight, float)
            c.mul(weight)
            dv.sum(c)
            weights += weight
        dv.dev(weights)
        return dv

    def smoothing(self):
        for i in range(self.num_iterations):
            laplacians = []
            for n in self.grid.Nodes:
                m = len(n.faces)
                w = [f.area() for f in n.faces]
                N = self.create_matrix_of_normals(n)
                dv = self.vector_to_avg_of_centroids(n, self.n_neighbours_for_border_nodes)

                assert N.shape == (m, 3)
                assert len(w) == m
                assert isinstance(dv, Vector)

                W = diag(w)
                NTW = dot(N.T, W)
                A = dot(NTW, N)
                assert W.shape == (m, m)
                assert NTW.shape == (3, m)
                assert A.shape == (3, 3)

                eigenValues, eigenVectors = eig(A)
                idx = eigenValues.argsort()[::-1]
                eigenValues = eigenValues[idx]
                eigenVectors = eigenVectors[:, idx]

                assert abs(det(A) - cumprod(eigenValues)[-1]) < DETERMINANT_ACCURACY, \
                    print(det(A), cumprod(eigenValues)[-1])

                k = sum((eigenValues > self.epsilon * eigenValues[0]))
                ns = eigenVectors[:, k:]
                dv = dv.coords_np_array().reshape(3, 1)

                assert ns.shape == (3, 3 - k), 'Wrong eigenvectors shape'
                assert dv.shape == (3, 1), 'Wrong shape'
                # self.print_info(n, eigenValues, ns, k)
                if k < 3:
                    ttT = dot(ns, ns.T)
                    if n.fixed:
                        t = 0.2 * self.st * dot(ttT, dv)
                    else:
                        t = self.st * dot(ttT, dv)
                    assert t.shape == (3, 1), 'Wrong shift shape'
                    laplacian = Vector(float(t[0, 0]), float(t[1, 0]), float(t[2, 0]))
                else:
                    laplacian = Vector(0, 0, 0)
                laplacians.append(laplacian)

            Smoothing.apply_laplacians(self, laplacians)
            Smoothing.write_grid_and_print_info(self, i)
