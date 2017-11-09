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
        self.frametree = ttk.Frame(self.frame)
        self.frameone.grid(column=0, row=0)
        self.frametwo.grid(column=1, row=0)
        self.frametree.grid(column=1, row=1)

        self.toolbarboolean = FALSE

        self.temptime = [1, 2, 3, 4, 5, 6, 7]
        self.tempvalue = [20, 17, 23, 20, 19, 18, 22]

        self.lighttime = [1, 2, 3, 4, 5, 6, 7]
        self.lightvalue = [12, 8, 9, 10, 13, 7, 10]

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



        self.master.add(self.frame, text="arduino")  # notebook tab label: deze moet nog even de text gewijzigd worden naar iets dynamics moet mogelijk naar beneden verhuist worden.

        self.f = Figure(figsize=(7, 7), dpi=100)
        self.a1 = self.f.add_subplot(211)
        self.a2 = self.f.add_subplot(212)

        self.a1.plot(self.temptime, self.tempvalue, label='Temp')
        self.a1.set_title('Temperatuur:', loc='left')
        self.a1.set_xlabel('Tijdstip')

        self.a1.set_ylabel('Waarde')
        self.a1.legend()

        self.a2.plot(self.lighttime, self.lightvalue, label='Light')
        self.a2.set_title('Licht:', loc='left')

        self.a2.set_xlabel('Tijdstip')
        self.a2.set_ylabel('Waarde')
        self.a2.legend()

        self.moddata = ttk.Button(self.frameone, text='mod data', width=25, command = self.modifydata)
        self.moddata.pack()

        self.redrawtestbutton = ttk.Button(self.frameone, text='redraw testen', width=25,
                                     command=self.redraw)
        self.redrawtestbutton.pack()

        self.toolbarOnOff = ttk.Button(self.frameone, text='addtoolbar', width=25, command = self.toolbarOnOff)
        self.toolbarOnOff.pack()

        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(self.f, master=self.frametwo)
        self.canvas.show()
        self.canvas.get_tk_widget().pack()

        # code voor de toolbar van mathplot
        #self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.frametwo) #doesnt work becahse it uses pack instead of Grid
        #self.toolbar.update()
        self.canvas._tkcanvas.pack()

    def remove(self):
        self.frame.destroy()

    def toolbarOnOff(self):
        if self.toolbarboolean == FALSE:
            self.toolbarboolean = TRUE
            self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.frametree)
            self.toolbar.update()
        elif self.toolbarboolean == TRUE:
            self.toolbarboolean = FALSE
            self.toolbar.destroy()


    # junkfunctie voor test
    def team(self):
        print("Team 6")

    def redraw(self):
        #self.frametwo.destroy()
        #self.a1.clear()
        #self.a1.redraw_in_frame()
        #self.a2.redraw_in_frame()

        #self.a1 = self.f.add_subplot(211)
        #self.a2 = self.f.add_subplot(212)

        #self.a1.plot(self.temptime, self.tempvalue)
        #self.a1.set_title('Temperatuur:', loc='left')
        #self.a1.set_xlabel('Tijdstip')
        #self.a1.set_ylabel('Waarde')
        #self.a1.legend()

        #self.a2.plot(self.lighttime, self.lightvalue)
        #self.a2.set_title('Licht:', loc='left')
        #self.a2.set_xlabel('Tijdstip')
        #self.a2.set_ylabel('Waarde')
        #self.a2.legend()

        print('godverdome')
        self.frametwo = ttk.Frame(self.frame)
        self.frametwo.grid(column=1, row=0)
        self.f = Figure(figsize=(7, 7), dpi=100)
        self.a1 = self.f.add_subplot(211)
        self.a2 = self.f.add_subplot(212)

        self.a1.plot(self.temptime, self.tempvalue, label='Temp')
        self.a1.set_title('Temperatuur:', loc='left')
        self.a1.set_xlabel('Tijdstip')

        self.a1.set_ylabel('Waarde')
        self.a1.legend()

        self.a2.plot(self.lighttime, self.lightvalue, label='Light')
        self.a2.set_title('Licht:', loc='left')

        self.a2.set_xlabel('Tijdstip')
        self.a2.set_ylabel('Waarde')
        self.a2.legend()

        self.canvas = FigureCanvasTkAgg(self.f, master=self.frametwo)
        self.canvas.show()
        self.canvas.get_tk_widget().pack()

        self.canvas._tkcanvas.pack()

    def modifydata(self):
        #self.temptime = self.temptime + 5
        self.tempvalue[0] = self.tempvalue[0] + 5
        #self.lighttime = self.lighttime + 5
        #self.lightvalue = self.lightvalue + 5
        print(self.tempvalue)


