import numpy as np
from PyQt5.QtWidgets import QGraphicsScene
from cell import Cell


class GridGraphicsScene(QGraphicsScene):
    def __init__(self, nb_rows: int = 50, nb_cols: int = 50, cell_size: int = 20):
        super().__init__()

        self.shape: tuple[int, int] = nb_rows, nb_cols
        self.cell_size: int = cell_size
        self.cells_interaction_enabled: bool = True

        self._grid: np.ndarray = np.empty((self.shape[0], self.shape[1]), dtype=Cell)

        for row in range(self.shape[0]):
            for col in range(self.shape[1]):
                cell: Cell = Cell(col, row, cell_size)
                self.addItem(cell)
                self._grid[row, col] = cell

    def clear(self):
        for row in range(self.shape[0]):
            for col in range(self.shape[1]):
                self._grid[row, col].set_alive(False)

    def set_cell_alive(self, row: int, col: int, alive: bool):
        self._grid[row, col].set_alive(alive)

    def is_cell_alive(self, row: int, col: int) -> bool:
        return self._grid[row, col].is_alive()

    def enable_cells_interaction(self):
        for row in range(self.shape[0]):
            for col in range(self.shape[1]):
                self._grid[row, col].enable_mouse_events()

        self.cells_interaction_enabled = True

    def disable_cells_interaction(self):
        for row in range(self.shape[0]):
            for col in range(self.shape[1]):
                self._grid[row, col].disable_mouse_events()

        self.cells_interaction_enabled = False
