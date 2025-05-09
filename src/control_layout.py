from PyQt5.QtWidgets import (
    QComboBox,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QSlider,
    QLineEdit,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QIntValidator
from controller import Controller


class ControlLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()

        self.controller: Controller = Controller()

        self.create_ui()

    def create_ui(self):
        self.setContentsMargins(0, 75, 0, 100)

        sub_layout = QVBoxLayout()
        sub_layout.setSpacing(30)
        self.addLayout(sub_layout)

        rules_layout = QVBoxLayout()
        rules_layout.setSpacing(5)
        sub_layout.addLayout(rules_layout)

        rules_label = QLabel("Rules:")
        rules_layout.addWidget(rules_label)

        self.rules_combo_box = QComboBox()
        self.rules_combo_box.setToolTip("Select rules for the simulation")
        self.rules_combo_box.setCursor(QCursor(Qt.PointingHandCursor))
        self.rules_combo_box.addItem("Conway rules")
        self.rules_combo_box.addItem("HighLife rules")
        self.rules_combo_box.addItem("Seeds rules")
        self.rules_combo_box.addItem("Day and Night rules")
        rules_layout.addWidget(self.rules_combo_box)

        game_speed_layout = QVBoxLayout()
        game_speed_layout.setSpacing(5)
        sub_layout.addLayout(game_speed_layout)

        game_speed_label = QLabel("Game Speed:")
        game_speed_layout.addWidget(game_speed_label)

        self.game_speed_slider = QSlider(Qt.Horizontal)
        self.game_speed_slider.setToolTip("Set game speed")
        self.game_speed_slider.setRange(1, 10)
        self.game_speed_slider.setValue(1)
        self.game_speed_slider.setSingleStep(1)
        self.game_speed_slider.setPageStep(1)
        self.game_speed_slider.setTickPosition(QSlider.TicksBelow)
        self.game_speed_slider.setTickInterval(1)
        self.game_speed_slider.setCursor(QCursor(Qt.PointingHandCursor))
        game_speed_layout.addWidget(self.game_speed_slider)

        iterations_layout = QVBoxLayout()
        iterations_layout.setSpacing(5)
        sub_layout.addLayout(iterations_layout)

        iterations_label = QLabel("Iterations:")
        iterations_layout.addWidget(iterations_label)

        self.iterations_line_edit = QLineEdit()
        self.iterations_line_edit.setValidator(QIntValidator(0, 2**31 - 1))
        self.iterations_line_edit.setClearButtonEnabled(True)
        self.iterations_line_edit.setToolTip("Set number of iterations")
        self.iterations_line_edit.setPlaceholderText("Iterations")
        self.iterations_line_edit.setCursor(QCursor(Qt.PointingHandCursor))
        iterations_layout.addWidget(self.iterations_line_edit)

        truc = QHBoxLayout()
        truc.setSpacing(10)
        sub_layout.addLayout(truc)

        self.pause_btn = QPushButton("Pause")
        self.pause_btn.setToolTip("Pause simulation")
        self.pause_btn.clicked.connect(self.on_pause_btn_clicked)
        self.pause_btn.setEnabled(False)
        self.pause_btn.setCursor(QCursor(Qt.PointingHandCursor))
        truc.addWidget(self.pause_btn)

        self.start_btn = QPushButton("Start")
        self.start_btn.setToolTip("Start simulation")
        self.start_btn.clicked.connect(self.on_start_btn_clicked)
        self.start_btn.setCursor(QCursor(Qt.PointingHandCursor))
        truc.addWidget(self.start_btn)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setToolTip("Clear simulation")
        self.clear_btn.clicked.connect(self.controller.clear_simulation)
        self.clear_btn.setCursor(QCursor(Qt.PointingHandCursor))
        sub_layout.addWidget(self.clear_btn)

        self.addStretch()

        close_btn = QPushButton("Quit")
        close_btn.setToolTip("Quit application")
        close_btn.clicked.connect(self.controller.close_application)
        close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.addWidget(close_btn)

    def on_pause_btn_clicked(self):
        self.pause_btn.setEnabled(False)
        self.rules_combo_box.setEnabled(True)
        self.game_speed_slider.setEnabled(True)
        self.iterations_line_edit.setEnabled(True)
        self.start_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)

        self.controller.pause_simulation()

    def on_start_btn_clicked(self):
        self.rules_combo_box.setEnabled(False)
        self.game_speed_slider.setEnabled(False)
        self.iterations_line_edit.setEnabled(False)
        self.start_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)

        iterations: int = 0

        if self.iterations_line_edit.text():
            iterations = int(self.iterations_line_edit.text())

        self.controller.start_simulation(
            self.rules_combo_box.currentText(),
            self.game_speed_slider.value(),
            iterations,
        )
