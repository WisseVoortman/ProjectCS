from tkinter import *
from tkinter import ttk

class arduinoGUI:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(self.master)

        self.label1 = Label(self.frame, text="arduino GUI: ", bg='red')
        self.label1.grid(column=0, row=0)

        self.button1 = ttk.Button(self.frame, text='Geile button', width=25, command=self.team)
        self.button1.grid(column=0, row=1)

        # hier wordt begonnen aan de daadwerkelijke GUI above was een test
        self.mode = Label(self.frame, text = "Huidige modus: ")
        self.status = Label(self.frame, text = "Huidige status")
        self.changeMode = ttk.Button(self.frame, text='change mode', width=25, command=self.team) # bij command kunnen functies worden aangeroepen  uit de controller of gewoon deze file
        self.inrollen = ttk.Button(self.frame, text='Roll in', width=25, command=self.team)
        self.uitrollen = ttk.Button(self.frame, text='Roll out', width=25, command=self.team)

        self.frame.pack() # hier word de arudinoGUI aan de mainframe toegevoegd

    # junkfunctie voor test
    def team():
        print("Team 6")


