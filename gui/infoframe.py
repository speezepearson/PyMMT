from Tkinter import LabelFrame, EXTENDED
from useful.tkinter import Listbox
from historyframe import HistoryFrame

class InfoFrame(LabelFrame):
    def __init__(self, *args, **options):
        LabelFrame.__init__(self, *args, **options)

        self.listbox = Listbox(self)
        self.listbox.widget.configure(selectmode=EXTENDED)
        self.listbox.grid(row=0, column=0, sticky='nsew')

        self.history = HistoryFrame(self, width=200, height=100)
        self.history.grid(row=0, column=1, sticky='nsew')

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
