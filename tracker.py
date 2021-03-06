# This file declares the Tracker class, which controls a laser
# tracker. It provides client code with an interface that lets it send
# commands to the tracker and read measurements from it.
#
# With the current implementation, the Tracker class is mostly just a
# wrapper around a Java object, interfacing with the Java world using
# Py4J. (The Java part is likely here to stay -- there's no native
# Python library for controlling the tracker.)

import os
import random
from srptools.position import Position
from . import java

# Information about the laser tracker hardware:
TRACKER_TYPE = "TrackerKeystone"
IP_ADDRESS = "192.168.1.4"

# Login information so we can connect to the tracker:
USER = "user"
PASSWORD = ""

# The various measurement modes we can set the tracker to:
ADM = "ADM"
IFM = "IFM"
IFM_SET_BY_ADM = "IFM_SET_BY_ADM"
MODE_NAMES = (ADM, IFM, IFM_SET_BY_ADM)

def get_tracker_package():
    """Convenience function to get the JVM's smx.tracker package."""
    return java.get_gateway().jvm.smx.tracker

def name_to_mode(name):
    """Converts the name of a measurement mode to a MeasureMode Java object."""
    if name not in MODE_NAMES:
        raise ValueError("{!r} is not a mode name".format(name))

    tp = get_tracker_package()
    return (tp.ADMOnly() if name == ADM
            else tp.InterferometerOnly if name == IFM
            else tp.InterferometerSetByADM)

class Tracker(object):
    """Controls a laser tracker."""
    def __init__(self):
        self.tracker = get_tracker_package().Tracker(TRACKER_TYPE)

        # The tracker can be run in nonblocking mode, but that would
        # get us into a nightmare of threading. So we use blocking
        # mode instead.
        self.tracker.setBlocking(True)

    # We provide a context manager so that client code can make sure
    # we connect and disconnect properly.
    def __enter__(self):
        self.connect()
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        try:
            connected = self.tracker.connected()
        except py4j.protocol.Py4JJavaError:
            pass
        else:
            if connected:
                self.disconnect()

    def connect(self):
        """Connects to the tracker."""
        self.tracker.connect(IP_ADDRESS, USER, PASSWORD)
    def disconnect(self):
        """Disconnects from the tracker."""
        self.tracker.disconnect()
    def initialize(self):
        """Initializes the tracker."""
        self.tracker.initialize()

    def move(self, radius, theta, phi):
        """Moves the tracker relative to its current position."""
        self.tracker.move(phi, theta, radius, True)
    def move_absolute(self, radius, theta, phi):
        """Moves the tracker relative to its home position."""
        self.tracker.move(phi, theta, radius, False)
    def search(self, radius):
        """Tells the tracker to search for a target within the given radius."""
        self.tracker.search(radius)
    def home(self):
        """Moves the tracker to its home position."""
        self.tracker.home(False)
        
    def measure(self, observation_interval=1, samples_per_observation=9,
                number_of_observations=1):
        """Takes a series of data points from the tracker."""
        # The tracker takes a series of "observations", each
        # observation being a combination of several samples. A Filter
        # describes how the samples are combined into an observation,
        # and a Trigger defines what causes an observation to be
        # taken. Our Filter and Triggers say, "start immediately, take
        # a bunch of samples every T seconds, and average them
        # together for an observation".
        tp = get_tracker_package()
        filter = tp.AverageFilter()
        start_trigger = tp.NullStartTrigger()
        continue_trigger = tp.IntervalTrigger(observation_interval)
        configuration = tp.MeasureCfg(samples_per_observation, filter,
                                      start_trigger, continue_trigger)
        self.tracker.startMeasurePoint(configuration)
        points = self.tracker.readMeasurePointData(number_of_observations)
        self.tracker.stopMeasurePoint()
        return [DataPoint(point) for point in points]

    def is_looking_at_target(self):
        """Returns whether the tracker is tracking a retroreflector."""
        return self.tracker.targetPresent()
        
    def abort(self):
        """Aborts the tracker's current action."""
        self.tracker.abort()

    def set_mode(self, mode_name):
        """Sets the tracker's measurement mode."""
        mode = name_to_mode(mode_name)
        self.tracker.changeDistanceMeasureMode(mode)

class DataPoint(object):
    DATA_ACCURATE = "data_accurate"
    DATA_INACCURATE = "data_inaccurate"
    DATA_ERROR = "data_error"
    status_names = {0: DATA_ACCURATE,
                    1: DATA_INACCURATE,
                    2: DATA_ERROR}
    def __init__(self, jpoint):
        self.position = Position((jpoint.distance(), jpoint.zenith(),
                                  jpoint.azimuth()), polar=True)
        self.time = jpoint.time()
        self.status = self.status_names[jpoint.status()]

class _DummyMeasurePointData(object):
    status = (lambda self: 0)
    azimuth = distance = time = zenith = (lambda self: random.random())
_dummy_point = _DummyMeasurePointData()
class DummyTracker(object):
    def __init__(self):
        pass
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        pass
    connect = disconnect = initialize = abort = home = (lambda self: None)
    search = set_mode = (lambda self, x: None)
    move = move_absolute = (lambda self, x, y, z: None)

    def measure(self, observation_interval=1, samples_per_observation=9,
                number_of_observations=1):
        return [DataPoint(_dummy_point)
                for i in range(number_of_observations)]
