import pytest
from src.control.LevelController import LevelController
from src.control.LogicComponentController import LogicComponentController
from src.model.Input import Input
from src.model.Output import Output
from src.model.And import And


@pytest.fixture
def sample_level_data():
    """Returns sample level data for testing"""
    return {
        "level_id": 1,
        "name": "Test AND Gate Level",
        "description": "Test level for AND gate",
        "components": [
            {"type": "Input", "position": [4, 1]},
            {"type": "Input", "position": [4, 3]},
            {"type": "Output", "position": [8, 2]}
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
