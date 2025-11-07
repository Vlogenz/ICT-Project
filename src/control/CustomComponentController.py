import json
import shutil
from pathlib import Path
from typing import List

from src.constants import APP_NAME
from src.model.CustomLogicComponent import CustomLogicComponent

COMPONENT_DIRECTORY = Path.home() / APP_NAME / "custom_components"

class CustomComponentController:

    @staticmethod
    def createCustomComponent(data: dict) -> bool:
        """Accepts the data as a dict and returns whether the saving process was successful or not."""
        # Validate data
        try:
            name = data["name"]
        except KeyError as e:
            # Return False if data is invalid
            print(f"Error reading custom component data: {e}")
            return False
        # Save data as JSON

        try:
            # Create the directory if it does not exist
            filePath = Path(f"{COMPONENT_DIRECTORY}/{name}/{name}.json")
            filePath.parent.mkdir(exist_ok=True, parents=True)

            # Process components and connections
            components = [{"class": comp.__class__.__name__} for comp in data["components"]]
            connections = []
            for i, comp in enumerate(data["components"]):
                for input_key, connection in comp.inputs.items():
                    if connection is not None:
                        source_comp, output_key = connection
                        j = data["components"].index(source_comp)
                        connections.append({
                            "from": {"component": j, "output": output_key},
                            "to": {"component": i, "input": input_key}
                        })
            data["components"] = components
            data["connections"] = connections

            # Write to the file
            with open(filePath, "w") as f:
                json.dump(data, f, indent=4)

            # Copy the sprite image if provided
            if "spritePath" in data and data["spritePath"]:
                spritePath = Path(data["spritePath"])
                if spritePath.exists():
                    dest = filePath.parent / f"{name}{spritePath.suffix}"
                    shutil.copy(spritePath, dest)
                    # Optionally, update the data to point to the copied file
                    data["spritePath"] = str(dest)
                    # Re-save the JSON with updated path
                    with open(filePath, "w") as f:
                        json.dump(data, f, indent=4)
                else:
                    print(f"Sprite file does not exist: {spritePath}")
        except Exception as e:
            # Return False if JSON saving failed
            print(f"Error saving JSON file: {e}")
            return False
        # Return True otherwise
        return True

    def loadCustomComponents(self) -> List[CustomLogicComponent]:
        """Loads all custom components and returns them as a list of CustomLogicComponent"""
        pass