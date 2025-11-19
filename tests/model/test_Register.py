import pytest
from src.model.Or import Or
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus
from src.model.Register import Register

def test_register_initial_state():
    reg = Register()
    assert reg.getState()["outValue"] == (0,32), "Initial state of Register should be (0,1)."
    
def test_register_load_and_hold():
    getBus().setManual()
    reg = Register()
    input_signal = DummyInput(True)
    reg.addInput(input_signal, "outValue", "input")
    
    # Initial eval, should be (0,1)
    changed = reg.eval()
    assert reg.getState()["outValue"] == (0,32), "Register state should be (0,1) after initial eval."
    assert changed is False, "Register.eval() should return False"

def test_register_value_change():
    getBus().setManual()
    reg = Register()
    clk = DummyInput(True)
    reg.addInput(clk, "outValue", "clk")
    input_signal = DummyInput(5, bitwidth=32)  
    reg.addInput(input_signal, "outValue", "input")
    
    # Initial eval, should be (0,1)
    reg.eval()
    assert reg.nextState == (5,32), "Register nextState should be (5,32) after initial eval."
    assert reg.getState()["outValue"] == (0,32), "Register state should be (0,1) after initial eval."
    reg.updateState()  # Simulate clock edge to load initial value
    assert reg.getState()["outValue"] == (5,32), "Register state should be (5,32) after loading initial value."
    
    # Change input to 5 and eval
    input_signal.setValue(3723, bitwidth=32)
    reg.eval()
    reg.updateState()  # Simulate clock edge to load new value
    assert reg.getState()["outValue"] == (3723,32), "Register state should be (5,32) after loading value 5."
    
    
    # Change input to 10 and eval
    input_signal.setValue(10, bitwidth=32)
    reg.eval()
    reg.updateState()  # Simulate clock edge to load new value
    assert reg.getState()["outValue"] == (10,32), "Register state should be (10,32) after loading value 10."