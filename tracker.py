import time
import javapipe
import os
from . import TRACKER_DUMMY, RECOMPILE_JAVA

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
piping_dir = os.path.join(java_dir, "piping")
executor_dir = os.path.join(java_dir, ("DummyExecutor" if TRACKER_DUMMY
                                       else "RealExecutor"))
jclasses = [os.path.join(java_dir, 'TrackerController'),
            os.path.join(piping_dir, 'PipeInterface'),
            os.path.join(piping_dir, 'CommandExecutor'),
            os.path.join(executor_dir, 'TrackerExecutor')]
classpath = os.pathsep.join((java_dir, piping_dir, executor_dir))

if TRACKER_DUMMY:
    import logging as _logging
    _logging.warning("tracker.py is using dummy tracker library.")

if RECOMPILE_JAVA:
    print "Compiling java..."
    javapipe.compile(source_files=[jclass+".java" for jclass in jclasses],
                     options=['-classpath', classpath])
    print "Compiled."

class Tracker(object):
    def __init__(self):
        self.pipe = javapipe.JavaPipe(cwd=java_dir,
                                      jclass='TrackerController',
                                      classpath=classpath)

    def open(self):
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
