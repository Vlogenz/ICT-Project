import typing
from src.model import Input, InstructionMemory, ProgramCounter, Register
from src.constants import MAX_EVAL_CYCLES

class Algorithms:
    """
    A class that encapsulates the evaluation algorithms for logic circuits.
    """

    @staticmethod
    def khanFrontierEval(inputs, components, updateFunction = None, waitFunction = None):
        """evaluates all the components in topological order
           if there are no circular dependencies

        Returns:
            bool: if evaluation was successful or not
        """
        tick = 0
        indeg = {}  # indegree of each component
        for comp in components:
            if type(comp) != Input:
                # create a list of all components which are inputs to this component
                compo = [tuple[0] for tuple in comp.inputs.values() if tuple is not None and type(tuple[0]) != Register]
                indeg[comp] = len(set(compo))  # count only unique components

        currentTick = inputs.copy()  # start with inputs
        updateInTick: typing.Dict = {}
        while len(currentTick) > 0:  # while there are still components to process
            updateInTick[tick] = currentTick.copy()  # store current components in tick dictionary
            nextTick = []  # list of components for next tick
            for u in currentTick:
                vs = [tuple[0] for tuple in u.getOutputs()]  # get all components which are outputs of current component
                for v in vs:
                    indeg[v] -= 1  # decrease indegree of output component
                    if indeg[v] == 0:  # if indegree is 0, add to next tick
                        nextTick.append(v)
            # move to next tick
            currentTick = nextTick
            tick += 1  # increase tick count

        # if there are still components with indegree > 0, there is a circular dependency
        if sum(indeg.values()) > 0:
            return False
        else:
            # evaluate components tick by tick
            for tick in updateInTick:
                for comp in updateInTick[tick]:
                    comp.eval()
                if updateFunction is not None:
                    updateFunction(components=updateInTick[tick])
                if waitFunction is not None:
                    waitFunction()
            return True

    @staticmethod
    def eventDrivenEval(inputs, components, updateFunction=None, waitFunction = None, **kw: typing.List["LogicComponent"]):
        """evaluates components eventdriven (starting from one (or multiple) Components in waves)

        Args:
            startingComponents (typing.List[&quot;LogicComponent&quot;]): Optional List of components from which to start
            if not deliverd function will use the inputs as this list and evaluates everything. If there are no Inputs, it will start
            from the ProgramCounter(s)

        Returns:
            bool: wether evaluation was successful or not
        """
        
        maxEvaluationCycles = len(components)
        instructionMemory = None
        for comp in components:
            if type(comp) == InstructionMemory:
                instructionMemory = comp
                break
        # if there is a instruction memory, add its length to the maxEvaluationCycles
        # to allow enough cycles for all instructions to be processed
        if instructionMemory is not None:
            maxEvaluationCycles = maxEvaluationCycles + len(instructionMemory.instructionList)
            
        # Determine starting components:
        # - if startingComponents provided via kw, use it
        # - otherwise start from inputs (copy)
        # - if inputs are empty, fall back to any ProgramCounter components
        startingComponents = kw.get("startingComponents", None)
        if startingComponents is None:
            startingComponents = inputs.copy()

        # If still empty, try to start from ProgramCounter components
        if startingComponents is None or len(startingComponents) == 0:
            startingComponents = [comp for comp in components if type(comp) == ProgramCounter]

        if startingComponents is None or len(startingComponents) == 0:
            return False  # nothing to start from
        tick = 0
        currentTick = startingComponents  # start with inputs or given components
        while len(currentTick) > 0:  # while there are still components to process
            nextTick = []  # list of components for next tick
            for g in currentTick:
                if g.eval():  # evaluate component
                    # if evaluation changed the output, add all connected components to next tick
                    gOut = [tuple[0] for tuple in g.getOutputs()]
                    for out in gOut:
                        nextTick.append(out)
            if updateFunction is not None:
                updateFunction(components=currentTick)
            if waitFunction is not None:
                waitFunction()
            currentTick = nextTick
            tick += 1
            # if too many ticks, there is probably a circular dependency which don't has a stable state
            if tick > MAX_EVAL_CYCLES * maxEvaluationCycles:
                return False
        return True
