# This file defines the RepositioningFrame class, which helps the user
# handle the tracker being repositioned.

import os
import logging

from Tkinter import LabelFrame, Entry, Label, Button
from srptools.tkinter import FileSelectionFrame

from .. import nodes

logger = logging.getLogger(__name__)

here = os.path.dirname(os.path.abspath(__file__))
nodes_dir = os.path.join(os.path.dirname(here), 'nodes')

def caller(callback, *args, **kwargs):
    def result():
        return callback(*args, **kwargs)
    return result
class RepositioningFrame(LabelFrame):
    """Helps the user deal with the tracker being repositioned.
    
    Asks for a source file (CSV file containing name/x/y/z for many nodes)
    and a destination file (which will be the same). Also asks for the names
    of three points, whose positions are determined by querying a Tracker.
    Plugs the names/(original data)/positions into nodes.recomputing,
    which will determine the new position of the tracker and adjust the
    original file's x/y/z triplets accordingly, dumping the new values
    into the destination file.
    """
    def __init__(self, master, tracker, text="Repositioning", **kwargs):
        LabelFrame.__init__(self, master, text=text, **kwargs)
        self.tracker = tracker

        self.source_selector = FileSelectionFrame(self, initial_dir=nodes_dir,
                                                  ask_mode="open",
                                                  text="Source")
        self.source_selector.grid(row=0, column=0)
        self.dest_selector = FileSelectionFrame(self, initial_dir=nodes_dir,
                                                ask_mode="save", text="Dest")
        self.dest_selector.grid(row=0, column=1)

        # The names and positions we gather:
        self.name_fields = []
        self.posn_labels = []
        self.training_info = []

        for i in range(3):
            # Why three? Well, we need three training points to figure
            # out where all the other points are. Proof: take your
            # fist and move it around (it's a rigid structure, like
            # the arrangement of retroreflectors), and think about how
            # many points (e.g. knuckles) you'd need to know the
            # positions of to figure out the positions of all your
            # other knuckles.  (It's three. If you disagree, please
            # think about it more until you agree, because I am
            # absolutely confident.)
            f = LabelFrame(self, text="(Name/position) ({})".format(i))
            self.name_fields.append(Entry(f))
            self.name_fields[-1].grid(row=0, column=0)
            self.posn_labels.append(Label(f, text="<None>"))
            self.posn_labels[-1].grid(row=0, column=1)
            b = Button(f, command=caller(self.set_position, i), text="Set")
            b.grid(row=0, column=2)
            f.grid(row=1+i, column=0, columnspan=2)
            self.training_info.append(None)

        Button(self, text="Compute/Save", command=self.save).grid(row=4,
                                                                  column=0)

    def set_position(self, i):
        """Stores the Tracker's current (r,theta,phi)."""
        data = self.tracker.measure()[0]
        if data.status() != data.DATA_ACCURATE:
            logger.error("Data taken were inaccurate.")
            return
        
        self.training_info[i] = (data.distance(), data.zenith(),
                                 data.azimuth())
        self.posn_labels[i].configure(text=str(self.training_info[i]))

    def save(self):
        """Recomputes the x/y/z CSV file based on our (name,r,theta,phi)s."""
        if None in self.training_info:
            logger.error("Can't recompute -- need 3 training points")
            return

        source_path = self.source_selector.path.get()
        dest_path = self.dest_selector.path.get()
        if not (source_path and dest_path):
            logger.error("Can't recompute -- need source and dest files")
            return

        try:
            old_data = nodes.load(source_path)
        except IOError:
            logger.error("{!r} no longer exists".format(source_path))
            return

        training_data = {self.name_fields[i].get(): self.training_info[i]
                         for i in range(3)}

        try:
            new_data = nodes.recompute(old_data, training_data)
        except ValueError as e:
            logger.error("Error recomputing: {}".format(e.message))
            return

        nodes.save(new_data, dest_path)
        logger.info("Wrote recomputed data to {!r}".format(dest_path))
