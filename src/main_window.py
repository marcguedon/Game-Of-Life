from PyQt5.QtWidgets import (
    QWidget,
    QMainWindow,
    QHBoxLayout,
)
from controller import Controller
from control_layout import ControlLayout
from graphics_view import GraphicsView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.controller: Controller = Controller()
        self.controller.close_application_signal.connect(self.close)

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

        self.control_layout = ControlLayout()
        main_layout.addLayout(self.control_layout)
