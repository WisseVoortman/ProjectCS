import serial.tools.list_ports
import time

ports = list(serial.tools.list_ports.comports())
for p in ports:
    print("port: ", p)
    if "Arduino" in p[1]:
        print("This is an Arduino!")
        print("p0", p[0])

while True:
    oldports = ports
    ports = list(serial.tools.list_ports.comports())
    if oldports != ports:
        print("the ports have changed")
        time.sleep(5)
    else:
        print("no changes detected")
        time.sleep(5)