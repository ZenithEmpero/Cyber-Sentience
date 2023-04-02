from map_data import *
from settings import *
import pygame as pg, math as m


class Minimap:
    def __init__(self, game) -> None:
        self.window = game.window
        self.player = Player(game)

    def draw(self):
        self.draw_rect()
        self.player.draw()
        self.player.turn()

    def draw_rect(self):
        try:
            for a in rect_walls:
                pg.draw.line(self.window, wall_color, a[0], a[1])
                pg.draw.line(self.window, wall_color, a[1], a[2])
                pg.draw.line(self.window, wall_color, a[2], a[3])
                pg.draw.line(self.window, wall_color, a[3], a[0])
        except:
            print('MINIMAP ERROR')


class Player:
    def __init__(self, game):
        self.game = game
        self.window = game.window
        self.alive = True
        self.player_pos = [35, 20]
        self.angle = 0

    def draw(self):
        win = self.window
        self.draw_ray()
        self.player_circle = pg.draw.circle(win, 'white', self.player_pos, 10)
        self.movement()

    def draw_ray(self):
        win = self.window
        pos = self.player_pos
        ang = self.angle
        x = pos[0] + (m.cos(m.radians(ang)) * ray_length)
        y = pos[1] + (m.sin(m.radians(ang)) * ray_length)
        pg.draw.aaline(win, ray_color, pos, (x, y))

    def turn(self):
        if self.game.window_selected:
            mouse_rel = self.game.mouse_rel
            mouse_pos = self.game.mousepos
            win_size = pg.display.get_window_size()
            if mouse_rel != (0, 0):
                self.angle += (mouse_rel[0] * mouse_sensitivity)
            
            if (mouse_pos[0] > (WIDTH - 200)) or (mouse_pos[0] < 200) or (mouse_pos[1] > (HEIGHT - 200)) or (mouse_pos[1] < 200):
                pg.mouse.set_pos(WIDTH/2, HEIGHT/2)

    def movement(self):
        speed = (player_speed / 30) * self.game.delta_time
        sin_a = m.sin(m.radians(self.angle))
        cos_a = m.cos(m.radians(self.angle))
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        dx, dy = 0, 0

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        
        self.player_pos[0] += dx
        self.player_pos[1] += dy




