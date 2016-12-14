# -*- coding:utf-8 -*-
#import pygame_sdl2
#pygame_sdl2.import_as_pygame()

from pygame import init, font, Surface
from pygame.sprite import DirtySprite
from pygame.draw import polygon, aalines
from math import sin, cos, pi

init()
font.init()

class Hexagon(DirtySprite):
    def __init__(self, posx=0, posy=0, id_and_pos=(0, 0, 0), width=10, height=10, color=(70, 70, 125), prey_color=(225, 15, 15)):
        DirtySprite.__init__(self)
        self.image = Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.points = []
        self.color = color
        self.activ = False
        self.id_and_pos = id_and_pos
        self.prey_color = prey_color
        self.font = font.Font(None, 12)
        v = 0
        for i in range(6):
            self.points.append((cos(v)*((self.rect.width//2)-2)+self.rect.x,
                                sin(v)*((self.rect.height//2)-2)+self.rect.y))
            v += (pi*2)/6

    def update(self, surface, snake, prey, wall):
        if self.id_and_pos in snake:
            if self.id_and_pos == snake[-1:][0]:
                polygon(surface, (210, 205, 10), self.points, 0)
            else:
                polygon(surface, (35, 125, 30), self.points, 0)
        elif self is prey:
            polygon(surface, self.prey_color, self.points, 0)
        elif self.id_and_pos in wall:
            polygon(surface, (0, 0, 0), self.points, 0)
        else:
            polygon(surface, self.color, self.points, 0)
        aalines(surface, (210, 205, 10), 1, self.points, 1)
        #surface.blit(self.font.render(str(self.id_and_pos), 1, (255, 255, 255)), (self.rect.x - self.rect.width//3,
        #                                                                          self.rect.y - self.rect.height//9))