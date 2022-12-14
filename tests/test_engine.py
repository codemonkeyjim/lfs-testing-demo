import pytest

from engine import Engine, States, Operators


def input_digits(engine: Engine, digits: str):
    for digit in digits:
        engine.input_digit(digit)


def test_init():
    engine = Engine()
    assert engine.state == States.START
    assert engine.pending_operator == Operators.NOOP
    assert engine.accumulator == 0.0
    assert engine.display == "0"


def test_accumulate_digits():
    engine = Engine()
    engine.input_digit("1")
    engine.input_digit("2")
    engine.input_digit("3")
    assert engine.display == "123"


def test_accumulate_zeroes():
    engine = Engine()
    engine.input_digit("0")
    engine.input_digit("0")
    engine.input_digit("0")
    assert engine.display == "0"


def test_intermediate_operation():
    engine = Engine()
    input_digits(engine, "12")
    engine.input_operation(Operators.ADD)
    assert engine.display == "12"
    assert engine.pending_operator == Operators.ADD
    input_digits(engine, "34")
    engine.input_operation(Operators.SUBTRACT)
    assert engine.display == "46"
    input_digits(engine, "12")
    engine.input_operation(Operators.SUBTRACT)
    assert engine.display == "34"


@pytest.mark.parametrize(
    "l_operand, operator, r_operand, result",
    [
        ("12", Operators.ADD, "34", "46"),
        ("78", Operators.SUBTRACT, "56", "22"),
        # ("9", Operators.MULTIPLY, "10", "90"),
        # ("72", Operators.DIVIDE, "8", "9"),
    ],
)
def test_operators(l_operand, operator, r_operand, result):
    engine = Engine()
    input_digits(engine, l_operand)
    engine.input_operation(operator)
    input_digits(engine, r_operand)
    engine.input_equals()
    assert engine.display == result
    assert engine.state == States.START


def test_equals_at_start():
    engine = Engine()
    input_digits(engine, "24")
    engine.input_equals()
    engine.input_equals()
    assert engine.display == "24"
    assert engine.state == States.START


@pytest.mark.parametrize(
    "state, accumulator, display, pending_operator",
    [
        (States.START, 0.0, "0", Operators.NOOP),
        (States.ACCUMULATE, 12.0, "24", Operators.ADD),
        (States.COMPUTE, 12.0, "24", Operators.ADD),
        (States.ERROR, 12.0, "24", Operators.ADD),
    ],
)
def test_clear_all(state, accumulator, display, pending_operator):
    engine = Engine()
    engine.set_state(state)
    engine.accumulator = accumulator
    engine.display = display
    engine.pending_operator = pending_operator

    engine.clear_all()

    assert engine.state == States.START
    assert engine.accumulator == 0.0
    assert engine.display == "0"
    assert engine.pending_operator == Operators.NOOP


def test_compute_operator_error():
    engine = Engine()
    engine.set_state(States.COMPUTE)
    engine.input_operation(Operators.ADD)
    assert engine.state == States.ERROR


def test_divide_by_zero():
    engine = Engine()
    engine.set_state(States.ACCUMULATE)
    engine.accumulator = 123.0
    engine.display = "0"
    engine.pending_operator = Operators.DIVIDE

    engine.input_equals()

    assert engine.state == States.ERROR


def test_input_after_equals():
    engine = Engine()
    input_digits(engine, "12")
    engine.input_operation(Operators.ADD)
    input_digits(engine, "23")
    engine.input_equals()
    assert engine.display == "35"

    input_digits(engine, "99")
    assert engine.display == "99"
