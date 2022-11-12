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
        self.add_transition('input_digit', [States.START, States.ACCUMULATE], States.ACCUMULATE, before=self._input_digit, conditions=self._is_digit)
        self.add_transition('input_digit', States.COMPUTE, States.ACCUMULATE, before=self._reaccumulate, conditions=self._is_digit)
        self.add_transition('input_operation', States.ACCUMULATE, States.COMPUTE, before=self._input_operation)
        self._clear()

    def _clear(self):
        self.pending_operator = Operators.NOOP
        self.accumulator = 0.0
        self.display = "0"

    def _is_digit(self, digit: str):
        return digit in "0123456789"

    def _input_digit(self, digit: str):
        if self.display == "0":
            self.display = digit
        else:
            self.display += digit

    def _reaccumulate(self, digit: str):
        self.display = digit

    def _do_pending_operation(self):
        operand = float(self.display)
        match self.pending_operator:
            case Operators.NOOP:
                return
            case Operators.ADD:
                self.accumulator += operand
            case Operators.SUBTRACT:
                self.accumulator -= operand
            case Operators.MULTIPLY:
                self.accumulator *= operand
            case Operators.DIVIDE:
                self.accumulator /= operand
        self.display = f'{self.accumulator:g}'

    def _input_operation(self, operation: Operators):
        self._do_pending_operation()
        self.pending_operator = operation
        self.accumulator = float(self.display)
