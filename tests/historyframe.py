from PyMMT.gui import HistoryFrame
from Tkinter import Tk
import time

root = Tk()
hf = HistoryFrame(root)
hf.grid()

hf.add("Hellooooooo sexy!")
for i in range(20):
    root.after(500*(1+i), hf.add, str(i))

root.mainloop()
