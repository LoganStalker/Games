# -*- coding:utf-8 -*-

#import pygame_sdl2
#pygame_sdl2.import_as_pygame()


from pygame.display import Info, set_mode, flip
from pygame.sprite import Group, LayeredDirty
from pygame import Surface, mixer
from pygame.time import Clock
from pygame.event import get
from pygame import QUIT, KEYDOWN, MOUSEBUTTONDOWN, mouse, K_RIGHT, K_LEFT, K_ESCAPE, K_RETURN, FULLSCREEN, KEYUP, K_UP, init, quit, display, HWSURFACE, DOUBLEBUF
from random import choice
from hexagon import Hexagon
from labels import Text
from buttons import Hexagon_Button
import sys

init()
info_display = Info()
print info_display
DISPLAY_WIDTH = info_display.current_w
DISPLAY_HEIGHT = info_display.current_h
#DISPLAY_WIDTH = 1280
#DISPLAY_HEIGHT = 720

window = set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), FULLSCREEN | HWSURFACE | DOUBLEBUF, 32)
screen = Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
screen.set_alpha(None)

def generate_court(size=50, col_rows=10, col_cols=17, start_posx=0, start_posy=0):
    hexes = LayeredDirty()
    id, x = 0, 0
    posy = start_posy
    posx = start_posx
    for j in range(col_cols):
        posx += size//1.45
        y = 0
        for i in range(col_rows):
            posy += size//1.24
            hexes.add(Hexagon(posx=posx, posy=posy, id_and_pos=(id, x, y), width=size, height=size))
            x += 2
            y += 1
        id += 1
        if posy == size//1.24 * col_rows + start_posy:
            posy = size//2.4 + start_posy
            x = 1
        elif posy == size//1.24 * col_rows + size//2.4 + start_posy:
            posy = start_posy
            x = 0
    return hexes

def Game_loop(mode=1):
    BOTTOM_BORDER = 20
    RIGHT_BORDER = 33
    size = DISPLAY_WIDTH / 32.0
    posx = (DISPLAY_WIDTH - (size//2) * RIGHT_BORDER) * 30 // 100
    posy = (DISPLAY_WIDTH - (size//2) * BOTTOM_BORDER) * 4 // 100
    court = generate_court(size=size, start_posx=posx, start_posy=posy, col_cols=RIGHT_BORDER, col_rows=BOTTOM_BORDER)
    snake = [(8, 18, 9),
             (8, 16, 8),
             (8, 14, 7)]
    prey = 0

    button_group = Group()
    left_button = Text(text=u'<', x=5, y=50, size=22,
                       font_file='a_Albionic.ttf', color=(250, 250, 250),
                       surface=screen)
    right_button = Text(text=u'>', x=85, y=50, size=22,
                       font_file='a_Albionic.ttf', color=(250, 250, 250),
                       surface=screen)
    button_group.add(left_button, right_button)
    menu_button = Hexagon_Button(lable=u'меню', posx=87, posy=2, font_size=3, font_file='a_Albionic.ttf',
                                  color=(35, 125, 30), text_color=(210, 205, 10), border_color=(210, 205, 10))

    wasted = Text(text=u'Потрачено!', x=6, y=35, size=7,
                  font_file='a_Albionic.ttf', color=(250, 150, 120), surface=screen)
    win = Text(text=u'Победа!', x=20, y=35, size=14,
                  font_file='a_Albionic.ttf', color=(250, 150, 120), surface=screen)
    points_label = Text(text=u'Очки: 0', x=2, y=2, size=3,
                  font_file='a_Albionic.ttf', color=(85, 170, 10), surface=screen)

    fps = Text(text=u'0', x=30, y=2, size=2, font_file='a_Albionic.ttf',
                color=(85, 170, 10), surface=screen)

    apple_eat_sound = mixer.Sound('sounds/Apple_eat.ogg')
    apple_eat_sound.set_volume(1.0)

    finally_background = Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    vector = 1
    alpha = 0
    id = 8
    x = 14
    y = 7
    dt = 0
    clock = Clock()
    wall = ((22, 38, 19),
            (22, 36, 18),
            (22, 34, 17),
            (22, 32, 16),
            (22, 30, 15),
            (22, 28, 14),
            (22, 26, 13),
            (22, 24, 12),
            (22, 22, 11),
            (22, 20, 10),
            (22, 18, 9),
            (22, 16, 8),
            (22, 14, 7),
            (10, 0, 0),
            (10, 2, 1),
            (10, 4, 2),
            (10, 6, 3),
            (10, 8, 4),
            (10, 10, 5),
            (10, 12, 6),
            (10, 14, 7),
            (10, 16, 8),
            (10, 18, 9),
            (10, 20, 10))
    #wall = ()
    razgon = 0
    done = False
    while not done:
        mp = mouse.get_pos()
        for event in get():
            if event.type == QUIT:
                done = True
                continue
            if event.type == KEYDOWN:
                if vector > 0:
                    if event.key == K_LEFT:
                        vector -= 1
                    if event.key == K_RIGHT:
                        vector += 1
                    if event.key == K_UP:
                        razgon = 350
                if event.key == K_ESCAPE:
                    done = True
            if event.type == KEYUP:
                if event.key == K_UP:
                    razgon = 0

            if event.type == MOUSEBUTTONDOWN:
                if vector > 0:
                    if left_button.rect.collidepoint(mp):
                        vector -= 1
                    elif right_button.rect.collidepoint(mp):
                        vector += 1
                if menu_button.rect.collidepoint(mp):
                    done = True
                    continue
            if vector < 1 and vector > -1:
                vector = 6
            elif vector > 6:
                vector = 1

        if not prey:
            prey = choice(tuple(court))
            in_snake = True
            in_wall = True
            while in_snake and in_wall:
                while prey.id_and_pos in wall:
                    prey = choice(tuple(court))
                in_wall = False
                while prey.id_and_pos in snake:
                    prey = choice(tuple(court))
                in_snake = False

        if dt > 400 - razgon:
            dt = 0
            if vector == 1:
                x -= 2
                y -= 1
            elif vector == 2:
                x -= 1
                if x % 2 != 0:
                    y -= 1
                id += 1
            elif vector == 3:
                x += 1
                if x % 2 == 0:
                    y += 1
                id += 1
            elif vector == 4:
                x += 2
                y += 1
            elif vector == 5:
                x += 1
                if x % 2 == 0:
                    y += 1
                id -= 1
            elif vector == 6:
                x -= 1
                if x % 2 != 0:
                    y -= 1
                id -= 1


            if mode == 1:
                if id < 0 or id > RIGHT_BORDER-1 or y < 0 or y > BOTTOM_BORDER-1:
                    vector = -2
            elif mode == 2:
                if id < 0:
                    id = RIGHT_BORDER-1
                    x += 1
                    y += 1
                if id > RIGHT_BORDER-1:
                    id = 0
                    x += 1
                    y += 1
                if y < 0:
                    y = BOTTOM_BORDER - 1
                    if id % 2 == 0:
                        x = y * 2
                    else:
                        x = y * 2 + 1
                if y > BOTTOM_BORDER - 1:
                    y = 0
                    if id % 2 == 0:
                        x = 0
                    else:
                        x = 1
            if (id, x, y) in wall:
                vector = -2

            next_step = (id, x, y)
            if next_step not in snake:
                if prey.id_and_pos != next_step:
                    snake.append(next_step)
                    snake.pop(0)
                else:
                    snake.append(next_step)
                    apple_eat_sound.play(0)
                    points_label.set_text(text=u'Очки: %s' % str(len(snake)-3))
                    prey = 0
                    #if len(snake) > 13:
                    #    vector = -2
            else:
                vector = -2

        screen.lock()
        screen.fill((20, 20, 40))
        court.update(screen, snake, prey, wall)
        screen.unlock()

        if vector == -2:
            if alpha < 200:
                alpha += 3
                finally_background.set_alpha(alpha)
            screen.lock()
            screen.blit(finally_background, (0, 0))
            #if len(snake) < 12:
            #    wasted.draw()
            #else:
            #    win.draw()
            wasted.set_text(text=u'Уничтожено %s жертв!' % str(len(snake)-3))
            wasted.draw()
            screen.unlock()

        #fps.set_text(u'FPS: %s' % clock.get_fps())
        #fps.draw()

        button_group.draw(screen)
        menu_button.draw(screen, mp)
        points_label.draw()

        window.blit(screen, (0, 0))
        clock.tick()

        dt += clock.get_time()

        flip()

        sys.stdout.write(str(clock.get_fps()) + '\n')
        sys.stdout.flush()


def Main_loop():

    mixer.init()
    background_sound = mixer.Sound('sounds/Dr_Mario.ogg')
    #background_sound = mixer.Sound('sounds/Skillet - Monster.ogg')
    background_sound.set_volume(0.2)
    background_sound.play(-1)
    Main_done = False

    size = DISPLAY_WIDTH / 6
    background = generate_court(size=size, start_posy=-size, start_posx=-size, col_rows=5, col_cols=10)
    start_button = Hexagon_Button(lable=u'Выжить', posx=2, posy=1, font_size=7, font_file='a_Albionic.ttf',
                                  text_color=(95, 210, 10), border_color=(95, 210, 10))
    exit_button = Hexagon_Button(lable=u'Выйти', posx=65, posy=25, font_size=7, font_file='a_Albionic.ttf',
                                  text_color=(95, 210, 10), border_color=(95, 210, 10))
    button = Hexagon_Button(lable=u'Нажраться', posx=35, posy=50, font_size=4, font_file='a_Albionic.ttf',
                                  text_color=(95, 210, 10), border_color=(95, 210, 10))
    while not Main_done:
        mp = mouse.get_pos()
        for event in get():
            if event.type == QUIT:
                Main_done = True
                continue
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Main_done = True
                if event.key == K_RETURN:
                    Game_loop()
            if event.type == MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(mp):
                    Game_loop()
                if exit_button.rect.collidepoint(mp):
                    Main_done = True
                    continue
                if button.rect.collidepoint(mp):
                    Game_loop(mode=2)

        background.update(screen, (0, 0, 0), (0, 0, 0), (1, 1, 0))

        start_button.draw(screen, mp)
        exit_button.draw(screen, mp)
        button.draw(screen, mp)

        window.blit(screen, (0, 0))
        flip()

if __name__ == "__main__":
    print display.list_modes(16)
    Main_loop()
    quit()
