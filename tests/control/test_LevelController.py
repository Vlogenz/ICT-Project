import pytest
from src.control.LevelController import LevelController
from src.control.LogicComponentController import LogicComponentController
from src.model import DataMemory, InstructionMemory
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
def sample_level_data_with_memoryBlocks():
    """Returns sample level data for testing"""
    return {
        "level_id": 1,
        "name": "Test AND Gate Level",
        "description": "Test level for AND gate",
        "components": [
            {"type": "Input", "position": [4, 1], "immovable": True},
            {"type": "Input", "position": [4, 3], "immovable": True},
            {"type": "Output", "position": [8, 2], "immovable": True},
            {"type": "And", "position": [6,2], "immovable": True},
        {"type": "InstructionMemory", "position": [2,5], "immovable": False},
        {"type": "DataMemory", "position": [4,5], "immovable": False}
        
    ],
    "memoryContents": {
        "instructionMemory": [
            0,203,1,234,4624,4572,564,1234,425323,3465134,65344,23534,6345,234,1234,6543
        ],
        "dataMemory": [
            123,543,23,76,234,87,345,23,78,90,1234,5678,91011,1213,1415,1617
        ]
    },
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

@pytest.fixture
def level_controller_with_memoryBlocks(sample_level_data_with_memoryBlocks, logic_controller):
    """Creates a LevelController with sample data including memory blocks"""
    controller = LevelController(logic_controller)
    controller.setLevel(sample_level_data_with_memoryBlocks)
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

def test_adding_InstructionMemory(level_controller_with_memoryBlocks, logic_controller):
    """Test that InstructionMemory is added and loaded correctly"""
    level_controller_with_memoryBlocks.buildLevel()
    
    instruction_memory = None
    for comp in logic_controller.getComponents():
        if type(comp) == InstructionMemory:
            instruction_memory = comp
            break
    assert instruction_memory is not None

    im = instruction_memory
    expected_instructions = level_controller_with_memoryBlocks.levelData["memoryContents"]["instructionMemory"]
    assert im.instructionList == expected_instructions
    
def test_adding_DataMemory(level_controller_with_memoryBlocks, logic_controller):
    """Test that DataMemory is added and loaded correctly"""
    level_controller_with_memoryBlocks.buildLevel()
    
    data_memory = None
    for comp in logic_controller.getComponents():
        if type(comp) == DataMemory:
            data_memory = comp
            break
    assert data_memory is not None

    dm = data_memory
    expected_data = level_controller_with_memoryBlocks.levelData["memoryContents"]["dataMemory"]
    assert dm.dataList[:len(expected_data)] == expected_data
