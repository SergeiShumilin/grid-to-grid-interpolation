"""This algorithm uses MO's KNN idea to relocate face's values from one grid to another."""

class KnnApproximator:
    """
    The underlying idea is similar to that of KNN method.
    We assume that original grid's nodes represent a cloud of points.

        1. relocate values in faces of original grid to nodes.
        2. when adding new result grid's node find 1 NEAREST NEIGHBOUR from original grid and take it's value.
        3. finally in the result grid set values in faces calculating it from nodes (the reverse of step 1).

    """
    def __init__(self, original_grid=None, result_grid=None):
        pass
