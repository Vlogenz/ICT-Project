from abc import ABC, abstractmethod
import typing

class LogicComponent(ABC):
    
    id = 0
    
    def __init__(self):
        
        self.inputs: typing.Dict = {} #list of tupels
        self.outputs: typing.List[("LogicComponent",str)] = []
        self.id = LogicComponent.id
        LogicComponent.id +=1
        # Default state for components with one output: (0,1) = (value, bitlength)
        self.state: dict = {}  

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
    def addInput(self, input: "LogicComponent", key: str, internelKey: str):
        if internelKey in self.inputs and self.inputs[internelKey] is None:
            self.inputs[internelKey] = (input,key)
        else:
            raise KeyError(f"Key {internelKey} not found in inputs or already occupied.")  
        

    def removeInput(self, input: "LogicComponent", key:str, internelKey: str):        
        if internelKey in self.inputs and self.inputs[internelKey] == (input,key):
            self.inputs[internelKey] = None
        else:
            raise KeyError(f"Key {internelKey} not found in inputs or input does not match.")

    def getOutputs(self) -> typing.List["LogicComponent"]:
        return self.outputs
    
    def addOutput(self, output: "LogicComponent", key: str):
        self.outputs.append((output,key))
    
    def removeOutput(self, input: "LogicComponent", key:str):
        if (input,key) in self.outputs:
            self.outputs.remove((input,key))

    def getState(self):
        return self.state
    
    def __hash__(self):
        return self.id