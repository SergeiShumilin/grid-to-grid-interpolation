"""Module describing grid's node"""


class Node:
    __doc__ = "class describing node"

    def __init__(self, x=None, y=None, z=None, value=None):
        """
        Construct node.
        :param id: node's id in the grid.
        """
        self.Id = None
        self.x = x
        self.y = y
        self.z = z

        self.value = value
        self.faces = list()
        self.edges = list()

    def coordinates(self) -> tuple:
        return (self.x, self.y, self.z)