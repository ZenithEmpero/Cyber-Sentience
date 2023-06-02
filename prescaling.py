import pygame as pg

powersystem_img = pg.image.load('textures/ps_0.png')
powercell_img = pg.image.load('textures/powercell.png')

scaled_img = {}
for i in range(0, 26):
    x = i / 5
    scaled_img[i] = pg.transform.scale(powersystem_img, (powersystem_img.get_width() * x, powersystem_img.get_height() * x))

scaled_img_powercell = {}
for i in range(0, 11):
    x = i / 10
    scaled_img_powercell[i] = pg.transform.scale(powercell_img, (powercell_img.get_width() * x, powercell_img.get_height() * x))
