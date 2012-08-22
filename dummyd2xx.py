# This file provides functions and classes that look like those in the
# d2xx library, so that the actuator-controlling portion of this package
# can run on computers that don't have it.
# We provide only as much "functionality" as is required to keep
# PyMMT/actuators/board.py running semi-realistically.

# A real system only produces messages once in a while. To simulate that,
# we throw in a waiting period every so often. We also have to be thread-
# safe, since different threads may try to read and write from us.
import time as _time
import threading as _threading

OPEN_BY_SERIAL_NUMBER = None
BAUD_9600 = None
BITS_8 = None
STOP_BITS_1 = None
PARITY_NONE = None
BITMODE_ASYNC_BITBANG = None

def openEx(*args):
    return DummyHandle()

class DummyHandle(object):
    _status_message = "blah blah posn 0 pot 0 enc 0 MtrHome eol"
    _ack_message = "good checksum eol"
    _nack_message = "bad checksum eol"
    def __init__(self):
        self.buffer = ''
        self.lock = _threading.Lock()
    def setBaudRate(self, rate):
        pass
    def setDataCharacteristics(self, word_length, stop_bits, parity):
        pass
    def setBitMode(self, mask, mode):
        pass
    def read(self, num_bytes):
        """Waits until num_bytes are available, then returns them."""
        while len(self.buffer) < num_bytes:
            _time.sleep(1)
            with self.lock:
                self.buffer += self._status_message
        result, self.buffer = self.buffer[:num_bytes], self.buffer[num_bytes:]
        return result
    def write(self, data):
        """Adds an ack or a nack to the buffer. Depends on checksum."""
        checksum = reduce((lambda x,y: x^y),
                          [ord(c) for c in data], 0)
                          
        with self.lock:
            self.buffer += (self._ack_message if checksum==0
                            else self._nack_message)
    def close(self):
        pass
