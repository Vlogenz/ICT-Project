import typing

from src.Algorithms import Algorithms
from src.model import DataMemory, InstructionMemory, ProgramCounter
from src.model.CustomLogicComponent import CustomLogicComponent
from src.model.CustomLogicComponentData import CustomLogicComponentData
from src.model.Output import Output
from src.model.LogicComponent import LogicComponent
from src.model.Input import Input
from src.infrastructure.eventBus import getBus
from src.model.RegisterBlock import RegisterBlock
from PySide6.QtCore import QTimer, QEventLoop

class LogicComponentController:    
    
    def __init__(self):
        self.components: typing.List["LogicComponent"] = []
        self.inputs: typing.List["Input"] = []
        self.outputs: typing.List["LogicComponent"] = []
        self.updateInTick: typing.Dict = {}
        # tickLength defaults to 0, i.e. the evaluation happens instantly
        self.tickLength = 0
        self.bus = getBus()
        # Registrierung: ab jetzt wird der Handler automatisch aufgerufen
        self.bus.subscribe("model:input_changed", self.onModelInputUpdate)
        self.bus.subscribe("newCycle", self.updateRegisters)
        self.registerBlock = None
        self.instructionMemory = None
        self.dataMemory = None
    
    
    def updateComponents(self, **tickList) -> None:
        """updates all or selected components
        
        optional Arguments:
            components= List of components which has to be updated
        """
        componentsToUpdate = tickList["components"]
        if len(componentsToUpdate) == 0:
            componentsToUpdate = self.components
        self.bus.emit("view:components_updated", componentsToUpdate)

    def _waitWithEventLoop(self) -> None:
        """Wait for the amount of seconds specified by self.tickLength while processing Qt events to keep GUI responsive"""
        if self.tickLength > 0:
            loop = QEventLoop()
            QTimer.singleShot(int(self.tickLength * 1000), loop.quit)
            loop.exec()


    def eval(self) -> bool:
        """Evaluates all the components in order.
        
        Returns:
          Bool: True if evaluation was successful, false if not.
        """
        # We currently do not know why the manual mode was here.
        # Using it prevented the view:components_updated event from emitting.
        # I just left it commented out so we can use it just in case.
        #getBus().setManual()
        self.bus.emit("logic:instruction_count",len(self.instructionMemory.instructionList) if self.instructionMemory is not None else 0)
        if Algorithms.khanFrontierEval(self.inputs, self.components, self.updateComponents, self._waitWithEventLoop):
            self.updateRegisters()
            getBus().setAuto()
            return True
        elif Algorithms.eventDrivenEval(self.inputs, self.components, self.updateComponents, self._waitWithEventLoop):
            self.updateRegisters()
            getBus().setAuto()
            return True
        else:
            return False


    def getInputs(self) -> typing.List[Input]:
        return self.inputs

    def getOutputs(self) -> typing.List[LogicComponent]:
        return self.outputs
    
    T = typing.TypeVar("T",bound=LogicComponent)
    def addLogicComponent(self, component: typing.Type[T]) -> T:
        """creates a new component of given type

        Args:
            component (typing.Type[T]): type of component which shoud be created

        Returns:
            LogicComponent: the new component 
        """
        comp = component()
        self.components.append(comp)
        if type(comp) == Input:
            self.inputs.append(comp)
        if type(comp) == Output:
            self.outputs.append(comp)
        if type(comp) == RegisterBlock:
            if self.registerBlock is None:
                self.registerBlock = comp
            else:
                return None
        if type(comp) == InstructionMemory:
            if self.instructionMemory is None:
                self.instructionMemory = comp
            else:
                return None
        if type(comp) == DataMemory:
            if self.dataMemory is None:
                self.dataMemory = comp
            else:
                return None
            
        
        return comp

    def addCustomLogicComponent(self, componentData: CustomLogicComponentData) -> LogicComponent:
        """Adds a custom logic component by adding all native subcomponents.

        Returns:
            LogicComponent: the new component
        """
        comp = CustomLogicComponent(componentData)
        self.components.append(comp)
        return comp


    def removeLogicComponent(self, component:LogicComponent) -> None:
        """removes a component from controller

        Args:
            component (LogicComponent): the component to remove

        Raises:
            ReferenceError: If component was not present in the controllers list
        """
        if component in self.components:
            # remove all connections to and from this component
            
            # Remove the component from the inputs' outputs
            for inputKey, origin in component.getInputs().items():
                if origin is not None:
                    origin[0].removeOutput(component, inputKey)
            
            for output in component.getOutputs():
                # Remove the input from the output's inputs
                # output[0] is the target component, output[1] is the target key
                # output[0].getInputs()[output[1]] is the internal state key
                output[0].removeInput(component, output[0].getInputs()[output[1]][1], output[1])

            self.components.remove(component)
            if type(component) == Input:
                self.inputs.remove(component)
            if type(component) == Output:
                self.outputs.remove(component)
            if type(component) == RegisterBlock:
                self.registerBlock = None
            if type(component) == InstructionMemory:
                self.instructionMemory = None
            if type(component) == DataMemory:
                self.dataMemory = None
            if type(component) == ProgramCounter:
                self.bus.unsubscribe("logic:instruction_count", component.onInstructionCount)
        else:
            raise ReferenceError("Can't remove non existent component from controller")


    def getComponents(self) -> typing.List[LogicComponent]:
        return self.components

    def onModelInputUpdate(self, model: LogicComponent) -> None:
        """uses the eventdriveneval to update starting from a changed component

        Args:
            model (LogicComponent): changed component
        """
        Algorithms.eventDrivenEval(self.inputs, self.components, self.updateComponents, self._waitWithEventLoop, startingComponents=[model])

    def setTickLength(self, length: float) -> None:
        """sets the tick length for evaulation in seconds

        Args:
            length (float): The tick length in seconds
        """
        self.tickLength = length
        
    def addConnection(self, origin: "LogicComponent", originKey: str, target: "LogicComponent", targetKey: str) -> bool:
        """
        Adds a connection from the origin component to the target component.
        Args:
            origin (LogicComponent): The component where the connection starts.
            originKey (str): The key of the output from the origin component.
            target (LogicComponent): The component where the connection ends.
            targetKey (str): The key of the input on the target component.
        Returns:
            bool: True if the connection was added successfully, False otherwise.  
            """
        if target.getBitwidth(targetKey) == 0 or origin.getState()[originKey][1] == target.getBitwidth(targetKey):
            #check if bitlengths of inputs and output are thesame or if input has bitlength 0 (means bitlength hasnt been set yet)
            if target.addInput(origin, originKey, targetKey):
                origin.addOutput(target, targetKey)
                return True
            return False
        else:
            print("Bitwidth was incompatible")
            return False


    def removeConnection(self, origin: "LogicComponent", originKey: str, target: "LogicComponent", targetKey: str) -> None:
        """
        Removes a connection from the origin component to the target component.
        Args:
            origin (LogicComponent): The component where the connection starts.
            originKey (str): The key of the output from the origin component.
            target (LogicComponent): The component where the connection ends.
            targetKey (str): The key of the input on the target component.
        """
        origin.removeOutput(target, targetKey)
        target.removeInput(origin, originKey, targetKey)


    def updateRegisters(self) -> None:
        """ Updates all registers and evaluates the circuit starting from the outputs of the registers.
        """
        componentsToUpdate = []
        for comp in self.components:
            if hasattr(comp, "updateState"):
                comp.updateState()
                # collect all components which are connected to the output of the register
                componentsToUpdate.extend([out[0] for out in comp.getOutputs()])
            if type(comp) == RegisterBlock:
                comp.updateRegisterValues()
                
                
        componentsToUpdate = list(set(componentsToUpdate))
        Algorithms.eventDrivenEval(self.inputs, self.components, self.updateComponents, self._waitWithEventLoop, startingComponents=componentsToUpdate)

    def clearComponents(self) -> None:
        """Removes all components from the controller
        """
        self.components.clear()
        self.inputs.clear()
        self.outputs.clear()
        self.updateInTick.clear()
        self.registerBlock = None
        self.instructionMemory = None
        self.dataMemory = None
        self.bus.emit("view:components_cleared")
