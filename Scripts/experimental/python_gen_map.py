# This script is to create some image-based map layouts because i am fighting gdscript a little bit
# nothing against it, I'm just more familiar with python so I'll port this once it works

from PIL import Image
import numpy as np 
from random import randint, choice
# define colour names
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
grey = (128,128,128)


class Level:
    def __init__(self, entry_x, entry_y, size = [64,64]):
        self.size = size
        self.entry = [entry_x, entry_y]
        self.map = np.full(size, (0,0,0)) # give a black void
        self.door_locs = [] # so we can see them
        self.stair_locs = [self.entry] # basically two lists of reserved squares
        self.points = []
        self.rooms = [] # list of rooms, so we can check their locations
        entry_room_origin = [randint(0,-4) + self.entry[0], randint(0,-4) + self.entry[1]]
        entry_room_size = [randint(0,6), randint(0,6)]
        self.rooms.append(Room(entry_room_origin, entry_room_size, 0))
        points = get_points_of_interest(self.size, 23)
        # iterate over our points of interest, and do a double check to make sure it's not overwriting the stairs up.
        for i in points:
            if i not in self.points:
                self.points.append(i)
        
    def output_file(self, file_name):
        out_img = Image.fromArray(self.map, mode = "RGB")
        out_img.save(file_name + ".png")
        return

    def populate_map(self):
        # broken from init so we can change the layout using the same given points
        # Why? idk, errors? 
        # Iterate over the points of interest
        current_point = 0
        while current_point < len(self.points) - 2: # end one loop early because otherwise it will freak out with list length
            # Put the room tiles on the map
            room_tiles = self.rooms[current_point].get_room_tiles()
            for t in room_tiles: 
                self.map[t[0]][t[1]] = grey 
            
            # Draw a path to the next room
            hall_origin = self.points[current_point]
            target = self.points[current_point + 1]
            target_direction = [0,0]
            start_choices = []
            if target[0] > hall_origin[0]:
                target_direction[0] = 1
            elif target[0] < hall_origin[0]:
                target_direction = -1
            if target[1] > hall_origin[1]:
                target_direction[1] = 1
            elif target[1] < hall_origin[1]:
                target_direction[1] = -1

            

            
            
            
            
            
            
            current_point += 1
            
    



    


class Room:
    def __init__(self, origin, size):
        self.origin = origin
        self.size = size

    def get_room_tiles(self):
        output = []
        for i in range(self.size[0]):
            for n in range(self.size[1]):
                out_p = [self.origin[0] + i, self.origin[1] + n]
                if out_p not in output: # sanity check in case it somehow duplicates
                    output.append(out_p)
        return output
    def get_border_tiles(self, directions):
        border_tiles = []
        if directions[0] == 1:
            pass # add tiles
        elif directions[0] == -1:
            pass # add tiles

                
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
        
        


        


def get_points_of_interest(size, number = 24):
        out_list = []
        while len(out_list) < number:
            check_point = [randint(1,size[0]- 1), randint(1,size[1] - 1)]
            if check_point not in out_list:
                out_list.append(check_point)
        return out_list