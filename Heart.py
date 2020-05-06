from Cell import Cell
from Cell import Celltype
import csv


class Heart:
    def __init__(self):  # constructor
        # TODO read count of rows and columns from CSV directly
        self.rows = 49  # the resolution of the y-axis in a carthesian coordinate system
        self.columns = 67  # the resolution of the x-axis in a carthesian coordinate system
        self.heart = self.init_matrix()

    def init_matrix(self):
        matrix = []

        with open("heart.csv", 'r') as f:  # TODO filename as function argument
            heart = list(csv.reader(f, delimiter=";"))  # TODO check: what if open() has failed for some reason?

        # TODO read count of rows and columns from CSV directly

        for i in range(int(self.rows)):  # loop as many times as variable rows

            r = []  # create a row list

            for j in range(int(self.columns)):  # loop as many times as variable columns

                # TODO replace the if-elif tree by a switcher. Such a switcher already exists in Cell.
                if heart[i][j] == '0':
                    no_heart_cell = Cell(Celltype.NO_HEART_CELL)
                    r.append(no_heart_cell.get_color_state())
                elif heart[i][j] == '1':
                    right_atrium = Cell(Celltype.RIGHT_ATRIUM)
                    r.append(right_atrium.get_color_state())
                elif heart[i][j] == '2':
                    sinus_knot = Cell(Celltype.SINUS_KNOT)
                    r.append(sinus_knot.get_color_state())
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

    def placeCell(self, cell, x, y):
        # TODO: check x and y for validity (IndexError: list index out of range)
        self.cells[x][y] = cell  # TODO: some of the cells must be "copied", not referenced!
        return

    # TODO: Frage von Ingo: Benötigen wir diese funktion noch?
    def getState(self):  # returns a matrix that indicates the current state of each heart cell
        state = []
        for i in range(int(self.columns)):  # loop as many times as variable rows
            state.append([])
            for j in range(int(self.rows)):
                state[i].append(self.cells[i][j].get_state())
        return state

    def step(self):  # one step transits the heart simulation 1 millisecond ahead
        # step all (cells except sine-knot) according to their neighbours (Moore neighbourhood)
        # TODO
        # step for sine-knot
        # TODO
        # comments Anna:
        # 1) alle Sinusknotenzellen gleichzeitig im Zeitpunkt 0 auf getriggered
        # 2) Vorhof (links und rechts) beginnt sich gleicheitig vom Sinusknoten aus zu depolarizen (isTriggered) und gibt Impuls an Nachbarzellen weiter
        #    2.1) Wenn meine Nachbarzelle depolarized ist und ich polarizable --> isTriggered
        # 3) Vorhof darf nicht His-Bündel aktivieren, sondern nur AV Knoten
        # 4) Erst wenn alle AV-Knoten Zellen vollständig geladen (depolarized) sind, dürfen Vorhofzellen (links) an benachbarte Hisbündelzellen weitergeben
        # 5) Normale Weitergabe an Nachbarzellen für Tawara und Purkinje
        # 6) Myokard darf sich erst anfangen lassen von Nachbarzellen zu aktivieren, wenn alle Purkinje Fasern auf depolarized (3) sind
        return
