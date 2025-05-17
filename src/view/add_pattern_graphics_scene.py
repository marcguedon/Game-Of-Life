from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QMouseEvent, QBrush
from PyQt5.QtCore import Qt
from view.cell import Cell


class AddPatternGraphicsScene(QGraphicsScene):
    def __init__(self, nb_rows: int = 10, nb_cols: int = 10, cell_size: int = 15):
        super().__init__()

        self.nb_rows: int = nb_rows
        self.nb_cols: int = nb_cols
        self.cell_size: int = cell_size

        self.cells_interaction_enabled: bool = True
        self._mouse_dragging: bool = False
        self._visited_cells = set()
        self._drag_initial_state: bool = None

        self.setBackgroundBrush(QBrush(Qt.black))

        for row in range(self.nb_rows):
            for col in range(self.nb_cols):
                cell: Cell = Cell(col, row, cell_size)
                self.addItem(cell)

    def clear_scene(self):
        for item in self.items():
            if isinstance(item, Cell):
                item.set_alive(False)

    def mousePressEvent(self, event: QMouseEvent):
        # Enable cell toggling on mouse press
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

    def mouseMoveEvent(self, event: QMouseEvent):
        pos = event.scenePos()
        item = self.itemAt(pos, self.views()[0].transform())

        if not isinstance(item, Cell):
            return

        # Toggle cell state on mouse move
        if self.cells_interaction_enabled and self._mouse_dragging:
            if item not in self._visited_cells:
                self._visited_cells.add(item)
                item.set_alive(self._drag_initial_state)

    def mouseReleaseEvent(self, event: QMouseEvent):
        # Disable cell toggling when the mouse is released
        if event.button() == Qt.LeftButton:
            self._mouse_dragging = False
            self._visited_cells.clear()
            self._drag_initial_state = None
