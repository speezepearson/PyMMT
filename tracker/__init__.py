import time
import javapipe
import os
from .. import TRACKER_DUMMY

IFM = "IFM"
ADM = "ADM"
IFM_SET_BY_ADM = "IFM set by ADM"

CONNECT = "connect"
DISCONNECT = "disconnect"
INITIALIZE = "initialize"
ABORT = "abort"
MEASURE = "measure"
SET_MODE = "set mode"
SEARCH = "search"
MOVE = "move"
MOVE_ABSOLUTE = "move absolute"

here = os.path.dirname(os.path.abspath(__file__))
if TRACKER_DUMMY:
    import logging as _logging
    _logging.warning("Using dummy tracker library.")
    javapipe_dir = os.path.join(os.path.dirname(here), "dummies",
                                "trackerjava")
else:
    javapipe_dir = os.path.join(here, "javapipe")

class Tracker(object):
    def __init__(self):
        self.pipe = None

    def open(self):
        self.pipe = javapipe.JavaPipe(cwd=javapipe_dir,
                                      jclass='TrackerPipeMain')
    def close(self):
        self.pipe.close()
        
    def connect(self):
        return self.pipe.command_and_listen(CONNECT)
    def disconnect(self):
        return self.pipe.command_and_listen(DISCONNECT)
    def initialize(self):
        return self.pipe.command_and_listen(INITIALIZE)
    
    def move(self, radius, theta, phi):
        return self.pipe.command_and_listen(MOVE, radius, theta, phi)
    def move_absolute(self, radius, theta, phi):
        return self.pipe.command_and_listen(MOVE_ABSOLUTE, radius, theta, phi)
    def search(self, radius):
        return self.pipe.command_and_listen(SEARCH, radius)
        
    def measure(self):
        return self.pipe.command_and_listen(MEASURE)
        
    def abort(self):
        return self.pipe.command_and_listen(ABORT)

    def set_mode(self, mode):
        return self.pipe.command_and_listen(SET_MODE, mode)
