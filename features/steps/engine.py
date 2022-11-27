from behave import *  # pyright: ignore[reportWildcardImportFromLibrary]

from src.engine import Engine, States, Operators


@given("the engine is ready")
def step_impl(context):
    context.engine = Engine()
    assert context.engine.state == States.START


@when("I input {input:d}")
def step_impl(context, input):
    for digit in str(input):
        context.engine.input_digit(digit)


@then("the display is {expected:d}")
def step_impl(context, expected):
    assert context.engine.display == str(expected)
