# This file defines the ActuatorFrame class (et al.), which provides a
# bunch of controls for an ActuatorBoard.

import logging

from Tkinter import Frame, Button, Label, Entry, LabelFrame, EXTENDED
from srptools.tkinter import Listbox

logger = logging.getLogger(__name__)

class ActuatorFrame(LabelFrame):
    """Provides a bunch of controls for an ActuatorBoard."""
    def __init__(self, master, board, text="Actuators", *args, **kwargs):
        LabelFrame.__init__(self, master, text=text, *args, **kwargs)
        self.board = board
        
        # The listbox contains integers: port numbers we might
        # want to send messages out to through the Board.
        self.listbox = Listbox(self)
        self.listbox.widget.configure(selectmode=EXTENDED)
        self.listbox.grid(row=0, column=0, sticky='nsew')
        for i in range(192, 208, 2):
            self.listbox.add(i)

        self.movement_frame = MovementFrame(self)
        self.movement_frame.grid()

        self.get_status_button = Button(self, text="Get status",
                                        command=self.get_status)
        self.get_status_button.grid()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def get_status(self):
        for port in self.listbox.get_selected_items():
            status = self.board.get_status(port)
            logger.info("Status of actuator {}: {}".format(port, status))


class MovementFrame(LabelFrame):
    """Provides motion-related controls for an ActuatorBoard."""
    def __init__(self, master, text="Movement", **options):
        LabelFrame.__init__(self, master, text=text, **options)
        self.listbox = master.listbox
        self.board = master.board

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
        for port in self.listbox.get_selected_items():
            self.board.move(microns=microns, port=port)
            logger.info("Moved actuator {} by {} microns.".format(port,
                                                                  microns))
    def move_absolute(self):
        microns = self.get_microns()
        if microns is None:
            return
        for port in self.listbox.get_selected_items():
            self.board.move_absolute(microns=microns, port=port)
            logger.info("Moved actuator {} by {} microns (absolute)."
                        .format(port, microns))

    def _unsafe_parse_microns(self):
        return 
    def get_microns(self):
        try:
            return float(self.micron_field.get())
        except ValueError:
            logger.error("Unable to parse micron field.")
            return None
