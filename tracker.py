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
from . import java

ADM = "ADM"
IFM = "IFM"
IFM_SET_BY_ADM = "IFM_SET_BY_ADM"
MODES = (ADM, IFM, IFM_SET_BY_ADM)

TRACKER_TYPE = "TrackerKeystone"
USER = "user"
PASSWORD = ""
IP_ADDRESS = "192.168.1.4"

def get_tracker_package():
    return java.get_gateway().jvm.smx.tracker

class Tracker(object):
    """Controls a laser tracker."""
    def __init__(self):
        self.tracker = get_tracker_package().Tracker(TRACKER_TYPE)
        self.tracker.setBlocking(True)
        
    def __del__(self):
        if hasattr(self, 'tracker') and self.tracker.connected():
            self.tracker.disconnect()

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
        """Tells the tracker to go home."""
        self.tracker.home()
        
    def measure(self, observation_rate=1, samples_per_observation=9,
                number_of_observations=1):
        """Reads the tracker's current (r, theta, phi)."""
        filter = get_tracker_package().AverageFilter()
        start_trigger = get_tracker_package().NullStartTrigger()
        continue_trigger = get_tracker_package().IntervalTrigger(observation_rate)
        configuration = get_tracker_package().MeasureCfg(samples_per_observation,
                                                         filter, start_trigger,
                                                         continue_trigger)
        self.tracker.startMeasurePoint(configuration)
        result = self.tracker.readMeasurePointData(number_of_observations)
        self.tracker.stopMeasurePoint()
        return result
        
    def abort(self):
        """Aborts the tracker's current command."""
        self.tracker.abort()

    def set_mode(self, mode_string):
        """Sets the tracker's measurement mode."""
        if mode_string not in MODES:
            raise ValueError("mode string must be in {!r}".format(MODES))

        mode = (get_tracker_package().ADMOnly() if mode_string == ADM
                else get_tracker_package().InterferometerOnly() if mode_string == IFM
                else get_tracker_package().InterferometerSetByADM())
        self.tracker.setMode(mode)


class _DummyMeasurePointData(object):
    DATA_ACCURATE = DATA_INACCURATE = DATA_ERROR = 0
    azimuth = distance = status = time = zenith = (lambda: 0)
_dummy_data = _DummyMeasurePointData()
class DummyTracker(object):
    def connect(self):
        pass
    def disconnect(self):
        pass
    def initialize(self):
        pass
    def abort(self):
        pass
    def home(self):
        pass
    def move(self, radius, theta, phi):
        pass
    def move_absolute(self, radius, theta, phi):
        pass
    def search(self, radius):
        pass
    def set_mode(self, mode_string):
        pass
    def measure(self, observation_rate=1, samples_per_observation=9,
                number_of_observations=1):
        return [_dummy_data] * number_of_observations
