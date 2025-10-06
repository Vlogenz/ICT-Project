import pytest
from src.model.Splitter32to8 import Splitter32to8
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus


class TestSplitter32to8:
    """Comprehensive tests for Splitter32to8 component covering all edge cases - reverse of Collector8to32 tests."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        getBus().setManual()
        self.splitter = Splitter32to8()

    def test_splitter_initialization(self):
        """Test that Splitter32to8 initializes correctly."""
        assert len(self.splitter.inputs) == 1
        assert self.splitter.inputs["input1"] is None
        assert self.splitter.inputBitwidths["input1"] == 32
        # Check all 4 outputs are initialized to (0,8)
        for i in range(1, 5):
            assert self.splitter.state[f"outValue{i}"] == (0, 8)

    def test_splitter_no_input_connected(self):
        """Test splitter behavior when no input is connected."""
        changed = self.splitter.eval()
        # All outputs should be (0,8)
        for i in range(1, 5):
            assert self.splitter.state[f"outValue{i}"] == (0, 8)
        assert changed is False  # No change from initial state

    def test_splitter_single_byte_values(self):
        """Test splitter with single byte values (reverse of collector single input)."""
        test_values = [0x01, 0x0F, 0x55, 0xAA, 0xFF]
        
        for byte_position in range(4):
            for test_value in test_values:
                splitter = Splitter32to8()
                input_value = test_value << (byte_position * 8)
                splitter.addInput(DummyInput(input_value, 32), "outValue", "input1")
                changed = splitter.eval()
                
                # Check that only the corresponding output has the test value
                for i in range(1, 5):
                    if i == byte_position + 1:  # byte_position is 0-indexed, outputs are 1-indexed
                        assert splitter.state[f"outValue{i}"] == (test_value, 8)
                    else:
                        assert splitter.state[f"outValue{i}"] == (0, 8)
                assert changed is True

    def test_splitter_all_outputs_high(self):
        """Test splitter when input has all bytes set to maximum (reverse of collector all inputs high)."""
        input_value = 0xFFFFFFFF  # All 32 bits set
        self.splitter.addInput(DummyInput(input_value, 32), "outValue", "input1")
        
        changed = self.splitter.eval()
        # All outputs should be (0xFF, 8)
        for i in range(1, 5):
            assert self.splitter.state[f"outValue{i}"] == (0xFF, 8)
        assert changed is True

    def test_splitter_all_outputs_low(self):
        """Test splitter when input is zero (reverse of collector all inputs low)."""
        input_value = 0x00000000  # All bits clear
        self.splitter.addInput(DummyInput(input_value, 32), "outValue", "input1")
        
        changed = self.splitter.eval()
        # All outputs should be (0x00, 8)
        for i in range(1, 5):
            assert self.splitter.state[f"outValue{i}"] == (0x00, 8)
        assert changed is False  # No change from initial state

    @pytest.mark.parametrize("input_value, expected1, expected2, expected3, expected4", [
        (0x78563412, 0x12, 0x34, 0x56, 0x78),  
        (0x000000FF, 0xFF, 0x00, 0x00, 0x00),  
        (0x0000FF00, 0x00, 0xFF, 0x00, 0x00),  
        (0x00FF0000, 0x00, 0x00, 0xFF, 0x00),  
        (0xFF000000, 0x00, 0x00, 0x00, 0xFF),  
        (0xDDCCBBAA, 0xAA, 0xBB, 0xCC, 0xDD),  
        (0x67452301, 0x01, 0x23, 0x45, 0x67),  
    ])
    def test_splitter_byte_patterns(self, input_value, expected1, expected2, expected3, expected4):
        """Test splitter with various byte patterns (reverse of collector byte patterns)."""
        splitter = Splitter32to8()
        splitter.addInput(DummyInput(input_value, 32), "outValue", "input1")
        
        changed = splitter.eval()
        
        assert splitter.state["outValue1"] == (expected1, 8)
        assert splitter.state["outValue2"] == (expected2, 8)
        assert splitter.state["outValue3"] == (expected3, 8)
        assert splitter.state["outValue4"] == (expected4, 8)
        assert changed is True

    def test_splitter_state_change_detection(self):
        """Test that eval() correctly detects state changes."""
        # Initial evaluation with no input
        changed = self.splitter.eval()
        assert changed is False  # No change from initial state
        
        # Add an input and evaluate
        self.splitter.addInput(DummyInput(0x42, 32), "outValue", "input1")
        changed = self.splitter.eval()
        assert changed is True
        assert self.splitter.state["outValue1"] == (0x42, 8)
        for i in range(2, 5):
            assert self.splitter.state[f"outValue{i}"] == (0x00, 8)
        
        # Evaluate again without changes
        changed = self.splitter.eval()
        assert changed is False  # No change from previous state


        """Test that Splitter and Collector are inverse operations."""
        from src.model.Collector8to32 import Collector8to32
        
        test_patterns = [
            0x12345678, 0xAABBCCDD, 0xFF00FF00, 0x00FF00FF, 
            0x80808080, 0x01234567, 0xFEDCBA98
        ]
        
        for original_pattern in test_patterns:
            # Split the pattern using Splitter
            splitter = Splitter32to8()
            splitter.addInput(DummyInput(original_pattern, 32), "outValue", "input1")
            splitter.eval()
            
            # Collect the split bytes using Collector
            collector = Collector8to32()
            for i in range(1, 5):
                byte_value = splitter.state[f"outValue{i}"][0]
                collector.addInput(DummyInput(byte_value, 8), "outValue", f"input{i}")
            
            collector.eval()
            
            # Verify we get back the original pattern
            assert collector.state["outValue"] == (original_pattern, 32)