import javapipe
import os

here = os.path.dirname(os.path.abspath(__file__))
jpipe_dir = os.path.join(os.path.dirname(here), "jpipe")

class Tracker(object):
    def __init__(self):
        self.pipe = None

    def open(self):
        self.pipe = javapipe.JavaPipe(cwd=jpipe_dir,
                                      jclass='TrackerPipeMain')
    def close(self):
        self.pipe.close()

    def send_command(self, *strings):
        self.pipe.writeline("\t".join(strings))
        
    def connect(self):
        self.send_command("connect")
        print self.pipe.read_response()
    def disconnect(self):
        self.send_command("disconnect")
        print self.pipe.read_response()
    def initialize(self):
        self.send_command("initialize")
        print self.pipe.read_response()
    
    def move(self, radius, theta, phi):
        self.send_command("move", "%.8f"%radius, "%.8f"%theta, "%.8f"%phi)
        print self.pipe.read_response()
    def move_absolute(self, radius, theta, phi):
        self.send_command("move_absolute", "%.8f"%radius, "%.8f"%theta, "%.8f"%phi)
        print self.pipe.read_response()
    def search(self, radius):
        self.send_command("search", "%.8f"%radius)
        print self.pipe.read_response()
    
    def measure(self):
        self.send_command("measure")
        print self.pipe.read_response()
