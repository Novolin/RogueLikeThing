########################
#   PYTHON ROGUELIKE   #
#     I TRY AGAIN      #
#     VERSION 0.0a     #
########################

'''
This file contains game logic and related data
It is the base script for the game itself, and will call other scripts as needed.

'''


'''
This file contains game logic and related data
It is the base script for the game itself, and will call other scripts as needed.

'''


import pygame
import numpy as np 

# Import subscripts:

import graphics
from actors import Player #just import the player actor for now, we can do the other stuff at a later point.
import mapdata

actorList = [False]

DEBUG_plr_loc = [0,0] # !! DEBUG !!: x/y coords for the camera to follow.
actorList = []

DEBUG_plr_loc = [0,0] # !! DEBUG !!: x/y coords for the camera to follow.

# !! Main game loop !!
def main():
    # Pygame Setup:
    pygame.init()
    screen = pygame.display.set_mode((1024,768))
    clock = pygame.time.Clock()
    running = True
    # Init game state:
    gamestate = 0 # Default game state, turn-based map stuff.
    currentMap = mapdata.DungeonLevel(0,0) # this will need a replacement eventually
    turnProcess = 0 #where are we in the "initiative"

    # Init graphics data:
    

    #temp: figure out a nicer way to do this when things are hectic
    actorList[0] = Player(0,0)
    # Fire the loop!

    while running:
        # !! Check for events !!
        for event in pygame.event.get():
            # If the window is closed, kill the script.
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    try:
                        graphics.debug_draw_scr_data(currentMap.map, tilemap, DEBUG_plr_loc)

                    except:
                        print("Map Generation Error, Retrying...")
                        pass
                    screen_need_refresh = True
                elif event.key == pygame.K_1:
                    screen.fill("pink")
                elif event.key == pygame.K_UP:
                    if not actorList[0].posy == 0:
                        actorList[0].move_actor(-1, True)
                elif event.key == pygame.K_DOWN:
                    if not actorList[0].posy == currentMap.map.shape[1]:
                        actorList[0].move_actor(1, True)
                elif event.key == pygame.K_LEFT:
                    if not actorList[0].posx == 0:
                        actorList[0].move_actor(-1, False)
                elif event.key == pygame.K_RIGHT:
                    if not actorList[0].posx == currentMap.map.shape[0]:
                        actorList[0].move_actor(1, False)
        # !! Tick game logic here !!

        # !! Handle graphics processing here !!
        #todo: differentiate between menus/game/etc. 
        screen.blit(graphics.render_map_data(currentMap.map, tilemap, (actorList[0].posx, actorList[0].posy)), (0,0))
        graphics.draw_actors(actorList, screen)
        # Draw the changes to the display
        pygame.display.flip()

        # Set a 60 fps refresh rate cap
        clock.tick(60) 

def spawn_player(map, player = False):
    '''Place the player on the map, in map mode'''
    if not player: #if no player is present, aka, we're spawning one for the first time.
        pass
#Run the main loop if we run this file directly
if __name__ == "__main__":
    main()