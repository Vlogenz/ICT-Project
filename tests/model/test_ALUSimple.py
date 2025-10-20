import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..', 'src'))

from src.model.ALUSimple import ALUSimple
from tests.model.DummyInput import DummyInput


class TestALUSimple:
    
    def test_basic_and_operation(self):
        """Test basic AND operation without inversion."""
        alu = ALUSimple()
        alu.addInput(DummyInput(0b1010, 32), "outValue", "input1")
        alu.addInput(DummyInput(0b1100, 32), "outValue", "input2")
        alu.addInput(DummyInput(0, 2), "outValue", "OP")  # AND operation
        alu.addInput(DummyInput(0, 1), "outValue", "Ainvert")  # No inversion
        alu.addInput(DummyInput(0, 1), "outValue", "Binvert")  # No inversion
        alu.addInput(DummyInput(0, 1), "outValue", "CarryIn")  # No carry in
        
        alu.eval()
        expected = 0b1010 & 0b1100  # 0b1000 = 8
        assert alu.state["outValue"] == (expected, 32)
    
    def test_basic_or_operation(self):
        """Test basic OR operation without inversion."""
        alu = ALUSimple()
        alu.addInput(DummyInput(0b1010, 32), "outValue", "input1")
        alu.addInput(DummyInput(0b1100, 32), "outValue", "input2")
        alu.addInput(DummyInput(1, 2), "outValue", "OP")  # OR operation
        alu.addInput(DummyInput(0, 1), "outValue", "Ainvert")  # No inversion
        alu.addInput(DummyInput(0, 1), "outValue", "Binvert")  # No inversion
        alu.addInput(DummyInput(0, 1), "outValue", "CarryIn")  # No carry in
        
        alu.eval()
        expected = 0b1010 | 0b1100  # 0b1110 = 14
        assert alu.state["outValue"] == (expected, 32)
    
    def test_basic_add_operation(self):
        """Test basic ADD operation without inversion."""
        alu = ALUSimple()
        alu.addInput(DummyInput(10, 32), "outValue", "input1")
        alu.addInput(DummyInput(5, 32), "outValue", "input2")
        alu.addInput(DummyInput(2, 2), "outValue", "OP")  # ADD operation
        alu.addInput(DummyInput(0, 1), "outValue", "Ainvert")  # No inversion
        alu.addInput(DummyInput(0, 1), "outValue", "Binvert")  # No inversion
        alu.addInput(DummyInput(0, 1), "outValue", "CarryIn")  # No carry in
        
        alu.eval()
        assert alu.state["outValue"] == (15, 32)
    
    def test_ainvert_functionality(self):
        """Test A input inversion."""
        alu = ALUSimple()
        alu.addInput(DummyInput(0b1010, 32), "outValue", "input1")
        alu.addInput(DummyInput(0b1100, 32), "outValue", "input2")
        alu.addInput(DummyInput(0, 2), "outValue", "OP")  # AND operation
        alu.addInput(DummyInput(1, 1), "outValue", "Ainvert")  # Invert A
        alu.addInput(DummyInput(0, 1), "outValue", "Binvert")  # No inversion
        alu.addInput(DummyInput(0, 1), "outValue", "CarryIn")  # No carry in
        
        alu.eval()
        inverted_a = (~0b1010) & 0xFFFFFFFF
        expected = inverted_a & 0b1100
        assert alu.state["outValue"] == (expected, 32)
    
    def test_binvert_functionality(self):
        """Test B input inversion."""
        alu = ALUSimple()
        alu.addInput(DummyInput(0b1010, 32), "outValue", "input1")
        alu.addInput(DummyInput(0b1100, 32), "outValue", "input2")
        alu.addInput(DummyInput(0, 2), "outValue", "OP")  # AND operation
        alu.addInput(DummyInput(0, 1), "outValue", "Ainvert")  # No inversion
        alu.addInput(DummyInput(1, 1), "outValue", "Binvert")  # Invert B
        alu.addInput(DummyInput(0, 1), "outValue", "CarryIn")  # No carry in
        
        alu.eval()
        inverted_b = (~0b1100) & 0xFFFFFFFF
        expected = 0b1010 & inverted_b
        assert alu.state["outValue"] == (expected, 32)
    
    def test_both_invert_functionality(self):
        """Test both A and B input inversion."""
        alu = ALUSimple()
        alu.addInput(DummyInput(0b1010, 32), "outValue", "input1")
        alu.addInput(DummyInput(0b1100, 32), "outValue", "input2")
        alu.addInput(DummyInput(0, 2), "outValue", "OP")  # AND operation
        alu.addInput(DummyInput(1, 1), "outValue", "Ainvert")  # Invert A
        alu.addInput(DummyInput(1, 1), "outValue", "Binvert")  # Invert B
        alu.addInput(DummyInput(0, 1), "outValue", "CarryIn")  # No carry in
        
        alu.eval()
        inverted_a = (~0b1010) & 0xFFFFFFFF
        inverted_b = (~0b1100) & 0xFFFFFFFF
        expected = inverted_a & inverted_b
        assert alu.state["outValue"] == (expected, 32)
    
    def test_subtraction_simulation(self):
        """Test subtraction using inverted B input and ADD operation (A - B = A + ~B + 1)."""
        alu = ALUSimple()
        a = 10
        b = 3
        
        # To perform A - B, we need A + ~B + 1 (true two's complement subtraction)
        alu.addInput(DummyInput(a, 32), "outValue", "input1")
        alu.addInput(DummyInput(b, 32), "outValue", "input2")
        alu.addInput(DummyInput(2, 2), "outValue", "OP")  # ADD operation
        alu.addInput(DummyInput(0, 1), "outValue", "Ainvert")  # No inversion
        alu.addInput(DummyInput(1, 1), "outValue", "Binvert")  # Invert B
        alu.addInput(DummyInput(1, 1), "outValue", "CarryIn")  # Add +1 for two's complement
        
        alu.eval()
        # This should give us true subtraction: A - B
        expected = a - b  # 10 - 3 = 7
        assert alu.state["outValue"] == (expected, 32)
    
    def test_carryin_functionality(self):
        """Test that CarryIn adds +1 to ADD operations."""
        alu = ALUSimple()
        alu.addInput(DummyInput(10, 32), "outValue", "input1")
        alu.addInput(DummyInput(5, 32), "outValue", "input2")
        alu.addInput(DummyInput(2, 2), "outValue", "OP")  # ADD operation
        alu.addInput(DummyInput(0, 1), "outValue", "Ainvert")  # No inversion
        alu.addInput(DummyInput(0, 1), "outValue", "Binvert")  # No inversion
        alu.addInput(DummyInput(1, 1), "outValue", "CarryIn")  # Add +1
        
        alu.eval()
        expected = 10 + 5 + 1  # 16
        assert alu.state["outValue"] == (expected, 32)
    
    def test_true_two_complement_subtraction(self):
        """Test various subtraction scenarios using Binvert + CarryIn."""
        test_cases = [
            (15, 7, 8),    # 15 - 7 = 8
            (100, 25, 75), # 100 - 25 = 75
            (5, 5, 0),     # 5 - 5 = 0
            (0, 1, 0xFFFFFFFF),  # 0 - 1 = -1 (in unsigned: 0xFFFFFFFF)
        ]
        
        for a, b, expected in test_cases:
            alu = ALUSimple()
            alu.addInput(DummyInput(a, 32), "outValue", "input1")
            alu.addInput(DummyInput(b, 32), "outValue", "input2")
            alu.addInput(DummyInput(2, 2), "outValue", "OP")  # ADD operation
            alu.addInput(DummyInput(0, 1), "outValue", "Ainvert")  # No inversion
            alu.addInput(DummyInput(1, 1), "outValue", "Binvert")  # Invert B
            alu.addInput(DummyInput(1, 1), "outValue", "CarryIn")  # Add +1 for two's complement
            
            alu.eval()
            result = alu.state["outValue"][0]
            assert result == expected, f"Failed for {a} - {b}: got {result}, expected {expected}"
    
    def test_or_with_inversion(self):
        """Test OR operation with input inversion."""
        alu = ALUSimple()
        alu.addInput(DummyInput(0b1010, 32), "outValue", "input1")
        alu.addInput(DummyInput(0b1100, 32), "outValue", "input2")
        alu.addInput(DummyInput(1, 2), "outValue", "OP")  # OR operation
        alu.addInput(DummyInput(1, 1), "outValue", "Ainvert")  # Invert A
        alu.addInput(DummyInput(0, 1), "outValue", "Binvert")  # No inversion
        alu.addInput(DummyInput(0, 1), "outValue", "CarryIn")  # No carry in
        
        alu.eval()
        inverted_a = (~0b1010) & 0xFFFFFFFF
        expected = inverted_a | 0b1100
        assert alu.state["outValue"] == (expected, 32)
    
    def test_no_inputs_connected(self):
        """Test ALU behavior when no inputs are connected."""
        alu = ALUSimple()
        alu.eval()
        # All inputs default to 0, OP=0 means AND, so 0 & 0 = 0
        assert alu.state["outValue"] == (0, 32)
    
    def test_32bit_overflow(self):
        """Test that results are properly masked to 32 bits."""
        alu = ALUSimple()
        large_value1 = 0xFFFFFFFF  # Maximum 32-bit value
        large_value2 = 1
        
        alu.addInput(DummyInput(large_value1, 32), "outValue", "input1")
        alu.addInput(DummyInput(large_value2, 32), "outValue", "input2")
        alu.addInput(DummyInput(2, 2), "outValue", "OP")  # ADD operation
        alu.addInput(DummyInput(0, 1), "outValue", "Ainvert")  # No inversion
        alu.addInput(DummyInput(0, 1), "outValue", "Binvert")  # No inversion
        alu.addInput(DummyInput(0, 1), "outValue", "CarryIn")  # No carry in
        
        alu.eval()
        # This should overflow and wrap around to 0
        expected = (large_value1 + large_value2) & 0xFFFFFFFF
        assert alu.state["outValue"] == (expected, 32)
        assert alu.state["outValue"][0] == 0  # Should wrap to 0
    
    def test_invalid_op_code(self):
        """Test that invalid OP codes raise an exception."""
        alu = ALUSimple()
        alu.addInput(DummyInput(1, 32), "outValue", "input1")
        alu.addInput(DummyInput(1, 32), "outValue", "input2")
        alu.addInput(DummyInput(0, 1), "outValue", "Ainvert")
        alu.addInput(DummyInput(0, 1), "outValue", "Binvert")
        alu.addInput(DummyInput(0, 1), "outValue", "CarryIn")
        
        # In some test contexts, the controller's event system is active and will trigger
        # automatic evaluation when inputs are connected, causing the ValueError during addInput.
        # In other contexts, the event system is inactive and we need to call eval() manually.
        # We test both scenarios:
        try:
            # Try to connect the invalid OP - might raise ValueError due to auto-evaluation
            alu.addInput(DummyInput(3, 2), "outValue", "OP")
            # If we get here, auto-evaluation didn't happen, so test manual evaluation
            with pytest.raises(ValueError) as excinfo:
                alu.eval()
            assert "Invalid OP code: 3" in str(excinfo.value)
        except ValueError as e:
            # Auto-evaluation happened during addInput - verify it's the right error
            assert "Invalid OP code: 3" in str(e)
