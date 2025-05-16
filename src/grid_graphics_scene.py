from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QMouseEvent, QTransform, QBrush
from PyQt5.QtCore import Qt
from controller import Controller
from cell import Cell
from pattern import Pattern


class GridGraphicsScene(QGraphicsScene):
    def __init__(self, nb_rows: int = 146, nb_cols: int = 225, cell_size: int = 20):
        super().__init__()

        self.controller = Controller()
        self.controller.clear_simulation_signal.connect(self.clear_scene)
        self.controller.update_scene_signal.connect(self.update_scene)
        self.controller.toggle_cells_interaction_signal.connect(
            self.toggle_cells_interaction
        )
        self.controller.show_hide_grid_signal.connect(self.toggle_grid)
        self.controller.preview_pattern_signal.connect(self.enable_preview_pattern)

        self.nb_rows: int = nb_rows
        self.nb_cols: int = nb_cols
        self.cell_size: int = cell_size

        self.cells_interaction_enabled: bool = True
        self._mouse_dragging: bool = False
        self._visited_cells = set()
        self._drag_initial_state: bool = None

        self._preview_enabled: bool = False
        self._preview_pattern: Pattern = None
        self._previewed_cells: set[Cell] = set()
        self._preview_original_states: dict[Cell, bool] = {}
        self._rotated_pattern_matrix: list[list[bool]] = None

        self.show_grid: bool = True
        self.setBackgroundBrush(QBrush(Qt.black))

        for row in range(self.nb_rows):
            for col in range(self.nb_cols):
                cell: Cell = Cell(col, row, cell_size)
                self.addItem(cell)

    def clear_scene(self):
        for item in self.items():
            if isinstance(item, Cell):
                item.set_alive(False)

    def update_scene(self, changed_cells: list[tuple[int, int]]):
        for row, col in changed_cells:
            cell: Cell = self.itemAt(
                col * self.cell_size, row * self.cell_size, QTransform()
            )
            if cell:
                cell.set_alive(not cell.is_alive())

        self.update()

    def toggle_cells_interaction(self):
        self.cells_interaction_enabled = not self.cells_interaction_enabled

    def toggle_grid(self):
        self.show_grid = not self.show_grid

        if self.show_grid:
            self.setBackgroundBrush(QBrush(Qt.black))

        else:
            self.setBackgroundBrush(QBrush(Qt.NoBrush))

        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if self.cells_interaction_enabled and self._preview_enabled:
            if event.button() == Qt.LeftButton:
                for cell in self._previewed_cells:
                    cell.set_alive(True)
                    self.controller.toggle_cell_alive(cell.row, cell.col)
                self._previewed_cells.clear()
                self._preview_enabled = False
                self._preview_pattern = None
                return

            if event.button() == Qt.RightButton:
                for cell in self._previewed_cells:
                    cell.set_alive_preview(False)
                    cell.set_alive(
                        self._preview_original_states.get(cell, cell.is_alive())
                    )
                self._previewed_cells.clear()
                self._preview_original_states.clear()
                self._preview_enabled = False
                self._preview_pattern = None
                return

        if self.cells_interaction_enabled:
            pos = event.scenePos()
            item = self.itemAt(pos, self.views()[0].transform())

            if isinstance(item, Cell):
                if event.button() == Qt.LeftButton:
                    self._mouse_dragging = True
                    self._visited_cells = set()
                    self._visited_cells.add(item)
                    self._drag_initial_state = not item.is_alive()
                    item.set_alive(self._drag_initial_state)
                    self.controller.toggle_cell_alive(item.row, item.col)

    def mouseMoveEvent(self, event: QMouseEvent):
        pos = event.scenePos()
        item = self.itemAt(pos, self.views()[0].transform())

        if not isinstance(item, Cell):
            return

        if self.cells_interaction_enabled and self._preview_enabled:
            for cell in self._previewed_cells:
                cell.set_alive_preview(False)
                # Restaure l'état visuel réel
                cell.set_alive(self._preview_original_states.get(cell, cell.is_alive()))
            self._previewed_cells.clear()
            self._preview_original_states.clear()

            pos = event.scenePos()
            item = self.itemAt(pos, self.views()[0].transform())

            if isinstance(item, Cell):
                start_row, start_col = item.row, item.col
                matrix = self._preview_pattern.matrix  # taille (N, M)
                pattern_rows = len(matrix)
                pattern_cols = len(matrix[0]) if matrix else 0

                for dy in range(pattern_rows):
                    for dx in range(pattern_cols):
                        if matrix[dy][dx]:  # Si cellule vivante dans le motif
                            target_row = start_row + dy
                            target_col = start_col + dx

                            if (
                                0 <= target_row < self.nb_rows
                                and 0 <= target_col < self.nb_cols
                            ):
                                cell = self.itemAt(
                                    target_col * self.cell_size,
                                    target_row * self.cell_size,
                                    QTransform(),
                                )
                                if isinstance(cell, Cell):
                                    self._preview_original_states[cell] = (
                                        cell.is_alive()
                                    )
                                    cell.set_alive_preview(True)
                                    self._previewed_cells.add(cell)

        if self.cells_interaction_enabled and self._mouse_dragging:
            if item not in self._visited_cells:
                self._visited_cells.add(item)
                item.set_alive(self._drag_initial_state)
                self.controller.toggle_cell_alive(item.row, item.col)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._mouse_dragging = False
            self._visited_cells.clear()
            self._drag_initial_state = None

    def enable_preview_pattern(self, pattern: Pattern):
        self._preview_enabled = True
        self._preview_pattern = pattern
        self._rotated_pattern_matrix = [row[:] for row in pattern.matrix]

    def _rotate_pattern_90(self):
        if self._rotated_pattern_matrix:
            self._rotated_pattern_matrix = [
                list(reversed(col)) for col in zip(*self._rotated_pattern_matrix)
            ]
