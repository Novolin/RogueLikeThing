# This script is to create some image-based map layouts because im borde

import PIL
import numpy as np 
from random import randint
# define colour names
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
grey = (128,128,128)


class Level:
    def __init__(self, entry_x, entry_y, file_out, size = [64,64]):
        self.entry = [entry_x, entry_y]
        self.map = np.full(size, (0,0,0))
        self.map[entry_x][entry_y] = green # place the up stair
        self.door_locs = [] # so we can see them
        self.stair_locs = [self.entry] # basically two lists of reserved squares
        self.points = []
        entry_room_offset = [randint(0,-4), randint(0,-4)]
        self.rooms = [] # list of rooms, so we can check their locations

        #im sleepy now so idk what to do


    def get_points_of_interest(self, number = 24):
        pass


class Room:
    def __init__(self, origin, size):
        self.origin = origin
        self.size = size
        self.border_tiles = []
        # top/bottom
        for i in range(self.size[0]):
            self.border_tiles.append([origin[0] + i, origin[1] - 1])
            self.border_tiles.append([origin[0] + i, origin[1] + size[1] + 1])
        for i in range(self.size[1]):
            self.border_tiles.append([origin[0] - 1, origin[1] + i])
            self.border_tiles.append([origin[0] + size[0] + 1, origin[1] + i])

class Hall:
    def __init__(self, origin, target):
        self.origin = origin
        self.target = target
        

            