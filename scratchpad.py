import time
def delay_ms(milliseconds):
    time.sleep(milliseconds / 1000)

"""
# timestamp = time.time_ns()
Replacing time.time_ns(), as time_ns() was new in python 3.7
see also: https://github.com/raysect/source/issues/303 (2020-05-11)
"""

# create initial state of visualization
#heartVis = createVisualizationMatrix(heart.heart)


# for step in frequency:
#    print(step)
# print(frequency[2])

# Show first image - which is the initial board
#im = plt.imshow(heartVis, extent=extent, cmap=cmap, alpha=0.8)

# Helper function that updates visualization -> function that FuncAnimation calls
"""
def animate(frame):
    heart.step()
    im.set_data(createVisualizationMatrix(heart.heart))
    return im
"""


# actual animation
#anim = animation.FuncAnimation(fig, animate, frames=1, interval=1)
#plt.show()

# steps for animation 10 ms (Zyklus: 0 - 200ms + 300ms Pause = 500ms gesamter Zyklus)
# Cells look to neighbour and start contracting if neighbour has reached its mV
# no-heart-cell || heart-cell

def testString(matrix):
    visualization = []

    for i in range(int(rows)):  # loop as many times as variable rows

        r = []  # create a row list

        for j in range(int(columns)):  # loop as many times as variable columns
            r.append(matrix[i][j].getState())
            if matrix[i][j].celltype == Celltype.SINUS_KNOT:
                print("is triggered") if matrix[i][j].isTriggered else print("Is not triggered")
                print(matrix[i][j].getState())

        visualization.append(r)

    for line in visualization:
        print(line)

    NeighbourIsDepolarized = False
    row = 14
    column = 19
    # neighbourhood: Moore
    north = 13 if 13 in range(len(matrix)) else row
    south = 15 if 15 in range(len(matrix)) else row
    east = 20 if 20 in range(len(matrix[row])) else column
    west = 18 if 18 in range(len(matrix[row])) else column

    # for all 8 neighbours: check if they are depolirated (if they exist)#
    if matrix[north][column].getState() == 3: NeighbourIsDepolarized = True
    print("North is", matrix[north][column].getState())
    if matrix[north][east].getState() == 3: NeighbourIsDepolarized = True
    print("North-east is", matrix[north][east].getState())
    if matrix[row][east].getState() == 3: NeighbourIsDepolarized = True
    print("East is", matrix[row][east].getState())
    if matrix[south][east].getState() == 3: NeighbourIsDepolarized = True
    print("South-East is", matrix[south][east].getState())
    if matrix[south][column].getState() == 3: NeighbourIsDepolarized = True
    print("South is", matrix[south][column].getState())
    if matrix[south][west].getState() == 3: aNeighbourIsDepolarized = True
    print("South-west is", matrix[south][west].getState())
    if matrix[row][west].getState() == 3: NeighbourIsDepolarized = True
    print("West is", matrix[row][west].getState())
    if matrix[north][west].getState() == 3: NeighbourIsDepolarized = True
    print("North-west is", matrix[north][west].getState())

    return visualization



# LOOP
#while True:
    # print( [ [1,2], [3,4] ] )
    # print(heart.test())
   # testString(heart.heart)
    #heart.step()
    #delay_ms(1000)

# print (heart.heart[0][0].stateMachine.currentState.stateName)
# test anna
# for step in frequency:
#    if(step == 10):
#        cell_test = Cell(1,-70)
#        cell_test.trigger(step)
#        print("stop")


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
"""
def test(self):
    visualization = []

    for i in range(int(self.rows)):  # loop as many times as variable rows

        r = []  # create a row list

        for j in range(int(self.columns)):  # loop as many times as variable columns
            r.append(self.heart[i][j].getState())

        visualization.append(r)

    return visualization
"""


# comments Anna:
# 1) alle Sinusknotenzellen gleichzeitig im Zeitpunkt 0 auf getriggered -> geschieht in Heart.__init__()
# 2) Vorhof (links und rechts) beginnt sich gleicheitig vom Sinusknoten aus zu depolarizen (isTriggered) und gibt Impuls an Nachbarzellen weiter
#    2.1) Wenn meine Nachbarzelle depolarized ist und ich polarizable --> isTriggered
# 3) Vorhof darf nicht His-Bündel aktivieren, sondern nur AV Knoten
# 4) Erst wenn alle AV-Knoten Zellen vollständig geladen (depolarized) sind, dürfen Vorhofzellen (links) an benachbarte Hisbündelzellen weitergeben
# 5) Normale Weitergabe an Nachbarzellen für Tawara und Purkinje
# 6) Myokard darf sich erst anfangen lassen von Nachbarzellen zu aktivieren, wenn alle Purkinje Fasern auf depolarized (3) sind


# from matplotlib.animation import FuncAnimation


# in Heart.__init__(): these are for test purposes only
# print("The x dimension of cells is:", len(self.cells))
# print("The y dimension of cells is:", len(self.cells[1]))

# Sinusknoten hat potential von -70mV zu Beginn, und über Zeit bekommt er immer mehr mV bis
# hin zu -40mV (schwellenpotential) und dann ist sein state 1

# Muskelzellen haben entweder state 0 oder 1

class Polarization:
    POLARIZED = 1  # aktivierbar - sobald nachbar aktiviert -> von 1 auf 2 in ausbreitungs_geschwindigkeit
    DEPOLARIZED = 2  # aktiviert - solange wie dauer_erregung
    REFRACTORY = 3  # refrektär - solange wie refrektaerzeit

    # potential = -70  # Startpotential
    # frequenz = 0  # Wann soll Zelle wieder beginnen potential aufzubauen
    # schwellen_potential = -40  # Wann fangt Zelle an Spannung weiterzugeben
    #ausbreitungs_geschwindigkeit = 0  # wie lange braucht Zelle von 0 bis 1
        # rechter vorhof: 13 schritte - 50 ms --> alle 4 ms
        # linker vorhof: 31 schritte - 85 ms --> alle 3 ms
        # bis AV: 17 Schritte - 50 ms --> alle 3 ms (gleich wie linker Vorhof)
        # AV Knoten: 2 Schritte - 70 ms --> 35 ms
        # His Bündel: fängt erst an, wenn alle AV Knoten zellen aktiviert sind
                    # 2 Schrotte - 5 ms --> 3 ms
        # Tawaraschenkel: 10 Schritte - 15 ms --> 2 ms
        # Purkinje Fasern: 38 Schritte - 5 ms --> zu schnell --> schrittweise mit Nachbar würd zu lang dauern
                    # sobald eine Puriknje Faser Zelle aktiviert --> alle gleichzeitig aktivieren? innerhalb 5 ms (Schritte)?
                    # bei Ausbreitung Myokard "zu viel Zeit" von dort "hernehmen" damit schrittweise auf Nachbarzelle sich ausgeht
                    # (langsamer als eigentlich wäre, aber verglichen immer noch sehr schnell)
                    # --> 1 ms
        # Myokard: 9 Schritte - 75 ms bis alles aktivert (-33 ms für Purkinje Fasern "verwendet") = 42 ms --> 5 ms
                    # Erregung beginnt erst, wenn alle Purkinje Fasern erregt sind


def trigger(self,
            time):  # time wäre index von zeitpunkt von range frequency (1000 steps zu je 10) wo gerade zelle getriggered
    # wird aufgerufen wenn Nachbarzelle aktiviert und man selbst state 1 hat; für Sinusknoten rufen wir es alle 1000ms auf.
    # only gets triggered when neighbor is triggered and cell itself is polarized (state = 1)
    # wait for time (ausbreitungs_geschwindigkeit) --> außerhalb einbauen --> zB rechter Vorhof 14 Schritte (wenn eine Ebene pro Schritt) -->
    # würde aber 140 ms statt 50 ms dauern --> ausbreitungsgeschwindigkeit = 0.3 --> beschleunigung --> oder einfach steps in 1er schritte
    self.ausbreitungs_geschwindigkeit = 0.3
    trigger = self.ausbreitungs_geschwindigkeit * 10
    start = time
    stop = start + self.dauer_erregung + self.refrektaer_zeit + 100  # + self.ausbreitungs_geschwindigkeit
    trigger_time = range(start, stop, 1)
    i = 1
    # nur wenn zustand 1 aktiviert --> sonst gleich wida beendet
    # einzige wo 1 auf 2 auf 3 wechseln
    # wenn wida in trigger function time step von letztem mal vergleichen, wieviel zeit vergangen --> zustand geändert
    # farblicher verlauf --> von e.g. 3 ms von status 1 auf 2 --> 1/3
    # zustandsänderung = refresh
    # timestamp - wann zustand betreten (step counter)
    # wieviele schritte bin ich schon in diesem zustand (altersbedingung) --> nach so und so vielen schritten ändere zustand
    # farben tabelle anzeigen der unterschiedlichen strukturen
    while (i):
        # self.state = 2 #ist schon erregt
        for step in trigger_time:
            # print(step)
            if (i == 1):
                if (step < start + trigger):
                    self.state = 1
                # innerhalb von meiner ausbreitungs_geschwindigkeit gehe ich auf 2
                elif (step >= start + trigger and step <= start + trigger + self.dauer_erregung):
                    self.state = 2
                # für dauer_erregung bin ich 2 und dann gehe ich auf 3
                elif (
                        step > start + trigger + self.dauer_erregung and step <= start + trigger + self.dauer_erregung + self.refrektaer_zeit):
                    self.state = 3
                else:
                    self.state = 1
                    i = 0
            else:
                break
        # für refrektaerzeit bin ich auf 3 und dann gehe ich wieder auf 1 und warte
        # print(self.state)