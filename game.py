##########################
#     PYTHON ROGUELIKE   #
#      I TRY AGAIN       #
# WHO CARES WHAT VERSION #
##########################

import pygame
import numpy as np 

# Import subscripts:

import graphics
import Actors
import mapdata


# !! Main game loop !!
def main():
    # Pygame Setup:
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    clock = pygame.time.Clock()
    running = True
    # Fire the loop!
    while running:
        # !! Check for events !!
        for event in pygame.event.get():
            # If the window is closed, kill the script.
            if event.type == pygame.QUIT:
                running = False

        # !! Tick game logic here !!

        # Fill the screen with nothing to clear the last frame
        screen.fill("pink")

        # !! Handle graphics processing here !!
        
        # Draw the changes to the display
        pygame.display.flip()

        # Set a 60 fps refresh rate cap
        clock.tick(60) 


#Run the main loop if we run this file directly
if __name__ == "__main__":
    main()