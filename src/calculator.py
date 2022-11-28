from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import var
from textual.widgets import Button, Static

from src.engine import Engine, Operators

# Based on Textual example calculator
# https://github.com/Textualize/textual/blob/main/examples/calculator.py


class CalculatorApp(App):
    CSS_PATH = "calculator.css"

    OPERATORS = {
        "add": Operators.ADD,
        "subtract": Operators.SUBTRACT,
        "multiply": Operators.MULTIPLY,
        "divide": Operators.DIVIDE,
    }

    digits = var("0")

    def __init__(self, engine=Engine()):
        super().__init__()
        self.engine = engine

    def watch_digits(self, value: str) -> None:
        self.query_one("#digits", Static).update(value)

    def compose(self) -> ComposeResult:
        yield Container(
            Static(id="digits"),
            Button("÷", id="operation-divide", variant="warning"),
            Button("7", id="number-7"),
            Button("8", id="number-8"),
            Button("9", id="number-9"),
            Button("×", id="operation-multiply", variant="warning"),
            Button("4", id="number-4"),
            Button("5", id="number-5"),
            Button("6", id="number-6"),
            Button("-", id="operation-subtract", variant="warning"),
            Button("1", id="number-1"),
            Button("2", id="number-2"),
            Button("3", id="number-3"),
            Button("+", id="operation-add", variant="warning"),
            Button("0", id="number-0"),
            Button("=", id="action-equals", variant="warning"),
            Button("C", id="action-clear", variant="primary"),
            id="calculator",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        assert button_id is not None

        match button_id.split("-", maxsplit=2):
            case ["number", number]:
                self.engine.input_digit(number)
            case ["operation", key]:
                operator = self.OPERATORS[key]
                self.engine.input_operation(operator)
            case ["action", "clear"]:
                self.engine.clear_all()
            case ["action", "equals"]:
                self.engine.input_equals()
        self.digits = self.engine.display


def main():
    CalculatorApp().run()


if __name__ == "__main__":
    main()
