from PyMMT.gui import MainFrame
from Tkinter import Tk

root = Tk()
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
f = MainFrame(root, None, None)
f.grid(sticky='nsew')
root.mainloop()
