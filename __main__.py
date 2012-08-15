from Tkinter import Tk
from PyMMT.gui import MainFrame
from PyMMT.tracker import Tracker
from PyMMT.actuators import ActuatorController

tracker = Tracker()
tracker.open()
controller = ActuatorController()
controller.open()

root = Tk()
main_frame = MainFrame(master=root, tracker=tracker, controller=controller)
main_frame.grid()

root.mainloop()

tracker.close()
controller.close()
