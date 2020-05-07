from FiniteStateMachine import *

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
        Celltype.RIGHT_ATRIUM: 1,
        Celltype.LEFT_ATRIUM: 1,
        Celltype.SINUS_KNOT: 3,
        Celltype.MYOKARD: 1,
        Celltype.PURKINJE: 11,
        Celltype.TAWARA: 9,
        Celltype.HIS_BUNDLE: 7,
        Celltype.AV_KNOT: 5
    }
    color_state_depolarized = {  # aktiviert
        Celltype.NO_HEART_CELL: 0,
        Celltype.RIGHT_ATRIUM: 2,
        Celltype.LEFT_ATRIUM: 2,
        Celltype.SINUS_KNOT: 4,
        Celltype.MYOKARD: 2,
        Celltype.PURKINJE: 12,
        Celltype.TAWARA: 10,
        Celltype.HIS_BUNDLE: 8,
        Celltype.AV_KNOT: 6
    }

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

    def __init__(self, celltype):  # constructor
        self.celltype = celltype
        self.stateMachine = FiniteStateMachine(self.ausbreitungs_geschwindigkeit[self.celltype],
                                               self.dauer_erregung, self.refrektaer_zeit)
        self.isTriggered = False
        self.step = 0

    def trigger(self):
        self.isTriggered = True

    def step(self):
        self.step += 1
        self.stateMachine.refreshState(self.step, self.isTriggered)
        self.isTriggered = False  # reset depolarization trigger

    def get_color_state(self):
        # print(self.state)
        return self.color_state_polarized[self.celltype]

