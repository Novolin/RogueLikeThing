###########################################
#   Python Roguelike Graphics Processing  #
# Separated to keep the main code cleaner #
###########################################
import numpy as np
import pygame 
from math import ceil, floor

class Camera:
    # A Camera object that can be used to manage the viewport
    def __init__(self, target, cam_res = [1024,768], scale = 32):
        self.origin = [0,0] # Top Left X/Y
        self.target = target # What the camera is focused on, usually the player.
        self.viewport_resolution = cam_res # What is the size of the camera space (in case we do multi window/ui stuff?)
        self.scale = scale # How many pixels per tile
    def render_map_data(map_data, map_tilemap):
        floor_tile = map_tilemap.floor_tile
        wall_tile = map_tilemap.wall_tile # Eventually change to be a 9 way dealio, this is just for testing atm




class TileSet:
    # Parent class for handling tile maps
    def __init__(self, asset_file):
        self.asset_file = pygame.image.load("graphics/Tilemap.png").convert()
class MapTiles(TileSet):
    pass

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
    camera_origin = [playerPos[0] - camera_min[0], playerPos[1] - camera_min[1]] 
    if camera_origin[0] < 0:
        camera_origin[0] = 0
    elif camera_origin[0] > map_dims[0]:
        camera_origin[0] = map_dims[0]
    if camera_origin[1] < 0:
        camera_origin[1] = 0
    elif camera_origin[1] > map_dims[1]:
        camera_origin[1] = map_dims[1]
    map_surface = pygame.Surface((tile_count[0] * graphicsScale, tile_count[1] * graphicsScale))

    # I think this is a slow method, but it's what I have in my head right now. I'll figure something better out eventually.
    tiles_to_write = []
    map_x_count = camera_origin[0]
    while map_x_count < camera_origin[0] + tile_count[0]:
        map_y_count = camera_origin[1]
        while map_y_count < camera_origin[1] + tile_count[1]:
            tileType = map_data[map_x_count, map_y_count].sprite
            if tileType == "map_5": #For now, just do if/else, maybe index tiles in the map data itself? i.e. assign each one a number, then have an array of tile objects to choose from?
                write_tile = floor_tile
            else:
                write_tile = wall_tile
            tiles_to_write.append([write_tile, ((map_x_count - camera_origin[0]) * graphicsScale , (map_y_count - camera_origin[1]) * graphicsScale)]) #this is what I need to fix to make tiles render correctly, I think?
            map_y_count += 1
        map_x_count += 1
    map_surface.blits(tiles_to_write)
    return map_surface #output the surface so it can be drawn to the screen.

def draw_actors(actorList, surf, graphicsScale = 32) -> list:
    # return a list of surfaces with each actor on the screen
    output = []
    for actor in actorList:
        if type(actor) == Player:
            # With player position, check that we're in bounds:
            pass
    surf.blits(output)

def obj_in_view(posx, posy, playerPosX, playerPosY, windowRes, graphicsScale = 32):
    # Tells you if an object is within the rendered area.
    scr_width = windowRes[0] / graphicsScale
    scr_height = windowRes[1] / graphicsScale
    cam_top_left = (playerPosX - scr_width, playerPosY - scr_height)
    