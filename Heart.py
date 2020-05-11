from Cell import *
# from Cell import Celltype
import csv


class Heart:
    def __init__(self):  # constructor
        # TODO read count of rows and columns from CSV directly
        self.rows = 49  # the resolution of the y-axis in a carthesian coordinate system
        self.columns = 67  # the resolution of the x-axis in a carthesian coordinate system
        self.heart = self.init_matrix()
        # self.visualization = self.createVisualizationMatrix(self.heart)

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
                    r.append(no_heart_cell)
                elif heart[i][j] == '1':
                    right_atrium = Cell(Celltype.RIGHT_ATRIUM)
                    r.append(right_atrium)
                elif heart[i][j] == '2':
                    sinus_knot = Cell(Celltype.SINUS_KNOT)
                    sinus_knot.trigger()  # sine knot immediately triggered.
                    r.append(sinus_knot)
                elif heart[i][j] == '3':
                    av_knot = Cell(Celltype.AV_KNOT)
                    r.append(av_knot)
                elif heart[i][j] == '4':
                    his_bundle = Cell(Celltype.HIS_BUNDLE)
                    r.append(his_bundle)
                elif heart[i][j] == '5':
                    tawara = Cell(Celltype.TAWARA)
                    r.append(tawara)
                elif heart[i][j] == '6':
                    purkinje = Cell(Celltype.PURKINJE)
                    r.append(purkinje)
                elif heart[i][j] == '7':
                    left_atrium = Cell(Celltype.LEFT_ATRIUM)
                    r.append(left_atrium)
                elif heart[i][j] == '8':
                    myokard = Cell(Celltype.MYOKARD)
                    r.append(myokard)

            matrix.append(r)  # add the rows filled with columns to existing matrix list

        return matrix

    """
    def toString(self):
        stringMatrix = []
        for row in range(len(self.heart),1):
            r = []
            for column in range(0,len(self.heart[row]),1):
                r.append(self.heart[row][column].getState())
            stringMatrix.append(r)
        return stringMatrix
    """

    def test(self):
        visualization = []

        for i in range(int(self.rows)):  # loop as many times as variable rows

            r = []  # create a row list

            for j in range(int(self.columns)):  # loop as many times as variable columns
                r.append(self.heart[i][j].getState())

            visualization.append(r)

        return visualization

    def step(self):  # one step transits the heart simulation 1 time step ahead
        # comments Anna:
        # 1) alle Sinusknotenzellen gleichzeitig im Zeitpunkt 0 auf getriggered -> geschieht in Heart.__init__()
        # 2) Vorhof (links und rechts) beginnt sich gleicheitig vom Sinusknoten aus zu depolarizen (isTriggered) und gibt Impuls an Nachbarzellen weiter
        #    2.1) Wenn meine Nachbarzelle depolarized ist und ich polarizable --> isTriggered
        # 3) Vorhof darf nicht His-Bündel aktivieren, sondern nur AV Knoten
        # 4) Erst wenn alle AV-Knoten Zellen vollständig geladen (depolarized) sind, dürfen Vorhofzellen (links) an benachbarte Hisbündelzellen weitergeben
        # 5) Normale Weitergabe an Nachbarzellen für Tawara und Purkinje
        # 6) Myokard darf sich erst anfangen lassen von Nachbarzellen zu aktivieren, wenn alle Purkinje Fasern auf depolarized (3) sind

        for row in range(0,len(self.heart),1):
            for column in range(0,len(self.heart[row]),1):

                if self.heart[row][column].celltype == Celltype.HIS_BUNDLE:
                    # trigger if: (1) all AV knots are depolarized and (2) neighbourhood contains an depolarized cell
                    if self.allDepolarized(Celltype.AV_KNOT) and self.aNeighbourIsDepolarized(row, column):
                        self.heart[row][column].trigger()

                elif self.heart[row][column].celltype == Celltype.MYOKARD:
                    # trigger if all Purkinje Fibres are depolarized
                    if self.allDepolarized(Celltype.PURKINJE):
                        self.heart[row][column].trigger()

                else:
                    # trigger if neighbourhood contains an depolarized cell
                    if self.aNeighbourIsDepolarized(row, column):
                        self.heart[row][column].trigger()

                self.heart[row][column].step()

    def aNeighbourIsDepolarized(self, row, column):
        aNeighbourIsDepolarized = False

        # neighbourhood: Moore
        north = row-1 if row-1 in range(0, 1, len(self.heart)) else row
        south = row + 1 if row + 1 in range(0, 1, len(self.heart)) else row
        east = column + 1 if column + 1 in range(0, 1, len(self.heart[row])) else column
        west = column - 1 if column - 1 in range(0, 1, len(self.heart[row])) else column

        # for all 8 neighbours: check if they are depolirated (if they exist)#
        if self.heart[north][column].getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True
        if self.heart[north][east].getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True
        if self.heart[row][east].getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True
        if self.heart[south][east].getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True
        if self.heart[south][column].getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True
        if self.heart[south][west].getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True
        if self.heart[row][west].getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True
        if self.heart[north][west].getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True

        return aNeighbourIsDepolarized

    def allDepolarized(self, cellytpe):
        allDepolarized = True

        for row in range(0,len(self.heart),1):
            for column in range(0,len(self.heart[row]),1):

                if self.heart[row][column].celltype == cellytpe:
                    if self.heart[row][column].getState() != StateName.DEPOLARIZED: allDepolarized = False

        return allDepolarized
