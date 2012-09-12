import csv
import logging

from Tkinter import LabelFrame, Button, Entry, Checkbutton, BooleanVar
from srptools.tkinter import FileSelectionFrame, NamedEntryFrame

logger = logging.getLogger(__name__)

OBS_RATE = "Observation rate"
NUM_SAMPLES = "Samples per observation"
NUM_OBSS = "Number of observations"

class MeasureFrame(LabelFrame):
    def __init__(self, master, tracker, text="Measuring", *args, **kwargs):
        LabelFrame.__init__(self, master, text=text, *args, **kwargs)
        self.tracker = tracker

        self.dest_selector = FileSelectionFrame(self, ask_mode="save")
        self.dest_selector.grid(row=0, column=0, columnspan=2)

        self.config_frame = NamedEntryFrame(self, (OBS_RATE,
                                                   NUM_SAMPLES,
                                                   NUM_OBSS),
                                            parsers={OBS_RATE: float,
                                                     NUM_SAMPLES: int,
                                                     NUM_OBSS: int})
        self.config_frame.grid(row=1, column=0, columnspan=2)

        self.dump_button = Button(self, text="Dump",
                                     command=self.dump)
        self.dump_button.grid(row=2, column=0)

        self.appending = BooleanVar()
        self.append_checkbutton = Checkbutton(self, text="Append",
                                              variable=self.appending)
        self.append_checkbutton.grid(row=2, column=1)

    def measure(self):
        rate = self.config_frame.get(OBS_RATE)
        samples = self.config_frame.get(NUM_SAMPLES)
        num_obss = self.config_frame.get(NUM_OBSS)
        return self.tracker.measure(observation_rate=rate,
                                    samples_per_observation=samples,
                                    number_of_observations=num_obss)

    def dump(self):
        dest = self.dest_selector.path.get()
        if not dest:
            logging.error("Must select a destination file.")
            return

        data = self.measure()
        invalid_points = 0
        w = csv.writer(open(dest, 'a' if self.appending.get() else 'w'))
        for point in data:
            if point.status() == point.DATA_ACCURATE:
                w.writerow((point.time(), point.distance(),
                            point.zenith(), point.azimuth()))
            else:
                invalid_points += 1

        if invalid_points > 0:
            logger.warning("Ignored {} inaccurate data points (out of {})."
                           .format(invalid_points, len(data)))
        logger.info("Dumped measurements into {!r}".format(dest))
