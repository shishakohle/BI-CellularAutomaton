"""
    BI-CellularAutomaton - A graphical model for the excitation propagation
    at the myocardium, implemented as a Cellular Automaton.
    Copyright (C) 2020  Anna Friedl, Kerstin Pegler, Ingo Weigel

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see https://www.gnu.org/licenses/ .
"""

"""
Cell behaviour may be implemented as a finite-state machine with these characteristics:

    STATES (ST*)

    (ST1) POLARIZED
    (ST2) DEPOLARIZING
    (ST3) DEPOLARIZED
    (ST4) REFRACTORY
          where (ST1) is the initial state (ST*.init).

    STATE VARIABLES (SV*)

    (SV1) timestamp
          where 0 is its initial value (SV1.init)

    GRADIENT VARIABLES (GV*)

    (GV1) step
    (GV2) isTriggered

    CONSTANTS and THRESHOLDS (THR*)

    (THR1) duration_depolarizing_phase
    (THR2) duration_depolarized_phase
    (THR3) duration_refractory_phase

    ON STATE ENTRY (ST*.E*)
    (ST2.E1) (SV1) = (GV1)
    (ST3.E1) (SV1) = (GV1)
    (ST4.E1) (SV1) = (GV1)

    EVENTS indicated by CONDITIONS (EV*)

    (EV1) (GV2) == TRUE
    (EV2) age >= (THR1)
    (EV3) age >= (THR2)
    (EV4) age >= (THR3)
          where age = (GV1) - (SV1)

    TRANSITIONS (TR*)

    (TR1) (ST1)--(EV1)-->(ST2)
    (TR2) (ST2)--(EV2)-->(ST3)
    (TR3) (ST3)--(EV3)-->(ST4)
    (TR4) (ST4)--(EV4)-->(ST1)
"""


# represent state names as class (as python natively doesn't know enumerations)

class StateName:      # (ST*)
    POLARIZED    = 1  # (ST1)
    DEPOLARIZING = 2  # (ST2)
    DEPOLARIZED  = 3  # (ST3)
    REFRACTORY   = 4  # (ST4)


class FiniteStateMachine:

    # set constants and thresholds in constructor, init state machine with initial state

    def __init__(self, duration_depolarizing_phase, duration_depolarized_phase,
                 duration_refractory_phase):                                       # (THR*) and (ST*.init)
        self.duration_depolarizing_phase   = duration_depolarizing_phase           # (THR1)
        self.duration_depolarized_phase    = duration_depolarized_phase            # (THR2)
        self.duration_refractory_phase     = duration_refractory_phase             # (THR3)
        self.currentState = self.State()                                           # (ST*.init)

    # bundle up state with state name and state variables in an inner class

    class State:                         # (ST*) and (SV*)
        # initalise with (*.init)
        stateName = StateName.POLARIZED  # (ST*.init)
        timestamp = 0                    # (SV1.init)

    # calculate the next state based on the current state and the gradient variables

    def refreshState(self, step, isTriggered):                        # (GV*)

        # check all events (EV*) for an potential transition (TR*)

        if self.currentState.stateName == StateName.POLARIZED:        # (TR1): (ST1) --> ?
            if isTriggered:                                           # (EV1)
                # complete transition by entering new state
                self.currentState.stateName = StateName.DEPOLARIZING  # (ST2)
                self.currentState.timestamp = step                    # (ST2.E1)

        elif self.currentState.stateName == StateName.DEPOLARIZING:   # (TR2): (ST2) --> ?
            if (step - self.currentState.timestamp) >=\
                    self.duration_depolarizing_phase:                 # (EV2)
                # complete transition by entering new state
                self.currentState.stateName = StateName.DEPOLARIZED   # (ST3)
                self.currentState.timestamp = step                    # (ST3.E1)

        elif self.currentState.stateName == StateName.DEPOLARIZED:    # (TR3): (ST3) --> ?
            if (step - self.currentState.timestamp) >=\
                    self.duration_depolarized_phase:                  # (EV3)
                # complete transition by entering new state
                self.currentState.stateName = StateName.REFRACTORY    # (ST4)
                self.currentState.timestamp = step                    # (ST4.E1)

        elif self.currentState.stateName == StateName.REFRACTORY:     # (TR4): (ST4) --> ?
            if (step - self.currentState.timestamp) >=\
                    self.duration_refractory_phase:                   # (EV4)
                # complete transition by entering new state
                self.currentState.stateName = StateName.POLARIZED     # (ST1)

        # also return refreshed state to do the calling instance a favor

        return self.currentState
