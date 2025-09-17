import typing

from model.LogicComponent import LogicComponent
from model.Input import Input
from model.GlobalConstants import MAX_EVAL_CYCLES

class LogicComponentController:    
    
    def __init__(self):
        self.components: typing.List["LogicComponent"] = []
        self.inputs: typing.List["Input"] = []
        self.updateInTick: typing.Dict = {}
    
    
    def updateComponents(self, **kw):
        """updates all or selected components
        
        optional Arguments:
            components= List of components which has to be updated
        """
        componentsToUpdate = []
        componentsToUpdate = kw["components"]
        if len(componentsToUpdate) == 0:
            componentsToUpdate = self.components
        for comp in self.components:
            # TODO UI update
            pass
    
    def khanFrontierEval(self):
        """evaluates all the components in topological order
           if there are no circular dependencies

        Returns:
            bool: if evaluation was successful or not
        """
        tick = 0
        indeg = {}
        for comp in self.components:
            indeg[comp] = len(comp.getInputs())
        
        currentTick = self.inputs.copy()
        while len(currentTick) > 0:
            self.updateInTick[tick] = currentTick.copy()
            nextTick = []
            for u in currentTick:
                for v in u.getOutputs():
                    indeg[v] -= 1
                    if indeg[v] == 0:
                        nextTick.append(v)
            currentTick = nextTick
            tick +=1
        
        sumIndeg = 0
        for comp in indeg:
            sumIndeg += indeg[comp]
        
        if sumIndeg > 0:
            return False
        else:
            for tick in self.updateInTick:
                for comp in self.updateInTick[tick]:
                    comp.eval()
                self.updateComponents(self.updateInTick[tick])
                #TODO maybe a short sleep
            return True
        
    
    def eventDrivenEval(self, **kw: typing.List["LogicComponent"]):
        """evaluates components eventdriven (starting from one (or multiple) Components in waves)

        Args:
            startingComponents (typing.List[&quot;LogicComponent&quot;]): Optional List of components from which to start 
            if not deliverd function will use the inputs as this list and evaluates everything

        Returns:
            bool: wether evaluation was successful or not
        """
        tick = 0
        currentTick = kw["startingComponents"]
        if len(currentTick) == 0:
            currentTick = self.inputs.copy()
        while len(currentTick)>0:
            nextTick = []
            for g in currentTick:
                if g.eval():
                    for out in g.getOutputs():
                        nextTick.append(out)
            
            
            self.updateComponents(currentTick)
            #TODO short sleep
            currentTick = nextTick
            tick +=1
            
            if tick > MAX_EVAL_CYCLES:
                return False
        return True
            
                        
    def eval(self):
        """Evaluates all the components in order.
        
        Returns:
          Bool: True if evaluation was successful, false if not.
        """
        if self.khanFrontierEval():
            return True
        elif self.eventDrivenEval():
            return True
        else:
            return False
        
        
    def getInputs(self):
        return self.inputs
    
    T = typing.TypeVar("T",bound=LogicComponent)
    def addLogicComponent(self, component: typing.Type[T]):
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
        
        return comp
    
    
    def removeLogicComponent(self, component:LogicComponent):
        """removes a component from controller

        Args:
            component (LogicComponent): the component to remove

        Raises:
            ReferenceError: If component was not present in the controllers list
        """
        if component in self.components:
            self.components.remove(component)
            if type(component) == Input:
                self.inputs.remove(component)
        else:
            raise ReferenceError("Can't remove non existent component from controller")