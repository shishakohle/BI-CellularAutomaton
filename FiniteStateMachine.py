"""
Cell behaviour may be implemented as a finite-state machine with these characteristics:

    STATES (ST*)

    (ST1) POLARIZED
    (ST2) DEPOLARIZING
    (ST3) REFRACTORY
          where (ST1) is the initial state (ST*.init).

    STATE VARIABLES (SV*)

    (SV1) timestamp
          where 0 is its initial value (SV1.init)

    GRADIENT VARIABLES (GV*)

    (GV1) time
    (GV2) isTriggered

    CONSTANTS and THRESHOLDS (THR*)

    (THR1) duration_depolarization_phase
    (THR2) duration_refractory_phase

    ON STATE ENTRY (ST*.E*)
    (ST2.E1) (SV1) = (GV1)
    (ST3.E1) (SV1) = (GV1)

    EVENTS indicated by CONDITIONS (EV*)

    (EV1) (GV2) == TRUE
    (EV2) age >= (THR1)
    (EV2) age >= (THR2)
          where age = (GV1) - (SV1)

    TRANSITIONS (TR*)

    (TR1) (ST1)--(EV1)-->(ST2)
    (TR2) (ST2)--(EV2)-->(ST3)
    (TR3) (ST3)--(EV3)-->(ST1)

See doc for UML notation.
"""


# represent state names as class (as python natively doesn't know enumerations)

class StateName:      # (ST*)
    POLARIZED = 1     # (ST1)
    DEPOLARIZING = 2  # (ST2)
    REFRACTORY = 3    # (ST3)


class FiniteStateMachine:

    # set constants and thresholds in constructor, init state machine with initial state

    def __init__(self, duration_depolarization_phase, duration_refractory_phase):  # (THR*) and (ST*.init)
        self.duration_depolarization_phase = duration_depolarization_phase         # (THR1)
        self.duration_refractory_phase     = duration_refractory_phase             # (THR2)
        self.currentState = self.State()                                           # (ST*.init)

    # bundle up state with state name and state variables in an inner class

    class State:                         # (ST*) and (SV*)
        # initalise with (*.init)
        stateName = StateName.POLARIZED  # (ST*.init)
        timestamp = 0                    # (SV1.init)

    # calculate the next state based on the current state and the gradient variables

    def refreshState(self, time, isTriggered):                        # (GV*)

        # check all events (EV*) for an potential transition (TR*)

        if self.currentState == StateName.POLARIZED:                  # (TR1): (ST1) --> ?
            if isTriggered:                                           # (EV1)
                # complete transition by entering new state
                self.currentState.stateName = StateName.DEPOLARIZING  # (ST2)
                self.currentState.timestamp = time                    # (ST2.E1)

        elif self.currentState == StateName.DEPOLARIZING:             # (TR2): (ST2) --> ?
            if (time - self.timestamp) >=\
                    self.duration_depolarization_phase:               # (EV2)
                # complete transition by entering new state
                self.currentState.stateName = StateName.REFRACTORY    # (ST3)
                self.currentState.timestamp = time                    # (ST3.E1)

        elif self.currentState == StateName.REFRACTORYD:              # (TR3): (ST3) --> ?
            if (time - self.timestamp) >=\
                    self.duration_refractory_phase:                   # (EV3)
                # complete transition by entering new state
                self.currentState.stateName = StateName.REFRACTORY    # (ST1)

        # also return refreshed state to do the calling instance a favor

        return self.currentState
