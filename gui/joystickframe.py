from Tkinter import LabelFrame, Canvas, Scale, HORIZONTAL

class JoystickFrame(LabelFrame):
    def __init__(self, master, tracker, history, text="Joystick", **options):
        LabelFrame.__init__(self, master, text=text, **options)
        self.tracker = tracker
        self.history = history

        self.width = 400
        self.height = 400
        self.canvas = Canvas(self, height=self.height, width=self.width)
        self.canvas.grid()
        self.canvas.create_oval((self.width/2 - 3, self.height/2 - 3,
                                 self.width/2 + 3, self.height/2 + 3))
        self.canvas.bind("<Button-1>", self.move_tracker)

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

    def move_tracker(self, event):
        dx = event.x - self.width/2.
        dy = event.y - self.height/2.
        dx_rad = dx*self.sensitivity
        dy_rad = dy*self.sensitivity
        dtheta = dy_rad
        dphi = -dx_rad
        self.tracker.move(0, dtheta, dphi)
        self.history.add("Moved tracker by ({}, {})".format(dtheta, dphi))
