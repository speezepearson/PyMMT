from PyMMT.gui import ActuatorFrame
from Tkinter import Tk

root = Tk()

f = ActuatorFrame(root, board=None)
f.pack()

root.mainloop()
