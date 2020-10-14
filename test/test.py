from algorithms.avl_tree import AVLTree
from triangular_grid.node import Node
from triangular_grid.grid import Grid
from tecplot.reader import read_tecplot
from triangular_grid.face import Face
from geom.vector import Vector
from geom.point import Point
from geom.basics import *


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

    assert avl.find(n5).Id == 5, 'Wrong node found'
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

    assert avl.find(n5).Id == 5, 'Wrong node found'
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
    n8 = Node(-1, 1.0000000000001, 0, 8)
    n9 = Node(0.0000000000000001, 0, 0, 9)

    nodes = [n1, n2, n3, n4, n5, n6]

    for n in nodes:
        avl.insert(n)

    assert not avl.find(n8), 'Wrong nearest neighbour found. test3.'
    assert not avl.find(n9), 'Wrong nearest neighbour found. test3.'
    print('Test 3 OK')


def test_isomorphism():
    grid = Grid()
    isomorphic_grid = Grid()
    non_isomorphic_grid = Grid()
    read_tecplot(grid, '../wing_1.dat')
    read_tecplot(isomorphic_grid, '../wing_1_tm.dat')
    read_tecplot(non_isomorphic_grid, '../wing_10.dat')

    assert grid.is_isomprphic_to(isomorphic_grid), 'Grids are not isomorphic'
    assert not grid.is_isomprphic_to(non_isomorphic_grid), 'Grids are isomorphic, but shouldn\'t be'
    print('Test isomorphism OK')


def test_normals():
    n1 = Node(0, 0, 0)
    n2 = Node(0, -1, 0)
    n3 = Node(1, 0, 0)
    f = Face()
    f.nodes = [n1, n2, n3]
    assert f.normal().x == 0, 'Wrong normal'
    assert f.normal().y == 0, 'Wrong normal'
    assert f.normal().z == 1, 'Wrong normal'

    n1 = Node(0, 0, 0)
    n2 = Node(0, -1, 0)
    n3 = Node(0, -2, 1)
    f = Face()
    f.nodes = [n1, n2, n3]
    assert f.normal().x == -1, 'Wrong normal'
    assert f.normal().y == 0, 'Wrong normal'
    assert f.normal().z == 0, 'Wrong normal'


def test_dot():
    v1 = Vector(1, 1, 1)
    v2 = Vector(1, 1, 1)
    assert dot_product(v1, v2) == 3, 'Wrong dot product'

    v1 = Vector(0, 0, 0)
    v2 = Vector(0, 0, 0)
    assert dot_product(v1, v2) == 0, 'Wrong dot product'

    v1 = Vector(-1, 0, 1)
    v2 = Vector(2, 1, -1)
    assert dot_product(v1, v2) == -3, 'Wrong dot product'

    v1 = Vector(0.5, 4, -1)
    v2 = Vector(2, 3, 1)
    assert dot_product(v1, v2) == 12, 'Wrong dot product'


def test_cross():
    v1 = Vector(1, 1, 1)
    v2 = Vector(1, 1, 1)
    assert cross_product(v1, v2).x == 0, 'Wrong cross product'
    assert cross_product(v1, v2).y == 0, 'Wrong cross product'
    assert cross_product(v1, v2).z == 0, 'Wrong cross product'

    v1 = Vector(-1, 4, 19)
    v2 = Vector(1.5, 5, -3)
    assert cross_product(v1, v2).x == -107, 'Wrong cross product'
    assert cross_product(v1, v2).y == 25.5, 'Wrong cross product'
    assert cross_product(v1, v2).z == -11, 'Wrong cross product'

    v1 = Vector(-1, -1, -13)
    v2 = Vector(-32, -1, -12.4)
    assert cross_product(v1, v2).x == -0.5999999999999996, 'Wrong cross product'
    assert cross_product(v1, v2).y == 403.6, 'Wrong cross product'
    assert cross_product(v1, v2).z == -31, 'Wrong cross product'


def test_area():
    n1 = Node(0, 0, 0)
    n2 = Node(0, -0.5, 0)
    n3 = Node(1, -0.5, 0)
    f = Face()
    f.nodes = [n1, n2, n3]
    assert f.area() == 0.25, 'Wrong area'

    n1 = Node(10, -7, 1.45)
    n2 = Node(82, -0.5, 0)
    n3 = Node(1.222, 56, -18)
    f = Face()
    f.nodes = [n1, n2, n3]
    assert f.area() == 2402.8282235671577, 'Wrong area'

    n1 = Node(0.0001, 0.1122, -0.00012)
    n2 = Node(0.000001, -0.23123, -0.00000005)
    n3 = Node(1.222, -0.231200000001, -18)
    f = Face()
    f.nodes = [n1, n2, n3]
    assert f.area() == 3.0979846549411496, print(f.area())


def test_vector():
    v = Vector()
    v2 = Vector(1, 0.1, -1)
    assert v.coords() == (0, 0, 0), "Wrong vector initialization"
    v.sum(v2)
    assert v.coords() == (1, 0.1, -1), 'Wrong vector sum'
    v.sub(v2)
    assert v.coords() == (0, 0, 0), 'Wrong subtraction'
    v.sum(v2)
    assert v.coords() == (1, 0.1, -1), print('Wrong vector sum', v.coords())
    v.mul(3.1)
    assert v.coords() == (3.1, 0.31000000000000005, -3.1), print('Wrong vector multiplication', v.coords())
    v.dev(2)
    assert v.coords() == (1.55, 0.15500000000000003, -1.55), print('Wrong vector division', v.coords())


def test_all():
    test_comparing_of_nodes()
    test_avl()
    test2()
    test3()
    # test_isomorphism()
    test_vector()
    test_normals()
    test_dot()
    test_cross()
    test_area()


if __name__ == '__main__':
    test_all()
