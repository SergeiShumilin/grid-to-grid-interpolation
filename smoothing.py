from geom.basic import *
from scipy.linalg import eig, det
import numpy as np
from geom.vector import Vector
from tecplot import writer, reader
from _grid.grid import Grid
from copy import deepcopy

DETERMINANT_ACCURACY = 10e-5


def create_matrix_of_normals(node) -> np.array:
    N = node.faces[0].normal().coords_np_array()
    N = N.reshape((1, 3))
    for f in node.faces[1:]:
        normal = f.normal().coords_np_array()
        assert N.shape[1] == normal.shape[1], print(N.shape, normal.shape)
        N = np.vstack((N, normal))

    return N


def print_info(node, eigenValues, nullspace, k):
    print('Узел', node.x, node.y, node.z)
    print('k =', k)
    print(eigenValues)
    print(nullspace)
    print('-------------')


def name_of_iteration(i):
    iteration_name = str(i)
    zeros = '000'
    return zeros[:-len(iteration_name)] + iteration_name


def mark_all_fixed_nodes(grid):
    number_of_bondary_nodes = 0
    for e in grid.Edges:
        if len(e.faces) == 1:
            e.border = True
            for n in e.nodes:
                if not n.fixed:
                    number_of_bondary_nodes += 1
                    n.fixed = True

    # check_euler_equations(grid, number_of_bondary_nodes)


def check_euler_equations(grid, number_of_bondary_nodes):
    E = len(grid.Edges)
    N = len(grid.Nodes)
    F = len(grid.Faces)
    n = number_of_bondary_nodes
    print(E)
    print(3 * N - n - 3)
    print(F)
    print(2 * N - n - 2)
    assert E == 3 * N - n - 3, 'Wrong number of edges. Euler proves'
    assert F == 2 * N - n - 2, 'Wrong number of edges. Euler proves'


def border_edge_to_project_on(n, shift_vector):
    border_edges = [e for e in n.edges if e.border]
    assert len(border_edges) == 2, 'Wrong number of border edges'
    dot_products_between_edges_and_shift = [dot_product(edge_to_vector(e), shift_vector) for e in border_edges]
    edge_to_project_on_number = np.argmax(dot_products_between_edges_and_shift)
    assert edge_to_project_on_number == 0 or edge_to_project_on_number == 1

    edge_to_project_on = edge_to_vector(border_edges[edge_to_project_on_number])
    edge_to_project_on.make_unit()
    assert isinstance(edge_to_project_on, Vector)
    corrected_for_border_node_shift = dot_product(shift_vector, edge_to_project_on)
    edge_to_project_on.mul(corrected_for_border_node_shift)
    return edge_to_project_on


def null_space_smoothing(grid: Grid, num_iter=20, st=0.2, epsilon=10e-3, fix_border_nodes=False,
                         fix_direction_of_border_nodes=False):
    for i in range(num_iter):
        for n in grid.Nodes:
            if fix_border_nodes:
                if n.fixed:
                    continue

            m = len(n.faces)
            p = point_to_vector(n.as_point())
            w = [f.area() for f in n.faces]
            N = create_matrix_of_normals(n)

            dv = Vector()
            weights = 0
            for f in n.faces:
                c = point_to_vector(f.centroid())
                c.sub(p)

                # Find shifting
                # normal = f.normal()
                # normal.mul(SHIFT)
                # c.sum(normal)

                weight = f.area()
                assert isinstance(c, Vector)
                assert isinstance(weight, float)
                c.mul(weight)
                dv.sum(c)
                weights += weight
            dv.dev(weights)

            assert N.shape == (m, 3)
            assert len(w) == m
            assert isinstance(dv, Vector)

            W = np.diag(w)
            NTW = np.dot(N.T, W)
            A = np.dot(NTW, N)

            assert W.shape == (m, m)
            assert NTW.shape == (3, m)
            assert A.shape == (3, 3)

            eigenValues, eigenVectors = eig(A)
            idx = eigenValues.argsort()[::-1]
            eigenValues = eigenValues[idx]
            eigenVectors = eigenVectors[:, idx]

            assert np.abs(det(A) - np.cumprod(eigenValues)[-1]) < DETERMINANT_ACCURACY, \
                print(det(A), np.cumprod(eigenValues)[-1])

            k = np.sum((eigenValues > epsilon * eigenValues[0]))
            ns = eigenVectors[:, k:]
            dv = dv.coords_np_array().reshape(3, 1)

            assert ns.shape == (3, 3 - k), 'Wrong eigenvectors shape'
            assert dv.shape == (3, 1), 'Wrong shape'
            # print_info(n, eigenValues, ns, k)
            if k < 3:
                ttT = np.dot(ns, ns.T)
                t = st * np.dot(ttT, dv)
                assert t.shape == (3, 1), 'Wrong shift shape'
                shift = Vector(float(t[0, 0]), float(t[1, 0]), float(t[2, 0]))
                if fix_direction_of_border_nodes:
                    if n.fixed:
                        n.move(border_edge_to_project_on(n, shift))
                    else:
                        n.move(shift)
                else:
                    n.move(shift)

        print('{}th iteration'.format(i))
        writer.write_tecplot(g, 'smoothing_res_{}.dat'.format(name_of_iteration(i)))


class Smoothing:
    __name__ = ''

    def __init__(self, grid, num_interations=20, fix_border_nodes=False):
        self.grid = grid
        self.num_iterations = num_interations
        self.fix_border_nodes = fix_border_nodes

    def smoothing(self):
        raise NotImplementedError

    def move_node(self, node, shift: Vector):
        if self.fix_border_nodes:
            if node.fixed:
                node.move(border_edge_to_project_on(node, shift))
            else:
                node.move(shift)
        else:
            node.move(shift)

    def write_grid_and_print_info(self, iteration):
        print('{}th iteration of {} smoothing'.format(iteration, self.__name__))
        writer.write_tecplot(self.grid, '{}_smoothing_fixed_{}.dat'.format(self.__name__, name_of_iteration(iteration)))


class LaplacianSmoothing(Smoothing):
    __name__ = 'Laplacian'

    def __init__(self, grid: Grid, num_iterations=20, alpha=0.2, fix_border_nodes=False):
        self.alpha = alpha
        Smoothing.__init__(self, grid, num_iterations, fix_border_nodes)

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

    def __init__(self, grid: Grid, num_iterations=20, lamb=0.5, mu=0.52, fix_border_nodes=False):
        self.lamb = lamb
        self.mu = mu
        Smoothing.__init__(self, grid, num_iterations, fix_border_nodes)

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


if __name__ == '__main__':
    # g = create_half_cylinder(20, 20, 'easy.dat', plot_pyplot=True)
    g = Grid()
    reader.read_tecplot(g, 'grids/var8.dat')
    mark_all_fixed_nodes(g)
    null_space_smoothing(g, num_iter=100, st=0.1, epsilon=0.2, fix_direction_of_border_nodes=True)
    #TaubinSmoothing(g, num_iterations=50, lamb=0.5, mu=0.8).smoothing()
