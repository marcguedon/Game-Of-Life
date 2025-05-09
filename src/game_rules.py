from grid_graphics_scene import GridGraphicsScene


def count_neighbors(grid: GridGraphicsScene, row: int, col: int) -> int:
    rows, cols = grid.shape

    count = 0

    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue

            nr, nc = row + dr, col + dc

            if 0 <= nr < rows and 0 <= nc < cols:
                count += grid.is_cell_alive(nr, nc)

    return count


def conway_rules(grid: GridGraphicsScene):
    nb_rows, nb_cols = grid.shape
    cell_size = grid.cell_size

    new_grid = GridGraphicsScene(nb_rows, nb_cols, cell_size)

    for row in range(nb_rows):
        for col in range(nb_cols):
            neighbors = count_neighbors(grid, row, col)

            if grid.is_cell_alive(row, col):
                new_grid.set_cell_alive(row, col, neighbors in [2, 3])

            else:
                new_grid.set_cell_alive(row, col, neighbors == 3)

    return new_grid


def highlife_rules(grid: GridGraphicsScene):
    nb_rows, nb_cols = grid.shape
    cell_size = grid.cell_size

    new_grid = GridGraphicsScene(nb_rows, nb_cols, cell_size)

    for row in range(nb_rows):
        for col in range(nb_cols):
            neighbors = count_neighbors(grid, row, col)

            if grid.is_cell_alive(row, col):
                new_grid.set_cell_alive(row, col, neighbors in [2, 3])

            else:
                new_grid.set_cell_alive(row, col, neighbors == 3 or neighbors == 6)

    return new_grid


def seeds_rules(grid: GridGraphicsScene):
    nb_rows, nb_cols = grid.shape
    cell_size = grid.cell_size

    new_grid = GridGraphicsScene(nb_rows, nb_cols, cell_size)

    for row in range(nb_rows):
        for col in range(nb_cols):
            neighbors = count_neighbors(grid, row, col)

            if grid.is_cell_alive(row, col):
                new_grid.set_cell_alive(row, col, neighbors in [2, 3])

            else:
                new_grid.set_cell_alive(row, col, neighbors == 2)

    return new_grid


def day_and_night_rules(grid: GridGraphicsScene):
    nb_rows, nb_cols = grid.shape
    cell_size = grid.cell_size

    new_grid = GridGraphicsScene(nb_rows, nb_cols, cell_size)

    for row in range(nb_rows):
        for col in range(nb_cols):
            neighbors = count_neighbors(grid, row, col)

            if grid.is_cell_alive(row, col):
                new_grid.set_cell_alive(row, col, neighbors in [2, 3])

            else:
                new_grid.set_cell_alive(row, col, neighbors == 3 or neighbors == 6)

    return new_grid
