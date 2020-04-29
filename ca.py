import matplotlib.pyplot as plt
import numpy as np

from matplotlib.animation import FuncAnimation


# steps for animation 10 ms (Zyklus: 0 - 200ms + 300ms Pause = 500ms gesamter Zyklus)
# Cells look to neighbour and start contracting if neighbour has reached its mV
# no-heart-cell || heart-cell

# make these smaller to increase the resolution
dx, dy = 0.05, 0.05

x = np.arange(0, 67, dx)
y = np.arange(0, 49, dy)
X, Y = np.meshgrid(x, y)

rows = 49
columns = 67
image = plt.imread("heart.png")
extent = np.min(X), np.max(X), np.min(Y), np.max(Y)

class Cell:
    state = 0
    mV = 0

    def __init__(self, state, mV):  # constructor
        self.state = state
        self.mV = mV

    def get_state(self):
        print(self.state)
        return self.state;


class Heart:
    heart = []
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

    def init_heart(self):
        matrix = []

        for i in range(int(rows)):  # loop as many times as variable rows
            r = []  # create a row list
            for j in range(int(columns)):  # loop as many times as variable columns
                if i == 13 and j >= 16 and j <= 17 or i >= 14 and i <= 15 and j >= 15 and j <= 17:
                    r.append(self.sinus_knot.get_state())
                else:
                    r.append(self.no_heart_cell.get_state())

            matrix.append(r)  # add the rows filled with columns to existing matrix list

        return matrix


heart = Heart()

# plt.clf() clears window


print(heart.heart)
plt.imshow(image, extent=extent)
plt.imshow(heart.heart, extent=extent, cmap="Reds", alpha= 0.7)
plt.title("Cellular Automata")
plt.show()