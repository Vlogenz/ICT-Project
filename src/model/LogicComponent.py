from abc import ABC, abstractmethod
import typing
from src.infrastructure.eventBus import getBus

class LogicComponent(ABC):
    
    id = 0
    
    def __init__(self):
        
        self.inputs: typing.Dict = {} #internalKey where a input is connected to and tupels of inputs and the key of the inputs output (important for the controllers algorithms)
        self.outputs: typing.List[("LogicComponent",str)] = [] # list of tupels of outputs and the key they are connected to (important for the controllers algorithms)
        self.id = LogicComponent.id
        LogicComponent.id +=1
        # Default state for components with one output: (0,1) = (value, bitlength)
        self.state: dict = {}
        self.bus = getBus()

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
    def addInput(self, input: "LogicComponent", key: str, internalKey: str):
        """
        Add an input connection to this component.
        Args:
            input (LogicComponent): The input component to be added.
            key (str): The key of the output from the input component that is connected.
            internalKey (str): The internal key of this component where the input is connected.
        Raises:
            KeyError: If the internalKey is not found in inputs or already occupied.
        """
        if internalKey in self.inputs and self.inputs[internalKey] is None:
            self.inputs[internalKey] = (input,key)
            self.bus.emit("model:input_changed",self)
        else:
            raise KeyError(f"Key {internalKey} not found in inputs or already occupied.")  
        

    def removeInput(self, input: "LogicComponent", key:str, internalKey: str):
        """
        Remove an input connection from this component.
        Args:
            input (LogicComponent): The input component to be removed.
            key (str): The key of the output from the input component that is connected.
            internalKey (str): The internal key of this component where the input is connected.
        Raises:
            KeyError: If the internalKey is not found in inputs or the input does not match"""     
        if internalKey in self.inputs and self.inputs[internalKey] == (input,key):
            self.inputs[internalKey] = None
        else:
            raise KeyError(f"Key {internalKey} not found in inputs or input does not match.")

    def getOutputs(self) -> typing.List["LogicComponent"]:
        return self.outputs
    
    def addOutput(self, output: "LogicComponent", key: str):
        """Add an output connection to this component

        Args:
            output (LogicComponent): the outputcomponent to be added
            key (str): the key of the input from the output component
        """
        self.outputs.append((output,key))
    
    def removeOutput(self, output: "LogicComponent", key:str):
        """Remove an output connection from this component

        Args:
            output (LogicComponent): the output component to be removed 
            key (str): the input key of the output component
        """
        if (output,key) in self.outputs:
            self.outputs.remove((output,key))

    def getState(self):
        return self.state
    
    def __hash__(self):
        return self.id