import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import QMessageBox
from pattern import Pattern
from game_rules import (
    conway_rules,
    highlife_rules,
    seeds_rules,
    day_and_night_rules,
    life_wo_death_rules,
    diamoeba_rules,
    replicator_rules,
    anneal_rules,
)


class Controller(QObject):
    _instance = None

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
        self.timer = QTimer()
        self.timer.timeout.connect(self._step_simulation)

        self.iteration_limit: int = None
        self.current_iteration: int = None
        self.rules = None

    def close_application(self):
        self.close_application_signal.emit()

    def toggle_cell_alive(self, row: int, col: int):
        if self.grid[row, col]:
            self.grid[row, col] = False
        else:
            self.grid[row, col] = True

    def start_simulation(self, rules: str, speed: int, iterations: int):
        self.start_simulation_signal.emit()
        self.toggle_cells_interaction_signal.emit()

        if rules == "Conway (B3/S23) rules":
            self.rules = conway_rules

        elif rules == "HighLife (B36/S23) rules":
            self.rules = highlife_rules

        elif rules == "Seeds (B2/S) rules":
            self.rules = seeds_rules

        elif rules == "Day and Night (B3678/S34678) rules":
            self.rules = day_and_night_rules

        elif rules == "Life w/o death (B3/S012345678) rules":
            self.rules = life_wo_death_rules

        elif rules == "Diamoeba (B35678/S5678) rules":
            self.rules = diamoeba_rules

        elif rules == "Replicator (B1357/S1357) rules":
            self.rules = replicator_rules

        elif rules == "Anneal (B4678/S35678) rules":
            self.rules = anneal_rules

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

    def show_help(self):
        help_dialog = QMessageBox()
        help_dialog.setWindowTitle("Help")
        help_dialog.setText(
            "This is a simulation of Conway's Game of Life and other cellular automata.\n"
            "You can select different rules and adjust the game speed.\n"
            "Click on the grid to toggle cell states."
        )
        help_dialog.setIcon(QMessageBox.Information)
        help_dialog.setStandardButtons(QMessageBox.Ok)
        help_dialog.setModal(True)
        help_dialog.exec_()

    def show_hide_grid(self):
        self.show_hide_grid_signal.emit()

    def preview_pattern(self, pattern: Pattern):
        self.preview_pattern_signal.emit(pattern)

    def add_custom_pattern(self):
        print("Add custom pattern clicked")
        pass
