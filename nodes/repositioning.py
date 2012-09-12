import math
from srptools.position import Vector
from .mathystuff import find_R_and_p
from . import io

def recompute(original_data, training_data):
    if len(training_data) != 3:
        raise ValueError("Exactly 3 training points are required")

    names = training_data.keys()
    for name in names:
        if name not in original_data:
            raise ValueError("{!r} is not a node name".format(name))
    x,y,z = [original_data[name] for name in names]
    xp,yp,zp = [training_data[name] for name in names]
    R, p = find_R_and_p(x, y, z, xp, yp, zp)

    return {name: R.dot(vector).view(Vector) + p
            for (name, vector) in original_data.items()}

