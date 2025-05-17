from PyQt5.QtWidgets import (
    QWidget,
    QMainWindow,
    QHBoxLayout,
)
from controller import Controller
from control_layout import ControlLayout
from graphics_view import GraphicsView
from add_custom_pattern_dialog import AddCustomPatternDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.controller: Controller = Controller()
        self.controller.close_application_signal.connect(self.close)
        self.controller.open_add_custom_pattern_dialog_signal.connect(
            self.show_add_custom_pattern_dialog
        )

        self.setWindowTitle("Game of Life")
        self.resize(1920, 1080)

        self.create_ui()

    def create_ui(self):
        window_widget = QWidget()
        self.setCentralWidget(window_widget)

        main_layout = QHBoxLayout()
        window_widget.setLayout(main_layout)

        self.graphics_view = GraphicsView()
        main_layout.addWidget(self.graphics_view, stretch=1)

        control_widget = QWidget()
        control_widget.setMaximumWidth(267)
        main_layout.addWidget(control_widget)

        control_layout = ControlLayout()
        control_widget.setLayout(control_layout)

    def show_add_custom_pattern_dialog(self):
        add_custom_pattern_dialog = AddCustomPatternDialog()
        add_custom_pattern_dialog.exec_()
