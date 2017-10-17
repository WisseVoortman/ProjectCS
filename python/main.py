from tkinter import *
from tkinter import ttk
import serial.tools.list_ports
import time
from ArduinoGUI import *
from PyCtrl import PyCtrl


class mainView:
    def __init__(self, master):
        """Initialize the main Program View.
        """
        self.ports = list(serial.tools.list_ports.comports())
        self.master = master  # initialize Root window
        self.master.title('Centrale Project 2.1 - Computer System ')  # set title for Root window
        self.master.geometry("800x500+200+200")  # set size and location for Root window
        self.mainframe = ttk.Notebook(self.master, padding="0 0 0 0")  # left top right bottem    create mainframe in Root winow
        self.mainframe.grid(column=0, row=0, sticky=(N, W, S, E))  # set mainframe to root windows size

        menubar = Menu(self.master)  # create a menubar

        # create a pulldown menu "FILE", and add it to the menu bar
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Team", command=mainView.team)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="Commands", menu=filemenu)  # se the label in the menubar

        # display the menu
        self.master.config(menu=menubar)

        #label = Label(self.mainframe, text="Hieronder de control units: ", bg='red')
        #label.pack()

        # for element in list of arduino's (het is handig om dit mogelijk met een functie te doen zodat je die ook later kan aanroepen)
        self.views = {}  # Empty dict
        self.pyctrl = PyCtrl(self)
        self.pyctrl.start()
        #ArduinoGUI(self.mainframe)
        #ArduinoGUI(self.mainframe)


    def team():
        print("Team 6")

    def quit(self):
        self.pyctrl.stop()  # Will automatically stop all arduinos
        self.master.quit()
# END OF class: Mainview--------------------------------------------------------------------------


def main():
    root = Tk()
    mainView(root)
    root.mainloop()

main()

