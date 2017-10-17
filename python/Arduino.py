from Util import *

import time
import serial.tools.list_ports
import serial
import threading
from arduinoGUI import arduinoGUI

class Arduino:
    _stop = False  # Used to exit threads within THIS class.
    _state = STATE.STOPPED

    def __init__(self, port, model):
        self._port = port
        self._ser = serial.Serial(port=self._port)  # Defaults to 9600 baudrate
        self._listener = threading.Thread(target=self._listen, args=(.2,))  # Prepare listener for .2 second interval
        self._model = model

    def start(self):
        self._stop = False  # Make sure it's not going to stop immediately.
        self._state = STATE.RUNNING
        self._listener.start()
        self._model.views[self._port] = arduinoGUI(self._model.mainframe, self)

    def stop(self):
        self._stop = True
        self._state = STATE.STOPPED
        if DEBUG:
            print('{0} Arduino connection on port: {1}'
                  .format(color('STOPPING', COLORS.RED),
                          color(self._port, COLORS.CYAN)))

        try:
            self._model.views[self._port].remove()
        except:
            print("Couldn't delete view?")

    def get_state(self):
        return self._state

    def get_port(self):
        return self._port

    def send(self, command, args):
        send_thread = threading.Thread(target=self._send, args=(command, args))
        send_thread.start()

    def _send(self, command, args):
        self._ser.write(command)  # Send the command
        for param in args:
            self._ser.write(param)  # Send all parameters

    def _listen(self, delay):
        while not self._stop:
            try:
                if self._ser.inWaiting() > 0:
                    byte = self._ser.read()
                    byte = '0x' + byte.hex()  # Write it as a proper hexadecimal

                    if DEBUG:
                        print('[{0}]: {1}'.format(self._port, byte))

                    if byte == COMMANDS.NOP:
                        pass

            except:
                print(color('Failed to read data.', COLORS.RED))
                # Try to restart our serial connection
                try:
                    print(color('Attempting to re-open port: {0}'
                                .format(color(self._port, COLORS.RED)), COLORS.LIME))
                    self._ser = serial.Serial(port=self._port)
                except:
                    print(color('Failed to re-open port: {0}'
                                .format(self._port), COLORS.RED))
                time.sleep(5)  # Wait at least 5 seconds before continuing

            time.sleep(delay)  # Wait before polling again.
