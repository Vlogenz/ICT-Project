import pytest
from src.control.LogicComponentController import LogicComponentController
from src.model.LogicComponent import LogicComponent
from src.model.Input import Input
from src.model.And import And
from src.model.Or import Or
from src.model.Output import Output
from src.model.Not import Not
from src.model.Nor import Nor

@pytest.fixture
def lC(): 
    return LogicComponentController()
    

def test_addLogicComponent(lC):
    assert lC.getInputs() == []
    assert lC.getComponents() == []
    
    lC.addLogicComponent(Input)
    assert len(lC.getInputs()) == 1
    assert len(lC.getComponents()) == 1
    
    lC.addLogicComponent(And)
    assert len(lC.getComponents()) == 2
    assert len(lC.getInputs()) == 1
    
    
def test_removeLogicComponent(lC):
    
    in1 = lC.addLogicComponent(Input)
    in2 = lC.addLogicComponent(Input)
    and1 = lC.addLogicComponent(And)
    lC.addLogicComponent(Or)
    lC.addLogicComponent(Output)
    
    assert len(lC.getComponents()) == 5
    assert len(lC.getInputs()) == 2
    
    lC.removeLogicComponent(and1)
    assert len(lC.getComponents()) == 4
    assert len(lC.getInputs()) == 2
    
    lC.removeLogicComponent(in1)
    assert len(lC.getComponents()) == 3
    assert len(lC.getInputs()) == 1
    
    with pytest.raises(ReferenceError):
        lC.removeLogicComponent(and1)
    

def test_khanFrontierEval(lC):
    in1 = lC.addLogicComponent(Input)
    in2 = lC.addLogicComponent(Input)
    in3 = lC.addLogicComponent(Input)
    and1 = lC.addLogicComponent(And)
    or1 = lC.addLogicComponent(Or)
    out1 = lC.addLogicComponent(Output)
    
    in1.addOutput(and1,"input1")
    in2.addOutput(and1,"input2")
    and1.addInput(in1,"outValue","input1")
    and1.addInput(in2,"outValue","input2")
    
    and1.addOutput(or1,"input1")
    in3.addOutput(or1,"input2")
    or1.addInput(and1,"outValue","input1")
    or1.addInput(in3,"outValue","input2")
    
    or1.addOutput(out1,"input")
    out1.addInput(or1,"outValue","input")
    
    in1.setState((1,1))
    in2.setState((0,1))
    
    assert lC.khanFrontierEval() == True
    assert and1.getState()["outValue"] ==  (0,1)
    assert or1.getState()["outValue"] ==  (0,1)
    assert out1.getState()["outValue"] ==  (0,1)
    
    in2.setState((1,1))
    assert lC.khanFrontierEval() == True
    assert and1.getState()["outValue"] ==  (1,1)
    assert or1.getState()["outValue"] ==  (1,1)
    assert out1.getState()["outValue"] ==  (1,1)
    
    assert len(lC.updateInTick[0]) == 3
    assert len(lC.updateInTick[1]) == 1
    assert len(lC.updateInTick[2]) == 1
    assert len(lC.updateInTick[3]) == 1
    
    
def test_eventDrivenEval(lC):
    in1 = lC.addLogicComponent(Input)
    in2 = lC.addLogicComponent(Input)
    in3 = lC.addLogicComponent(Input)
    and1 = lC.addLogicComponent(And)
    or1 = lC.addLogicComponent(Or)
    out1 = lC.addLogicComponent(Output)
    
    in1.addOutput(and1,"input1")
    in2.addOutput(and1,"input2")
    and1.addInput(in1,"outValue","input1")
    and1.addInput(in2,"outValue","input2")
    
    and1.addOutput(or1,"input1")
    in3.addOutput(or1,"input2")
    or1.addInput(and1,"outValue","input1")
    or1.addInput(in3,"outValue","input2")
    
    or1.addOutput(out1,"input")
    out1.addInput(or1,"outValue","input")
    
    in1.setState( (1,1))
    in2.setState( (0,1))
    in3.setState( (0,1))
    
    assert lC.eventDrivenEval() == True
    assert and1.getState()["outValue"] ==  (0,1)
    assert or1.getState()["outValue"] ==  (0,1)
    assert out1.getState()["outValue"] ==  (0,1)
    
    in2.setState( (1,1))
    assert lC.eventDrivenEval(startingComponents=[in2]) == True
    assert and1.getState()["outValue"] ==  (1,1)
    assert or1.getState()["outValue"] ==  (1,1)
    assert out1.getState()["outValue"] ==  (1,1)
    
    in3.setState( (1,1))
    assert lC.eventDrivenEval(startingComponents=[in3]) == True
    assert and1.getState()["outValue"] ==  (1,1)
    assert or1.getState()["outValue"] ==  (1,1)
    assert out1.getState()["outValue"] ==  (1,1)

def test_eventDrivenEvalCircularBadDependency(lC):
    in1 = lC.addLogicComponent(Input)
    and1 = lC.addLogicComponent(And)
    not1 = lC.addLogicComponent(Not)
    out1 = lC.addLogicComponent(Output)
    
    in1.addOutput(and1,"input1")
    and1.addInput(in1,"outValue","input1")
    
    and1.addOutput(not1,"input")
    not1.addInput(and1,"outValue","input")
    
    not1.addOutput(and1,"input2")
    and1.addInput(not1,"outValue","input2")
    not1.addOutput(out1,"input")
    out1.addInput(not1,"outValue","input")
    
    in1.setState((1,1))
    
    assert lC.khanFrontierEval() == False
    assert lC.eventDrivenEval() == False
    
@pytest.mark.parametrize("a, b, expected", [
 (0, 1, 1),	
 (1, 0, 0),
	
])
def test_eventDrivenEvalCircularGoodDependency(lC,a,b,expected):
    # Zwei Inputs
    r = lC.addLogicComponent(Input)
    s = lC.addLogicComponent(Input)
    # Zwei AND-Gates
    nor1 = lC.addLogicComponent(Nor)
    nor2 = lC.addLogicComponent(Nor)
    # Zwei Outputs
    q = lC.addLogicComponent(Output)
    notQ = lC.addLogicComponent(Output)

    # Inputs an ANDs
    r.addOutput(nor1, "input1")
    nor1.addInput(r, "outValue", "input1")
    lC.eventDrivenEval(startingComponents=[nor1])
    s.addOutput(nor2, "input2")
    nor2.addInput(s, "outValue", "input2")
    lC.eventDrivenEval(startingComponents=[nor2])

    # Gegenseitige Rückkopplung (Kreis)
    nor1.addOutput(nor2, "input1")
    nor2.addInput(nor1, "outValue", "input1")
    lC.eventDrivenEval(startingComponents=[nor2])
    
    nor1.addInput(nor2, "outValue", "input2")
    nor2.addOutput(nor1, "input2")
    lC.eventDrivenEval(startingComponents=[nor1])
    # Outputs(0, 0, 0),
    
    assert nor1.getState()["outValue"] == (1,1)
    assert nor2.getState()["outValue"] == (0,1)
    
    
    nor1.addOutput(q, "input")
    q.addInput(nor1, "outValue", "input")
    lC.eventDrivenEval(startingComponents=[q])
    notQ.addInput(nor2, "outValue", "input")
    nor2.addOutput(notQ, "input")
    lC.eventDrivenEval(startingComponents=[notQ])
    
    
    r.setState( (a,1))
    s.setState( (b,1))
    
    assert lC.khanFrontierEval() == False
    assert lC.eventDrivenEval() == True
    assert q.getState()["outValue"] == (expected,1)
    assert notQ.getState()["outValue"] == (1-expected,1)
    
    
def test_eva1(lC):
    in1 = lC.addLogicComponent(Input)
    in2 = lC.addLogicComponent(Input)
    in3 = lC.addLogicComponent(Input)
    and1 = lC.addLogicComponent(And)
    or1 = lC.addLogicComponent(Or)
    out1 = lC.addLogicComponent(Output)
    
    in1.addOutput(and1,"input1")
    in2.addOutput(and1,"input2")
    and1.addInput(in1,"outValue","input1")
    and1.addInput(in2,"outValue","input2")
    
    and1.addOutput(or1,"input1")
    in3.addOutput(or1,"input2")
    or1.addInput(and1,"outValue","input1")
    or1.addInput(in3,"outValue","input2")
    
    or1.addOutput(out1,"input")
    out1.addInput(or1,"outValue","input")
    
    in1.setState( (1,1))
    in2.setState( (0,1))
    in3.setState( (0,1))
    
    assert lC.eval() == True
    assert and1.getState()["outValue"] ==  (0,1)
    assert or1.getState()["outValue"] ==  (0,1)
    assert out1.getState()["outValue"] ==  (0,1)
    
    in2.setState( (1,1))
    assert lC.eval() == True
    assert and1.getState()["outValue"] ==  (1,1)
    assert or1.getState()["outValue"] ==  (1,1)
    assert out1.getState()["outValue"] ==  (1,1)
    
    in3.setState( (1,1))
    assert lC.eval() == True
    assert and1.getState()["outValue"] ==  (1,1)
    assert or1.getState()["outValue"] ==  (1,1)
    assert out1.getState()["outValue"] ==  (1,1)
    

def test_eval2(lC):
    # Zwei Inputs
    r = lC.addLogicComponent(Input)
    s = lC.addLogicComponent(Input)
    # Zwei AND-Gates
    nor1 = lC.addLogicComponent(Nor)
    nor2 = lC.addLogicComponent(Nor)
    # Zwei Outputs
    q = lC.addLogicComponent(Output)
    notQ = lC.addLogicComponent(Output)

    # Inputs an ANDs
    r.addOutput(nor1, "input1")
    nor1.addInput(r, "outValue", "input1")
    lC.eventDrivenEval(startingComponents=[nor1])
    s.addOutput(nor2, "input2")
    nor2.addInput(s, "outValue", "input2")
    lC.eventDrivenEval(startingComponents=[nor2])

    # Gegenseitige Rückkopplung (Kreis)
    nor1.addOutput(nor2, "input1")
    nor2.addInput(nor1, "outValue", "input1")
    lC.eventDrivenEval(startingComponents=[nor2])
    
    nor1.addInput(nor2, "outValue", "input2")
    nor2.addOutput(nor1, "input2")
    lC.eventDrivenEval(startingComponents=[nor1])
    # Outputs(0, 0, 0),
    
    assert nor1.getState()["outValue"] == (1,1)
    assert nor2.getState()["outValue"] == (0,1)
    
    
    nor1.addOutput(q, "input")
    q.addInput(nor1, "outValue", "input")
    lC.eventDrivenEval(startingComponents=[q])
    notQ.addInput(nor2, "outValue", "input")
    nor2.addOutput(notQ, "input")
    lC.eventDrivenEval(startingComponents=[notQ])
    
    
    r.setState( (1,1))
    s.setState( (0,1))
    
    assert lC.eval() == True
    assert q.getState()["outValue"] == (0,1)
    assert notQ.getState()["outValue"] == (1,1)
    
def test_eval3(lC): 
    in1 = lC.addLogicComponent(Input)
    and1 = lC.addLogicComponent(And)
    not1 = lC.addLogicComponent(Not)
    out1 = lC.addLogicComponent(Output)
    
    in1.addOutput(and1,"input1")
    and1.addInput(in1,"outValue","input1")
    
    and1.addOutput(not1,"input")
    not1.addInput(and1,"outValue","input")
    
    not1.addOutput(and1,"input2")
    and1.addInput(not1,"outValue","input2")
    not1.addOutput(out1,"input")
    out1.addInput(not1,"outValue","input")
    
    in1.setState((1,1))
    
    assert lC.eval() == False