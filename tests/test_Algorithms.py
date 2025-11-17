import pytest
from src.Algorithms import Algorithms
from src.model.Input import Input
from src.model.And import And
from src.model.Or import Or
from src.model.Output import Output
from src.model.Not import Not
from src.model.Nor import Nor
from tests.model.DummyInput import DummyInput


def test_khanFrontierEval_simple():
    """Test khanFrontierEval with a simple circuit: in1, in2 -> and1 -> or1 -> out1"""
    in1 = Input()
    in2 = Input()
    in3 = Input()
    and1 = And()
    or1 = Or()
    out1 = Output()

    in1.addOutput(and1, "input1")
    in2.addOutput(and1, "input2")
    and1.addInput(in1, "outValue", "input1")
    and1.addInput(in2, "outValue", "input2")

    and1.addOutput(or1, "input1")
    in3.addOutput(or1, "input2")
    or1.addInput(and1, "outValue", "input1")
    or1.addInput(in3, "outValue", "input2")

    or1.addOutput(out1, "input")
    out1.addInput(or1, "outValue", "input")

    in1.setState((1, 1))
    in2.setState((0, 1))
    in3.setState((0, 1))

    inputs = [in1, in2, in3]
    components = [in1, in2, in3, and1, or1, out1]

    assert Algorithms.khanFrontierEval(inputs, components) == True
    assert and1.getState()["outValue"] == (0, 1)
    assert or1.getState()["outValue"] == (0, 1)
    assert out1.getState()["outValue"] == (0, 1)

    in2.setState((1, 1))
    assert Algorithms.khanFrontierEval(inputs, components) == True
    assert and1.getState()["outValue"] == (1, 1)
    assert or1.getState()["outValue"] == (1, 1)
    assert out1.getState()["outValue"] == (1, 1)


def test_khanFrontierEval_circular_bad_dependency():
    """Test khanFrontierEval with a circular dependency that has no stable state"""
    in1 = Input()
    and1 = And()
    not1 = Not()
    out1 = Output()

    in1.addOutput(and1, "input1")
    and1.addInput(in1, "outValue", "input1")

    and1.addOutput(not1, "input")
    not1.addInput(and1, "outValue", "input")

    not1.addOutput(and1, "input2")
    and1.addInput(not1, "outValue", "input2")
    not1.addOutput(out1, "input")
    out1.addInput(not1, "outValue", "input")

    in1.setState((1, 1))

    inputs = [in1]
    components = [in1, and1, not1, out1]

    assert Algorithms.khanFrontierEval(inputs, components) == False


def test_eventDrivenEval_simple():
    """Test eventDrivenEval with a simple circuit"""
    in1 = Input()
    in2 = Input()
    in3 = Input()
    and1 = And()
    or1 = Or()
    out1 = Output()

    in1.addOutput(and1, "input1")
    in2.addOutput(and1, "input2")
    and1.addInput(in1, "outValue", "input1")
    and1.addInput(in2, "outValue", "input2")

    and1.addOutput(or1, "input1")
    in3.addOutput(or1, "input2")
    or1.addInput(and1, "outValue", "input1")
    or1.addInput(in3, "outValue", "input2")

    or1.addOutput(out1, "input")
    out1.addInput(or1, "outValue", "input")

    in1.setState((1, 1))
    in2.setState((0, 1))
    in3.setState((0, 1))

    inputs = [in1, in2, in3]
    components = [in1, in2, in3, and1, or1, out1]

    assert Algorithms.eventDrivenEval(inputs, components) == True
    assert and1.getState()["outValue"] == (0, 1)
    assert or1.getState()["outValue"] == (0, 1)
    assert out1.getState()["outValue"] == (0, 1)

    in2.setState((1, 1))
    assert Algorithms.eventDrivenEval(inputs, components, startingComponents=[in2]) == True
    assert and1.getState()["outValue"] == (1, 1)
    assert or1.getState()["outValue"] == (1, 1)
    assert out1.getState()["outValue"] == (1, 1)

    in3.setState((1, 1))
    assert Algorithms.eventDrivenEval(inputs, components, startingComponents=[in3]) == True
    assert and1.getState()["outValue"] == (1, 1)
    assert or1.getState()["outValue"] == (1, 1)
    assert out1.getState()["outValue"] == (1, 1)


def test_eventDrivenEval_circular_bad_dependency():
    """Test eventDrivenEval with a circular dependency that has no stable state"""
    in1 = Input()
    and1 = And()
    not1 = Not()
    out1 = Output()

    in1.addOutput(and1, "input1")
    and1.addInput(in1, "outValue", "input1")

    and1.addOutput(not1, "input")
    not1.addInput(and1, "outValue", "input")

    not1.addOutput(and1, "input2")
    and1.addInput(not1, "outValue", "input2")
    not1.addOutput(out1, "input")
    out1.addInput(not1, "outValue", "input")

    in1.setState((1, 1))

    inputs = [in1]
    components = [in1, and1, not1, out1]

    assert Algorithms.khanFrontierEval(inputs, components) == False
    assert Algorithms.eventDrivenEval(inputs, components) == False


@pytest.mark.parametrize("a, b, expected", [
    (0, 1, 1),
    (1, 0, 0),
])
def test_eventDrivenEval_circular_good_dependency(a, b, expected):
    """Test eventDrivenEval with a circular dependency (SR latch) that has a stable state"""
    # Two Inputs
    r = Input()
    s = Input()
    # Two NOR gates
    nor1 = Nor()
    nor2 = Nor()
    # Two Outputs
    q = Output()
    notQ = Output()

    # Inputs to NORs
    r.addOutput(nor1, "input1")
    nor1.addInput(r, "outValue", "input1")
    Algorithms.eventDrivenEval([r], [r, nor1], startingComponents=[nor1])

    s.addOutput(nor2, "input2")
    nor2.addInput(s, "outValue", "input2")
    Algorithms.eventDrivenEval([s], [s, nor2], startingComponents=[nor2])

    # Mutual feedback (circular)
    nor1.addOutput(nor2, "input1")
    nor2.addInput(nor1, "outValue", "input1")
    Algorithms.eventDrivenEval([r, s], [r, s, nor1, nor2], startingComponents=[nor2])

    nor1.addInput(nor2, "outValue", "input2")
    nor2.addOutput(nor1, "input2")
    Algorithms.eventDrivenEval([r, s], [r, s, nor1, nor2], startingComponents=[nor1])

    assert nor1.getState()["outValue"] == (1, 1)
    assert nor2.getState()["outValue"] == (0, 1)

    # Outputs
    nor1.addOutput(q, "input")
    q.addInput(nor1, "outValue", "input")
    Algorithms.eventDrivenEval([r, s], [r, s, nor1, nor2, q], startingComponents=[q])

    notQ.addInput(nor2, "outValue", "input")
    nor2.addOutput(notQ, "input")
    Algorithms.eventDrivenEval([r, s], [r, s, nor1, nor2, q, notQ], startingComponents=[notQ])

    r.setState((a, 1))
    s.setState((b, 1))

    inputs = [r, s]
    components = [r, s, nor1, nor2, q, notQ]

    assert Algorithms.khanFrontierEval(inputs, components) == False
    assert Algorithms.eventDrivenEval(inputs, components) == True
    assert q.getState()["outValue"] == (expected, 1)
    assert notQ.getState()["outValue"] == (1 - expected, 1)
    
    
def test_eventDrivenEval_no_starting_components():
    """Test eventDrivenEval without starting components (should start from Inputs)"""
    in1 = Input()
    in2 = Input()
    and1 = And()
    out1 = Output()

    in1.addOutput(and1, "input1")
    in2.addOutput(and1, "input2")
    and1.addInput(in1, "outValue", "input1")
    and1.addInput(in2, "outValue", "input2")

    and1.addOutput(out1, "input")
    out1.addInput(and1, "outValue", "input")

    in1.setState((1, 1))
    in2.setState((1, 1))

    inputs = [in1, in2]
    components = [in1, in2, and1, out1]

    assert Algorithms.eventDrivenEval(inputs, components) == True
    assert and1.getState()["outValue"] == (1, 1)
    assert out1.getState()["outValue"] == (1, 1)


def test_eventDrivenEval_no_inputs_and_no_starting_components():
    """Test eventDrivenEval without inputs and starting components (should not evaluate anything)"""
    and1 = And()
    out1 = Output()

    assert Algorithms.eventDrivenEval([], [and1, out1]) == False
    assert and1.getState()["outValue"] == (0, 1)
    assert out1.getState()["outValue"] == (0, 0)
    
def test_eventDrivenEval_with_kw_starting_components():
    """Test eventDrivenEval with starting components provided via kwarg"""
    in1 = Input()
    in2 = Input()
    and1 = And()
    out1 = Output()

    in1.addOutput(and1, "input1")
    in2.addOutput(and1, "input2")
    and1.addInput(in1, "outValue", "input1")
    and1.addInput(in2, "outValue", "input2")

    and1.addOutput(out1, "input")
    out1.addInput(and1, "outValue", "input")

    in1.setState((1, 1))
    in2.setState((1, 1))

    inputs = [in1, in2]
    components = [in1, in2, and1, out1]

    assert Algorithms.eventDrivenEval(inputs, components, startingComponents=[and1]) == True
    assert and1.getState()["outValue"] == (1, 1)
    assert out1.getState()["outValue"] == (1, 1)
    
def test_eventDrivenEval_with_ProgramCounter_start():
    """Test eventDrivenEval starting from ProgramCounter components when no startingComponents are provided"""
    from src.model.ProgramCounter import ProgramCounter

    pc = ProgramCounter()
    out1 = Output()

    pc.addInput(DummyInput(8, 32), "outValue", "input")
    pc.addOutput(out1, "outValue")
    out1.addInput(pc, "outValue", "input")


    inputs = []
    components = [pc, out1]

    assert Algorithms.eventDrivenEval(inputs, components) == True
    assert pc.getState()["outValue"] == (8, 32)
    assert out1.getState()["outValue"] == (8, 32)
    
    
def test_eventDrivenEval_with_PC_and_instruction_memory():
    """Test eventDrivenEval with ProgramCounter and InstructionMemory components"""
    from src.model.ProgramCounter import ProgramCounter
    from src.model.InstructionMemory import InstructionMemory

    pc = ProgramCounter()
    im = InstructionMemory()

    pc.addInput(im, "instruction", "input")
    im.addOutput(pc, "input")
    
    im.addInput(pc, "outValue", "readAddress")
    pc.addOutput(im, "readAddress")

    im.loadInstructions([4,8,12,16,20,24,28,32,32]) # Sample instructions

    inputs = []
    components = [pc, im]
    im.eval()
    assert pc.getState()["outValue"] == (0, 32)
    assert im.getState()["instruction"] == (4, 32)
    
    assert Algorithms.eventDrivenEval(inputs, components)
    assert pc.getState()["outValue"] == (32, 32)
    assert im.getState()["instruction"] == (32, 32)


def test_eventDrivenEval_with_PC_and_instruction_memory_many_instructions():
    """Test eventDrivenEval with ProgramCounter and InstructionMemory components"""
    from src.model.ProgramCounter import ProgramCounter
    from src.model.InstructionMemory import InstructionMemory

    pc = ProgramCounter()
    im = InstructionMemory()

    pc.addInput(im, "instruction", "input")
    im.addOutput(pc, "input")
    
    im.addInput(pc, "outValue", "readAddress")
    pc.addOutput(im, "readAddress")
    
    
    instructions = [i for i in range(4, 1000, 4)] + [996,996]
    im.loadInstructions(instructions) # Sample instructions

    inputs = []
    components = [pc, im]
    im.eval()
    assert pc.getState()["outValue"] == (0, 32)
    assert im.getState()["instruction"] == (4, 32)
    
    assert Algorithms.eventDrivenEval(inputs, components)
    assert pc.getState()["outValue"] == (996, 32)
    assert im.getState()["instruction"] == (996, 32)
    
