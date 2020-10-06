from geom.basic import create_half_cylinder, point_to_vector, dot_product
from scipy.linalg import eig
import numpy as np
from geom.vector import Vector
from tecplot import writer, reader
from _grid.grid import Grid
from copy import deepcopy

def create_matrix_of_normals(node) -> np.array:
    N = node.faces[0].normal().coords_np_array()
    N = N.reshape((1, 3))
    for f in node.faces[1:]:
        normal = f.normal().coords_np_array()
        assert N.shape[1] == normal.shape[1], print(N.shape, normal.shape)
        N = np.vstack((N, normal))
    return N

# g = create_half_cylinder(5, 5, 'easy.dat', plot_pyplot=True)
g = Grid()
reader.read_tecplot(g, 'tu1_0060000000.dat')

N_ITER = 3
SHIFT = 1.0
st = 0.2
epsilon = 10e-3

for i in range(N_ITER):
    for n in g.Nodes:
        m = len(n.faces)
        p = point_to_vector(n.as_point())
        w = [f.area() for f in n.faces]
        N = create_matrix_of_normals(n)

        dv = Vector()
        weights = 0
        for f in n.faces:
            c = deepcopy(p)
            c.sub(point_to_vector(f.centroid()))

            # Find shifting
            normal = f.normal()
            normal.mul(SHIFT)
            c.sum(normal)

            weight = f.area()
            assert isinstance(c, Vector)
            assert isinstance(weight, float)
            c.mul(weight)
            dv.sum(c)
            weights += weight
        dv.dev(weights)

        assert N.shape == (m, 3)
        assert len(w) == m
        assert isinstance(dv, Vector)

        W = np.diag(w)
        NTW = np.dot(N.T, W)
        A = np.dot(NTW, N)

        assert W.shape == (m, m)
        assert NTW.shape == (3, m)
        assert A.shape == (3, 3)

        eigenValues, eigenVectors = eig(A)
        idx = eigenValues.argsort()[::-1]
        eigenValues = eigenValues[idx]
        eigenVectors = eigenVectors[:, idx]

        k = np.sum((eigenValues > epsilon * eigenValues[0]))
        e_ns = eigenVectors[:, k:]
        lambdas = eigenValues[k:]
        dv = dv.coords_np_array().reshape(3, 1)

        assert e_ns.shape == (3, 3 - k), 'Wrong eigenvectors shape'
        assert dv.shape == (3, 1), 'Wrong shape'

        if k < 3:
            a = np.dot(e_ns.T, dv)
            b = a * e_ns.T
            assert a.shape == (3 - k, 1)
            assert b.shape == (3 - k, 3)
            t = st * np.sum(b, axis=0, keepdims=True)
            assert t.shape == (1, 3), 'Wrong shift shape'
            n.move(Vector(float(t[0, 0]), float(t[0, 1]), float(t[0, 2])))

writer.write_tecplot(g, 'smoothing_res.dat')
