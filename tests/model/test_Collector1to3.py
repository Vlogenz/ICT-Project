import pytest
from src.model.Collector1to3 import Collector1to3
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus


class TestCollector1to3:
    """Tests for Collector1to3 component (3 inputs -> 3-bit output)."""

    def setup_method(self):
        getBus().setManual()
        self.collector = Collector1to3()

    def test_collector_initialization(self):
        assert len(self.collector.inputs) == 3
        for i,value in self.collector.getInputs().items():
            assert self.collector.getInputs()[i] is None
            assert self.collector.getBitwidth(i) == 1
        assert self.collector.getState()["outValue"] == (0, 3)

    def test_collector_no_inputs_connected(self):
        changed = self.collector.eval()
        assert self.collector.getState()["outValue"] == (0, 3)
        assert changed is False

    def test_collector_single_input_connected(self):
        for i in range(3):
            collector = Collector1to3()
            collector.addInput(DummyInput(1), "outValue", f"input{2**i}")
            changed = collector.eval()
            expected_value = 1 << (i)
            assert collector.state["outValue"] == (expected_value, 3)
            assert changed is True

    def test_collector_all_inputs_high(self):
        for key,value in self.collector.getInputs().items():
            self.collector.addInput(DummyInput(1), "outValue", key)

        changed = self.collector.eval()
        expected_value = 0b111
        assert self.collector.getState()["outValue"] == (expected_value, 3)
        assert changed is True

    def test_collector_all_inputs_low(self):
        for key,value in self.collector.getInputs().items():
            self.collector.addInput(DummyInput(0), "outValue", key)

        changed = self.collector.eval()
        assert self.collector.state["outValue"] == (0, 3)
        assert changed is False

    @pytest.mark.parametrize("pattern", [0b001, 0b010, 0b100, 0b111, 0b101, 0b011, 0b110])
    def test_collector_bit_patterns(self, pattern):
        collector = Collector1to3()

        for i in range(3):
            bit_value = (pattern >> i) & 1
            collector.addInput(DummyInput(bit_value), "outValue", f"input{2**i}")

        changed = collector.eval()
        assert collector.state["outValue"] == (pattern, 3)
        assert changed is True

    def test_collector_mixed_connected_disconnected_inputs(self):
        # Connect only input2
        self.collector.addInput(DummyInput(1), "outValue", "input2")

        changed = self.collector.eval()
        expected_value = 0b010
        assert self.collector.state["outValue"] == (expected_value, 3)
        assert changed is True

    def test_collector_state_change_detection(self):
        changed = self.collector.eval()
        assert changed is False

        self.collector.addInput(DummyInput(1), "outValue", "input1")
        changed = self.collector.eval()
        assert changed is True
        assert self.collector.state["outValue"] == (1, 3)

        changed = self.collector.eval()
        assert changed is False

    def test_collector_input_overwrite_behavior(self):
        dummy1 = DummyInput(1)
        dummy2 = DummyInput(0)

        success1 = self.collector.addInput(dummy1, "outValue", "input1")
        assert success1 is True

        success2 = self.collector.addInput(dummy2, "outValue", "input1")
        assert success2 is False

        self.collector.eval()
        assert self.collector.state["outValue"] == (1, 3)

    def test_collector_invalid_input_keys(self):
        dummy = DummyInput(1)
        with pytest.raises(KeyError):
            self.collector.addInput(dummy, "outValue", "invalid_input")
