from itertools import product
import numpy as np


def _count_neighbors(grid: np.ndarray, cell_row: int, cell_col: int) -> int:
    nb_rows, nb_cols = grid.shape
    nb_neighbors: int = 0

    for row_offset, col_offset in product((-1, 0, 1), repeat=2):
        if row_offset == 0 and col_offset == 0:
            continue

        neighbor_row, neighbor_col = cell_row + row_offset, cell_col + col_offset

        if 0 <= neighbor_row < nb_rows and 0 <= neighbor_col < nb_cols:
            nb_neighbors += grid[neighbor_row, neighbor_col]

    return nb_neighbors


def _get_cells_to_check(grid: np.ndarray) -> set:
    nb_rows, nb_cols = grid.shape
    living_cells = np.argwhere(grid)
    neighbors_offsets = np.array(list(product((-1, 0, 1), repeat=2)))

    # Generating all neighbors for living cells
    all_neighbors = living_cells[:, None, :] + neighbors_offsets[None, :, :]
    all_neighbors = all_neighbors.reshape(-1, 2)

    # Filtering neighbors out of the grid
    valid_mask = (
        (all_neighbors[:, 0] >= 0)
        & (all_neighbors[:, 0] < nb_rows)
        & (all_neighbors[:, 1] >= 0)
        & (all_neighbors[:, 1] < nb_cols)
    )
    valid_neighbors = all_neighbors[valid_mask]

    cells_to_check = set(map(tuple, valid_neighbors))

    return cells_to_check


def conway_rules(grid: np.ndarray) -> np.ndarray:
    nb_rows, nb_cols = grid.shape
    new_grid = np.full((nb_rows, nb_cols), False, dtype=bool)

    cells_to_check = _get_cells_to_check(grid)

    for cell_row, cell_col in cells_to_check:
        nb_neighbors = _count_neighbors(grid, cell_row, cell_col)

        if grid[cell_row, cell_col]:
            new_grid[cell_row, cell_col] = nb_neighbors in [2, 3]
        else:
            new_grid[cell_row, cell_col] = nb_neighbors == 3

    return new_grid


def highlife_rules(grid: np.ndarray) -> np.ndarray:
    nb_rows, nb_cols = grid.shape
    new_grid = np.full((nb_rows, nb_cols), False, dtype=bool)

    cells_to_check = _get_cells_to_check(grid)

    for cell_row, cell_col in cells_to_check:
        nb_neighbors = _count_neighbors(grid, cell_row, cell_col)

        if grid[cell_row, cell_col]:
            new_grid[cell_row, cell_col] = nb_neighbors in [2, 3]

        else:
            new_grid[cell_row, cell_col] = nb_neighbors in [3, 6]

    return new_grid


def day_and_night_rules(grid: np.ndarray) -> np.ndarray:
    nb_rows, nb_cols = grid.shape
    new_grid = np.full((nb_rows, nb_cols), False, dtype=bool)

    cells_to_check = _get_cells_to_check(grid)

    for cell_row, cell_col in cells_to_check:
        nb_neighbors = _count_neighbors(grid, cell_row, cell_col)

        if grid[cell_row, cell_col]:
            new_grid[cell_row, cell_col] = nb_neighbors in [3, 4, 6, 7, 8]

        else:
            new_grid[cell_row, cell_col] = nb_neighbors in [3, 6, 7, 8]

    return new_grid


def seeds_rules(grid: np.ndarray) -> np.ndarray:
    nb_rows, nb_cols = grid.shape
    new_grid = np.full((nb_rows, nb_cols), False, dtype=bool)

    cells_to_check = _get_cells_to_check(grid)

    for cell_row, cell_col in cells_to_check:
        nb_neighbors = _count_neighbors(grid, cell_row, cell_col)

        if grid[cell_row, cell_col]:
            new_grid[cell_row, cell_col] = False

        else:
            new_grid[cell_row, cell_col] = nb_neighbors == 2

    return new_grid


def life_wo_death_rules(grid: np.ndarray) -> np.ndarray:
    nb_rows, nb_cols = grid.shape
    new_grid = np.full((nb_rows, nb_cols), False, dtype=bool)

    cells_to_check = _get_cells_to_check(grid)

    for cell_row, cell_col in cells_to_check:
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

    cells_to_check = _get_cells_to_check(grid)

    for cell_row, cell_col in cells_to_check:
        nb_neighbors = _count_neighbors(grid, cell_row, cell_col)

        if grid[cell_row, cell_col]:
            new_grid[cell_row, cell_col] = nb_neighbors in [5, 6, 7, 8]

        else:
            new_grid[cell_row, cell_col] = nb_neighbors in [3, 5, 6, 7, 8]

    return new_grid


def replicator_rules(grid: np.ndarray) -> np.ndarray:
    nb_rows, nb_cols = grid.shape
    new_grid = np.full((nb_rows, nb_cols), False, dtype=bool)

    cells_to_check = _get_cells_to_check(grid)

    for cell_row, cell_col in cells_to_check:
        nb_neighbors = _count_neighbors(grid, cell_row, cell_col)

        new_grid[cell_row, cell_col] = nb_neighbors in [1, 3, 5, 7]

    return new_grid


def anneal_rules(grid: np.ndarray) -> np.ndarray:
    nb_rows, nb_cols = grid.shape
    new_grid = np.full((nb_rows, nb_cols), False, dtype=bool)

    cells_to_check = _get_cells_to_check(grid)

    for cell_row, cell_col in cells_to_check:
        nb_neighbors = _count_neighbors(grid, cell_row, cell_col)

        if grid[cell_row, cell_col]:
            new_grid[cell_row, cell_col] = nb_neighbors in [3, 5, 6, 7, 8]

        else:
            new_grid[cell_row, cell_col] = nb_neighbors in [4, 6, 7, 8]

    return new_grid


GAME_RULES_REGISTRY = {
    "Conway (B3/S23)": conway_rules,
    "HighLife (B36/S23)": highlife_rules,
    "Seeds (B2/S)": seeds_rules,
    "Day and Night (B3678/S34678)": day_and_night_rules,
    "Life w/o death (B3/S012345678)": life_wo_death_rules,
    "Diamoeba (B35678/S5678)": diamoeba_rules,
    "Replicator (B1357/S1357)": replicator_rules,
    "Anneal (B4678/S35678)": anneal_rules,
}
