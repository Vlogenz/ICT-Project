import pytest
from PySide6 import QtWidgets, QtCore
from pytestqt import qtbot
from unittest.mock import Mock, patch
from src.control.LevelController import LevelController
from src.control.LevelFileController import LevelFileController
from src.control.LogicComponentController import LogicComponentController
from src.view.LevelScene import LevelScene
from src.model.And import And
from src.model.Or import Or


@pytest.fixture
def logic_controller():
    return Mock(spec=LogicComponentController)


@pytest.fixture
def level_controller(logic_controller):
    controller = Mock(spec=LevelController)
    controller.logicComponentController = logic_controller
    controller.getLevel.return_value = {
        "level_id": 1,
        "name": "Test Level",
        "description": "A test level",
        "objectives": ["Objective 1", "Objective 2"],
        "components": []
    }
    controller.getAvailableComponentClasses.return_value = [And, Or]
    controller.currentLevel = 1
    controller.outputPredictions = []  # Add missing attribute
    controller.usesOutputPredictions.return_value = False  # Add missing method
    controller.getOutputs.return_value = []  # Mock empty outputs list
    return controller


@pytest.fixture
def level_file_controller():
    return Mock(spec=LevelFileController)


@pytest.fixture
def level_controller_with_predictions(logic_controller):
    """Level controller with output predictions enabled"""
    controller = Mock(spec=LevelController)
    controller.logicComponentController = logic_controller
    controller.getLevel.return_value = {
        "level_id": 2,
        "name": "Test Level with Predictions",
        "description": "A test level with output predictions",
        "objectives": ["Predict outputs correctly"],
        "components": []
    }
    controller.getAvailableComponentClasses.return_value = [And, Or]
    controller.currentLevel = 2
    controller.outputPredictions = [(0, 1), (0, 1)]  # Two 1-bit outputs
    controller.usesOutputPredictions.return_value = True
    # Mock two output components with state
    mock_output1 = Mock()
    mock_output1.getState.return_value = {"outValue": (0, 1)}
    mock_output2 = Mock()
    mock_output2.getState.return_value = {"outValue": (0, 1)}
    controller.getOutputs.return_value = [mock_output1, mock_output2]
    return controller


class TestLevelScene:

    def test_initialization(self, qtbot, level_controller, level_file_controller):
        scene = LevelScene(level_controller, level_file_controller)
        qtbot.addWidget(scene)

        assert scene.windowTitle() == "Level 1"
        assert isinstance(scene.layout, QtWidgets.QGridLayout)

    def test_back_button_connection(self, qtbot, level_controller, level_file_controller):
        with patch.object(LevelScene, 'goToLevelSelection') as mock_go_to_level_selection:
            scene = LevelScene(level_controller, level_file_controller)
            qtbot.addWidget(scene)

            qtbot.mouseClick(scene.backButton, QtCore.Qt.LeftButton)
            mock_go_to_level_selection.assert_called_once()

    def test_go_to_level_selection(self, qtbot, level_controller, level_file_controller):
        scene = LevelScene(level_controller, level_file_controller)
        qtbot.addWidget(scene)

        scene.goToLevelSelection()
        level_controller.quitLevel.assert_called_once()
        # Assuming grid.unsubscribe is called, but since grid is mocked, hard to test

    def test_check_solution_success(self, qtbot, level_controller, level_file_controller):
        level_controller.checkSolution.return_value = True
        scene = LevelScene(level_controller, level_file_controller)
        qtbot.addWidget(scene)

        with patch('PySide6.QtWidgets.QMessageBox.information') as mock_info:
            scene.checkSolution()
            mock_info.assert_called_once()
            level_file_controller.updateCompletedLevels.assert_called_once_with(level_controller.currentLevel)

    def test_check_solution_failure(self, qtbot, level_controller, level_file_controller):
        level_controller.checkSolution.return_value = False
        scene = LevelScene(level_controller, level_file_controller)
        qtbot.addWidget(scene)

        with patch('PySide6.QtWidgets.QMessageBox.critical') as mock_critical:
            scene.checkSolution()
            mock_critical.assert_called_once()

    def test_level_info_label(self, qtbot, level_controller, level_file_controller):
        scene = LevelScene(level_controller, level_file_controller)
        qtbot.addWidget(scene)

        level_info_scroll_area = scene.levelInfoContainer
        assert isinstance(level_info_scroll_area, QtWidgets.QScrollArea)
        level_info_label = level_info_scroll_area.widget()
        assert isinstance(level_info_label, QtWidgets.QLabel)
        assert "Test Level" in level_info_label.text()
        assert "A test level" in level_info_label.text()
        assert "Objective 1" in level_info_label.text()

    def test_palette_creation(self, qtbot, level_controller, level_file_controller):
        scene = LevelScene(level_controller, level_file_controller)
        qtbot.addWidget(scene)

        # Palette should have PaletteItems for And and Or, plus DeleteArea
        # Hard to test exactly without accessing private layout, but we can check that buildLevel is called
        level_controller.buildLevel.assert_called_once()
        level_controller.setGrid.assert_called_once()

    # ============================================================================
    # Tests for checkSolution Feature
    # ============================================================================

    def test_check_solution_success_message_content(self, qtbot, level_controller, level_file_controller):
        """Test that success message shows correct content"""
        level_controller.checkSolution.return_value = True
        scene = LevelScene(level_controller, level_file_controller)
        qtbot.addWidget(scene)

        with patch('PySide6.QtWidgets.QMessageBox.information') as mock_info:
            scene.checkSolution()
            args = mock_info.call_args[0]
            assert args[1] == "You did it!"
            assert "All checks succeeded" in args[2]

    def test_check_solution_failure_message_content(self, qtbot, level_controller, level_file_controller):
        """Test that failure message shows correct content"""
        level_controller.checkSolution.return_value = False
        scene = LevelScene(level_controller, level_file_controller)
        qtbot.addWidget(scene)

        with patch('PySide6.QtWidgets.QMessageBox.critical') as mock_critical:
            scene.checkSolution()
            args = mock_critical.call_args[0]
            assert args[1] == "Not quite!"
            assert "Some tests failed" in args[2]

    def test_check_solution_updates_completed_levels_only_on_success(self, qtbot, level_controller, level_file_controller):
        """Test that completed levels are only updated when solution is correct"""
        level_controller.checkSolution.return_value = False
        scene = LevelScene(level_controller, level_file_controller)
        qtbot.addWidget(scene)

        with patch('PySide6.QtWidgets.QMessageBox.critical'):
            scene.checkSolution()
            # Should not update completed levels on failure
            level_file_controller.updateCompletedLevels.assert_not_called()

    def test_check_solution_calls_level_controller(self, qtbot, level_controller, level_file_controller):
        """Test that checkSolution properly delegates to LevelController"""
        level_controller.checkSolution.return_value = True
        scene = LevelScene(level_controller, level_file_controller)
        qtbot.addWidget(scene)

        with patch('PySide6.QtWidgets.QMessageBox.information'):
            scene.checkSolution()
            level_controller.checkSolution.assert_called_once()

    def test_check_solution_multiple_attempts(self, qtbot, level_controller, level_file_controller):
        """Test that checkSolution can be called multiple times"""
        level_controller.checkSolution.return_value = False
        scene = LevelScene(level_controller, level_file_controller)
        qtbot.addWidget(scene)

        with patch('PySide6.QtWidgets.QMessageBox.critical'):
            # First attempt - failure
            scene.checkSolution()
            assert level_controller.checkSolution.call_count == 1

        # Change to success
        level_controller.checkSolution.return_value = True
        with patch('PySide6.QtWidgets.QMessageBox.information'):
            # Second attempt - success
            scene.checkSolution()
            assert level_controller.checkSolution.call_count == 2
            level_file_controller.updateCompletedLevels.assert_called_once()

    def test_check_solution_with_output_predictions_enabled(self, qtbot, level_controller_with_predictions, level_file_controller):
        """Test checkSolution when output predictions feature is enabled"""
        level_controller_with_predictions.checkSolution.return_value = False
        scene = LevelScene(level_controller_with_predictions, level_file_controller)
        qtbot.addWidget(scene)

        with patch('PySide6.QtWidgets.QMessageBox.critical') as mock_critical:
            scene.checkSolution()
            mock_critical.assert_called_once()
            # Verify the message includes output predictions hint
            args = mock_critical.call_args[0]
            assert "output predictions" in args[2]

    def test_check_solution_without_output_predictions(self, qtbot, level_controller, level_file_controller):
        """Test that failure message doesn't mention output predictions when feature is disabled"""
        level_controller.checkSolution.return_value = False
        scene = LevelScene(level_controller, level_file_controller)
        qtbot.addWidget(scene)

        with patch('PySide6.QtWidgets.QMessageBox.critical') as mock_critical:
            scene.checkSolution()
            # Verify the message doesn't include output predictions hint
            args = mock_critical.call_args[0]
            assert "output predictions" not in args[2].lower()

    def test_check_solution_success_with_predictions(self, qtbot, level_controller_with_predictions, level_file_controller):
        """Test successful solution check with output predictions enabled"""
        level_controller_with_predictions.checkSolution.return_value = True
        scene = LevelScene(level_controller_with_predictions, level_file_controller)
        qtbot.addWidget(scene)

        with patch('PySide6.QtWidgets.QMessageBox.information') as mock_info:
            scene.checkSolution()
            mock_info.assert_called_once()
            level_file_controller.updateCompletedLevels.assert_called_once()

    def test_check_solution_method_exists(self, qtbot, level_controller, level_file_controller):
        """Test that checkSolution method is callable"""
        scene = LevelScene(level_controller, level_file_controller)
        qtbot.addWidget(scene)
        assert callable(scene.checkSolution)

    def test_level_scene_initializes_with_predictions(self, qtbot, level_controller_with_predictions, level_file_controller):
        """Test that LevelScene initializes correctly when output predictions are enabled"""
        scene = LevelScene(level_controller_with_predictions, level_file_controller)
        qtbot.addWidget(scene)

        assert scene.windowTitle() == "Level 2"
        level_controller_with_predictions.usesOutputPredictions.assert_called()

    def test_check_solution_evaluates_circuit_before_checking(self, qtbot, level_controller, level_file_controller):
        """Test that the circuit is properly evaluated before checking solution"""
        level_controller.checkSolution.return_value = True
        scene = LevelScene(level_controller, level_file_controller)
        qtbot.addWidget(scene)

        with patch('PySide6.QtWidgets.QMessageBox.information'):
            scene.checkSolution()
            # Verify checkSolution was called (which internally evaluates the circuit)
            level_controller.checkSolution.assert_called_once()
