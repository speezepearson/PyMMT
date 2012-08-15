class Actuator(object):
    microns_per_step = 0.158
    steps_per_micron = 1/microns_per_step
    def __init__(self, controller, port):
        self.controller = controller
        self.port = port

    def move(self, microns):
        steps = round(microns * self.steps_per_micron)
        self.controller.send_long_command('move', steps, self.port)
    def move_absolute(self, microns):
        steps = round(microns * self.steps_per_micron)
        self.controller.send_long_command('move_absolute', steps, self.port)

    def turn_motor_on(self):
        self.controller.send_short_command('turn_motor_on', self.port)
    def turn_motor_off(self):
        self.controller.send_short_command('turn_motor_off', self.port)

    def get_status(self):
        with self.controller.lock:
            self.controller.send_short_command('get_status', self.port)
            return Status(self.controller.read())


class Status(object):
    def __init__(self, status_string):
        split = status_string.split(" ")
        self.position = int(split[3])
        self.potentiometer_value = int(split[5])
        self.encoder_value = int(split[7])
        self.is_home = (split[8] == "MtrHome")

    def __str__(self):
        return "(posn {}, pot {}, enc {})".format(self.position,
                                                  self.potentiometer_value,
                                                  self.encoder_value)
