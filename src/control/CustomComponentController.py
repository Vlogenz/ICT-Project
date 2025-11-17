import json
import shutil
from json import JSONDecodeError
from pathlib import Path
from typing import List
from dataclasses import asdict

from src.constants import APP_NAME
from src.model.CustomLogicComponentData import CustomLogicComponentData

COMPONENT_DIRECTORY = Path.home() / APP_NAME / "custom_components"

class CustomComponentController:
    """A controller to handle the custom components and store them in JSON files.
    The files will be stored in the App's home directory (user home -> APP_NAME).
    For each custom component, there will be a folder with the JSON file and a sprite.
    """

    @staticmethod
    def createCustomComponent(data: dict) -> bool:
        """Accepts the data as a dict and returns whether the saving process was successful or not.
        Args:
            data (dict): The data of the custom component to create.

        Returns:
            bool: True if and only if the saving process was successful, i.e. the data vas valid and no other errors occurred.
        """
        # Validate data
        try:
            name = data["name"]
            inputMap = data["inputMap"]
            outputMap = data["outputMap"]
            if not (isinstance(name, str) and isinstance(inputMap, dict) and isinstance(outputMap, dict)):
                print("Invalid custom component data")
                return False
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
            components = [comp.__class__.__name__ for comp in data["components"]]
            connections = []
            for i, comp in enumerate(data["components"]):
                for input_key, connection in comp.inputs.items():
                    if connection is not None:
                        source_comp, output_key = connection
                        j = data["components"].index(source_comp)
                        connections.append({
                            "origin": j,
                            "originKey": output_key,
                            "destination": i,
                            "destinationKey": input_key
                        })

            newComponentData = CustomLogicComponentData(
                name = name,
                inputMap = inputMap,
                outputMap= outputMap,
                components=components,
                connections=connections
            )

            # Write to the file
            with open(filePath, "w") as f:
                json.dump(asdict(newComponentData), f, indent=4)

            # Copy the sprite image if provided
            if "spritePath" in data and data["spritePath"]:
                spritePath = Path(data["spritePath"])
                if spritePath.exists():
                    dest = filePath.parent / f"{name}{spritePath.suffix}"
                    shutil.copy(spritePath, dest)
                else:
                    print(f"Sprite file does not exist: {spritePath}")
        except Exception as e:
            # Return False if saving failed
            print(f"Error saving custom component data: {e}")
            return False
        #Return True otherwise
        return True

    @staticmethod
    def loadCustomComponents() -> List[CustomLogicComponentData]:
        """Loads all custom components and returns them as a list of CustomLogicComponent

        Returns:
            List[CustomLogicComponentData]: The list of all currently available custom logic components.
        """
        # Create empty list to for custom components
        customComponentList: List[CustomLogicComponentData] = []

        # If component directory exists...
        if COMPONENT_DIRECTORY.exists():
            # Iterate subfolders of components directory
            for entry in COMPONENT_DIRECTORY.iterdir():
                if entry.is_dir():
                    # Try loading the JSON file
                    try:
                        filePath = entry / f"{entry.name}.json"
                        with open(filePath, "r") as f:
                            componentJson = json.load(f)
                            newComponent = CustomLogicComponentData(
                                componentJson["name"],
                                componentJson["inputMap"],
                                componentJson["outputMap"],
                                componentJson["components"],
                                componentJson["connections"]
                            )
                            customComponentList.append(newComponent)

                    # Catch possible exceptions
                    except JSONDecodeError as e:
                        print(f"Error decoding JSON files: {e}")
                    except KeyError as e:
                        print(f"Key error reading custom component data: {e}")
                    except Exception as e:
                        print(f"Uncaught error loading custom components: {e}")
        return customComponentList
