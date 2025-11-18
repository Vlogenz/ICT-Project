import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..', 'src'))

from src.model.ControlUnit import ControlUnit
from tests.model.DummyInput import DummyInput


class TestControlUnit:
    """Test class for the ControlUnit component.
    
    The ControlUnit generates control signals based on instruction opcodes for:
    - R-type instructions (opcode 0)
    - lw instruction (opcode 35)
    - sw instruction (opcode 43)
    - beq instruction (opcode 4)
    """
    
    def test_initialization(self):
        """Test that the ControlUnit initializes with default values."""
        cu = ControlUnit()
        
        # Check that inputs are properly initialized
        assert "input" in cu.inputs
        assert cu.inputs["input"] is None
        
        # Check that all control signals are initialized
        assert "RegDst" in cu.state
        assert "Branch" in cu.state
        assert "MemRead" in cu.state
        assert "MemtoReg" in cu.state
        assert "AluOp" in cu.state
        assert "MemWrite" in cu.state
        assert "AluSrc" in cu.state
        assert "RegWrite" in cu.state
        
        # Check default values
        assert cu.state["RegDst"] == (0, 1)
        assert cu.state["Branch"] == (0, 1)
        assert cu.state["MemRead"] == (0, 1)
        assert cu.state["MemtoReg"] == (0, 1)
        assert cu.state["AluOp"] == (0, 2)
        assert cu.state["MemWrite"] == (0, 1)
        assert cu.state["AluSrc"] == (0, 1)
        assert cu.state["RegWrite"] == (0, 1)
    
    def test_rtype_instruction(self):
        """Test control signals for R-type instructions (opcode 0)."""
        cu = ControlUnit()
        cu.addInput(DummyInput(0, 6), "outValue", "input")
        
        cu.eval()
        
        # R-type control signals
        assert cu.state["RegDst"] == (1, 1), "RegDst should be 1 for R-type"
        assert cu.state["Branch"] == (0, 1), "Branch should be 0 for R-type"
        assert cu.state["MemRead"] == (0, 1), "MemRead should be 0 for R-type"
        assert cu.state["MemtoReg"] == (0, 1), "MemtoReg should be 0 for R-type"
        assert cu.state["AluOp"] == (2, 2), "AluOp should be 2 for R-type"
        assert cu.state["MemWrite"] == (0, 1), "MemWrite should be 0 for R-type"
        assert cu.state["AluSrc"] == (0, 1), "AluSrc should be 0 for R-type"
        assert cu.state["RegWrite"] == (1, 1), "RegWrite should be 1 for R-type"
    
    def test_lw_instruction(self):
        """Test control signals for lw instruction (opcode 35)."""
        cu = ControlUnit()
        cu.addInput(DummyInput(35, 6), "outValue", "input")
        
        cu.eval()
        
        # lw control signals
        assert cu.state["RegDst"] == (0, 1), "RegDst should be 0 for lw"
        assert cu.state["Branch"] == (0, 1), "Branch should be 0 for lw"
        assert cu.state["MemRead"] == (1, 1), "MemRead should be 1 for lw"
        assert cu.state["MemtoReg"] == (1, 1), "MemtoReg should be 1 for lw"
        assert cu.state["AluOp"] == (0, 2), "AluOp should be 0 for lw"
        assert cu.state["MemWrite"] == (0, 1), "MemWrite should be 0 for lw"
        assert cu.state["AluSrc"] == (1, 1), "AluSrc should be 1 for lw"
        assert cu.state["RegWrite"] == (1, 1), "RegWrite should be 1 for lw"
    
    def test_sw_instruction(self):
        """Test control signals for sw instruction (opcode 43)."""
        cu = ControlUnit()
        cu.addInput(DummyInput(43, 6), "outValue", "input")
        
        cu.eval()
        
        # sw control signals
        assert cu.state["RegDst"] == (0, 1), "RegDst for sw (don't care)"
        assert cu.state["Branch"] == (0, 1), "Branch should be 0 for sw"
        assert cu.state["MemRead"] == (0, 1), "MemRead should be 0 for sw"
        assert cu.state["MemtoReg"] == (0, 1), "MemtoReg for sw (don't care)"
        assert cu.state["AluOp"] == (0, 2), "AluOp should be 0 for sw"
        assert cu.state["MemWrite"] == (1, 1), "MemWrite should be 1 for sw"
        assert cu.state["AluSrc"] == (1, 1), "AluSrc should be 1 for sw"
        assert cu.state["RegWrite"] == (0, 1), "RegWrite should be 0 for sw"
    
    def test_beq_instruction(self):
        """Test control signals for beq instruction (opcode 4).
        
        Note: There appears to be a bug in the ControlUnit implementation where
        the beq case is missing the 'elif opcode == 4:' condition, causing it
        to always execute. This test may fail until the bug is fixed.
        """
        cu = ControlUnit()
        cu.addInput(DummyInput(4, 6), "outValue", "input")
        
        cu.eval()
        
        # beq control signals
        assert cu.state["RegDst"] == (0, 1), "RegDst for beq (don't care)"
        assert cu.state["Branch"] == (1, 1), "Branch should be 1 for beq"
        assert cu.state["MemRead"] == (0, 1), "MemRead should be 0 for beq"
        assert cu.state["MemtoReg"] == (0, 1), "MemtoReg for beq (don't care)"
        assert cu.state["AluOp"] == (1, 2), "AluOp should be 1 for beq"
        assert cu.state["MemWrite"] == (0, 1), "MemWrite should be 0 for beq"
        assert cu.state["AluSrc"] == (0, 1), "AluSrc should be 0 for beq"
        assert cu.state["RegWrite"] == (0, 1), "RegWrite should be 0 for beq"
    
    def test_no_input_defaults_to_rtype(self):
        """Test that no input (None) defaults to opcode 0 (R-type)."""
        cu = ControlUnit()
        # Don't add any input
        
        cu.eval()
        
        # Should behave like R-type (opcode 0)
        assert cu.state["RegDst"] == (1, 1)
        assert cu.state["AluOp"] == (2, 2)
        assert cu.state["RegWrite"] == (1, 1)
    
    def test_unknown_opcode_defaults_to_zero(self):
        """Test that an unknown opcode defaults to all zero signals."""
        cu = ControlUnit()
        cu.addInput(DummyInput(63, 6), "outValue", "input")  # Unknown opcode (max 6-bit value)
        
        cu.eval()
        
        # All signals should be 0 for unsupported opcodes
        assert cu.state["RegDst"] == (0, 1)
        assert cu.state["Branch"] == (0, 1)
        assert cu.state["MemRead"] == (0, 1)
        assert cu.state["MemtoReg"] == (0, 1)
        assert cu.state["AluOp"] == (0, 2)
        assert cu.state["MemWrite"] == (0, 1)
        assert cu.state["AluSrc"] == (0, 1)
        assert cu.state["RegWrite"] == (0, 1)
    
    def test_multiple_evaluations(self):
        """Test that the ControlUnit can be evaluated multiple times with different inputs."""
        cu = ControlUnit()
        input_component = DummyInput(0, 6)
        cu.addInput(input_component, "outValue", "input")
        
        # First evaluation: R-type
        cu.eval()
        assert cu.state["RegDst"] == (1, 1)
        assert cu.state["AluOp"] == (2, 2)
        
        # Change input to lw
        input_component.setValue(35, 6)
        cu.eval()
        assert cu.state["RegDst"] == (0, 1)
        assert cu.state["MemRead"] == (1, 1)
        assert cu.state["AluOp"] == (0, 2)
        
        # Change input to sw
        input_component.setValue(43, 6)
        cu.eval()
        assert cu.state["MemWrite"] == (1, 1)
        assert cu.state["RegWrite"] == (0, 1)
    
    def test_input_bitwidth(self):
        """Test that the input bitwidth is correctly defined."""
        cu = ControlUnit()
        assert "input" in cu.inputBitwidths
        assert cu.inputBitwidths["input"] == 6
    
    def test_all_signals_have_correct_bitwidth(self):
        """Test that all control signals have the correct bitwidth."""
        cu = ControlUnit()
        cu.addInput(DummyInput(0, 6), "outValue", "input")
        cu.eval()
        
        # Most signals are 1-bit
        assert cu.state["RegDst"][1] == 1
        assert cu.state["Branch"][1] == 1
        assert cu.state["MemRead"][1] == 1
        assert cu.state["MemtoReg"][1] == 1
        assert cu.state["MemWrite"][1] == 1
        assert cu.state["AluSrc"][1] == 1
        assert cu.state["RegWrite"][1] == 1
        
        # AluOp is 2-bit
        assert cu.state["AluOp"][1] == 2
