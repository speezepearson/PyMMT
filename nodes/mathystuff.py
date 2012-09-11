import numpy
import math
from srptools.position import Vector

def rotation_matrix(vector, angle):
    """Matrix whose columns are the standard basis rotated by `angle` about `vector`."""
    ex = Vector((1,0,0)).rotated(angle, vector)
    ey = Vector((0,1,0)).rotated(angle, vector)
    ez = Vector((0,0,1)).rotated(angle, vector)
    return numpy.transpose(numpy.array((ex, ey, ez)))

def find_R(x, y, xp, yp):
    """If possible, finds orthogonal R: R*x=xp, R*y=yp."""
    # The result R can be expressed as R2*R1, where
    # - R1 is any rotation matrix such that R1*x = xp, and
    # - R2 rotates things around xp such that R2*R1*y = yp.
    # Since R2 is a rotation about xp (which is R1*x),
    #  R*x = R2*R1*x = R1*x = xp
    # and we design R2 such that R*y = R2*R1*y = yp.

    # First, we find R1. Since x and xp are both perpendicular to (x
    # cross xp), we know we can generate a rotation matrix about (x
    # cross xp) that will rotate x to xp.
    omega = x.cross(xp).unit_vector()
    theta = math.acos(x.cos_with(xp))
    R1 = rotation_matrix(omega, theta)

    # Now express x and y in the rotated-by-R1 frame.
    x = R1.dot(x).view(Vector)
    y = R1.dot(y).view(Vector)

    # Now, we find R2.
    # We flatten y and yp into the plane perpendicular to xp, then
    # just find the angle we need to rotate y(flattened) by to get
    # yp(flattened).
    y = R1.dot(y).view(Vector)
    y_flattened = y.component_perpendicular_to(xp)
    yp_flattened = yp.component_perpendicular_to(xp)
    theta = math.acos(y_flattened.cos_with(yp_flattened))

    # (Since cosine is even, we still need to figure out whether we
    # rotate CW or CCW around xp now, and we do so by determining
    # whether
    #   (y_flattened, yp_flattened, xp)
    # is a left-handed or right-handed basis.)
    # (For a right-handed basis (x, y, z), ((x cross y) dot z) > 0.)
    righthanded = (y_flattened.cross(yp_flattened).dot(xp) > 0)
    if not righthanded:
        theta *= -1

    R2 = rotation_matrix(xp, theta)

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
