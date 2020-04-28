"""This algorithm uses MO's KNN idea to relocate face's values from one grid to another."""
from numpy import inf
from sklearn.neighbors import KNeighborsRegressor
from geom import basic


def my_squared_knn(old_grid, new_grid):
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
    """Implementation of knn with binary search of the neighbour."""


def sklearn_knn(old_grid, new_grid):
    """Implementation with sklearn's KNN."""
    X_train = old_grid.coordinates_to_array()
    y_train = old_grid.values_from_nodes_to_array()
    X_test = new_grid.coordinates_to_array()
    knn = KNeighborsRegressor(n_neighbors=1, weights='distance')
    knn.fit(X_train, y_train)
    return knn.predict(X_test)


def interpolate(old_grid, new_grid):
    """Relocate values from the old grid to the new one.
    """
    old_grid.relocate_values_from_faces_to_nodes()
    predicted = my_squared_knn(old_grid, new_grid)
    new_grid.set_node_values(predicted)
    new_grid.relocate_values_from_nodes_to_faces()
