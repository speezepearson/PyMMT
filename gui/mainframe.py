# This file defines the MainFrame class, which just contains an
# ActuatorFrame and a TrackerFrame. Pretty boring!

from Tkinter import Frame, Button, LabelFrame, Toplevel

from .trackerframe import TrackerFrame
from .joystickframe import JoystickFrame
from .repositioningframe import RepositioningFrame
from .actuatorframe import ActuatorFrame
from .measureframe import MeasureFrame
from .plottingframe import PlottingFrame

class MainFrame(Frame):
    def __init__(self, tracker, board, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.tracker = tracker
        self.board = board

        tracker_subframe = LabelFrame(self, text="Tracker stuff")
        self.tracker_button = Button(tracker_subframe, text="Tracker",
                                     command=self.open_tracker_frame)
        self.tracker_button.grid()
        self.joystick_button = Button(tracker_subframe, text="Joystick",
                                      command=self.open_joystick_frame)
        self.joystick_button.grid()
        self.reposn_button = Button(tracker_subframe, text="Repositioning",
                                    command=self.open_repositioning_frame)
        self.reposn_button.grid()
        self.measure_button = Button(tracker_subframe, text="Measure",
                                     command=self.open_measure_frame)
        self.measure_button.grid()
        self.plotting_button = Button(tracker_subframe, text="Plotting",
                                      command=self.open_plotting_frame)
        self.plotting_button.grid()
        tracker_subframe.grid()

        self.actuator_button = Button(self, text="Actuators",
                                      command=self.open_actuator_frame)
        self.actuator_button.grid()

    def open_tracker_frame(self):
        window = Toplevel()
        window.title = "Tracker"
        TrackerFrame(window, self.tracker).grid()
    def open_joystick_frame(self):
        window = Toplevel()
        window.title = "Joystick"
        JoystickFrame(window, self.tracker).grid()
    def open_repositioning_frame(self):
        window = Toplevel()
        window.title = "Repositioning"
        RepositioningFrame(window, self.tracker).grid()
    def open_measure_frame(self):
        window = Toplevel()
        window.title = "Measurements"
        MeasureFrame(window, self.tracker).grid()
    def open_plotting_frame(self):
        window = Toplevel()
        window.title = "Plotting"
        PlottingFrame(window, self.tracker).grid()
    def open_actuator_frame(self):
        window = Toplevel()
        window.title = "Actuators"
        ActuatorFrame(window, self.board).grid()

