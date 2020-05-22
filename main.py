from grid import grid, node, tecplot, face, tecplot_crystal
from matplotlib.tri import Triangulation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from algorithms import knn, kdtree
import time
from test.test import test_all


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
        tecplot.print_tecplot(mgrid, filename)

    return mgrid


# grid1 = create_half_cylinder(20, 5, 'original_grid_kdtree.dat')
# grid2 = create_half_cylinder(20, 5, 'new_grid_kdtree.dat')
# kdtree.interpolate(grid1, grid2)
# tecplot.print_tecplot(grid2, 'result_grid_kdtree.dat')

# fig = plt.figure(figsize=(10, 10))
# ax = fig.add_subplot()
# ns = []
# square_times = []
# kdtree_times = []
# n2s = []
# nlogns = []
# logns = []
#
# for x in range(5, 500, 50):
#     print('--------------------------------------')
#     print('Текущий размер сетки:', x * x)
#     grid1 = create_half_cylinder(x, x, 'original_grid_kdtree.dat', create_dat=False)
#     print('Триангуляция оригинального цилиндра')
#     grid2 = create_half_cylinder(x, x, 'new_grid_kdtree.dat', create_dat=False)
#     print('Триангуляция нового цилиндра')
#     start = time.time()
#     print('Интерполяция квадратичная')
#     #knn.interpolate(grid1, grid2)
#     #square_times.append(time.time() - start)
#     start = time.time()
#     print('Интерполяция kdtree')
#     kdtree.interpolate(grid1, grid2)
#     kdtree_times.append(time.time() - start)
#
#     ns.append(x * x)
#     n2s.append((x * x) * 2)
#     nlogns.append(x * np.log2(x))
#     logns.append(np.log2(x))
#
# #ax.plot(ns, square_times, label='brute force')
# ax.plot(ns, kdtree_times, label='kd tree')
# #ax.plot(ns, n2s, label='n^2')
# ax.plot(ns, nlogns, label='nlogn')
# ax.plot(ns, logns, label='logn')
# plt.legend()
# plt.show()
test_all()

start = time.time()
grid1 = grid.Grid()
grid2 = grid.Grid()
tecplot_crystal.read_tecplot(grid1, 'air_inlet_2700000000.dat')
print('считалась первая сетка')
tecplot_crystal.read_tecplot(grid2, 'air_inlet.dat')
print('считалась вторая сетка')
kdtree.interpolate(grid1, grid2, by_value='T')
kdtree.interpolate(grid1, grid2, by_value='Hw')
print('прошла интерполяция')
tecplot_crystal.print_tecplot(grid2, 'air2.dat')
print('время работы:', time.time() - start)
