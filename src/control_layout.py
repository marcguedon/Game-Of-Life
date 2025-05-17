from PyQt5.QtWidgets import (
    QComboBox,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QSlider,
    QLineEdit,
    QFrame,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QIntValidator
from controller import Controller
from patterns_tab_widget import PatternsTabWidget


class ControlLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()

        self.controller: Controller = Controller()
        self.controller.pause_simulation_signal.connect(self.pause_simulation)

        self.create_ui()

    # TODO: Improve the UI
    def create_ui(self):
        self.setContentsMargins(20, 75, 20, 100)

        sub_layout = QVBoxLayout()
        sub_layout.setSpacing(30)
        self.addLayout(sub_layout)

        rules_layout = QVBoxLayout()
        rules_layout.setSpacing(5)
        sub_layout.addLayout(rules_layout)

        rules_sub_layout = QHBoxLayout()
        rules_sub_layout.setContentsMargins(0, 0, 2, 0)
        rules_layout.addLayout(rules_sub_layout)

        rules_label = QLabel("Select rules")
        rules_sub_layout.addWidget(rules_label)

        rules_sub_layout.addStretch()

        game_rules_help_btn = QPushButton("?")
        game_rules_help_btn.setFixedSize(20, 20)
        game_rules_help_btn.setStyleSheet(
            """
                QPushButton {
                    background-color: transparent;
                    border: none;
                }
                QPushButton:hover {
                    text-decoration: underline;
                }
            """
        )
        game_rules_help_btn.setToolTip("Help")
        game_rules_help_btn.setCursor(QCursor(Qt.PointingHandCursor))
        game_rules_help_btn.clicked.connect(self.controller.show_games_rules_help)
        rules_sub_layout.addWidget(game_rules_help_btn)

        self.rules_combo_box = QComboBox()
        self.rules_combo_box.setToolTip("Select rules for the simulation")
        self.rules_combo_box.setCursor(QCursor(Qt.PointingHandCursor))
        self.rules_combo_box.addItem("Conway (B3/S23) rules")
        self.rules_combo_box.addItem("HighLife (B36/S23) rules")
        self.rules_combo_box.addItem("Day and Night (B3678/S34678) rules")
        self.rules_combo_box.addItem("Seeds (B2/S) rules")
        self.rules_combo_box.addItem("Life w/o death (B3/S012345678) rules")
        self.rules_combo_box.addItem("Diamoeba (B35678/S5678) rules")
        self.rules_combo_box.addItem("Replicator (B1357/S1357) rules")
        self.rules_combo_box.addItem("Anneal (B4678/S35678) rules")
        rules_layout.addWidget(self.rules_combo_box)

        game_speed_layout = QVBoxLayout()
        game_speed_layout.setSpacing(5)
        sub_layout.addLayout(game_speed_layout)

        game_speed_label = QLabel("Game Speed")
        game_speed_layout.addWidget(game_speed_label)

        self.game_speed_slider = QSlider(Qt.Horizontal)
        self.game_speed_slider.setToolTip("Set game speed")
        self.game_speed_slider.setRange(1, 10)
        self.game_speed_slider.setValue(1)
        self.game_speed_slider.setPageStep(1)
        self.game_speed_slider.setTickPosition(QSlider.TicksBelow)
        self.game_speed_slider.setCursor(QCursor(Qt.PointingHandCursor))
        game_speed_layout.addWidget(self.game_speed_slider)

        iterations_layout = QVBoxLayout()
        iterations_layout.setSpacing(5)
        sub_layout.addLayout(iterations_layout)

        iterations_label = QLabel("Iterations")
        iterations_layout.addWidget(iterations_label)

        self.iterations_line_edit = QLineEdit()
        self.iterations_line_edit.setValidator(QIntValidator(0, 2**31 - 1))
        self.iterations_line_edit.setClearButtonEnabled(True)
        self.iterations_line_edit.setToolTip("Set number of iterations")
        self.iterations_line_edit.setPlaceholderText("Iterations")
        self.iterations_line_edit.setCursor(QCursor(Qt.PointingHandCursor))
        iterations_layout.addWidget(self.iterations_line_edit)

        start_pause_layout = QHBoxLayout()
        start_pause_layout.setSpacing(10)
        sub_layout.addLayout(start_pause_layout)

        self.pause_btn = QPushButton("Pause")
        self.pause_btn.setToolTip("Pause simulation")
        self.pause_btn.clicked.connect(self.controller.pause_simulation)
        self.pause_btn.setEnabled(False)
        self.pause_btn.setCursor(QCursor(Qt.PointingHandCursor))
        start_pause_layout.addWidget(self.pause_btn)

        self.start_btn = QPushButton("Start")
        self.start_btn.setToolTip("Start simulation")
        self.start_btn.clicked.connect(self.start_simulation)
        self.start_btn.setCursor(QCursor(Qt.PointingHandCursor))
        start_pause_layout.addWidget(self.start_btn)

        self.clear_btn = QPushButton("Clear simulation")
        self.clear_btn.setToolTip("Clear simulation")
        self.clear_btn.clicked.connect(self.controller.clear_simulation)
        self.clear_btn.setCursor(QCursor(Qt.PointingHandCursor))
        sub_layout.addWidget(self.clear_btn)

        patterns_layout = QVBoxLayout()
        patterns_layout.setSpacing(5)
        sub_layout.addLayout(patterns_layout)

        patterns_sub_layout = QHBoxLayout()
        patterns_sub_layout.setContentsMargins(0, 0, 2, 0)
        patterns_layout.addLayout(patterns_sub_layout)

        patterns_label = QLabel("Patterns")
        patterns_sub_layout.addWidget(patterns_label)

        patterns_sub_layout.addStretch()

        patterns_help_btn = QPushButton("?")
        patterns_help_btn.setFixedSize(20, 20)
        patterns_help_btn.setStyleSheet(
            """
                QPushButton {
                    background-color: transparent;
                    border: none;
                }
                QPushButton:hover {
                    text-decoration: underline;
                    
                }
            """
        )
        patterns_help_btn.setToolTip("Help")
        patterns_help_btn.setCursor(QCursor(Qt.PointingHandCursor))
        patterns_help_btn.clicked.connect(self.controller.show_patterns_help)
        patterns_sub_layout.addWidget(patterns_help_btn)

        patterns_tab_widget = PatternsTabWidget()
        patterns_layout.addWidget(patterns_tab_widget)

        self.show_hide_grid_btn = QPushButton("Show/hide grid")
        self.show_hide_grid_btn.setToolTip("Show/hide grid")
        self.show_hide_grid_btn.clicked.connect(self.controller.show_hide_grid)
        self.show_hide_grid_btn.setCursor(QCursor(Qt.PointingHandCursor))
        sub_layout.addWidget(self.show_hide_grid_btn)

        self.stretch(1)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        self.addWidget(separator)

        close_btn = QPushButton("Quit")
        close_btn.setToolTip("Quit application")
        close_btn.clicked.connect(self.controller.close_application)
        close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.addWidget(close_btn)

    def pause_simulation(self):
        self.pause_btn.setEnabled(False)
        self.rules_combo_box.setEnabled(True)
        self.game_speed_slider.setEnabled(True)
        self.iterations_line_edit.setEnabled(True)
        self.start_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)

    def start_simulation(self):
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
