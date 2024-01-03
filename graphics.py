###########################################
#   Python Roguelike Graphics Processing  #
# Separated to keep the main code cleaner #
###########################################
import numpy as np
import pygame #i swear if you give me a redundant import error i will shit my pants

 # Edit this if you want to change how many pixels per tile
def render_map_data(map_data, tilemap, graphicsScale = 32):
    #load the tilemap:

    floor_tile = tilemap.subsurface(0,0,graphicsScale,graphicsScale)
    wall_tile = tilemap.subsurface(0,graphicsScale,graphicsScale,graphicsScale)
    map_dims = map_data.shape #get the map array shape
    map_surface = pygame.Surface((map_dims[0] * graphicsScale, map_dims[1] * graphicsScale))
# I think this is a slow method, but it's what I have in my head right now. I'll figure something better out eventually.
    tiles_to_write = []
    map_x_count = 0
    while map_x_count < map_dims [0]:
        map_y_count = 0
        while map_y_count < map_dims[1]:
            tileType = map_data[map_x_count, map_y_count].sprite[0]
            if tileType == "floor": #For now, just do if/else, maybe index tiles in the map data itself? i.e. assign each one a number, then have an array of tile objects to choose from?
                write_tile = floor_tile
            else:
                write_tile = wall_tile
            tiles_to_write.append([write_tile, (map_x_count * graphicsScale, map_y_count * graphicsScale)])
            map_y_count += 1
        map_x_count += 1
    map_surface.blits(tiles_to_write)
    return map_surface #output the surface so it can be drawn to the screen.

def draw_new_frame():
    pass