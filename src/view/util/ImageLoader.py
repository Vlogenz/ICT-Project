from PySide6.QtGui import QColor, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import Qt

class ImageLoader:
    @staticmethod
    def svg_to_pixmap(svg_filename: str, color: QColor) -> QPixmap:
        renderer = QSvgRenderer(svg_filename)
        pixmap = QPixmap(renderer.defaultSize())
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)  # this is the destination, and only its alpha is used!
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()
        return pixmap