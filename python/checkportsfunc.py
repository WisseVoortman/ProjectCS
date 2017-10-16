def checkPortsOnce():
    View.ports = list(serial.tools.list_ports.comports())

    for p in View.ports:
        print("port: ", p)


def checkPortsLoop():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print("port: ", p)
        if "Arduino" in p[1]:
            print("This is an Arduino!")
            print("p0", p[0])
    i = 0
    while i in range(10):
        oldports = ports
        ports = list(serial.tools.list_ports.comports())
        if oldports != ports:
            print("the ports have changed")
            time.sleep(3)
            i = i + 1
            print(i)
        else:
            print("no changes detected")
            time.sleep(3)
            i = i + 1
            print(i)