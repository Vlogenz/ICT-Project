import pytest
from PySide6 import QtWidgets, QtCore
from pytestqt import qtbot
from unittest.mock import Mock, patch
from src.control.LogicComponentController import LogicComponentController
from src.view.SimulationControls import SimulationControls


@pytest.fixture
def logic_controller():
    return LogicComponentController()


class TestSimulationControls:

    def test_initialization(self, qtbot, logic_controller):
        controls = SimulationControls(logic_controller)
        qtbot.addWidget(controls)

        assert controls.startStopButton.text() == "Start"
        assert controls.resetButton.text() == "Reset"
        assert controls.speedSlider.minimum() == 1
        assert controls.speedSlider.maximum() == 10
        assert controls.speedSlider.value() == 10
        assert controls.speedLabel.text() == "Speed: Instant"

    def test_speed_slider_at_10(self, qtbot, logic_controller):
        controls = SimulationControls(logic_controller)
        qtbot.addWidget(controls)

        controls.speedSlider.setValue(10)
        assert controls.speedLabel.text() == "Speed: Instant"
        # Assuming setTickLength is called with 0

    def test_speed_slider_at_1(self, qtbot, logic_controller):
        controls = SimulationControls(logic_controller)
        qtbot.addWidget(controls)

        controls.speedSlider.setValue(1)
        assert controls.speedLabel.text() == "Speed: 1 step/sec"

    def test_speed_slider_at_5(self, qtbot, logic_controller):
        controls = SimulationControls(logic_controller)
        qtbot.addWidget(controls)

        controls.speedSlider.setValue(5)
        assert controls.speedLabel.text() == "Speed: 5 steps/sec"

    def test_configure_start_button(self, qtbot, logic_controller):
        controls = SimulationControls(logic_controller)
        qtbot.addWidget(controls)

        mock_function = Mock()
        controls.configureStart(mock_function)

        qtbot.mouseClick(controls.startStopButton, QtCore.Qt.LeftButton)
        mock_function.assert_called_once()

    def test_configure_reset_button(self, qtbot, logic_controller):
        controls = SimulationControls(logic_controller)
        qtbot.addWidget(controls)

        mock_function = Mock()
        controls.configureReset(mock_function)

        qtbot.mouseClick(controls.resetButton, QtCore.Qt.LeftButton)
        mock_function.assert_called_once()

    def test_default_start_button_connection(self, qtbot, logic_controller):
        with patch.object(logic_controller, 'eval', Mock()) as mock_eval:
            controls = SimulationControls(logic_controller)
            qtbot.addWidget(controls)

            # The start button is connected to controller.eval by default
            qtbot.mouseClick(controls.startStopButton, QtCore.Qt.LeftButton)
            mock_eval.assert_called_once()

    def test_layout_and_widgets(self, qtbot, logic_controller):
        controls = SimulationControls(logic_controller)
        qtbot.addWidget(controls)

        layout = controls.layout()
        assert isinstance(layout, QtWidgets.QHBoxLayout)

        # Check widgets in layout
        widgets = [layout.itemAt(i).widget() for i in range(layout.count())]
        assert controls.startStopButton in widgets
        assert controls.resetButton in widgets
        assert controls.speedLabel in widgets
        assert controls.speedSlider in widgets

    def test_frame_properties(self, qtbot, logic_controller):
        controls = SimulationControls(logic_controller)
        qtbot.addWidget(controls)

        assert controls.frameShape() == QtWidgets.QFrame.StyledPanel
        assert controls.maximumHeight() == 50  # fixed height
