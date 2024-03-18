##############################################
#  Python Roguelike Map Data and Generation  #
#  WHERE THE FUCK AM I? HOW DID I GET HERE?  #
##############################################

import numpy as np
import json 

# Other scripts:
import actors

class Tile:
    '''Parent class for a map tile.'''
    def __init__(self, tile_type):
        self.tile_type = tile_type # Floor, what kind of wall, etc.
        self.visible = True # Can the player see it
        self.revealed = True # Has the player discovered it

    def activate_tile(self):
        if self.tile_type == "stairup":
            # go up
            pass
        

class DungeonLevel:
    '''parent class for a dungeon floor, which we can use for basically everything'''
    def __init__(self, load_from = False, origin = False):
        self.actors = []
        self.items = []
        if load_from: # If it's coming from a file
            self.file_loc = load_from
            map_data = self.get_from_file(load_from)
        else: # If we're generating a fresh level
            map_data = self.get_new_map(origin) #TODO: MAKE IT WORK
        self.map = map_data[0]
        self.actors = map_data[1]
        self.items = map_data[2]
        self.tileset = map_data[3]
        self.name = map_data[4]

    def get_new_map(self, origin):
        pass # Use the mapgen code when it works
    def get_from_file(self, map_file):
        with open(map_file) as map_json:
            place_data = json.load(map_json)
            tile_set = place_data["tileset"]
            name = place_data["name"]
            #Make a 2d array of walls
            loaded_map = np.full((place_data["sizex"], place_data["sizey"]), Tile("wall"))
            map_objects = []
            map_actors = []
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
            for door in place_data["doors"]:
                map_actors.append(actors.Door(place_data["doors"][door]["x"], place_data["doors"][door]["y"], place_data["doors"][door]["state"]))
            for actor in place_data["actors"]:
                map_actors.append(actors.Player(place_data["actors"][actor]["x"],[place_data["actors"][actor]["y"]]))
            return (loaded_map, map_actors, map_objects, tile_set, name)

class Dungeon:
    def __init__(self, depth):
        self.depth = depth
        self.floors = []

    def load_floor_data(self):
        # Placeholder: Will be used to load saved map data
        pass

class Town:
    def __init__(self):
        pass
