from Util import *

import time
import serial.tools.list_ports
import _thread


class Arduino:
    _port = 0
    _stop = False  # Used to exit threads within THIS class.

    def __init__(self, port):
        self._port = port

    def start(self):
        self._stop = False  # Make sure it's not going to stop immediately.
        # TODO: Add listener

    def stop(self):
        self._stop = True
        if DEBUG:
            print('Sending {0} signal to Arduino on port: {1}'
                  .format(color('STOP', COLORS.RED),
                          color(self._port, COLORS.CYAN)))

    def get_port(self):
        return self._port
