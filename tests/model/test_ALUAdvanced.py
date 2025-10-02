import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..', 'src'))

from src.model.ALUAdvanced import ALUAdvanced
from tests.model.DummyInput import DummyInput


class TestALUAdvanced:
    
    def test_basic_and_operation(self):
        """Test basic AND operation without inversion."""
        alu = ALUAdvanced()
        alu.addInput(DummyInput(0b0000000000000000001010, 32), "outValue", "input1")
        alu.addInput(DummyInput(0b0000000000000000001100, 32), "outValue", "input2")
        alu.addInput(DummyInput(0, 2), "outValue", "OP")  # AND operation
        alu.addInput(DummyInput(0, 1), "outValue", "Ainvert")  # No inversion
        alu.addInput(DummyInput(0, 1), "outValue", "Bnegate")  # No negation
        
        alu.eval()
        expected = 0b0000000000000000001000  # 0b1000 = 8
        assert alu.state["outValue"] == (expected, 32)
        assert alu.state["zero"] == (0, 1)  # Result is not zero
    
    def test_basic_or_operation(self):
        """Test basic OR operation without inversion."""
        alu = ALUAdvanced()
        alu.addInput(DummyInput(10, 32), "outValue", "input1") #0b1010
        alu.addInput(DummyInput(12, 32), "outValue", "input2") #0b1100
        alu.addInput(DummyInput(1, 2), "outValue", "OP")  # OR operation
        alu.addInput(DummyInput(0, 1), "outValue", "Ainvert")  # No inversion
        alu.addInput(DummyInput(0, 1), "outValue", "Bnegate")  # No negation
        
        alu.eval()
        expected = 14 # 0b1110 = 14
        assert alu.state["outValue"] == (expected, 32)
        assert alu.state["zero"] == (0, 1)  # Result is not zero
    
    def test_basic_add_operation(self):
        """Test basic ADD operation without inversion."""
        alu = ALUAdvanced()
        alu.addInput(DummyInput(10, 32), "outValue", "input1")
        alu.addInput(DummyInput(5, 32), "outValue", "input2")
        alu.addInput(DummyInput(2, 2), "outValue", "OP")  # ADD operation
        alu.addInput(DummyInput(0, 1), "outValue", "Ainvert")  # No inversion
        alu.addInput(DummyInput(0, 1), "outValue", "Bnegate")  # No negation
        
        alu.eval()
        assert alu.state["outValue"] == (15, 32)
        assert alu.state["zero"] == (0, 1)  # Result is not zero
    
    def test_slt_operation_less_than(self):
        """Test SLT operation when input1 < input2."""
        alu = ALUAdvanced()
        alu.addInput(DummyInput(5, 32), "outValue", "input1")
        alu.addInput(DummyInput(10, 32), "outValue", "input2")
        alu.addInput(DummyInput(3, 2), "outValue", "OP")  # SLT operation
        alu.addInput(DummyInput(0, 1), "outValue", "Ainvert")  # No inversion
        alu.addInput(DummyInput(0, 1), "outValue", "Bnegate")  # No negation
        
        alu.eval()
        assert alu.state["outValue"] == (1, 32)  # 5 < 10, so result is 1
        assert alu.state["zero"] == (0, 1)  # Result is not zero
    
    def test_slt_operation_greater_than(self):
        """Test SLT operation when input1 > input2."""
        alu = ALUAdvanced()
        alu.addInput(DummyInput(10, 32), "outValue", "input1")
        alu.addInput(DummyInput(5, 32), "outValue", "input2")
        alu.addInput(DummyInput(3, 2), "outValue", "OP")  # SLT operation
        alu.addInput(DummyInput(0, 1), "outValue", "Ainvert")  # No inversion
        alu.addInput(DummyInput(0, 1), "outValue", "Bnegate")  # No negation
        
        alu.eval()
        assert alu.state["outValue"] == (0, 32)  # 10 > 5, so result is 0
        assert alu.state["zero"] == (1, 1)  # Result is zero
    
    def test_slt_operation_equal(self):
        """Test SLT operation when input1 == input2."""
        alu = ALUAdvanced()
        alu.addInput(DummyInput(7, 32), "outValue", "input1")
        alu.addInput(DummyInput(7, 32), "outValue", "input2")
        alu.addInput(DummyInput(3, 2), "outValue", "OP")  # SLT operation
        alu.addInput(DummyInput(0, 1), "outValue", "Ainvert")  # No inversion
        alu.addInput(DummyInput(0, 1), "outValue", "Bnegate")  # No negation
        
        alu.eval()
        assert alu.state["outValue"] == (0, 32)  # 7 == 7, so result is 0
        assert alu.state["zero"] == (1, 1)  # Result is zero
    
    def test_ainvert_functionality(self):
        """Test A input inversion."""
        alu = ALUAdvanced()
        alu.addInput(DummyInput(0b1010, 32), "outValue", "input1")
        alu.addInput(DummyInput(0b1100, 32), "outValue", "input2")
        alu.addInput(DummyInput(0, 2), "outValue", "OP")  # AND operation
        alu.addInput(DummyInput(1, 1), "outValue", "Ainvert")  # Invert A
        alu.addInput(DummyInput(0, 1), "outValue", "Bnegate")  # No negation
        
        alu.eval()
        expected = 0b0101 & 0b1100
        assert alu.state["outValue"] == (expected, 32)
        assert alu.state["zero"] == (0, 1)  # Result is not zero
    
    def test_bnegate_functionality(self):
        """Test B input negation (two's complement)."""
        alu = ALUAdvanced()
        alu.addInput(DummyInput(10, 32), "outValue", "input1")
        alu.addInput(DummyInput(3, 32), "outValue", "input2")
        alu.addInput(DummyInput(2, 2), "outValue", "OP")  # ADD operation
        alu.addInput(DummyInput(0, 1), "outValue", "Ainvert")  # No inversion
        alu.addInput(DummyInput(1, 1), "outValue", "Bnegate")  # Negate B (subtraction)
        
        alu.eval()
        # This should perform subtraction: 10 - 3 = 7
        expected = 10 - 3
        assert alu.state["outValue"] == (expected, 32)
        assert alu.state["zero"] == (0, 1)  # Result is not zero
    
    def test_both_invert_functionality(self):
        """Test both A inversion and B negation."""
        alu = ALUAdvanced()
        alu.addInput(DummyInput(0b1010, 32), "outValue", "input1")
        alu.addInput(DummyInput(0b1100, 32), "outValue", "input2")
        alu.addInput(DummyInput(0, 2), "outValue", "OP")  # AND operation
        alu.addInput(DummyInput(1, 1), "outValue", "Ainvert")  # Invert A
        alu.addInput(DummyInput(1, 1), "outValue", "Bnegate")  # Negate B
        
        alu.eval()
        inverted_a = (~0b1010) & 0xFFFFFFFF
        negated_b = (~0b1100 + 1) & 0xFFFFFFFF
        expected = inverted_a & negated_b
        assert alu.state["outValue"] == (expected, 32)
    
    def test_subtraction_various_cases(self):
        """Test various subtraction scenarios using Bnegate."""
        test_cases = [
            (15, 7, 8),    # 15 - 7 = 8
            (100, 25, 75), # 100 - 25 = 75
            (5, 5, 0),     # 5 - 5 = 0
            (0, 1, 0xFFFFFFFF),  # 0 - 1 = -1 (in unsigned: 0xFFFFFFFF)
        ]
        
        for a, b, expected in test_cases:
            alu = ALUAdvanced()
            alu.addInput(DummyInput(a, 32), "outValue", "input1")
            alu.addInput(DummyInput(b, 32), "outValue", "input2")
            alu.addInput(DummyInput(2, 2), "outValue", "OP")  # ADD operation
            alu.addInput(DummyInput(0, 1), "outValue", "Ainvert")  # No inversion
            alu.addInput(DummyInput(1, 1), "outValue", "Bnegate")  # Negate B for subtraction
            
            alu.eval()
            result = alu.state["outValue"][0]
            assert result == expected, f"Failed for {a} - {b}: got {result}, expected {expected}"
            
            # Test zero flag
            expected_zero = 1 if expected == 0 else 0
            assert alu.state["zero"] == (expected_zero, 1), f"Zero flag incorrect for {a} - {b}"
    
    def test_zero_flag_functionality(self):
        """Test zero flag for various operations that result in zero."""
        test_cases = [
            # (input1, input2, op, ainvert, bnegate, description)
            (5, 5, 2, 0, 1, "Subtraction resulting in zero"),  # 5 - 5 = 0
            (0, 0, 0, 0, 0, "AND with zeros"),  # 0 & 0 = 0
            (0, 0, 1, 0, 0, "OR with zeros"),   # 0 | 0 = 0
            (0, 0, 2, 0, 0, "ADD with zeros"),  # 0 + 0 = 0
            (7, 7, 3, 0, 0, "SLT with equal values"),  # 7 == 7, so SLT = 0
        ]
        
        for input1, input2, op, ainvert, bnegate, description in test_cases:
            alu = ALUAdvanced()
            alu.addInput(DummyInput(input1, 32), "outValue", "input1")
            alu.addInput(DummyInput(input2, 32), "outValue", "input2")
            alu.addInput(DummyInput(op, 2), "outValue", "OP")
            alu.addInput(DummyInput(ainvert, 1), "outValue", "Ainvert")
            alu.addInput(DummyInput(bnegate, 1), "outValue", "Bnegate")
            
            alu.eval()
            assert alu.state["outValue"][0] == 0, f"Result should be zero for: {description}"
            assert alu.state["zero"] == (1, 1), f"Zero flag should be 1 for: {description}"
    
    def test_zero_flag_non_zero_results(self):
        """Test zero flag for operations that result in non-zero values."""
        test_cases = [
            # (input1, input2, op, ainvert, bnegate, description)
            (5, 3, 2, 0, 0, "Addition with non-zero result"),  # 5 + 3 = 8
            (0b1010, 0b1100, 0, 0, 0, "AND with non-zero result"),  # 0b1010 & 0b1100 = 0b1000
            (0b1010, 0b0101, 1, 0, 0, "OR with non-zero result"),   # 0b1010 | 0b0101 = 0b1111
            (3, 10, 3, 0, 0, "SLT with less than"),  # 3 < 10, so SLT = 1
        ]
        
        for input1, input2, op, ainvert, bnegate, description in test_cases:
            alu = ALUAdvanced()
            alu.addInput(DummyInput(input1, 32), "outValue", "input1")
            alu.addInput(DummyInput(input2, 32), "outValue", "input2")
            alu.addInput(DummyInput(op, 2), "outValue", "OP")
            alu.addInput(DummyInput(ainvert, 1), "outValue", "Ainvert")
            alu.addInput(DummyInput(bnegate, 1), "outValue", "Bnegate")
            
            alu.eval()
            assert alu.state["outValue"][0] != 0, f"Result should be non-zero for: {description}"
            assert alu.state["zero"] == (0, 1), f"Zero flag should be 0 for: {description}"
    
    def test_or_with_inversion(self):
        """Test OR operation with input inversion."""
        alu = ALUAdvanced()
        alu.addInput(DummyInput(0b1010, 32), "outValue", "input1")
        alu.addInput(DummyInput(0b1100, 32), "outValue", "input2")
        alu.addInput(DummyInput(1, 2), "outValue", "OP")  # OR operation
        alu.addInput(DummyInput(1, 1), "outValue", "Ainvert")  # Invert A
        alu.addInput(DummyInput(0, 1), "outValue", "Bnegate")  # No negation
        
        alu.eval()
        inverted_a = (~0b1010) & 0xFFFFFFFF
        expected = inverted_a | 0b1100
        assert alu.state["outValue"] == (expected, 32)
        assert alu.state["zero"] == (0, 1)  # Result is not zero
    
    def test_no_inputs_connected(self):
        """Test ALU behavior when no inputs are connected."""
        alu = ALUAdvanced()
        alu.eval()
        # All inputs default to 0, OP=0 means AND, so 0 & 0 = 0
        assert alu.state["outValue"] == (0, 32)
        assert alu.state["zero"] == (1, 1)  # Result is zero
    
    def test_32bit_overflow(self):
        """Test that results are properly masked to 32 bits."""
        alu = ALUAdvanced()
        large_value1 = 0xFFFFFFFF  # Maximum 32-bit value
        large_value2 = 1
        
        alu.addInput(DummyInput(large_value1, 32), "outValue", "input1")
        alu.addInput(DummyInput(large_value2, 32), "outValue", "input2")
        alu.addInput(DummyInput(2, 2), "outValue", "OP")  # ADD operation
        alu.addInput(DummyInput(0, 1), "outValue", "Ainvert")  # No inversion
        alu.addInput(DummyInput(0, 1), "outValue", "Bnegate")  # No negation
        
        alu.eval()
        # This should overflow and wrap around to 0
        expected = (large_value1 + large_value2) & 0xFFFFFFFF
        assert alu.state["outValue"] == (expected, 32)
        assert alu.state["outValue"][0] == 0  # Should wrap to 0
        assert alu.state["zero"] == (1, 1)  # Zero flag should be set
    
    def test_slt_with_inversion_and_negation(self):
        """Test SLT operation with input modifications."""
        alu = ALUAdvanced()
        alu.addInput(DummyInput(10, 32), "outValue", "input1")  # Will be inverted
        alu.addInput(DummyInput(5, 32), "outValue", "input2")   # Will be negated
        alu.addInput(DummyInput(3, 2), "outValue", "OP")  # SLT operation
        alu.addInput(DummyInput(1, 1), "outValue", "Ainvert")  # Invert A
        alu.addInput(DummyInput(1, 1), "outValue", "Bnegate")  # Negate B
        
        alu.eval()
        inverted_a = (~10) & 0xFFFFFFFF
        negated_b = (~5 + 1) & 0xFFFFFFFF
        expected = 1 if inverted_a < negated_b else 0
        assert alu.state["outValue"] == (expected, 32)
        
        expected_zero = 1 if expected == 0 else 0
        assert alu.state["zero"] == (expected_zero, 1)
    
    def test_invalid_op_code(self):
        """Test that invalid OP codes raise an exception."""
        alu = ALUAdvanced()
        alu.addInput(DummyInput(1, 32), "outValue", "input1")
        alu.addInput(DummyInput(1, 32), "outValue", "input2")
        alu.addInput(DummyInput(0, 1), "outValue", "Ainvert")
        alu.addInput(DummyInput(0, 1), "outValue", "Bnegate")
        
        # Test with a valid OP code that should trigger an error during evaluation
        # We'll use a mock approach to test invalid OP codes since DummyInput 
        # validates bitwidth constraints
        alu.addInput(DummyInput(0, 2), "outValue", "OP")  # Start with valid OP
        
        # Directly modify the OP input to simulate an invalid value
        # This bypasses DummyInput's validation to test ALU's validation
        original_eval = alu.eval
        
        def test_invalid_op(op_value):
            # Temporarily override the OP input's state
            if alu.inputs["OP"] is not None:
                original_state = alu.inputs["OP"][0].state
                alu.inputs["OP"][0].state = {"outValue": (op_value, 2)}
                try:
                    with pytest.raises(ValueError) as excinfo:
                        alu.eval()
                    assert f"Invalid OP code: {op_value}" in str(excinfo.value)
                finally:
                    # Restore original state
                    alu.inputs["OP"][0].state = original_state
        
        # Test various invalid OP codes that would occur in practice
        # (these could happen due to hardware errors or bit corruption)
        test_invalid_op(4)  # Invalid - only 0-3 are supported
        test_invalid_op(5)  # Invalid
        test_invalid_op(7)  # Invalid (maximum value for 2-bit, but not supported)
    
    def test_beq_simulation_equal_values(self):
        """Test simulation of beq (branch if equal) with equal values."""
        alu = ALUAdvanced()
        # Simulate comparing two equal values for beq
        alu.addInput(DummyInput(42, 32), "outValue", "input1")
        alu.addInput(DummyInput(42, 32), "outValue", "input2")
        alu.addInput(DummyInput(2, 2), "outValue", "OP")  # ADD (subtraction with Bnegate)
        alu.addInput(DummyInput(0, 1), "outValue", "Ainvert")  # No inversion
        alu.addInput(DummyInput(1, 1), "outValue", "Bnegate")  # Subtraction mode
        
        alu.eval()
        assert alu.state["outValue"] == (0, 32)  # 42 - 42 = 0
        assert alu.state["zero"] == (1, 1)  # Zero flag set, indicating values are equal
    
    def test_slt_signed_comparison(self):
        """Test SLT operation with signed 32-bit values (negative numbers)."""
        test_cases = [
            # (input1, input2, expected_result, description)
            (0x7FFFFFFF, 0x80000000, 0, "Max positive vs min negative: 2147483647 > -2147483648"),
            (0x80000000, 0x7FFFFFFF, 1, "Min negative vs max positive: -2147483648 < 2147483647"), 
            (0xFFFFFFFF, 0x00000001, 1, "Negative vs positive: -1 < 1"),
            (0x00000001, 0xFFFFFFFF, 0, "Positive vs negative: 1 > -1"),
            (0x80000000, 0x80000001, 1, "Two negatives: -2147483648 < -2147483647"),
            (0x80000001, 0x80000000, 0, "Two negatives: -2147483647 > -2147483648"),
        ]
        
        for input1, input2, expected, description in test_cases:
            alu = ALUAdvanced()
            alu.addInput(DummyInput(input1, 32), "outValue", "input1")
            alu.addInput(DummyInput(input2, 32), "outValue", "input2")
            alu.addInput(DummyInput(3, 2), "outValue", "OP")  # SLT operation
            alu.addInput(DummyInput(0, 1), "outValue", "Ainvert")
            alu.addInput(DummyInput(0, 1), "outValue", "Bnegate")
            
            alu.eval()
            result = alu.state["outValue"][0]
            assert result == expected, f"SLT failed for {description}: got {result}, expected {expected}"
            
            expected_zero = 1 if expected == 0 else 0
            assert alu.state["zero"] == (expected_zero, 1), f"Zero flag incorrect for {description}"

    def test_beq_simulation_different_values(self):
        """Test simulation of beq (branch if equal) with different values."""
        alu = ALUAdvanced()
        # Simulate comparing two different values for beq
        alu.addInput(DummyInput(42, 32), "outValue", "input1")
        alu.addInput(DummyInput(37, 32), "outValue", "input2")
        alu.addInput(DummyInput(2, 2), "outValue", "OP")  # ADD (subtraction with Bnegate)
        alu.addInput(DummyInput(0, 1), "outValue", "Ainvert")  # No inversion
        alu.addInput(DummyInput(1, 1), "outValue", "Bnegate")  # Subtraction mode
        
        alu.eval()
        assert alu.state["outValue"] == (5, 32)  # 42 - 37 = 5
        assert alu.state["zero"] == (0, 1)  # Zero flag not set, indicating values are different