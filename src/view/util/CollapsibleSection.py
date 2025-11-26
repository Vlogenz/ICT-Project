from PySide6 import QtWidgets, QtCore

class CollapsibleSection(QtWidgets.QWidget):
    """A collapsible section widget with a title and content area"""

    def __init__(self, title: str, parent=None):
        super().__init__(parent)

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        # Create toggle button
        self.toggleButton = QtWidgets.QToolButton()
        self.toggleButton.setText(title)
        self.toggleButton.setCheckable(True)
        self.toggleButton.setChecked(True)
        self.toggleButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toggleButton.setArrowType(QtCore.Qt.DownArrow)
        self.toggleButton.clicked.connect(self.toggle)

        # Create content area
        self.contentArea = QtWidgets.QWidget()
        self.contentLayout = QtWidgets.QGridLayout(self.contentArea)

        self.mainLayout.addWidget(self.toggleButton)
        self.mainLayout.addWidget(self.contentArea)

    def toggle(self):
        """Toggle the visibility of the content area"""
        checked = self.toggleButton.isChecked()
        self.contentArea.setVisible(checked)
        if checked:
            self.toggleButton.setArrowType(QtCore.Qt.DownArrow)
        else:
            self.toggleButton.setArrowType(QtCore.Qt.RightArrow)

    def addWidget(self, widget, row, col):
        """Add a widget to the content layout"""
        self.contentLayout.addWidget(widget, row, col)
