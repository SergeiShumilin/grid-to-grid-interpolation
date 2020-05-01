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
    print('Test 1 OK')


def test2():
    avl = AVLTree()

    n1 = Node(0, 0, 0, 1)
    n2 = Node(1, 0, 0, 2)
    n3 = Node(-1, 0, 0, 3)
    n4 = Node(1, 1, 0, 4)
    n5 = Node(1, -1, 0.000000000000001, 5)
    n6 = Node(1, -1, 0.0000000000000001, 6)
    n7 = Node(-1, 0, 0.0000000000000001, 7)

    nodes = [n1, n2, n3, n4, n5]

    for n in nodes:
        avl.insert(n)

    assert avl.find(n5).key.value == 5, 'Wrong node found'
    assert not avl.find(n6), 'Wrong node found'
    assert avl.find(n5, return_nearest=True).key.value == 5, 'Wrong nearest neighbour found (search for itself)'
    assert avl.find(n6, return_nearest=True).key.value == 5, 'Wrong nearest neighbour found'
    assert avl.find(n1, return_nearest=True).key.value == 1, 'Wrong nearest neighbour found'
    assert avl.find(n3, return_nearest=True).key.value == 3, 'Wrong nearest neighbour found'
    assert avl.find(n6, return_nearest=True).key.value == 5, 'Wrong nearest neighbour found'
    assert avl.find(n7, return_nearest=True).key.value == 3, 'Wrong nearest neighbour found'
    print('Test 2 OK')


if __name__ == '__main__':
    test_avl()
    test2()
