import pygame as pg
from main_lib import *

'''outer_wall = ((0, 0), (0, 600), (800, 600), (800, 0))

#Rooms
room1 = ((70, 0), (70, 100), (300, 100), (300, 0))
room2 = ((70, 170), (70, 370), (300, 370), (300, 170))
room3 = ((70, 440), (70, 530), (220, 530), (220, 440))
room4 = ((220, 440), (220, 530), (370, 530), (370, 440))
room5 = ((370, 280), (370, 530), (500, 530), (500, 280))
room6 = ((370, 70), (370, 210), (550, 210), (550, 70))
room7 = ((550, 70), (550, 210), (730, 210), (730, 70))
room8 = ((570, 280), (570, 400), (730, 400), (730, 280))
room9 = ((570, 400), (570, 600), (730, 600), (730, 400))'''

outer_wall = [(0, 0, 0, 600), (0, 600, 800, 600), (800, 600, 800, 0), (800, 0, 0, 0)]
room1 = [(70, 0, 70, 100), (70, 100, 300, 100), (300, 100, 300, 0), (300, 0, 70, 0)]
room2 = [(70, 170, 70, 370), (70, 370, 300, 370), (300, 370, 300, 170), (300, 170, 70, 170)]
room3 = [(70, 440, 70, 530), (70, 530, 220, 530), (220, 530, 220, 440), (220, 440, 70, 440)]
room4 = [(220, 440, 220, 530), (220, 530, 370, 530), (370, 530, 370, 440), (370, 440, 220, 440)]
room5 = [(370, 280, 370, 530), (370, 530, 500, 530), (500, 530, 500, 280), (500, 280, 370, 280)]
room6 = [(370, 70, 370, 210), (370, 210, 550, 210), (550, 210, 550, 70), (550, 70, 370, 70)]
room7 = [(550, 70, 550, 210), (550,210, 730, 210), (730, 210, 730, 70), (730, 70, 550, 70)]
room8 = [(570, 280, 570, 400), (570, 400, 730, 400), (730, 400, 730, 280), (730, 280, 570, 280)]
room9 = [(570, 400, 570, 600), (570, 600, 730, 600), (730, 600, 730, 400), (730, 400, 570, 400)]

line_walls = [outer_wall, room1, room2, room3, room4, room5, room6, room7, room8, room9]

#RECT COLLISION
# ROOM 1

OWC1 = pg.Rect(0, 0, 1, 600)
OWC2 = pg.Rect(0, 600, 800, 1)
OWC3 = pg.Rect(800, 0, 1, 600)
OWC4 = pg.Rect(0, 0, 800, 1)

wall1 = pg.Rect(70, 0, 1, 100)
wall2 = pg.Rect(70, 100, 230, 1)
wall3 = pg.Rect(300, 100, 1, 100)

rect_walls = [OWC1, OWC2, OWC3, OWC4, wall1, wall2]