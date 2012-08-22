from PyMMT.gui.repositioningframe import RepositioningFrame
from Tkinter import Tk
from PyMMT.tracker import Tracker

with Tracker() as tracker:
    root = Tk()
    RepositioningFrame(root, tracker).grid()
    root.mainloop()
