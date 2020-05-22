from grid.node import Node

NODE_COMPARE_ACCURACY = 10e-18


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

        if self.is_node_less(key, root.key):
            left_sub_root = self._insert(root.left, key)
            root.left = left_sub_root
            left_sub_root.parent = root
        elif self.is_node_less(root.key, key):
            right_sub_root = self._insert(root.right, key)
            root.right = right_sub_root
            right_sub_root.parent = root
        else:
            print(key.coordinates())
            print(root.key.coordinates())

            raise ValueError('The tree cannot contain identical keys')

        root.height = max(self._get_height(root.left), self._get_height(root.right)) + 1
        root.balance = self._get_height(root.left) - self._get_height(root.right)

        return self.rebalance(root)

    def find(self, key):
        """Find the key in the tree.
        :param key: Node the node to find"""
        found = self._find(self.root, key)
        if not found:
            return None
        else:
            return found.key

    def _find(self, root: AVLTreeNode, key: Node) -> (AVLTreeNode, None):
        """Find key in the tree."""
        if not root:
            return None

        if self.is_node_less(key, root.key):
            return self._find(root.left, key)
        elif self.is_node_less(root.key, key):
            return self._find(root.right, key)
        else:
            return root

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

    @staticmethod
    def is_node_less(n1: Node, n2: Node) -> bool:
        """Is n1 < n2 coordinate-wise."""
        if abs(n1.x - n2.x) > NODE_COMPARE_ACCURACY:
            if n1.x < n2.x:
                return True
            else:
                return False
        else:
            if abs(n1.y - n2.y) > NODE_COMPARE_ACCURACY:
                if n1.y < n2.y:
                    return True
                else:
                    return False
            else:
                if abs(n1.z - n2.z) > NODE_COMPARE_ACCURACY:
                    if n1.z < n2.z:
                        return True
                    else:
                        return False
                else:
                    return False
