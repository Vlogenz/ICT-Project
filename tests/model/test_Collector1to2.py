import pytest
from src.model.Collector1to2 import Collector1to2
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus


class TestCollector1to2:
    """Tests for Collector1to2 component (2 inputs -> 2-bit output)."""

    def setup_method(self):
        getBus().setManual()
        self.collector = Collector1to2()

    def test_collector_initialization(self):
        assert len(self.collector.inputs) == 2
        assert all(self.collector.inputs[f"input{2**i}"] is None for i in range(1, 2))
        assert all(self.collector.inputBitwidths[f"input{2**i}"] == 1 for i in range(1, 2))
        assert self.collector.state["outValue"] == (0, 2)

    def test_collector_no_inputs_connected(self):
        changed = self.collector.eval()
        assert self.collector.state["outValue"] == (0, 2)
        assert changed is False

    def test_collector_single_input_connected(self):
        for i in range(2):
            collector = Collector1to2()
            collector.addInput(DummyInput(1), "outValue", f"input{2**i}")
            changed = collector.eval()
            expected_value = 1 << (i)
            assert collector.state["outValue"] == (expected_value, 2)
            assert changed is True

    def test_collector_all_inputs_high(self):
        for i in range(2):
            self.collector.addInput(DummyInput(1), "outValue", f"input{2**i}")

        changed = self.collector.eval()
        expected_value = 0b11
        assert self.collector.state["outValue"] == (expected_value, 2)
        assert changed is True

    def test_collector_all_inputs_low(self):
        for i in range(1, 2):
            self.collector.addInput(DummyInput(0), "outValue", f"input{2**i}")

        changed = self.collector.eval()
        assert self.collector.state["outValue"] == (0, 2)
        assert changed is False

    @pytest.mark.parametrize("pattern", [0b01, 0b10, 0b11])
    def test_collector_bit_patterns(self, pattern):
        collector = Collector1to2()

        for i in range(2):
            bit_value = (pattern >> i) & 1
            collector.addInput(DummyInput(bit_value), "outValue", f"input{2**i}")

        changed = collector.eval()
        assert collector.state["outValue"] == (pattern, 2)
        assert changed is True

    def test_collector_mixed_connected_disconnected_inputs(self):
        # Connect only input2
        self.collector.addInput(DummyInput(1), "outValue", "input2")

        changed = self.collector.eval()
        expected_value = 0b10
        assert self.collector.state["outValue"] == (expected_value, 2)
        assert changed is True

    def test_collector_state_change_detection(self):
        changed = self.collector.eval()
        assert changed is False

        self.collector.addInput(DummyInput(1), "outValue", "input1")
        changed = self.collector.eval()
        assert changed is True
        assert self.collector.state["outValue"] == (1, 2)

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
        assert self.collector.state["outValue"] == (1, 2)

    def test_collector_invalid_input_keys(self):
        dummy = DummyInput(1)
        with pytest.raises(KeyError):
            self.collector.addInput(dummy, "outValue", "invalid_input")
