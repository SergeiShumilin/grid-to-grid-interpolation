from grid.node import Node
from numpy import inf
from geom.basic import euclidian_distance

NODE_COMPARISON_ACCURACY = 10e-18

class AVLTreeNode:
    def __init__(self, key=None):
        self.left = None
        self.right = None
        self.key = key
        self.parent = None
        self.balance = 0
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None
        self.n = 0

    def insert(self, key):
        self.root = self._insert(self.root, key)
        self.n += 1

    def _insert(self, root, key):
        if not root:
            return AVLTreeNode(key)

        if key.coordinates() < root.key.coordinates():
            left_sub_root = self._insert(root.left, key)
            root.left = left_sub_root
            left_sub_root.parent = root
        elif key.coordinates() > root.key.coordinates():
            right_sub_root = self._insert(root.right, key)
            root.right = right_sub_root
            right_sub_root.parent = root
        else:
            raise ValueError('The tree cannot contain identical keys')

        root.height = max(self._get_height(root.left), self._get_height(root.right)) + 1
        root.balance = self._get_height(root.left) - self._get_height(root.right)

        return root

    def find(self, key, return_nearest=False):
        """Find the key in the tree.
        :param key: Node the node to find
        :param return_nearest: returns the nearest of the nodes by euclidean distance."""
        nbr_dist = [None, inf]
        found = self._find(self.root, key, nbr_dist)
        if return_nearest:
            return nbr_dist[0]
        else:
            return found

    def _find(self, root: AVLTreeNode, key: Node, nbr_dist) -> (AVLTreeNode, None):
        """Find key in the tree.
        :param nbr_dist: saves nearest encountered node and distance to it."""
        if not root:
            return None

        d = euclidian_distance(key, root.key)
        if d < nbr_dist[1]:
            nbr_dist[1] = d
            nbr_dist[0] = root

        if d < NODE_COMPARISON_ACCURACY:
            return root

        if root.left:
            dist_to_left = euclidian_distance(key, root.left.key)
        if root.right:
            dist_to_right = euclidian_distance(key, root.right.key)

        if root.left and root.right:
            if dist_to_left < dist_to_right:
                return self._find(root.left, key, nbr_dist)
            else:
                return self._find(root.right, key, nbr_dist)
        elif not root.left and not root.right:
            return None  # todo это только если ищем ближайшего.
        elif root.left and not root.right:
            return self._find(root.left, key, nbr_dist)
        elif root.right and not root.left:
            return self._find(root.right, key, nbr_dist)

    @staticmethod
    def _get_height(root: AVLTreeNode) -> int:
        if not root:
            return 0
        return root.height

    def rebalance(self, root: AVLTreeNode) -> AVLTreeNode:
        if root.balance == 2:
            if root.left.balance < 0:  # L-R case
                root.left = self.rotate_left(root.left)
                return self.rotate_right(root)
            else:  # L-L case
                return self.rotate_right(root)

        elif root.balance == -2:
            if root.right.balance > 0:  # R-L case
                root.right = self.rotate_right(root.right)
                return self.rotate_left(root)
            else:  # R-R case
                return self.rotate_left(root)
        else:
            return root

    def rotate_right(self, root: AVLTreeNode) -> AVLTreeNode:
        pivot = root.left  # set up pointers
        tmp = pivot.right

        pivot.right = root
        pivot.parent = root.parent  # pivot's parent now root's parent
        root.parent = pivot  # root's parent now pivot

        root.left = tmp
        if tmp:  # tmp can be null
            tmp.parent = root

        # update pivot's parent (manually check which one matches the root that was passed)
        if pivot.parent:
            if pivot.parent.left == root:  # if the parent's left subtree is the one to be updated
                pivot.parent.left = pivot  # assign the pivot as the new child
            else:
                pivot.parent.right = pivot  # vice-versa for right child

        # update heights and balance's using tracked heights
        root.height = max(self._get_height(root.left), self._get_height(root.right)) + 1
        root.balance = self._get_height(root.left) - self._get_height(root.right)
        pivot.height = max(self._get_height(pivot.left), self._get_height(pivot.right)) + 1
        pivot.balance = self._get_height(pivot.left) - self._get_height(pivot.right)
        return pivot

    def rotate_left(self, root: AVLTreeNode) -> AVLTreeNode:
        pivot = root.right
        tmp = pivot.left

        pivot.left = root
        pivot.parent = root.parent
        root.parent = pivot

        root.right = tmp
        if tmp:
            tmp.parent = root

        if pivot.parent:
            if pivot.parent.left == root:
                pivot.parent.left = pivot
            else:
                pivot.parent.right = pivot

        root.height = max(self._get_height(root.left), self._get_height(root.right)) + 1
        root.balance = self._get_height(root.left) - self._get_height(root.right)
        pivot.height = max(self._get_height(pivot.left), self._get_height(pivot.right)) + 1
        pivot.balance = self._get_height(pivot.left) - self._get_height(pivot.right)
        return pivot
