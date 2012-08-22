# This file declares the Tracker class, which controls a laser tracker
# and provides an interface to client code that lets it send commands
# and read measurements from the tracker.
#
# With the current implementation, the Tracker class passes the commands
# to a Java subprocess, since there's no Python wrapper for the tracker
# library and I haven't been able to get any call-Java-from-Python libraries
# working.

import os
import logging
from subprocesspipe import pipe_to_std_java_layout

# The command words we can write into the pipe -- \x00 and \x01 are the
#  special delimiters used by subprocesspipe, but any other characters
#  are fair game.
CONNECT = "connect"
DISCONNECT = "disconnect"
INITIALIZE = "initialize"
ABORT = "abort"
MEASURE = "measure"
SET_MODE = "set mode"
SEARCH = "search"
MOVE = "move"
MOVE_ABSOLUTE = "move absolute"

# The different modes we can set the tracker's measuring mode to:
IFM = "IFM"
ADM = "ADM"
IFM_SET_BY_ADM = "IFM set by ADM"

# Information about where we live and where the Java program we're
# running lives:
here = os.path.dirname(os.path.abspath(__file__))
java_dir = os.path.join(here, "java")
jclassname = '.'.join(('trackercontrolling', 'Main'))
jprocess_args = []

def set_dummy(dummy):
    """Configures the module to use/not use the dummy tracker program."""
    global jprocess_args
    import logging
    if dummy:
        logging.warning("Configuring PyMMT.tracker to use dummy tracker")
        jprocess_args = ["dummy"]
    else:
        logging.info("Configuring PyMMT.tracker to use real tracker")
        jprocess_args = []

class Tracker(object):
    """Controls a laser tracker."""
    def __init__(self):
        self.pipe = pipe_to_std_java_layout(java_dir, jclassname)
    def __enter__(self):
        # Just to make sure we open and close the tracker properly,
        # we make the Tracker a context manager so we can easily ensure
        # it gets closed.
        print "Opening tracker..."
        self.open()
        print "Opened!"
        return self
    def __exit__(self, type, value, traceback):
        print "Closing tracker..."
        self.close()
        print "Closed."

    def open(self):
        """Starts the subprocess that communicates with the tracker."""
        self.pipe.start(*jprocess_args)
    def close(self):
        """Stops the subprocess that communicates with the tracker."""
        self.pipe.stop()
        
    def connect(self):
        """Connects to the tracker."""
        return self.pipe.command_and_listen(CONNECT)
    def disconnect(self):
        """Disconnects from the tracker."""
        return self.pipe.command_and_listen(DISCONNECT)
    def initialize(self):
        """Initializes the tracker."""
        return self.pipe.command_and_listen(INITIALIZE)
    
    def move(self, radius, theta, phi):
        """Moves the tracker relative to its current position."""
        return self.pipe.command_and_listen(MOVE, radius, theta, phi)
    def move_absolute(self, radius, theta, phi):
        """Moves the tracker relative to its home position."""
        return self.pipe.command_and_listen(MOVE_ABSOLUTE, radius, theta, phi)
    def search(self, radius):
        """Tells the tracker to search for a target within the given radius."""
        return self.pipe.command_and_listen(SEARCH, radius)
        
    def measure(self):
        """Reads the tracker's current (r, theta, phi)."""
        response = self.pipe.command_and_listen(MEASURE)
        return [float(x) for x in response.split(" ")]
        
    def abort(self):
        """Aborts the tracker's current command."""
        return self.pipe.command_and_listen(ABORT)

    def set_mode(self, mode):
        """Sets the tracker's measurement mode."""
        return self.pipe.command_and_listen(SET_MODE, mode)
