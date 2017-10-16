from tkinter import *
from tkinter import ttk

class arduinoGUI:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(self.master)

        self.label1 = Label(self.frame, text="arduino GUI: ", bg='red')
        self.label1.grid(column=0, row=0)

        self.button1 = ttk.Button(self.frame, text='New Window', width=25, command=self.team)
        self.button1.grid(column=0, row=1)

        self.frame.pack()

    def team():
        print("Team 6")


