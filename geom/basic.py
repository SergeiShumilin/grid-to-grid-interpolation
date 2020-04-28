"""This module implements basic geometrical routines."""
import numpy as np


def euclidian_distance(n1, n2):
    return np.sqrt((n1.x - n2.x) ** 2 + (n1.y - n2.y) ** 2 + (n1.z - n2.z) ** 2)