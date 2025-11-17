import pytest
from src.model.Or import Or
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus
from src.model.ProgramCounter import ProgramCounter

def test_program_counter_initial_state():
    pc = ProgramCounter()
    assert pc.getState()["outValue"] == (0,32), "Initial state of ProgramCounter should be (0,32)."
    
def test_program_counter_value_change():
    getBus().setManual()
    pc = ProgramCounter()
    pc.maxValue = 4000  # Set maxValue high enough for testing
    input_signal = DummyInput(10, bitwidth=32)  
    pc.addInput(input_signal, "outValue", "input")
    
    # Initial eval, should be (0,32)
    changed = pc.eval()
    assert pc.getState()["outValue"] == (10,32), "ProgramCounter state should be (10,32) after initial eval."
    assert changed is True, "ProgramCounter.eval() should return True"
    
    # Change input to 3723 and eval
    input_signal.setValue(3723, bitwidth=32)
    changed = pc.eval()
    assert pc.getState()["outValue"] == (3723,32), "ProgramCounter state should be (3723,32) after changing input."
    assert changed is True, "ProgramCounter.eval() should return True after input change."
    
    # Change input to 0 and eval
    input_signal.setValue(0, bitwidth=32)
    changed = pc.eval()
    assert pc.getState()["outValue"] == (0,32), "ProgramCounter state should be (0,32) after changing input to 0."
    assert changed is True, "ProgramCounter.eval() should return True after input change to 0."
