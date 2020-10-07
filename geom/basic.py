"""This module implements basic geometrical routines."""

from tecplot import writer
from matplotlib.tri import Triangulation
import matplotlib.pyplot as plt
import numpy as np
from .vector import Vector
from .point import Point
from _grid.edge import Edge


def edge_to_vector(e: Edge) -> Vector:
    assert len(e.nodes) == 2, 'Wrong number of nodes in the edge'
    n1 = e.nodes[0]
    n2 = e.nodes[1]
    p1 = point_to_vector(n1.as_point())
    p2 = point_to_vector(n2.as_point())
    return Vector.subtract_vectors(p2, p1)


def dot_product(v1: Vector, v2: Vector) -> float:
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z


def cross_product(v1: Vector, v2: Vector):
    return Vector(v1.y * v2.z - v1.z * v2.y, v1.z * v2.x - v1.x * v2.z, v1.x * v2.y - v1.y * v2.x)


def point_to_vector(point: Point):
    return Vector(point.x, point.y, point.z)


def euclidian_distance(p1: Point, p2: Point):
    """:param n1, n2 Nodes"""
    return np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2)


def create_half_cylinder(vertical_points=3, horizontal_points=5, filename='_grid', create_dat=True, plot_pyplot=False):
    """Create half-cylinder triangular _grid, using Delaunay triangulation.

    :param n_points : int How many points on the circle (cylinder's base) to create.
    :param filename: file ti write .dat file in.
    :param create_dat : bool create .dat file containing _grid in the projects dir.
    :param plot_pyplot: bool show pyplot visualization of the _grid.

    :return Grid obj."""
    u = np.linspace(0, np.pi, num=vertical_points, endpoint=True)
    v = np.linspace(0, 3, num=horizontal_points, endpoint=True)

    u, zs = np.meshgrid(u, v)

    delaunuy = Triangulation(u.flatten(), zs.flatten())
    xs = np.sin(u)
    ys = np.cos(u)

    x = ys.flatten()
    y = zs.flatten()
    z = xs.flatten()
    from _grid import grid
    mgrid = grid.Grid()

    mgrid.set_nodes_and_faces(x, y, z, delaunuy.triangles)

    if plot_pyplot:
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_trisurf(x, y, z, triangles=delaunuy.triangles)
        plt.show()

    if create_dat:
        if not filename.endswith('.dat'):
            filename += '.dat'
        writer.write_tecplot(mgrid, filename)

    for f in mgrid.Faces:
        n1 = mgrid.Nodes[f.nodes_ids[0] - 1]
        n2 = mgrid.Nodes[f.nodes_ids[1] - 1]
        n3 = mgrid.Nodes[f.nodes_ids[2] - 1]

        # Link faces, nodes and edges.
        e1 = mgrid.is_edge_present(n1, n2)
        if e1 is None:
            e1 = Edge()
            mgrid.link_face_and_edge(f, e1)
            mgrid.link_node_and_edge(n1, e1)
            mgrid.link_node_and_edge(n2, e1)
            mgrid.Edges.append(e1)
        else:
            mgrid.link_face_and_edge(f, e1)

        e2 = mgrid.is_edge_present(n2, n3)
        if e2 is None:
            e2 = Edge()
            mgrid.link_face_and_edge(f, e2)
            mgrid.link_node_and_edge(n2, e2)
            mgrid.link_node_and_edge(n3, e2)
            mgrid.Edges.append(e2)
        else:
            mgrid.link_face_and_edge(f, e2)

        e3 = mgrid.is_edge_present(n3, n1)
        if e3 is None:
            e3 = Edge()
            mgrid.link_face_and_edge(f, e3)
            mgrid.link_node_and_edge(n3, e3)
            mgrid.link_node_and_edge(n1, e3)
            mgrid.Edges.append(e3)
        else:
            mgrid.link_face_and_edge(f, e3)

    assert len(mgrid.Edges) < 3 * len(mgrid.Nodes) - 3, 'Wrong number of edges'
    assert len(mgrid.Faces) < 2 * len(mgrid.Nodes) - 2, 'Wrong number of faces'

    return mgrid


def create_plane(n, m, filename='_grid', create_dat=True, plot_pyplot=False):
    u = np.linspace(0, 1, n, endpoint=True)
    v = np.linspace(0, 1, m, endpoint=True)

    u, v = np.meshgrid(u, v)

    delaunuy = Triangulation(u.flatten(), v.flatten())

    z = np.sin(u + v)

    x = u.flatten()
    y = v.flatten()
    z = z.flatten()

    values = x + y
    from _grid import grid
    mgrid = grid.Grid()

    mgrid.set_nodes_and_faces(x, y, z, delaunuy.triangles)

    if plot_pyplot:
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_trisurf(x, y, z, triangles=delaunuy.triangles)
        plt.show()

    if create_dat:
        if not filename.endswith('.dat'):
            filename += '.dat'
        writer.write_tecplot(mgrid, filename)

    return mgrid


def create_uneven_plane(n, m, filename='_grid', create_dat=True, plot_pyplot=False):
    u = np.logspace(-2, 0, n, base=2.0, endpoint=True)
    v = np.linspace(0, 1, m, endpoint=True)

    u, v = np.meshgrid(u, v)

    delaunuy = Triangulation(u.flatten(), v.flatten())

    z = np.zeros(u.shape)

    x = u.flatten()
    y = v.flatten()
    z = z.flatten()

    from _grid import grid
    mgrid = grid.Grid()

    mgrid.set_nodes_and_faces(x, y, z, delaunuy.triangles)

    if plot_pyplot:
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_trisurf(x, y, z, triangles=delaunuy.triangles)
        plt.show()

    if create_dat:
        if not filename.endswith('.dat'):
            filename += '.dat'
        writer.write_tecplot(mgrid, filename)

    return mgrid
