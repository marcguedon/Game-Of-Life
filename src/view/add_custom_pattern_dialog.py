import numpy as np
from PyQt5.QtWidgets import (
    QDialog,
    QDoubleSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from controller.controller import Controller
from view.add_pattern_graphics_scene import AddPatternGraphicsScene
from view.add_pattern_graphics_view import AddPatternGraphicsview
from view.cell import Cell
from model.pattern import Pattern
from utils import from_pattern_matrix_to_image


class AddCustomPatternDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.controller: Controller = Controller()

        self.setWindowTitle("Add custom pattern")
        self.setMinimumSize(600, 600)

        self.create_ui()

    def create_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        sub_layout = QHBoxLayout()
        main_layout.addLayout(sub_layout)

        pattern_name_layout: QHBoxLayout = QHBoxLayout()
        pattern_name_layout.setAlignment(Qt.AlignLeft)
        sub_layout.addLayout(pattern_name_layout)

        name_label = QLabel("Pattern name:")
        pattern_name_layout.addWidget(name_label)

        self.pattern_name_line_edit = QLineEdit()
        self.pattern_name_line_edit.textChanged.connect(
            lambda _: self.update_add_button_state()
        )
        self.pattern_name_line_edit.setPlaceholderText("Name...")
        self.pattern_name_line_edit.setToolTip("Set pattern name")
        self.pattern_name_line_edit.setCursor(QCursor(Qt.IBeamCursor))
        pattern_name_layout.addWidget(self.pattern_name_line_edit)

        pattern_name_layout.addStretch()

        pattern_size_layout: QHBoxLayout = QHBoxLayout()
        pattern_size_layout.setAlignment(Qt.AlignLeft)
        main_layout.addLayout(pattern_size_layout)

        pattern_size_label = QLabel("Pattern size (width/height):")
        pattern_size_layout.addWidget(pattern_size_label)

        self.pattern_width_spin = QDoubleSpinBox(self)
        self.pattern_width_spin.setToolTip("Set pattern width")
        self.pattern_width_spin.setRange(1, 30)
        self.pattern_width_spin.setValue(10)
        self.pattern_width_spin.setSingleStep(1)
        self.pattern_width_spin.setSuffix(" cells")
        self.pattern_width_spin.setDecimals(0)
        pattern_size_layout.addWidget(self.pattern_width_spin)

        pattern_size_layout.addWidget(QLabel("/"))

        self.pattern_height_spin = QDoubleSpinBox(self)
        self.pattern_height_spin.setToolTip("Set pattern height")
        self.pattern_height_spin.setRange(1, 30)
        self.pattern_height_spin.setValue(10)
        self.pattern_height_spin.setSingleStep(1)
        self.pattern_height_spin.setSuffix(" cells")
        self.pattern_height_spin.setDecimals(0)
        pattern_size_layout.addWidget(self.pattern_height_spin)

        self.add_pattern_graphics_view: AddPatternGraphicsview = (
            AddPatternGraphicsview()
        )
        self.add_pattern_graphics_view.viewport().installEventFilter(self)
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

        clear_button = QPushButton("Clear grid")
        clear_button.setToolTip("Clear grid")
        clear_button.setCursor(QCursor(Qt.PointingHandCursor))
        clear_button.clicked.connect(self.clear_scene)
        buttons_layout.addWidget(clear_button)

        buttons_layout.addStretch()

        self.add_button = QPushButton("Add")
        self.add_button.setToolTip("Add pattern")
        self.add_button.setEnabled(False)
        self.add_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.add_button.clicked.connect(self.add_pattern)
        buttons_layout.addWidget(self.add_button)

        self.pattern_width_spin.valueChanged.connect(
            lambda value: self.change_pattern_size()
        )
        self.pattern_height_spin.valueChanged.connect(
            lambda value: self.change_pattern_size()
        )

    def change_pattern_size(self):
        self.add_pattern_graphics_view.scene = AddPatternGraphicsScene(
            nb_rows=int(self.pattern_height_spin.value()),
            nb_cols=int(self.pattern_width_spin.value()),
        )
        self.add_pattern_graphics_view.setScene(self.add_pattern_graphics_view.scene)
        self.update_add_button_state()

    def clear_scene(self):
        for item in self.add_pattern_graphics_view.scene.items():
            if isinstance(item, Cell):
                if item.is_alive():
                    item.set_alive(False)

        self.update_add_button_state()

    def add_pattern(self):
        matrix: list[list[bool]] = []

        for item in self.add_pattern_graphics_view.scene.items():
            if isinstance(item, Cell):
                row: int = item.row
                # col: int = item.col

                while len(matrix) <= row:
                    matrix.append([])

                matrix[row].append(item.is_alive())

        image: np.ndarray = from_pattern_matrix_to_image(matrix)

        pattern: Pattern = Pattern(
            name=self.pattern_name_line_edit.text(),
            image=image,
            matrix=matrix,
        )

        self.controller.add_custom_pattern(pattern)
        self.close()

    def cancel(self):
        self.close()

    def update_add_button_state(self):
        has_alive_cells = any(
            isinstance(item, Cell) and item.is_alive()
            for item in self.add_pattern_graphics_view.scene.items()
        )
        name_filled: bool = bool(self.pattern_name_line_edit.text().strip())
        self.add_button.setEnabled(has_alive_cells and name_filled)

    def eventFilter(self, source, event):
        if event.type() == event.MouseButtonRelease:
            self.update_add_button_state()

        return super().eventFilter(source, event)
