from tkinter import *
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import threading
import time


class ArduinoGUI:
    def __init__(self, master, arduino):
        self.master = master
        self.frame = ttk.Frame(self.master)

        # Reference for arduino object
        self._arduino = arduino

        # verdeel het GUI scherm in 2 aparte frame 1 voor data en knoppen, de ander voor de mathplot
        self.frameone = ttk.Frame(self.frame)
        self.frametwo = ttk.Frame(self.frame)
        self.frameone.grid(column=0, row=0)
        self.frametwo.grid(column=1, row=0)



        # hier wordt begonnen aan de daadwerkelijke GUI above was een test
        self.id = Label(self.frameone, text="ID: " + self._arduino.get_port())
        self.id.pack()



        self.mode = Label(self.frameone, text = "Huidige modus: ")
        self.mode.pack()


        self.status = Label(self.frameone, text = "Huidige status")
        self.status.pack()


        self.changeMode = ttk.Button(self.frameone, text='change mode', width=25, command=self.team)
        self.changeMode.pack()


        self.inrollen = ttk.Button(self.frameone, text='Roll in', width=25, command=self.team)
        self.inrollen.pack()


        self.uitrollen = ttk.Button(self.frameone, text='Roll out', width=25, command=self.team)
        self.uitrollen.pack()


        self.master.add(self.frame, text="arduino")  # notebook tab label: deze moet nog even de text gewijzigd worden naar iets dynamics

        temptime = [1, 2, 3, 4, 5, 6, 7]
        tempvalue = [20, 17, 23, 20, 19, 18, 22]

        lighttime = [1, 2, 3, 4, 5, 6, 7]
        lightvalue = [12, 8, 9, 10, 13, 7, 10]

        self.f = Figure(figsize=(7, 7), dpi=100)
        self.a1 = self.f.add_subplot(211)
        self.a2 = self.f.add_subplot(212)

        # plt.title("Hier is die fucking dikke title  bitch")
        # plt.ylabel('Temp Value')
        # plt.xlabel('Time ')
        # plt.legend()
        self.a1.plot(temptime, tempvalue, label='Temp')
        self.a1.set_title('Temperatuur:', loc='left')
        self.a1.set_xlabel('Tijdstip')

        self.a1.set_ylabel('Waarde')
        self.a1.legend()

        # plt.ylabel('Light Value')
        # plt.xlabel('Time ')
        self.a2.plot(lighttime, lightvalue, label='Light')
        self.a2.set_title('Licht:', loc='left')
        #self.a2.set_title()
        self.a2.set_xlabel('Tijdstip')
        self.a2.set_ylabel('Waarde')
        self.a2.legend()

        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(self.f, master=self.frametwo)
        self.canvas.show()
        self.canvas.get_tk_widget().pack()

        # code voor de toolbar van mathplot
        #toolbar = NavigationToolbar2TkAgg(self.canvas, self.frametwo) #doesnt work becahse it uses pack instead of Grid
        #toolbar.update()
        self.canvas._tkcanvas.pack()

        # Chart lists
        self.temp_list_value = []
        self.temp_list_time = []
        self.light_list_value = []
        self.light_list_time = []

    def remove(self):
        self.frame.destroy()

    # junkfunctie voor test
    def team(self):
        print("Team 6")
