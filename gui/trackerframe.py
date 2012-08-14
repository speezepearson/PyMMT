from Tkinter import (Frame, Button, Label, Entry,
                     LabelFrame, END, SINGLE)
from .historyframe import HistoryFrame
from useful.tkinter import ScrollableFrame, Listbox, OptionMenu

IFM = 'IFM'
ADM = 'ADM'
IFM_SET_BY_ADM = 'IFM set by ADM'

class TrackerFrame(LabelFrame):
    def __init__(self, master, tracker, *args, **kwargs):
        kwargs['text'] = 'Tracker'
        LabelFrame.__init__(self, master, *args, **kwargs)
        self.tracker = tracker

        self.history = HistoryFrame(self)
        self.history.grid(sticky='nsew')

        self.command_frame = CommandFrame(self)
        self.command_frame.grid()

        self.mode_frame = ModeFrame(self)
        self.mode_frame.grid()

        self.movement_frame = MovementFrame(self)
        self.movement_frame.grid()

        self.position_frame = PositionFrame(self)
        self.position_frame.grid()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)


class CommandFrame(LabelFrame):
    def __init__(self, master, history=None, tracker=None,
                 text="Basic commands", **options):
        LabelFrame.__init__(self, master, text=text, **options)
        self.history = (master.history if history is None else history)
        self.tracker = (master.tracker if tracker is None else tracker)

        self.connect_button = Button(self, text="Connect",
                                     command=self.connect)
        self.connect_button.grid(row=0, column=0)
        self.disconnect_button = Button(self, text="Disconnect",
                                        command=self.disconnect)
        self.disconnect_button.grid(row=0, column=1)
        self.measure_button = Button(self, text="Measure",
                                     command=self.measure)
        self.measure_button.grid(row=0, column=2)

    def connect(self):
        self.history.add("Connecting.")
    def disconnect(self):
        self.history.add("Disconnecting.")
    def measure(self):
        self.history.add("Measuring.")


class ModeFrame(LabelFrame):
    def __init__(self, master, history=None, tracker=None,
                 text="Modes", **options):
        LabelFrame.__init__(self, master, text=text, **options)
        self.history = (master.history if history is None else history)
        self.tracker = (master.tracker if tracker is None else tracker)

        self.mode_menu = OptionMenu(self, (IFM_SET_BY_ADM, IFM, ADM))
        self.mode_menu.grid(row=0, column=0)
        self.set_mode_button = Button(self, text="Set mode",
                                      command=self.set_mode)
        self.set_mode_button.grid(row=0, column=1)

    def set_mode(self):
        self.history.add("Setting mode to {}."
                                .format(self.mode_menu.get()))
        

class MovementFrame(LabelFrame):
    def __init__(self, master, history=None, tracker=None,
                 text="Movement", **options):
        LabelFrame.__init__(self, master, text=text, **options)
        self.history = (master.history if history is None else history)
        self.tracker = (master.tracker if tracker is None else tracker)

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
        self.history.add("Moved tracker by ({}, {}, {})."
                         .format(r, theta, phi))
    def move_absolute(self):
        coords = self.coordinate_frame.parse_r_theta_phi()
        if coords is None:
            return
        r, theta, phi = coords
        self.history.add("Moved tracker by ({}, {}, {}) (absolute)."
                         .format(r, theta, phi))
    def search(self):
        r = self.coordinate_frame.parse_radius()
        if r is None:
            return
        self.history.add("Searching with radius {}".format(r))


class CoordinateFrame(LabelFrame):
    def __init__(self, master, history=None, tracker=None,
                 text="R, Theta, Phi", **options):
        LabelFrame.__init__(self, master, text=text, **options)
        self.history = (master.history if history is None else history)
        self.tracker = (master.tracker if tracker is None else tracker)

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
    def __init__(self, master, history=None, tracker=None,
                 text="Position", **options):
        LabelFrame.__init__(self, master, text=text, **options)
        self.history = (master.history if history is None else history)
        self.tracker = (master.tracker if tracker is None else tracker)

        self.listbox = Listbox(self)
        self.listbox.listbox.configure(selectmode=SINGLE)
        self.listbox.grid(row=0, column=0, rowspan=3)

        self.name_frame = LabelFrame(self, text="Name")
        self.name_field = Entry(self.name_frame)
        self.name_field.grid()
        self.name_frame.grid(row=0, column=1)

        self.save_button = Button(self, text="Save current",
                                  command=self.save_position)
        self.save_button.grid(row=1, column=1)
        self.delete_button = Button(self, text="Delete",
                                    command=self.delete_position)
        self.delete_button.grid(row=2, column=1)

    def save_position(self):
        self.listbox.add(NotImplementedError(),
                         self.name_field.get())
    def delete_position(self):
        self.listbox.remove_selected()
        
