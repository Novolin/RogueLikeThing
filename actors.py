###########################
# Python Roguelike Actors #
# All The World's A Stage #
###########################
'''
This is where all the actor types will live!

The actual enemy data will likely live in a json or csv or something funky.
'''

import graphics
import pygame

class GameActor:
    '''This is a parent class for all Actors'''

    def __init__(self, posx, posy, name, static):
        self.posx = posx #we're going to use the location to check tiles for movement/etc. 
        self.posy = posy
        self.name = name
        self.static = static
        self.sprite_id = False #int to find id
        self.visible = True
        self.solid = True # Assume nothing can pass

    def get_actor_sprite(self, graphicsScale = 32):
        sprite_sheet = pygame.image.load("Graphics/Tilemap.png").convert()
        actor_sprite = sprite_sheet.subsurface(0, graphicsScale * self.sprite_id, graphicsScale, graphicsScale)
        return actor_sprite

    def move_actor(self, distance, vertical = False):
        if vertical:
            self.posy += distance
        else:
            self.posx += distance

    def attack(self, targetx, targety):
        pass #tbd

    def get_visible(self, camera_origin, camera_size):
        if self.visible:
            camera_bounds = [camera_origin[0], camera_origin[0] + camera_size[0], camera_origin[1], camera_origin[1] + camera_size[1]]
            if camera_bounds[0] <= self.posx <= camera_bounds[1]:
                # X good, check Y
                if camera_bounds[2] <= self.posy <= camera_bounds[3]:
                    view_relative_pos = [self.posx - camera_origin[0], self.posy - camera_origin[1]]
                    return view_relative_pos
        return False #if it falls through the cracks, say no.
class Player(GameActor):
    '''The Player, The Main Character, You!'''
    def __init__(self, posx, posy):
        # We won't use this for loading the player data directly.
        super().__init__(posx, posy, "Player", False)

    def get_player_data(self, useSave):
        if useSave:
            try:
                playerData = open("save/playerData.json", "r")
                # Assign saved attributes/etc. to player object
                return True
            except:
                return False # Use False for a load error
        else:
            # We're making new player data, so run whatever character creator
            # for now, just use a set of default values:
            super().__init__(0,0,"Player", False)
            self.hp = 100
            self.mp = 100
            self.inventory = []
            self.equipment = {}
            self.level = 1
            self.xp = 0
            self.sprite_id = 2 # The ID for the sprite to use, for indexing on the sprite list.

class Enemy(GameActor):
    # the stuff
    pass
                

        