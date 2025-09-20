from src.model.LogicComponent import LogicComponent


class DummyInput(LogicComponent):
    def __init__(self, value):
        super().__init__()
        self.state = {"outValue": (1,1) if value else (0,1)}

    def eval(self):
        return True

    def setValue(self, value):
        self.state["outValue"] = (1,1) if value else (0,1)