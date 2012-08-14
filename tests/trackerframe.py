from PyMMT.gui import TrackerFrame
from Tkinter import Tk

root = Tk()
f = TrackerFrame(root, tracker=None)
f.grid()
root.mainloop()