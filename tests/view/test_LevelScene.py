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
    return controller


@pytest.fixture
def level_file_controller():
    return Mock(spec=LevelFileController)


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

        # Find the label in the layout
        level_info_label = None
        for i in range(scene.layout.count()):
            item = scene.layout.itemAt(i)
            if item.widget() and isinstance(item.widget(), QtWidgets.QLabel):
                level_info_label = item.widget()
                break

        assert level_info_label is not None
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
