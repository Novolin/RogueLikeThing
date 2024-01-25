####
# Window Rendering Stuff
# Separated from graphics for dev playaround.
###

import pygame

#Define Colours for UI elements:
windowBlue = (0,0,180)
windowGrey = (192,192,192)
windowDarkGrey = (128,128,128)
# Black and White are included in pygame
# Define font objects:
text_font = pygame.font.SysFont("fixedsys", 11)


class ViewWindow:
    # Parent class for the window
    # We'll also use this for the main view
    def __init__(self, title, origin, width, height):
        self.title = title
        self.title_size = text_font.size(title)
        self.origin = origin
        self.pos_x = origin[0]
        self.pos_y = origin[1]
        self.width = width
        self.height = height
        self.window_surface = pygame.Surface()
        self.sub_windows = {}
        self.needs_refresh = True

    def render_contents(self):
        self.needs_refresh = False # We don't need to re-draw this window
        pass # this will read the contents of any sub windows and then stick them on their surface

    def render_title_bar(self):
        title_surface = pygame.Surface()
        title_surface.fill("black")
        pygame.draw.rect(title_surface, windowBlue, self.pos_x + 1, self.width - 2)
        text_size = text_font.size(self.title)
        text_surf = text_font.render(self.title, False, "white", windowBlue)
        title_surface.blit(text_surf, self.pos_x + (text_size[1] / 2))
        return title_surface

    def define_sub_window(self, sub_window_data, window_loc):
        self.sub_windows[window_loc] = sub_window_data

class GameWindow(ViewWindow):
    def __init__(self, title, origin, width, height, view_type = "map"):
        super().__init__(title, origin, width, height)
        if view_type == "map":
            # render map data within the map window
            # for now do the border dealio
            # i need to figure out 9 way tiling lmao
            self.border_data = pygame.image.load("data/bordertest.png").convert()

class PlayerStatus(ViewWindow):
    def __init__(self, player_name):
        super().__init__(player_name, (1,48), 303, 143)
        self.health_bar = False
        self.mana_bar = False
        self.player_status = False
    
    def update_player_state(self, player):
        # read the player object to get their health/mana/etc.
        pass
        

class TextFeed(ViewWindow):
    pass

class MenuBar:
    def __init__(self):
        #this will be the menu bar
        #its handled differently :)
        pass