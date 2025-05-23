import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import QMessageBox
from model.pattern import Pattern
from game_rules import GAME_RULES_REGISTRY
from utils import save_pattern_to_file


class Controller(QObject):
    _instance: bool = None

    NB_ROWS: int = 146
    NB_COLS: int = 225

    close_application_signal = pyqtSignal()

    update_scene_signal = pyqtSignal(list)
    start_simulation_signal = pyqtSignal()
    pause_simulation_signal = pyqtSignal()
    clear_simulation_signal = pyqtSignal()

    toggle_cells_interaction_signal = pyqtSignal()
    show_hide_grid_signal = pyqtSignal()

    preview_pattern_signal = pyqtSignal(Pattern)
    stop_preview_pattern_signal = pyqtSignal()

    open_add_custom_pattern_dialog_signal = pyqtSignal()
    add_custom_pattern_signal = pyqtSignal(Pattern)

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Controller, cls).__new__(cls)
            cls._instance._initialized = False

        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        super().__init__()
        self._initialized = True

        self.grid: np.ndarray = np.full((self.NB_ROWS, self.NB_COLS), False, dtype=bool)
        self.timer: QTimer = QTimer()
        self.timer.timeout.connect(self._step_simulation)

        self.iteration_limit: int = None
        self.current_iteration: int = None
        self.rules = None

    def close_application(self):
        self.close_application_signal.emit()

    def toggle_cell_alive(self, row: int, col: int):
        self.grid[row, col] = not self.grid[row, col]

    def start_simulation(self, rules: str, speed: int, iterations: int):
        self.start_simulation_signal.emit()
        self.toggle_cells_interaction_signal.emit()

        self.rules = GAME_RULES_REGISTRY.get(rules)

        self.iteration_limit = iterations
        self.current_iteration = 0

        interval: int = int(1000 / speed)
        self.timer.start(interval)

    def pause_simulation(self):
        self.timer.stop()
        self.toggle_cells_interaction_signal.emit()
        self.pause_simulation_signal.emit()

    def clear_simulation(self):
        self.grid = np.full((self.NB_ROWS, self.NB_COLS), False, dtype=bool)
        self.clear_simulation_signal.emit()

    def _step_simulation(self):
        if self.iteration_limit and self.current_iteration >= self.iteration_limit:
            self.pause_simulation()
            return

        new_grid: np.ndarray = self.rules(self.grid)
        changed_cells: list[tuple[int, int]] = [
            (x, y)
            for x in range(self.NB_ROWS)
            for y in range(self.NB_COLS)
            if new_grid[x, y] != self.grid[x, y]
        ]
        self.grid = new_grid
        self.update_scene_signal.emit(changed_cells)
        self.current_iteration += 1

    def show_games_rules_help(self):
        help_dialog = QMessageBox()
        help_dialog.setWindowTitle("Game rules help")
        help_dialog.setText(
            "Different game rules are available. The 'B/S' notation means:\n"
            "- 'B' stands for 'Birth': the conditions under which a dead cell becomes alive,\n"
            "- 'S' stands for 'Survival': the conditions under which a living cell stays alive.\n"
            "\n"
            "Example with Conway (B3/S23) rules:\n"
            "- 'B3' means a dead cell becomes alive if it has exactly 3 living neighbors,\n"
            "- 'S23' means a living cell stays alive if it has 2 or 3 living neighbors."
        )
        help_dialog.setIcon(QMessageBox.Information)
        help_dialog.setStandardButtons(QMessageBox.Ok)
        help_dialog.setModal(True)
        help_dialog.exec_()

    def show_patterns_help(self):
        help_dialog = QMessageBox()
        help_dialog.setWindowTitle("Patterns help")
        help_dialog.setText(
            "Patterns are predefined configurations of cells that can be placed on the grid.\n"
            "\n"
            "The ones already available are made to work with the Conway rules:\n"
            "- Canons: structures that periodically produce spaceships,\n"
            "- Oscillators: patterns that return to their original configuration after a fixed number of generations,\n"
            "- Spaceships: patterns that travel across the grid over time while periodically returning to their original shape,\n"
            "- Still lifes: patterns that are completely stable,\n"
            "- Puffers: moving patterns that leave behind a trail of debris,\n"
            "- Mathusalems: small starting patterns that take a very large number of generations to stabilize.\n"
            "\n"
            "You can add custom patterns by clicking the 'Add' button in the Customs tab."
        )
        help_dialog.setIcon(QMessageBox.Information)
        help_dialog.setStandardButtons(QMessageBox.Ok)
        help_dialog.setModal(True)
        help_dialog.exec_()

    def show_iterations_help(self):
        help_dialog = QMessageBox()
        help_dialog.setWindowTitle("Iterations help")
        help_dialog.setText(
            "The number of iterations is the number of generations the simulation will run before stopping.\n"
            "If you set it to 0, the simulation will run indefinitely until you pause it."
        )
        help_dialog.setIcon(QMessageBox.Information)
        help_dialog.setStandardButtons(QMessageBox.Ok)
        help_dialog.setModal(True)
        help_dialog.exec_()

    def show_hide_grid(self):
        self.show_hide_grid_signal.emit()

    def preview_pattern(self, pattern: Pattern):
        self.preview_pattern_signal.emit(pattern)

    def stop_preview_pattern(self):
        self.stop_preview_pattern_signal.emit()

    def open_add_custom_pattern_dialog(self):
        self.open_add_custom_pattern_dialog_signal.emit()

    def add_custom_pattern(self, pattern: Pattern):
        save_pattern_to_file(pattern)
        self.add_custom_pattern_signal.emit(pattern)
