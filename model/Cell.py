from model.FiniteStateMachine import *

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
    TEST = 9


class Cell:
    color_state_polarized = {  # aktivierbar
        Celltype.NO_HEART_CELL: 7,
        Celltype.RIGHT_ATRIUM: 8,
        Celltype.LEFT_ATRIUM: 8,
        Celltype.SINUS_KNOT: 10,
        Celltype.MYOKARD: 8,
        Celltype.PURKINJE: 5,
        Celltype.TAWARA: 3,
        Celltype.HIS_BUNDLE: 1,
        Celltype.AV_KNOT: 12,
    }
    color_state_depolarized = {  # aktiviert
        Celltype.NO_HEART_CELL: 7,
        Celltype.RIGHT_ATRIUM: 9,
        Celltype.LEFT_ATRIUM: 9,
        Celltype.SINUS_KNOT: 11,
        Celltype.MYOKARD: 9,
        Celltype.PURKINJE: 6,
        Celltype.TAWARA: 4,
        Celltype.HIS_BUNDLE: 2,
        Celltype.AV_KNOT: 0,
    }

    dauer_erregung = 200  # für alle Zellen gleich 20 Zeiteinheiten (200 ms)
    refrektaer_zeit = 300  # für alle Zellen gleich 30 Zeiteinheiten (300ms)
    testCount = 0
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

    def __init__(self, celltype):  # constructor
        self.celltype = celltype
        self.stateMachine = FiniteStateMachine(self.ausbreitungs_geschwindigkeit[self.celltype],
                                               self.dauer_erregung, self.refrektaer_zeit)
        self.isTriggered = False
        self.stepCount = 0

    def trigger(self):
        self.isTriggered = True

    def step(self):
        self.stepCount += 1
        self.stateMachine.refreshState(self.stepCount, self.isTriggered)
        self.isTriggered = False  # reset depolarization trigger

    def getState(self):
        return self.stateMachine.currentState.stateName

    def get_color_state(self):
        if self.getState() == 3:
            return self.color_state_depolarized[self.celltype]
        else:
            return self.color_state_polarized[self.celltype]
