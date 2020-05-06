class Celltype:
    NO_HEART_CELL = 0
    RIGHT_ATRIUM = 1
    SINUS_KNOT = 2
    AV_KNOT = 3
    HIS_BUNDLE = 4
    TAWARA = 5
    PURKINJE = 6
    LEFT_ATRIUM = 7
    MYOKARD = 8


class Cell:
    color_state_polarized = {  # aktivierbar
        Celltype.NO_HEART_CELL: 0,
        Celltype.RIGHT_ATRIUM: 4,
        Celltype.LEFT_ATRIUM: 3,
        Celltype.SINUS_KNOT: 1,
        Celltype.MYOKARD: 5,
        Celltype.PURKINJE: 1,
        Celltype.TAWARA: 2,
        Celltype.HIS_BUNDLE: 3,
        Celltype.AV_KNOT: 4
    }
    color_state_depolarized = {  # aktiviert
        Celltype.NO_HEART_CELL: 0,
        Celltype.RIGHT_ATRIUM: 4,
        Celltype.LEFT_ATRIUM: 3,
        Celltype.SINUS_KNOT: 1,
        Celltype.MYOKARD: 5,
        Celltype.PURKINJE: 1,
        Celltype.TAWARA: 2,
        Celltype.HIS_BUNDLE: 3,
        Celltype.AV_KNOT: 4
    }
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

    dauer_erregung = 200  # für alle Zellen gleich 20 Zeiteinheiten (200 ms)
    refrektaer_zeit = 300  # für alle Zellen gleich 30 Zeiteinheiten (300ms)
    ausbreitungs_geschwindigkeit = {
        Celltype.NO_HEART_CELL: 0,
        Celltype.RIGHT_ATRIUM: 4,
        Celltype.LEFT_ATRIUM: 3,
        Celltype.SINUS_KNOT: 1,
        Celltype.MYOKARD: 5,
        Celltype.PURKINJE: 1,
        Celltype.TAWARA: 2,
        Celltype.HIS_BUNDLE: 3,
        Celltype.AV_KNOT: 35
    }

    # Sinusknoten hat potential von -70mV zu Beginn, und über Zeit bekommt er immer mehr mV bis
    # hin zu -40mV (schwellenpotential) und dann ist sein state 1

    # Muskelzellen haben entweder state 0 oder 1

    class Polarization:
        POLARIZED = 1  # aktivierbar - sobald nachbar aktiviert -> von 1 auf 2 in ausbreitungs_geschwindigkeit
        DEPOLARIZED = 2  # aktiviert - solange wie dauer_erregung
        REFRACTORY = 3  # refrektär - solange wie refrektaerzeit

    def __init__(self, cell_type):  # constructor
        self.cell_type = cell_type
        self.ausbreitungs_geschwindigkeit[cell_type]

    def get_color_state(self):
        # print(self.state)
        return self.color_state_polarized[self.cell_type]

    def trigger(self,time): #time wäre index von zeitpunkt von range frequency (1000 steps zu je 10) wo gerade zelle getriggered
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
        #nur wenn zustand 1 aktiviert --> sonst gleich wida beendet
        #einzige wo 1 auf 2 auf 3 wechseln
        #wenn wida in trigger function time step von letztem mal vergleichen, wieviel zeit vergangen --> zustand geändert
        #farblicher verlauf --> von e.g. 3 ms von status 1 auf 2 --> 1/3
        #zustandsänderung = refresh
        #timestamp - wann zustand betreten (step counter)
        #wieviele schritte bin ich schon in diesem zustand (altersbedingung) --> nach so und so vielen schritten ändere zustand
        #farben tabelle anzeigen der unterschiedlichen strukturen
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
