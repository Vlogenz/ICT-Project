import pytest
import json
from pathlib import Path
from src.control.CustomComponentController import CustomComponentController, COMPONENT_DIRECTORY
from src.model.CustomLogicComponentData import CustomLogicComponentData
from src.model.And import And
from src.model.Or import Or
from src.model.Not import Not


@pytest.fixture
def temp_component_dir(tmp_path, monkeypatch):
    """Create a temporary directory for custom components"""
    temp_dir = tmp_path / "custom_components"
    temp_dir.mkdir()
    monkeypatch.setattr("src.control.CustomComponentController.COMPONENT_DIRECTORY", temp_dir)
    return temp_dir


@pytest.fixture
def sample_component_data():
    """Returns sample component data for testing"""
    # Create mock components with proper structure
    and_gate = And()
    or_gate = Or()
    not_gate = Not()
    
    # Set up connections between components
    and_gate.inputs = {"input1": None, "input2": None}
    or_gate.inputs = {"input1": (and_gate, "outValue"), "input2": None}
    not_gate.inputs = {"input": (or_gate, "outValue")}
    
    return {
        "name": "TestComponent",
        "inputMap": {"A": 0, "B": 1, "C": 2},
        "outputMap": {"Out": 0},
        "components": [and_gate, or_gate, not_gate],
        "spritePath": None
    }


@pytest.fixture
def sample_component_data_with_sprite(sample_component_data, tmp_path):
    """Returns sample component data with a sprite file"""
    # Create a dummy sprite file
    sprite_path = tmp_path / "test_sprite.svg"
    sprite_path.write_text("<svg></svg>")
    
    data = sample_component_data.copy()
    data["spritePath"] = str(sprite_path)
    return data


@pytest.fixture
def existing_custom_component(temp_component_dir):
    """Create an existing custom component in the temp directory"""
    component_name = "ExistingComponent"
    component_dir = temp_component_dir / component_name
    component_dir.mkdir()
    
    component_data = {
        "name": component_name,
        "inputMap": {"in1": 0, "in2": 1},
        "outputMap": {"out": 0},
        "components": ["And", "Or"],
        "connections": [
            {"from": {"component": 0, "output": "outValue"}, "to": {"component": 1, "input": "input1"}}
        ]
    }
    
    json_path = component_dir / f"{component_name}.json"
    with open(json_path, "w") as f:
        json.dump(component_data, f, indent=4)
    
    return component_data


class TestCreateCustomComponent:
    """Test suite for createCustomComponent method"""
    
    def test_create_component_success(self, temp_component_dir, sample_component_data):
        """Test successful creation of a custom component"""
        result = CustomComponentController.createCustomComponent(sample_component_data)
        
        assert result is True
        
        # Check that the directory was created
        component_dir = temp_component_dir / "TestComponent"
        assert component_dir.exists()
        
        # Check that the JSON file was created
        json_file = component_dir / "TestComponent.json"
        assert json_file.exists()
        
        # Check the contents of the JSON file
        with open(json_file, "r") as f:
            saved_data = json.load(f)
        
        assert saved_data["name"] == "TestComponent"
        assert saved_data["inputMap"] == {"A": 0, "B": 1, "C": 2}
        assert saved_data["outputMap"] == {"Out": 0}
        assert saved_data["components"] == ["And", "Or", "Not"]
        assert len(saved_data["connections"]) == 2  # or_gate and not_gate have connections
    
    def test_create_component_with_sprite(self, temp_component_dir, sample_component_data_with_sprite):
        """Test creating a custom component with a sprite file"""
        result = CustomComponentController.createCustomComponent(sample_component_data_with_sprite)
        
        assert result is True
        
        # Check that the sprite file was copied
        component_dir = temp_component_dir / "TestComponent"
        sprite_file = component_dir / "TestComponent.svg"
        assert sprite_file.exists()
        assert sprite_file.read_text() == "<svg></svg>"
    
    def test_create_component_missing_name(self, temp_component_dir):
        """Test that creating a component without a name returns False"""
        invalid_data = {
            "inputMap": {"A": 0},
            "outputMap": {"Out": 0},
            "components": []
        }
        
        result = CustomComponentController.createCustomComponent(invalid_data)
        assert result is False
    
    def test_create_component_sprite_not_exists(self, temp_component_dir, sample_component_data, capsys):
        """Test creating a component with non-existent sprite path"""
        data = sample_component_data.copy()
        data["spritePath"] = "/nonexistent/path/sprite.svg"
        
        result = CustomComponentController.createCustomComponent(data)
        
        # Should still succeed but print a warning
        assert result is True
        captured = capsys.readouterr()
        assert "Sprite file does not exist" in captured.out
    
    def test_create_component_invalid_data_structure(self, temp_component_dir):
        """Test creating a component with invalid data structure"""
        invalid_data = {
            "name": "Invalid",
            "inputMap": "not a dict",  # Invalid type
            "outputMap": {"Out": 0},
            "components": []
        }
        
        # This should fail during processing
        result = CustomComponentController.createCustomComponent(invalid_data)
        # The method catches all exceptions and returns False
        assert result is False
    
    def test_create_component_connections_structure(self, temp_component_dir):
        """Test that connections are properly structured in the saved JSON"""
        # Create components with specific connections
        and_gate = And()
        or_gate = Or()
        
        and_gate.inputs = {"input1": None, "input2": None}
        or_gate.inputs = {"input1": (and_gate, "outValue"), "input2": (and_gate, "outValue")}
        
        data = {
            "name": "ConnectionTest",
            "inputMap": {"A": 0},
            "outputMap": {"Out": 0},
            "components": [and_gate, or_gate]
        }
        
        result = CustomComponentController.createCustomComponent(data)
        assert result is True
        
        # Load and verify the connections
        json_file = temp_component_dir / "ConnectionTest" / "ConnectionTest.json"
        with open(json_file, "r") as f:
            saved_data = json.load(f)
        
        # Should have 2 connections (or_gate has 2 inputs from and_gate)
        assert len(saved_data["connections"]) == 2
        assert saved_data["connections"][0]["from"]["component"] == 0
        assert saved_data["connections"][0]["to"]["component"] == 1


class TestLoadCustomComponents:
    """Test suite for loadCustomComponents method"""
    
    def test_load_existing_component(self, temp_component_dir, existing_custom_component):
        """Test loading an existing custom component"""
        components = CustomComponentController.loadCustomComponents()
        
        assert len(components) == 1
        component = components[0]
        
        assert isinstance(component, CustomLogicComponentData)
        assert component.name == "ExistingComponent"
        assert component.inputMap == {"in1": 0, "in2": 1}
        assert component.outputMap == {"out": 0}
        assert component.components == ["And", "Or"]
        assert len(component.connections) == 1
    
    def test_load_multiple_components(self, temp_component_dir):
        """Test loading multiple custom components"""
        # Create multiple components
        for i in range(3):
            component_name = f"Component{i}"
            component_dir = temp_component_dir / component_name
            component_dir.mkdir()
            
            component_data = {
                "name": component_name,
                "inputMap": {"in": 0},
                "outputMap": {"out": 0},
                "components": ["And"],
                "connections": []
            }
            
            json_path = component_dir / f"{component_name}.json"
            with open(json_path, "w") as f:
                json.dump(component_data, f)
        
        components = CustomComponentController.loadCustomComponents()
        assert len(components) == 3
        
        names = [comp.name for comp in components]
        assert "Component0" in names
        assert "Component1" in names
        assert "Component2" in names
    
    def test_load_empty_directory(self, temp_component_dir):
        """Test loading when no custom components exist"""
        components = CustomComponentController.loadCustomComponents()
        assert len(components) == 0
    
    def test_load_with_invalid_json(self, temp_component_dir, capsys):
        """Test loading when a JSON file is invalid"""
        # Create a component with invalid JSON
        component_dir = temp_component_dir / "InvalidJSON"
        component_dir.mkdir()
        
        json_path = component_dir / "InvalidJSON.json"
        json_path.write_text("{ invalid json content")
        
        components = CustomComponentController.loadCustomComponents()
        
        # Should return empty list and print error
        assert len(components) == 0
        captured = capsys.readouterr()
        assert "Error decoding JSON files" in captured.out
    
    def test_load_with_missing_keys(self, temp_component_dir, capsys):
        """Test loading when JSON is missing required keys"""
        component_dir = temp_component_dir / "MissingKeys"
        component_dir.mkdir()
        
        # Create JSON with missing keys
        incomplete_data = {
            "name": "MissingKeys",
            "inputMap": {"in": 0}
            # Missing outputMap, components, connections
        }
        
        json_path = component_dir / "MissingKeys.json"
        with open(json_path, "w") as f:
            json.dump(incomplete_data, f)
        
        components = CustomComponentController.loadCustomComponents()
        
        # Should return empty list and print error
        assert len(components) == 0
        captured = capsys.readouterr()
        assert "Key error reading custom component data" in captured.out
    
    def test_load_ignores_non_directories(self, temp_component_dir):
        """Test that loading ignores files in the component directory"""
        # Create a file (not a directory) in the component directory
        file_path = temp_component_dir / "not_a_directory.txt"
        file_path.write_text("This is not a component")
        
        # Also create a valid component
        component_dir = temp_component_dir / "ValidComponent"
        component_dir.mkdir()
        component_data = {
            "name": "ValidComponent",
            "inputMap": {"in": 0},
            "outputMap": {"out": 0},
            "components": ["And"],
            "connections": []
        }
        json_path = component_dir / "ValidComponent.json"
        with open(json_path, "w") as f:
            json.dump(component_data, f)
        
        components = CustomComponentController.loadCustomComponents()
        
        # Should only load the valid component, ignoring the file
        assert len(components) == 1
        assert components[0].name == "ValidComponent"
    
    def test_load_missing_json_file(self, temp_component_dir, capsys):
        """Test loading when component directory exists but JSON file doesn't"""
        # Create directory without JSON file
        component_dir = temp_component_dir / "NoJSON"
        component_dir.mkdir()
        
        components = CustomComponentController.loadCustomComponents()
        
        # Should return empty list and print error
        assert len(components) == 0
        captured = capsys.readouterr()
        assert "Uncaught error loading custom components" in captured.out


class TestComponentDirectory:
    """Test suite for component directory handling"""
    
    def test_component_directory_constant(self):
        """Test that COMPONENT_DIRECTORY is properly defined"""
        assert COMPONENT_DIRECTORY is not None
        assert isinstance(COMPONENT_DIRECTORY, Path)
        # Should be in user's home directory
        assert str(Path.home()) in str(COMPONENT_DIRECTORY)
        assert "CircuitQuest" in str(COMPONENT_DIRECTORY)
        assert "custom_components" in str(COMPONENT_DIRECTORY)


class TestEdgeCases:
    """Test suite for edge cases and corner scenarios"""
    
    def test_component_with_empty_connections(self, temp_component_dir):
        """Test creating a component with no connections"""
        and_gate = And()
        and_gate.inputs = {"input1": None, "input2": None}
        
        data = {
            "name": "NoConnections",
            "inputMap": {"A": 0},
            "outputMap": {"Out": 0},
            "components": [and_gate]
        }
        
        result = CustomComponentController.createCustomComponent(data)
        assert result is True
        
        json_file = temp_component_dir / "NoConnections" / "NoConnections.json"
        with open(json_file, "r") as f:
            saved_data = json.load(f)
        
        assert saved_data["connections"] == []
    
    def test_component_with_special_characters_in_name(self, temp_component_dir):
        """Test creating a component with special characters in name"""
        and_gate = And()
        and_gate.inputs = {"input1": None, "input2": None}
        
        data = {
            "name": "Test-Component_123",
            "inputMap": {"A": 0},
            "outputMap": {"Out": 0},
            "components": [and_gate]
        }
        
        result = CustomComponentController.createCustomComponent(data)
        assert result is True
        
        component_dir = temp_component_dir / "Test-Component_123"
        assert component_dir.exists()
    
    def test_recreate_existing_component(self, temp_component_dir, sample_component_data):
        """Test that recreating a component overwrites the existing one"""
        # Create component first time
        result1 = CustomComponentController.createCustomComponent(sample_component_data)
        assert result1 is True
        
        # Modify data and create again
        modified_data = sample_component_data.copy()
        modified_data["inputMap"] = {"X": 0, "Y": 1}
        
        result2 = CustomComponentController.createCustomComponent(modified_data)
        assert result2 is True
        
        # Load and verify it was overwritten
        json_file = temp_component_dir / "TestComponent" / "TestComponent.json"
        with open(json_file, "r") as f:
            saved_data = json.load(f)
        
        assert saved_data["inputMap"] == {"X": 0, "Y": 1}

