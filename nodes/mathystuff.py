import numpy
import math
from srptools.position import Vector, Position

def rotation_matrix(vector, angle):
    """Matrix whose columns are (i,j,k) rotated by `angle` about `vector`."""
    ex = Vector((1,0,0)).rotated(angle, vector)
    ey = Vector((0,1,0)).rotated(angle, vector)
    ez = Vector((0,0,1)).rotated(angle, vector)
    return numpy.transpose(numpy.array((ex, ey, ez)))

def find_R(original, transformed):
    """If possible, finds orthogonal R: R*original[i]=transformed[i].

    The input should be two 2-tuples of Vectors, either one of which
    can be transformed into the other by multiplying its elements by a
    rotation matrix. If that's the case, or nearly the case, this
    function will return that matrix.
    """
    x, y = original
    xp, yp = transformed
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

def find_R_and_p(original, transformed):
    """If possible, finds (R, p): R*original[i]+p = transformed[i].

    The input should be two 3-tuples of Positions. Each trio of
    Positions should form the same shape -- that is, the two triangles
    should be congruent. If they aren't exactly congruent, this
    function will still function pretty well. It returns a rotation
    matrix R and a vector p such that
        R*original[i]+p = transformed[i].
    """
    x, y, z = original
    xp, yp, zp = transformed
    R = find_R((y-x, z-x), (yp-xp, zp-xp))
    Rx = R.dot(x).view(Position)
    return R, xp-Rx.view(Position)


if __name__ == '__main__':
    from srptools.floats import floateq

    def arrays_equal(A, B):
        if A.shape != B.shape:
            return False
        elif A.shape == ():
            return True

        return all(arrays_equal(A[i], B[i]) for i in range(A.shape[0]))

    v = Vector((1,0,0))
    R = rotation_matrix(v, numpy.pi)
    expected_R = numpy.array([[1, 0, 0],
                              [0, -1, 0],
                              [0, 0, -1]])
    assert arrays_equal(R, expected_R)

    v = Vector((1,1,1))
    R = rotation_matrix(v, 2*numpy.pi/3)
    expected_R = numpy.array([[0, 0, 1],
                              [1, 0, 0],
                              [0, 1, 0]])
    assert arrays_equal(R, expected_R)

    ex, ey, ez = Vector((1,0,0)), Vector((0,1,0)), Vector((0,0,1))
    R = find_R((ex, ey), (ey, ez))
    expected_R = numpy.array([[0, 0, 1],
                              [1, 0, 0],
                              [0, 1, 0]])
    assert arrays_equal(R, expected_R)

    expected_R = rotation_matrix(Vector((1,1,0)), numpy.pi)
    expected_p = ex+ey
    R, p = find_R_and_p((ex, ey, ez),
                        (expected_R.dot(ex).view(Position) + expected_p,
                         expected_R.dot(ey).view(Position) + expected_p,
                         expected_R.dot(ez).view(Position) + expected_p))
    assert arrays_equal(R, expected_R)
    assert arrays_equal(p, expected_p)
