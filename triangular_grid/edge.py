"""Module describing triangular_grid's edge."""


class Edge:
    __doc__ = "Module describing triangular_grid's edge."

    def __init__(self):
        """
        Construct an edge.
        :param id: edge's id.
        """
        self.Id = None
        self.nodes = list()
        self.faces = list()
        self.border = False
