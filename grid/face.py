"""Module describing grid's face."""


class Face:
    __doc__ = "Module describing grid's face."

    def __init__(self, value=None):
        """
        Construct a face.
        :param id: face's id.
        """
        self.Id = None

        # Nodes and edges set clockwise.
        self.nodes = list()
        self.nodes_ids = list()
        self.edges = list()

        self.V = value

        self.T = None
        self.Hw = None
        self.Hi = None
        self.HTC = None
        self.Beta = None
        self.TauX = None
        self.TauY = None
        self.TauZ = None