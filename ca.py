import matplotlib.pyplot as plt
import numpy as np
# from matplotlib.animation import FuncAnimation


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


class Cell:
    state = 0
    mV = 0

    def __init__(self, state, mV):  # constructor
        self.state = state
        self.mV = mV

    def get_state(self):
        # print(self.state)
        return self.state;


class Heart:
    heart = []
    # initialise the cell matrix with cells that are "no heart cells"
    # TODO: which paramters for the Cell() constructor?
    cells = [[Cell(0,10) for y in range(rows)] for x in range(columns)]

    # define cell types
    heart_cell = Cell(1, 30)
    no_heart_cell = Cell(0, 10)
    muscle_cell = Cell(1, 10)
    sinus_knot = Cell(1, 10)
    av_knot = Cell(1, 10)
    his_bundle = Cell(1, 10)
    tawara = Cell(1, 10)
    purkinje = Cell(1, 10)

    def __init__(self):  # constructor
        self.heart = self.init_heart()
        # TODO: these are for test purposes only
        print("The x dimension of cells is:", len(self.cells))
        print("The y dimension of cells is:", len(self.cells[1]))

    def init_heart(self):
        matrix = []

        for i in range(int(rows)):  # loop as many times as variable rows
            r = []  # create a row list
            for j in range(int(columns)):  # loop as many times as variable columns
                if i == 13 and j >= 16 and j <= 17 or i >= 14 and i <= 15 and j >= 15 and j <= 17:
                    r.append(self.sinus_knot.get_state())
                else:
                    r.append(self.no_heart_cell.get_state()) # TODO: cells must be copied, not referenced

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

#print(heart.heart)
plt.imshow(image, extent=extent)
plt.imshow(heart.heart, extent=extent, cmap="Reds", alpha= 0.7)
#plt.imshow(heart.getState(), extent=extent, cmap="Reds", alpha= 0.7)
plt.title("Cellular Automata of the Heart")
# TODO: remove axis labels
plt.show()
