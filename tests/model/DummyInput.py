from src.model.LogicComponent import LogicComponent


class DummyInput(LogicComponent):
    def __init__(self, value,bitwidth=1):
        super().__init__()
        if value > (1 << bitwidth)-1 or value < 0:
            raise ValueError(f"Value {value} does not fit in bitwidth {bitwidth}.")
        else:
            self.state = {"outValue": (value,bitwidth)}

    def eval(self):
        return True

    def setValue(self, value,bitwidth=1):
        if value > (1 << bitwidth)-1 or value < 0:
            raise ValueError(f"Value {value} does not fit in bitwidth {bitwidth}.")
        else:
            self.state["outValue"] = (value,bitwidth)
            

class DummyOutput(LogicComponent):
    def __init__(self,bitwidth=1):
        super().__init__()
        self.inputs = {"input": None}
        self.inputBitwidths = {"input": bitwidth}
        self.state = {"state": (0,bitwidth)}

    def eval(self):
        self.state["state"] = self.inputs["input"][0].getState()[self.inputs["input"][1]]
        return True