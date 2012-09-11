# This submodule defines all the user-interface-related stuff that goes on.
# Mostly it's just laying out Tkinter frames and passing commands on
# to the workhorses (e.g. Tracker, ActuatorBoard) in other submodules.

from .actuatorframe import ActuatorFrame
from .trackerframe import TrackerFrame
from .mainframe import MainFrame
from .repositioningframe import RepositioningFrame
