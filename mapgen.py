#########################
# Map Generation Script #
#########################
from math import floor, ceil
import random
import numpy as np
from mapdata import Floor, Wall, Stair

class Room:
    def __init__(self, size, origin):
        self.width = random.randint(size, size * 2)
        self.height = random.randint(size, size * 2)
        self.origin = origin
        self.shape = "rect"
        self.floor_points = self.get_room_points()

    def get_room_points(self):
        output = []
        w = 0
        while w < self.width:
            h = 0
            while h < self.height:
                output.append((self.origin + w, self.origin + h))
                h += 1
            w += 1
        return output

class RoundRoom(Room):
    def __init__(self, size, origin):
        self.radius = random.randint(size, size * 2)
        self.width = self.radius # it lives in a square box
        self.height = self.radius # do both in case we use them for checking for oob
        self.center = self.width / 2 # this can be a float, since we don't directly reference it
        self.origin = [origin[0] - floor(self.center), origin[1] - floor(self.center)]
        self.shape = "circ"
        self.floor_points = self.get_room_points()

    def get_room_points(self):
        output = []
        w = 0
        while w < self.width:
            h = 0
            while h < self.height:
                # Check if it's within the radius of the circle
                dist_chk = (w - self.center)**2 + (h-self.center)**2
                if dist_chk < self.radius ** 2:
                    output.append((self.origin + w, self.origin + h))
                h += 1
            w += 1
        return output

def generate_map(width, height, origin = False):
    # Returns a Numpy array which can be plopped into the DungeonLevel map attribute
    output = np.full([width, height], Wall())
    total_floor = 0
    density_goal = floor((width * height) / 3) #aim for 33% floor, by volume
    if not origin: #Place the entry at the bottom center
        origin = (width // 2, height - 2)
    next_room = RoundRoom(3, origin) # force a round stairwell room for now

    while total_floor <= density_goal:
        total_floor += len(next_room.floor_points) # Add our last room to the floor counter
        for tile in next_room.floor_points: # Stick the floor tiles into the map
            output[tile] = Floor()
        next_target = [random.randint(1, output.shape[0] - 1), random.randint(1, output.shape[1] - 1)]
        # check if the target point is inside another room or hallway:
        while type(output[next_target]) == Floor:
            print("Already a floor tile, retrying...")
            next_target = [random.randint(1, output.shape[0] - 1), random.randint(1, output.shape[1] - 1)]
        last_room = next_room
        if next_target[0] % 2 == 1 and last_room.shape == "rect": # make circular rooms less common
            next_room = RoundRoom(2, next_target)
        else:
            next_room = Room(3, next_target)
        hall_tiles = calculate_hall(random.choice(last_room.floor_points), random.choice(next_room.floor_points))
        
    


def calculate_hall(start, end):
    # returns a list of tiles which will form a hallway.
    output = []
    hor_len = end[0] - start[0]
    ver_len = end[1] - start[1]
    turns = random.randint(0,3) # Let the hall get a lil twisty

    

    



