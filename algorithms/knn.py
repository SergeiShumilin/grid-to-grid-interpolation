"""This algorithm uses MO's KNN idea to relocate face's values from one grid to another."""
from numpy import inf
from sklearn.neighbors import KNeighborsRegressor

class KnnApproximator:
    """
    The underlying idea is similar to that of KNN method.
    We assume that original grid's nodes represent a cloud of points.

        1. relocate values in faces of original grid to nodes.
        2. when adding new result grid's node find 1 NEAREST NEIGHBOUR from original grid and take it's value.
        3. finally in the result grid set values in faces calculating it from nodes (the reverse of step 1).

    """
    def __init__(self, original_grid=None, result_grid=None):
        self.original_grid = original_grid
        self.result_grid = result_grid

    def interpolate(self):
        self.original_grid.relocate_values_from_faces_to_nodes()

    def find_neighbours(self, node):
        neighbour = None
        dist = inf
        for n in self.original_grid.Nodes:
            pass


def interpolate_with_KNN(original_grid, result_grid):
    original_grid.relocate_values_from_faces_to_nodes()

    X_train = original_grid.coordinates_to_array()
    y_train = original_grid.values_from_nodes_to_array()
    X_test = result_grid.coordinates_to_array()

    knn = KNeighborsRegressor(n_neighbors=1, weights='distance')
    knn.fit(X_train, y_train)

    predicted = knn.predict(X_test)
    result_grid.set_node_values(predicted)

    result_grid.relocate_values_from_faces_to_nodes()
