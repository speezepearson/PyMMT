import numpy
import math
from srptools.position import Vector

def rotation_matrix(vector, angle):
    ex = Vector((1,0,0)).rotated(angle, vector)
    ey = Vector((0,1,0)).rotated(angle, vector)
    ez = Vector((0,0,1)).rotated(angle, vector)
    return numpy.transpose(numpy.array((ex, ey, ez)))

def find_R(x, y, xp, yp):
    """If possible, finds orthogonal R: R*x=xp, R*y=yp."""
    w = x.cross(xp).unit_vector()
    theta = math.acos(x.cos_with(xp))
    R1 = rotation_matrix(w, theta)

    y = R1.dot(y).view(Vector)
    w = xp
    flat = y.component_perpendicular_to(w)
    flatp = yp.component_perpendicular_to(w)
    righthanded = (w.cross(flat).dot(flatp) > 0)
    theta = math.acos(flat.cos_with(flatp))
    if not righthanded:
        theta *= -1
    R2 = rotation_matrix(w, theta)

    return R2.dot(R1)

def find_R_and_p(x, y, z, xp, yp, zp):
    """If possible, finds vector p and orthogonal R: R*x+p = xp, ..."""
    R = find_R(x-y, y-z, xp-yp, yp-zp)
    Rx = R.dot(x).view(Vector)
    return R, xp-Rx


if __name__ == '__main__':
    def printm(A):
        A = A.copy()
        for i in range(A.shape[0]):
            for j in range(A.shape[1]):
                if abs(A[i,j]) < 10**-6:
                    A[i,j] = 0
        print A
    v = Vector((1,0,0))
    print "v =", v
    print "rotation_matrix(v, pi):"
    printm(rotation_matrix(v, numpy.pi))

    v = Vector((1,1,1))
    print "v =", v
    print "rotation_matrix(v, 2*pi/3):"
    printm(rotation_matrix(v, 2*numpy.pi/3))

    ex, ey, ez = Vector((1,0,0)), Vector((0,1,0)), Vector((0,0,1))
    print "find_R(ex, ey, ey, ez):"
    printm(find_R(ex, ey, ey, ez))

    R = rotation_matrix(Vector((1,1,0)), numpy.pi)
    p = ex+ey
    print "True R:"
    printm(R)
    print "True p:", p
    calcR, calcp = find_R_and_p(ex, ey, ez,
                                R.dot(ex).view(Vector) + p,
                                R.dot(ey).view(Vector) + p,
                                R.dot(ez).view(Vector) + p)
    print "Calculated R:"
    printm(calcR)
    print "Calculated p:", calcp
