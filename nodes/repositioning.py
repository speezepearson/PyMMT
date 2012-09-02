import math
from srptools.position import Vector
from .mathystuff import find_R_and_p
from . import io

def rtps2vectors(rtps):
    return {key: Vector((r*math.sin(theta)*math.cos(phi),
                         r*math.sin(theta)*math.sin(phi),
                         r*math.cos(theta)))
            for key, (r, theta, phi) in rtps.items()}
def vectors2rtps(vectors):
    return {key: (math.sqrt(v.x**2+v.y**2+v.z**2),
                  math.atan2(math.sqrt(v.x**2+v.y**2), v.z),
                  math.atan2(v.y, v.x))
            for key, v in vectors.items()}


def recompute(original_rtps, training_rtps):
    if len(training_rtps) != 3:
        raise ValueError("Exactly 3 training points are required")
    original_data = rtps2vectors(original_rtps)
    training_data = rtps2vectors(training_rtps)

    names = training_data.keys()
    for name in names:
        if name not in original_data:
            raise ValueError("{!r} is not a node name".format(name))
    x,y,z = [original_data[name] for name in names]
    xp,yp,zp = [training_data[name] for name in names]
    R, p = find_R_and_p(x, y, z, xp, yp, zp)

    new_data = {name: R.dot(vector).view(Vector) + p
                for (name, vector) in original_data.items()}
    return vectors2rtps(new_data)

