from behave import *  # pyright: ignore[reportWildcardImportFromLibrary]
from behave.api.async_step import async_run_until_complete
from textual.widgets import Button, Static

from src.calculator import CalculatorApp


@given("the calculator is ready")
def calculator_ready(context):
    context.calculator = CalculatorApp().run_test()


@when("I click {input:d}")
@async_run_until_complete
async def click_digits(context, input):
    async with context.calculator as calculator:
        for digit in str(input):
            button = calculator.app.query_one(f"#number-{digit}", Button)
            button.press()

@when("I click {operator:W}")
@async_run_until_complete
async def click_operator(context, operator):
    async with context.calculator as calculator:
        match operator:
            case "=":
                button = calculator.app.query_one(f"#action-equals", Button)
            case "+":
                button = calculator.app.query_one(f"#operation-add", Button)
            case "-":
                button = calculator.app.query_one(f"#operation-subtract", Button)
            case "*":
                button = calculator.app.query_one(f"#operation-multiply", Button)
            case "/":
                button = calculator.app.query_one(f"#operation-divide", Button)
            case _:
                raise ValueError(f"Unknown button '{operator}'")
        button.press()

@then("the display is {expected:d}")
@async_run_until_complete
async def display_is(context, expected):
    async with context.calculator as calculator:
        assert calculator.app.query_one("#display", Static).value == str(expected)
