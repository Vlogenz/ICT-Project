import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..', 'src'))

from src.model.ALUControl import ALUControl
from tests.model.DummyInput import DummyInput


class TestALUControl:
    
    def test_initialization(self):
        """Test that ALUControl initializes correctly."""
        alu_control = ALUControl()
        assert alu_control.inputs == {"ALUop": None, "funct": None}
        assert alu_control.inputBitwidths == {"ALUop": 2, "funct": 6}
        assert alu_control.state == {"ainvert": (0, 1), "binvert": (0, 1), "operation": (0, 2)}
    
    def test_lw_sw_operation_aluop_0(self):
        """Test lw/sw operation (ALUop = 0) - should perform ADD."""
        alu_control = ALUControl()
        alu_control.addInput(DummyInput(0, 2), "outValue", "ALUop")  # ALUop = 0
        alu_control.addInput(DummyInput(0, 6), "outValue", "funct")  # funct = 0 (doesn't matter for ALUop=0)
        
        changed = alu_control.eval()
        
        # Should produce ADD operation: ainvert=0, binvert=0, operation=0
        assert alu_control.state["ainvert"] == (0, 1)
        assert alu_control.state["binvert"] == (0, 1)
        assert alu_control.state["operation"] == (0, 2)
        assert changed == False  # State didn't change from initial state
    
    def test_beq_operation_aluop_1(self):
        """Test beq operation (ALUop = 1) - should perform SUBTRACT."""
        alu_control = ALUControl()
        alu_control.addInput(DummyInput(1, 2), "outValue", "ALUop")  # ALUop = 1
        alu_control.addInput(DummyInput(0, 6), "outValue", "funct")  # funct = 0 (doesn't matter for ALUop=1)
        
        changed = alu_control.eval()
        
        # Should produce SUBTRACT operation: ainvert=0, binvert=1, operation=2
        assert alu_control.state["ainvert"] == (0, 1)
        assert alu_control.state["binvert"] == (1, 1)
        assert alu_control.state["operation"] == (2, 2)
        # Note: changed might be False if state was already set to this before eval()
    
    def test_rtype_add_aluop_2_funct_0(self):
        """Test R-type ADD operation (ALUop = 2, funct = 0)."""
        alu_control = ALUControl()
        alu_control.addInput(DummyInput(2, 2), "outValue", "ALUop")  # ALUop = 2 (R-type)
        alu_control.addInput(DummyInput(0, 6), "outValue", "funct")  # funct = 0 (ADD)
        
        changed = alu_control.eval()
        
        # Should produce ADD operation: ainvert=0, binvert=0, operation=2
        assert alu_control.state["ainvert"] == (0, 1)
        assert alu_control.state["binvert"] == (0, 1)
        assert alu_control.state["operation"] == (2, 2)
        # Note: changed might be False if state was already set to this before eval()
    
    def test_rtype_subtract_aluop_2_funct_2(self):
        """Test R-type SUBTRACT operation (ALUop = 2, funct = 2)."""
        alu_control = ALUControl()
        alu_control.addInput(DummyInput(2, 2), "outValue", "ALUop")  # ALUop = 2 (R-type)
        alu_control.addInput(DummyInput(2, 6), "outValue", "funct")  # funct = 2 (SUBTRACT)
        
        changed = alu_control.eval()
        
        # Should produce SUBTRACT operation: ainvert=0, binvert=1, operation=2
        assert alu_control.state["ainvert"] == (0, 1)
        assert alu_control.state["binvert"] == (1, 1)
        assert alu_control.state["operation"] == (2, 2)
        # Note: changed might be False if state was already set to this before eval()
    
    def test_rtype_and_aluop_2_funct_4(self):
        """Test R-type AND operation (ALUop = 2, funct = 4)."""
        alu_control = ALUControl()
        alu_control.addInput(DummyInput(2, 2), "outValue", "ALUop")  # ALUop = 2 (R-type)
        alu_control.addInput(DummyInput(4, 6), "outValue", "funct")  # funct = 4 (AND)
        
        changed = alu_control.eval()
        
        # Should produce AND operation: ainvert=0, binvert=0, operation=0
        assert alu_control.state["ainvert"] == (0, 1)
        assert alu_control.state["binvert"] == (0, 1)
        assert alu_control.state["operation"] == (0, 2)
        assert changed == False  # State didn't change from initial state
    
    def test_rtype_or_aluop_2_funct_5(self):
        """Test R-type OR operation (ALUop = 2, funct = 5)."""
        alu_control = ALUControl()
        alu_control.addInput(DummyInput(2, 2), "outValue", "ALUop")  # ALUop = 2 (R-type)
        alu_control.addInput(DummyInput(5, 6), "outValue", "funct")  # funct = 5 (OR)
        
        changed = alu_control.eval()
        
        # Should produce OR operation: ainvert=0, binvert=0, operation=1
        assert alu_control.state["ainvert"] == (0, 1)
        assert alu_control.state["binvert"] == (0, 1)
        assert alu_control.state["operation"] == (1, 2)
        # Note: changed might be False if state was already set to this before eval()
    
    def test_rtype_slt_aluop_2_funct_10(self):
        """Test R-type SLT (Set Less Than) operation (ALUop = 2, funct = 10)."""
        alu_control = ALUControl()
        alu_control.addInput(DummyInput(2, 2), "outValue", "ALUop")  # ALUop = 2 (R-type)
        alu_control.addInput(DummyInput(10, 6), "outValue", "funct")  # funct = 10 (SLT)
        
        changed = alu_control.eval()
        
        # Should produce SLT operation: ainvert=0, binvert=1, operation=3
        assert alu_control.state["ainvert"] == (0, 1)
        assert alu_control.state["binvert"] == (1, 1)
        assert alu_control.state["operation"] == (3, 2)
        # Note: changed might be False if state was already set to this before eval()
    
    def test_rtype_unknown_funct_defaults_to_add(self):
        """Test R-type with unknown funct code defaults to ADD."""
        alu_control = ALUControl()
        alu_control.addInput(DummyInput(2, 2), "outValue", "ALUop")  # ALUop = 2 (R-type)
        alu_control.addInput(DummyInput(63, 6), "outValue", "funct")  # funct = 63 (unknown)
        
        changed = alu_control.eval()
        
        # Should default to ADD operation: ainvert=0, binvert=0, operation=0
        assert alu_control.state["ainvert"] == (0, 1)
        assert alu_control.state["binvert"] == (0, 1)
        assert alu_control.state["operation"] == (0, 2)
        assert changed == False  # State didn't change from initial state
    
    def test_no_inputs_defaults_to_aluop_0(self):
        """Test that missing inputs default to ALUop = 0 behavior."""
        alu_control = ALUControl()
        # Don't add any inputs
        
        changed = alu_control.eval()
        
        # Should default to lw/sw operation: ainvert=0, binvert=0, operation=0
        assert alu_control.state["ainvert"] == (0, 1)
        assert alu_control.state["binvert"] == (0, 1)
        assert alu_control.state["operation"] == (0, 2)
        assert changed == False  # State didn't change from initial state
    
    def test_state_change_detection(self):
        """Test that eval() correctly detects state changes."""
        alu_control = ALUControl()
        alu_control.addInput(DummyInput(0, 2), "outValue", "ALUop")  # ALUop = 0
        alu_control.addInput(DummyInput(0, 6), "outValue", "funct")
        
        # First eval - state should not change from initial state
        changed1 = alu_control.eval()
        assert changed1 == False
        
        # Change ALUop to 1 (beq)
        alu_control.inputs["ALUop"][0].setValue(1, 2)
        changed2 = alu_control.eval()
        assert changed2 == True  # State should change
        
        # Eval again without changing inputs - state should not change
        changed3 = alu_control.eval()
        assert changed3 == False
    
    def test_multiple_operations_sequence(self):
        """Test a sequence of different operations."""
        alu_control = ALUControl()
        alu_input = DummyInput(0, 2)
        funct_input = DummyInput(0, 6)
        alu_control.addInput(alu_input, "outValue", "ALUop")
        alu_control.addInput(funct_input, "outValue", "funct")
        
        # Test lw/sw (ALUop = 0)
        alu_input.setValue(0, 2)
        alu_control.eval()
        assert alu_control.state["operation"] == (0, 2)
        
        # Test beq (ALUop = 1)
        alu_input.setValue(1, 2)
        alu_control.eval()
        assert alu_control.state["operation"] == (2, 2)
        assert alu_control.state["binvert"] == (1, 1)
        
        # Test R-type OR (ALUop = 2, funct = 5)
        alu_input.setValue(2, 2)
        funct_input.setValue(5, 6)
        alu_control.eval()
        assert alu_control.state["operation"] == (1, 2)
        assert alu_control.state["binvert"] == (0, 1)
        
        # Test R-type SLT (ALUop = 2, funct = 10)
        funct_input.setValue(10, 6)
        alu_control.eval()
        assert alu_control.state["operation"] == (3, 2)
        assert alu_control.state["binvert"] == (1, 1)
    
    def test_all_rtype_operations(self):
        """Test all supported R-type operations."""
        alu_control = ALUControl()
        alu_input = DummyInput(2, 2)  # R-type
        funct_input = DummyInput(0, 6)
        alu_control.addInput(alu_input, "outValue", "ALUop")
        alu_control.addInput(funct_input, "outValue", "funct")
        
        # Test cases: (funct, expected_ainvert, expected_binvert, expected_operation)
        test_cases = [
            (0, 0, 0, 2),   # ADD
            (2, 0, 1, 2),   # SUBTRACT
            (4, 0, 0, 0),   # AND
            (5, 0, 0, 1),   # OR
            (10, 0, 1, 3),  # SLT
        ]
        
        for funct, expected_ainv, expected_binv, expected_op in test_cases:
            funct_input.setValue(funct, 6)
            alu_control.eval()
            assert alu_control.state["ainvert"] == (expected_ainv, 1), f"Failed for funct={funct}"
            assert alu_control.state["binvert"] == (expected_binv, 1), f"Failed for funct={funct}"
            assert alu_control.state["operation"] == (expected_op, 2), f"Failed for funct={funct}"
