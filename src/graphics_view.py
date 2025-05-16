from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QMouseEvent
from controller import Controller
from grid_graphics_scene import GridGraphicsScene


class GraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.controller: Controller = Controller()

        self.scene: GridGraphicsScene = GridGraphicsScene(
            self.controller.NB_ROWS, self.controller.NB_COLS
        )
        self.setScene(self.scene)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

        self.scale_factor: float = 1.15
        self.current_scale: float = 1.0
        self.min_scale: float = 0.3
        self.max_scale: float = 5.0

        self._panning: bool = False
        self._pan_start = QPoint()

    def wheelEvent(self, event: QMouseEvent):
        if event.angleDelta().y() > 0 and self.current_scale < self.max_scale:
            self.scale(self.scale_factor, self.scale_factor)
            self.current_scale *= self.scale_factor

        elif event.angleDelta().y() < 0 and self.current_scale > self.min_scale:
            self.scale(1 / self.scale_factor, 1 / self.scale_factor)
            self.current_scale /= self.scale_factor

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MiddleButton:
            self._panning = True
            self.setCursor(Qt.ClosedHandCursor)
            self._pan_start = event.pos()

        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._panning:
            delta = self._pan_start - event.pos()
            self._pan_start = event.pos()
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() + delta.x()
            )
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() + delta.y()
            )

        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MiddleButton:
            self._panning = False
            self.setCursor(Qt.ArrowCursor)

        else:
            super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        pass
