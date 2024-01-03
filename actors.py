###########################
# Python Roguelike Actors #
# All The World's A Stage #
###########################
'''
This is where all the actor types will live!

The actual enemy data will likely live in a json or csv or something funky.
'''



class GameActor:
    '''This is a parent class for all Actors'''

    def __init__(self, posx, posy, name, static):
        self.posx = posx #we're going to use the location to check tiles for movement/etc. 
        self.posy = posy
        self.name = name
        self.static = static
    def attack(self, targetx, targety):
        pass #tbd


class Player(GameActor):
    '''The Player, The Main Character, You!'''
    def __init__(self):
        # We won't use this for loading the player data directly.
        pass

    def get_player_data(self, useSave):
        if useSave:
            try:
                playerData = open("save/playerData.json", "r")
                # Assign saved attributes/etc. to player object
                return True
            except:
                return False # Use False for a load error
        else:
            # We're making new player data, so run whatever character creator
            # for now, just use a set of default values:
            super.__init__(0,0,"Player", False)
            self.hp = 100
            self.mp = 100
            self.inventory = []
            self.equipment = {}
            self.level = 1
            self.xp = 0
            self.sprite = False # Load the sprite here, as image data, so it can be used by pygame rendering
                

        