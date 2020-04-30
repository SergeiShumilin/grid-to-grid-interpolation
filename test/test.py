from algorithms.avl_tree import AVLTree
from grid.node import Node


def test_avl():
    avl = AVLTree()

    n1 = Node(0, 0, 0, 1)
    n2 = Node(1, 0, 0, 2)
    n3 = Node(-1, 0, 0, 3)
    n4 = Node(1, 1, 0, 4)
    n5 = Node(1, -1, 0, 5)
    n6 = Node(1, -1, 1, 6)

    nodes = [n1, n2, n3, n4, n5]

    for n in nodes:
        avl.insert(n)

    assert avl.find(n5).key.value == 5, 'Wrong node found'
    assert not avl.find(n6), 'Wrong node found'
    assert avl.find(n5, return_nearest=True).key.value == 5, 'Wrong nearest neighbour found (search for itself)'
    assert avl.find(n6, return_nearest=True).key.value == 5, 'Wrong nearest neighbour found'


if __name__ == '__main__':
    test_avl()
