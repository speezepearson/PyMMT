from . import PAD
from .trackerframe import TrackerFrame
from .actuatorframe import ActuatorFrame
from Tkinter import Frame, LEFT, RIGHT

class MainFrame(Frame):
    def __init__(self, tracker, controller, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.tracker_frame = TrackerFrame(self, tracker,
                                          padx=PAD, pady=PAD)
        self.tracker_frame.grid(row=0, column=0, sticky="nsew",
                                padx=PAD, pady=PAD)
        self.actuator_frame = ActuatorFrame(self, controller,
                                            padx=PAD, pady=PAD)
        self.actuator_frame.grid(row=0, column=1, sticky="nsew",
                                 padx=PAD, pady=PAD)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
