# This submodule provides the rest of the PyMMT package with a
# simple-as-possible interface to the Java world. It provides three
# functions of note: get_gateway(), which returns a Py4J JavaGateway
# object; start_server(), which starts a Java GatewayServer running in
# the background; and compile(), which compiles the Java program which
# runs the GatewayServer.

import os
import subprocess
import atexit
import threading
import py4j.java_gateway

here = os.path.dirname(os.path.abspath(__file__))
classpath = os.pathsep.join(('.', 'lib', os.path.join('lib', '*')))
jclass = "StartServer"

_gateway = None
def get_gateway():
    global _gateway
    if _gateway is None:
        _gateway = py4j.java_gateway.JavaGateway()
    return _gateway

def compile():
    subprocess.call(['javac', '-classpath', classpath, jclass+".java"],
                    cwd=here)

def start_server():
    if not os.path.exists(os.path.join(here, jclass+".class")):
        try:
            compile()
        except OSError:
            raise OSError("can't compile program to start Java server")
    jprocess = subprocess.Popen(['java', '-classpath',
                                 classpath, jclass],
                                cwd=here,
                                stdout=subprocess.PIPE)
    jprocess.stdout.readline()
    atexit.register(jprocess.kill)
