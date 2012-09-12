import logging
import matplotlib.pyplot
from srptools.position import Vector

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
            logging.warning("No accurate data taken.")

        base_time = data[0].time
        base_vector = data[0].vector
        x = [point.time - base_time for point in data]
        y = [(base_vector-point.vector).magnitude() for point in data]
        matplotlib.pyplot.plot(x, y, marker=".")
        matplotlib.pyplot.show()
