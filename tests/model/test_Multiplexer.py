import pytest
from src.model.Multiplexer import Multiplexer2Inp
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus

def test_2i1b_multiplexer_raises_error_on_too_many_inputs():
    two_input_multiplexer = Multiplexer2Inp()
    two_input_multiplexer.addInput(DummyInput(True), "outValue", "selection")
    two_input_multiplexer.addInput(DummyInput(True), "outValue", "input1")
    two_input_multiplexer.addInput(DummyInput(False), "outValue", "input2")
    assert two_input_multiplexer.addInput(DummyInput(True), "outValue", "input1") == False
