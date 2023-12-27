##############################################
#  Python Roguelike Map Data and Generation  #
#  WHERE THE FUCK AM I? HOW DID I GET HERE?  #
##############################################
import random
import numpy as np
import json 

class Tile:
    '''Parent class for a map tile.'''
    def __init__(self, clip, actors, contents, sprite):
        self.clip = clip # Can you walk on it?
        self.actors = actors # Who is living here
        self.contents = contents # What does it have in its pockets
        self.sprite = sprite # what sprite should be displayed for it.
        # Add something for the sprite data here?

class Floor(Tile):
    '''A floor tile!'''
    def __init__(self):
        super().__init__(False, [], [], "floor")
        # Later, we can add some stuff to do with interacting with floors
        # also setting up floor traps, etc.

class Wall(Tile):
    '''A wall tile!'''
    def __init__(self):
        super().__init__(True, [], [], "wall")
        # We'll figure out interactions at some point, maybe even checking for what kind of neighbors it has
        # then we can render corners and stuff


class DungeonLevel:
    '''parent class for a dungeon floor, which we can use for basically everything'''
    def __init__(self, levelName, floorType):
        self.levelName = levelName # what are we calling this floor
        self.floorType = floorType # Is there anything we need to do with it?
        self.map = np.full([64,64], Wall()) # Create a 64x64 grid, filled with walls

    def generate_rand_layout(self, count = 5):
        '''Generate a random set of rooms'''
        # For now, just generate square rooms, maybe we can figure out how to do circles and other wild shapes later
        # Set  how big/small rooms can be.
        maxX = 9
        maxY = 9
        minX = 3
        minY = 3
        levelRange = self.map.shape

        output = []
        # List of rooms to write, structured as objects

        while len(output) < count:
            # Choose how big, where:
            isRoomOk = True # is our generated room ok to add to the list
            # Data Structured as: [Origin X, Origin Y, Size X, Size Y]
            newRoomData = [random.randint(0, levelRange[1]), random.randint(0, levelRange[0]), random.randint(minX, maxX), random.randint(minY, maxY)]
            # Now check for conflicts
            for existing in output:
                checkBounds = (existing[0] - 1, existing[1] - 1, existing[0] + existing[2] + 1, existing[0] + existing[3] + 1)
                checkY = False #Should we check the y axis?
                # Check for an X overlap:
                if newRoomData[0] <= checkBounds[2]: 
                    #origin is to the left of the right boundary, overlap is possible
                    if newRoomData[0] + newRoomData[2] >= checkBounds[2]:
                        # the right side is not to the left of the origin, overlap still possible, look for y conflicts
                        checkY = True
                elif newRoomData[0] + newRoomData[2] <= checkBounds[0]:
                    #right edge is past the origin, we may have a conflict
                    pass




        

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

