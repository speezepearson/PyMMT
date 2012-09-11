# This file defines the RepositioningFrame class, which helps the user
# handle the tracker being repositioned.

from Tkinter import LabelFrame, Entry, Label, Button
from tkMessageBox import showwarning
import tkFileDialog
from .. import nodes
import os

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

        self.source_path = None
        self.dest_path = None

        f = LabelFrame(self, text="Source file")
        self.source_label = Label(f)
        self.source_label.grid()
        self.source_button = Button(f, text="Set", command=self.set_source)
        self.source_button.grid()
        f.grid(row=0, column=0)
        f = LabelFrame(self, text="Destination file")
        self.dest_label = Label(f)
        self.dest_label.grid()
        self.dest_button = Button(f, text="Set", command=self.set_dest)
        self.dest_button.grid()
        f.grid(row=0, column=1)


        # The names and positions we gather:
        self.name_fields = []
        self.posn_labels = []
        self.training_info = []

        for i in range(3):
            # We need three training points. Proof: just take your fist
            # and move it around (it's a rigid structure, like the
            # arrangement of retroreflectors), and think about how many
            # points (e.g. knuckles) you'd need to know the positions of
            # to figure out the positions of all your other knuckles.
            # (It's three. If you disagree, please think about it more
            #  until you agree, because I am absolutely confident.)
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

    def set_source(self):
        self.source_path = tkFileDialog.askopenfilename(initialdir=nodes_dir)
        self.source_label.configure(text=self.source_path)
    def set_dest(self):
        self.dest_path = tkFileDialog.asksaveasfilename(initialdir=nodes_dir)
        self.dest_label.configure(text=self.dest_path)

    def set_position(self, i):
        """Stores the Tracker's current (r,theta,phi)."""
        self.training_info[i] = self.tracker.measure_rtp_once()
        self.posn_labels[i].configure(text=str(self.training_info[i]))

    def save(self):
        """Recomputes the x/y/z CSV file based on our (name,r,theta,phi)s."""
        if None in self.training_info:
            showwarning("Can't recompute",
                        "Need 3 training points to recompute")
            return
        if (self.source_path is None) or (self.dest_path is None):
            showwarning("Can't recompute",
                        "Need a source and destination file")
            return

        training_data = {self.name_fields[i].get(): self.training_info[i]
                         for i in range(3)}
        try:
            old_data = nodes.load(self.source_path)
        except IOError:
            showwarning("{!r} no longer exists".format(self.source_path))
            return

        try:
            new_data = nodes.recompute(old_data, training_data)
        except ValueError as e:
            showwarning("Value error", e.message)
            return

        nodes.save(new_data, self.dest_path)
