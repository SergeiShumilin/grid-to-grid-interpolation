"""This module implements basic geometrical routines."""
from grid import grid
from tecplot import writer
from matplotlib.tri import Triangulation, LinearTriInterpolator
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


def euclidian_distance(n1, n2):
    """:param n1, n2 Nodes"""
    return np.sqrt((n1.x - n2.x) ** 2 + (n1.y - n2.y) ** 2 + (n1.z - n2.z) ** 2)


def create_half_cylinder(vertical_points=3, horizontal_points=5, filename='grid', create_dat=True, plot_pyplot=False):
    """Create half-cylinder triangular grid, using Delaunay triangulation.

    :param n_points : int How many points on the circle (cylinder's base) to create.
    :param filename: file ti write .dat file in.
    :param create_dat : bool create .dat file containing grid in the projects dir.
    :param plot_pyplot: bool show pyplot visualization of the grid.

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


def create_plane(n, m, filename='grid', create_dat=True, plot_pyplot=False):
    u = np.linspace(0, 1, n, endpoint=True)
    v = np.linspace(0, 1, m, endpoint=True)

    u, v = np.meshgrid(u, v)

    delaunuy = Triangulation(u.flatten(), v.flatten())

    z = np.zeros((n, m))

    x = u.flatten()
    y = v.flatten()
    z = z.flatten()

    values = x + y

    print(LinearTriInterpolator(delaunuy, values).gradient(0.5, 0.5))
    mgrid = grid.Grid()

    mgrid.set_nodes_and_faces(x, y, z, delaunuy.triangles)

    if plot_pyplot:
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_trisurf(x, y, values, triangles=delaunuy.triangles)
        plt.show()

    if create_dat:
        if not filename.endswith('.dat'):
            filename += '.dat'
        writer.write_tecplot(mgrid, filename)

    return mgrid
