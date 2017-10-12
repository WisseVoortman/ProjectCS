import time
import serial.tools.list_ports
import _thread


class PyCtrl:
    _available_ports = {}
    _available_arduinos = {}

    def __init__(self):
        # Init

        # Make sure our list is always up-to-date
        _thread.start_new_thread(self._update_ports, self)

    # Listen to our available ports, and update them!
    def _update_ports(self):
        while True:
            # Get all ports
            ports = list(serial.tools.list_ports.comports())

            # Check all ports
            for p in ports:
                if "Arduino" in p[1]:
                    # Do we already have this arduino?
                    if not self._available_ports[p[0]]:
                        self._available_ports[p[0]] = True

            # Remove non-existent arduino
            for k in self._available_ports.keys():
                r = 1
                for p in ports:
                    if k == p[0]:
                        r = 0
                if r:
                    del self._available_ports[k]

            # Update our actual list
            
            time.sleep(1)  # Wait at least 1 second before re-checking


class Arduino:
    port = 0

    def __init__(self, port):
        self.port = port

    def get_port(self):
        return self.port
