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


def face_centered_interpolation(old_grid, new_grid):
    old_grid.compute_aux_nodes()
    new_grid.compute_aux_nodes()
    old_aux_nodes = old_grid.return_aux_nodes_as_a_ndim_array()
    kdtree = KDTree(old_aux_nodes)
    for f in new_grid.Faces:
        i = kdtree.query(f.aux_node.coordinates())[1]
        f.T = old_grid.Faces[i].T
        f.Hw = old_grid.Faces[i].Hw
