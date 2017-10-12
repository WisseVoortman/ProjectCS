from tkinter import *
from tkinter import ttk
import serial.tools.list_ports
import time

class View:
    def __init__(self):
        """Initialize the main Program View.
        """

        root = Tk() # initialize Root window

        root.title('Centrale Project 2.1 - Computer System ') # set title for Root window

        root.geometry("800x500+200+200") # set size and location for Root window

        mainframe = ttk.Frame(root, padding="3 3 12 12") # left top right bottem    create mainframe in Root winow

        mainframe.grid(column=0, row=0, sticky=(N, W, S, E)) # set mainframe to root windows size

        menubar = Menu(mainframe) # create a menubar

        # create a pulldown menu "FILE", and add it to the menu bar
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Team", command=team)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="Commands", menu=filemenu) # se the label in the menubar

        # display the menu
        root.config(menu=menubar)

        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        label = Label(mainframe, text="hieronder de control units:")
        label.pack()

        # arduino detection
        checkPortsOnce()

        root.mainloop()

def varInQuote():
    term = "foo"
    print("dikke vis %s" % term)

def team():
    print("Team 6")

def checkPortsOnce():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print("port: ", p)
        if "Arduino" in p[1]:
            print("This is an Arduino!")
            print("p0", p[0])

def addArduinoGUI():
    pass


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