import os
import json
import cv2
import numpy as np
from model.pattern import Pattern

BLACK = 0
WHITE = 255
GRAY = 128
CELL_SIZE = 20


def from_pattern_to_image(pattern: list[list[bool]]) -> np.ndarray:
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


def save_pattern_to_file(pattern: Pattern):
    name: str = pattern.name.lower().replace(" ", "_")
    width: int = len(pattern.matrix[0])
    height: int = len(pattern.matrix)
    cells = pattern.matrix

    pattern_data = {
        "name": name,
        "pattern": {
            "width": width,
            "height": height,
            "cells": cells,
        },
    }

    json_data = json.dumps(pattern_data, indent=4)
    filename: str = f"{name}.json"

    custom_patterns_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "patterns", "customs"
    )

    # TODO: Manage already existing files

    with open(
        os.path.join(custom_patterns_dir, filename), "w", encoding="UTF-8"
    ) as file:
        file.write(json_data)


def load_pattern_from_file(filename: str) -> Pattern:
    with open(filename, encoding="UTF-8") as file:
        pattern_data = json.load(file)

    pattern_name: str = pattern_data["name"]
    pattern_cells: list[list[bool]] = pattern_data["pattern"]["cells"]

    pattern_image: np.ndarray = from_pattern_to_image(pattern_cells)

    pattern: Pattern = Pattern(
        name=pattern_name,
        image=pattern_image,
        matrix=pattern_cells,
    )

    return pattern
