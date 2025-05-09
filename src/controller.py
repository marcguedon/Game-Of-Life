from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from grid_graphics_scene import GridGraphicsScene
from game_rules import (
    conway_rules,
    highlife_rules,
    seeds_rules,
    day_and_night_rules,
)


class Controller(QObject):
    _instance = None

    close_application_signal = pyqtSignal()
    clear_simulation_signal = pyqtSignal()
    update_scene_signal = pyqtSignal(GridGraphicsScene)

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

        self.grid_graphics_scene: GridGraphicsScene = GridGraphicsScene()
        self.timer = QTimer()
        self.timer.timeout.connect(self._step_simulation)

        self.iteration_limit: int = 0
        self.current_iteration: int = 0
        self.rules: function = None

    def close_application(self):
        self.close_application_signal.emit()

    def start_simulation(self, rules: str, speed: int, iterations: int):
        self.grid_graphics_scene.disable_cells_interaction()

        if rules == "Conway rules":
            self.rules = conway_rules

        elif rules == "HighLife rules":
            self.rules = highlife_rules

        elif rules == "Seeds rules":
            self.rules = seeds_rules

        elif rules == "Day and Night rules":
            self.rules = day_and_night_rules

        self.iteration_limit = iterations
        self.current_iteration = 0

        interval: int = int(1000 / max(1, min(speed, 10)))
        self.timer.start(interval)

    def pause_simulation(self):
        self.timer.stop()
        self.grid_graphics_scene.enable_cells_interaction()

    def clear_simulation(self):
        self.grid_graphics_scene.clear()

    def _step_simulation(self):
        if self.iteration_limit and self.current_iteration >= self.iteration_limit:
            self.pause_simulation()
            return

        self.grid_graphics_scene = self.rules(self.grid_graphics_scene)
        self.update_scene_signal.emit(self.grid_graphics_scene)
        self.current_iteration += 1
