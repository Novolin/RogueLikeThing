###########################################
#   Python Roguelike Graphics Processing  #
# Separated to keep the main code cleaner #
###########################################
import numpy as np
import pygame 
from math import ceil, floor

 # Edit this if you want to change how many pixels per tile
def render_map_data(map_data, tilemap, playerPos, windowRes = (1024,768), graphicsScale = 32):
    #load the tilemap:
    floor_tile = tilemap.subsurface(0,0,graphicsScale,graphicsScale)
    wall_tile = tilemap.subsurface(0,graphicsScale,graphicsScale,graphicsScale)

    # Find the bounds of our camera space:
    map_dims = map_data.shape #for the map
    tile_count = (ceil(windowRes[0] / graphicsScale), ceil(windowRes[1]/graphicsScale)) #for the window
    camera_min = (floor(tile_count[0]/2), floor(tile_count[1]/2)) #left/upper bound
    camera_max = (map_dims[0] - camera_min[0], map_dims[1] - camera_min[1]) # right/lower bound

    # find the top left square we want to render
    camera_origin = [playerPos[0] + camera_min[0], playerPos[1] + camera_min[0]] 
    if camera_origin[0] < camera_min[0]:
        camera_origin[0] = camera_min[0]
    elif camera_origin[0] > camera_max[0]:
        camera_origin[0] = map_dims[0] - camera_min[0]
    if camera_origin[1] < camera_min[1]:
        camera_origin[1] = camera_min[1]
    elif camera_origin[1] > camera_max[1]:
        camera_origin[1] = map_dims[1] - camera_min[1]
    map_surface = pygame.Surface((tile_count[0] * graphicsScale, tile_count[1] * graphicsScale))
    # I think this is a slow method, but it's what I have in my head right now. I'll figure something better out eventually.
    tiles_to_write = []
    map_x_count = camera_origin[0] - tile_count[0]
    while map_x_count < camera_origin[0] + tile_count[0]:
        map_y_count = camera_origin[1]- tile_count[1]
        while map_y_count < camera_origin[1] + tile_count[1]:
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

def draw_actors(actorList):
    # Draw all actors passed to this function to the screen.
    pass
def debug_draw_scr_data(map_data, tilemap, playerPos, windowRes = (1024,768), graphicsScale = 32):
    map_dims = map_data.shape #for the map
    tile_count = (ceil(windowRes[0] / graphicsScale), ceil(windowRes[1]/graphicsScale)) #for the window
    camera_min = (floor(tile_count[0]/2), floor(tile_count[1]/2)) #left/upper bound
    camera_max = (map_dims[0] - camera_min[0], map_dims[1] - camera_min[1]) # right/lower bound
    camera_origin = [playerPos[0] - camera_min[0], playerPos[1] - camera_min[1]] 
    print(map_dims, tile_count, camera_max, camera_min, camera_origin)