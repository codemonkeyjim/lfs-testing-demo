import pytest
from textual.pilot import Pilot
from textual.widgets import Button

from src.engine import Engine

class Helpers:
    @staticmethod
    def click_button(pilot: Pilot, id: str):
        pilot.app.query_one(id, Button).press()

@pytest.fixture
def helpers():
    return Helpers

@pytest.fixture
def mock_engine(mocker):
    return mocker.MagicMock(Engine)