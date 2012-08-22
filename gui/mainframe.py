# This file defines the MainFrame class, which just contains an
# ActuatorFrame and a TrackerFrame. Pretty boring!

from .trackerframe import TrackerFrame
from .actuatorframe import ActuatorFrame
from Tkinter import Frame

class MainFrame(Frame):
    def __init__(self, tracker, board, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.tracker_frame = TrackerFrame(self, tracker)
        self.tracker_frame.grid(row=0, column=0, sticky="nsew")
        self.actuator_frame = ActuatorFrame(self, board)
        self.actuator_frame.grid(row=0, column=1, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
