import Cell
from Cell import Celltype
# from matplotlib.animation import FuncAnimation
import csv




class Heart:
    heart = []
    rows = 49  # the resolution of the y-axis in a carthesian coordinate system
    columns = 67  # the resolution of the x-axis in a carthesian coordinate system
    # initialise the cell matrix with cells that are "no heart cells"
    # TODO: which paramters for the Cell() constructor?
    # TODO cells = [[Cell(0, 10) for y in range(self.rows)] for x in range(self.columns)]
    cells = [[Cell(0, 10) for y in range(49)] for x in range(67)]

    def __init__(self):  # constructor
        self.heart = self.init_heart()
        # TODO: these are for test purposes only

    # print("The x dimension of cells is:", len(self.cells))
    # print("The y dimension of cells is:", len(self.cells[1]))

    def init_heart(self):
        with open("heart.csv", 'r') as f:
            heart = list(csv.reader(f, delimiter=";"))

        matrix = []

        for i in range(int(self.rows)):  # loop as many times as variable rows
            r = []  # create a row list
            for j in range(int(self.columns)):  # loop as many times as variable columns
                if heart[i][j] == '0':
                    no_heart_cell = Cell(Celltype.NO_HEART_CELL)
                    r.append(no_heart_cell.get_color_state())
                elif heart[i][j] == '1':
                    right_atrium = Cell(Celltype.RIGHT_ATRIUM)
                    r.append(right_atrium.get_color_state())
                elif heart[i][j] == '2':
                    sinus_knot = Cell(1, 1)
                    r.append(Celltype.SINUS_KNOT)
                elif heart[i][j] == '3':
                    av_knot = Cell(Celltype.AV_KNOT)
                    r.append(av_knot.get_color_state())
                elif heart[i][j] == '4':
                    his_bundle = Cell(Celltype.HIS_BUNDLE)
                    r.append(his_bundle.get_color_state())
                elif heart[i][j] == '5':
                    tawara = Cell(Celltype.TAWARA)
                    r.append(tawara.get_color_state())
                elif heart[i][j] == '6':
                    purkinje = Cell(Celltype.PURKINJE)
                    r.append(purkinje.get_color_state())
                elif heart[i][j] == '7':
                    left_atrium = Cell(Celltype.LEFT_ATRIUM)
                    r.append(left_atrium.get_color_state())
                elif heart[i][j] == '8':
                    myokard = Cell(Celltype.MYOKARD)
                    r.append(myokard.get_color_state())

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
        for i in range(int(self.columns)):  # loop as many times as variable rows
            state.append([])
            for j in range(int(self.rows)):
                state[i].append(self.cells[i][j].get_state())
        return state

    def step(self):  # one step transits the heard simulation 10ms ahead
        # step all (cells except sine-knot) according to their neighbours (Moore neighbourhood)
        # TODO
        # step for sine-knot
        # TODO
        # comments Anna:
        # 1) alle Sinusknotenzellen gleichzeitig im Zeitpunkt 1 auf getriggered
        # 2) Vorhof (links und rechts) beginnt sich gleicheitig vom Sinusknoten aus zu depolarizen (isTriggered) und gibt Impuls an Nachbarzellen weiter
        #    2.1) Wenn meine Nachbarzelle depolarized ist und ich polarizable --> isTriggered
        # 3) Vorhof darf nicht His-Bündel aktivieren, sondern nur AV Knoten
        # 4) Erst wenn alle AV-Knoten Zellen vollständig geladen (depolarized) sind, dürfen Vorhofzellen (links) an benachbarte Hisbündelzellen weitergeben
        # 5) Normale Weitergabe an Nachbarzellen für Tawara und Purkinje
        # 6) Myokard darf sich erst anfangen lassen von Nachbarzellen zu aktivieren, wenn alle Purkinje Fasern auf depolarized (3) sind
        return
