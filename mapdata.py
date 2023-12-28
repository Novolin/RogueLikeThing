##############################################
#  Python Roguelike Map Data and Generation  #
#  WHERE THE FUCK AM I? HOW DID I GET HERE?  #
##############################################
import random
import numpy as np
import json 

class Tile:
    '''Parent class for a map tile.'''
    def __init__(self, clip, actors, contents):
        self.clip = clip # Can you walk on it?
        self.actors = actors # Who is living here
        self.contents = contents # What does it have in its pockets
        self.sprite = [] # what sprite should be displayed for it.
        self.visible = True # Can the player see it
        self.revealed = True # Has the player discovered it

class Floor(Tile):
    '''A floor tile!'''
    def __init__(self):
        super().__init__(False, [], [])
        self.sprite = ["floor"] #placeholder, give an actual sprite name
        # Later, we can add some stuff to do with interacting with floors
        # also setting up floor traps, etc.

class Wall(Tile):
    '''A wall tile!'''
    def __init__(self):
        super().__init__(True, [], [])
        self.sprite = ["wall"]
        # We'll figure out interactions at some point, maybe even checking for what kind of neighbors it has
        # then we can render corners and stuff


class DungeonLevel:
    '''parent class for a dungeon floor, which we can use for basically everything'''
    def __init__(self, levelName, floorType):
        self.levelName = levelName # what are we calling this floor
        self.floorType = floorType # Is there anything we need to do with it?
        self.map = np.full([64,64], Wall()) # Create a 64x64 grid, filled with walls

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