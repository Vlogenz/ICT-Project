from PySide6 import QtCore, QtGui
from pytestqt import qtbot
from src.control.LogicComponentController import LogicComponentController
from src.view.GridWidget import GridWidget
from src.model.And import And
from src.model.Not import Not
from src.constants import MIME_TYPE, CELL_SIZE
import json

class TestGridWidget:

    def test_drag_item_from_palette_to_empty_cell(self, qtbot):
        controller = LogicComponentController()
        grid = GridWidget(controller)
        qtbot.addWidget(grid)
        grid.show()

        # Create mime data for dragging And gate
        mime_data = QtCore.QMimeData()
        payload = {
            "action_type": "create",
            "class_name": "And"
        }
        mime_data.setData(MIME_TYPE, json.dumps(payload).encode('utf-8'))

        # Simulate drag enter
        drag_enter_event = QtGui.QDragEnterEvent(
            QtCore.QPoint(0, 0), QtCore.Qt.CopyAction, mime_data, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier
        )
        grid.dragEnterEvent(drag_enter_event)
        assert drag_enter_event.isAccepted()

        # Simulate drop at cell (0,0)
        drop_pos = QtCore.QPointF(CELL_SIZE // 2, CELL_SIZE // 2)
        drop_event = QtGui.QDropEvent(
            drop_pos, QtCore.Qt.CopyAction, mime_data, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier
        )
        grid.dropEvent(drop_event)

        # Check that an item was added
        assert len(grid.items) == 1
        assert isinstance(grid.items[0].logicComponent, And)

    def test_drag_item_from_palette_to_occupied_cell(self, qtbot):
        controller = LogicComponentController()
        grid = GridWidget(controller)
        qtbot.addWidget(grid)

        # Add an item first
        and_gate = controller.addLogicComponent(And)
        grid.addComponent((0, 0), and_gate)

        # Try to drag another item to the same cell
        mime_data = QtCore.QMimeData()
        payload = {
            "action_type": "create",
            "class_name": "Not"
        }
        mime_data.setData(MIME_TYPE, json.dumps(payload).encode('utf-8'))

        drop_pos = QtCore.QPointF(CELL_SIZE // 2, CELL_SIZE // 2)
        drop_event = QtGui.QDropEvent(
            drop_pos, QtCore.Qt.CopyAction, mime_data, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier
        )
        grid.dropEvent(drop_event)
        assert not drop_event.isAccepted()

        # Check that no new item was added
        assert len(grid.items) == 1

    def test_move_grid_item_to_empty_cell(self, qtbot):
        controller = LogicComponentController()
        grid = GridWidget(controller)
        qtbot.addWidget(grid)

        # Add an item at (0,0)
        and_gate = controller.addLogicComponent(And)
        grid.addComponent((0, 0), and_gate)
        item = grid.items[0]

        # Create mime data for moving
        mime_data = QtCore.QMimeData()
        payload = {
            "action_type": "move",
            "id": item.uid
        }
        mime_data.setData(MIME_TYPE, json.dumps(payload).encode('utf-8'))

        # Simulate drag move to (1,1)
        drag_move_event = QtGui.QDragMoveEvent(
            QtCore.QPoint(CELL_SIZE + CELL_SIZE // 2, CELL_SIZE + CELL_SIZE // 2),
            QtCore.Qt.CopyAction, mime_data, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier
        )
        grid.dragMoveEvent(drag_move_event)

        # Simulate drop
        drop_event = QtGui.QDropEvent(
            QtCore.QPointF(CELL_SIZE + CELL_SIZE // 2, CELL_SIZE + CELL_SIZE // 2),
            QtCore.Qt.CopyAction, mime_data, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier
        )
        grid.dropEvent(drop_event)
        assert drop_event.isAccepted()

        # Check position
        cell = grid.cellAt(item.pos())
        assert cell == (1, 1)

    def test_move_grid_item_to_occupied_cell(self, qtbot):
        controller = LogicComponentController()
        grid = GridWidget(controller)
        qtbot.addWidget(grid)

        # Add two items
        and_gate1 = controller.addLogicComponent(And)
        grid.addComponent((0, 0), and_gate1)
        and_gate2 = controller.addLogicComponent(Not)
        grid.addComponent((1, 1), and_gate2)
        item1 = grid.items[0]

        # Try to move item1 to (1,1)
        mime_data = QtCore.QMimeData()
        payload = {
            "action_type": "move",
            "id": item1.uid
        }
        mime_data.setData(MIME_TYPE, json.dumps(payload).encode('utf-8'))

        drop_pos = QtCore.QPointF(CELL_SIZE + CELL_SIZE // 2, CELL_SIZE + CELL_SIZE // 2)
        drop_event = QtGui.QDropEvent(
            drop_pos, QtCore.Qt.CopyAction, mime_data, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier
        )
        grid.dropEvent(drop_event)
        assert not drop_event.isAccepted()

        # Check position unchanged
        cell = grid.cellAt(item1.pos())
        assert cell == (0, 0)

    def test_create_valid_connection(self, qtbot):
        controller = LogicComponentController()
        grid = GridWidget(controller)
        qtbot.addWidget(grid)

        # Add two items
        not_gate = controller.addLogicComponent(Not)
        grid.addComponent((0, 0), not_gate)
        and_gate = controller.addLogicComponent(And)
        grid.addComponent((2, 0), and_gate)

        # Start connection from Not output
        output_rect = grid.items[0].getOutputRect("outValue")
        start_pos = grid.items[0].mapToParent(output_rect.center())
        mouse_press_event = QtGui.QMouseEvent(
            QtCore.QEvent.MouseButtonPress, start_pos, QtCore.Qt.LeftButton, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier
        )
        grid.items[0].mousePressEvent(mouse_press_event)

        # Move to And input
        input_rect = grid.items[1].getInputRect("input1")
        end_pos = grid.items[1].mapToParent(input_rect.center())
        mouse_move_event = QtGui.QMouseEvent(
            QtCore.QEvent.MouseMove, end_pos, QtCore.Qt.NoButton, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier
        )
        grid.mouseMoveEvent(mouse_move_event)

        # Release
        mouse_release_event = QtGui.QMouseEvent(
            QtCore.QEvent.MouseButtonRelease, end_pos, QtCore.Qt.LeftButton, QtCore.Qt.NoButton, QtCore.Qt.NoModifier
        )
        grid.mouseReleaseEvent(mouse_release_event)

        # Check connection created
        assert len(grid.connections) == 1

    def test_create_invalid_connection_same_item(self, qtbot):
        controller = LogicComponentController()
        grid = GridWidget(controller)
        qtbot.addWidget(grid)

        # Add one item
        and_gate = controller.addLogicComponent(And)
        grid.addComponent((0, 0), and_gate)

        # Try to connect output to input of same item
        output_rect = grid.items[0].getOutputRect("outValue")
        start_pos = grid.items[0].mapToParent(output_rect.center())
        mouse_press_event = QtGui.QMouseEvent(
            QtCore.QEvent.MouseButtonPress, start_pos, QtCore.Qt.LeftButton, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier
        )
        grid.items[0].mousePressEvent(mouse_press_event)

        input_rect = grid.items[0].getInputRect("input1")
        end_pos = grid.items[0].mapToParent(input_rect.center())
        mouse_release_event = QtGui.QMouseEvent(
            QtCore.QEvent.MouseButtonRelease, end_pos, QtCore.Qt.LeftButton, QtCore.Qt.NoButton, QtCore.Qt.NoModifier
        )
        grid.mouseReleaseEvent(mouse_release_event)

        # Check no connection created
        assert len(grid.connections) == 0

    def test_remove_connection(self, qtbot):
        controller = LogicComponentController()
        grid = GridWidget(controller)
        qtbot.addWidget(grid)

        # Add two items and connect them
        not_gate = controller.addLogicComponent(Not)
        grid.addComponent((0, 0), not_gate)
        and_gate = controller.addLogicComponent(And)
        grid.addComponent((2, 0), and_gate)

        # Manually add connection for simplicity
        controller.addConnection(not_gate, "outValue", and_gate, "input1")
        grid._visuallyAddConnection(not_gate, "outValue", and_gate, "input1")

        assert len(grid.connections) == 1

        # Remove connection
        grid.removeConnectionTo(grid.items[1], "input1")

        assert len(grid.connections) == 0

    def test_remove_item_removes_connections(self, qtbot):
        controller = LogicComponentController()
        grid = GridWidget(controller)
        qtbot.addWidget(grid)

        # Add two items and connect them
        not_gate = controller.addLogicComponent(Not)
        grid.addComponent((0, 0), not_gate)
        and_gate = controller.addLogicComponent(And)
        grid.addComponent((2, 0), and_gate)

        controller.addConnection(not_gate, "outValue", and_gate, "input1")
        grid._visuallyAddConnection(not_gate, "outValue", and_gate, "input1")

        assert len(grid.connections) == 1

        # Remove the source item
        grid.removeItem(grid.items[0])

        assert len(grid.items) == 1
        assert len(grid.connections) == 0

    def test_visually_clear_components(self, qtbot):
        controller = LogicComponentController()
        grid = GridWidget(controller)
        qtbot.addWidget(grid)

        # Add items and connections
        and_gate = controller.addLogicComponent(And)
        grid.addComponent((0, 0), and_gate)
        not_gate = controller.addLogicComponent(Not)
        grid.addComponent((1, 0), not_gate)
        controller.addConnection(and_gate, "outValue", not_gate, "input")
        grid._visuallyAddConnection(and_gate, "outValue", not_gate, "input")

        assert len(grid.items) == 2
        assert len(grid.connections) == 1

        # Clear components visually
        grid._visuallyRemoveAllItems()

        assert len(grid.items) == 0
        assert len(grid.connections) == 0

    def test_connection_line_activation(self, qtbot):
        controller = LogicComponentController()
        grid = GridWidget(controller)
        qtbot.addWidget(grid)

        # Add items and connection
        and_gate = controller.addLogicComponent(And)
        grid.addComponent((0, 0), and_gate)
        not_gate = controller.addLogicComponent(Not)
        grid.addComponent((1, 0), not_gate)
        controller.addConnection(and_gate, "outValue", not_gate, "input")
        grid._visuallyAddConnection(and_gate, "outValue", not_gate, "input")

        # Initially, connection is not active
        assert not grid.connections[0].isActive

        # Emit components updated event
        grid.eventBus.emit("view:components_updated", [and_gate, not_gate])

        # Check if activation is updated (depends on component states)
        # Since And has no inputs, out is 0, so connection is not active
        assert not grid.connections[0].isActive

    def test_deletion_via_delete_area(self, qtbot):
        from src.view.DeleteArea import DeleteArea
        controller = LogicComponentController()
        grid = GridWidget(controller)
        qtbot.addWidget(grid)

        # Add item
        and_gate = controller.addLogicComponent(And)
        grid.addComponent((0, 0), and_gate)
        item = grid.items[0]

        # Create delete area
        delete_area = DeleteArea(grid)
        qtbot.addWidget(delete_area)

        # Create mime data for moving the item
        mime_data = QtCore.QMimeData()
        payload = {
            "action_type": "move",
            "id": item.uid
        }
        mime_data.setData(MIME_TYPE, json.dumps(payload).encode('utf-8'))

        # Simulate drop on delete area
        drop_event = QtGui.QDropEvent(
            QtCore.QPointF(10, 10), QtCore.Qt.CopyAction, mime_data, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier
        )
        delete_area.dropEvent(drop_event)

        # Check item removed
        assert len(grid.items) == 0

    def test_visually_rebuild_circuit(self, qtbot):
        controller = LogicComponentController()
        grid = GridWidget(controller)
        qtbot.addWidget(grid)

        # Add components and connections to controller
        and_gate = controller.addLogicComponent(And)
        not_gate = controller.addLogicComponent(Not)
        controller.addConnection(and_gate, "outValue", not_gate, "input")

        # Component info: (x, y, immovable)
        component_info = [(0, 0, False), (1, 0, False)]

        # Call rebuild
        grid.rebuildCircuit(component_info)

        # Check items added
        assert len(grid.items) == 2
        assert grid.items[0].logicComponent == and_gate
        assert grid.items[1].logicComponent == not_gate

        # Check connections added
        assert len(grid.connections) == 1
        conn = grid.connections[0]
        assert conn.srcItem.logicComponent == and_gate
        assert conn.dstItem.logicComponent == not_gate
