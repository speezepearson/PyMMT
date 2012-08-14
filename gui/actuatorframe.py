from Tkinter import (Frame, Button, Label, Entry, LabelFrame,
                     END, EXTENDED)
from .historyframe import HistoryFrame
from .infoframe import InfoFrame
from useful.tkinter import ScrollableFrame, Listbox

class ActuatorFrame(LabelFrame):
    def __init__(self, controller, *args, **kwargs):
        kwargs['text'] = 'Actuators'
        LabelFrame.__init__(self, *args, **kwargs)
        self.controller = controller

        self.info_frame = InfoFrame(self, text="Selection / History")
        self.info_frame.grid(row=0, column=0, sticky='nsew')
        self.history = self.info_frame.history
        self.listbox = self.info_frame.listbox

        self.movement_frame = MovementFrame(self)
        self.movement_frame.grid()

        self.get_status_button = Button(self, text="Get status",
                                        command=self.get_status)
        self.get_status_button.grid()

        for i in range(192, 208, 2):
            self.listbox.add(i)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def get_status(self):
        for port in self.listbox.get_selection():
            self.history.add("Getting status from actuator {}".format(port))


class MovementFrame(LabelFrame):
    def __init__(self, master, history=None, listbox=None, controller=None,
                 text="Movement", **options):
        LabelFrame.__init__(self, master, text=text, **options)
        self.history = (master.history if history is None else history)
        self.listbox = (master.listbox if listbox is None else listbox)
        self.controller = (master.controller if controller is None
                           else controller)

        self.micron_frame = LabelFrame(self, text="Microns")
        self.micron_field = Entry(self.micron_frame)
        self.micron_field.grid()
        self.micron_frame.grid(row=0, column=0)

        self.move_button = Button(self, text="Move",
                                  command=self.move_actuators)
        self.move_button.grid(row=1, column=0)
        self.move_absolute_button = Button(self,
                                           text="Move absolute",
                                           command=self.move_absolute)
        self.move_absolute_button.grid(row=2, column=0)

    def move_actuators(self):
        microns = self.get_microns()
        if microns is not None:
            for port in self.listbox.get_selection():
                self.history.add("Moved actuator {} by {} microns."
                                 .format(port, microns))
    def move_absolute(self):
        microns = self.get_microns()
        if microns is not None:
            for port in self.listbox.get_selection():
                self.history.add("Moved actuator {} by {} microns"
                                 " (absolute)."
                                 .format(port, microns))

    def _unsafe_parse_microns(self):
        return float(self.micron_field.get())
    def get_microns(self):
        return self.history.try_callback(self._unsafe_parse_microns,
                                         "Unable to parse micron field.")

