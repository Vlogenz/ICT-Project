import pytest
from src.model.Multiplexer import Multiplexer2Inp
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus  

def test_2i1b_multiplexer_raises_error_on_too_many_inputs():
    two_input_multiplexer = Multiplexer2Inp()
    two_input_multiplexer.addInput(DummyInput(True, 1),"outValue","selection")
    two_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input1")
    two_input_multiplexer.addInput(DummyInput(False, 1),"outValue","input2")
    assert two_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input1") == False

def test_2i1b_multiplexer_raises_error_on_too_few_inputs():
    two_input_multiplexer = Multiplexer2Inp()
    two_input_multiplexer.addInput(DummyInput(True), "outValue", "selection")
    two_input_multiplexer.addInput(DummyInput(False), "outValue", "input1")
    assert two_input_multiplexer.state["outputValue"] == (0, 0)


def test_2i1b_multiplexer_selects_correct_output():
    two_input_multiplexer = Multiplexer2Inp()
    two_input_multiplexer.addInput(DummyInput(True, 1),"outValue","selection")
    two_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input1")
    two_input_multiplexer.addInput(DummyInput(False, 1),"outValue","input2")

    two_input_multiplexer.eval()
    assert two_input_multiplexer.state["outputValue"] == (0, 1)


