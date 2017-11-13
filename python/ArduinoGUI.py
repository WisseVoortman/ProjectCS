from tkinter import messagebox
from tkinter import *
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from Util import *

import threading
import time


class ArduinoGUI:
    def __init__(self, master, arduino):
        self.master = master
        self.frame = ttk.Frame(self.master)

        # Reference for arduino object
        self._arduino = arduino

        # verdeel het GUI scherm in 2 aparte frame 1 voor data en knoppen, de ander voor de mathplot
        self.frameone = ttk.Frame(self.frame)  # contains all the buttons and labels
        self.frametwo = ttk.Frame(self.frame)  # contains the mathplot
        self.frametree = ttk.Frame(self.frame)  # contains the toolbar for the mathplot
        self.frameone.grid(column=0, row=0, sticky='NW')  # sticks frames to the upper left corner of the root window
        self.frametwo.grid(column=1, row=0, sticky='NW')
        self.frametree.grid(column=1, row=1)

        self.toolbarboolean = FALSE  # control boolean for the toolbar rendering

        # list that will contain the data that is passed by the arduino sensors
        self.temptime = [0]
        self.tempvalue = [0]

        self.lighttime = [0]
        self.lightvalue = [0]

        # Control variables for the input fields
        self.temp = StringVar()
        self.light = StringVar()

        # start GUI
        self.id = Label(self.frameone, text="COM Port: " + self._arduino.get_port())
        self.id.grid(column=0, row=0, sticky=(W))

        self.status = Label(self.frameone, text="Huidige status: Rolled in")  # rolled in, rolled out, or rolling
        self.status.grid(column=0, row=1, sticky=(W))

        self.mode = Label(self.frameone, text="Huidige modus: Automatic")  # automatic or manual
        self.mode.grid(column=0, row=2, sticky=(W))

        self.changeMode = ttk.Button(self.frameone, text='change mode', width=25,
                                     command=self.change_mode)  # should change the mode from automatic to manual or the other way around
        self.changeMode.grid(column=0, row=3)

        self.inrollen = ttk.Button(self.frameone, text='Roll in', width=25,
                                   command=self.roll_in)  # should change the mode to manual and call roll in
        self.inrollen.grid(column=0, row=4)

        self.uitrollen = ttk.Button(self.frameone, text='Roll out', width=25,
                                    command=self.roll_out)  # should change the mode to manual and roll out
        self.uitrollen.grid(column=0, row=5)

        self.f = Figure(figsize=(7, 7), dpi=100)

        self.a1 = self.f.add_subplot(211)
        self.a1.set_ylim([0, 35])  # temp

        self.a2 = self.f.add_subplot(212)
        self.a2.set_ylim([0, 1023])  # light

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

        # self.tempceiling = ttk.Label(self.frameone, text = "Temperatuur: 50")
        # self.tempceiling.grid(column=0, row=6, sticky=(W))
        #
        # self.lightceiling = ttk.Label(self.frameone, text = "Light: 50")
        # self.lightceiling.grid(column=0, row=7, sticky=(W))
        #
        # self.temp_entry = ttk.Entry(self.frameone, width=25, textvariable=self.temp)
        # self.temp_entry.grid(column=0, row=10)
        #
        # self.templabel = Label(self.frameone, text="Temperatuur: ")  # rolled in, rolled out, or rolling
        # self.templabel.grid(column=0, row=9, sticky=(W))
        #
        # self.light_entry = ttk.Entry(self.frameone, width=25, textvariable=self.light)
        # self.light_entry.grid(column=0, row=12)

        # self.templabel = Label(self.frameone, text="Light: ")  # rolled in, rolled out, or rolling
        # self.templabel.grid(column=0, row=11, sticky=(W))

        # Temperature
        self.cur_temp = 50  # Default is 50
        self.dec_temp = ttk.Button(self.frameone, text="-2", width=5,
                                   command=self.dec_temp)
        self.dec_temp.grid(column=0, row=10)

        self.ceil_temp_label = Label(self.frameone, width=10, text="Temp: {0}".format(self.cur_temp))
        self.ceil_temp_label.grid(column=1, row=10)

        self.inc_temp = ttk.Button(self.frameone, text="+2", width=5,
                                   command=self.inc_temp)
        self.inc_temp.grid(column=2, row=10)

        # Light
        self.cur_light = 800  # Default is 800
        self.dec_light = ttk.Button(self.frameone, text="-25", width=5,
                                    command=self.dec_light)
        self.dec_light.grid(column=0, row=11)

        self.ceil_light_label = Label(self.frameone, width=10, text="Light: {0}".format(self.cur_light))
        self.ceil_light_label.grid(column=1, row=11)

        self.inc_light = ttk.Button(self.frameone, text="+25", width=5,
                                    command=self.inc_light)
        self.inc_light.grid(column=2, row=11)

        # self.setTemp = ttk.Button(self.frameone, text='Set temperatuur', width=25, command=self.setTemp)
        # self.setTemp.grid(column=1, row=10)

        # self.setLight = ttk.Button(self.frameone, text='Set temperatuur', width=25, command=self.setLight)
        # self.setLight.grid(column=1, row=12)

        self.toolbarOnOff = ttk.Button(self.frameone, text='addtoolbar', width=25, command=self.toolbarOnOff)
        self.toolbarOnOff.grid(column=0, row=13)

        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(self.f, master=self.frametwo)
        self.canvas.show()
        self.canvas.get_tk_widget().pack()

        self.canvas._tkcanvas.pack()

        for child in self.frameone.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.master.add(self.frame,
                        text="arduino")  # notebook tab label: deze moet nog even de text gewijzigd worden naar iets dynamics

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
        # self.a1.clear()                                # this commented out part somehow didnt do the trick, still havent found out why. therefore the entire mathplot frame is currently being scrapped and rerender agine.
        # self.a2.clear()
        # self.a1 = self.f.add_subplot(211)
        # self.a2 = self.f.add_subplot(212)

        # self.a1.plot(self.temptime, self.tempvalue)
        # self.a1.set_title('Temperatuur:', loc='left')
        # self.a1.set_xlabel('Tijdstip')
        # self.a1.set_ylabel('Waarde')
        # self.a1.legend()

        # self.a2.plot(self.lighttime, self.lightvalue)
        # self.a2.set_title('Licht:', loc='left')
        # self.a2.set_xlabel('Tijdstip')
        # self.a2.set_ylabel('Waarde')
        # self.a2.legend()

        print('godverdome')
        self.frametwo = ttk.Frame(self.frame)
        self.frametwo.grid(column=1, row=0)
        self.f = Figure(figsize=(7, 7), dpi=100)
        self.a1 = self.f.add_subplot(211)
        self.a2 = self.f.add_subplot(212)

        self.a1.set_ylim([0, 35])  # temp
        self.a2.set_ylim([0, 1023])  # light

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
        self.tempvalue[0] = self.tempvalue[0] + 5
        print(self.tempvalue)

    def roll_in(self):
        self._arduino.send(COMMANDS.ROLL_IN, [])

    def roll_out(self):
        self._arduino.send(COMMANDS.ROLL_OUT, [])

    def change_mode(self):
        self._arduino.send(COMMANDS.CHANGE_MODE, [])

    def inc_temp(self):
        self._arduino.send(COMMANDS.INC_TEMP, [])

    def dec_temp(self):
        self._arduino.send(COMMANDS.DEC_TEMP, [])

    def inc_light(self):
        self._arduino.send(COMMANDS.INC_LIGHT, [])

    def dec_light(self):
        self._arduino.send(COMMANDS.DEC_LIGHT, [])


    def update_labels(self):
        self.ceil_light_label.config(text="Light: {0}".format(self.cur_light))
        self.ceil_temp_label.config(text="Temp: {0}".format(self.cur_temp))

    def setTemp(self):

        try:
            templimit = int(self.temp.get())
            print(templimit)
        except:
            print('de input is niet te casten naar een int')
            messagebox.showerror('error, g', 'Dit is geen integer gast, wat denken jij?!')

    def setLight(self):
        try:
            lightlimit = int(self.light.get())
            print(lightlimit)
        except:
            print('de input is niet te casten naar int')
            messagebox.showerror('error, g', 'Dit is geen integer gast, wat denken jij?!')
