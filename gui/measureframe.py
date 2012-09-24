import csv
import logging
from srptools.guitools import bg_caller

from Tkinter import LabelFrame, Button, Entry, Checkbutton, BooleanVar
from srptools.tkinter import FileSelectionFrame, NamedEntryFrame

logger = logging.getLogger(__name__)

OBS_INTERVAL = "Observation interval"
NUM_SAMPLES = "Samples per observation"
NUM_OBSS = "Number of observations"

class MeasureFrame(LabelFrame):
    def __init__(self, master, tracker, text="Measuring", *args, **kwargs):
        LabelFrame.__init__(self, master, text=text, *args, **kwargs)
        self.tracker = tracker

        self.config_frame = NamedEntryFrame(self, (OBS_INTERVAL,
                                                   NUM_SAMPLES,
                                                   NUM_OBSS),
                                            parsers={OBS_INTERVAL: float,
                                                     NUM_SAMPLES: int,
                                                     NUM_OBSS: int})
        self.config_frame.grid()

        self.save_frame = LabelFrame(self, text="Saving")
        self.dest_selector = FileSelectionFrame(self.save_frame,
                                                ask_mode="save")
        self.dest_selector.grid(row=0, column=0, columnspan=2)
        self.save_button = Button(self.save_frame, text="Save",
                                  command=bg_caller(self.save))
        self.save_button.grid(row=1, column=0)
        self.appending_var = BooleanVar()
        self.append_checkbutton = Checkbutton(self.save_frame, text="Append",
                                              variable=self.appending_var)
        self.append_checkbutton.grid(row=1, column=1)
        self.save_frame.grid()

    def measure(self, only_accurate=True):
        try:
            interval = self.config_frame.get(OBS_INTERVAL)
            samples = self.config_frame.get(NUM_SAMPLES)
            num_obss = self.config_frame.get(NUM_OBSS)
        except ValueError:
            logger.error("Could not parse input fields.")
        data = self.tracker.measure(observation_interval=interval,
                                    samples_per_observation=samples,
                                    number_of_observations=num_obss)
        if only_accurate:
            accurate_data = [point for point in data
                             if point.status == point.DATA_ACCURATE]
            num_invalid = len(data) - len(accurate_data)
            if num_invalid > 0:
                logger.warning("Hiding {} inaccurate data points."
                               .format(num_invalid))
            return accurate_data
        else:
            return data

    def save(self, only_accurate=True):
        dest = self.dest_selector.path_var.get()
        if not dest:
            logger.error("Must select a destination file.")
            return

        data = self.measure(only_accurate=only_accurate)
        w = csv.writer(open(dest, 'a' if self.appending_var.get() else 'w'))
        for point in data:
            w.writerow((point.time, point.position.r,
                        point.position.theta, point.position.phi))

        logger.info("Saved measurements into {!r}".format(dest))
