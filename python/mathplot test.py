import matplotlib.pyplot as plt

temptime = [1, 2, 3, 4, 5, 6, 7]
tempvalues = [20, 17, 23, 20 , 19, 18, 22]

lighttime = [1, 2, 3, 4, 5, 6, 7]
lightvalues = [12, 8, 9, 10 , 13, 7, 10]


def redraw(xtemptime, ytempvalue, xlighttime, ylightvalue):
    a1.clear()
    a1.plot(xtemptime, ytempvalue, label='Temp')

    a2.clear()
    a2.plot(xlighttime,ylightvalue, label='Light')


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

a1.plot(temptime, tempvalues, label='Temp')
a1.legend()
a2.plot(lighttime, lightvalues, label='Light')
a2.legend()

redraw(temptime, tempvalues, lighttime, lightvalues)

plt.show()

# if you want to redraw a plot you first neet to cler the figure and then redraw the plots
