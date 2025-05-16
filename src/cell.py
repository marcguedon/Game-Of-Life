from PyQt5.QtWidgets import (
    QGraphicsRectItem,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPen


class Cell(QGraphicsRectItem):
    def __init__(self, x: int, y: int, size: int):
        super().__init__(0, 0, size - 1, size - 1)

        self.col: int = x
        self.row: int = y

        self.setPos(x * size, y * size)
        self.setBrush(QBrush(Qt.white))
        self.setPen(QPen(Qt.NoPen))

    def set_alive(self, alive: bool):
        self.setBrush(QBrush(Qt.black if alive else Qt.white))

    def is_alive(self) -> bool:
        return self.brush().color() == Qt.black

    def set_alive_preview(self, alive: bool):
        self.setBrush(QBrush(Qt.darkGray if alive else Qt.lightGray))
