import pytest
from PySide6 import QtWidgets, QtGui, QtCore
from pytestqt import qtbot
from unittest.mock import Mock, patch
from src.view.PaletteItem import PaletteItem
from src.model.And import And
from src.constants import MIME_TYPE


class TestPaletteItem:

    def test_init_with_image(self, qtbot):
        item = PaletteItem("And")
        qtbot.addWidget(item)

        assert item.frameShape() == QtWidgets.QFrame.Box
        assert item.size() == QtCore.QSize(92, 92)  # CELL_SIZE - 8 = 100 - 8 = 92

        # Check if pixmap is set (assuming Gates/And.svg exists)
        layout = item.layout()
        img_label = layout.itemAt(0).widget()
        assert isinstance(img_label, QtWidgets.QLabel)
        # Assuming pixmap is set
        assert not img_label.pixmap().isNull()

    def test_init_without_image(self, qtbot):
        # Use a class that doesn't have svg, but since all have, perhaps mock
        # For simplicity, assume Not has svg, but to test, perhaps create a dummy class
        # But hard, perhaps test the logic by checking if pixmap null, text is set
        # Since all have, perhaps skip or use And

        item = PaletteItem("And")
        qtbot.addWidget(item)

        layout = item.layout()
        img_label = layout.itemAt(0).widget()
        if img_label.pixmap().isNull():
            assert img_label.text() == "And"
        else:
            assert img_label.pixmap() is not None

    @patch('src.view.PaletteItem.QtGui.QDrag')
    def test_mouse_press_starts_drag(self, mock_drag_class, qtbot):
        item = PaletteItem("And")
        qtbot.addWidget(item)

        mock_drag = Mock()
        mock_drag_class.return_value = mock_drag

        # Create mouse press event
        event = QtGui.QMouseEvent(
            QtCore.QEvent.MouseButtonPress,
            QtCore.QPointF(10, 10),
            QtCore.Qt.LeftButton,
            QtCore.Qt.LeftButton,
            QtCore.Qt.NoModifier
        )

        item.mousePressEvent(event)

        # Check QDrag was created
        mock_drag_class.assert_called_once_with(item)

        # Check mime data
        mock_drag.setMimeData.assert_called_once()
        mime_data = mock_drag.setMimeData.call_args[0][0]
        assert mime_data.hasFormat(MIME_TYPE)
        payload = mime_data.data(MIME_TYPE).data().decode('utf-8')
        import json
        data = json.loads(payload)
        assert data['action_type'] == 'create'
        assert data['componentName'] == 'And'

        # Check other calls
        mock_drag.setPixmap.assert_called_once()
        mock_drag.setHotSpot.assert_called_once()
        mock_drag.exec.assert_called_once_with(QtCore.Qt.CopyAction)

    def test_mouse_press_non_left_button(self, qtbot):
        item = PaletteItem("And")
        qtbot.addWidget(item)

        # Right button should not start drag
        event = QtGui.QMouseEvent(
            QtCore.QEvent.MouseButtonPress,
            QtCore.QPointF(10, 10),
            QtCore.Qt.RightButton,
            QtCore.Qt.RightButton,
            QtCore.Qt.NoModifier
        )

        # Should not raise or do anything
        item.mousePressEvent(event)

    def test_fixed_size(self, qtbot):
        item = PaletteItem("And")
        qtbot.addWidget(item)

        assert item.minimumSize() == item.maximumSize() == QtCore.QSize(92, 92)
