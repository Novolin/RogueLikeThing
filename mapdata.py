##############################################
#  Python Roguelike Map Data and Generation  #
#  WHERE THE FUCK AM I? HOW DID I GET HERE?  #
##############################################
import random
import numpy as np
import json 

class Tile:
    '''Parent class for a map tile.'''
    def __init__(self, tile_type, actors, contents):
        self.tile_type = tile_type # Floor, what kind of wall, etc.
        self.actors = actors # Who is living here
        self.contents = contents # What does it have in its pockets
        self.visible = True # Can the player see it
        self.revealed = True # Has the player discovered it
    def get_tile_contents(self) -> bool:
        # Returns a list of tile contents and actors.
        content_list = {}
        content_list["actors"] = self.actors
        content_list["objects"] = self.contents
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

class Floor(Tile):
    '''A floor tile!'''
    def __init__(self, actors = [], contents = []):
        super().__init__("floor", actors, contents)
        # add stuff you might need with a floor, like interactions, traps, etc.

class Wall(Tile):
    '''A wall tile!'''
    def __init__(self, actors = [], contents = False):
        super().__init__("wall", actors, contents)
    
        # We'll figure out interactions at some point, maybe even checking for what kind of neighbors it has
        # then we can render corners and stuff
class Stair(Tile):
    def __init(self, direction, actors = [], contents = False):
        super().__init__("floor", actors, contents) #for now, play like its just a regular floor
        self.direction = direction
class DungeonLevel:
    '''parent class for a dungeon floor, which we can use for basically everything'''
    def __init__(self, levelName, floorType, tileset, origin):
        self.levelName = levelName # what are we calling this floor
        self.floorType = floorType # Is there anything we need to do with it?
        self.map = np.full([64,64], Wall()) # Create a 64x64 grid, filled with walls
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
        if not origin:
            origin = [floor(size[0]/2), size[1]] # Place at bottom center for any new floor
        # generate our first room based on the 

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

def save_map_as_file( map, ftype = "text" , location = "debug\mapfile.txt"):
    # outputs the map as a file
    
    if ftype == "text":
        with open(location) as outFile:
            outFile.write("pee")
    return True

## Debug block:
if __name__ == "__main__":
    test = DungeonLevel(0,0)
    test.generate_rand_layout()
    rendx = 0
    outstr = ""
    while rendx < 64:
        rendy = 0
        while rendy < 64:
            if type(test.map[rendx, rendy]) is Wall:
                print("#", end="")
                outstr += "#"
            else: 
                print(".", end="")
                outstr += "."
            rendy += 1
        print("")
        outstr += "\n"
        rendx += 1
    with open("out.txt", "w") as output:
        output.write(outstr)