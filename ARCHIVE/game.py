########################
#   PYTHON ROGUELIKE   #
#     I TRY AGAIN      #
#     VERSION 0.0a     #
########################

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
import window

actorList = [Player(0,0)]
screen_resolution = [1024, 768]



# !! Main game loop !!
def main():
    # Pygame Setup:
    pygame.init()
    screen = pygame.display.set_mode(screen_resolution)
    clock = pygame.time.Clock()
    window.text_font = pygame.font.SysFont("fixedsys", 16)
    running = True
    # Init game state:
    gamestate = 0 # Default game state, turn-based map stuff.
    turnProcess = 0 #where are we in the "initiative"

    
    currentMap = mapdata.DungeonLevel("maps/debugmap.json") # this will need a replacement eventually
    
    
    actorList[0].get_player_data(False)
    # Init graphics data:
    game_window = window.ViewWindow("TEST", screen_resolution[0], screen_resolution[1])

    # Fire the loop!

    while running:
        # !! Check for events !!
        for event in pygame.event.get():
            # If the window is closed, kill the script.
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    screen_need_refresh = True
                elif event.key == pygame.K_UP:
                    if not actorList[0].posy == 0:
                        actorList[0].move_actor(-1, True)
                elif event.key == pygame.K_DOWN:
                    if not actorList[0].posy == currentMap.map.shape[1] -1:
                        actorList[0].move_actor(1, True)
                elif event.key == pygame.K_LEFT:
                    if not actorList[0].posx == 0:
                        actorList[0].move_actor(-1, False)
                elif event.key == pygame.K_RIGHT:
                    if not actorList[0].posx == currentMap.map.shape[0] -1:
                        actorList[0].move_actor(1, False)
        # !! Tick game logic here !!

        # !! Handle graphics processing here !!
        game_window.render_contents()
        screen.blit(game_window.window_surface, [0,0])

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