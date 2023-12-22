##############################################
#  Python Roguelike Map Data and Generation  #
#  WHERE THE FUCK AM I? HOW DID I GET HERE?  #
##############################################

import numpy as np
import json 

class Tile:
    '''Parent class for a map tile.'''
    def __init__(self, clip, actors, contents, tileType):
        self.clip = clip # Can you walk on it?
        self.actors = actors # Who is living here
        self.contents = contents # What does it have in its pockets
        self.tileType = tileType # is it a wall/floor/etc.
class Floor:
    '''parent class for a dungeon floor, which we can use for basically everything'''
    def __init__(self, levelName, floorType):
        self.levelName = levelName # what are we calling this floor
        self.floorType = floorType # Is there anything we need to do with it?
        self.map = np.empty([64,64]) # Create a 64x64 grid

    def generate_rand_layout(self, sizex, sizey):
        '''Generate a random set of rooms'''
        pass

class Dungeon:
    def __init__(self, depth):
        self.depth = depth

    def load_data(self):
        # Placeholder: Will be used to load saved map data
        pass

class Town:
    def __init__(self):
        pass