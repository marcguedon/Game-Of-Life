from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
from view.add_pattern_graphics_scene import AddPatternGraphicsScene
from view.cell import Cell


class AddPatternGraphicsview(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene: AddPatternGraphicsScene = AddPatternGraphicsScene()
        self.setScene(self.scene)

        self.setMouseTracking(True)

    def mousePressEvent(self, event: QMouseEvent):
        item = self.itemAt(event.pos())

        if isinstance(item, Cell):
            self.setCursor(Qt.CrossCursor)

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        item = self.itemAt(event.pos())

        if isinstance(item, Cell):
            self.setCursor(Qt.CrossCursor)

        else:
            self.setCursor(Qt.ArrowCursor)

        super().mouseMoveEvent(event)
