from map_data import *
from settings import *
import pygame as pg


class Minimap:
    def __init__(self, window) -> None:
        self.window = window

    def draw(self):
        self.draw_rect()

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
    def __init__(self):
        pass