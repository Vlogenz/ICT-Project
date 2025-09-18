import pytest
from src.control.LogicComponentController import LogicComponentController
from src.model.LogicComponent import LogicComponent
from src.model.Input import Input
from src.model.And import And
from src.model.Or import Or
from src.model.Output import Output
from src.model.Not import Not

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
    
    in1.addOutput(and1)
    in2.addOutput(and1)
    and1.addInput(in1)
    and1.addInput(in2)
    
    and1.addOutput(or1)
    in3.addOutput(or1)
    or1.addInput(and1)
    or1.addInput(in3)
    
    or1.addOutput(out1)
    out1.addInput(or1)
    
    in1.setState( (1,1))
    in2.setState( (0,1))
    
    assert lC.khanFrontierEval() == True
    assert and1.getState() ==  (0,1)
    assert or1.getState() ==  (0,1)
    assert out1.getState() ==  (0,1)
    
    in2.setState( (1,1))
    assert lC.khanFrontierEval() == True
    assert and1.getState() ==  (1,1)
    assert or1.getState() ==  (1,1)
    assert out1.getState() ==  (1,1)
    
    assert len(lC.updateInTick[0]) == 3
    assert len(lC.updateInTick[1]) == 1
    assert len(lC.updateInTick[2]) == 1
    assert len(lC.updateInTick[3]) == 1
    
    
# def test_eventDrivenEval():
#     in1 = lC.addLogicComponent(Input)
#     in2 = lC.addLogicComponent(Input)
#     in3 = lC.addLogicComponent(Input)
#     and1 = lC.addLogicComponent(And)
#     or1 = lC.addLogicComponent(Or)
#     out1 = lC.addLogicComponent(Output)
    
#     in1.addOutput(and1)
#     in2.addOutput(and1)
#     and1.addInput(in1)
#     and1.addInput(in2)
    
#     and1.addOutput(or1)
#     in3.addOutput(or1)
#     or1.addInput(and1)
#     or1.addInput(in3)
    
#     or1.addOutput(out1)
#     out1.addInput(or1)
    
#     in1.setState( (1,1))
#     in2.setState( (0,1))
#     in3.setState( (0,1))
    
#     assert lC.eventDrivenEval() == True
#     assert and1.getState() ==  (0,1)
#     assert or1.getState() ==  (0,1)
#     assert out1.getState() ==  (0,1)
    
#     in2.setState( (1,1))
#     assert lC.eventDrivenEval([in2]) == True
#     assert and1.getState() ==  (1,1)
#     assert or1.getState() ==  (1,1)
#     assert out1.getState() ==  (1,1)
    
#     in3.setState( (1,1))
#     assert lC.eventDrivenEval([in3]) == True
#     assert and1.getState() ==  (1,1)
#     assert or1.getState() ==  (1,1)
#     assert out1.getState() ==  (1,1)

# def test_eventDrivenEvalCircularBadDependency():
#     in1 = lC.addLogicComponent(Input)
#     and1 = lC.addLogicComponent(And)
#     not1 = lC.addLogicComponent(Not)
#     out1 = lC.addLogicComponent(Output)
    
#     in1.addOutput(and1)
#     and1.addInput(in1)
    
#     and1.addOutput(not1)
#     not1.addInput(and1)
    
#     not1.addOutput(and1)
#     and1.addInput(not1)
#     not1.addOutput(out1)
#     out1.addInput(not1)
    
#     in1.setState( (1,1))
    
#     assert lC.khanFrontierEval() == False
#     assert lC.eventDrivenEval() == False
    
    