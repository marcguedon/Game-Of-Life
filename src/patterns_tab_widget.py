import os
import json
from PyQt5.QtWidgets import QTabWidget, QPushButton
from controller import Controller
from patterns_type_tab import PatternsTypeTab
from pattern_button import PatternButton
from pattern import Pattern
from utils import from_pattern_to_image


class PatternsTabWidget(QTabWidget):
    def __init__(self):
        super().__init__()

        self.controller = Controller()
        self.controller.start_simulation_signal.connect(
            lambda enabled=False: self.toggle_buttons(enabled)
        )
        self.controller.pause_simulation_signal.connect(
            lambda enabled=True: self.toggle_buttons(enabled)
        )

        patterns_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "patterns"
        )

        patterns_types = [patterns_type for patterns_type in os.listdir(patterns_dir)]

        for patterns_type in patterns_types:
            patterns_type_tab = PatternsTypeTab()
            self.addTab(patterns_type_tab, patterns_type.capitalize())

            if patterns_type == "customs":
                add_pattern_button = QPushButton("Add")
                add_pattern_button.clicked.connect(self.controller.add_custom_pattern)
                add_pattern_button.setFixedSize(55, 55)
                patterns_type_tab.add_pattern_button(add_pattern_button)

            for pattern_name in os.listdir(os.path.join(patterns_dir, patterns_type)):
                pattern_file = os.path.join(patterns_dir, patterns_type, pattern_name)
                pattern = self.get_pattern_object_from_pattern_path(pattern_file)

                pattern_button = PatternButton(pattern)
                patterns_type_tab.add_pattern_button(pattern_button)

        self.setTabPosition(QTabWidget.West)

    def toggle_buttons(self, enabled: bool):
        for i in range(self.count()):
            item = self.widget(i)

            if item is not None:
                item.toggle_buttons(enabled)

    @staticmethod
    def get_pattern_object_from_pattern_path(pattern_path: str) -> Pattern:
        with open(pattern_path, encoding="UTF-8") as file:
            pattern_data = json.load(file)

        pattern_name = pattern_data["name"]
        pattern_cells = pattern_data["pattern"]["cells"]
        pattern_image = from_pattern_to_image(pattern_cells)

        pattern = Pattern(
            name=pattern_name,
            image=pattern_image,
            matrix=pattern_cells,
        )

        return pattern
