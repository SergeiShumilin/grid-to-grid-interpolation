"""Module describing _grid's face."""
from .node import Node


class Face:
    __doc__ = "Module describing _grid's face."

    def __init__(self, Id=None):
        """
        Construct a face.
        :param id: face's id.
        """
        self.Id = Id

        # Nodes and edges set clockwise.
        self.nodes = list()
        self.nodes_ids = list()
        self.edges = list()

        self.T = None
        self.Hw = None
        self.Hi = None
        self.HTC = None
        self.Beta = None
        self.TauX = None
        self.TauY = None
        self.TauZ = None
        self.aux_node = Node()
