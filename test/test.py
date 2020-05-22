from algorithms.avl_tree import AVLTree
from grid.node import Node


def test_comparing_of_nodes():
    n1 = Node(0, 0, 0, 1)
    n2 = Node(1, 0, 0, 2)
    n3 = Node(10e-18, 0, 0)
    n4 = Node(10e-17, 0, 0)
    n5 = Node(0, 10e-18, 0)
    n6 = Node(0, 10e-17, 0)
    n7 = Node(0, 0, 10e-18)
    n8 = Node(0, 0, 10e-17)
    assert AVLTree.is_node_less(n1, n2), 'Wrong node comparison'
    assert AVLTree.is_node_less(n3, n4), 'Wrong node comparison'
    assert AVLTree.is_node_less(n5, n6), 'Wrong node comparison'
    assert AVLTree.is_node_less(n7, n8), 'Wrong node comparison'
    print('Node comparison OK')


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

    assert avl.find(n5).value == 5, 'Wrong node found'
    assert not avl.find(n6), 'Wrong node found'
    print('Test 1 OK')


def test2():
    avl = AVLTree()

    n1 = Node(0, 0, 0, 1)
    n2 = Node(1, 0, 0, 2)
    n3 = Node(-1, 0, 0, 3)
    n4 = Node(1, 1, 0, 4)
    n5 = Node(1, -1, 0.000000000000001, 5)
    n6 = Node(1, -1, 0.0000000000000001, 6)

    nodes = [n1, n2, n3, n4, n5]

    for n in nodes:
        avl.insert(n)

    assert avl.find(n5).value == 5, 'Wrong node found'
    assert not avl.find(n6), 'Wrong node found'
    print('Test 2 OK')


def test3():
    avl = AVLTree()

    n1 = Node(0, 0, 0, 1)
    n2 = Node(1, 0, 0, 2)
    n4 = Node(-1, 1, 0, 4)
    n3 = Node(-1, 0, 0, 3)
    n5 = Node(-1, 2, 0, 5)
    n6 = Node(-1, 3, 0, 6)
    n7 = Node(-0.6, 0, 0, 7)
    n8 = Node(-1, 1.0000000000001, 0, 8)
    n9 = Node(0.0000000000000001, 0, 0, 9)

    nodes = [n1, n2, n3, n4, n5, n6]

    for n in nodes:
        avl.insert(n)

    assert not avl.find(n8), 'Wrong nearest neighbour found. test3.'
    assert not avl.find(n9), 'Wrong nearest neighbour found. test3.'
    print('Test 3 OK')


def test_all():
    test_comparing_of_nodes()
    test_avl()
    test2()
    test3()


if __name__ == '__main__':
    test_all()
