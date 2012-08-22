# This file defines the RepositioningFrame class, which helps the user
# handle the tracker being repositioned.

from Tkinter import LabelFrame, Entry, Label, Button
from tkMessageBox import showwarning
from ..nodes.repositioning import recompute

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

        f = LabelFrame(self, text="Source file")
        self.source_field = Entry(f)
        self.source_field.insert(0, "nodes.csv") # suggested file in nodes/
        self.source_field.grid()
        f.grid(row=0, column=0)
        f = LabelFrame(self, text="Dest file")
        self.dest_field = Entry(f)
        self.dest_field.grid()
        f.grid(row=0, column=1)

        # The names and positions we gather:
        self.name_fields = []
        self.posn_labels = []
        self.rthetaphis = []

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
            self.rthetaphis.append(None)

        Button(self, text="Compute/Save", command=self.save).grid(row=4,
                                                                  column=0)

    def set_position(self, i):
        """Stores the Tracker's current (r,theta,phi)."""
        r, theta, phi = self.tracker.measure()
        self.rthetaphis[i] = (r, theta, phi)
        self.posn_labels[i].configure(text=str(self.rthetaphis[i]))

    def save(self):
        """Recomputes the x/y/z CSV file based on our (name,r,theta,phi)s."""
        if None in self.rthetaphis:
            showwarning("Can't recompute",
                        "Need 3 training points to recompute")
            return
        try:
            recompute(source_filename=self.source_field.get(),
                      dest_filename=self.dest_field.get(),
                      namerthetaphis=[((self.name_fields[i].get(),)
                                       + self.rthetaphis[i])
                                      for i in range(3)])
                        
        except IOError as e:
            showwarning("I/O Error", "Failed to open {!r}".format(e.filename))
        except ValueError as e:
            showwarning("Value Error", str(e.message))

