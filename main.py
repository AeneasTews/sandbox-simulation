import random
import pygame as pg

# setup pg
pg.init()

size = (500, 500)
screen = pg.display.set_mode(size)
fps = 60
clock = pg.time.Clock()

# setup game
# intialize cell types
EMPTY, SAND = 0, 1

# initiate sand colors
COLORS = [(0, 0, 0)]

SAND_COLORS = [(246, 215, 176), (242, 210, 169), (236, 204, 162), (231, 196, 150), (225, 191, 146)]
DUNE_COLORS = [(171, 148, 107), (186, 166, 132), (137, 120, 105), (182, 174, 166), (154, 140, 122)]

DIRT_COLORS = [(234, 208, 168), (182, 159, 102), (107, 84, 40), (118, 85, 43), (64, 41, 5)]
BROWN_DIRT_COLORS = [(90, 79, 62), (114, 93, 76), (79, 58, 43), (43, 24, 12), (51, 36, 25)]

# picked_colors = 0
# while not [1, 2, 3].__contains__(picked_colors):
#     picked_colors = int(input("Please select color palettes:\n"
#                               "1: sand colors\n"
#                               "2: dune colors\n"
#                               "3: sand and dune colors\n"))
#
# if picked_colors == 1:
#     COLORS.append(SAND_COLORS)
# elif picked_colors == 2:
#     COLORS.append(DUNE_COLORS)
# elif picked_colors == 3:
#     COLORS.append(SAND_COLORS + DUNE_COLORS]
COLORS.append(SAND_COLORS + DUNE_COLORS)
COLORS.append(DIRT_COLORS + BROWN_DIRT_COLORS)

# set up cursor and brush
# cursor_size = int(input("Please choose a cursor size: "))
cursor_size = 3
paint = SAND

# create grid
GRID_WIDTH = 100
GRID_HEIGHT = 100

CELL_WIDTH = size[0] / GRID_WIDTH
CELL_HEIGHT = size[1] / GRID_HEIGHT

grid = [[(EMPTY, COLORS[EMPTY]) for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]


def draw_grid():
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if grid[row][col][0] != EMPTY:
                pg.draw.rect(screen, grid[row][col][1], ((col * CELL_WIDTH, row * CELL_HEIGHT), (CELL_WIDTH, CELL_HEIGHT)))


def add_cell():
    mouse_pos = pg.mouse.get_pos()
    for i in range(cursor_size):
        for j in range(cursor_size):
            x = int(mouse_pos[0] / CELL_WIDTH + (cursor_size / 2 - i))
            y = int(mouse_pos[1] / CELL_HEIGHT + (cursor_size / 2 - j))

            if 0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH:
                grid[y][x] = (paint, random.choice(COLORS[paint]))


def check_mouse():
    if pg.mouse.get_pressed()[0]:
        add_cell()


def update_grid():
    global grid
    # create a new empty grid
    next_grid = [[(EMPTY, COLORS[EMPTY]) for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]

    # copy the bottom row to the new grid, since it isn't checked in the loops
    next_grid[len(grid) - 1] = grid[len(grid) - 1]

    # check every cell for its value
    for row in range(GRID_HEIGHT - 1):
        for col in range(GRID_WIDTH):

            # check every cell, that isn't empty
            if grid[row][col][0] != EMPTY:
                # copy all cells that have a value to the next grid
                next_grid[row][col] = grid[row][col]

                # check if a cell doesn't have a filled cell below it
                if grid[row + 1][col][0] == EMPTY:
                    # empty the current cell and fill the one below it
                    next_grid[row][col] = (EMPTY, COLORS[EMPTY])
                    next_grid[row + 1][col] = grid[row][col]

                    continue

                # generate a random direction for the cell to 'fall' to if the appropriate one is empty in order to
                # avoid it always filling up the right side first
                drop_dir = random.choice([-1, 1])

                # check if the outside columns are being checked
                if col != GRID_WIDTH - 1 and col != 0:
                    # check if the cell to the bottom right is empty
                    if grid[row + 1][col + drop_dir][0] == EMPTY:
                        next_grid[row][col] = (EMPTY, COLORS[EMPTY])
                        next_grid[row + 1][col + drop_dir] = grid[row][col]

                    # check if the cell to the bottom left is empty
                    elif grid[row + 1][col - drop_dir][0] == EMPTY:
                        next_grid[row][col] = (EMPTY, COLORS[EMPTY])
                        next_grid[row + 1][col - drop_dir] = grid[row][col]

                # handle outside columns separately in order to avoid list index errors
                else:
                    if col == 0:
                        if grid[row + 1][col + 1][0] == EMPTY:
                            next_grid[row][col] = (EMPTY, COLORS[EMPTY])
                            next_grid[row + 1][col + 1] = grid[row][col]
                    else:
                        if grid[row + 1][col - 1][0] == EMPTY:
                            next_grid[row][col] = (EMPTY, COLORS[EMPTY])
                            next_grid[row + 1][col - 1] = grid[row][col]

    grid = next_grid


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    # check for new cells being placed
    check_mouse()

    # clear the screen
    screen.fill(COLORS[EMPTY])

    # check the grid for falling
    update_grid()

    # draw the grid
    draw_grid()

    pg.display.flip()
    clock.tick(fps)
