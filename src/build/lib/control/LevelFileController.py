import json
from pathlib import Path
from typing import List

class LevelFileController:
    def __init__(self):
        self.path="levels/"  # example path to level files
        self.currentLevel = None
        
        
    def loadLevel(self, levelNumber: int):
        """Loads level data from file or database"""
        levelFile = Path(self.path) / f"level_{levelNumber}.json"
        if levelFile.exists():
            with open(levelFile, 'r') as f:
                self.currentLevel = levelNumber
                return json.load(f)
        else:
            raise FileNotFoundError(f"Level file {levelFile} not found.")
        
    def loadMetaFile(self):
        """Loads the meta file, if existing. Otherwise, it will create a new one."""
        metaFile = Path(self.path) / "meta.json"
        if metaFile.exists():
            with open(metaFile, 'r') as f:
                return json.load(f)
        else:
            metaJson = {
                "completed_levels": [],
                "all_levels_unlocked": False,
            }
            with open(metaFile, 'w') as f:
                json.dump(metaJson, f, indent=4)
            return metaJson
        
    def getAvailableLevels(self):
        """Returns a list of numbers of available levels by scanning the levels directory"""
        levelFiles = Path(self.path).glob("level_*.json")
        levelNumbers = []
        for levelFile in levelFiles:
            filename = levelFile.name
            if filename.startswith("level_") and filename.endswith(".json"):
                levelNumber = int(levelFile.stem.split('_')[1].split('.')[0])
                levelNumbers.append(levelNumber)  
        return sorted(levelNumbers)

    def getCompletedLevels(self) -> List[int]:
        """Returns the list of completed levels from the meta json file."""
        metaJson = self.loadMetaFile()
        return metaJson["completed_levels"]
    
    def updateCompletedLevels(self, levelId: int):
        """Updates the list of completed levels in the meta json file"""
        metaFile = Path(self.path) / "meta.json"
        with open(metaFile, 'r') as f:
            metaJson = json.load(f)
        with open(metaFile, 'w') as f:
            levelNumbers = metaJson["completed_levels"]
            levelNumbers.append(levelId)
            metaJson["completed_levels"] = sorted(levelNumbers)
            json.dump(metaJson, f, indent=4)

    def getAllLevelsUnlocked(self) -> bool:
        """Returns the value of the all_components_unlocked entry in the meta json file."""
        metaJson = self.loadMetaFile()
        return metaJson["all_levels_unlocked"]

    def setAllLevelsUnlocked(self, value: bool):
        """Returns the value of the all_components_unlocked entry in the meta json file."""
        metaFile = Path(self.path) / "meta.json"
        with open(metaFile, 'r') as f:
            metaJson = json.load(f)
        metaJson['all_levels_unlocked'] = value
        with open(metaFile, 'w') as f:
            json.dump(metaJson, f, indent=4)
