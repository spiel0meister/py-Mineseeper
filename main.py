from random import randint
import pygame


def get_neighbors(x, y, rows, cols):
    neighbors = []

    if x > 0:
        neighbors.append((x-1, y))
    if x < cols - 1:
        neighbors.append((x+1, y))
    if y > 0:
        neighbors.append((x, y-1))
    if y < rows - 1:
        neighbors.append((x, y+1))

    if x > 0:
        if y > 0:
            neighbors.append((x-1, y-1))
        if y < rows - 1:
            neighbors.append((x-1, y+1))
    if x < cols - 1:
        if y > 0:
            neighbors.append((x+1, y-1))
        if y < rows - 1:
            neighbors.append((x+1, y+1))

    return neighbors


def create_grid(rows, cols, bombs=None):
    if bombs is None:
        bombs = rows * cols * .33
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    count = 0
    bomb_pos = []
    while count < bombs:
        y = randint(0, rows - 1)
        x = randint(0, cols - 1)
        if grid[y][x] == -1:
            continue
        grid[y][x] = -1
        bomb_pos.append((x, y))
        count += 1
    for x, y in bomb_pos:
        neighbors = get_neighbors(x, y, rows, cols)
        for x, y in neighbors:
            if grid[y][x] != -1:
                grid[y][x] += 1
    return grid


COVER_MAP = {0: "covered", 1: "uncovered", -1: "flagged"}


def create_cover_grid(grid):
    return [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]


pygame.init()
WIDTH, HEIGHT = 400, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

ROWS, COLS = 10, 10
CELL_W = WIDTH / COLS
CELL_H = HEIGHT / ROWS

COLORS = {"red": (255, 0, 0), "white": (255, 255, 255), "black": (0, 0, 0)}


def draw():
    WIN.fill(COLORS["black"])


def main():
    grid = create_grid(ROWS, COLS)
    cover_grid = create_cover_grid(grid)

    for row in grid:
        print(row)
    for row in cover_grid:
        print(row)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        draw()
        pygame.display.update()


if __name__ == "__main__":
    main()