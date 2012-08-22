from position import Vector
import os
import csv

here = os.path.dirname(os.path.abspath(__file__))

def read_data(source_filename):
    source_file = open(os.path.join(here, source_filename))
    reader = csv.reader(source_file)
    return {name: Vector((float(x), float(y), float(z)))
            for (name, x, y, z) in reader}

def write_data(data, dest_filename):
    dest_file = open(os.path.join(here, dest_filename), 'w')
    writer = csv.writer(dest_file)
    for (name, (x,y,z)) in data.items():
        writer.writerow((name, x, y, z))


