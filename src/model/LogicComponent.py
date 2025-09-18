from abc import ABC, abstractmethod
import typing

class LogicComponent(ABC):
    
    id = 0
    
    def __init__(self):

        self.state: bool = False
        self.inputs: typing.List["LogicComponent"] = []
        self.outputs: typing.List["LogicComponent"] = []
        self.id = LogicComponent.id
        LogicComponent.id +=1
        # Default state for components with one output: (0,1) = (value, bitlength)
        self.state: dict = {"outValue": (0,1)}  

    # Implementation left to the subclasses
    @abstractmethod
    def eval(self) -> bool:
        pass

    # TODO: Implement sprite handling
    def getSprite(self) -> None:
        pass

    def getInputs(self) -> typing.List["LogicComponent"]:
        return self.inputs
    
    #if amount of inputs is restricted, it has to be implmenented in the subclass
    def addInput(self, input: "LogicComponent"):
        self.inputs.append(input)

    def getOutputs(self) -> typing.List["LogicComponent"]:
        return self.outputs
    
    def addOutput(self, output: "LogicComponent"):
        self.outputs.append(output)

    def getState(self):
        return self.state
    
    def __hash__(self):
        return self.id