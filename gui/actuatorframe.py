from Tkinter import Frame, Button, Label, Entry, LabelFrame, EXTENDED
from . import PAD
from .historyframe import HistoryFrame
from .infoframe import InfoFrame
from ..actuators import Actuator
from useful.tkinter import ScrollableFrame, Listbox

class ActuatorFrame(LabelFrame):
    def __init__(self, master, controller, text="Actuators", *args, **kwargs):
        LabelFrame.__init__(self, master, text=text, *args, **kwargs)
        self.controller = controller

        self.info_frame = InfoFrame(self, text="Selection / History",
                                    padx=PAD, pady=PAD)
        self.info_frame.grid(row=0, column=0, sticky='nsew')
        self.history = self.info_frame.history
        self.listbox = self.info_frame.listbox
        self.listbox.widget.configure(selectmode=EXTENDED)

        self.movement_frame = MovementFrame(self, padx=PAD, pady=PAD)
        self.movement_frame.grid()

        self.get_status_button = Button(self, text="Get status",
                                        command=self.get_status)
        self.get_status_button.grid()

        for i in range(192, 208, 2):
            self.listbox.add(Actuator(port=i, controller=controller),
                             name=str(i))

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def get_status(self):
        for actuator in self.listbox.get_selection():
            status = actuator.get_status()
            self.history.add("Status of actuator {}: {}"
                             .format(actuator.port, status))


class MovementFrame(LabelFrame):
    def __init__(self, master, text="Movement", **options):
        LabelFrame.__init__(self, master, text=text, **options)
        self.history = master.history
        self.listbox = master.listbox
        self.controller = master.controller

        self.micron_frame = LabelFrame(self, text="Microns")
        self.micron_field = Entry(self.micron_frame)
        self.micron_field.grid()
        self.micron_frame.grid(row=0, column=0, columnspan=2)

        self.move_button = Button(self, text="Move",
                                  command=self.move_actuators)
        self.move_button.grid(row=1, column=0)
        self.move_absolute_button = Button(self,
                                           text="Move absolute",
                                           command=self.move_absolute)
        self.move_absolute_button.grid(row=1, column=1)

    def move_actuators(self):
        microns = self.get_microns()
        if microns is None:
            return
        for actuator in self.listbox.get_selection():
            actuator.move(microns)
            self.history.add("Moved actuator {} by {} microns."
                             .format(actuator.port, microns))
    def move_absolute(self):
        microns = self.get_microns()
        if microns is None:
            return
        for actuator in self.listbox.get_selection():
            actuator.move(microns)
            self.history.add("Moved actuator {} by {} microns (absolute)."
                             .format(actuator.port, microns))

    def _unsafe_parse_microns(self):
        return float(self.micron_field.get())
    def get_microns(self):
        return self.history.try_callback(self._unsafe_parse_microns,
                                         "Unable to parse micron field.")

