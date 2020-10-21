"""This module implements basic geometrical routines."""

from tecplot import writer
from matplotlib.tri import Triangulation
import matplotlib.pyplot as plt
from numpy import linspace, meshgrid, sin, cos, pi, logspace, zeros, arccos, arcsin, sqrt, isnan
from triangular_grid.edge import Edge
from triangular_grid.grid import Grid
import numpy as np

def set_faces(grid, nodes, faces):
    """
    Link faces and nodes according to the connectivity list.

    1 2 3  -> Face 1
    2 3 4  -> Face 2

    Also, edges are created and linked basing on their presence in triangular_grid.Edge.

    :param grid: Grid object.
    :param nodes: list : nodes to link.
    :param faces: list : faces to link.
    """
    for f in faces:
        n1 = nodes[f.nodes_ids[0] - 1]
        n2 = nodes[f.nodes_ids[1] - 1]
        n3 = nodes[f.nodes_ids[2] - 1]

        # Link faces, nodes and edges.
        e = grid.is_edge_present(n1, n2)
        if e is None:
            e = Edge()
            grid.link_face_and_edge(f, e)
            grid.link_node_and_edge(n1, e)
            grid.link_node_and_edge(n2, e)
            grid.Edges.append(e)
        else:
            grid.link_face_and_edge(f, e)

        e = grid.is_edge_present(n2, n3)
        if e is None:
            e = Edge()
            grid.link_face_and_edge(f, e)
            grid.link_node_and_edge(n2, e)
            grid.link_node_and_edge(n3, e)
            grid.Edges.append(e)
        else:
            grid.link_face_and_edge(f, e)

        e = grid.is_edge_present(n3, n1)
        if e is None:
            e = Edge()
            grid.link_face_and_edge(f, e)
            grid.link_node_and_edge(n3, e)
            grid.link_node_and_edge(n1, e)
            grid.Edges.append(e)
        else:
            grid.link_face_and_edge(f, e)


def create_half_cylinder(m=3, n=5, filename='half_cylinder', create_dat=True, plot_pyplot=False):
    """Returns Grid object representing half cylinder.

    Args:
        m:
          Number of points along x axis.
        n:
          Number of point along y axis.
        filename:
          Name of the TECPLOT (.dat) file to write in.
          Only works if create_dat = True (default).
        create_dat:
          Crate TECPLOT (.dat) file. Default True.
        plot_pyplot:
          Plot pyplot view of the grid.

    Returns:
        Grid object
    """
    u = linspace(0, pi, num=m, endpoint=True)
    v = linspace(0, 3, num=n, endpoint=True)

    u, zs = meshgrid(u, v)

    delaunuy = Triangulation(u.flatten(), zs.flatten())
    xs = sin(u)
    ys = cos(u)

    x = ys.flatten()
    y = zs.flatten()
    z = xs.flatten()

    mgrid = Grid()
    mgrid.set_nodes_and_faces(x, y, z, delaunuy.triangles)
    set_faces(mgrid, mgrid.Nodes, mgrid.Faces)
    mgrid.init_adjacent_faces_list_for_border_nodes()

    if plot_pyplot:
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_trisurf(x, y, z, triangles=delaunuy.triangles)
        plt.show()

    if create_dat:
        if not filename.endswith('.dat'):
            filename += '.dat'
        writer.write_tecplot(mgrid, filename)

    assert len(mgrid.Edges) < 3 * len(mgrid.Nodes) - 3, 'Wrong number of edges'
    assert len(mgrid.Faces) < 2 * len(mgrid.Nodes) - 2, 'Wrong number of faces'

    return mgrid


def create_plane(n, m, filename='plane', create_dat=True, plot_pyplot=False, nodes_distribution='uniform'):
    """Returns Grid object representing plain.

    Args:
        m:
          Number of points along x axis.
        n:
          Number of point along y axis.
        filename:
          Name of the TECPLOT (.dat) file to write in.
          Only works if create_dat = True (default).
        create_dat:
          Crate TECPLOT (.dat) file. Default True.
        plot_pyplot:
          Plot pyplot view of the grid.
        nodes_distribution:
          distribution of points along x axis
            uniform:
            logarithmic:

    Returns:
        Grid object
    """
    if nodes_distribution == 'uniform':
        u = linspace(0, 1, n, endpoint=True)
    else:
        u = logspace(-2, 0, n, base=2.0, endpoint=True)

    v = linspace(0, 1, m, endpoint=True)

    u, v = meshgrid(u, v)

    delaunuy = Triangulation(u.flatten(), v.flatten())

    z = zeros(u.shape)

    x = u.flatten()
    y = v.flatten()
    z = z.flatten()

    mgrid = Grid()
    mgrid.set_nodes_and_faces(x, y, z, delaunuy.triangles)
    set_faces(mgrid, mgrid.Nodes, mgrid.Faces)
    mgrid.init_adjacent_faces_list_for_border_nodes()

    if plot_pyplot:
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_trisurf(x, y, z, triangles=delaunuy.triangles)
        plt.show()

    if create_dat:
        if not filename.endswith('.dat'):
            filename += '.dat'
        writer.write_tecplot(mgrid, filename)

    assert len(mgrid.Edges) < 3 * len(mgrid.Nodes) - 3, 'Wrong number of edges'
    assert len(mgrid.Faces) < 2 * len(mgrid.Nodes) - 2, 'Wrong number of faces'

    return mgrid


def create_circle(n, m, filename='plane', create_dat=True, plot_pyplot=False, nodes_distribution='uniform'):
    """Returns Grid object representing plain.
    #todo When n=4, m=4, something ruins
    Args:
        m:
          Number of points along x axis.
        n:
          Number of point along y axis.
        filename:
          Name of the TECPLOT (.dat) file to write in.
          Only works if create_dat = True (default).
        create_dat:
          Crate TECPLOT (.dat) file. Default True.
        plot_pyplot:
          Plot pyplot view of the grid.
        nodes_distribution:
          distribution of points along x axis
            uniform:
            logarithmic:

    Returns:
        Grid object
    """
    u = linspace(-1, 1, m, endpoint=True)

    v = linspace(-1, 1, n, endpoint=True)

    u, v = meshgrid(u, v)

    coss = []
    sins = []
    for _u, _v in zip(u.flatten(), v.flatten()):
        hip = sqrt(_u ** 2 + _v ** 2)
        if hip == 0:
            coss.append(0)
            sins.append(0)
            continue
        coss.append(_u / hip)
        sins.append(_v / hip)

    delaunuy = Triangulation(coss, sins)

    z = zeros(u.shape)

    x = coss
    y = sins
    z = z.flatten()

    mgrid = Grid()
    mgrid.set_nodes_and_faces(x, y, z, delaunuy.triangles)
    set_faces(mgrid, mgrid.Nodes, mgrid.Faces)
    mgrid.init_adjacent_faces_list_for_border_nodes()

    if plot_pyplot:
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_trisurf(x, y, z, triangles=delaunuy.triangles)
        plt.show()

    if create_dat:
        if not filename.endswith('.dat'):
            filename += '.dat'
        writer.write_tecplot(mgrid, filename)

    assert len(mgrid.Edges) < 3 * len(mgrid.Nodes) - 3, 'Wrong number of edges'
    assert len(mgrid.Faces) < 2 * len(mgrid.Nodes) - 2, 'Wrong number of faces'

    return mgrid

def cross(triangles):
    """
    Returns the cross product of two edges from input triangles
    Parameters
    --------------
    triangles: (n, 3, 3) float
      Vertices of triangles
    Returns
    --------------
    crosses : (n, 3) float
      Cross product of two edge vectors
    """
    vectors = np.diff(triangles, axis=1)
    crosses = np.cross(vectors[:, 0], vectors[:, 1])
    return crosses

def area(triangles=None, crosses=None, sum=False):
    """
    Calculates the sum area of input triangles
    Parameters
    ----------
    triangles : (n, 3, 3) float
      Vertices of triangles
    crosses : (n, 3) float or None
      As a speedup don't re- compute cross products
    sum : bool
      Return summed area or individual triangle area
    Returns
    ----------
    area : (n,) float or float
      Individual or summed area depending on `sum` argument
    """
    if crosses is None:
        crosses = cross(triangles)
    area = (np.sum(crosses**2, axis=1)**.5) * .5
    if sum:
        return np.sum(area)
    return area


def create_cylinder(height=1, radius=0.5, angle=None, sections=None, filename='cylinder', create_dat=True, plot_pyplot=False):
    half = abs(float(height)) / 2.0
    # create a profile to revolve
    linestring = [[0, -half],
                  [radius, -half],
                  [radius, half],
                  [0, half]]

    linestring = np.asanyarray(linestring, dtype=np.float64)

    # linestring must be ordered 2D points
    if len(linestring.shape) != 2 or linestring.shape[1] != 2:
        raise ValueError('linestring must be 2D!')

    if angle is None:
        # default to closing the revolution
        angle = np.pi * 2
        closed = True
    else:
        # check passed angle value
        closed = angle >= ((np.pi * 2) - 1e-8)

    if sections is None:
        # default to 32 sections for a full revolution
        sections = int(angle / (np.pi * 2) * 32)
    # change to face count
    sections += 1
    # create equally spaced angles
    theta = np.linspace(0, angle, sections)

    # 2D points around the revolution
    points = np.column_stack((np.cos(theta), np.sin(theta)))

    # how many points per slice
    per = len(linestring)
    # use the 2D X component as radius
    radius = linestring[:, 0]
    # use the 2D Y component as the height along revolution
    height = linestring[:, 1]
    # a lot of tiling to get our 3D vertices
    vertices = np.column_stack((
        np.tile(points, (1, per)).reshape((-1, 2)) *
        np.tile(radius, len(points)).reshape((-1, 1)),
        np.tile(height, len(points))))

    if closed:
        # should be a duplicate set of vertices
        assert np.allclose(vertices[:per],
                           vertices[-per:])
        # chop off duplicate vertices
        vertices = vertices[:-per]

    # how many slices of the pie
    slices = len(theta) - 1

    # start with a quad for every segment
    # this is a superset which will then be reduced
    quad = np.array([0, per, 1,
                     1, per, per + 1])
    # stack the faces for a single slice of the revolution
    single = np.tile(quad, per).reshape((-1, 3))
    # `per` is basically the stride of the vertices
    single += np.tile(np.arange(per), (2, 1)).T.reshape((-1, 1))
    # remove any zero-area triangle
    # this covers many cases without having to think too much
    single = single[area(vertices[single]) > 1e-8]

    # how much to offset each slice
    # note arange multiplied by vertex stride
    # but tiled by the number of faces we actually have
    offset = np.tile(np.arange(slices) * per,
                     (len(single), 1)).T.reshape((-1, 1))
    # stack a single slice into N slices
    stacked = np.tile(single.ravel(), slices).reshape((-1, 3))

    # offset stacked and wrap vertices
    faces = (stacked + offset) % len(vertices)

    x = vertices[:, 0]
    y = vertices[:, 1]
    z = vertices[:, 2]
    mgrid = Grid()
    mgrid.set_nodes_and_faces(x, y, z, faces)
    set_faces(mgrid, mgrid.Nodes, mgrid.Faces)
    mgrid.init_adjacent_faces_list_for_border_nodes()

    if plot_pyplot:
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_trisurf(x, y, z, triangles=faces)
        plt.show()

    if create_dat:
        if not filename.endswith('.dat'):
            filename += '.dat'
        writer.write_tecplot(mgrid, filename)

    assert len(mgrid.Edges) < 3 * len(mgrid.Nodes) - 3, 'Wrong number of edges'
    assert len(mgrid.Faces) < 2 * len(mgrid.Nodes) - 2, 'Wrong number of faces'

    return mgrid


def create_custom_cylinder(m, n, plot_pyplot=False):
    u = linspace(-1, 1, m, endpoint=True)

    v = linspace(-1, 1, n, endpoint=True)

    u, v = meshgrid(u, v)

    delaunuy = Triangulation(u.flatten(), v.flatten())

    COORDS = zeros((m*n, 3))

    tx = np.array([-1.0, 0, 1.0, 0])
    ty = np.array([0, 1.0, 0, -1.0])
    z = np.linspace(0, 1, num=n, endpoint=True)

    for j in range(n):
        for i in range(m):
            COORDS[i + j * m, 0] = tx[i % n]
            COORDS[i + j * m, 1] = ty[i % n]
            COORDS[i + j * m, 2] = z[j]

    x = COORDS[:, 0]
    y = COORDS[:, 1]
    z = COORDS[:, 2]
    print(x)
    print(y)
    print(z)
    print(len(delaunuy.triangles))
    print(len(x))
    assert len(x) == len(delaunuy.triangles)
    assert len(x) == m * n

    if plot_pyplot:
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_trisurf(x, y, z, triangles=delaunuy.triangles)
        plt.show()