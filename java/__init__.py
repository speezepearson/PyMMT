import os
import subprocess
import threading
import py4j.java_gateway

here = os.path.dirname(os.path.abspath(__file__))
classpath = os.pathsep.join(('.', 'lib', os.path.join('lib', '*')))

_gateway = None
def get_gateway():
    global _gateway
    if _gateway is None:
        _gateway = py4j.java_gateway.JavaGateway()
    return _gateway

class ServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.subprocess = subprocess.Popen(['java', '-classpath',
                                            classpath, 'StartServer'],
                                           cwd=here,
                                           stdout=subprocess.PIPE)
    def __del__(self):
        self.subprocess.kill()


def compile():
    subprocess.call(['javac', '-classpath', classpath, 'StartServer.java'],
                    cwd=here)

def start_server(blocking=True):
    t = ServerThread()
    t.start()
    print "Read {!r}".format(t.subprocess.stdout.readline())
    if blocking:
        t.join()
