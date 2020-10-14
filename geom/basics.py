"""This module implements basic geometrical routines."""

from numpy import sqrt
from .vector import Vector
from .point import Point
from triangular_grid.edge import Edge


def edge_to_vector(e: Edge) -> Vector:
    assert len(e.nodes) == 2, 'Wrong number of nodes in the edge'
    n1 = e.nodes[0]
    n2 = e.nodes[1]
    p1 = point_to_vector(n1.as_point())
    p2 = point_to_vector(n2.as_point())
    return Vector.subtract_vectors(p2, p1)


def dot_product(v1: Vector, v2: Vector) -> float:
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z


def cross_product(v1: Vector, v2: Vector):
    return Vector(v1.y * v2.z - v1.z * v2.y, v1.z * v2.x - v1.x * v2.z, v1.x * v2.y - v1.y * v2.x)


def point_to_vector(point: Point):
    return Vector(point.x, point.y, point.z)


def euclidian_distance(p1: Point, p2: Point):
    """:param n1, n2 Nodes"""
    return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2)
