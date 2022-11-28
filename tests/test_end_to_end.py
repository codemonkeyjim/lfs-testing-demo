import pytest

from calculator import CalculatorApp

OPERATOR_IDS = {
    '+': 'add',
    '-': 'subtract',
    '*': 'multiply',
    '/': 'divide',
}

@pytest.mark.parametrize(
    "l_operand, operator, r_operand, result",
    [
        ("12", "+", "34", "46"),
        ("78", "-", "56", "22"),
        ("9", "*", "10", "90"),
        ("72", "/", "8", "9"),
    ],
)
async def test_calculations_with_buttons(helpers, l_operand, operator, r_operand, result):
    async with CalculatorApp().run_test() as calculator:
        for digit in l_operand:
            helpers.click_button(calculator, f"#number-{digit}")
        helpers.click_button(calculator, f"#operation-{OPERATOR_IDS[operator]}")
        for digit in r_operand:
            helpers.click_button(calculator, f"#number-{digit}")
        helpers.click_button(calculator, "#action-equals")
        await calculator.pause()
        assert calculator.app.digits == result
