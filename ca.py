import matplotlib.pyplot as plt
import numpy as np
# from matplotlib.animation import FuncAnimation
import csv

# steps for animation 10 ms (Zyklus: 0 - 200ms + 300ms Pause = 500ms gesamter Zyklus)
# Cells look to neighbour and start contracting if neighbour has reached its mV
# no-heart-cell || heart-cell

# scale image and matrix
dx, dy = 0.05, 0.05
x = np.arange(0, 67, dx)
y = np.arange(0, 49, dy)
X, Y = np.meshgrid(x, y)
extent = np.min(X), np.max(X), np.min(Y), np.max(Y)

rows = 49  # the resolution of the y-axis in a carthesian coordinate system
columns = 67  # the resolution of the x-axis in a carthesian coordinate system
image = plt.imread("heart.png")

frequency = range(0, 1000, 10)
#for step in frequency:
#    print(step)
#print(frequency[2])

class Cell:
    state = 0 # aktiviert, refrektär oder aktivierbar
    # potential = -70  # Startpotential
    # frequenz = 0  # Wann soll Zelle wieder beginnen potential aufzubauen
    # schwellen_potential = -40  # Wann fangt Zelle an Spannung weiterzugeben
    ausbreitungs_geschwindigkeit = 0  # wie lange braucht Zelle von 0 bis 1
    dauer_erregung = 200  # für alle Zellen gleich 20 Zeiteinheiten (200 ms)
    refrektaer_zeit = 300  # für alle Zellen gleich 30 Zeiteinheiten (300ms)

    # Sinusknoten hat potential von -70mV zu Beginn, und über Zeit bekommt er immer mehr mV bis
    # hin zu -40mV (schwellenpotential) und dann ist sein state 1

    # Muskelzellen haben entweder state 0 oder 1

    class Polarization:
        POLARIZED = 1  # aktivierbar - sobald nachbar aktiviert -> von 1 auf 2 in ausbreitungs_geschwindigkeit
        DEPOLARIZED = 2  # aktiviert - solange wie dauer_erregung
        REFRACTORY = 3  # refrektär - solange wie refrektaerzeit

    def __init__(self, state, mV):  # constructor
        self.state = state
        self.mV = mV

    def get_state(self):
        # print(self.state)
        return self.state


    def trigger(self,time):  #time wäre index von zeitpunkt von range frequency (1000 steps zu je 10) wo gerade zelle getriggered
        # wird aufgerufen wenn Nachbarzelle aktiviert und man selbst state 1 hat; für Sinusknoten rufen wir es alle 1000ms auf.
        # only gets triggered when neighbor is triggered and cell itself is polarized (state = 1)
        # wait for time (ausbreitungs_geschwindigkeit) --> außerhalb einbauen --> zB rechter Vorhof 14 Schritte (wenn eine Ebene pro Schritt) -->
        # würde aber 140 ms statt 50 ms dauern --> ausbreitungsgeschwindigkeit = 0.3 --> beschleunigung --> oder einfach steps in 1er schritte
        self.ausbreitungs_geschwindigkeit = 0.3
        trigger = self.ausbreitungs_geschwindigkeit * 10
        start = time
        stop = start +self.dauer_erregung+self.refrektaer_zeit + 100#+ self.ausbreitungs_geschwindigkeit
        trigger_time = range(start,stop,1)
        i = 1

        while(i):
        #self.state = 2 #ist schon erregt
            for step in trigger_time:
                #print(step)
                if(i == 1):
                    if(step < start + trigger):
                        self.state = 1
            # innerhalb von meiner ausbreitungs_geschwindigkeit gehe ich auf 2
                    elif(step >= start + trigger and step <= start + trigger+self.dauer_erregung):
                        self.state = 2
            # für dauer_erregung bin ich 2 und dann gehe ich auf 3
                    elif (step > start + trigger+self.dauer_erregung and step <= start + trigger+self.dauer_erregung+self.refrektaer_zeit):
                        self.state = 3
                    else:
                        self.state = 1
                        i = 0
                else:
                    break
            # für refrektaerzeit bin ich auf 3 und dann gehe ich wieder auf 1 und warte
                #print(self.state)

class Heart:
    heart = []
    # initialise the cell matrix with cells that are "no heart cells"
    # TODO: which paramters for the Cell() constructor?
    cells = [[Cell(0,10) for y in range(rows)] for x in range(columns)]

    def __init__(self):  # constructor
        self.heart = self.init_heart()
        # TODO: these are for test purposes only
       # print("The x dimension of cells is:", len(self.cells))
        #print("The y dimension of cells is:", len(self.cells[1]))

    def init_heart(self):
        with open("heart.csv", 'r') as f:
            heart = list(csv.reader(f, delimiter=";"))

        matrix = []

        for i in range(int(rows)):  # loop as many times as variable rows
            r = []  # create a row list
            for j in range(int(columns)):  # loop as many times as variable columns
                if heart[i][j] == '0':
                    no_heart_cell = Cell(0, 10)
                    r.append(no_heart_cell.get_state())
                elif heart[i][j] == '1':
                    muscle_cell = Cell(1, 10)
                    r.append(muscle_cell.get_state())
                elif heart[i][j] == '2':
                    sinus_knot = Cell(1, 10)
                    r.append(sinus_knot.get_state())
                elif heart[i][j] == '3':
                    av_knot = Cell(1, 10)
                    r.append(av_knot.get_state())
                elif heart[i][j] == '4':
                    his_bundle = Cell(1, 10)
                    r.append(his_bundle.get_state())
                elif heart[i][j] == '5':
                    tawara = Cell(1, 10)
                    r.append(tawara.get_state())
                elif heart[i][j] == '6':
                    purkinje = Cell(1, 10)
                    r.append(purkinje.get_state())

            matrix.append(r)  # add the rows filled with columns to existing matrix list

        return matrix

    def init(self):
        # TODO: Here, use self.placeCell() to create the heart cell matrix
        return

    def placeCell(self, cell, x, y):
        # TODO: check x and y for validity (IndexError: list index out of range)
        self.cells[x][y] = cell  # TODO: some of the cells must be "copied", not referenced!
        return

    def getState(self):
        state = []
        for i in range(int(columns)):  # loop as many times as variable rows
            state.append([])
            for j in range(int(rows)):
                state[i].append(self.cells[i][j].get_state())
        return state

    def step(self):  # one step transits the heard simulation 10ms ahead
        # step all (cells except sine-knot) according to their neighbours (Moore neighbourhood)
        # TODO
        # step for sine-knot
        # TODO
        return


heart = Heart()

# plt.clf() clears window

plt.imshow(image, extent=extent)
plt.imshow(heart.heart, extent=extent, cmap="Reds", alpha= 0.7)
#plt.imshow(heart.getState(), extent=extent, cmap="Reds", alpha= 0.7)
plt.title("Cellular Automata of the Heart")
# TODO: remove axis labels
plt.show()

#test anna
#for step in frequency:
#    if(step == 10):
#        cell_test = Cell(1,-70)
#        cell_test.trigger(step)
#        print("stop")
