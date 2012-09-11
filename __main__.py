#!/usr/bin/python
#
# The main program file for the PyMMT project.
#
# When run, shows a window that gives you buttons and stuff that
# control the actuators and the laser tracker.

import argparse
from Tkinter import Tk
import PyMMT
import logging

logger = logging.getLogger("PyMMT")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

# We would like command-line flags allowing the user to use dummy
# versions of the other hardware components, in case they aren't
# hooked up.
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--dummy-tracker', action="store_true",
                    help="use dummy tracker controller")
parser.add_argument('-a', '--dummy-actuators', action="store_true",
                    help="use dummy actuator controller")

args = parser.parse_args()
TrackerClass = (PyMMT.tracker.DummyTracker if args.dummy_tracker
                else PyMMT.tracker.Tracker)
BoardClass = (PyMMT.actuators.DummyBoard if args.dummy_actuators
              else PyMMT.actuators.ActuatorBoard)

PyMMT.java.start_server()
with TrackerClass() as tracker, BoardClass() as board:
    root = Tk()
    main_frame = PyMMT.gui.MainFrame(master=root, tracker=tracker, board=board)
    main_frame.grid()

    root.mainloop()
