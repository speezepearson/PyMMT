import csv

def load(path):
    with open(path) as source_file:
        reader = csv.reader(source_file)
        return {name: (float(r), float(theta), float(phi))
                for (name, r, theta, phi) in reader}

def save(data, path):
    with open(path, 'w') as dest_file:
        writer = csv.writer(dest_file)
        for name, (r,theta,phi) in data.items():
            writer.writerow((name, r, theta, phi))


