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
        
    def loadMetaFile(self):
        metaFile = Path(self.path) / "meta.json"
        with open(metaFile, 'r') as f:
            return json.load(f)
        
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
    
    def updateCompletedLesson(self, levelId: int):
            metaFile = Path(self.path) / "meta.json"
            with open(metaFile, 'w'):
                metaJson = json.load(metaFile)
                metaJson.dumps({"level_unlocked": levelId})

    def forceCompleteLessons(self):
            metaFile = Path(self.path) / "meta.json"
            with open(metaFile, 'w'):
                metaJson = json.load(metaFile)
                metaJson.dumps({"level_unlocked": -1})