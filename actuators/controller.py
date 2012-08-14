import d2xx
import time
import struct
import threading

FT232_SERIAL_NUMBER = "A6007pN3"
FT245_SERIAL_NUMBER = "A3000wLU"

class HandleWrapper(object):
    def __init__(self, serial_number):
        self.serial_number = serial_number
        self.handle = None

    def open(self):
        self.handle = d2xx.openEx(self.serial_number,
                                  d2xx.OPEN_BY_SERIAL_NUMBER)
        self.configure_handle()
    def configure_handle(self):
        pass
    def close(self):
        self.handle.close()
        self.handle = None
    def __del__(self):
        if self.handle is not None:
            self.handle.close()

    def read(self, *args, **kwargs):
        return self.handle.read(*args, **kwargs)
    def write(self, *args, **kwargs):
        return self.handle.write(*args, **kwargs)

class FT232Wrapper(HandleWrapper):
    def configure_handle(self):
        self.handle.setBaudRate(d2xx.BAUD_9600)
        self.handle.setDataCharacteristics(d2xx.BITS_8,
                                           d2xx.STOP_BITS_1,
                                           d2xx.PARITY_NONE)

    def read(self):
        result = self.handle.read(1)
        while result[:-3] != 'eol':
            result += self.handle.read(1)
        return result[:-3].rstrip()

class FT245Wrapper(HandleWrapper):
    def configure_handle(self):
        self.ft245_handle.setBitMode(0xFF, d2xx.BITMODE_ASYNC_BITBANG)

    def set_port(self, port):
        bits = bin(port)[2:]
        flipped = int(''.join(reversed(bits)), 2)
        self.handle.write(chr(flipped))

    def write(self, message, port):
        self.set_port(port)

        checksum = 0
        for byte in message:
            checksum ^= ord(byte)
        return self.handle.write(message + chr(checksum))

class ActuatorController(object):
    long_commands = {'move': '\x50',
                     'move_absolute': '\xB0'}
    short_commands = {'motor_on': '\x11\xff',
                      'motor_off': '\x11\x00',
                      'motor_off_hard': '\x15\x00',
                      'get_status': '\x3C'}

    def __init__(self, ft232_serial_number, ft245_serial_number):
        self.ft232_wrapper = FT232Wrapper(ft232_serial_number)
        self.ft245_wrapper = FT245Wrapper(ft245_serial_number)
        self.lock = threading.ReentrantLock()
    
    def open(self):
        self.ft232_wrapper.open()
        self.ft245_wrapper.open()
    def close(self):
        self.ft232_wrapper.close()
        self.ft245_wrapper.close()
    
    def read(self):
        with self.lock:
            return self.ft232_wrapper.read()
    def write(self, message, port):
        with self.lock:
            return self.ft245_wrapper.write(message, port)

    def send_short_command(self, command, port):
        self.write(self.short_commands[command], port)
    def send_long_command(self, command, long, port):
        long_bytes = struct.pack('>l', long)
        self.write(self.long_commands[command] + long_bytes, port)
