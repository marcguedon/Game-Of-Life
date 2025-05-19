import sys
import os
from PyQt5.QtWidgets import QApplication
from view.main_window import MainWindow

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "/usr/lib/qt/plugins"


def main():
    app = QApplication([])

    window = MainWindow()

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
