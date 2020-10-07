from scipy.spatial import KDTree
from scipy.interpolate import griddata

def interpolate_(old_grid, new_grid):
    old_nodes = old_grid.return_coordinates_as_a_ndim_array()
    kdtree = KDTree(old_nodes)

    for new_n in new_grid.Nodes:
        i = kdtree.query(new_n.coordinates())[1]
        neighbour = old_grid.Nodes[i]

        new_n.T = neighbour.T
        new_n.Hw = neighbour.Hw


def interpolate_with_relocation(old_grid, new_grid):
    """Interpolation with relocation of values in consideration from
       faces to nodes - interpolate using knn - from nodes to faces.
    """
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


def linear_interpolation(old_grid, new_grid):
    old_grid.compute_aux_nodes()
    new_grid.compute_aux_nodes()
    old_aux_nodes = old_grid.return_aux_nodes_as_a_ndim_array()
    new_aux_nodes = new_grid.return_aux_nodes_as_a_ndim_array()
    values_T = old_grid.return_paramenter_as_ndarray(parameter='T')
    values_Hw = old_grid.return_paramenter_as_ndarray(parameter='Hw')
    res_T = griddata(old_aux_nodes, values_T, new_aux_nodes, method='linear')
    res_Hw = griddata(old_aux_nodes, values_Hw, new_aux_nodes, method='linear')
    new_grid.set_aux_nodes_parameters(res_T.T, 'T')
    new_grid.set_aux_nodes_parameters(res_Hw.T, 'Hw')

methods = {'cell_centered': face_centered_interpolation,
           'with_relocation': interpolate_with_relocation}
