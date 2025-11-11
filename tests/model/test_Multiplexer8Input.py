import pytest
from src.model.Multiplexer8Input import Multiplexer8Inp
from .DummyInput import DummyInput, DummyOutput

def test_8i1b_multiplexer_raises_error_on_too_many_inputs():
    eight_input_multiplexer = Multiplexer8Inp()
    eight_input_multiplexer.addInput(DummyInput(True, 8),"outValue","selection")
    eight_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input1")
    eight_input_multiplexer.addInput(DummyInput(False, 1),"outValue","input2")
    eight_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input3")
    eight_input_multiplexer.addInput(DummyInput(False, 1),"outValue","input4")
    eight_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input5")
    eight_input_multiplexer.addInput(DummyInput(False, 1),"outValue","input6")
    eight_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input7")
    eight_input_multiplexer.addInput(DummyInput(False, 1),"outValue","input8")
    assert eight_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input1") == False

def test_8i1b_multiplexer_evals_with_missing_selection():
    eight_input_multiplexer = Multiplexer8Inp()
    eight_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input1")
    eight_input_multiplexer.addInput(DummyInput(False, 1),"outValue","input2")
    eight_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input3")
    eight_input_multiplexer.addInput(DummyInput(False, 1),"outValue","input4")
    eight_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input5")
    eight_input_multiplexer.addInput(DummyInput(False, 1),"outValue","input6")
    eight_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input7")
    eight_input_multiplexer.addInput(DummyInput(False, 1),"outValue","input8")
    
    assert eight_input_multiplexer.eval() == True
    assert eight_input_multiplexer.state["outputValue"] == (1, 1)

def test_8i1b_multiplexer_evals_no_inputs_with_output():
    eight_input_multiplexer = Multiplexer8Inp()
    eight_input_multiplexer.addOutput(DummyOutput(1), "input")
    
    assert eight_input_multiplexer.eval() == True
    assert eight_input_multiplexer.state["outputValue"] == (0, 1)

def test_8i1b_multiplexer_allows_multiple_outputs():
    eight_input_multiplexer = Multiplexer8Inp()

    eight_input_multiplexer.addInput(DummyInput(True, 8), "outValue","selection")
    eight_input_multiplexer.addInput(DummyInput(True, 8), "outValue","input1")
    eight_input_multiplexer.addInput(DummyInput(False, 8), "outValue","input2")

    assert eight_input_multiplexer.addOutput(DummyOutput(8), "input") == True
    assert eight_input_multiplexer.addOutput(DummyOutput(8), "input") == True



def test_8i1b_multiplexer_selects_correct_output():
    eight_input_multiplexer = Multiplexer8Inp()
    eight_input_multiplexer.addInput(DummyInput(7, 8),"outValue","selection")
    eight_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input1")
    eight_input_multiplexer.addInput(DummyInput(False, 1),"outValue","input2")
    eight_input_multiplexer.addInput(DummyInput(False, 1),"outValue","input3")
    eight_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input4")
    eight_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input5")
    eight_input_multiplexer.addInput(DummyInput(False, 1),"outValue","input6")
    eight_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input7")
    eight_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input8")

    assert eight_input_multiplexer.eval() == True
    assert eight_input_multiplexer.state["outputValue"] == (1, 1)

def test_8i8b_multiplexer_selects_correct_output():
    eight_input_multiplexer = Multiplexer8Inp()
    eight_input_multiplexer.addInput(DummyInput(5, 8),"outValue","selection")
    eight_input_multiplexer.addInput(DummyInput(2, 8),"outValue","input1")
    eight_input_multiplexer.addInput(DummyInput(19, 8),"outValue","input2")
    eight_input_multiplexer.addInput(DummyInput(0, 8),"outValue","input3")
    eight_input_multiplexer.addInput(DummyInput(1, 8),"outValue","input4")
    eight_input_multiplexer.addInput(DummyInput(5, 8),"outValue","input5")
    eight_input_multiplexer.addInput(DummyInput(19, 8),"outValue","input6")
    eight_input_multiplexer.addInput(DummyInput(41, 8),"outValue","input7")
    eight_input_multiplexer.addInput(DummyInput(5, 8),"outValue","input8")

    assert eight_input_multiplexer.eval() == True
    assert eight_input_multiplexer.state["outputValue"] == (19, 8)

def test_8i1b_multiplexer_rejects_1bit_selection():
    eight_input_multiplexer = Multiplexer8Inp()
    assert eight_input_multiplexer.addInput(DummyInput(True, 1),"outValue","selection") == False

def test_8i_multiplexer_rejects_mixed_input_1_8_bitwidths():
    four_input_multiplexer = Multiplexer8Inp()
    four_input_multiplexer.addInput(DummyInput(True, 8),"outValue","selection")
    four_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input1")
    assert four_input_multiplexer.addInput(DummyInput(5, 8),"outValue","input2") == False

def test_8i_multiplexer_rejects_mixed_input_8_1_bitwidths():
    four_input_multiplexer = Multiplexer8Inp()
    four_input_multiplexer.addInput(DummyInput(True, 8),"outValue","selection")
    four_input_multiplexer.addInput(DummyInput(5, 8),"outValue","input1")
    assert four_input_multiplexer.addInput(DummyInput(False, 1),"outValue","input2") == False

def test_8i_multiplexer_rejects_mixed_output_1_8_bitwidths():
    four_input_multiplexer = Multiplexer8Inp()
    four_input_multiplexer.addOutput(DummyOutput(1), "input")
    four_input_multiplexer.addOutput(DummyOutput(8), "input")

    assert len(four_input_multiplexer.outputs) == 1

def test_8i_multiplexer_rejects_mixed_output_8_1_bitwidths():
    four_input_multiplexer = Multiplexer8Inp()
    four_input_multiplexer.addOutput(DummyOutput(8), "input")
    four_input_multiplexer.addOutput(DummyOutput(1), "input")

    assert len(four_input_multiplexer.outputs) == 1

def test_8i_multiplexer_rejects_mixed_io_bitwidths():
    four_input_multiplexer = Multiplexer8Inp()
    four_input_multiplexer.addInput(DummyInput(True, 8),"outValue","selection")
    four_input_multiplexer.addInput(DummyInput(True, 1),"outValue","input2")

    assert four_input_multiplexer.addOutput(DummyOutput(8), "input") == False

def test_8i_multiplexer_rejects_mixed_io_bitwidths_set_by_output():
    four_input_multiplexer = Multiplexer8Inp()
    four_input_multiplexer.addInput(DummyInput(True, 8),"outValue","selection")
    four_input_multiplexer.addOutput(DummyOutput(8), "input")

    assert four_input_multiplexer.addInput(DummyInput(True, 8), "outValue", "input1")

def test_8i_multiplexer_only_resets_bidwidths_when_emptied():
    eight_input_multiplexer = Multiplexer8Inp()
    input1 = DummyInput(5, 8)
    input2 = DummyInput(9, 8)
    input3 = DummyInput(5, 8)
    input4 = DummyInput(9, 8)
    input5 = DummyInput(12, 8)
    input6 = DummyInput(31, 8)
    input7 = DummyInput(2, 8)
    input8 = DummyInput(9, 8)
    output1 = DummyOutput(8)

    eight_input_multiplexer.addInput(DummyInput(True, 8),"outValue","selection")
    eight_input_multiplexer.addInput(input1,"outValue","input1")
    eight_input_multiplexer.addInput(input2,"outValue","input2")
    eight_input_multiplexer.addInput(input3,"outValue","input3")
    eight_input_multiplexer.addInput(input4,"outValue","input4")
    eight_input_multiplexer.addInput(input5,"outValue","input5")
    eight_input_multiplexer.addInput(input6,"outValue","input6")
    eight_input_multiplexer.addInput(input7,"outValue","input7")
    eight_input_multiplexer.addInput(input8,"outValue","input8")
    eight_input_multiplexer.addOutput(output1, "input")

    assert eight_input_multiplexer.getBitwidth("input1") == 8
    assert eight_input_multiplexer.getOutputBitwidth() == 8

    eight_input_multiplexer.removeInput(input1, "outValue", "input1")

    assert eight_input_multiplexer.getBitwidth("input1") == 8

    eight_input_multiplexer.removeInput(input2, "outValue", "input2")
    eight_input_multiplexer.removeInput(input3, "outValue", "input3")
    eight_input_multiplexer.removeInput(input4, "outValue", "input4")
    eight_input_multiplexer.removeInput(input5, "outValue", "input5")
    eight_input_multiplexer.removeInput(input6, "outValue", "input6")
    eight_input_multiplexer.removeInput(input7, "outValue", "input7")

    assert eight_input_multiplexer.getBitwidth("input1") == 8
    assert eight_input_multiplexer.getOutputBitwidth() == 8

    eight_input_multiplexer.removeInput(input8, "outValue", "input8")
    eight_input_multiplexer.removeOutput(output1, "input")
    
    assert eight_input_multiplexer.getBitwidth("input1") == 0
    assert eight_input_multiplexer.getOutputBitwidth() == 0

def test_8i_multiplexer_changes_bidwidths_after_emptying():
    eight_input_multiplexer = Multiplexer8Inp()
    input1 = DummyInput(5, 8)
    output1 = DummyOutput(8)
    output2 = DummyOutput(1)

    eight_input_multiplexer.addInput(DummyInput(True, 8),"outValue","selection")
    eight_input_multiplexer.addInput(input1,"outValue","input1")
    eight_input_multiplexer.addOutput(output1, "input")

    assert eight_input_multiplexer.getBitwidth("input1") == 8
    assert eight_input_multiplexer.getOutputBitwidth() == 8

    eight_input_multiplexer.removeInput(input1, "outValue", "input1")
    eight_input_multiplexer.removeOutput(output1, "input")

    assert eight_input_multiplexer.getBitwidth("input1") == 0
    assert eight_input_multiplexer.getOutputBitwidth() == 0

    eight_input_multiplexer.addInput(DummyInput(0, 1),"outValue","input1")
    eight_input_multiplexer.addOutput(output2, "input")

    assert eight_input_multiplexer.getBitwidth("input1") == 1
    assert eight_input_multiplexer.getOutputBitwidth() == 1