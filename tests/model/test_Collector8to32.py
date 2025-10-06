import pytest
from src.model.Collector8to32 import Collector8to32
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus


class TestCollector8to32:
    """Comprehensive tests for Collector8to32 component covering all edge cases."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        getBus().setManual()
        self.collector = Collector8to32()

    def test_collector_initialization(self):
        """Test that Collector8to32 initializes correctly."""
        assert len(self.collector.inputs) == 4
        assert all(self.collector.inputs[f"input{i}"] is None for i in range(1, 5))
        assert all(self.collector.inputBitwidths[f"input{i}"] == 8 for i in range(1, 5))
        assert self.collector.state["outValue"] == (0, 32)

    def test_collector_no_inputs_connected(self):
        """Test collector behavior when no inputs are connected."""
        changed = self.collector.eval()
        assert self.collector.state["outValue"] == (0, 32)
        assert changed is False  # No change from initial state

    def test_collector_single_input_connected(self):
        """Test collector with only one input connected."""
        test_values = [0x01, 0x0F, 0x55, 0xAA, 0xFF]
        
        for input_num in range(1, 5):
            for test_value in test_values:
                collector = Collector8to32()
                collector.addInput(DummyInput(test_value, 8), "outValue", f"input{input_num}")
                changed = collector.eval()
                expected_value = test_value << ((input_num - 1) * 8)
                assert collector.state["outValue"] == (expected_value, 32)
                assert changed is True

    def test_collector_all_inputs_high(self):
        """Test collector when all inputs are at maximum value (0xFF)."""
        for i in range(1, 5):
            self.collector.addInput(DummyInput(0xFF, 8), "outValue", f"input{i}")
        
        changed = self.collector.eval()
        expected_value = 0xFFFFFFFF  # All 32 bits set
        assert self.collector.state["outValue"] == (expected_value, 32)
        assert changed is True

    def test_collector_all_inputs_low(self):
        """Test collector when all inputs are zero."""
        for i in range(1, 5):
            self.collector.addInput(DummyInput(0x00, 8), "outValue", f"input{i}")
        
        changed = self.collector.eval()
        assert self.collector.state["outValue"] == (0, 32)
        assert changed is False  # No change from initial state

    @pytest.mark.parametrize("input1, input2, input3, input4, expected", [
        (0x12, 0x34, 0x56, 0x78, 0x78563412),
        (0xFF, 0x00, 0x00, 0x00, 0x000000FF),
        (0x00, 0xFF, 0x00, 0x00, 0x0000FF00),
        (0x00, 0x00, 0xFF, 0x00, 0x00FF0000),
        (0x00, 0x00, 0x00, 0xFF, 0xFF000000),
        (0xAA, 0xBB, 0xCC, 0xDD, 0xDDCCBBAA),
        (0x01, 0x23, 0x45, 0x67, 0x67452301),
    ])
    def test_collector_byte_patterns(self, input1, input2, input3, input4, expected):
        """Test collector with various byte patterns."""
        collector = Collector8to32()
        
        collector.addInput(DummyInput(input1, 8), "outValue", "input1")
        collector.addInput(DummyInput(input2, 8), "outValue", "input2")
        collector.addInput(DummyInput(input3, 8), "outValue", "input3")
        collector.addInput(DummyInput(input4, 8), "outValue", "input4")
        
        changed = collector.eval()
        assert collector.state["outValue"] == (expected, 32)
        assert changed is True

    def test_collector_mixed_connected_disconnected_inputs(self):
        """Test collector with some inputs connected and others disconnected."""
        # Connect only input2 and input4
        self.collector.addInput(DummyInput(0xAB, 8), "outValue", "input2")
        self.collector.addInput(DummyInput(0xCD, 8), "outValue", "input4")
        
        changed = self.collector.eval()
        expected_value = (0xAB << 8) | (0xCD << 24)  # 0xCD00AB00
        assert self.collector.state["outValue"] == (expected_value, 32)
        assert changed is True

    def test_collector_state_change_detection(self):
        """Test that eval() correctly detects state changes."""
        # Initial evaluation with no inputs
        changed = self.collector.eval()
        assert changed is False  # No change from initial state
        
        # Add an input and evaluate
        self.collector.addInput(DummyInput(0x42, 8), "outValue", "input1")
        changed = self.collector.eval()
        assert changed is True
        assert self.collector.state["outValue"] == (0x42, 32)
        
        # Evaluate again without changes
        changed = self.collector.eval()
        assert changed is False  # No change from previous state

 
    def test_collector_byte_boundary_values(self):
        """Test collector with byte boundary values."""
        # Test minimum and maximum values for each input
        boundary_tests = [
            ([0x00, 0x00, 0x00, 0x00], 0x00000000),  # All minimum
            ([0xFF, 0xFF, 0xFF, 0xFF], 0xFFFFFFFF),  # All maximum
            ([0x00, 0xFF, 0x00, 0xFF], 0xFF00FF00),  # Alternating
            ([0xFF, 0x00, 0xFF, 0x00], 0x00FF00FF),  # Inverse alternating
        ]
        
        for input_values, expected in boundary_tests:
            collector = Collector8to32()
            for i, value in enumerate(input_values):
                collector.addInput(DummyInput(value, 8), "outValue", f"input{i+1}")
            
            collector.eval()
            assert collector.state["outValue"] == (expected, 32)
