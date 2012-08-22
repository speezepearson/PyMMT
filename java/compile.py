import os
import subprocess

here = os.path.dirname(os.path.abspath(__file__))

def run():
    if not os.path.exists(os.path.join(here, "bin")):
        os.mkdir(os.path.join(here, "bin"))
    subprocess.call(['javac', '-d', 'bin',
                     '-classpath', os.pathsep.join(('lib',
                                                    os.path.join('lib', '*'),
                                                    'src')),
                     os.path.join('src', 'trackercontrolling', 'Main.java')],
                    cwd=here)
