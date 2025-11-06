import pytest
from src.model.Multiplexer4Input import Multiplexer4Inp
from .DummyInput import DummyInput, DummyOutput

def test_4i1b_multiplexer_raises_error_on_too_many_inputs():
    four_input_multiplexer = Multiplexer4Inp()
    four_input_multiplexer.addInput(DummyInput(True, 8),"outValue","selection")
    four_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input1")
    four_input_multiplexer.addInput(DummyInput(False, 1),"outValue","input2")
    four_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input3")
    four_input_multiplexer.addInput(DummyInput(False, 1),"outValue","input4")
    assert four_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input1") == False

def test_4i1b_multiplexer_raises_error_on_no_inputs():
    four_input_multiplexer = Multiplexer4Inp()
    
    assert four_input_multiplexer.eval() == False
    assert four_input_multiplexer.state["outputValue"] == (0, 0)

def test_4i1b_multiplexer_raises_error_with_no_bitwidth():
    four_input_multiplexer = Multiplexer4Inp()
    four_input_multiplexer.addInput(DummyInput(True, 1), "outValue", "selection")
    
    assert four_input_multiplexer.eval() == False
    assert four_input_multiplexer.state["outputValue"] == (0, 0)

def test_4i1b_multiplexer_evals_with_missing_selection():
    four_input_multiplexer = Multiplexer4Inp()
    four_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input1")
    four_input_multiplexer.addInput(DummyInput(False, 1),"outValue","input2")
    four_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input3")
    four_input_multiplexer.addInput(DummyInput(False, 1),"outValue","input4")
    
    assert four_input_multiplexer.eval() == True
    assert four_input_multiplexer.state["outputValue"] == (1, 1)

def test_4i1b_multiplexer_evals_no_inputs_with_output():
    four_input_multiplexer = Multiplexer4Inp()
    four_input_multiplexer.addOutput(DummyOutput(1), "input")
    
    assert four_input_multiplexer.eval() == True
    assert four_input_multiplexer.state["outputValue"] == (0, 1)

def test_4i1b_multiplexer_allows_multiple_outputs():
    four_input_multiplexer = Multiplexer4Inp()

    four_input_multiplexer.addInput(DummyInput(True, 8), "outValue","selection")
    four_input_multiplexer.addInput(DummyInput(True, 8), "outValue","input1")
    four_input_multiplexer.addInput(DummyInput(False, 8), "outValue","input2")

    assert four_input_multiplexer.addOutput(DummyOutput(8), "input") == True
    assert four_input_multiplexer.addOutput(DummyOutput(8), "input") == True



def test_4i1b_multiplexer_selects_correct_output():
    four_input_multiplexer = Multiplexer4Inp()
    four_input_multiplexer.addInput(DummyInput(3, 8),"outValue","selection")
    four_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input1")
    four_input_multiplexer.addInput(DummyInput(False, 1),"outValue","input2")
    four_input_multiplexer.addInput(DummyInput(False, 1),"outValue","input3")
    four_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input4")

    four_input_multiplexer.eval()
    assert four_input_multiplexer.state["outputValue"] == (1, 1)

def test_4i8b_multiplexer_selects_correct_output():
    four_input_multiplexer = Multiplexer4Inp()
    four_input_multiplexer.addInput(DummyInput(False, 8),"outValue","selection")
    four_input_multiplexer.addInput(DummyInput(2, 8),"outValue","input1")
    four_input_multiplexer.addInput(DummyInput(19, 8),"outValue","input2")
    four_input_multiplexer.addInput(DummyInput(False, 8),"outValue","input3")
    four_input_multiplexer.addInput(DummyInput(True, 8),"outValue","input4")

    four_input_multiplexer.eval()
    assert four_input_multiplexer.state["outputValue"] == (2, 8)

def test_4i1b_multiplexer_rejects_1bit_selection():
    four_input_multiplexer = Multiplexer4Inp()
    assert four_input_multiplexer.addInput(DummyInput(True, 1),"outValue","selection") == False

def test_4i_multiplexer_rejects_mixed_input_1_8_bitwidths():
    four_input_multiplexer = Multiplexer4Inp()
    four_input_multiplexer.addInput(DummyInput(True, 8),"outValue","selection")
    four_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input1")
    assert four_input_multiplexer.addInput(DummyInput(5, 8),"outValue","input2") == False

def test_4i_multiplexer_rejects_mixed_input_8_1_bitwidths():
    four_input_multiplexer = Multiplexer4Inp()
    four_input_multiplexer.addInput(DummyInput(True, 8),"outValue","selection")
    four_input_multiplexer.addInput(DummyInput(5, 8),"outValue","input1")
    assert four_input_multiplexer.addInput(DummyInput(False, 1),"outValue","input2") == False

def test_4i_multiplexer_rejects_mixed_output_1_8_bitwidths():
    four_input_multiplexer = Multiplexer4Inp()
    four_input_multiplexer.addOutput(DummyOutput(1), "input")
    four_input_multiplexer.addOutput(DummyOutput(8), "input")

    assert len(four_input_multiplexer.outputs) == 1

def test_4i_multiplexer_rejects_mixed_output_8_1_bitwidths():
    four_input_multiplexer = Multiplexer4Inp()
    four_input_multiplexer.addOutput(DummyOutput(8), "input")
    four_input_multiplexer.addOutput(DummyOutput(1), "input")

    assert len(four_input_multiplexer.outputs) == 1

def test_4i_multiplexer_rejects_mixed_io_bitwidths():
    four_input_multiplexer = Multiplexer4Inp()
    four_input_multiplexer.addInput(DummyInput(True, 8),"outValue","selection")
    four_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input2")

    assert four_input_multiplexer.addOutput(DummyOutput(8), "input") == False

def test_4i_multiplexer_rejects_mixed_io_bitwidths_set_by_output():
    four_input_multiplexer = Multiplexer4Inp()
    four_input_multiplexer.addInput(DummyInput(True, 8),"outValue","selection")
    four_input_multiplexer.addOutput(DummyOutput(8), "input")

    assert four_input_multiplexer.addInput(DummyInput(True, 8), "outValue", "input1")

def test_4i_multiplexer_only_resets_bidwidths_when_emptied():
    four_input_multiplexer = Multiplexer4Inp()
    input1 = DummyInput(5, 8)
    input2 = DummyInput(9, 8)
    input3 = DummyInput(5, 8)
    input4 = DummyInput(9, 8)
    output1 = DummyOutput(8)

    four_input_multiplexer.addInput(DummyInput(True, 8),"outValue","selection")
    four_input_multiplexer.addInput(input1,"outValue","input1")
    four_input_multiplexer.addInput(input2,"outValue","input2")
    four_input_multiplexer.addInput(input3,"outValue","input3")
    four_input_multiplexer.addInput(input4,"outValue","input4")
    four_input_multiplexer.addOutput(output1, "input")

    assert four_input_multiplexer.getBitwidth("input1") == 8
    assert four_input_multiplexer.getOutputBitwidth() == 8
    four_input_multiplexer.removeInput(input1, "outValue", "input1")

    assert four_input_multiplexer.getBitwidth("input1") == 8
    four_input_multiplexer.removeInput(input2, "outValue", "input2")
    four_input_multiplexer.removeInput(input3, "outValue", "input3")

    assert four_input_multiplexer.getBitwidth("input1") == 8
    four_input_multiplexer.removeInput(input4, "outValue", "input4")
    four_input_multiplexer.removeOutput(output1, "input")

    assert four_input_multiplexer.getBitwidth("input1") == 0
    assert four_input_multiplexer.getOutputBitwidth() == 0

def test_4i_multiplexer_changes_bidwidths_after_emptying():
    four_input_multiplexer = Multiplexer4Inp()
    input1 = DummyInput(5, 8)
    output1 = DummyOutput(8)
    output2 = DummyOutput(1)

    four_input_multiplexer.addInput(DummyInput(True, 8),"outValue","selection")
    four_input_multiplexer.addInput(input1,"outValue","input1")
    four_input_multiplexer.addOutput(output1, "input")

    assert four_input_multiplexer.getBitwidth("input1") == 8
    assert four_input_multiplexer.getOutputBitwidth() == 8

    four_input_multiplexer.removeInput(input1, "outValue", "input1")
    four_input_multiplexer.removeOutput(output1, "input")

    assert four_input_multiplexer.getBitwidth("input1") == 0

    four_input_multiplexer.addInput(DummyInput(0, 1),"outValue","input1")
    four_input_multiplexer.addOutput(output2, "input")

    assert four_input_multiplexer.getBitwidth("input1") == 1
    assert four_input_multiplexer.getOutputBitwidth() == 1
