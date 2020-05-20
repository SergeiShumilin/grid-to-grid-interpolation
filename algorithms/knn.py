"""This algorithm uses MO's KNN idea to relocate face's values from one grid to another."""
from numpy import inf
from geom import basic
from algorithms.avl_tree import AVLTree, AVLTreeNode


def my_squared_knn(old_grid, new_grid) -> list:
    """My implementation of ordinary knn with squared search.
    The underlying idea is similar to that of KNN method.
    We assume that original grid's nodes represent a cloud of points.

        1. relocate values in faces of original grid to nodes.
        2. when adding new result grid's node find 1 NEAREST NEIGHBOUR from original grid and take it's value.
        3. finally in the result grid set values in faces calculating it from nodes (the reverse of step 1)."""
    res = list()

    for new_n in new_grid.Nodes:
        neighbour = None
        dist = inf
        for old_n in old_grid.Nodes:
            new_dist = basic.euclidian_distance(new_n, old_n)
            if new_dist < dist:
                neighbour = old_n
                dist = new_dist

        res.append(neighbour.value)

    return res


def my_nlogn_knn(old_grid, new_grid):
    """Implementation of knn with binary search of the neighbour using AVL tree."""
    avl = AVLTree()
    res = list()

    for node in old_grid.Nodes:
        avl.insert(node)
    print('уже создали дерево')
    for new_n in new_grid.Nodes:
        print('ищем узел')
        neighbour = avl.find(new_n, return_nearest=True)
        res.append(neighbour.key.value)

        neighbour2 = None
        dist = inf
        for old_n in old_grid.Nodes:
            new_dist = basic.euclidian_distance(new_n, old_n)
            if new_dist < dist:
                neighbour2 = old_n
                dist = new_dist

        if neighbour.key is not neighbour2:
            print('Они не совпали')
            print(new_n.coordinates())
            print(neighbour.key.coordinates())
            print(neighbour2.coordinates())
            exit(1)

    return res


def interpolate(old_grid, new_grid):
    """Relocate values from the old grid to the new one."""
    old_grid.relocate_values_from_faces_to_nodes()
    predicted = my_squared_knn(old_grid, new_grid)
    new_grid.set_node_values(predicted)
    new_grid.relocate_values_from_nodes_to_faces()
