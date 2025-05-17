import numpy as np
from PyQt5.QtWidgets import (
    QDialog,
    QDoubleSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QGraphicsView,
    QPushButton,
    QLineEdit,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from controller import Controller
from add_pattern_graphics_scene import AddPatternGraphicsScene
from cell import Cell
from pattern import Pattern
from utils import from_pattern_to_image


class AddCustomPatternDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.controller = Controller()

        self.setWindowTitle("Add Custom Pattern")
        self.setMinimumSize(600, 600)

        self.create_ui()

    # TODO: Improve the UI
    def create_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        pattern_size_layout = QHBoxLayout()
        main_layout.addLayout(pattern_size_layout)

        self.pattern_width_spin = QDoubleSpinBox(self)
        self.pattern_width_spin.setRange(1, 32)
        self.pattern_width_spin.setValue(10)
        self.pattern_width_spin.setSingleStep(1)
        self.pattern_width_spin.setPrefix("Width: ")
        self.pattern_width_spin.setSuffix(" cells")
        self.pattern_width_spin.setDecimals(0)
        pattern_size_layout.addWidget(self.pattern_width_spin)

        self.pattern_height_spin = QDoubleSpinBox(self)
        self.pattern_height_spin.setRange(1, 32)
        self.pattern_height_spin.setValue(10)
        self.pattern_height_spin.setSingleStep(1)
        self.pattern_height_spin.setPrefix("Height: ")
        self.pattern_height_spin.setSuffix(" cells")
        self.pattern_height_spin.setDecimals(0)
        pattern_size_layout.addWidget(self.pattern_height_spin)

        self.pattern_name_line_edit = QLineEdit()
        self.pattern_name_line_edit.textChanged.connect(
            lambda text: add_button.setEnabled(bool(text.strip()))
        )
        self.pattern_name_line_edit.setPlaceholderText("Pattern name")
        self.pattern_name_line_edit.setToolTip("Pattern name")
        self.pattern_name_line_edit.setCursor(QCursor(Qt.PointingHandCursor))
        pattern_size_layout.addWidget(self.pattern_name_line_edit)

        pattern_size_layout.addStretch()

        clear_button = QPushButton("Clear")
        clear_button.setToolTip("Clear grid")
        clear_button.setCursor(QCursor(Qt.PointingHandCursor))
        clear_button.clicked.connect(self.clear_scene)
        pattern_size_layout.addWidget(clear_button)

        self.add_pattern_graphics_view: QGraphicsView = QGraphicsView()
        self.add_pattern_graphics_view.scene: AddPatternGraphicsScene = (
            AddPatternGraphicsScene()
        )
        self.add_pattern_graphics_view.setScene(self.add_pattern_graphics_view.scene)
        main_layout.addWidget(self.add_pattern_graphics_view)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(100, 10, 100, 10)
        main_layout.addLayout(buttons_layout)

        cancel_button = QPushButton("Cancel")
        cancel_button.setToolTip("Cancel adding pattern")
        cancel_button.setCursor(QCursor(Qt.PointingHandCursor))
        cancel_button.clicked.connect(self.cancel)
        buttons_layout.addWidget(cancel_button)

        buttons_layout.addStretch()

        add_button = QPushButton("Add")
        add_button.setToolTip("Add pattern")
        add_button.setEnabled(False)
        add_button.setCursor(QCursor(Qt.PointingHandCursor))
        add_button.clicked.connect(self.add_pattern)
        buttons_layout.addWidget(add_button)

        self.pattern_width_spin.valueChanged.connect(self.change_pattern_size)
        self.pattern_height_spin.valueChanged.connect(self.change_pattern_size)

    def change_pattern_size(self, value: int):
        self.add_pattern_graphics_view.scene = AddPatternGraphicsScene(
            nb_rows=int(self.pattern_height_spin.value()),
            nb_cols=int(self.pattern_width_spin.value()),
        )
        self.add_pattern_graphics_view.setScene(self.add_pattern_graphics_view.scene)

    def clear_scene(self):
        for item in self.add_pattern_graphics_view.scene.items():
            if isinstance(item, Cell):
                if item.is_alive():
                    item.set_alive(False)

    def add_pattern(self):
        matrix: list[list[bool]] = []

        for item in self.add_pattern_graphics_view.scene.items():
            if isinstance(item, Cell):
                row: int = item.row
                col: int = item.col

                while len(matrix) <= row:
                    matrix.append([])

                matrix[row].append(item.is_alive())

        image: np.ndarray = from_pattern_to_image(matrix)

        pattern: Pattern = Pattern(
            name=self.pattern_name_line_edit.text(),
            image=image,
            matrix=matrix,
        )

        self.controller.add_custom_pattern(pattern)
        self.close()

    def cancel(self):
        self.close()
