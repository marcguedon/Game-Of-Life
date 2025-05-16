from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtCore import Qt
from pattern_button import PatternButton


class PatternsTypeTab(QWidget):
    def __init__(self):
        super().__init__()

        self.grid_layout = QGridLayout()
        self.grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.setLayout(self.grid_layout)

        self.nb_columns: int = 3
        self.current_row: int = 0
        self.current_column: int = 0

    def add_pattern_button(self, pattern_button: PatternButton):
        self.grid_layout.addWidget(
            pattern_button, self.current_row, self.current_column
        )
        self.current_column += 1

        if self.current_column >= self.nb_columns:
            self.current_column = 0
            self.current_row += 1

    def toggle_buttons(self, enabled: bool):
        for i in range(self.grid_layout.count()):
            item = self.grid_layout.itemAt(i)

            if item is not None:
                widget = item.widget()

                if isinstance(widget, PatternButton):
                    widget.setEnabled(enabled)
