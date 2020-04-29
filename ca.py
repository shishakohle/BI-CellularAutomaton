import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# steps for animation 10 ms (Zyklus: 0 - 200ms + 300ms Pause = 500ms gesamter Zyklus)
# Cells look to neighbour and start contracting if neighbour has reached its mV
# no-heart-cell || heart-cell

rows = 12
columns = 5


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

    def __init__(self):  # constructor
        self.heart = self.init_heart()

    def init_heart(self):
        matrix = []

        for i in range(int(rows)):  # loop as many times as variable rows
            r = []  # create a row list
            for j in range(int(columns)):  # loop as many times as variable columns
                if i == 0 and j == 2:
                    r.append(self.heart_cell.get_state())
                elif i == 1 and j == 1:
                    r.append(self.heart_cell.get_state())
                elif i == 1 and j == 2:
                    r.append(self.heart_cell.get_state())
                elif i == 1 and j == 3:
                    r.append(self.heart_cell.get_state())
                elif i > 1 and j == 0:
                    r.append(self.heart_cell.get_state())
                elif i > 1 and j == 2:
                    r.append(self.heart_cell.get_state())
                elif i > 1 and j == 4:
                    r.append(self.heart_cell.get_state())
                elif i == 11 and j == 1:
                    r.append(self.heart_cell.get_state())
                elif i == 11 and j == 3:
                    r.append(self.heart_cell.get_state())
                else:
                    r.append(self.no_heart_cell.get_state())

            matrix.append(r)  # add the rows filled with columns to existing matrix list

        return matrix


heart = Heart()

# plt.clf() clears window

print(heart.heart)
plt.imshow(heart.heart, cmap="Reds")
plt.title("Cellular Automata")
plt.show()