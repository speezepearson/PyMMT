from Tkinter import Tk
from .gui.actuatorframe import ActuatorFrame
from .gui.trackerframe import TrackerFrame

root = Tk()

tracker_frame = TrackerFrame(root)
actuator_frame = ActuatorFrame(root)

tracker_frame.grid(row=0, column=0)
actuator_frame.grid(row=0, column=1)

root.mainloop()
