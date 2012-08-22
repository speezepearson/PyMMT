from position import Vector
import math
from .mathystuff import find_R_and_p
from .io import read_data, write_data

def recompute(source_filename, dest_filename,
              namerthetaphis):
    training_points = {name: Vector((r*math.sin(theta)*math.cos(phi),
                                     r*math.sin(theta)*math.sin(phi),
                                     r*math.cos(theta)))
                       for name, r, theta, phi in namerthetaphis}
    original_data = read_data(source_filename)
    new_data = compute_new_data(original_data, training_points)
    write_data(new_data, dest_filename)

def compute_new_data(original_data, training_points):
    names = training_points.keys()
    for name in names:
        if name not in original_data:
            raise ValueError("{!r} is not a node name".format(name))
    x,y,z = [original_data[name] for name in names]
    xp,yp,zp = [training_points[name] for name in names]
    R, p = find_R_and_p(x, y, z, xp, yp, zp)
    return {name: R.dot(vector).view(Vector) + p
            for (name, vector) in original_data.items()}

