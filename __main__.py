from Tkinter import Tk
from PyMMT.gui import MainFrame
from PyMMT.tracker import Tracker
from PyMMT.actuators import ActuatorController
from PyMMT.java import compile
from PyMMT import RECOMPILE_JAVA

if RECOMPILE_JAVA:
    print "Recompiling Java code..."
    compile.run()
    print "Done."

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
