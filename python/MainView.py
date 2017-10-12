from tkinter import *
from tkinter import ttk
import serial.tools.list_ports
import time
import arduinoGUI

class View:
    def __init__(self):
        """Initialize the main Program View.
        """
        self.ports = list(serial.tools.list_ports.comports())

        self.root = Tk() # initialize Root window

        self.root.title('Centrale Project 2.1 - Computer System ') # set title for Root window

        self.root.geometry("800x500+200+200") # set size and location for Root window

        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12") # left top right bottem    create mainframe in Root winow

        self.mainframe.grid(column=0, row=0, sticky=(N, W, S, E)) # set mainframe to root windows size

        menubar = Menu(self.mainframe) # create a menubar

        # create a pulldown menu "FILE", and add it to the menu bar
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Team", command=View.team)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="Commands", menu=filemenu) # se the label in the menubar

        # display the menu
        self.root.config(menu=menubar)

        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        label = Label(self.mainframe, text="hieronder de control units:")
        label.pack()

        label2 = Label(self.mainframe, text="hier een 2e label")
        label2.pack()

        # arduino detection
        View.checkPortsOnce()

        for p in View.ports:
            if "Arduino" in p[1]:
                print("Arduino Gevonden op Poort: ", p[0])
                exec("View." + p[0] + " = arduinoGUI.GUI()") # going to assign a class here that is going to render the gui items that belong to a specific arduino
                print("printing variable com3: ", View.COM3)

            else:
                pass



        self.root.mainloop()

    def checkPortsOnce():
        View.ports = list(serial.tools.list_ports.comports())

        for p in View.ports:
            print("port: ", p)



    def team():
        print("Team 6")

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
