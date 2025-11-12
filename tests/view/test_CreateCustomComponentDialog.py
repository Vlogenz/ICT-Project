import pytest
from unittest.mock import Mock, patch, MagicMock
from PySide6.QtWidgets import QLineEdit, QLabel, QPushButton, QDialogButtonBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from src.view.CreateCustomComponentDialog import CreateCustomComponentDialog
from src.control.LogicComponentController import LogicComponentController
from src.control.CustomComponentController import CustomComponentController
from src.model.Input import Input
from src.model.Output import Output
from src.model.And import And
from src.model.Or import Or


@pytest.fixture
def logic_controller():
    """Create a LogicComponentController with some test components"""
    controller = LogicComponentController()
    return controller


@pytest.fixture
def logic_controller_with_io(logic_controller):
    """Create a LogicComponentController with inputs and outputs"""
    # Add 2 inputs with different bitwidths
    input1 = logic_controller.addLogicComponent(Input)
    input1.state = {"outValue": (0, 1)}  # 1-bit input

    input2 = logic_controller.addLogicComponent(Input)
    input2.state = {"outValue": (0, 8)}  # 8-bit input

    # Add 2 outputs
    output1 = logic_controller.addLogicComponent(Output)
    output1.state = {"outValue": (0, 1)}

    output2 = logic_controller.addLogicComponent(Output)
    output2.state = {"outValue": (0, 1)}

    # Add some internal components
    logic_controller.addLogicComponent(And)
    logic_controller.addLogicComponent(Or)

    return logic_controller


class TestCreateCustomComponentDialogInitialization:
    """Test suite for dialog initialization"""

    def test_dialog_initialization_basic(self, qtbot, logic_controller):
        """Test basic dialog initialization"""
        dialog = CreateCustomComponentDialog(logic_controller)
        qtbot.addWidget(dialog)

        assert dialog.windowTitle() == "Create Custom Component"
        assert dialog.logicController == logic_controller
        assert isinstance(dialog.nameEdit, QLineEdit)
        assert dialog.spritePath is None
        assert dialog.inputNameLabels == []
        assert dialog.outputNameLabels == []

    def test_dialog_initialization_with_inputs_outputs(self, qtbot, logic_controller_with_io):
        """Test dialog initialization with inputs and outputs"""
        dialog = CreateCustomComponentDialog(logic_controller_with_io)
        qtbot.addWidget(dialog)

        # Should have 2 input name fields
        assert len(dialog.inputNameLabels) == 2
        assert all(isinstance(label, QLineEdit) for label in dialog.inputNameLabels)

        # Should have 2 output name fields
        assert len(dialog.outputNameLabels) == 2
        assert all(isinstance(label, QLineEdit) for label in dialog.outputNameLabels)

        # Check default input names
        assert dialog.inputNameLabels[0].text() == "input1"
        assert dialog.inputNameLabels[1].text() == "input2"

        # Check default output names
        assert dialog.outputNameLabels[0].text() == "output1"
        assert dialog.outputNameLabels[1].text() == "output2"

    def test_help_label_hidden_initially(self, qtbot, logic_controller):
        """Test that help label is hidden initially"""
        dialog = CreateCustomComponentDialog(logic_controller)
        qtbot.addWidget(dialog)

        assert not dialog.helpLabel.isVisible()
        assert dialog.toggleHelpButton.text() == "Help"

    def test_sprite_label_initial_state(self, qtbot, logic_controller):
        """Test sprite label initial state"""
        dialog = CreateCustomComponentDialog(logic_controller)
        qtbot.addWidget(dialog)

        assert dialog.spriteLabel.text() == "No sprite selected"
        assert dialog.spritePath is None


class TestToggleHelp:
    """Test suite for help toggle functionality"""

    def test_toggle_help_show(self, qtbot, logic_controller):
        """Test showing the help section"""
        dialog = CreateCustomComponentDialog(logic_controller)
        qtbot.addWidget(dialog)
        dialog.show()  # Need to show widget for visibility tests

        # Initially hidden
        assert not dialog.helpLabel.isVisible()

        # Click to show
        dialog.toggleHelp()

        assert dialog.helpLabel.isVisible()
        assert dialog.toggleHelpButton.text() == "Hide help"

    def test_toggle_help_hide(self, qtbot, logic_controller):
        """Test hiding the help section"""
        dialog = CreateCustomComponentDialog(logic_controller)
        qtbot.addWidget(dialog)
        dialog.show()  # Need to show widget for visibility tests

        # Show first
        dialog.toggleHelp()
        assert dialog.helpLabel.isVisible()

        # Then hide
        dialog.toggleHelp()

        assert not dialog.helpLabel.isVisible()
        assert dialog.toggleHelpButton.text() == "Help"

    def test_toggle_help_button_click(self, qtbot, logic_controller):
        """Test help button click triggers toggle"""
        dialog = CreateCustomComponentDialog(logic_controller)
        qtbot.addWidget(dialog)
        dialog.show()  # Need to show widget for visibility tests

        # Click the button
        qtbot.mouseClick(dialog.toggleHelpButton, Qt.LeftButton)

        assert dialog.helpLabel.isVisible()

        # Click again
        qtbot.mouseClick(dialog.toggleHelpButton, Qt.LeftButton)

        assert not dialog.helpLabel.isVisible()

    def test_help_label_content(self, qtbot, logic_controller):
        """Test help label has proper content"""
        dialog = CreateCustomComponentDialog(logic_controller)
        qtbot.addWidget(dialog)

        help_text = dialog.helpLabel.text()
        assert "order" in help_text.lower()
        assert "input" in help_text.lower()
        assert "output" in help_text.lower()


class TestSelectSprite:
    """Test suite for sprite selection functionality"""

    def test_select_sprite_success(self, qtbot, logic_controller, tmp_path):
        """Test successful sprite selection"""
        dialog = CreateCustomComponentDialog(logic_controller)
        qtbot.addWidget(dialog)

        # Create a temporary SVG file
        sprite_file = tmp_path / "test_sprite.svg"
        sprite_file.write_text("<svg><rect width='100' height='100'/></svg>")

        # Mock QFileDialog to return our test file
        with patch('src.view.CreateCustomComponentDialog.QFileDialog.getOpenFileName') as mock_dialog:
            mock_dialog.return_value = (str(sprite_file), "Image Files (*.svg)")

            dialog.selectSprite()

            assert dialog.spritePath == str(sprite_file)
            assert dialog.spriteLabel.text() == ""  # Text is cleared when pixmap is set

    def test_select_sprite_cancel(self, qtbot, logic_controller):
        """Test canceling sprite selection"""
        dialog = CreateCustomComponentDialog(logic_controller)
        qtbot.addWidget(dialog)

        original_path = dialog.spritePath
        original_text = dialog.spriteLabel.text()

        # Mock QFileDialog to return empty (user canceled)
        with patch('src.view.CreateCustomComponentDialog.QFileDialog.getOpenFileName') as mock_dialog:
            mock_dialog.return_value = ("", "")

            dialog.selectSprite()

            # Nothing should change
            assert dialog.spritePath == original_path
            assert dialog.spriteLabel.text() == original_text


class TestSubmitForm:
    """Test suite for form submission"""

    def test_submit_form_basic(self, qtbot, logic_controller_with_io):
        """Test basic form submission"""
        dialog = CreateCustomComponentDialog(logic_controller_with_io)
        qtbot.addWidget(dialog)

        # Set component name
        dialog.nameEdit.setText("MyCustomComponent")

        # Modify input/output names
        dialog.inputNameLabels[0].setText("inputA")
        dialog.inputNameLabels[1].setText("inputB")
        dialog.outputNameLabels[0].setText("outputX")
        dialog.outputNameLabels[1].setText("outputY")

        with patch.object(CustomComponentController, 'createCustomComponent') as mock_create:
            dialog.submitForm()

            mock_create.assert_called_once()
            call_args = mock_create.call_args[0][0]

            assert call_args["name"] == "MyCustomComponent"
            assert "inputA" in call_args["inputMap"]
            assert "inputB" in call_args["inputMap"]
            assert "outputX" in call_args["outputMap"]
            assert "outputY" in call_args["outputMap"]

    def test_submit_form_with_sprite(self, qtbot, logic_controller_with_io, tmp_path):
        """Test form submission with sprite"""
        dialog = CreateCustomComponentDialog(logic_controller_with_io)
        qtbot.addWidget(dialog)

        sprite_file = tmp_path / "component_sprite.svg"
        sprite_file.write_text("<svg></svg>")
        dialog.spritePath = str(sprite_file)

        dialog.nameEdit.setText("ComponentWithSprite")

        with patch.object(CustomComponentController, 'createCustomComponent') as mock_create:
            dialog.submitForm()

            call_args = mock_create.call_args[0][0]
            assert call_args["spritePath"] == str(sprite_file)

    def test_submit_form_without_sprite(self, qtbot, logic_controller_with_io):
        """Test form submission without sprite"""
        dialog = CreateCustomComponentDialog(logic_controller_with_io)
        qtbot.addWidget(dialog)

        dialog.nameEdit.setText("ComponentNoSprite")

        with patch.object(CustomComponentController, 'createCustomComponent') as mock_create:
            dialog.submitForm()

            call_args = mock_create.call_args[0][0]
            assert call_args["spritePath"] is None

    def test_submit_form_input_map_bitwidths(self, qtbot, logic_controller_with_io):
        """Test that input map contains correct bitwidths"""
        dialog = CreateCustomComponentDialog(logic_controller_with_io)
        qtbot.addWidget(dialog)

        dialog.nameEdit.setText("TestBitwidths")

        with patch.object(CustomComponentController, 'createCustomComponent') as mock_create:
            dialog.submitForm()

            call_args = mock_create.call_args[0][0]
            input_map = call_args["inputMap"]

            # First input has bitwidth 1, second has bitwidth 8
            assert input_map["input1"] == 1
            assert input_map["input2"] == 8

    def test_submit_form_output_map_bitwidths(self, qtbot, logic_controller_with_io):
        """Test that output map contains correct bitwidths"""
        dialog = CreateCustomComponentDialog(logic_controller_with_io)
        qtbot.addWidget(dialog)

        dialog.nameEdit.setText("TestOutputBitwidths")

        with patch.object(CustomComponentController, 'createCustomComponent') as mock_create:
            dialog.submitForm()

            call_args = mock_create.call_args[0][0]
            output_map = call_args["outputMap"]

            # Both outputs have bitwidth 1
            assert output_map["output1"] == 1
            assert output_map["output2"] == 1

    def test_submit_form_includes_components(self, qtbot, logic_controller_with_io):
        """Test that submitted data includes all components from controller"""
        dialog = CreateCustomComponentDialog(logic_controller_with_io)
        qtbot.addWidget(dialog)

        dialog.nameEdit.setText("TestComponents")

        with patch.object(CustomComponentController, 'createCustomComponent') as mock_create:
            dialog.submitForm()

            call_args = mock_create.call_args[0][0]
            components = call_args["components"]

            # Should include all components from the logic controller
            assert components == logic_controller_with_io.getComponents()

    def test_submit_form_empty_name(self, qtbot, logic_controller_with_io):
        """Test form submission with empty component name"""
        dialog = CreateCustomComponentDialog(logic_controller_with_io)
        qtbot.addWidget(dialog)

        # Leave name empty
        dialog.nameEdit.setText("")

        with patch.object(CustomComponentController, 'createCustomComponent') as mock_create:
            dialog.submitForm()

            # Should still attempt to create, but with empty name
            call_args = mock_create.call_args[0][0]
            assert call_args["name"] == ""

    def test_submit_form_custom_input_names(self, qtbot, logic_controller_with_io):
        """Test form submission with custom input names"""
        dialog = CreateCustomComponentDialog(logic_controller_with_io)
        qtbot.addWidget(dialog)

        dialog.nameEdit.setText("CustomNames")
        dialog.inputNameLabels[0].setText("clk")
        dialog.inputNameLabels[1].setText("data")
        dialog.outputNameLabels[0].setText("q")
        dialog.outputNameLabels[1].setText("qbar")

        with patch.object(CustomComponentController, 'createCustomComponent') as mock_create:
            dialog.submitForm()

            call_args = mock_create.call_args[0][0]

            assert "clk" in call_args["inputMap"]
            assert "data" in call_args["inputMap"]
            assert "q" in call_args["outputMap"]
            assert "qbar" in call_args["outputMap"]


class TestDialogButtons:
    """Test suite for dialog button functionality"""

    def test_ok_button_triggers_submit(self, qtbot, logic_controller_with_io):
        """Test that OK button triggers form submission"""
        dialog = CreateCustomComponentDialog(logic_controller_with_io)
        qtbot.addWidget(dialog)

        dialog.nameEdit.setText("TestOKButton")

        with patch.object(CustomComponentController, 'createCustomComponent') as mock_create:
            with patch.object(dialog, 'accept') as mock_accept:
                # Find and click OK button
                button_box = dialog.findChild(QDialogButtonBox)
                ok_button = button_box.button(QDialogButtonBox.Ok)
                qtbot.mouseClick(ok_button, Qt.LeftButton)

                # Should call both submitForm and accept
                mock_create.assert_called_once()
                mock_accept.assert_called_once()

    def test_cancel_button(self, qtbot, logic_controller):
        """Test that Cancel button rejects dialog"""
        dialog = CreateCustomComponentDialog(logic_controller)
        qtbot.addWidget(dialog)

        with patch.object(dialog, 'reject') as mock_reject:
            with patch.object(CustomComponentController, 'createCustomComponent') as mock_create:
                # Find and click Cancel button
                button_box = dialog.findChild(QDialogButtonBox)
                cancel_button = button_box.button(QDialogButtonBox.Cancel)
                qtbot.mouseClick(cancel_button, Qt.LeftButton)

                # Should reject but not create component
                mock_reject.assert_called_once()
                mock_create.assert_not_called()


class TestEdgeCases:
    """Test suite for edge cases and corner scenarios"""

    def test_no_inputs_or_outputs(self, qtbot, logic_controller):
        """Test dialog with no inputs or outputs"""
        dialog = CreateCustomComponentDialog(logic_controller)
        qtbot.addWidget(dialog)

        assert len(dialog.inputNameLabels) == 0
        assert len(dialog.outputNameLabels) == 0

        # Should still be able to submit
        dialog.nameEdit.setText("EmptyComponent")

        with patch.object(CustomComponentController, 'createCustomComponent') as mock_create:
            dialog.submitForm()

            call_args = mock_create.call_args[0][0]
            assert call_args["inputMap"] == {}
            assert call_args["outputMap"] == {}

    def test_many_inputs_outputs(self, qtbot, logic_controller):
        """Test dialog with many inputs and outputs"""
        # Add 5 inputs and 5 outputs
        for _ in range(5):
            input_comp = logic_controller.addLogicComponent(Input)
            input_comp.state = {"outValue": (0, 1)}
            output_comp = logic_controller.addLogicComponent(Output)
            output_comp.state = {"outValue": (0, 1)}

        dialog = CreateCustomComponentDialog(logic_controller)
        qtbot.addWidget(dialog)

        assert len(dialog.inputNameLabels) == 5
        assert len(dialog.outputNameLabels) == 5

        # Check default naming
        for i in range(5):
            assert dialog.inputNameLabels[i].text() == f"input{i+1}"
            assert dialog.outputNameLabels[i].text() == f"output{i+1}"

    def test_special_characters_in_names(self, qtbot, logic_controller_with_io):
        """Test form with special characters in custom names"""
        dialog = CreateCustomComponentDialog(logic_controller_with_io)
        qtbot.addWidget(dialog)

        dialog.nameEdit.setText("Component-With_Special.Chars123")
        dialog.inputNameLabels[0].setText("input_A")
        dialog.outputNameLabels[0].setText("output-1")

        with patch.object(CustomComponentController, 'createCustomComponent') as mock_create:
            dialog.submitForm()

            call_args = mock_create.call_args[0][0]
            assert call_args["name"] == "Component-With_Special.Chars123"
            assert "input_A" in call_args["inputMap"]
            assert "output-1" in call_args["outputMap"]

    def test_duplicate_input_output_names(self, qtbot, logic_controller_with_io):
        """Test form with duplicate input/output names"""
        dialog = CreateCustomComponentDialog(logic_controller_with_io)
        qtbot.addWidget(dialog)

        # Set duplicate names
        dialog.inputNameLabels[0].setText("duplicate")
        dialog.inputNameLabels[1].setText("duplicate")

        with patch.object(CustomComponentController, 'createCustomComponent') as mock_create:
            dialog.submitForm()

            call_args = mock_create.call_args[0][0]
            # Second one will overwrite the first in the dict
            assert "duplicate" in call_args["inputMap"]
