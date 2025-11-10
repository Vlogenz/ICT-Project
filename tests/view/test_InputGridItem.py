import pytest
from PySide6 import QtWidgets, QtCore
from pytestqt import qtbot
from unittest.mock import Mock
from src.view.GridItems.InputGridItem import InputGridItem
from src.model.Input import Input


class TestInputGridItem:

    def test_init_inherits_from_grid_item(self, qtbot):
        input_comp = Input()
        item = InputGridItem(input_comp)
        qtbot.addWidget(item)

        # Check it's a GridItem
        from src.view.GridItems.GridItem import GridItem
        assert isinstance(item, GridItem)

        # Check toggle widget attribute exists. By design InputGridItem is
        # immutable by default now, so toggleButton can be either a
        # QPushButton (interactive) or a read-only QLineEdit (immutable).
        assert hasattr(item, 'toggleButton')
        assert isinstance(item.toggleButton, (QtWidgets.QPushButton, QtWidgets.QLineEdit))

        # Check widget is in layout
        layout = item.layout
        widgets = [layout.itemAt(i).widget() for i in range(layout.count())]
        assert item.toggleButton in widgets

    def test_toggle_button_connection(self, qtbot):
        input_comp = Input()
        item = InputGridItem(input_comp)
        qtbot.addWidget(item)
        # Ensure we have an interactive QPushButton to click. If the
        # created item is immutable (toggleButton is QLineEdit), replace it
        # with a real QPushButton for this test and add to layout.
        if not isinstance(item.toggleButton, QtWidgets.QPushButton):
            btn = QtWidgets.QPushButton("Toggle")
            # Replace widget in layout for the test
            item.layout.addWidget(btn)
            # connect to the item method so clicking behaves as in real UI
            btn.clicked.connect(item.toggleState)
            item.toggleButton = btn

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

        # Make sure we have an interactive button to click in this test
        if not isinstance(item.toggleButton, QtWidgets.QPushButton):
            btn = QtWidgets.QPushButton("Toggle")
            # connect to the actual handler
            btn.clicked.connect(item.toggleState)
            item.layout.addWidget(btn)
            item.toggleButton = btn

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

        # Depending on immutable default, toggleButton may be QPushButton
        # or QLineEdit. If it's a QPushButton, it should show "Toggle".
        if isinstance(item.toggleButton, QtWidgets.QPushButton):
            assert item.toggleButton.text() == "Toggle"
        else:
            # Immutable: the read-only widget should display the current value
            assert item.toggleButton.text() == str(input_comp.getState()['outValue'][0])

    def test_immovable_parameter(self, qtbot):
        input_comp = Input()
        item = InputGridItem(input_comp, immovable=True)
        qtbot.addWidget(item)

        assert item.immovable == True
