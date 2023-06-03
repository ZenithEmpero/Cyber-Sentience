import pygame as pg

powersystem_img0 = pg.image.load('textures/ps_0.png')
powersystem_img1 = pg.image.load('textures/ps_1.png')
powersystem_img2 = pg.image.load('textures/ps_2.png')
powersystem_img3 = pg.image.load('textures/ps_3.png')
powercell_img = pg.image.load('textures/powercell.png')
portal_img = pg.image.load('textures/portal.png')

scaled_img_ps0 = {}
for i in range(0, 26):
    x = i / 5
    scaled_img_ps0[i] = pg.transform.scale(powersystem_img0, (powersystem_img0.get_width() * x, powersystem_img0.get_height() * x))
scaled_img_ps1 = {}
for i in range(0, 26):
    x = i / 5
    scaled_img_ps1[i] = pg.transform.scale(powersystem_img1, (powersystem_img1.get_width() * x, powersystem_img1.get_height() * x))
scaled_img_ps2 = {}
for i in range(0, 26):
    x = i / 5
    scaled_img_ps2[i] = pg.transform.scale(powersystem_img2, (powersystem_img2.get_width() * x, powersystem_img2.get_height() * x))
scaled_img_ps3 = {}
for i in range(0, 26):
    x = i / 5
    scaled_img_ps3[i] = pg.transform.scale(powersystem_img3, (powersystem_img3.get_width() * x, powersystem_img3.get_height() * x))

scaled_img_powercell = {}
for i in range(0, 16):
    x = i / 10
    scaled_img_powercell[i] = pg.transform.scale(powercell_img, (powercell_img.get_width() * x, powercell_img.get_height() * x))

scaled_img_portal = {}
for i in range(0, 21):
    x = i / 7
    scaled_img_portal[i] = pg.transform.scale(portal_img, (portal_img.get_width() * x, portal_img.get_height() * x))