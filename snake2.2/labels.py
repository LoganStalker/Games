# -*- coding:utf-8 -*-
#import pygame_sdl2
#pygame_sdl2.import_as_pygame()

from pygame import init, font, display
from pygame.sprite import DirtySprite

init()
font.init()
info_display = display.Info()
DISPLAY_WIDTH = info_display.current_w
DISPLAY_HEIGHT = info_display.current_h
#DISPLAY_WIDTH = 1280
#DISPLAY_HEIGHT = 720

class Text(DirtySprite):
    def __init__(self, text='TEXT', x=1, y=2, size=10, font_file=None, color=(255, 255, 255), surface=None):
        DirtySprite.__init__(self)
        self.color = color
        self.surface = surface
        self.font = font.Font(font_file, int(DISPLAY_WIDTH * size // 100))
        self.image = self.font.render(text, 1, self.color)
        self.rect = self.image.get_rect()
        self.rect.x = DISPLAY_WIDTH * x / 100
        self.rect.y = DISPLAY_HEIGHT * y / 100

    def set_text(self, text=''):
        self.image = self.font.render(text, 1, self.color)

    def update(self):
        pass

    def draw(self):
        self.surface.blit(self.image, (self.rect.x, self.rect.y))