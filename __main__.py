#!/usr/bin/python
#
# The main program file for the PyMMT project.
#
# When run, shows a window that gives you buttons and stuff that
# control the actuators and the laser tracker. Might also recompile
# the Java part of the program, depending on the settings defined in
# __init__.py.
#

import argparse
from Tkinter import Tk
import PyMMT

parser = argparse.ArgumentParser()
parser.add_argument('-j', '--recompile-java', action="store_true")
parser.add_argument('-t', '--real-tracker', action="store_true")
parser.add_argument('-a', '--real-actuators', action="store_true")

args = parser.parse_args()
if args.recompile_java:
    print "Recompiling Java code..."
    PyMMT.java.compile()
    print "Done."

_TrackerClass = (PyMMT.tracker.Tracker if args.real_tracker
                 else PyMMT.tracker.DummyTracker)
_BoardClass = (PyMMT.actuators.ActuatorBoard if args.real_actuators
               else PyMMT.actuators.DummyBoard)

#PyMMT.java.start_server(blocking=False)

tracker = _TrackerClass()
board = _BoardClass()
board.open()

root = Tk()
main_frame = PyMMT.gui.MainFrame(master=root, tracker=tracker, board=board)
main_frame.grid()

root.mainloop()
