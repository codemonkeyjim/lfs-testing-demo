import pytest

from textual.widgets import Static

from calculator import CalculatorApp


class TestCalculatorUI:
    @pytest.mark.parametrize(
        "digit", [("1"), ("2"), ("3"), ("4"), ("5"), ("6"), ("7"), ("8"), ("9"), ("0")]
    )
    async def test_digits(self, mock_engine, helpers, digit):
        async with CalculatorApp(engine=mock_engine).run_test() as calculator:
            helpers.click_button(calculator, f"#number-{digit}")
        mock_engine.input_digit.assert_called_once_with(digit)

    @pytest.mark.parametrize(
        "operation, operator",
        [
            ("add", "Operators.ADD"),
            ("subtract", "Operators.SUBTRACT"),
            ("multiply", "Operators.MULTIPLY"),
            ("divide", "Operators.DIVIDE"),
        ],
    )
    async def test_operations(self, mock_engine, helpers, operation, operator):
        async with CalculatorApp(engine=mock_engine).run_test() as calculator:
            helpers.click_button(calculator, f"#operation-{operation}")
        # Jump thorugh hoops because asserting the enum passed matched the
        # operator was failing, even though they looked the same 🤷🏻‍♂️
        mock_engine.input_operation.assert_called()
        assert str(mock_engine.input_operation.call_args.args[0]) == operator
        assert len(mock_engine.input_operation.call_args.args) == 1

    async def test_clear(self, mock_engine, helpers):
        async with CalculatorApp(engine=mock_engine).run_test() as calculator:
            helpers.click_button(calculator, "#action-clear")
        mock_engine.clear_all.assert_called_once()

    async def test_equals(self, mock_engine, helpers):
        async with CalculatorApp(engine=mock_engine).run_test() as calculator:
            helpers.click_button(calculator, "#action-equals")
        mock_engine.input_equals.assert_called_once()

    async def test_reactivity(self, mock_engine, helpers):
        async with CalculatorApp(engine=mock_engine).run_test() as calculator:
            assert calculator.app.digits == "0"

            mock_engine.display = "123"
            # Click a button to force a refresh
            helpers.click_button(calculator, "#action-equals")
            await calculator.pause()
            assert calculator.app.digits == "123"

            mock_engine.display = "456"
            # Click a button to force a refresh
            helpers.click_button(calculator, "#action-equals")
            await calculator.pause()
            assert calculator.app.digits == "456"
