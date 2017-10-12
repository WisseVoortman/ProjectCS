import Util

import time
import serial.tools.list_ports
import _thread


class Arduino:
    port = 0

    def __init__(self, port):
        self.port = port

    def get_port(self):
        return self.port
