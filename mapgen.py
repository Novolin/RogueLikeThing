import numpy as np
import mapdata
from math import random
class RectRoom:
    '''A class for defining a rectangular room'''
    def __init__(self, height, width, pos):
        self.height = height
        self.width = width
        self.pos = pos #top left corner position
        # Where any special objects are, like stairs or special enemies or whatever.
        self.special_locations = {}
        # Set somewhere for the hall algo to target
        self.hallTarget = (random.randint(1, width - 1), random.randint(1, height - 1))
    def place_asset(self, asset, pos):
        self.special_locations[asset] = pos 
    def get_room_tiles(self):
        '''return a 2d array of tiles which are in the room'''
        out_arr = []
        wcount = 0
        while wcount < self.width:
            hcount = 0
            harray = [] #temp array to store the horizontal tiles
            while hcount < self.height:
                harray.append(mapdata.Floor())
            out_arr[wcount] = harray
        ## THIS IS WHERE PLACING OBJECTS WOULD LIVE ##
        return out_arr

class RoundRoom:
    def __init__(self, radius, pos):
        self.pos = pos # center of circle 
        self.radius = radius
        self.special_locations = {}

    def place_asset(self, asset, pos):
        self.special_locations[asset] = pos

def generate_full_map(size):
    '''Generates a map which will fit the given space'''
    map_output = np.full(size, mapdata.Wall()) #start with all walls

    return map_output 
def make_round_room(radius):
    output_rooms = np.full((radius*2, radius*2))
