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



