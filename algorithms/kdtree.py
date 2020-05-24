from scipy.spatial import KDTree


def interpolate_(old_grid, new_grid):
    old_nodes = old_grid.return_coordinates_as_a_ndim_array()
    kdtree = KDTree(old_nodes)

    for new_n in new_grid.Nodes:
        i = kdtree.query(new_n.coordinates())[1]
        neighbour = old_grid.Nodes[i]

        new_n.T = neighbour.T
        new_n.Hw = neighbour.Hw


def interpolate(old_grid, new_grid):
    """Interpolate grids using K-D tree."""
    old_grid.relocate_values_from_faces_to_nodes()
    interpolate_(old_grid, new_grid)
    new_grid.relocate_values_from_nodes_to_faces()
