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
        if type(target) == list:
            self.target_point = True
        else:
            self.target_point = False
        self.target = target # What the camera is focused on, usually the player.
        self.viewport_resolution = cam_res # What is the size of the camera space (in case we do multi window/ui stuff?)
        self.viewport_grid_size = [ceil(cam_res[0] / scale), ceil(cam_res[1] / scale)] #how many grid tiles will it display
        self.scale = scale # How many pixels per tile
        self.update_cam_origin()
        self.cam_surface = pygame.Surface(cam_res)

    def render_map_data(self, map_data, map_tilemap):
        floor_tile = map_tilemap.floor_tile
        wall_tile = map_tilemap.wall_tile # Eventually change to be a 9 way dealio, this is just for testing atm
        
        # Update the camera origin, and ensure that it doesn't go out of bounds
        self.update_cam_origin()
        if self.origin[0] + self.viewport_grid_size[0] > map_data.shape[0]: # We need map data to do these checks
            self.origin[0] = map_data.shape[0] - self.viewport_grid_size[0]
        if self.origin[1] + self.viewport_grid_size[1] > map_data.shape[1]:
            self.origin[1] = map_data.shape[1] - self.viewport_grid_size[1]
        tiles_to_write = []
        map_x_count = self.origin[0]
        while map_x_count < self.origin[0] + self.viewport_grid_size[0]:
            map_y_count = self.origin[1]
            while map_y_count < self.origin[1] + self.viewport_grid_size[1]:
                tile = map_data[map_x_count, map_y_count]
                if tile.tile_type == "floor": 
                    write_tile = map_tilemap.floor_tile # write something in tilemap that will return the correct subtile
                elif len(tile.actors) > 0 and tile.actors[0] == "door":
                    write_tile = map_tilemap.door_tile
                else:
                    write_tile = map_tilemap.wall_tile
                tiles_to_write.append([write_tile, ((map_x_count - self.origin[0]) * self.scale , (map_y_count - self.origin[1]) * self.scale)])
                map_y_count += 1
            map_x_count += 1
        self.cam_surface.blits(tiles_to_write)
        return

    def update_cam_origin(self):
        if self.target_point:
            self.origin = [self.target[0] - floor(self.viewport_grid_size[0]/2), self.target[1] - floor(self.viewport_grid_size[1]/2)]
        else:
            self.origin = [self.target.posx - floor(self.viewport_grid_size[0]/2), self.target.posy - floor(self.viewport_grid_size[1]/2)]
        if self.origin[0] < 0:
            self.origin[0] = 0
        if self.origin[1] < 0:
            self.origin[1] = 0
        return 

    def draw_actors_in_view(self, actor_list):
        for actor in actor_list:
            act_rel_pos = actor.get_visible(self.origin, self.viewport_grid_size)
            if act_rel_pos:
                self.cam_surface.blit(actor.get_actor_sprite(), (act_rel_pos[0] * self.scale, act_rel_pos[1] * self.scale))

    def refresh_screen(self, map_obj, actors):
        self.update_cam_origin()
        self.cam_surface.fill("white")
        self.render_map_data(map_obj.map, map_obj.tileset)
        self.draw_actors_in_view(actors)

class TileSet:
    # Parent class for handling tile maps
    def __init__(self, asset_file, grid = 32):
        self.asset_file = asset_file
        self.tile_surface = pygame.image.load(asset_file).convert()
class MapTiles(TileSet):
    def __init__(self, asset_file = "data/Tilemap.png", grid = 32):
        super().__init__(asset_file, grid)
        self.floor_tile = self.tile_surface.subsurface(0,0,grid,grid)
        self.wall_tile = self.tile_surface.subsurface(0,grid, grid, grid) #Figure out a 9 way system
        self.door_tile = self.tile_surface.subsurface(0,grid * 3, grid, grid)

 # Edit this if you want to change how many pixels per tile

