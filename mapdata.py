##############################################
#  Python Roguelike Map Data and Generation  #
#  WHERE THE FUCK AM I? HOW DID I GET HERE?  #
##############################################
import random
import numpy as np
import json 

class Tile:
    '''Parent class for a map tile.'''
    def __init__(self, tile_type):
        self.tile_type = tile_type # Floor, what kind of wall, etc.
        self.actors = [] # Who is living here
        self.contents = [] # What does it have in its pockets
        self.visible = True # Can the player see it
        self.revealed = True # Has the player discovered it
    def get_tile_contents(self):
        # Returns a list of tile contents and actors.
        content_list = {}
        content_list["actors"] = self.actors
        content_list["objects"] = self.contents
        return content_list
    def can_actor_enter(self):
        if self.tile_type == "wall":
            return False
        if len(self.actors) > 0:
            for actor in self.actors: 
                if actor.solid:
                    return False
        return True
    def activate_tile(self):
        return False
    def add_actor(self, actor):
        # Check if an actor can go in the tile, return true if successful.
        self.actors.append(actor)
        return True

class DungeonLevel:
    '''parent class for a dungeon floor, which we can use for basically everything'''
    def __init__(self, levelName, floorType, tileset, origin):
        self.levelName = levelName # what are we calling this floor
        self.floorType = floorType # Is there anything we need to do with it?
        self.map = np.full([64,64], Tile("wall")) # Create a 64x64 grid, filled with walls
        self.tileset = tileset # What tile set should we use to display the map
        self.entry_point = origin # Where should the entrance be?
        self.active = True # Is this the map that we are currently using

    def generate_rand_layout(self, count = 8):
        '''Generate a random set of rooms'''
        # For now, just generate square rooms, maybe we can figure out how to do circles and other wild shapes later
        # Set  how big/small rooms can be.
        counter = count
        maxX = 9
        maxY = 9
        minX = 4
        minY = 4
        roomList = []
        levelRange = self.map.shape
        retry = 5 # If we can't place a room, how many tries before we give up
        while counter > 0:
            # Choose how big, where:
            # Data Structured as: [Origin X, Origin Y, Size X, Size Y]
            newRoomData = [random.randint(1, levelRange[1]), random.randint(1, levelRange[0]), random.randint(minX, maxX), random.randint(minY, maxY)]
            # Don't place our room out of bounds:
            while newRoomData[0] + newRoomData[2] > 63 or newRoomData[1] + newRoomData[3] > 63:
                newRoomData = [random.randint(1, levelRange[1]), random.randint(1, levelRange[0]), random.randint(minX, maxX), random.randint(minY, maxY)]

            # Now check for conflicts
            roomValid = True
            checkX = newRoomData[0] - 1
            checkY = newRoomData[1] - 1
            while checkX <= newRoomData[0] + newRoomData[2] + 1 and roomValid:
                while checkY <= newRoomData[1] + newRoomData[3] + 1 and roomValid:
                    if type(self.map[checkX, checkY]) is Floor:
                        retry = retry - 1 #decrement retry counter
                        roomValid = False
                    checkY += 1
                checkX += 1
            if roomValid or retry < 1:
                #If the room passes our check, or we're out of tries, place it on the map
                # add it to the room list as well, so we can make hallways, too.
                roomList.append(newRoomData)
                placeX = newRoomData[0]
                placeY = newRoomData[1]
                while placeX <= newRoomData[0] + newRoomData[2]:
                    while placeY <= newRoomData[1] + newRoomData[3]:
                        self.map[placeX, placeY] = Floor()
                        placeY += 1
                    placeX += 1
                    placeY = newRoomData[1]
                retry = 5 # Reset the retry counter
                counter = counter - 1 # decrement the counter
    def generate_map(self, size, origin = False):
        pass # call from mapgen?

class Dungeon:
    def __init__(self, depth):
        self.depth = depth
        self.floors = []

    def load_data(self):
        # Placeholder: Will be used to load saved map data
        pass

class Town:
    def __init__(self):
        pass

def save_map_as_file(map, ftype = "text" , location = "debug\mapfile.txt"):
    # outputs the map as a file
    
    if ftype == "text":
        with open(location) as outFile:
            outFile.write("pee")
    return True

def load_map_from_file(filename):
    #Open the file and load into a dict
    with open(filename) as map_json:
        place_data = json.load(map_json)
        #Make a 2d array of walls
        loaded_map = np.full((place_data["sizex"], place_data["sizey"]), Tile("wall"))
        # Place rooms:
        for room in place_data["rooms"]:
            countx = place_data["rooms"][room]["origin"]["x"]
            while countx < place_data["rooms"][room]["origin"]["x"] + place_data["rooms"][room]["width"]:
                county = place_data["rooms"][room]["origin"]["y"]
                while county < place_data["rooms"][room]["origin"]["y"] +place_data["rooms"][room]["height"]:
                    loaded_map[countx][county] = Tile("floor")
                    county += 1
                countx += 1
        # Place halls
        for hall in place_data["halls"]:
            # Find the direction it's going:
            hcount = 0
            if place_data["halls"][hall]["direction"] == "-x":
                while hcount < place_data["halls"][hall]["length"]:
                    loaded_map[place_data["halls"][hall]["start"]["x"] - hcount][place_data["halls"][hall]["start"]["y"]] = Tile("floor")
                    hcount += 1
            elif place_data["halls"][hall]["direction"] == "+x":
                while hcount < place_data["halls"][hall]["length"]:
                    loaded_map[place_data["halls"][hall]["start"]["x"] + hcount][place_data["halls"][hall]["start"]["y"]] = Tile("floor")
                    hcount += 1
            elif place_data["halls"][hall]["direction"] == "-y":
                while hcount < place_data["halls"][hall]["length"]:
                    loaded_map[place_data["halls"][hall]["start"]["x"]][place_data["halls"][hall]["start"]["y"] - hcount] = Tile("floor")
                    hcount += 1
            elif place_data["halls"][hall]["direction"] == "+y":
                while hcount < place_data["halls"][hall]["length"]:
                    loaded_map[place_data["halls"][hall]["start"]["x"]][place_data["halls"][hall]["start"]["y"] + hcount] = Tile("floor")
                    hcount += 1
        # Place Stairs
        for stair in place_data["stairs"]:
            loaded_map[place_data["stairs"][stair]["x"]][place_data["stairs"][stair]["y"]] = Tile("stair"+stair)
        # Doors and other actors #
        #NOTE: you need to make this pass a separate list, 
        for door in place_data["doors"]:
            loaded_map[place_data["doors"][door]["x"]][place_data["doors"][door]["y"]].add_actor(place_data["doors"][door]["state"]) #temp, since we don't have a door actor yet.
        for actor in place_data["actors"]:
            loaded_map[place_data["actors"][actor]["x"]][place_data["actors"][actor]["y"]].add_actor(actor)
        return loaded_map