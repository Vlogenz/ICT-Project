import pytest
import json
import tempfile
from pathlib import Path
from src.control.LevelFileController import LevelFileController


@pytest.fixture
def temp_levels_dir():
    """Creates a temporary directory for test level files"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_level_data():
    """Returns sample level data for testing"""
    return {
        "level_id": 0,
        "name": "Test Level",
        "description": "A test level",
        "difficulty": "Easy",
        "components": [
            {"type": "Input", "position": [4, 1], "immovable": True},
            {"type": "Output", "position": [8, 2], "immovable": True}
        ],
        "tests": [
            {
                "inputs": [[True, True]],
                "expected_output": [[True]]
            }
        ]
    }


@pytest.fixture
def level_controller(temp_levels_dir):
    """Creates a LevelFileController with temporary levels directory"""
    controller = LevelFileController()
    controller.path = str(temp_levels_dir) + "/"
    return controller


def test_init():
    """Test that LevelFileController initializes correctly"""
    controller = LevelFileController()
    assert controller.path == "levels/"
    assert controller.currentLevel is None


def test_loadLevel_success(level_controller, temp_levels_dir, sample_level_data):
    """Test loading a level successfully"""
    # Create test level file
    level_file = temp_levels_dir / "level_0.json"
    with open(level_file, 'w') as f:
        json.dump(sample_level_data, f)
    
    # Load level
    loaded_data = level_controller.loadLevel(0)
    
    # Verify
    assert loaded_data == sample_level_data
    assert level_controller.currentLevel == 0


def test_loadLevel_file_not_found(level_controller):
    """Test loading a non-existent level raises FileNotFoundError"""
    with pytest.raises(FileNotFoundError):
        level_controller.loadLevel(999)


def test_getAvailableLevels_empty_directory(level_controller):
    """Test getting available levels from empty directory"""
    levels = level_controller.getAvailableLevels()
    assert list(levels) == []


def test_getAvailableLevels_with_levels(level_controller, temp_levels_dir, sample_level_data):
    """Test getting available levels when levels exist"""
    # Create multiple test level files
    for i in [0, 1, 2]:
        level_file = temp_levels_dir / f"level_{i}.json"
        data = sample_level_data.copy()
        data["level_id"] = i
        with open(level_file, 'w') as f:
            json.dump(data, f)
    
    # Get available levels
    levels = list(level_controller.getAvailableLevels())
    
    # Verify (should find 3 levels)
    assert len(levels) == 3


def test_loadLevel_invalid_json(level_controller, temp_levels_dir):
    """Test loading a level with invalid JSON"""
    # Create file with invalid JSON
    level_file = temp_levels_dir / "level_5.json"
    with open(level_file, 'w') as f:
        f.write("{ invalid json }")
    
    # Should raise JSONDecodeError
    with pytest.raises(json.JSONDecodeError):
        level_controller.loadLevel(5)
