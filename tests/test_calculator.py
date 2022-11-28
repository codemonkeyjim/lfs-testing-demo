import pytest

from textual.pilot import Pilot
from textual.widgets import Button

from calculator import CalculatorApp

class TestCalculator:
    OPERATOR_IDS = {
        '+': 'add',
        '-': 'subtract',
        '*': 'multiply',
        '/': 'divide',
    }

    def click_button(self, pilot: Pilot, id: str):
        pilot.app.query_one(id, Button).press()

    @pytest.mark.parametrize(
        "l_operand, operator, r_operand, result",
        [
            ("12", "+", "34", "46"),
            ("78", "-", "56", "22"),
            ("9", "*", "10", "90"),
            ("72", "/", "8", "9"),
        ],
    )
    async def test_calculations_with_buttons(self, l_operand, operator, r_operand, result):
        async with CalculatorApp().run_test() as calculator:
            for digit in l_operand:
                self.click_button(calculator, f"#number-{digit}")
            self.click_button(calculator, f"#operation-{self.OPERATOR_IDS[operator]}")
            for digit in r_operand:
                self.click_button(calculator, f"#number-{digit}")
            self.click_button(calculator, "#action-equals")
            await calculator.pause()
            assert calculator.app.digits == result
