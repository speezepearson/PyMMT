import logging
import matplotlib.pyplot

from Tkinter import Frame, Button
from .measureframe import MeasureFrame

class PlottingFrame(Frame):
    def __init__(self, master, tracker, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.tracker = tracker

        self.measure_frame = MeasureFrame(self, tracker)
        self.measure_frame.grid()
        self.plot_button = Button(self, text="Plot", command=self.plot)
        self.plot_button.grid()

    def plot(self):
        data = self.measure_frame.measure(only_accurate=True)
        if not data:
            logger.warning("No accurate data taken.")

        base_time = data[0].time
        base_posn = data[0].position
        x = [point.time - base_time for point in data]
        y = [(base_posn-point.position).magnitude() for point in data]
        matplotlib.pyplot.plot(x, y, marker=".")
        matplotlib.pyplot.show()
