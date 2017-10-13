from Util import *

import time
import serial.tools.list_ports
import serial
import threading


class Arduino:
    _stop = False  # Used to exit threads within THIS class.
    _state = STATE.STOPPED

    def __init__(self, port):
        self._port = port
        self._ser = serial.Serial(port=self._port)  # Defaults to 9600 baudrate
        self._listener = threading.Thread(target=self._listen, args=(.2,))  # Prepare listener for .2 second interval

    def start(self):
        self._stop = False  # Make sure it's not going to stop immediately.
        self._state = STATE.RUNNING
        self._listener.start()

    def stop(self):
        self._stop = True
        self._state = STATE.STOPPED
        if DEBUG:
            print('{0} Arduino connection on port: {1}'
                  .format(color('STOPPING', COLORS.RED),
                          color(self._port, COLORS.CYAN)))

    def get_state(self):
        return self._state

    def get_port(self):
        return self._port

    def _listen(self, delay):
        while not self._stop:
            if self._ser.inWaiting() > 0:
                byte = self._ser.read()

                if byte == COMMANDS.NOP:
                    pass

            time.sleep(delay)  # Wait about 100ms before polling again.
