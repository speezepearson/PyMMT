import csv
from srptools.position import Vector

def load(path):
    with open(path) as source_file:
        reader = csv.reader(source_file)
        return {name: Vector((float(r), float(theta), float(phi)),
                             polar=True)
                for (name, r, theta, phi) in reader}

def save(data, path):
    with open(path, 'w') as dest_file:
        writer = csv.writer(dest_file)
        for name, vector in data.items():
            writer.writerow((name, vector.r, vector.theta, vector.phi))


