import pytest
from src.model.RegisterBlock import RegisterBlock
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus


class TestRegisterBlockRead:
    """Tests for reading from the RegisterBlock"""
    
    def test_initial_state(self):
        """Test that RegisterBlock initializes with correct state"""
        getBus().setManual()
        rb = RegisterBlock()
        
        # Check initial state
        assert rb.state["readData1"] == (0, 32)
        assert rb.state["readData2"] == (0, 32)
        
        # Check that all registers are initialized to 0
        assert len(rb.registers) == 20
        assert all(reg == 0 for reg in rb.registers)
    
    def test_read_from_register_zero(self):
        """Test reading from register 0"""
        getBus().setManual()
        rb = RegisterBlock()
        
        # Set up inputs to read from register 0
        rb.addInput(DummyInput(0, 32), "outValue", "readReg1")
        rb.addInput(DummyInput(0, 32), "outValue", "readReg2")
        
        rb.eval()
        
        assert rb.state["readData1"] == (0, 32)
        assert rb.state["readData2"] == (0, 32)
    
    def test_read_from_different_registers(self):
        """Test reading from different registers"""
        getBus().setManual()
        rb = RegisterBlock()
        
        # Set some register values manually for testing
        rb.registers[5] = 42
        rb.registers[10] = 123
        
        # Read from registers 5 and 10
        rb.addInput(DummyInput(5, 32), "outValue", "readReg1")
        rb.addInput(DummyInput(10, 32), "outValue", "readReg2")
        
        rb.eval()
        
        assert rb.state["readData1"] == (42, 32)
        assert rb.state["readData2"] == (123, 32)
    
    def test_read_same_register_twice(self):
        """Test reading from the same register on both ports"""
        getBus().setManual()
        rb = RegisterBlock()
        
        # Set a register value
        rb.registers[7] = 999
        
        # Read from register 7 on both ports
        rb.addInput(DummyInput(7, 32), "outValue", "readReg1")
        rb.addInput(DummyInput(7, 32), "outValue", "readReg2")
        
        rb.eval()
        
        assert rb.state["readData1"] == (999, 32)
        assert rb.state["readData2"] == (999, 32)
    
    def test_read_without_inputs(self):
        """Test reading when no inputs are connected (should default to register 0)"""
        getBus().setManual()
        rb = RegisterBlock()
        
        rb.registers[0] = 55
        
        rb.eval()
        
        # Should read from register 0 when inputs are None
        assert rb.state["readData1"] == (55, 32)
        assert rb.state["readData2"] == (55, 32)
    
    def test_read_out_of_bounds_register(self):
        """Test reading from a register index that's out of bounds"""
        getBus().setManual()
        rb = RegisterBlock()
        
        # Try to read from register 25 (out of bounds - only 20 registers)
        rb.addInput(DummyInput(25, 32), "outValue", "readReg1")
        rb.addInput(DummyInput(30, 32), "outValue", "readReg2")
        
        rb.eval()
        
        # Should return 0 for out of bounds
        assert rb.state["readData1"] == (0, 32)
        assert rb.state["readData2"] == (0, 32)
    
    @pytest.mark.parametrize("reg_index,value", [
        (0, 0),
        (1, 255),
        (5, 1024),
        (10, 65535),
        (19, 2**31 - 1),  # Max 32-bit positive value
    ])
    def test_read_various_register_values(self, reg_index, value):
        """Test reading various values from different registers"""
        getBus().setManual()
        rb = RegisterBlock()
        
        rb.registers[reg_index] = value
        rb.addInput(DummyInput(reg_index, 32), "outValue", "readReg1")
        
        rb.eval()
        
        assert rb.state["readData1"] == (value, 32)


class TestRegisterBlockWrite:
    """Tests for writing to the RegisterBlock"""
    
    def test_write_when_regwrite_is_zero(self):
        """Test that write doesn't occur when regWrite is 0"""
        getBus().setManual()
        rb = RegisterBlock()
        
        # Set up write inputs but with regWrite = 0
        rb.addInput(DummyInput(5, 32), "outValue", "writeReg")
        rb.addInput(DummyInput(42, 32), "outValue", "writeData")
        rb.addInput(DummyInput(0, 1), "outValue", "regWrite")
        
        rb.updateRegisterValues()
        
        # Register should still be 0 (no write occurred)
        assert rb.registers[5] == 0
    
    def test_write_when_regwrite_is_one(self):
        """Test that write occurs when regWrite is 1"""
        getBus().setManual()
        rb = RegisterBlock()
        
        # Set up write inputs with regWrite = 1
        rb.addInput(DummyInput(5, 32), "outValue", "writeReg")
        rb.addInput(DummyInput(42, 32), "outValue", "writeData")
        rb.addInput(DummyInput(1, 1), "outValue", "regWrite")
        
        rb.updateRegisterValues()
        
        # Register 5 should now contain 42
        assert rb.registers[5] == 42
    
    def test_write_out_of_bounds(self):
        """Test writing to an out-of-bounds register (should not crash)"""
        getBus().setManual()
        rb = RegisterBlock()
        
        rb.addInput(DummyInput(25, 32), "outValue", "writeReg")
        rb.addInput(DummyInput(123, 32), "outValue", "writeData")
        rb.addInput(DummyInput(1, 1), "outValue", "regWrite")
        
        # Should not crash
        rb.updateRegisterValues()
        
        # All registers should still be 0
        assert all(reg == 0 for reg in rb.registers)
    
    def test_write_without_writereg_input(self):
        """Test write when writeReg input is not connected"""
        getBus().setManual()
        rb = RegisterBlock()
        
        rb.addInput(DummyInput(42, 32), "outValue", "writeData")
        rb.addInput(DummyInput(1, 1), "outValue", "regWrite")
        
        # Should not crash
        rb.updateRegisterValues()
    
    def test_write_without_writedata_input(self):
        """Test write when writeData input is not connected"""
        getBus().setManual()
        rb = RegisterBlock()
        
        rb.addInput(DummyInput(5, 32), "outValue", "writeReg")
        rb.addInput(DummyInput(1, 1), "outValue", "regWrite")
        
        # Should not crash
        rb.updateRegisterValues()
    
    @pytest.mark.parametrize("reg_index,value", [
        (0, 1),
        (1, 255),
        (5, 1024),
        (10, 65535),
        (15, 2**20),
        (19, 2**31 - 1),
    ])
    def test_write_various_values(self, reg_index, value):
        """Test writing various values to different registers"""
        getBus().setManual()
        rb = RegisterBlock()
        
        rb.addInput(DummyInput(reg_index, 32), "outValue", "writeReg")
        rb.addInput(DummyInput(value, 32), "outValue", "writeData")
        rb.addInput(DummyInput(1, 1), "outValue", "regWrite")
        
        rb.updateRegisterValues()
        
        assert rb.registers[reg_index] == value


class TestRegisterBlockReadWrite:
    """Tests for combined read and write operations"""
    
    def test_write_then_read(self):
        """Test writing to a register and then reading from it"""
        getBus().setManual()
        rb = RegisterBlock()
        
        # Write to register 8
        rb.addInput(DummyInput(8, 32), "outValue", "writeReg")
        rb.addInput(DummyInput(555, 32), "outValue", "writeData")
        rb.addInput(DummyInput(1, 1), "outValue", "regWrite")
        rb.updateRegisterValues()
        
        # Now read from register 8
        rb.addInput(DummyInput(8, 32), "outValue", "readReg1")
        rb.eval()
        
        assert rb.state["readData1"] == (555, 32)
    
    def test_multiple_writes_to_same_register(self):
        """Test multiple writes to the same register (last write wins)"""
        getBus().setManual()
        rb = RegisterBlock()
        
        # First write
        rb.addInput(DummyInput(3, 32), "outValue", "writeReg")
        rb.addInput(DummyInput(100, 32), "outValue", "writeData")
        rb.addInput(DummyInput(1, 1), "outValue", "regWrite")
        rb.updateRegisterValues()
        
        assert rb.registers[3] == 100
        
        # Second write to same register
        write_reg_input = DummyInput(3, 32)
        write_data_input = DummyInput(200, 32)
        rb.inputs["writeReg"] = (write_reg_input, "outValue")
        rb.inputs["writeData"] = (write_data_input, "outValue")
        rb.updateRegisterValues()
        
        assert rb.registers[3] == 200
    
