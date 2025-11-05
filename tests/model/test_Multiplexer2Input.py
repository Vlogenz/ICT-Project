import pytest
from src.model.Multiplexer2Input import Multiplexer2Inp
from .DummyInput import DummyInput, DummyOutput

#   Note: many instances of "bidwidth" typo in test names
#   May break things to just rename them, so be careful of that
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

    assert two_input_multiplexer.eval() == False
    assert two_input_multiplexer.state["outputValue"] == (0, 0)

def test_2i1b_multiplexer_allows_multiple_outputs():
    two_input_multiplexer = Multiplexer2Inp()

    two_input_multiplexer.addInput(DummyInput(True, 1), "outValue","selection")
    two_input_multiplexer.addInput(DummyInput(True, 1), "outValue","input1")
    two_input_multiplexer.addInput(DummyInput(False, 1), "outValue","input2")

    assert two_input_multiplexer.addOutput(DummyOutput(), "input") == True
    assert two_input_multiplexer.addOutput(DummyOutput(), "input") == True



def test_2i1b_multiplexer_selects_correct_output():
    two_input_multiplexer = Multiplexer2Inp()
    two_input_multiplexer.addInput(DummyInput(False, 1),"outValue","selection")
    two_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input1")
    two_input_multiplexer.addInput(DummyInput(False, 1),"outValue","input2")

    two_input_multiplexer.eval()
    assert two_input_multiplexer.state["outputValue"] == (1, 1)

def test_2i8b_multiplexer_selects_correct_output():
    two_input_multiplexer = Multiplexer2Inp()
    two_input_multiplexer.addInput(DummyInput(False, 1),"outValue","selection")
    two_input_multiplexer.addInput(DummyInput(2, 8),"outValue","input1")
    two_input_multiplexer.addInput(DummyInput(19, 8),"outValue","input2")

    two_input_multiplexer.eval()
    assert two_input_multiplexer.state["outputValue"] == (2, 8)

def test_2i_multiplexer_rejects_8bit_selection():
    two_input_multiplexer = Multiplexer2Inp()
    assert two_input_multiplexer.addInput(DummyInput(5, 8),"outValue","selection") == False

def test_2i_multiplexer_rejects_mixed_input_1_8_bitwidths():
    two_input_multiplexer = Multiplexer2Inp()
    two_input_multiplexer.addInput(DummyInput(True, 1),"outValue","selection")
    two_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input1")
    assert two_input_multiplexer.addInput(DummyInput(5, 8),"outValue","input2") == False

def test_2i_multiplexer_rejects_mixed_input_8_1_bitwidths():
    two_input_multiplexer = Multiplexer2Inp()
    two_input_multiplexer.addInput(DummyInput(True, 1),"outValue","selection")
    two_input_multiplexer.addInput(DummyInput(5, 8),"outValue","input1")
    assert two_input_multiplexer.addInput(DummyInput(False, 1),"outValue","input2") == False

def test_2i_multiplexer_rejects_mixed_output_1_8_bitwidths():
    two_input_multiplexer = Multiplexer2Inp()
    two_input_multiplexer.addOutput(DummyOutput(1), "input")
    two_input_multiplexer.addOutput(DummyOutput(8), "input")

    assert len(two_input_multiplexer.outputs) == 1

def test_2i_multiplexer_rejects_mixed_output_8_1_bitwidths():
    two_input_multiplexer = Multiplexer2Inp()
    two_input_multiplexer.addOutput(DummyOutput(8), "input")
    two_input_multiplexer.addOutput(DummyOutput(1), "input")

    assert len(two_input_multiplexer.outputs) == 1

def test_2i_multiplexer_rejects_mixed_io_bitwidths():
    two_input_multiplexer = Multiplexer2Inp()
    two_input_multiplexer.addInput(DummyInput(True, 1),"outValue","selection")
    two_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input2")
    assert two_input_multiplexer.addOutput(DummyOutput(8), "input") == False

def test_2i_multiplexer_rejects_mixed_io_bitwidths_set_by_output():
    two_input_multiplexer = Multiplexer2Inp()
    two_input_multiplexer.addInput(DummyInput(True, 1),"outValue","selection")
    two_input_multiplexer.addOutput(DummyOutput(8), "input")

    assert two_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input2") == False

def test_2i_multiplexer_resets_bidwidths_when_emptied():
    two_input_multiplexer = Multiplexer2Inp()
    input1 = DummyInput(5, 8)
    output1 = DummyOutput(8)

    two_input_multiplexer.addInput(DummyInput(True, 1),"outValue","selection")
    two_input_multiplexer.addInput(input1,"outValue","input1")
    two_input_multiplexer.addOutput(output1, "input")

    assert two_input_multiplexer.getBitwidth("input1") == 8
    assert two_input_multiplexer.getOutputBitwidth() == 8

    two_input_multiplexer.removeInput(input1, "outValue", "input1")
    two_input_multiplexer.removeOutput(output1, "input")

    assert two_input_multiplexer.getBitwidth("input1") == 0
    assert two_input_multiplexer.getOutputBitwidth() == 0

def test_2i_multiplexer_only_resets_bidwidths_when_emptied():
    two_input_multiplexer = Multiplexer2Inp()
    input1 = DummyInput(5, 8)
    input2 = DummyInput(9, 8)
    output1 = DummyOutput(8)

    two_input_multiplexer.addInput(DummyInput(True, 1),"outValue","selection")
    two_input_multiplexer.addInput(input1,"outValue","input1")
    two_input_multiplexer.addInput(input2,"outValue","input2")
    two_input_multiplexer.addOutput(output1, "input")

    assert two_input_multiplexer.getBitwidth("input2") == 8
    assert two_input_multiplexer.getOutputBitwidth() == 8

    two_input_multiplexer.removeInput(input2, "outValue", "input2")
    two_input_multiplexer.removeOutput(output1, "input")

    assert two_input_multiplexer.getBitwidth("input2") == 8
    assert two_input_multiplexer.getOutputBitwidth() == 8

    two_input_multiplexer.removeInput(input1, "outValue", "input1")

    assert two_input_multiplexer.getBitwidth("input2") == 0
    assert two_input_multiplexer.getOutputBitwidth() == 0

def test_2i_multiplexer_changes_bidwidths_after_emptying():
    two_input_multiplexer = Multiplexer2Inp()
    input1 = DummyInput(5, 8)

    two_input_multiplexer.addInput(DummyInput(True, 1),"outValue","selection")
    two_input_multiplexer.addInput(input1,"outValue","input1")

    assert two_input_multiplexer.getBitwidth("input1") == 8
    two_input_multiplexer.removeInput(input1, "outValue", "input1")
    assert two_input_multiplexer.getBitwidth("input1") == 0
    two_input_multiplexer.addInput(DummyInput(0, 1),"outValue","input1")
    assert two_input_multiplexer.getBitwidth("input1") == 1