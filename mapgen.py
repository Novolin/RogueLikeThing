#########################
# Map Generation Script #
#########################
from math import floor, ceil
import random
import numpy as np
from mapdata import Tile

class Room:
    def __init__(self, width, height, origin, flags = []):
        self.origin = origin
        self.width = width
        self.height = height
        self.reserved_points = {}
        self.floor_points = []
        self.tile_count = width * height
        self.connected_to_entrance = False
        
        # Now let's actually prepare the room
        if "dungeon_start" in flags: # If it's flagged as the start of the dungeon
            self.reserved_points["in"] = [origin[0], origin[1]]
            print(self.origin)
            self.origin = [origin[0] - floor(width/2), origin[1] - height]
            print(self.origin)
            self.connected_to_entrance = True
        elif "floor_start" in flags: # First room of a floor, but not the dungeon
            self.reserved_points["in"] = origin
            self.connected_to_entrance = True
            self.move_origin_around()
        elif "exit" in flags:
            self.reserved_points["out"] = origin
            self.move_origin_around()
        
        # Append tiles to the room
        CX = 0
        while CX < width:
            CY = 0
            while CY < height:
                self.floor_points.append([CX + origin[0], CY + origin[1]])
                CY += 1
            CX += 1
        for p in self.reserved_points:
            insert_at = self.floor_points.index(self.reserved_points[p])
            self.floor_points[insert_at] = self.reserved_points[p] + [p]


    def get_bordering_points(self, side = False):
        out_list = []
        # Returns a list of tiles that border the room, and what side of the room it is on
        CX = 0
        while CX < self.width:
            out_list.append([self.origin[0] + CX, self.origin[1] - 1, "N"])
            out_list.append([self.origin[0] + CX, self.origin[1] + self.width + 1, "S"])
            CX += 1
        CY = 0
        while CY < self.height:
            out_list.append([self.origin[0] - 1, self.origin[1] + CY, "W"])
            out_list.append([self.origin[0] + 1 + self.width, self.origin[1] + CY, "E"])
            CY += 1
        out_list.append([self.origin[0] - 1, self.origin[1] - 1, "NW"])
        out_list.append([self.origin[0] + self.width + 1, self.origin[1] - 1, "NE"])
        out_list.append([self.origin[0] - 1, self.origin[1] + self.width + 1, "SW"])
        out_list.append([self.origin[0] + self.width + 1, self.origin[1] + self.width + 1, "SE"])
        
        if side: # filter by what side you want
            filter( lambda x: x[2] == side, out_list)

        return out_list

        
    def move_origin_around(self):
        # shifts the room around the origin
        # otherwise stairs would always be in the top left
        x_offset = random.randint(0, self.width)
        y_offset = random.randint(0, self.height)
        if x_offset - self.origin[0] < 0:
            x_offset = self.origin[0] # move it to the side
        if y_offset - self.origin[1] < 0:
            y_offset = self.origin[1] # just shift it to the side.
        self.origin = [self.origin[0] - x_offset, self.origin[1] - y_offset]

class Hall:
    def __init__(self, start, length, direction, doors = 1):
        self.start_point = start
        self.doors = doors
        self.length = length
        self.direction = direction

    def get_hall_doors(self):
        door_coords = []
        if self.doors % 2 == 1:
            door_coords = [self.start_point]
        if self.doors > 0 and self.doors % 2 == 0:
            if self.direction == "+x":
                door_coords.append([self.start_point[0] + self.length, self.start_point[1]])
            elif self.direction == "-x":
                door_coords.append([self.start_point[0] - self.length, self.start_point[1]])
            elif self.direction == "+y":    
                door_coords.append([self.start_point[0], self.start_point[1] + self.length])
            elif self.direction == "-y":
                door_coords.append([self.start_point[0], self.start_point[1] - self.length])
        return door_coords


def is_room_valid(room, map_size, existing_rooms = []):
    # Returns true if the room will fit, returns false if it will not.
    # Start with checking OOB:
    if room.origin[0] + room.width >= map_size[0] - 1:
        return False
    if room.origin[1] + room.height >= map_size[1] -1:
        return False
    for r in existing_rooms:
        for p in r.floor_points:
            if p in room.floor_points:
                return False
    # If it passes those checks:
    return True

def generate_map(width, height, name, origin = False):
    print("Generating Map:", end = "")
    map_dict = {"sizex": width, "sizey":height, "name":name}
    density_goal = ceil(width * height / 4)
    room_list = []
    new_room = False
    
    if not origin:
        new_room = Room(3,3,[floor(width / 2), floor(height/2)], "dungeon_start")
    else:
        new_room = Room(random.randint(1, 8), random.randint(1, 8), origin, "floor_start")
        while not is_room_valid(new_room, (width, height), room_list):
            new_room = Room(random.randint(1, 8), random.randint(1, 8), origin, "floor_start")
    room_list.append(new_room)
    density = new_room.tile_count
    # Find where to put the exit.
    while True:
        next_width = random.randint(1,8)
        next_height = random.randint(1,8)
        next_origin = [random.randint(1, width - next_width), random.randint(1, height - next_height)]
        next_room = Room(next_width, next_height, next_origin, "E")
        if is_room_valid(next_room, (width, height), room_list):
            room_list.append(next_room)
            density += next_width * next_height
            print(".", end = "")
            make_exit_room = False
            break
    # Place the rest of the rooms:
    while density < density_goal:
        while True: 
            next_width = random.randint(1,8)
            next_height = random.randint(1,8)
            next_origin = [random.randint(1, width - next_width), random.randint(1, height - next_height)]
            next_room = Room(next_width, next_height, next_origin)
            if is_room_valid(next_room, (width, height), room_list): #make sure it's valid
                density += next_width * next_height
                room_list.append(next_room)
                print(".", end = "")
                break
    # Calculate the hallways:
    hall_count = 1
    print("\nFinding Hallways:", end = "")
    print(len(room_list))
    halls = []
    while hall_count < len(room_list):
        print(".", end = "")
        halls.append(get_hall_points(room_list[hall_count - 1], room_list[hall_count]))
        hall_count += 1

    # place these items in a dictionary:
        
    return map_dict
    