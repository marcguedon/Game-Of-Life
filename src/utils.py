import cv2
import numpy as np

BLACK = 0
WHITE = 255
GRAY = 128
CELL_SIZE = 20


def from_pattern_to_image(pattern: list[list[int]]) -> np.ndarray:
    nb_rows: int = len(pattern)
    nb_cols: int = len(pattern[0])
    height: int = nb_rows * CELL_SIZE
    width: int = nb_cols * CELL_SIZE

    image: np.ndarray = np.full((height, width, 1), WHITE, dtype=np.uint8)

    for y in range(nb_rows):
        for x in range(nb_cols):
            top_left: int = (x * CELL_SIZE, y * CELL_SIZE)
            bottom_right: int = ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE)
            color: int = GRAY if pattern[y][x] else WHITE

            cv2.rectangle(image, top_left, bottom_right, color, thickness=-1)

    for y in range(nb_rows + 1):
        y_coord: int = y * CELL_SIZE

        cv2.line(image, (0, y_coord), (width, y_coord), BLACK, 1)

    for x in range(nb_cols + 1):
        x_coord: int = x * CELL_SIZE

        cv2.line(image, (x_coord, 0), (x_coord, height), BLACK, 1)

    return image
