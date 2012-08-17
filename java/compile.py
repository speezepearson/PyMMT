import os
import subprocess

here = os.path.dirname(os.path.abspath(__file__))

def run():
    subprocess.call(['javac', '-d', 'bin',
                     '-classpath', os.pathsep.join(('lib', 'lib/*', 'src')),
                     'src/trackercontrolling/Main.java'],
                    cwd=here)
