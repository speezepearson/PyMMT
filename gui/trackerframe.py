# This file defines the TrackerFrame class, which provides the user with
# a bunch of controls for sending commands to the tracker and taking
# measurements with it.

import os
import logging

from Tkinter import (Frame, Button, Label, Entry,
                     LabelFrame, Toplevel, END, SINGLE)
import tkFileDialog
from srptools.tkinter import (ScrollableFrame, Listbox, OptionMenu,
                              NamedEntryFrame)

from .. import tracker
from .repositioningframe import RepositioningFrame
from .joystickframe import JoystickFrame
from .. import nodes

logger = logging.getLogger(__name__)

here = os.path.dirname(os.path.abspath(__file__))
nodes_dir = os.path.join(os.path.dirname(here), "nodes")

class TrackerFrame(LabelFrame):
    """Provides controls for a laser tracker."""
    def __init__(self, master, tracker, text="Tracker",
                 *args, **kwargs):
        LabelFrame.__init__(self, master, text=text, *args, **kwargs)
        self.tracker = tracker

        self.command_frame = CommandFrame(self)
        self.command_frame.grid(row=0, column=0)

        self.mode_frame = ModeFrame(self)
        self.mode_frame.grid(row=1, column=0)

        self.movement_frame = MovementFrame(self)
        self.movement_frame.grid(row=2, column=0)

        self.position_frame = PositionFrame(self)
        self.position_frame.grid(row=0, column=1, rowspan=3)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

class CommandFrame(LabelFrame):
    """Has several buttons for simple, no-argument commands."""
    def __init__(self, master, text="Basic commands", **options):
        LabelFrame.__init__(self, master, text=text, **options)
        self.tracker = master.tracker

        self.initialize_button = Button(self, text="Initialize",
                                        command=self.initialize)
        self.initialize_button.grid(row=0, column=0)
        self.measure_button = Button(self, text="Measure once",
                                     command=self.measure)
        self.measure_button.grid(row=0, column=1)
        self.abort_button = Button(self, text="Abort",
                                   command=self.abort)
        self.abort_button.grid(row=1, column=0)
        self.home_button = Button(self, text="Home",
                                   command=self.home)
        self.home_button.grid(row=1, column=1)

    def initialize(self):
        self.tracker.initialize()
        logger.info("Initialized tracker.")
    def disconnect(self):
        self.tracker.disconnect()
        logger.info("Disconnected tracker.")
    def measure(self):
        response = self.tracker.measure()[0]
        logger.info("Tracker is at {}".format((response.distance(),
                                               response.zenith(),
                                               response.azimuth())))
    def abort(self):
        self.tracker.abort()
        logger.info("Aborted tracker action.")
    def home(self):
        self.tracker.home()
        logger.info("Homed tracker.")


class ModeFrame(LabelFrame):
    """Has controls for setting the laser tracker's mode."""
    def __init__(self, master, text="Modes", **options):
        LabelFrame.__init__(self, master, text=text, **options)
        self.tracker = master.tracker

        self.mode_menu = OptionMenu(self, (tracker.IFM_SET_BY_ADM,
                                           tracker.IFM, tracker.ADM))
        self.mode_menu.grid(row=0, column=0)
        self.set_mode_button = Button(self, text="Set mode",
                                      command=self.set_mode)
        self.set_mode_button.grid(row=0, column=1)

    def set_mode(self):
        mode = self.mode_menu.get()
        response = self.tracker.set_mode(mode)
        logger.info("Set tracker mode to {}.".format(mode))
        

class MovementFrame(LabelFrame):
    """Has controls for aiming the laser tracker."""
    def __init__(self, master, text="Movement", **options):
        LabelFrame.__init__(self, master, text=text, **options)
        self.tracker = master.tracker

        self.coordinate_frame = NamedEntryFrame(self, ("Radius", "Theta",
                                                       "Phi"),
                                                parsers={"Radius": float,
                                                         "Theta": float,
                                                         "Phi": float})
        self.coordinate_frame.grid(row=0, column=0, rowspan=3)

        self.search_button = Button(self, text="Search",
                                    command=self.search)
        self.search_button.grid(row=0, column=1)
        self.move_button = Button(self, text="Move",
                                  command=self.move_tracker)
        self.move_button.grid(row=1, column=1)
        self.move_absolute_button = Button(self, text="Move (absolute)",
                                           command=self.move_absolute)
        self.move_absolute_button.grid(row=2, column=1)

    def move_tracker(self):
        try:
            coords = self.coordinate_frame.get_all()
        except ValueError as e:
            logger.error("Parsing error: {}".format(e.message))
            return

        r, theta, phi = coords["Radius"], coords["Theta"], coords["Phi"]
        self.tracker.move(r, theta, phi)
        logger.info("Moved tracker by {}".format((r, theta, phi)))

    def move_absolute(self):
        try:
            coords = self.coordinate_frame.get_all()
        except ValueError as e:
            logger.error("Parsing error: {}".format(e.message))
            return

        r, theta, phi = coords["Radius"], coords["Theta"], coords["Phi"]
        self.tracker.move(r, theta, phi)
        logger.info("Moved tracker by {}".format((r, theta, phi)))
    def search(self):
        try:
            r = self.coordinate_frame.get("Radius")
        except ValueError:
            logger.error("Couldn't parse radius field.")
            return

        self.tracker.search(r)
        logger.info("Searched with radius {}.".format(r))

class PositionFrame(LabelFrame):
    """Remembers tracker positions."""
    def __init__(self, master, text="Position", **options):
        LabelFrame.__init__(self, master, text=text, **options)
        self.tracker = master.tracker

        self.listbox = Listbox(self)
        self.listbox.widget.configure(selectmode=SINGLE)
        self.listbox.grid(row=0, column=0, rowspan=6)

        self.name_frame = LabelFrame(self, text="Name")
        self.name_field = Entry(self.name_frame)
        self.name_field.grid()
        self.name_frame.grid(row=0, column=1)

        self.save_button = Button(self, text="Save current",
                                  command=self.save_position)
        self.save_button.grid(row=1, column=1)
        self.go_to_button = Button(self, text="Go to",
                                   command=self.go_to_position)
        self.go_to_button.grid(row=2, column=1)
        self.delete_button = Button(self, text="Delete",
                                    command=self.delete_position)
        self.delete_button.grid(row=3, column=1)
        self.write_button = Button(self, text="Write to file",
                                   command=self.write_to_file)
        self.write_button.grid(row=4, column=1)
        self.load_button = Button(self, text="Load from file",
                                   command=self.load_from_file)
        self.load_button.grid(row=5, column=1)

    def save_position(self):
        """Records the tracker's current position."""
        data = self.tracker.measure()[0]
        if data.status() != data.DATA_ACCURATE:
            logger.error("Data taken were not accurate.")
            return

        name = self.name_field.get()
        r, theta, phi = data.distance(), data.zenith(), data.azimuth()
        self.listbox.add((r, theta, phi), name)
        logger.info("Saved {} as {}".format((r, theta, phi), name))
    
    def go_to_position(self):
        """Moves the tracker to the selected position."""
        selection = self.listbox.get_selected_items()
        names = self.listbox.get_selected_names()
        if len(selection) > 0:
            r, theta, phi = selection[0]
            name = names[0]
            response = self.tracker.move_absolute(r, theta, phi)
            logger.info("Moved tracker to {!r}".format(name, response))
        else:
            logger.error("Must select a position to go to.")
        

    def delete_position(self):
        """Deletes the selected position."""
        self.listbox.remove_selected()

    def write_to_file(self):
        filename = tkFileDialog.asksaveasfilename(initialdir=nodes_dir)
        if filename:
            nodes.io.save(self.listbox.as_dict(), filename)
            logger.info("Wrote current node list to {!r}".format(filename))
    def load_from_file(self):
        filename = tkFileDialog.askopenfilename(initialdir=nodes_dir)
        if filename:
            self.listbox.clear()
            for (key, value) in nodes.io.load(filename).items():
                self.listbox.add(item=value, name=key)
            logger.info("Loaded node list from {!r}".format(filename))
