import numpy as np
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt
from cell import Cell


class GridGraphicsScene(QGraphicsScene):
    def __init__(self, nb_rows: int = 146, nb_cols: int = 225, cell_size: int = 20):
        super().__init__()

        self.shape: tuple[int, int] = nb_rows, nb_cols
        self.cell_size: int = cell_size
        self.grid: np.ndarray = np.empty((self.shape[0], self.shape[1]), dtype=Cell)

        self.cells_interaction_enabled: bool = True
        self._mouse_dragging: bool = False
        self._visited_cells = set()
        self._drag_initial_state: bool = None

        for row in range(self.shape[0]):
            for col in range(self.shape[1]):
                cell: Cell = Cell(col, row, cell_size)
                self.addItem(cell)
                self.grid[row, col] = cell

    def clear(self):
        for row in range(self.shape[0]):
            for col in range(self.shape[1]):
                self.grid[row, col].set_alive(False)

    def set_cell_alive(self, row: int, col: int, alive: bool):
        self.grid[row, col].set_alive(alive)

    def is_cell_alive(self, row: int, col: int) -> bool:
        return self.grid[row, col].is_alive()

    def disable_cells_interaction(self):
        self.cells_interaction_enabled = False

    def enable_cells_interaction(self):
        self.cells_interaction_enabled = True

    def mousePressEvent(self, event: QMouseEvent):
        if not self.cells_interaction_enabled:
            return

        pos = event.scenePos()
        item = self.itemAt(pos, self.views()[0].transform())

        if isinstance(item, Cell):
            if event.button() == Qt.LeftButton:
                self._mouse_dragging = True
                self._visited_cells = set()
                self._visited_cells.add(item)
                self._drag_initial_state = not item.is_alive()
                item.set_alive(self._drag_initial_state)

        else:
            raise ValueError(
                "Invalid item clicked in the scene. Expected a Cell instance."
            )

    def mouseMoveEvent(self, event: QMouseEvent):
        if not self.cells_interaction_enabled or not self._mouse_dragging:
            return

        pos = event.scenePos()
        item = self.itemAt(pos, self.views()[0].transform())

        if isinstance(item, Cell):
            if item not in self._visited_cells:
                item.set_alive(self._drag_initial_state)
                self._visited_cells.add(item)

        else:
            raise ValueError(
                "Invalid item clicked in the scene. Expected a Cell instance."
            )

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._mouse_dragging = False
            self._visited_cells.clear()
            self._drag_initial_state = None
