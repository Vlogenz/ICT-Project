from abc import ABC, abstractmethod
import typing

class LogicComponent(ABC):
    def __init__(self):
        self.state: bool = False
        self.inputs: typing.List["LogicComponent"] = []
        self.outputs: typing.List["LogicComponent"] = []

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

   