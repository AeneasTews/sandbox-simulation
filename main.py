import random
import pygame as pg
from element_config import ELEMENTS

# setup pg
pg.init()

size = (500, 500)
screen = pg.display.set_mode(size)
fps = 60
clock = pg.time.Clock()

# setup game

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

# set up cursor and brush
# cursor_size = int(input("Please choose a cursor size: "))
cursor_size = 3
paint = ELEMENTS['dirt']

# create grid
GRID_WIDTH = 100
GRID_HEIGHT = 100

CELL_WIDTH = size[0] / GRID_WIDTH
CELL_HEIGHT = size[1] / GRID_HEIGHT

grid = [[(ELEMENTS['empty'], ELEMENTS['empty'].colors[0]) for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]

# animation fix
# this should absolutely be considered a botch
change_col_checking_dir = True


def draw_grid():
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if grid[row][col] != ELEMENTS['empty']:
                pg.draw.rect(screen, 
                             grid[row][col][1],
                             ((col * CELL_WIDTH, row * CELL_HEIGHT), (CELL_WIDTH, CELL_HEIGHT)))


def add_cell():
    mouse_pos = pg.mouse.get_pos()
    for i in range(cursor_size):
        for j in range(cursor_size):
            x = int(mouse_pos[0] / CELL_WIDTH + (cursor_size / 2 - i))
            y = int(mouse_pos[1] / CELL_HEIGHT + (cursor_size / 2 - j))

            if 0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH:
                grid[y][x] = (paint, random.choice(paint.colors))


def check_mouse():
    if pg.mouse.get_pressed()[0]:
        add_cell()


def update_grid():
    global grid

    # check every cell for its value
    for row in range(GRID_HEIGHT - 1):
        # reverse checking order this is necessary as falling objects would otherwise be checked multiple times per
        # frame
        row = GRID_HEIGHT - 2 - row
        for col in range(GRID_WIDTH):
            # change counting order
            if change_col_checking_dir:
                col = GRID_WIDTH - 1 - col

            current_cell = grid[row][col]

            # check every cell, that isn't empty
            if current_cell[0] != ELEMENTS['empty']:

                # check falling cell types
                if current_cell[0].has_gravity:
                    # generate a random direction for the cell to 'fall' to if the appropriate one is empty in order to
                    # avoid it always filling up the right side first
                    drop_dir = random.choice([-1, 1])

                    # check if the outside columns are being checked
                    if col != GRID_WIDTH - 1 and col != 0:
                        # check if a cell doesn't have a filled cell below it
                        if grid[row + 1][col][0] == ELEMENTS['empty']:
                            grid[row][col] = (ELEMENTS['empty'], ELEMENTS['empty'].colors[0])
                            grid[row + 1][col] = current_cell

                        # check if the cell to the bottom right is empty
                        elif grid[row + 1][col + drop_dir][0] == ELEMENTS['empty']:
                            grid[row][col] = (ELEMENTS['empty'], ELEMENTS['empty'].colors[0])
                            grid[row + 1][col + drop_dir] = current_cell

                        # check if the cell to the bottom left is empty
                        elif grid[row + 1][col - drop_dir][0] == ELEMENTS['empty']:
                            grid[row][col] = (ELEMENTS['empty'], ELEMENTS['empty'].colors[0])
                            grid[row + 1][col - drop_dir] = current_cell

                    # handle outside columns separately in order to avoid list index errors
                    else:
                        if col == 0:
                            if grid[row + 1][col + 1][0] == ELEMENTS['empty']:
                                grid[row][col] = (ELEMENTS['empty'], ELEMENTS['empty'].colors[0])
                                grid[row + 1][col + 1] = current_cell
                        else:
                            if grid[row + 1][col - 1][0] == ELEMENTS['empty']:
                                grid[row][col] = (ELEMENTS['empty'], ELEMENTS['empty'].colors[0])
                                grid[row + 1][col - 1] = current_cell

                # if the type is stationary, nothing else should be checked
                else:
                    pass

                if grid[row][col][0].is_liquid:
                    # random direction in order to balance
                    move_dir = random.choice([-1, 1])

                    if col != 0 and col != GRID_WIDTH - 1:
                        if grid[row][col - move_dir][0] == ELEMENTS['empty']:
                            grid[row][col - move_dir] = current_cell
                            grid[row][col] = (ELEMENTS['empty'], ELEMENTS['empty'].colors[0])

                        elif grid[row][col + move_dir][0] == ELEMENTS['empty']:
                            grid[row][col + move_dir] = current_cell
                            grid[row][col] = (ELEMENTS['empty'], ELEMENTS['empty'].colors[0])

                    elif col == 0:
                        if grid[row][col + 1][0] == ELEMENTS['empty']:
                            grid[row][col + 1] = current_cell
                            grid[row][col] = (ELEMENTS['empty'], ELEMENTS['empty'].colors[0])
                    else:
                        if grid[row][col - 1][0] == ELEMENTS['empty']:
                            grid[row][col - 1] = current_cell
                            grid[row][col] = (ELEMENTS['empty'], ELEMENTS['empty'].colors[0])


# initialize debug stuff
debug_frame_counter = 0
debug = False
debug_fps = 1
game_fps = fps
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_s:
                paint = ELEMENTS['sand']

            if event.key == pg.K_d:
                paint = ELEMENTS['dirt']

            if event.key == pg.K_e:
                paint = ELEMENTS['empty']

            if event.key == pg.K_w:
                paint = ELEMENTS['stone_wall']

            if event.key == pg.K_l:
                paint = ELEMENTS['water']

            # debug mode
            if event.key == pg.K_f:
                debug = not debug
                fps = debug_fps if fps == 60 else 60

            if event.key == pg.K_0:
                cursor_size = 0
            elif event.key == pg.K_1:
                cursor_size = 1
            elif event.key == pg.K_2:
                cursor_size = 2
            elif event.key == pg.K_3:
                cursor_size = 3
            elif event.key == pg.K_4:
                cursor_size = 4
            elif event.key == pg.K_5:
                cursor_size = 5
            elif event.key == pg.K_6:
                cursor_size = 6
            elif event.key == pg.K_7:
                cursor_size = 7
            elif event.key == pg.K_8:
                cursor_size = 8
            elif event.key == pg.K_9:
                cursor_size = 9

    # check for new cells being placed
    check_mouse()

    # clear the screen
    screen.fill(ELEMENTS['empty'].colors[0])

    # check the grid for falling
    update_grid()

    # draw the grid
    draw_grid()

    pg.display.flip()
    clock.tick(fps)

    # randomize / switch checking of columns
    # change_col_checking_dir = not change_col_checking_dir
    change_col_checking_dir = random.choice([True, False])

    if debug:
        pg.image.save(screen, f"./debug_images/{debug_frame_counter}.png")
        debug_frame_counter += 1
