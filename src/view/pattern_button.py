from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt
from model.pattern import Pattern
from controller.controller import Controller


class PatternButton(QPushButton):
    def __init__(self, pattern: Pattern):
        super().__init__()

        self.controller = Controller()
        self.pattern: Pattern = pattern

        self.setCursor(Qt.PointingHandCursor)
        self.setIcon(self.pattern.get_icon())
        self.setIconSize(self.pattern.get_icon().pixmap(40, 40).size())
        self.setFixedSize(55, 55)
        self.setToolTip(pattern.name)

        self.clicked.connect(
            lambda state, pattern=self.pattern: self.controller.preview_pattern(pattern)
        )
