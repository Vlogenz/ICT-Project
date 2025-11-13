import pytest
from src.control.LevelController import LevelController
from src.control.LogicComponentController import LogicComponentController
from src.model.And import And
from src.model.Or import Or


@pytest.fixture
def sample_level_data():
    """Returns sample level data for testing"""
    return {
        "level_id": 1,
        "name": "Test AND Gate Level",
        "description": "Test level for AND gate",
        "components": [
            {"type": "Input", "position": [4, 1], "immovable": True},
            {"type": "Input", "position": [4, 3], "immovable": True},
            {"type": "Output", "position": [8, 2], "immovable": True}
        ],
        "connections": [],
        "tests": [
            {
                "inputs": [[1, 1], [1, 1]],
                "expected_output": [[1, 1]]
            },
            {
                "inputs": [[1, 1], [0, 1]],
                "expected_output": [[0, 1]]
            },
            {
                "inputs": [[0, 1], [1, 1]],
                "expected_output": [[0, 1]]
            },
            {
                "inputs": [[0, 1], [0, 1]],
                "expected_output": [[0, 1]]
            }
        ]
    }

@pytest.fixture
def sample_level_data_with_connections():
    """Returns sample level data for testing"""
    return {
        "level_id": 1,
        "name": "Test AND Gate Level",
        "description": "Test level for AND gate",
        "components": [
            {"type": "Input", "position": [4, 1], "immovable": True},
            {"type": "Input", "position": [4, 3], "immovable": True},
            {"type": "Output", "position": [8, 2], "immovable": True},
            {"type": "And", "position": [6,2], "immovable": True}
        ],
        "connections": [
            {"origin": 0, "originKey": "outValue", "destination": 3, "destinationKey": "input1"},
            {"origin": 1, "originKey": "outValue", "destination": 3, "destinationKey": "input2"},
            {"origin": 3, "originKey": "outValue", "destination": 2, "destinationKey": "input"}
        ],
        "tests": [
            {
                "inputs": [[1, 1], [1, 1]],
                "expected_output": [[1, 1]]
            },
            {
                "inputs": [[1, 1], [0, 1]],
                "expected_output": [[0, 1]]
            },
            {
                "inputs": [[0, 1], [1, 1]],
                "expected_output": [[0, 1]]
            },
            {
                "inputs": [[0, 1], [0, 1]],
                "expected_output": [[0, 1]]
            }
        ]
    }


@pytest.fixture
def logic_controller():
    """Creates a LogicComponentController for testing"""
    controller = LogicComponentController()
    controller.setTickLength(0)
    return controller

@pytest.fixture
def level_controller(sample_level_data, logic_controller):
    """Creates a LevelController with sample data"""
    controller = LevelController(logic_controller)
    controller.setLevel(sample_level_data)
    return controller

@pytest.fixture
def level_controller_with_connections(sample_level_data_with_connections, logic_controller):
    """Creates a LevelController with sample data including connections"""
    controller = LevelController(logic_controller)
    controller.setLevel(sample_level_data_with_connections)
    return controller


def test_init(sample_level_data, logic_controller):
    """Test that LevelController initializes correctly"""
    controller = LevelController(logic_controller)
    
    assert controller.levelData is None  # levelData is not set in __init__
    assert controller.logicComponentController == logic_controller
    assert controller.currentLevel is None


def test_setLevel(logic_controller):
    """Test that setLevel correctly sets level data"""
    controller = LevelController(logic_controller)
    assert controller.levelData is None
    
    controller.setLevel(sample_level_data)
    assert controller.levelData == sample_level_data


def test_buildLevel(level_controller, logic_controller):
    """Test building a level from level data"""
    # Initially no components
    assert len(logic_controller.getComponents()) == 0

    # Build level
    level_controller.buildLevel()

    # Check that components were added
    assert len(logic_controller.getComponents()) == 3
    assert level_controller.currentLevel == 1

    # Verify component types
    inputs = logic_controller.getInputs()
    outputs = logic_controller.getOutputs()
    assert len(inputs) == 2
    assert len(outputs) == 1


def test_resetLevel(level_controller, logic_controller):
    """Test resetting a level to initial state"""
    # Build level first
    level_controller.buildLevel()
    assert len(logic_controller.getComponents()) == 3

    # Modify something (e.g., clear components manually)
    logic_controller.clearComponents()
    assert len(logic_controller.getComponents()) == 0

    # Reset should rebuild
    level_controller.resetLevel()
    assert len(logic_controller.getComponents()) == 3
    assert level_controller.currentLevel == 1


def test_quitLevel(level_controller, logic_controller):
    """Test quitting a level cleans up properly"""
    # Build level
    level_controller.buildLevel()
    assert len(logic_controller.getComponents()) == 3
    assert level_controller.currentLevel == 1
    
    # Quit level
    level_controller.quitLevel()
    
    # Verify cleanup
    assert len(logic_controller.getComponents()) == 0
    assert level_controller.currentLevel is None


def test_checkSolution_correct(level_controller, logic_controller):
    """Test checkSolution returns True for correct solution"""
    # Build level
    level_controller.buildLevel()
    
    # Manually set up correct AND gate configuration
    # Add AND gate and connect properly
    logic_controller.addLogicComponent(And)
    and_gate = logic_controller.getComponents()[3]  # After 2 inputs and 1 output
    
    inputs = logic_controller.getInputs()
    outputs = logic_controller.getOutputs()
    
    # Connect: Input0 -> And, Input1 -> And, And -> Output
    logic_controller.addConnection(inputs[0], "outValue", and_gate, "input1")
    logic_controller.addConnection(inputs[1], "outValue", and_gate, "input2")
    logic_controller.addConnection(and_gate, "outValue", outputs[0], "input")
    
    # Check solution
    result = level_controller.checkSolution()
    assert result == True


def test_checkSolution_incorrect(level_controller, logic_controller):
    """Test checkSolution returns False for incorrect solution"""
    # Build level
    level_controller.buildLevel()
    
    # Don't add AND gate or connect properly
    # Solution is incomplete/incorrect
    
    # Check solution should fail
    result = level_controller.checkSolution()
    assert result == False


def test_buildLevel_multiple_times(level_controller, logic_controller):
    """Test building level multiple times doesn't duplicate components"""
    # Build level
    level_controller.buildLevel()
    first_count = len(logic_controller.getComponents())
    
    # Build again (should clear first)
    level_controller.resetLevel()
    second_count = len(logic_controller.getComponents())
    
    # Should have same number of components
    assert first_count == second_count


def test_level_with_empty_components(logic_controller):
    """Test level with no components"""
    level_data = {
        "level_id": 99,
        "name": "Empty Level",
        "components": [],
        "tests": []
    }
    
    controller = LevelController(logic_controller)
    controller.setLevel(level_data)
    controller.buildLevel()
    
    assert len(logic_controller.getComponents()) == 0
    assert controller.currentLevel == 99
    
def test_getHints(level_controller):
    """Test getting hints from level data"""
    # Add hints to level data
    level_controller.levelData["hints"] = [
        "Remember to connect inputs to the AND gate.",
        "The output should only be high when both inputs are high."
    ]
    
    hints = level_controller.getHints()
    assert len(hints) == 2
    assert hints[0] == "Remember to connect inputs to the AND gate."
    assert hints[1] == "The output should only be high when both inputs are high."

def test_buildLevel_with_connections(level_controller_with_connections, logic_controller):
    """Test building a level that includes connections"""
    # Build level
    level_controller_with_connections.buildLevel()

    # Check that components were added
    assert len(logic_controller.getComponents()) == 4  # 2 Inputs, 1 And, 1 Output

    for comp in logic_controller.getInputs():
        assert len(comp.getOutputs()) == 1  # Inputs should have one output

    for comp in logic_controller.getOutputs():
        assert len(comp.getInputs()) == 1  # Outputs should have one input
    and_gates = [comp for comp in logic_controller.getComponents() if isinstance(comp, And)]
    assert len(and_gates) == 1  # There should be one And gate
    and_gate = and_gates[0]
    assert len(and_gate.getInputs()) == 2  # And gate should have two inputs
    assert len(and_gate.getOutputs()) == 1  # And gate should have one output

def test_getAvailableComponentClasses(logic_controller):
    """Test getting available component classes from level data"""
    level_data = {
        "available_components": [
            {"type": "And"},
            {"type": "Or"}
        ]
    }

    controller = LevelController(logic_controller)
    controller.setLevel(level_data)

    available = controller.getAvailableComponentClasses()

    assert len(available) == 2
    assert And in available
    assert Or in available

def test_getAvailableComponentClasses_none_levelData(logic_controller):
    """Test getAvailableComponentClasses with None levelData"""
    controller = LevelController(logic_controller)

    available = controller.getAvailableComponentClasses()

    assert available == []

def test_getAvailableComponentClasses_missing_key(logic_controller):
    """Test getAvailableComponentClasses with missing available_components key"""
    level_data = {}

    controller = LevelController(logic_controller)
    controller.setLevel(level_data)

    available = controller.getAvailableComponentClasses()

    assert available == []


# ============================================================================
# Tests for Output Predictions Feature
# ============================================================================

@pytest.fixture
def sample_level_data_with_output_predictions():
    """Returns sample level data with output predictions enabled"""
    return {
        "level_id": 2,
        "name": "Test Level with Output Predictions",
        "description": "Test level that uses output predictions",
        "usesOutputPredictions": True,
        "components": [
            {"type": "Input", "position": [4, 1], "immovable": True},
            {"type": "Input", "position": [4, 3], "immovable": True},
            {"type": "Output", "position": [8, 2], "immovable": True},
            {"type": "And", "position": [6, 2], "immovable": True}
        ],
        "connections": [
            {"origin": 0, "originKey": "outValue", "destination": 3, "destinationKey": "input1"},
            {"origin": 1, "originKey": "outValue", "destination": 3, "destinationKey": "input2"},
            {"origin": 3, "originKey": "outValue", "destination": 2, "destinationKey": "input"}
        ],
        "tests": [
            {
                "inputs": [[1, 1], [1, 1]],
                "expected_output": [[1, 1]]
            },
            {
                "inputs": [[1, 1], [0, 1]],
                "expected_output": [[0, 1]]
            },
            {
                "inputs": [[0, 1], [1, 1]],
                "expected_output": [[0, 1]]
            },
            {
                "inputs": [[0, 1], [0, 1]],
                "expected_output": [[0, 1]]
            }
        ]
    }


@pytest.fixture
def level_controller_with_output_predictions(sample_level_data_with_output_predictions, logic_controller):
    """Creates a LevelController with output predictions enabled"""
    controller = LevelController(logic_controller)
    controller.setLevel(sample_level_data_with_output_predictions)
    return controller


def test_usesOutputPredictions_true(level_controller_with_output_predictions):
    """Test usesOutputPredictions returns True when feature is enabled"""
    assert level_controller_with_output_predictions.usesOutputPredictions() == True


def test_usesOutputPredictions_false(level_controller):
    """Test usesOutputPredictions returns False when feature is not enabled"""
    assert level_controller.usesOutputPredictions() == False


def test_usesOutputPredictions_missing_key(logic_controller):
    """Test usesOutputPredictions returns False when key is missing from levelData"""
    level_data = {
        "level_id": 1,
        "components": []
    }
    controller = LevelController(logic_controller)
    controller.setLevel(level_data)

    assert controller.usesOutputPredictions() == False


def test_usesOutputPredictions_none_levelData(logic_controller):
    """Test usesOutputPredictions with None levelData"""
    controller = LevelController(logic_controller)
    # levelData is None by default

    # Should not crash and return False
    assert controller.usesOutputPredictions() == False


def test_buildLevel_sets_output_predictions(level_controller_with_output_predictions, logic_controller):
    """Test that buildLevel sets outputPredictions when usesOutputPredictions is True"""
    # Initially outputPredictions should be empty
    assert level_controller_with_output_predictions.outputPredictions == []

    # Build level
    level_controller_with_output_predictions.buildLevel()

    # After building, outputPredictions should be set based on current output values
    assert len(level_controller_with_output_predictions.outputPredictions) == 1
    # Initially outputs should be (0, 1) since inputs are off
    assert level_controller_with_output_predictions.outputPredictions[0] == (0, 1)


def test_buildLevel_does_not_set_output_predictions_when_disabled(level_controller, logic_controller):
    """Test that buildLevel does not set outputPredictions when feature is disabled"""
    # Build level without output predictions
    level_controller.buildLevel()

    # outputPredictions should remain empty
    assert level_controller.outputPredictions == []


def test_buildLevel_multiple_outputs_predictions(logic_controller):
    """Test buildLevel sets predictions for multiple outputs"""
    level_data = {
        "level_id": 3,
        "name": "Multi-output Level",
        "usesOutputPredictions": True,
        "components": [
            {"type": "Input", "position": [1, 1], "immovable": True},
            {"type": "Output", "position": [3, 1], "immovable": True},
            {"type": "Output", "position": [3, 2], "immovable": True},
            {"type": "Output", "position": [3, 3], "immovable": True}
        ],
        "connections": [
            {"origin": 0, "originKey": "outValue", "destination": 1, "destinationKey": "input"},
            {"origin": 0, "originKey": "outValue", "destination": 2, "destinationKey": "input"},
            {"origin": 0, "originKey": "outValue", "destination": 3, "destinationKey": "input"}
        ],
        "tests": []
    }

    controller = LevelController(logic_controller)
    controller.setLevel(level_data)
    controller.buildLevel()

    # Should have 3 output predictions
    assert len(controller.outputPredictions) == 3
    # All should be (0, 1) initially
    assert controller.outputPredictions[0] == (0, 1)
    assert controller.outputPredictions[1] == (0, 1)
    assert controller.outputPredictions[2] == (0, 1)


def test_checkSolution_with_correct_output_predictions(level_controller_with_output_predictions, logic_controller):
    """Test checkSolution passes when output predictions match current output"""
    # Build level
    level_controller_with_output_predictions.buildLevel()

    # Get the current output state and set it as prediction
    outputs = logic_controller.getOutputs()
    current_output_value = outputs[0].getState()["outValue"]
    level_controller_with_output_predictions.outputPredictions = [current_output_value]

    # Check solution should pass (predictions are correct)
    result = level_controller_with_output_predictions.checkSolution()
    assert result == True


def test_checkSolution_with_incorrect_output_predictions(level_controller_with_output_predictions, logic_controller):
    """Test checkSolution fails when output predictions don't match current output"""
    # Build level
    level_controller_with_output_predictions.buildLevel()

    # Set incorrect prediction (opposite of current state)
    outputs = logic_controller.getOutputs()
    current_output_value = outputs[0].getState()["outValue"]

    # If current is (0, 1), predict (1, 1), and vice versa
    if current_output_value[0] == 0:
        wrong_prediction = (1, 1)
    else:
        wrong_prediction = (0, 1)

    level_controller_with_output_predictions.outputPredictions = [wrong_prediction]

    # Check solution should fail due to wrong predictions
    result = level_controller_with_output_predictions.checkSolution()
    assert result == False


def test_checkSolution_with_predictions_and_tests(level_controller_with_output_predictions, logic_controller):
    """Test checkSolution validates both predictions and tests"""
    # Build level
    level_controller_with_output_predictions.buildLevel()

    # Set correct prediction for current state
    outputs = logic_controller.getOutputs()
    current_output_value = outputs[0].getState()["outValue"]
    level_controller_with_output_predictions.outputPredictions = [current_output_value]

    # checkSolution should validate predictions first, then run tests
    # Since the AND gate is correctly wired, tests should pass
    result = level_controller_with_output_predictions.checkSolution()
    assert result == True


def test_checkSolution_multiple_output_predictions_all_correct(logic_controller):
    """Test checkSolution with multiple outputs where all predictions are correct"""
    level_data = {
        "level_id": 4,
        "name": "Multi-output with predictions",
        "usesOutputPredictions": True,
        "components": [
            {"type": "Input", "position": [1, 1], "immovable": True},
            {"type": "Output", "position": [3, 1], "immovable": True},
            {"type": "Output", "position": [3, 2], "immovable": True}
        ],
        "connections": [
            {"origin": 0, "originKey": "outValue", "destination": 1, "destinationKey": "input"},
            {"origin": 0, "originKey": "outValue", "destination": 2, "destinationKey": "input"}
        ],
        "tests": [
            {
                "inputs": [[0, 1]],
                "expected_output": [[0, 1], [0, 1]]
            },
            {
                "inputs": [[1, 1]],
                "expected_output": [[1, 1], [1, 1]]
            }
        ]
    }

    controller = LevelController(logic_controller)
    controller.setLevel(level_data)
    controller.buildLevel()

    # Set correct predictions (both outputs mirror input which starts at 0)
    controller.outputPredictions = [(0, 1), (0, 1)]

    # Should pass
    result = controller.checkSolution()
    assert result == True


def test_checkSolution_multiple_output_predictions_one_wrong(logic_controller):
    """Test checkSolution with multiple outputs where one prediction is wrong"""
    level_data = {
        "level_id": 5,
        "name": "Multi-output with predictions",
        "usesOutputPredictions": True,
        "components": [
            {"type": "Input", "position": [1, 1], "immovable": True},
            {"type": "Output", "position": [3, 1], "immovable": True},
            {"type": "Output", "position": [3, 2], "immovable": True}
        ],
        "connections": [
            {"origin": 0, "originKey": "outValue", "destination": 1, "destinationKey": "input"},
            {"origin": 0, "originKey": "outValue", "destination": 2, "destinationKey": "input"}
        ],
        "tests": []
    }

    controller = LevelController(logic_controller)
    controller.setLevel(level_data)
    controller.buildLevel()

    # Set one correct and one wrong prediction
    controller.outputPredictions = [(0, 1), (1, 1)]  # Second is wrong

    # Should fail
    result = controller.checkSolution()
    assert result == False


def test_resetLevel_preserves_output_predictions_feature(level_controller_with_output_predictions, logic_controller):
    """Test that resetLevel maintains the output predictions feature setting"""
    # Build level
    level_controller_with_output_predictions.buildLevel()

    # Verify feature is enabled
    assert level_controller_with_output_predictions.usesOutputPredictions() == True

    # Reset level
    level_controller_with_output_predictions.resetLevel()

    # Feature should still be enabled after reset
    assert level_controller_with_output_predictions.usesOutputPredictions() == True

    # Output predictions should be reset based on new build
    assert len(level_controller_with_output_predictions.outputPredictions) == 1


def test_output_predictions_empty_list_for_level_without_outputs(logic_controller):
    """Test that buildLevel handles levels with no outputs gracefully"""
    level_data = {
        "level_id": 6,
        "name": "Level without outputs",
        "usesOutputPredictions": True,
        "components": [
            {"type": "Input", "position": [1, 1], "immovable": True}
        ],
        "connections": [],
        "tests": []
    }

    controller = LevelController(logic_controller)
    controller.setLevel(level_data)
    controller.buildLevel()

    # Should have empty predictions list
    assert controller.outputPredictions == []


def test_checkSolution_without_predictions_runs_tests_only(level_controller, logic_controller):
    """Test that checkSolution only runs tests when output predictions are disabled"""
    # Build level without output predictions
    level_controller.buildLevel()

    # Add AND gate and connect properly
    logic_controller.addLogicComponent(And)
    and_gate = logic_controller.getComponents()[3]

    inputs = logic_controller.getInputs()
    outputs = logic_controller.getOutputs()

    logic_controller.addConnection(inputs[0], "outValue", and_gate, "input1")
    logic_controller.addConnection(inputs[1], "outValue", and_gate, "input2")
    logic_controller.addConnection(and_gate, "outValue", outputs[0], "input")

    # checkSolution should only validate tests, not predictions
    result = level_controller.checkSolution()
    assert result == True

    # outputPredictions should still be empty
    assert level_controller.outputPredictions == []


def test_output_predictions_with_different_bitwidths(logic_controller):
    """Test output predictions work correctly with different bitwidths (1-bit, 8-bit, 32-bit)"""
    level_data = {
        "level_id": 7,
        "name": "Multi-bitwidth Level with Predictions",
        "usesOutputPredictions": True,
        "components": [
            # 1-bit inputs
            {"type": "Input", "position": [1, 1], "immovable": True},
            {"type": "Input", "position": [1, 2], "immovable": True},
            {"type": "Input", "position": [1, 3], "immovable": True},
            {"type": "Input", "position": [1, 4], "immovable": True},
            {"type": "Input", "position": [1, 5], "immovable": True},
            {"type": "Input", "position": [1, 6], "immovable": True},
            {"type": "Input", "position": [1, 7], "immovable": True},
            {"type": "Input", "position": [1, 8], "immovable": True},
            # Collector1to8 to combine 8 1-bit inputs into 8-bit output
            {"type": "Collector1to8", "position": [3, 4], "immovable": True},
            # Output for 1-bit
            {"type": "Output", "position": [5, 1], "immovable": True},
            # Output for 8-bit
            {"type": "Output", "position": [5, 4], "immovable": True},
        ],
        "connections": [
            # Connect inputs to collector
            {"origin": 0, "originKey": "outValue", "destination": 8, "destinationKey": "input1"},
            {"origin": 1, "originKey": "outValue", "destination": 8, "destinationKey": "input2"},
            {"origin": 2, "originKey": "outValue", "destination": 8, "destinationKey": "input3"},
            {"origin": 3, "originKey": "outValue", "destination": 8, "destinationKey": "input4"},
            {"origin": 4, "originKey": "outValue", "destination": 8, "destinationKey": "input5"},
            {"origin": 5, "originKey": "outValue", "destination": 8, "destinationKey": "input6"},
            {"origin": 6, "originKey": "outValue", "destination": 8, "destinationKey": "input7"},
            {"origin": 7, "originKey": "outValue", "destination": 8, "destinationKey": "input8"},
            # Connect first input directly to 1-bit output
            {"origin": 0, "originKey": "outValue", "destination": 9, "destinationKey": "input"},
            # Connect collector to 8-bit output
            {"origin": 8, "originKey": "outValue", "destination": 10, "destinationKey": "input"},
        ],
        "tests": [
            {
                "inputs": [[0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1]],
                "expected_output": [[0, 1], [0, 8]]
            },
            {
                "inputs": [[1, 1], [0, 1], [1, 1], [0, 1], [1, 1], [0, 1], [1, 1], [0, 1]],
                "expected_output": [[1, 1], [85, 8]]  # 0b01010101 = 85
            },
            {
                "inputs": [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1]],
                "expected_output": [[1, 1], [255, 8]]
            }
        ]
    }

    controller = LevelController(logic_controller)
    controller.setLevel(level_data)
    controller.buildLevel()

    # Should have 2 output predictions (one 1-bit, one 8-bit)
    assert len(controller.outputPredictions) == 2
    # Both should be (0, bitwidth) initially
    assert controller.outputPredictions[0] == (0, 1)  # 1-bit output
    assert controller.outputPredictions[1] == (0, 8)  # 8-bit output

    # Test with correct predictions
    result = controller.checkSolution()
    assert result == True

    # Test with wrong 1-bit prediction
    controller.outputPredictions = [(1, 1), (0, 8)]  # First is wrong
    result = controller.checkSolution()
    assert result == False

    # Test with wrong 8-bit prediction
    controller.outputPredictions = [(0, 1), (42, 8)]  # Second is wrong
    result = controller.checkSolution()
    assert result == False

    # Test with both wrong
    controller.outputPredictions = [(1, 1), (42, 8)]  # Both wrong
    result = controller.checkSolution()
    assert result == False


def test_output_predictions_with_32bit_output(logic_controller):
    """Test output predictions work correctly with 32-bit outputs using Collector8to32"""
    level_data = {
        "level_id": 8,
        "name": "32-bit Level with Predictions",
        "usesOutputPredictions": True,
        "components": [
            # Four 8-bit inputs (by cycling bitwidth on Input components)
            {"type": "Input", "position": [1, 1], "immovable": True},
            {"type": "Input", "position": [1, 2], "immovable": True},
            {"type": "Input", "position": [1, 3], "immovable": True},
            {"type": "Input", "position": [1, 4], "immovable": True},
            # Collector8to32 to combine four 8-bit inputs into 32-bit output
            {"type": "Collector8to32", "position": [3, 2], "immovable": True},
            # Output for 32-bit
            {"type": "Output", "position": [5, 2], "immovable": True},
        ],
        "connections": [
            {"origin": 0, "originKey": "outValue", "destination": 4, "destinationKey": "input1"},
            {"origin": 1, "originKey": "outValue", "destination": 4, "destinationKey": "input2"},
            {"origin": 2, "originKey": "outValue", "destination": 4, "destinationKey": "input3"},
            {"origin": 3, "originKey": "outValue", "destination": 4, "destinationKey": "input4"},
            {"origin": 4, "originKey": "outValue", "destination": 5, "destinationKey": "input"},
        ],
        "tests": []
    }

    controller = LevelController(logic_controller)
    controller.setLevel(level_data)
    controller.buildLevel()

    # The Collector8to32 outputs 32-bit even with 1-bit inputs (treating them as 8-bit with value 0)
    # So the output should already be 32-bit
    assert len(controller.outputPredictions) == 1

    # Get current output value
    outputs = logic_controller.getOutputs()
    current_value = outputs[0].getState()["outValue"]

    # The output should be 32-bit (from Collector8to32)
    assert current_value[1] == 32
    # Value should be 0 since all inputs are 0
    assert current_value[0] == 0

    # Set correct prediction
    controller.outputPredictions = [current_value]

    # Verify checkSolution works with correct 32-bit prediction
    result = controller.checkSolution()
    assert result == True

    # Test with wrong 32-bit value prediction
    controller.outputPredictions = [(12345, 32)]
    result = controller.checkSolution()
    assert result == False

    # Test with wrong bitwidth in prediction
    controller.outputPredictions = [(0, 8)]  # Wrong bitwidth
    result = controller.checkSolution()
    assert result == False
