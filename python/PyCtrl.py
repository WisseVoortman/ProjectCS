import time
import serial.tools.list_ports
import _thread


# Main controller for back-end
class PyCtrl:
    _available_ports = {}
    _available_arduinos = {}

    def __init__(self):
        # Make sure our list is always up-to-date
        _thread.start_new_thread(self._update_ports, self)

        # Gotta go fast
        while 1:
            pass

    # Listen to our available ports, and update them
    def _update_ports(self):
        while True:
            # Get all ports
            ports = list(serial.tools.list_ports.comports())

            # Check all ports
            for p in ports:
                if "Arduino" in p[1]:
                    # Add port to our list if it isn't there yet
                    if not self._available_ports[p[0]]:
                        self._available_ports[p[0]] = True

            # Remove non-existent ports
            for k in self._available_ports.keys():
                r = 1
                for p in ports:
                    if k == p[0]:
                        r = 0
                if r:
                    del self._available_ports[k]

            # Update our actual list
            for a in self._available_arduinos:
                if not a.get_port() in self._available_ports:
                    del a

            time.sleep(1)  # Wait at least 1 second before re-checking

# Class for actually controlling any in/out-going connections
class Arduino:
    port = 0

    def __init__(self, port):
        self.port = port

    def get_port(self):
        return self.port
