import pygame as pg
from settings import *


outer_wall = [(0, 0, 0, 600), (0, 600, 800, 600), (800, 600, 800, 0), (800, 0, 0, 0)]
room1 = [(70, 0, 70, 100), (70, 100, 300, 100), (300, 100, 300, 0), (300, 0, 70, 0)]
room2 = [(70, 170, 70, 370), (70, 370, 115, 370), (185, 370, 300, 370), (300, 370, 300, 170), (300, 170, 265, 170), (210, 170, 70, 170)]
room3 = [(70, 440, 70, 530), (70, 530, 220, 530), (220, 530, 220, 510), (220, 470, 220, 440), (220, 440, 70, 440)]
room4 = [(220, 530, 280, 530), (320, 530, 370, 530), (370, 440, 220, 440)]
room5 = [(370, 280, 370, 480), (370, 520, 370, 530), (370, 530, 500, 530), (500, 530, 500, 280), (500, 280, 455, 280), (410, 280, 370, 280)]
room6 = [(370, 70, 370, 110), (370, 145, 370, 210), (370, 210, 550, 210), (550, 210, 550, 190), (550, 150, 550, 70), (550, 70, 370, 70)]
room7 = [(550,210, 730, 210), (730, 210, 730, 165), (730, 125, 730, 70), (730, 70, 550, 70)]
room8 = [(570, 280, 570, 400), (730, 400, 730, 350), (730, 310, 730, 280), (730, 280, 570, 280)]
room9 = [(570, 400, 570, 545), (570, 585, 570, 600), (570, 600, 730, 600), (730, 600, 730, 400), (730, 400, 660, 400), (620, 400, 570, 400)]

line_walls = [outer_wall, room1, room2, room3, room4, room5, room6, room7, room8, room9]

door1 = (370, 110, 370, 145)
door2 = (550, 190, 550, 150)
door3 = (730, 165, 730, 125)
door4 = (455, 280, 410, 280)
door5 = (220, 510, 220, 470)
door6 = (660, 400, 620, 400)


doors = [door1, door2, door3, door4, door5, door6]

#RECT COLLISION
# ROOM 1

OWC1 = (0, 0, 1, 600)
OWC2 = (0, 600, 800, 1)
OWC3 = (800, 0, 1, 600)
OWC4 = (0, 0, 800, 1)

vert1 = (70, 0, 1, 97)
vert2 = (300, 0, 1, 97)
vert3 = (70, 173, 1, 194)
vert4 = (300, 173, 1, 194)
vert5 = (70, 440, 1, 90)
vert6 = (220, 440, 1, 30)
vert7 = (220, 510, 1, 20)
vert8 = (370, 280, 1, 200)
vert9 = (370, 520, 1, 10)
vert10 = (500, 280, 1, 250)
vert11 = (370, 70, 1, 40)
vert12 = (370, 145, 1, 65)
vert13 = (550, 190, 1, 20)
vert14 = (550, 70, 1, 80)
vert15 = (730, 165, 1, 45)
vert16 = (730, 70, 1, 55)
vert17 = (570, 280, 1, 265)
vert18 = (570, 585, 1, 15)
vert19 = (730, 350, 1, 250)
vert20 = (730, 280, 1, 30)
vert21 = (170, 260, 1, 20)
vert22 = (200, 260, 1, 20)

hor1 = (73, 100, 224, 1)
hor2 = (73, 370, 42, 1)
hor3 = (185, 370, 112, 1)
hor4 = (265, 170, 32, 1)
hor5 = (70, 440, 300, 1)
hor6 = (70, 530, 210, 1)
hor7 = (320, 530, 180, 1)
hor8 = (370, 280, 40, 1)
hor9 = (455, 280, 45, 1)
hor10 = (370, 210, 360, 1)
hor11 = (370, 70, 360, 1)
hor12 = (570, 280, 160, 1)
hor13 = (570, 400, 50, 1)
hor14 = (660, 400, 70, 1)
hor15 = (73, 170, 137, 1)
hor16 = (175, 255, 20, 1)
hor17 = (175, 285, 20, 1)

vertical_collision = [OWC1, OWC3, vert1, vert2, vert3, vert4, vert5, vert6,
                      vert7, vert8, vert9, vert10, vert11, vert12, vert13, 
                      vert14, vert15, vert16, vert17, vert18, vert19, vert20,
                      vert21, vert22]
horizontal_collision = [OWC2, OWC4, hor1, hor2, hor3, hor4, hor5, hor6, hor7,
                        hor8, hor9, hor10, hor11, hor12, hor13, hor14, hor15,
                        hor16, hor17]

rect_walls = []

for i in vertical_collision:
    rect_walls.append(i)
for i in horizontal_collision:
    rect_walls.append(i)

matrix = [[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,],
          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,],
          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,],
          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0,],
          [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0,],
          [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,],
          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0,],
          [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,],
          [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,],
          [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,],
          [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,],
          [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,],
          [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0,],
          [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,],
          [0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0,],
          [0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0,],
          [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0,],
          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0,],
          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0,],
          [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0,],
          [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0,],
          [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0,],
          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0,],
          [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0,],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]]

#x = 36
#y = 25
num_of_1 = 0
row_length = len(matrix)
column_lenght = len(matrix[0])

nodes = {}

y_dif = HEIGHT / len(matrix)
x_dif =  WIDTH / len(matrix[0])

additional_grid_value = 12
x = additional_grid_value
y = additional_grid_value

r = -1
for row in matrix:
    r += 1

    s = -1
    for i in row:
        s += 1
        if i != 0:
            num_of_1 += 1
            nodes[(s, r)] = (x, y)
        x += x_dif
    y += y_dif
    x = additional_grid_value

print('####################################')
print('#  C Y B E R    S E N T I E N C E  #')
print('#                                  #')
print('#                                  #')
print('#   Coded by: Balbutin             #')
print('#   Members:                       #')
print('#     + Torres                     #')
print('#     + Guiling                    #')
print('#     + Atienza                    #')
print('#     + Padilla                    #')
print('#     + Acuno                      #')
print('#                                  #')
print('####################################')