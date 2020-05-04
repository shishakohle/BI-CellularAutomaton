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
