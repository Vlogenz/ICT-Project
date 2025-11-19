import pytest
from src.model.DataMemory import DataMemory
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus


class TestDataMemoryRead:
    """Tests for reading from DataMemory"""
    
    def test_initial_state(self):
        """Test that DataMemory initializes with correct state"""
        getBus().setManual()
        dm = DataMemory()
        
        # Check initial state
        assert dm.state["readData"] == (0, 32)
        
        # Check that all memory locations are initialized to 0
        assert len(dm.dataList) == 128
        assert all(data == 0 for data in dm.dataList)
    
    
    def test_read_with_byte_addressing(self):
        """Test that byte addresses are converted to word addresses (divided by 4)"""
        getBus().setManual()
        dm = DataMemory()
        dm.addInput(DummyInput(1,1), "outValue", "memRead")
        # Set data at word address 5 (byte address 20)
        dm.dataList[5] = 999
        
        # Read using byte address 20 (should access word 5)
        dm.addInput(DummyInput(20, 32), "outValue", "address")
        dm.eval()
        
        assert dm.state["readData"] == (999, 32)
    
    def test_read_various_addresses(self):
        """Test reading from various memory addresses"""
        getBus().setManual()
        dm = DataMemory()
        dm.addInput(DummyInput(1,1), "outValue", "memRead")
        
        # Set different values at different addresses
        dm.dataList[0] = 10
        dm.dataList[10] = 100
        dm.dataList[50] = 500
        dm.dataList[127] = 1270
        
        # Read from word 10 (byte address 40)
        dm.addInput(DummyInput(40, 32), "outValue", "address")
        dm.eval()
        assert dm.state["readData"] == (100, 32)
        
        # Read from word 50 (byte address 200)
        address_input = DummyInput(200, 32)
        dm.inputs["address"] = (address_input, "outValue")
        dm.eval()
        assert dm.state["readData"] == (500, 32)
        
        # Read from word 127 (byte address 508)
        address_input2 = DummyInput(508, 32)
        dm.inputs["address"] = (address_input2, "outValue")
        dm.eval()
        assert dm.state["readData"] == (1270, 32)
    
    def test_read_without_address_input(self):
        """Test reading when no address input is connected (should default to 0)"""
        getBus().setManual()
        dm = DataMemory()
        dm.addInput(DummyInput(1,1), "outValue", "memRead")
        
        dm.dataList[0] = 77
        
        dm.eval()
        
        # Should read from address 0 when address input is None
        assert dm.state["readData"] == (77, 32)
    
    def test_read_out_of_bounds_address(self):
        """Test reading from an address that's out of bounds"""
        getBus().setManual()
        dm = DataMemory()
        dm.addInput(DummyInput(1,1), "outValue", "memRead")
        
        # Try to read from word 200 (byte address 800), which is out of bounds (only 128 words)
        dm.addInput(DummyInput(800, 32), "outValue", "address")
        dm.eval()
        
        # Should return 0 for out of bounds
        assert dm.state["readData"] == (0, 32)
    
    @pytest.mark.parametrize("word_address,byte_address", [
        (0, 0),
        (1, 4),
        (2, 8),
        (10, 40),
        (25, 100),
        (100, 400),
        (127, 508),
    ])
    def test_byte_to_word_address_conversion(self, word_address, byte_address):
        """Test that byte addresses are correctly converted to word addresses"""
        getBus().setManual()
        dm = DataMemory()
        dm.addInput(DummyInput(1,1), "outValue", "memRead")
        
        # Set a unique value at the word address
        test_value = word_address * 11 + 7
        dm.dataList[word_address] = test_value
        
        # Read using byte address
        dm.addInput(DummyInput(byte_address, 32), "outValue", "address")
        dm.eval()
        
        assert dm.state["readData"] == (test_value, 32)
    
    @pytest.mark.parametrize("address,value", [
        (0, 0),
        (4, 255),
        (40, 1024),
        (100, 65535),
        (200, 2**20),
        (508, 2**31 - 1),
    ])
    def test_read_various_values(self, address, value):
        """Test reading various values from memory"""
        getBus().setManual()
        dm = DataMemory()
        dm.addInput(DummyInput(1,1), "outValue", "memRead")
        
        word_addr = address // 4
        dm.dataList[word_addr] = value
        
        dm.addInput(DummyInput(address, 32), "outValue", "address")
        dm.eval()
        
        assert dm.state["readData"] == (value, 32)

class TestDataMemoryWrite:
    """Tests for writing to DataMemory"""
    
    def test_write_and_read_back(self):
        """Test writing a value and reading it back"""
        getBus().setManual()
        dm = DataMemory()
        
        # Write value 1234 to address 16 (word 4)
        dm.addInput(DummyInput(16, 32), "outValue", "address")
        dm.addInput(DummyInput(1234, 32), "outValue", "writeData")
        dm.addInput(DummyInput(1, 1), "outValue", "memWrite")  # Enable write
        changed = dm.eval()
        assert not changed  # No output change on write
        
        # Disable write and enable read
        dm.inputs["memWrite"] = None
        dm.addInput(DummyInput(1, 1), "outValue", "memRead")  # Enable read
        changed = dm.eval()
        assert changed  # No output change on read
        assert dm.state["readData"] == (1234, 32)
        
    def test_write_without_memwrite(self):
        """Test that no write occurs when memWrite is not enabled"""
        getBus().setManual()
        dm = DataMemory()
        
        # Attempt to write value 5678 to address 32 (word 8) without memWrite
        dm.addInput(DummyInput(32, 32), "outValue", "address")
        dm.addInput(DummyInput(5678, 32), "outValue", "writeData")
        changed = dm.eval()
        assert not changed  # No output change on write attempt
        
        # Now read back from address 32
        dm.addInput(DummyInput(1, 1), "outValue", "memRead")  # Enable read
        changed = dm.eval()
        assert changed  # Output should change on read
        assert dm.state["readData"] == (0, 32)  # Should still be 0 since no write occurred
        
        
    @pytest.mark.parametrize("address,value", [
        (0, 0),
        (4, 255),
        (40, 1024),
        (100, 65535),
        (200, 2**20),
        (508, 2**31 - 1),
        
    ])
    def test_write_and_read_multiple_addresses(self, address, value):
        """Test writing and reading from multiple addresses"""
        getBus().setManual()
        dm = DataMemory()

        # Write the value to the specified address
        dm.addInput(DummyInput(address, 32), "outValue", "address")
        dm.addInput(DummyInput(value, 32), "outValue", "writeData")
        dm.addInput(DummyInput(1, 1), "outValue", "memWrite")  # Enable write
        changed = dm.eval()
        assert not changed  # No output change on write

        # Disable write and enable read
        dm.inputs["memWrite"] = None
        dm.addInput(DummyInput(1, 1), "outValue", "memRead")  # Enable read
        changed = dm.eval()
        assert changed  # Output should change on read
        assert dm.state["readData"] == (value, 32)
        
    def test_write_and_read_without_address_input(self):
        """Test writing and reading when no address input is connected (should default to 0)"""
        getBus().setManual()
        dm = DataMemory()
        
        # Write value 8888 without address input (should write to address 0)
        dm.addInput(DummyInput(8888, 32), "outValue", "writeData")
        dm.addInput(DummyInput(1, 1), "outValue", "memWrite")  # Enable write
        changed = dm.eval()
        assert not changed  # No output change on write
        
        # Disable write and enable read
        dm.inputs["memWrite"] = None
        dm.addInput(DummyInput(1, 1), "outValue", "memRead")  # Enable read
        changed = dm.eval()
        assert changed  # Output should change on read
        assert dm.state["readData"] == (8888, 32)
        
    def test_write_out_of_bounds_address(self):
        """Test writing to an address that's out of bounds"""
        getBus().setManual()
        dm = DataMemory()
        
        # Attempt to write to word 200 (byte address 800), which is out of bounds
        dm.addInput(DummyInput(800, 32), "outValue", "address")
        dm.addInput(DummyInput(12345, 32), "outValue", "writeData")
        dm.addInput(DummyInput(1, 1), "outValue", "memWrite")  # Enable write
        changed = dm.eval()
        assert not changed  # No output change on write attempt
        
        # Now read back from address 800
        dm.inputs["memWrite"] = None
        dm.addInput(DummyInput(1, 1), "outValue", "memRead")  # Enable read
        changed = dm.eval()
        assert changed  # Output should change on read
        assert dm.state["readData"] == (0, 32)  # Should still be 0 since write was out of bounds

    def test_read_while_writing_raises_error(self):
        """Test that reading and writing at the same time raises an error"""
        getBus().setManual()
        dm = DataMemory()
        
        dm.addInput(DummyInput(0, 32), "outValue", "address")
        dm.addInput(DummyInput(1111, 32), "outValue", "writeData")
        dm.addInput(DummyInput(1, 1), "outValue", "memWrite")  # Enable write
        dm.addInput(DummyInput(1, 1), "outValue", "memRead")   # Enable read
        
        with pytest.raises(ValueError, match="DataMemory cannot read and write at the same time."):
            dm.eval()
            
    def test_load_data(self):
        """Test loading data into DataMemory"""
        getBus().setManual()
        dm = DataMemory()
        
        test_data = [i * 10 for i in range(128)]
        dm.loadData(test_data)
        
        # Verify that data was loaded correctly
        for addr in range(128):
            assert dm.dataList[addr] == test_data[addr]
    
