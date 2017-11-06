from tkinter import *
from tkinter import ttk
import threading
import time


class ArduinoGUI:
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

        self.changeMode = ttk.Button(self.frame, text='change mode', width=25, command=self.team)
        self.changeMode.grid(column=0, row=self.row)

        self.row = self.row + 1

        self.inrollen = ttk.Button(self.frame, text='Roll in', width=25, command=self.team)
        self.inrollen.grid(column=0, row=self.row)

        self.row = self.row + 1

        self.uitrollen = ttk.Button(self.frame, text='Roll out', width=25, command=self.team)
        self.uitrollen.grid(column=0, row=self.row)

        self.row = self.row + 1

        self.master.add(self.frame, text="arduino")  # deze moet nog even de text gewijzigd worden naar iets dynamics

        # Chart lists
        temp_list_value = []
        temp_list_time = []
        light_list_value = []
        light_list_time = []

    def remove(self):
        self.frame.destroy()

    # junkfunctie voor test
    def team(self):
        print("Team 6")
