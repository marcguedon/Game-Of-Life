from PyQt5.QtWidgets import (
    QGraphicsRectItem,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush


class Cell(QGraphicsRectItem):
    def __init__(self, x: int, y: int, size: int):
        super().__init__(0, 0, size, size)

        self.setPos(x * size, y * size)
        self.setBrush(QBrush(Qt.white))
        self.setPen(Qt.black)

        self.alive: bool = False

    def set_alive(self, alive: bool):
        self.alive = alive
        self.setBrush(QBrush(Qt.black if self.alive else Qt.white))

    def is_alive(self) -> bool:
        return self.alive
