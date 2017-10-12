from Arduino import Arduino
from Util import *

import time
import serial.tools.list_ports
import _thread


# Main controller for back-end
class PyCtrl:
    _available_ports = []
    _available_arduinos = []
    _stop = False  # Used to exit threads within THIS class

    def start(self):
        _thread.start_new_thread(self._update_ports, (5,))
        while not self._stop:
            time.sleep(2)  # Reduce CPU usage

    def stop(self):
        if DEBUG:
            print(color('Stopping back-end process.', COLORS.YELLOW))
        self._stop = True
        for ard in self._available_arduinos:
            ard.stop()

    # Listen to our available ports, and update them
    def _update_ports(self, delay):
        while True:
            if self._stop:
                _thread.exit_thread()
            if DEBUG:
                print('Running port-scan.')
            # Get all ports
            ports = list(serial.tools.list_ports.comports())

            # Check all ports
            for p in ports:
                if "Arduino" in p[1]:
                    if not p[0] in self._available_ports:
                        self._available_ports.append(p[0])  # Set port to in-use
                        self._available_arduinos.append(Arduino(p[0]))  # Add a new arduino to our list
                        if DEBUG:
                            print('Added new Arduino on port: {0}'.format(color(p[0], COLORS.CYAN)))

            # Remove inactive ports
            for k in self._available_ports:
                r = 1
                for p in ports:
                    if k == p[0]:
                        r = 0
                if r:
                    del self._available_ports[k]
                    if DEBUG:
                        print('Removed inactive port: {0}'.format(color(k, COLORS.CYAN)))

            # Update our actual list
            for ard in self._available_arduinos:
                if not ard.get_port() in self._available_ports:
                    ard.stop()
                    del ard

            time.sleep(delay)
