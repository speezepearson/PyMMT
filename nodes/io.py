import csv
from srptools.position import Position

def load(path):
    with open(path) as source_file:
        reader = csv.reader(source_file)
        return {name: Position((float(r), float(theta), float(phi)),
                               polar=True)
                for (name, r, theta, phi) in reader}

def save(data, path):
    with open(path, 'w') as dest_file:
        writer = csv.writer(dest_file)
        for name, position in data.items():
            writer.writerow((name, position.r, position.theta, position.phi))


