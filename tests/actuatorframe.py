from PyMMT.gui import ActuatorFrame
from Tkinter import Tk

root = Tk()

f = ActuatorFrame(root, controller=None)
f.pack()

root.mainloop()
