import matplotlib.pyplot as plt

temptime = [1, 2, 3, 4, 5, 6, 7]
tempvalues = [20, 17, 23, 20 , 19, 18, 22]

lighttime = [1, 2, 3, 4, 5, 6, 7]
lightvalues = [12, 8, 9, 10 , 13, 7, 10]

temptime2 = [1, 2, 3, 4, 5, 6, 7]
tempvalues2 = [30, 27, 33, 30 , 29, 28, 32]

lighttime2 = [1, 2, 3, 4, 5, 6, 7]
lightvalues2 = [22, 18, 19, 20 , 23, 17, 20]

global fig

global a1
global a2

def draw(xtemptime, ytempvalue, xlighttime, ylightvalue):
    global fig
    global a1
    global a2
    fig = plt.figure()

    #                   (width height plotnumber)
    a1 = fig.add_subplot(211)
    plt.title("Hier is die fucking dikke title  bitch")
    plt.ylabel('Temp Value')
    plt.xlabel('Time ')
    plt.legend()
    a2 = fig.add_subplot(212)
    plt.ylabel('Light Value')
    plt.xlabel('Time ')

    a1.plot(xtemptime, ytempvalue, label='Temp')
    a1.legend()
    a2.plot(xlighttime, ylightvalue, label='Light')
    a2.legend()

def redraw(xtemptime, ytempvalue, xlighttime, ylightvalue):
    global a1
    global a2

    a1.clear()
    a2.clear()

    a1 = fig.add_subplot(211)
    plt.title("Hier is die fucking dikke title  bitch")
    plt.ylabel('Temp Value')
    plt.xlabel('Time ')
    plt.legend()
    a2 = fig.add_subplot(212)
    plt.ylabel('Light Value')
    plt.xlabel('Time ')

    a1.plot(xtemptime, ytempvalue, label='Temp')
    a1.legend()
    a2.plot(xlighttime, ylightvalue, label='Light')
    a2.legend()



draw(temptime, tempvalues, lighttime, lightvalues)
redraw(temptime2, tempvalues2, lighttime2, lightvalues2)
plt.show()
# if you want to redraw a plot you first neet to cler the figure and then redraw the plots
