import numpy as np


def _count_neighbors(grid: np.ndarray, cell_row: int, cell_col: int) -> int:
    nb_rows, nb_cols = grid.shape

    nb_neighbors = 0

    for row_offset in (-1, 0, 1):
        for col_offset in (-1, 0, 1):
            if row_offset == 0 and col_offset == 0:
                continue

            neighbor_row, neighbor_col = cell_row + row_offset, cell_col + col_offset

            if 0 <= neighbor_row < nb_rows and 0 <= neighbor_col < nb_cols:
                nb_neighbors += grid[neighbor_row, neighbor_col]

    return nb_neighbors


def conway_rules(grid: np.ndarray) -> np.ndarray:
    nb_rows, nb_cols = grid.shape

    new_grid = np.full((nb_rows, nb_cols), False, dtype=bool)

    for cell_row in range(nb_rows):
        for cell_col in range(nb_cols):
            nb_neighbors = _count_neighbors(grid, cell_row, cell_col)

            if grid[cell_row, cell_col]:
                new_grid[cell_row, cell_col] = nb_neighbors in [2, 3]

            else:
                new_grid[cell_row, cell_col] = nb_neighbors == 3

    return new_grid


def highlife_rules(grid: np.ndarray) -> np.ndarray:
    nb_rows, nb_cols = grid.shape

    new_grid = np.full((nb_rows, nb_cols), False, dtype=bool)

    for cell_row in range(nb_rows):
        for cell_col in range(nb_cols):
            nb_neighbors = _count_neighbors(grid, cell_row, cell_col)

            if grid[cell_row, cell_col]:
                new_grid[cell_row, cell_col] = nb_neighbors in [2, 3]

            else:
                new_grid[cell_row, cell_col] = nb_neighbors in [3, 6]

    return new_grid


def day_and_night_rules(grid: np.ndarray) -> np.ndarray:
    nb_rows, nb_cols = grid.shape

    new_grid = np.full((nb_rows, nb_cols), False, dtype=bool)

    for cell_row in range(nb_rows):
        for cell_col in range(nb_cols):
            nb_neighbors = _count_neighbors(grid, cell_row, cell_col)

            if grid[cell_row, cell_col]:
                new_grid[cell_row, cell_col] = nb_neighbors in [3, 4, 6, 7, 8]

            else:
                new_grid[cell_row, cell_col] = nb_neighbors in [3, 6, 7, 8]

    return new_grid


def seeds_rules(grid: np.ndarray) -> np.ndarray:
    nb_rows, nb_cols = grid.shape

    new_grid = np.full((nb_rows, nb_cols), False, dtype=bool)

    for cell_row in range(nb_rows):
        for cell_col in range(nb_cols):
            nb_neighbors = _count_neighbors(grid, cell_row, cell_col)

            if grid[cell_row, cell_col]:
                new_grid[cell_row, cell_col] = False

            else:
                new_grid[cell_row, cell_col] = nb_neighbors == 2

    return new_grid


def life_wo_death_rules(grid: np.ndarray) -> np.ndarray:
    nb_rows, nb_cols = grid.shape

    new_grid = np.full((nb_rows, nb_cols), False, dtype=bool)

    for cell_row in range(nb_rows):
        for cell_col in range(nb_cols):
            nb_neighbors = _count_neighbors(grid, cell_row, cell_col)

            if grid[cell_row, cell_col]:
                new_grid[cell_row, cell_col] = nb_neighbors in [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                ]

            else:
                new_grid[cell_row, cell_col] = nb_neighbors == 3

    return new_grid


def diamoeba_rules(grid: np.ndarray) -> np.ndarray:
    nb_rows, nb_cols = grid.shape

    new_grid = np.full((nb_rows, nb_cols), False, dtype=bool)

    for cell_row in range(nb_rows):
        for cell_col in range(nb_cols):
            nb_neighbors = _count_neighbors(grid, cell_row, cell_col)

            if grid[cell_row, cell_col]:
                new_grid[cell_row, cell_col] = nb_neighbors in [5, 6, 7, 8]

            else:
                new_grid[cell_row, cell_col] = nb_neighbors in [3, 5, 6, 7, 8]

    return new_grid


def replicator_rules(grid: np.ndarray) -> np.ndarray:
    nb_rows, nb_cols = grid.shape

    new_grid = np.full((nb_rows, nb_cols), False, dtype=bool)

    for cell_row in range(nb_rows):
        for cell_col in range(nb_cols):
            nb_neighbors = _count_neighbors(grid, cell_row, cell_col)

            if grid[cell_row, cell_col]:
                new_grid[cell_row, cell_col] = nb_neighbors in [1, 3, 5, 7]

            else:
                new_grid[cell_row, cell_col] = nb_neighbors in [1, 3, 5, 7]

    return new_grid


def anneal_rules(grid: np.ndarray) -> np.ndarray:
    nb_rows, nb_cols = grid.shape

    new_grid = np.full((nb_rows, nb_cols), False, dtype=bool)

    for cell_row in range(nb_rows):
        for cell_col in range(nb_cols):
            nb_neighbors = _count_neighbors(grid, cell_row, cell_col)

            if grid[cell_row, cell_col]:
                new_grid[cell_row, cell_col] = nb_neighbors in [3, 5, 6, 7, 8]

            else:
                new_grid[cell_row, cell_col] = nb_neighbors in [4, 6, 7, 8]

    return new_grid
