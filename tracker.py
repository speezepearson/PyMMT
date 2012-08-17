import time
import os
import logging
from . import TRACKER_DUMMY
from subprocesspipe import pipe_to_std_java_layout

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
java_dir = os.path.join(here, "java")
jclassname = os.path.join('trackercontrolling', 'Main')

class Tracker(object):
    def __init__(self):
        self.pipe = pipe_to_std_java_layout(java_dir, jclassname)

    def open(self):
        if TRACKER_DUMMY:
            logging.warning("opening a dummy tracker.")
            self.pipe.start('dummy')
        else:
            self.pipe.start()
    def close(self):
        self.pipe.stop()
        
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
