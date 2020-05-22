from scipy.spatial import KDTree
from numpy import inf
from geom.basic import euclidian_distance


def interpolate_(old_grid, new_grid):
    res = []
    old_nodes = old_grid.return_coordinates_as_a_ndim_array()
    kdtree = KDTree(old_nodes)

    for new_n in new_grid.Nodes:
        i = kdtree.query(new_n.coordinates())[1]
        neighbour = old_grid.Nodes[i]
        res.append(neighbour.T)

        # neighbour2 = None
        # dist = inf
        # for old_n in old_grid.Nodes:
        #     new_dist = euclidian_distance(new_n, old_n)
        #     if new_dist < dist:
        #         neighbour2 = old_n
        #         dist = new_dist
        #
        # if neighbour is not neighbour2:
        #     print('Они не совпали')
        #     print(new_n.coordinates())
        #     print(neighbour.key.coordinates())
        #     print(neighbour2.coordinates())
        #     exit(1)

    return res


def interpolate(old_grid, new_grid):
    """Interpolate grids using K-D tree."""
    old_grid.relocate_values_from_faces_to_nodes(value='T')
    print('значения перемещены из граней в узлы')
    predicted = interpolate_(old_grid, new_grid)
    print('произведена интерполяция')
    new_grid.set_node_values(predicted, value='T')
    print('полученные значения перенесены в узлы')
    del predicted
    new_grid.relocate_values_from_nodes_to_faces(value='T')
    print('значения перемещены из узлов в грани')
