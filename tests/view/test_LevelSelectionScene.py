import pytest
from PySide6 import QtWidgets, QtCore
from pytestqt import qtbot
from unittest.mock import Mock, patch
from src.control.LevelFileController import LevelFileController
from src.view.LevelSelectionScene import LevelSelectionScene


@pytest.fixture
def level_file_controller():
    controller = Mock(spec=LevelFileController)
    controller.getAvailableLevels.return_value = [0, 1, 2, 3]
    controller.getCompletedLevels.return_value = [0, 1]
    controller.getAllLevelsUnlocked.return_value = False
    return controller


class TestLevelSelectionScene:

    def test_initialization(self, qtbot, level_file_controller):
        scene = LevelSelectionScene(level_file_controller)
        qtbot.addWidget(scene)

        assert scene.windowTitle() == "Level selection"
        assert isinstance(scene.layout, QtWidgets.QVBoxLayout)

    def test_create_level_buttons(self, qtbot, level_file_controller):
        scene = LevelSelectionScene(level_file_controller)
        qtbot.addWidget(scene)

        # Check that buttons are created
        assert len(scene.levelButtons) == 4
        assert scene.levelButtons[0].text() == "Level 0 (Done)"
        assert scene.levelButtons[1].text() == "Level 1 (Done)"
        assert scene.levelButtons[2].text() == "Level 2"
        assert scene.levelButtons[3].text() == "Level 3 (Locked)"

    def test_on_level_clicked(self, qtbot, level_file_controller):
        with patch('src.view.LevelSelectionScene.getBus') as mock_get_bus:
            mock_bus = Mock()
            mock_get_bus.return_value = mock_bus

            scene = LevelSelectionScene(level_file_controller)
            qtbot.addWidget(scene)

            scene.onLevelClicked(1)
            mock_bus.emit.assert_called_once_with("levelSelection:levelSelected", 1)

    def test_toggle_level_lock_unlock(self, qtbot, level_file_controller):
        level_file_controller.getAllLevelsUnlocked.return_value = False
        scene = LevelSelectionScene(level_file_controller)
        qtbot.addWidget(scene)

        # Initially unlocked is False
        assert scene.toggleLevelLockButton.text() == "Unlock all levels"

        # Click to unlock
        qtbot.mouseClick(scene.toggleLevelLockButton, QtCore.Qt.LeftButton)
        level_file_controller.setAllLevelsUnlocked.assert_called_with(True)
        assert scene.toggleLevelLockButton.text() == "Lock levels"

    def test_toggle_level_lock_lock(self, qtbot, level_file_controller):
        level_file_controller.getAllLevelsUnlocked.return_value = True
        scene = LevelSelectionScene(level_file_controller)
        qtbot.addWidget(scene)

        # Initially unlocked is True
        assert scene.toggleLevelLockButton.text() == "Lock levels"

        # Click to lock
        qtbot.mouseClick(scene.toggleLevelLockButton, QtCore.Qt.LeftButton)
        level_file_controller.setAllLevelsUnlocked.assert_called_with(False)
        assert scene.toggleLevelLockButton.text() == "Unlock all levels"

    def test_update_level_buttons(self, qtbot, level_file_controller):
        scene = LevelSelectionScene(level_file_controller)
        qtbot.addWidget(scene)

        initial_count = len(scene.levelButtons)
        scene.updateLevelButtons()
        assert len(scene.levelButtons) == initial_count  # Should recreate the same number
