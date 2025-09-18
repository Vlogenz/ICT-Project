from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtGui import QGuiApplication
import sys

class AppController:
    def __init__(self):
        self.app = QGuiApplication(sys.argv)
        self.engine = QQmlApplicationEngine()

        # Expose the model to QML
        # self.engine.rootContext().setContextProperty("greetingsModel", self.model)

        # Load QML view
        self.engine.load("view/dragAndDrop/gridview.qml")
        if not self.engine.rootObjects():
            sys.exit(-1)

    def run(self):
        sys.exit(self.app.exec())
