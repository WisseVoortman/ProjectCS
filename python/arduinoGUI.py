from tkinter import *
from tkinter import ttk

class arduinoGUI:
    def __init__(self, master, arduino):
        self.master = master
        self.frame = ttk.Frame(self.master)

        self.row = 0

        # Reference for arduino object
        self._arduino = arduino

        # hier wordt begonnen aan de daadwerkelijke GUI above was een test
        self.id = Label(self.frame, text="ID: " + self._arduino.get_port())
        self.id.grid(column=0, row=self.row)

        self.row = self.row + 1

        self.mode = Label(self.frame, text = "Huidige modus: ")
        self.mode.grid(column=0, row=self.row)

        self.row = self.row + 1

        self.status = Label(self.frame, text = "Huidige status")
        self.status.grid(column=0, row=self.row)

        self.row = self.row + 1

        self.changeMode = ttk.Button(self.frame, text='change mode', width=25, command=arduinoGUI.team) # bij command kunnen functies worden aangeroepen  uit de controller of gewoon deze file
        self.changeMode.grid(column=0, row=self.row)

        self.row = self.row + 1

        self.inrollen = ttk.Button(self.frame, text='Roll in', width=25, command=arduinoGUI.team)
        self.inrollen.grid(column=0, row=self.row)

        self.row = self.row + 1

        self.uitrollen = ttk.Button(self.frame, text='Roll out', width=25, command=arduinoGUI.team)
        self.uitrollen.grid(column=0, row=self.row)

        self.row = self.row + 1

        self.master.add(self.frame, text="arduino") # deze moet nog even de text gewijzigd worden naar iets dynamics

    # junkfunctie voor test
    def team():
        print("Team 6")


