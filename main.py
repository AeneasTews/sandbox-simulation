import random

import pygame as pg

# setup pg
pg.init()

size = (500, 500)
screen = pg.display.set_mode(size)
fps = 60
clock = pg.time.Clock()

# setup game
# create grid
grid_width = 100
grid_height = 100

cell_width = size[0] / grid_width
cell_height = size[1] / grid_height

grid = [[(0, 0, 0) for x in range(grid_width)] for y in range(grid_height)]

# initiate sand colors
sand_colors = [(246, 215, 176), (242, 210, 169), (236, 204, 162), (231, 196, 150), (225, 191, 146)]
dune_colors = [(171, 148, 107), (186, 166, 132), (137, 120, 105), (182, 174, 166), (154, 140, 122)]

picked_colors = 0
while not [1, 2, 3].__contains__(picked_colors):
    picked_colors = int(input("Please select color palettes:\n"
                              "1: sand colors\n"
                              "2: dune colors\n"
                              "3: sand and dune colors\n"))

if picked_colors == 1:
    colors = sand_colors
elif picked_colors == 2:
    colors = dune_colors
elif picked_colors == 3:
    colors = sand_colors + dune_colors

# set up cursor
cursor_size = int(input("Please choose a cursor size: "))


def draw_grid():
    for row in range(grid_height):
        for col in range(grid_width):
            pg.draw.rect(screen, grid[row][col], ((col * cell_width, row * cell_height), (cell_width, cell_height)))


def add_cell():
    mouse_pos = pg.mouse.get_pos()
    for i in range(cursor_size):
        for j in range(cursor_size):
            x = int(mouse_pos[0] / cell_width + (cursor_size / 2 - i))
            y = int(mouse_pos[1] / cell_height + (cursor_size / 2 - j))

            if 0 <= y < grid_height and 0 <= x < grid_width:
                grid[y][x] = random.choice(colors)


def check_mouse():
    if pg.mouse.get_pressed()[0]:
        add_cell()


def update_grid():
    global grid
    # create a new empty grid
    next_grid = [[(0, 0, 0) for x in range(grid_width)] for y in range(grid_height)]

    # copy the bottom row to the new grid, since it isn't checked in the loops
    next_grid[len(grid) - 1] = grid[len(grid) - 1]

    # check every cell for its value
    for row in range(grid_height - 1):
        for col in range(grid_width):

            # check every cell, that isn't empty
            if grid[row][col] != (0, 0, 0):
                # copy all cells that have a value to the next grid
                next_grid[row][col] = grid[row][col]

                # check if a cell doesn't have a filled cell below it
                if grid[row + 1][col] == (0, 0, 0):
                    # empty the current cell and fill the one below it
                    next_grid[row][col] = (0, 0, 0)
                    next_grid[row + 1][col] = grid[row][col]

                    continue

                # generate a random direction for the cell to 'fall' to if the appropriate one is empty in order to
                # avoid it always filling up the right side first
                drop_dir = random.choice([-1, 1])

                # check if the outside columns are being checked
                if col != grid_width - 1 and col != 0:
                    # check if the cell to the bottom right is empty
                    if grid[row + 1][col + drop_dir] == (0, 0, 0):
                        next_grid[row][col] = (0, 0, 0)
                        next_grid[row + 1][col + drop_dir] = grid[row][col]

                    # check if the cell to the bottom left is empty
                    elif grid[row + 1][col - drop_dir] == (0, 0, 0):
                        next_grid[row][col] = (0, 0, 0)
                        next_grid[row + 1][col - drop_dir] = grid[row][col]

                # handle outside columns separately in order to avoid list index errors
                else:
                    if col == 0:
                        if grid[row + 1][col + 1] == (0, 0, 0):
                            next_grid[row][col] = (0, 0, 0)
                            next_grid[row + 1][col + 1] = grid[row][col]
                    else:
                        if grid[row + 1][col - 1] == (0, 0, 0):
                            next_grid[row][col] = (0, 0, 0)
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
    screen.fill((0, 0, 0))

    # check the grid for falling
    update_grid()

    # draw the grid
    draw_grid()

    pg.display.flip()
    clock.tick(fps)
