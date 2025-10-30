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
def sample_meta_data():
    """Returns a sample meta file for testing"""
    return {
        "completed_levels": [0,1,2],
        "all_levels_unlocked": False
    }


@pytest.fixture
def level_file_controller(temp_levels_dir):
    """Creates a LevelFileController with temporary levels directory"""
    controller = LevelFileController()
    controller.path = str(temp_levels_dir) + "/"
    return controller


def test_init():
    """Test that LevelFileController initializes correctly"""
    controller = LevelFileController()
    assert controller.path == "levels/"
    assert controller.currentLevel is None


def test_loadLevel_success(level_file_controller, temp_levels_dir, sample_level_data):
    """Test loading a level successfully"""
    # Create test level file
    level_file = temp_levels_dir / "level_0.json"
    with open(level_file, 'w') as f:
        json.dump(sample_level_data, f)
    
    # Load level
    loaded_data = level_file_controller.loadLevel(0)
    
    # Verify
    assert loaded_data == sample_level_data
    assert level_file_controller.currentLevel == 0


def test_loadLevel_file_not_found(level_file_controller):
    """Test loading a non-existent level raises FileNotFoundError"""
    with pytest.raises(FileNotFoundError):
        level_file_controller.loadLevel(999)


def test_getAvailableLevels_empty_directory(level_file_controller):
    """Test getting available levels from empty directory"""
    levels = level_file_controller.getAvailableLevels()
    assert list(levels) == []


def test_getAvailableLevels_with_levels(level_file_controller, temp_levels_dir, sample_level_data):
    """Test getting available levels when levels exist"""
    # Create multiple test level files
    for i in [0, 1, 2]:
        level_file = temp_levels_dir / f"level_{i}.json"
        data = sample_level_data.copy()
        data["level_id"] = i
        with open(level_file, 'w') as f:
            json.dump(data, f)
    
    # Get available levels
    levels = list(level_file_controller.getAvailableLevels())
    
    # Verify (should find 3 levels)
    assert len(levels) == 3


def test_loadLevel_invalid_json(level_file_controller, temp_levels_dir):
    """Test loading a level with invalid JSON"""
    # Create file with invalid JSON
    level_file = temp_levels_dir / "level_5.json"
    with open(level_file, 'w') as f:
        f.write("{ invalid json }")
    
    # Should raise JSONDecodeError
    with pytest.raises(json.JSONDecodeError):
        level_file_controller.loadLevel(5)

def test_loadMetaFile_success(level_file_controller, temp_levels_dir, sample_meta_data):
    """Test loading the meta file successfully"""
    # Create test level file
    level_file = temp_levels_dir / "meta.json"
    with open(level_file, 'w') as f:
        json.dump(sample_meta_data, f)

    # Load level
    loaded_data = level_file_controller.loadMetaFile()

    # Verify
    assert loaded_data == sample_meta_data


def test_getCompletedLevels(level_file_controller, temp_levels_dir, sample_meta_data):
    """Test getting completed levels"""
    # Create meta.json
    meta_file = temp_levels_dir / "meta.json"
    with open(meta_file, 'w') as f:
        json.dump(sample_meta_data, f)

    # Get completed levels
    completed = level_file_controller.getCompletedLevels()

    # Verify
    assert completed == [0, 1, 2]


def test_getAllLevelsUnlocked(level_file_controller, temp_levels_dir, sample_meta_data):
    """Test getting all levels unlocked status"""
    # Create meta.json
    meta_file = temp_levels_dir / "meta.json"
    with open(meta_file, 'w') as f:
        json.dump(sample_meta_data, f)

    # Get status
    unlocked = level_file_controller.getAllLevelsUnlocked()

    # Verify
    assert unlocked == False


def test_setAllLevelsUnlocked(level_file_controller, temp_levels_dir, sample_meta_data):
    """Test setting all levels unlocked status"""
    # Create meta.json
    meta_file = temp_levels_dir / "meta.json"
    with open(meta_file, 'w') as f:
        json.dump(sample_meta_data, f)

    # Set to True
    level_file_controller.setAllLevelsUnlocked(True)

    # Verify
    assert level_file_controller.getAllLevelsUnlocked() == True

    # Set back to False
    level_file_controller.setAllLevelsUnlocked(False)

    # Verify
    assert level_file_controller.getAllLevelsUnlocked() == False


def test_updateCompletedLevels(level_file_controller, temp_levels_dir, sample_meta_data):
    """Test updating completed levels"""
    # Create meta.json
    meta_file = temp_levels_dir / "meta.json"
    with open(meta_file, 'w') as f:
        json.dump(sample_meta_data, f)

    # Update with new level
    level_file_controller.updateCompletedLevels(3)

    # Verify
    completed = level_file_controller.getCompletedLevels()
    assert completed == [0, 1, 2, 3]


def test_loadMetaFile_creates_file_if_not_exists(level_file_controller, temp_levels_dir):
    """Test that loadMetaFile creates meta.json if it doesn't exist"""
    # Ensure meta.json doesn't exist
    meta_file = temp_levels_dir / "meta.json"
    assert not meta_file.exists()

    # Call loadMetaFile
    meta_data = level_file_controller.loadMetaFile()

    # Verify file was created
    assert meta_file.exists()

    # Verify content
    with open(meta_file, 'r') as f:
        loaded_data = json.load(f)
    expected = {
        "completed_levels": [],
        "all_levels_unlocked": False,
    }
    assert loaded_data == expected
    assert meta_data == expected

