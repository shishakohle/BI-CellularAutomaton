from model.FiniteStateMachine import *

import matplotlib.colors as colors


# represent celltypes as class (as python natively doesn't know enumerations)
class Celltype:
    NO_HEART_CELL = 0
    RIGHT_ATRIUM  = 1
    SINUS_KNOT    = 2
    AV_KNOT       = 3
    HIS_BUNDLE    = 4
    TAWARA        = 5
    PURKINJE      = 6
    LEFT_ATRIUM   = 7
    MYOKARD       = 8


class Cell:

    # colors used to indicate cells and their state
    cmap = colors.ListedColormap(['#2e4a1e', '#00baff', '#000b34', '#fff313', '#7b7b00', '#fcc926', '#bf7600',
                                  '#FFFFFF', '#E9967A', '#8B0000', '#605acd', '#3e135e', '#A2CD5A'])

    # associate each celltype with a color that indicates the cell is polarized
    color_state_polarized = {
        Celltype.NO_HEART_CELL: 7,
        Celltype.RIGHT_ATRIUM:  8,
        Celltype.LEFT_ATRIUM:   8,
        Celltype.SINUS_KNOT:   10,
        Celltype.MYOKARD:       8,
        Celltype.PURKINJE:      5,
        Celltype.TAWARA:        3,
        Celltype.HIS_BUNDLE:    1,
        Celltype.AV_KNOT:      12
    }

    # associate each celltype with a color that indicates the cell is depolarizing or depolarized
    color_state_depolarized = {
        Celltype.NO_HEART_CELL: 7,
        Celltype.RIGHT_ATRIUM:  9,
        Celltype.LEFT_ATRIUM:   9,
        Celltype.SINUS_KNOT:   11,
        Celltype.MYOKARD:       9,
        Celltype.PURKINJE:      6,
        Celltype.TAWARA:        4,
        Celltype.HIS_BUNDLE:    2,
        Celltype.AV_KNOT:       0
    }

    excitation_time = 200  # time for which cells stay excited, i.e. in state DEPOLARIZED (same for all cells, 200 ms)
    refractory_time = 300  # time for which cells stay in REFRACTORY state (same for all cells, 300 ms)

    # associate each celltype with the specific time it stays in state DEPOLARIZING,
    # i.e. the time it (once triggered) needs to fully transit from its POLARIZED to its DEPOLARIZED state
    depolarizing_time = {
        Celltype.NO_HEART_CELL: 0,
        Celltype.RIGHT_ATRIUM:  4,
        Celltype.LEFT_ATRIUM:   3,
        Celltype.SINUS_KNOT:    1,
        Celltype.MYOKARD:       5,
        Celltype.PURKINJE:      1,
        Celltype.TAWARA:        2,
        Celltype.HIS_BUNDLE:    3,
        Celltype.AV_KNOT:      35
    }

    def __init__(self, celltype):  # constructor
        self.celltype = celltype
        self.stateMachine = FiniteStateMachine(self.depolarizing_time[self.celltype],
                                               self.excitation_time, self.refractory_time)
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
        if self.getState() == StateName.DEPOLARIZED:
            return self.color_state_depolarized[self.celltype]
        else:
            return self.color_state_polarized[self.celltype]
