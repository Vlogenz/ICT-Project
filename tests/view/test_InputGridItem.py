import pytest
from PySide6 import QtWidgets, QtCore
from pytestqt import qtbot
from unittest.mock import Mock
from src.view.InputGridItem import InputGridItem
from src.model.Input import Input


class TestInputGridItem:

    def test_init_inherits_from_grid_item(self, qtbot):
        input_comp = Input()
        item = InputGridItem(input_comp)
        qtbot.addWidget(item)

        # Check it's a GridItem
        from src.view.GridItem import GridItem
        assert isinstance(item, GridItem)

        # Check toggle button is added
        assert hasattr(item, 'toggleButton')
        assert isinstance(item.toggleButton, QtWidgets.QPushButton)
        assert item.toggleButton.text() == "Toggle"

        # Check button is in layout
        layout = item.layout
        widgets = [layout.itemAt(i).widget() for i in range(layout.count())]
        assert item.toggleButton in widgets

    def test_toggle_button_connection(self, qtbot):
        input_comp = Input()
        item = InputGridItem(input_comp)
        qtbot.addWidget(item)

        # Mock toggleState and updatePortLabels
        item.logicComponent.toggleState = Mock()
        item.updatePortLabels = Mock()

        # Click the button
        qtbot.mouseClick(item.toggleButton, QtCore.Qt.LeftButton)

        # Check methods were called
        item.logicComponent.toggleState.assert_called_once()
        item.updatePortLabels.assert_called_once()

    def test_toggle_state_changes_component_state(self, qtbot):
        input_comp = Input()
        item = InputGridItem(input_comp)
        qtbot.addWidget(item)

        # Assume initial state is 0
        initial_state = input_comp.getState()['outValue'][0]
        assert initial_state == 0

        # Click toggle
        qtbot.mouseClick(item.toggleButton, QtCore.Qt.LeftButton)

        # Check state changed to 1
        new_state = input_comp.getState()['outValue'][0]
        assert new_state == 1

        # Click again
        qtbot.mouseClick(item.toggleButton, QtCore.Qt.LeftButton)

        # Back to 0
        final_state = input_comp.getState()['outValue'][0]
        assert final_state == 0

    def test_toggle_button_text(self, qtbot):
        input_comp = Input()
        item = InputGridItem(input_comp)
        qtbot.addWidget(item)

        assert item.toggleButton.text() == "Toggle"

    def test_immovable_parameter(self, qtbot):
        input_comp = Input()
        item = InputGridItem(input_comp, immovable=True)
        qtbot.addWidget(item)

        assert item.immovable == True
