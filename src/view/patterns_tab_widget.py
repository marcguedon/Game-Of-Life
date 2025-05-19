import os
from PyQt5.QtWidgets import QTabWidget, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from controller.controller import Controller
from view.patterns_type_tab import PatternsTypeTab
from view.pattern_button import PatternButton
from model.pattern import Pattern
from utils import load_pattern_from_file


class PatternsTabWidget(QTabWidget):
    def __init__(self):
        super().__init__()

        self.controller: Controller = Controller()
        self.controller.start_simulation_signal.connect(
            lambda enabled=False: self.toggle_buttons(enabled)
        )
        self.controller.pause_simulation_signal.connect(
            lambda enabled=True: self.toggle_buttons(enabled)
        )
        self.controller.add_custom_pattern_signal.connect(self.add_custom_pattern)

        self.create_ui()

    def create_ui(self):
        patterns_dir: str = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "patterns"
        )

        patterns_types: list[str] = [
            patterns_type for patterns_type in os.listdir(patterns_dir)
        ]

        for patterns_type in sorted(patterns_types, key=str.lower):
            patterns_type_tab: PatternsTypeTab = PatternsTypeTab()
            patterns_type_tab.setObjectName(patterns_type)
            self.addTab(patterns_type_tab, patterns_type.capitalize())

            if patterns_type == "customs":
                add_pattern_button: QPushButton = QPushButton("Add")
                add_pattern_button.setToolTip("Add a custom pattern")
                add_pattern_button.setCursor(QCursor(Qt.PointingHandCursor))
                add_pattern_button.clicked.connect(
                    self.controller.open_add_custom_pattern_dialog
                )
                add_pattern_button.setFixedSize(55, 55)
                patterns_type_tab.add_pattern_button(add_pattern_button)

            for pattern_name in os.listdir(os.path.join(patterns_dir, patterns_type)):
                pattern_file: str = os.path.join(
                    patterns_dir, patterns_type, pattern_name
                )
                pattern: Pattern = load_pattern_from_file(pattern_file)

                pattern_button: PatternButton = PatternButton(pattern)
                patterns_type_tab.add_pattern_button(pattern_button)

        self.setTabPosition(QTabWidget.West)

    def toggle_buttons(self, enabled: bool):
        for i in range(self.count()):
            item: PatternsTypeTab = self.widget(i)

            if item is not None:
                item.toggle_buttons(enabled)

    def add_custom_pattern(self, pattern: Pattern):
        for i in range(self.count()):
            tab: PatternsTypeTab = self.widget(i)

            if tab.objectName().lower() == "customs":
                pattern_button = PatternButton(pattern)
                tab.add_pattern_button(pattern_button)
                break
