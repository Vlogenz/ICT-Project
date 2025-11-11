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
        
        dm.dataList[0] = 77
        
        dm.eval()
        
        # Should read from address 0 when address input is None
        assert dm.state["readData"] == (77, 32)
    
    def test_read_out_of_bounds_address(self):
        """Test reading from an address that's out of bounds"""
        getBus().setManual()
        dm = DataMemory()
        
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
        
        word_addr = address // 4
        dm.dataList[word_addr] = value
        
        dm.addInput(DummyInput(address, 32), "outValue", "address")
        dm.eval()
        
        assert dm.state["readData"] == (value, 32)


