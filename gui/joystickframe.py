from Tkinter import Label, LabelFrame, Canvas, Scale, HORIZONTAL
import tkFont

class JoystickFrame(LabelFrame):
    def __init__(self, master, tracker, text="Joystick", **options):
        LabelFrame.__init__(self, master, text=text, **options)
        self.tracker = tracker

        self.width = 400
        self.height = 400
        self.canvas = Canvas(self, height=self.height, width=self.width)
        self.canvas.grid()
        self.canvas.create_oval((self.width/2 - 3, self.height/2 - 3,
                                 self.width/2 + 3, self.height/2 + 3))
        self.canvas.bind("<Button-1>", self.move_tracker)
        self.canvas.bind("<Motion>", self.update_label)

        self.motion_label = Label(self, text="",
                                  font=tkFont.Font(family="Courier"))
        self.motion_label.grid()

        f = LabelFrame(self, text="Sensitivity")
        self.sensitivity_scale = Scale(f, from_=0, to=10,
                                       resolution=0.01,
                                       orient=HORIZONTAL,
                                       length=self.width)
        self.sensitivity_scale.set(5)
        self.sensitivity_scale.grid()
        f.grid()

    @property
    def sensitivity(self):
        return self.sensitivity_scale.get() / 2000.

    def get_delta(self, event):
        dx = event.x - int(self.canvas['width'])/2.
        dy = event.y - int(self.canvas['height'])/2.
        dx_rad = dx*self.sensitivity
        dy_rad = dy*self.sensitivity
        dtheta = dy_rad
        dphi = -dx_rad
        return (dtheta, dphi)

    def update_label(self, event):
        dtheta, dphi = self.get_delta(event)
        self.motion_label.configure(text="<{:8.5f}, {:8.5f}>".format(dtheta,
                                                                     dphi))

    def move_tracker(self, event):
        dtheta, dphi = self.get_delta(event)
        self.tracker.move(0, dtheta, dphi)
