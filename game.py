##########################
#     PYTHON ROGUELIKE   #
#      I TRY AGAIN       #
# WHO CARES WHAT VERSION #
##########################

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
    currentMap = mapdata.DungeonLevel(0,0)
    turnProcess = 0 #where are we in the "initiative"

    # Init graphics data:
    tilemap = pygame.image.load("graphics/Tilemap.png").convert()
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
                    currentMap.generate_rand_layout()
                elif event.key == pygame.K_UP:
                    DEBUG_plr_loc[1] -= 1
                    print(DEBUG_plr_loc)
                elif event.key == pygame.K_DOWN:
                    DEBUG_plr_loc[1] += 1
                    print(DEBUG_plr_loc)
                elif event.key == pygame.K_LEFT:
                    DEBUG_plr_loc[0] -= 1
                    print(DEBUG_plr_loc)
                elif event.key == pygame.K_RIGHT:
                    DEBUG_plr_loc[0] += 1
                    print(DEBUG_plr_loc)
        # !! Tick game logic here !!

        # !! Handle graphics processing here !!
        screen.blit(graphics.render_map_data(currentMap.map, tilemap, DEBUG_plr_loc), (0,0))
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