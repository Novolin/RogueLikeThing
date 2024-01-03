###########################################
#   Python Roguelike Graphics Processing  #
# Separated to keep the main code cleaner #
###########################################

import pygame #i swear if you give me a redundant import error i will shit my pants

graphicsScale = 16 # Edit this if you want to change how many pixels per tile
def render_map_data(map):
    tileMap = pygame.image.load("graphics/Tilemap.png")
    # look at the map data, see what needs to be rendered.
    

