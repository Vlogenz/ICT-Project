import pytest
from src.model.LogicComponent import LogicComponent
from src.model.Xor import Xor
from src.model.Input import Input
from src.infrastructure.eventBus import EventBus,getBus
from src.control.LogicComponentController import LogicComponentController

def test_getBus():
    b = getBus()
    assert b == getBus()
    
def test_subscriptionAndEmmiting():
    getBus().setAuto()
    lC = LogicComponentController()
    
    in1 = lC.addLogicComponent(Input)
    in1.setState((1,1))
    
    in2 = lC.addLogicComponent(Input)
    in2.setState((1,1))
    
    xor = lC.addLogicComponent(Xor)
    assert xor.getState()["outValue"] == (0,1)
    
    in1.addOutput(xor,"input1")
    xor.addInput(in1,"outValue","input1")
    assert xor.getState()["outValue"] == (1,1)

    in2.addOutput(xor,"input2")
    xor.addInput(in2,"outValue","input2")
    assert xor.getState()["outValue"] == (0,1)
    
    in1.removeOutput(xor,"input1")
    xor.removeInput(in1,"outValue","input1")
    assert xor.getState()["outValue"] == (1,1)
    
    in2.removeOutput(xor,"input2")
    xor.removeInput(in2,"outValue","input2")
    assert xor.getState()["outValue"] == (0,1)