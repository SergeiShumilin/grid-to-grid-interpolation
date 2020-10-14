"""This module implements basic geometrical routines."""

from tecplot import writer
from matplotlib.tri import Triangulation
import matplotlib.pyplot as plt
from numpy import linspace, meshgrid, sin, cos, pi, logspace, zeros
from triangular_grid.edge import Edge
from triangular_grid.grid import Grid


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

    z = sin(u + v)

    x = u.flatten()
    y = v.flatten()
    z = z.flatten()

    mgrid = Grid()
    mgrid.set_nodes_and_faces(x, y, z, delaunuy.triangles)
    set_faces(mgrid, mgrid.Nodes, mgrid.Faces)

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
