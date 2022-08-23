import pygame
from static_main import upper_font

class Button:
    def __init__(self, str, x, y):
        self.x = x
        self.y = y
        self.str = str
        self.brect = pygame.Rect(x, y, 150, 90)

    def render(self, win):
        pygame.draw.rect(win, (125, 125, 0), self.brect)   
        self.render_text(win)     

    def render_text(self, win):
        text_surface = upper_font.render(self.str, True, (0, 0, 0))
        win.blit(text_surface, ( self.x+75 - text_surface.get_width()/2 ,  self.y+45 - text_surface.get_height()/2) ) 

    def get_pressed(self, pos):
        if self.brect.collidepoint(pos):
            return self.str
        return False