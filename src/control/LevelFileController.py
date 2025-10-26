import json
from pathlib import Path

class LevelFileController:
    def __init__(self):
        self.path="levels/"  # Beispielpfad zu Level-Dateien
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
        
    def getAvailableLevels(self):
        """Returns a list of available levels by scanning the levels directory"""
        return Path(self.path).glob("level_*.json")  
