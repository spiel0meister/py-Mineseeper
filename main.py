import itertools
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
font1 = pygame.font.SysFont('freesanbold.ttf', 50)
FPS_CLOCK = pygame.time.Clock()

ROWS, COLS = 10, 10
CELL_W = WIDTH / COLS
CELL_H = HEIGHT / ROWS

COLORS = {"red": (255, 0, 0), "white": (255, 255, 255), "black": (0, 0, 0)}


def draw(grid, cover_grid):
    WIN.fill(COLORS["black"])

    for y, x in itertools.product(range(ROWS), range(COLS)):
        if grid[y][x] != 0:
            text1 = font1.render(
                str(grid[y][x]) if grid[y][x] != -1 else "X", True, COLORS["white"])
            WIN.blit(text1, (x * CELL_W + (CELL_W/2 - text1.get_width()/2), y * CELL_H + (
                CELL_H/2 - text1.get_height()/2)))

    for y, x in itertools.product(range(ROWS), range(COLS)):
        value = cover_grid[y][x]
        if value != 1:
            if value == 0:
                color = COLORS["white"]
            elif value == -1:
                color = COLORS["red"]
            pygame.draw.rect(
                WIN, COLORS["black"], (x * CELL_W, y * CELL_H, CELL_W, CELL_H))
            pygame.draw.rect(
                WIN, color, (x * CELL_W, y * CELL_H, CELL_W - 2, CELL_H - 2))


def switch_cover(switch, x, y, grid, cover_grid):
    cover_grid[y][x] = switch
    if switch == 1 and grid[y][x] == 0:
        neighbors = get_neighbors(x, y, len(grid), len(grid[0]))
        for x, y in neighbors:
            if cover_grid[y][x] == 0:
                switch_cover(switch, x, y, grid, cover_grid)


def main():
    grid = create_grid(ROWS, COLS)
    cover_grid = create_cover_grid(grid)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                row, col = int(my/CELL_H), int(mx/CELL_W)
                left, _, right = pygame.mouse.get_pressed()
                if left:
                    switch_cover(1, col, row, grid, cover_grid)
                elif right:
                    if cover_grid[row][col] == -1:
                        switch_cover(0, col, row, grid, cover_grid)
                    else:
                        switch_cover(-1, col, row, grid, cover_grid)
        draw(grid, cover_grid)
        pygame.display.update()
        FPS_CLOCK.tick(30)


if __name__ == "__main__":
    main()
