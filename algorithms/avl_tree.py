from grid.node import Node

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

        if key.coordinates < root.key.coordinates:
            left_sub_root = self._insert(root.left, key)
            root.left = left_sub_root
            left_sub_root.parent = root
        elif key.coordinates > root.key.coordinates:
            right_sub_root = self._insert(root.right, key)
            root.right = right_sub_root
            right_sub_root.parent = root
        else:
            raise ValueError('The tree cannot contain identical keys')

        root.height = max(self._get_height(root.left), self._get_height(root.right)) + 1
        root.balance = self._get_height(root.left) - self._get_height(root.right)

    def find(self, coordinates: tuple) -> Node:
        pass

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
                root.left = self.rotate_right(root.left)
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
