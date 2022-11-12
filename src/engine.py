import enum
from transitions import Machine

# Implement the calculator FSM from https://www.clear.rice.edu/comp212/06-spring/labs/13/


class States(enum.Enum):
    START = 0
    ACCUMULATE = 1
    COMPUTE = 2
    ERROR = 3
    POINT = 4


class Operators(enum.Enum):
    NOOP = 0
    ADD = 1
    SUBTRACT = 2
    MULTIPLY = 3
    DIVIDE = 4


class Engine(Machine):
    def __init__(self):
        Machine.__init__(self, states=States, initial=States.START)
        self.clear()

    def clear(self):
        self.pending_op = Operators.NOOP
        self.accumulator = 0.0
        self.display = "0"

    def enterDigit(self, digit: int):
        ...
