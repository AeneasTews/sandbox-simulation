from color_palettes import *


class Element:
    def __init__(self, name, value, colors, has_gravity=True, density=1, is_liquid=False):
        self.name = name
        self.value = value
        self.colors = colors
        self.has_gravity = has_gravity
        self.density = density
        self.is_liquid = is_liquid


EMPTY = Element('empty', 0, EMPTY_COLORS, has_gravity=False)
SAND = Element('sand', 1, SAND_COLORS + DUNE_COLORS)
DIRT = Element('dirt', 2, BROWN_DIRT_COLORS)
STONE_WALL = Element('stone_wall', 3, STONE_WALL_COLORS, has_gravity=False)
WATER = Element('water', 4, WATER_COLORS, is_liquid=True)

ELEMENTS = {'empty': EMPTY,
            'sand': SAND,
            'dirt': DIRT,
            'stone_wall': STONE_WALL,
            'water': WATER}
