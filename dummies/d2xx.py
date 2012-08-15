OPEN_BY_SERIAL_NUMBER = None
BAUD_9600 = None
BITS_8 = None
STOP_BITS_1 = None
PARITY_NONE = None
BITMODE_ASYNC_BITBANG = None

def openEx(*args):
    return DummyHandle()

class DummyHandle(object):
    _status_message = "blah blah posn 0 pot 0 enc 0 not_home eol"
    def __init__(self):
        self.buffer = ''
    def setBaudRate(self, rate):
        pass
    def setDataCharacteristics(self, word_length, stop_bits, parity):
        pass
    def setBitMode(self, mask, mode):
        pass
    def read(self, num_bytes):
        while len(self.buffer) < num_bytes:
            self.buffer += self._status_message
        result, self.buffer = self.buffer[:num_bytes], self.buffer[num_bytes:]
        return result
    def write(self, data):
        pass
    def close(self):
        pass
