import numpy as np
from PyQt5.QtGui import QIcon, QImage, QPixmap


class Pattern:
    def __init__(self, name: str, image: np.ndarray, matrix: list[list[bool]]):
        self.name: str = name
        self.image: np.ndarray = image
        self.height: int = len(matrix)
        self.width: int = len(matrix[0])
        self.matrix: list[list[bool]] = matrix

    def get_icon(self) -> QIcon:
        image_matrix: np.ndarray = np.array(self.image, dtype=np.uint8)

        image: QImage = QImage(
            image_matrix.data,
            image_matrix.shape[1],
            image_matrix.shape[0],
            image_matrix.shape[1],
            QImage.Format_Grayscale8,
        )
        pixmap: QPixmap = QPixmap.fromImage(image)
        icon: QIcon = QIcon(pixmap)

        return icon
