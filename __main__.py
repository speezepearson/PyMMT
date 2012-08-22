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
from PyMMT.gui import MainFrame
from PyMMT.actuators import ActuatorBoard, set_dummy as set_dummy_actuators
from PyMMT.tracker import Tracker, set_dummy as set_dummy_tracker
from PyMMT.java import compile

parser = argparse.ArgumentParser()
parser.add_argument('-j', '--recompile-java', action="store_true")
parser.add_argument('-t', '--real-tracker', action="store_true")
parser.add_argument('-a', '--real-actuators', action="store_true")

args = parser.parse_args()
set_dummy_actuators(not args.real_actuators)
set_dummy_tracker(not args.real_tracker)
if args.recompile_java:
    print "Recompiling Java code..."
    compile.run()
    print "Done."

with Tracker() as tracker,  ActuatorBoard() as board:
    root = Tk()
    main_frame = MainFrame(master=root, tracker=tracker, board=board)
    main_frame.grid()

    root.mainloop()
