from grid import grid, node, tecplot, face
from matplotlib.tri import Triangulation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from algorithms import knn


def create_half_cylinder(n_points=3, filename='grid', create_dat=True, plot_pyplot=False):
    """Create half-cylinder triangular grid, using Delaunay triangulation.

    :param n_points : int How many points on the circle (cylinder's base) to create.
    :param filename: file ti write .dat file in.
    :param create_dat : bool create .dat file containing grid in the projects dir.
    :param plot_pyplot: bool show pyplot visualization of the grid.

    :return Grid obj."""
    u = np.linspace(0, np.pi, num=n_points, endpoint=True)
    v = np.linspace(0, 3, num=10, endpoint=True)

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
        tecplot.print_tecplot(mgrid, filename)

    return mgrid


grid1 = create_half_cylinder(20, 'original_grid_my_nlogn.dat')
grid2 = create_half_cylinder(40, 'new_grid_nlogn.dat')

knn.interpolate(grid1, grid2)

tecplot.print_tecplot(grid2, 'result_grid_my_nlogn.dat')
