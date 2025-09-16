from Model.LogicComponent import LogicComponent


class DummyInput(LogicComponent):
    def __init__(self, value):
        super().__init__()
        self.state = value
    def eval(self):
        return self.state