import pytest
from PySide6 import QtWidgets
from pytestqt import qtbot
from unittest.mock import Mock
from src.control.LogicComponentController import LogicComponentController
from src.view.SandboxModeScene import SandboxModeScene
from src.view.SimulationControls import SimulationControls
from src.view.GridWidget import GridWidget
import src.model


@pytest.fixture
def logic_controller():
    return Mock(spec=LogicComponentController)


class TestSandboxModeScene:

    def test_initialization(self, qtbot, logic_controller):
        scene = SandboxModeScene(logic_controller)
        qtbot.addWidget(scene)

        assert scene.windowTitle() == "Sandbox Mode"
        assert isinstance(scene.layout(), QtWidgets.QGridLayout)

    def test_widgets_in_layout(self, qtbot, logic_controller):
        scene = SandboxModeScene(logic_controller)
        qtbot.addWidget(scene)

        layout = scene.layout()
        # Check that there are widgets in the layout
        assert layout.count() > 0

        # Find palette frame, sim controls, grid by position
        backButton = layout.itemAtPosition(0, 0).widget()
        palette_frame = layout.itemAtPosition(1, 0).widget()
        sim_controls = layout.itemAtPosition(0, 1).widget()
        grid = layout.itemAtPosition(1, 1).widget()

        assert isinstance(backButton, QtWidgets.QPushButton)
        assert isinstance(palette_frame, QtWidgets.QFrame)
        assert isinstance(sim_controls, SimulationControls)
        assert isinstance(grid, QtWidgets.QScrollArea)

    def test_iter_classes_in_package(self, qtbot, logic_controller):
        scene = SandboxModeScene(logic_controller)
        qtbot.addWidget(scene)

        # Test the method
        classes = list(scene.iter_classes_in_package(src.model))
        assert len(classes) > 0  # Should find some classes like And, Or, etc.
