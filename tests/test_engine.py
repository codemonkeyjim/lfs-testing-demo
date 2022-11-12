from engine import Engine, States


class TestEngine:
    def test_init(self):
        engine = Engine()
        assert engine.state == States.START
        assert engine.accumulator == 0.0
        assert engine.display == "0"
