from PySide6 import QtWidgets

from src.control.LevelController import LevelController


class OutputPrediction(QtWidgets.QFrame):
    def __init__(self, levelController: LevelController):
        super().__init__()
        self.levelController = levelController

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(QtWidgets.QLabel("<h2>Output predictions:</h2>"), 0, 0)
        for i, output in enumerate(self.levelController.getOutputs()):
            value, bitwidth = output.getState()["outValue"]
            if output.getLabel() != "":
                labelText = output.getLabel()
            else:
                labelText = f"Output {i+1}"
            predictionLabel = QtWidgets.QLabel(f"{labelText} (Bitwidth: {bitwidth})")
            predictionInput = QtWidgets.QLineEdit(str(value))
            predictionInput.editingFinished.connect(lambda: self.enterPrediction(predictionInput, bitwidth, i))
            self.layout.addWidget(predictionLabel, i+1, 0)
            self.layout.addWidget(predictionInput, i+1, 1)

    def enterPrediction(self, fromInput: QtWidgets.QLineEdit, bitwidth, index):
        enteredInt = int(fromInput.text())
        maxValue = 2^bitwidth-1
        if maxValue < enteredInt:
            fromInput.setText(str(maxValue))
            newState = (maxValue, bitwidth)
        else:
            newState = (enteredInt, bitwidth)
        self.levelController.outputPredictions[index] = newState
