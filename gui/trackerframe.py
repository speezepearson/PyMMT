# This file defines the TrackerFrame class, which provides the user with
# a bunch of controls for sending commands to the tracker and taking
# measurements with it.

from Tkinter import (Frame, Button, Label, Entry,
                     LabelFrame, Toplevel, END, SINGLE)
from .historyframe import HistoryFrame
from .. import tracker
from .repositioningframe import RepositioningFrame
from .joystickframe import JoystickFrame
from .. import nodes
import tkFileDialog

from srptools.tkinter import ScrollableFrame, Listbox, OptionMenu

class TrackerFrame(LabelFrame):
    """Provides controls for a laser tracker."""
    def __init__(self, master, tracker, text="Tracker",
                 *args, **kwargs):
        LabelFrame.__init__(self, master, text=text, *args, **kwargs)
        self.tracker = tracker

        self.history = HistoryFrame(self)
        self.history.grid(row=0, column=0, columnspan=2, sticky='nsew')

        self.command_frame = CommandFrame(self)
        self.command_frame.grid(row=1, column=0)

        self.mode_frame = ModeFrame(self)
        self.mode_frame.grid(row=2, column=0)

        self.movement_frame = MovementFrame(self)
        self.movement_frame.grid(row=3, column=0)

        self.position_frame = PositionFrame(self)
        self.position_frame.grid(row=1, column=1, rowspan=3)

        self.reposition_button = Button(self, text="Reposition",
                                        command=self.open_reposition_frame)
        self.reposition_button.grid()

        self.joystick_button = Button(self, text="Joystick",
                                        command=self.open_joystick_frame)
        self.joystick_button.grid()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def open_reposition_frame(self):
        """Opens a window to deal with the tracker being repositioned."""
        window = Toplevel()
        window.title("Repositioning")
        RepositioningFrame(window, self.tracker).grid()
    def open_joystick_frame(self):
        """Opens a joystick window for mouse-based tracker control."""
        window = Toplevel()
        window.title("Joystick")
        JoystickFrame(window, self.tracker, self.history).grid()


class CommandFrame(LabelFrame):
    """Has several buttons for simple, no-argument commands."""
    def __init__(self, master, text="Basic commands", **options):
        LabelFrame.__init__(self, master, text=text, **options)
        self.history = master.history
        self.tracker = master.tracker

        self.connect_button = Button(self, text="Connect",
                                     command=self.connect)
        self.connect_button.grid(row=0, column=0)
        self.initialize_button = Button(self, text="initialize",
                                        command=self.initialize)
        self.initialize_button.grid(row=0, column=1)
        self.disconnect_button = Button(self, text="Disconnect",
                                        command=self.disconnect)
        self.disconnect_button.grid(row=0, column=2)
        self.measure_button = Button(self, text="Measure",
                                     command=self.measure)
        self.measure_button.grid(row=1, column=0)
        self.abort_button = Button(self, text="Abort",
                                   command=self.abort)
        self.abort_button.grid(row=1, column=1)

    def connect(self):
        self.tracker.connect()
        self.history.add("Connected.")
    def initialize(self):
        self.tracker.initialize()
        self.history.add("Initialized.")
    def disconnect(self):
        self.tracker.disconnect()
        self.history.add("Disconnected.")
    def measure(self):
        response = self.tracker.measure()
        self.history.add("Measured; response = {!r}".format(response))
    def abort(self):
        self.tracker.abort()
        self.history.add("Aborted.")


class ModeFrame(LabelFrame):
    """Has controls for setting the laser tracker's mode."""
    def __init__(self, master, text="Modes", **options):
        LabelFrame.__init__(self, master, text=text, **options)
        self.history = master.history
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
        self.history.add("Set mode to {}.".format(mode))
        

class MovementFrame(LabelFrame):
    """Has controls for aiming the laser tracker."""
    def __init__(self, master, text="Movement", **options):
        LabelFrame.__init__(self, master, text=text, **options)
        self.history = master.history
        self.tracker = master.tracker

        self.coordinate_frame = CoordinateFrame(self)
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
        coords = self.coordinate_frame.parse_r_theta_phi()
        if coords is None:
            return
        r, theta, phi = coords
        self.tracker.move(r, theta, phi)
        self.history.add("Moved tracker by {}".format((r, theta, phi)))
    def move_absolute(self):
        coords = self.coordinate_frame.parse_r_theta_phi()
        if coords is None:
            return
        r, theta, phi = coords
        self.tracker.move_absolute(r, theta, phi)
        self.history.add("Moved tracker by {} (absolute)".format((r, theta,
                                                                  phi)))
    def search(self):
        r = self.coordinate_frame.parse_radius()
        if r is None:
            return
        self.tracker.search(r)
        self.history.add("Searched with radius {}.".format(r))


class CoordinateFrame(LabelFrame):
    """Gives fields for entering spherical polar coordinates."""
    def __init__(self, master, text="R, Theta, Phi", **options):
        LabelFrame.__init__(self, master, text=text, **options)
        self.history = master.history
        self.tracker = master.tracker

        self.radius_field = Entry(self)
        self.radius_field.grid(row=0, column=0)
        self.theta_field = Entry(self)
        self.theta_field.grid(row=1, column=0)
        self.phi_field = Entry(self)
        self.phi_field.grid(row=2, column=0)

    def parse_r_theta_phi(self):
        result = (self.parse_radius(), self.parse_theta(), self.parse_phi())
        return (None if None in result else result)
    def parse_radius(self):
        return self.history.try_callback(self._unsafe_parse_radius,
                                         "Failed to parse radius field.")
    def parse_theta(self):
        return self.history.try_callback(self._unsafe_parse_theta,
                                         "Failed to parse theta field.")
    def parse_phi(self):
        return self.history.try_callback(self._unsafe_parse_phi,
                                         "Failed to parse phi field.")
    def _unsafe_parse_radius(self):
        return float(self.radius_field.get())
    def _unsafe_parse_theta(self):
        return float(self.theta_field.get())
    def _unsafe_parse_phi(self):
        return float(self.phi_field.get())

class PositionFrame(LabelFrame):
    """Remembers tracker positions."""
    def __init__(self, master, text="Position", **options):
        LabelFrame.__init__(self, master, text=text, **options)
        self.history = master.history
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
        r, theta, phi = self.tracker.measure()
        name = self.name_field.get()
        self.listbox.add((r, theta, phi), name)
        self.history.add("Saved {} as {}".format((r, theta, phi), name))
    
    def go_to_position(self):
        """Moves the tracker to the selected position."""
        selection = self.listbox.get_selection()
        names = self.listbox.get_selected_names()
        if len(selection) > 0:
            r, theta, phi = selection[0]
            name = names[0]
            response = self.tracker.move_absolute(r, theta, phi)
            self.history.add("Moved tracker to {!r}: response is {!r}"
                             .format(name, response))
        else:
            self.history.add("Must select a position to go to.")
        

    def delete_position(self):
        """Deletes the selected position."""
        self.listbox.remove_selected()

    def write_to_file(self):
        filename = tkFileDialog.asksaveasfilename()
        if filename:
            nodes.io.save(self.listbox.as_dict(), filename)
    def load_from_file(self):
        filename = tkFileDialog.askopenfilename()
        if filename:
            self.listbox.clear()
            for (key, value) in nodes.io.load(filename).items():
                self.listbox.add(item=value, name=key)
