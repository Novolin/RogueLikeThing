##########################
#     PYTHON ROGUELIKE   #
#      I TRY AGAIN       #
# WHO CARES WHAT VERSION #
##########################

import pygame
import numpy as np 


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
                        currentMap.generate_rand_layout()
                    except:
                        print("fuck")
                        pass
                    screen_need_refresh = True
                if event.key == pygame.K_1:
                    screen.fill("pink")
        # !! Tick game logic here !!

        # !! Handle graphics processing here !!
        screen.blit(graphics.render_map_data(currentMap.map, tilemap), (0,0))
        # Draw the changes to the display
        pygame.display.flip()

        # Set a 60 fps refresh rate cap
        clock.tick(60) 


#Run the main loop if we run this file directly
if __name__ == "__main__":
    main()