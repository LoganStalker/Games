# -*- coding:utf-8 -*-

#import pygame_sdl2
#pygame_sdl2.import_as_pygame()

from pygame.display import Info
from pygame.sprite import DirtySprite
from pygame import Surface, font
from pygame.draw import polygon, aalines
from math import sin, cos, pi

info_display = Info()
DISPLAY_WIDTH = info_display.current_w
DISPLAY_HEIGHT = info_display.current_h
#DISPLAY_WIDTH = 1280
#DISPLAY_HEIGHT = 720

class Hexagon_Button(DirtySprite):
    def __init__(self, posx=0, posy=0, color=(100, 100, 100), border_color=(255, 255, 255), lable=u'Text', font_file=None, text_color=(0, 0, 0), font_size=10):
        DirtySprite.__init__(self)
        self.color = color
        self.color_text = text_color
        self.points = []
        self.border_color = border_color
        self.lable_text = lable
        font_size = DISPLAY_WIDTH * font_size // 100
        self.font = font.Font(font_file, font_size)
        self.lable = self.font.render(self.lable_text, 0, (self.color_text))
        self.image = Surface((self.lable.get_width()+self.lable.get_height(),
                              self.lable.get_width()+self.lable.get_height()))
        self.rect = self.image.get_rect()
        self.rect.x = DISPLAY_WIDTH * posx // 100
        self.rect.y = DISPLAY_HEIGHT * posy // 100

        v = 0
        for i in range(6):
            self.points.append((cos(v) * ((self.rect.width // 2) - 2) + self.rect.x+self.rect.width//2,
                                sin(v) * ((self.rect.height // 2) - 2) + self.rect.y+self.rect.height//2))
            v += (pi * 2) / 6

    def update(self, lable_text=u'new_text', posx=0, posy=0):
        self.lable = self.font.render(lable_text, 1, (self.color_text))
        self.image = Surface((self.lable.get_width()+self.lable.get_height(),
                              self.lable.get_width()+self.lable.get_height()))
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy

    def draw(self, surface, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            polygon(surface, (255-self.color[0], 255-self.color[1], 255-self.color[2]), self.points, 0)
        else:
            polygon(surface, self.color, self.points, 0)
        aalines(surface, self.border_color, True, self.points, 1)
        #aalines(surface, self.border_color, True, ((self.rect.x, self.rect.y),
        #                                           (self.rect.x + self.rect.width, self.rect.y),
        #                                           (self.rect.x + self.rect.width, self.rect.y + self.rect.height),
        #                                           (self.rect.x, self.rect.y + self.rect.height)), 1)
        surface.blit(self.lable, (self.rect.x + self.rect.width//9.4, self.rect.y + self.rect.height//2.5))