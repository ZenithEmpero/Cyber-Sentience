import pygame as pg

pg.init()
window = pg.display.set_mode((800, 600))

rect1_color = 'white'

running = True
while running:
    #Variables
    mouse_pos = pg.mouse.get_pos()
    rect1 = pg.Rect(mouse_pos[0] - 50, mouse_pos[1] - 50, 100, 100)

    rect2 = pg.Rect(400, 300, 100, 100)

    window.fill('black')

    pg.draw.rect(window, rect1_color, rect1)
    #pg.draw.rect(window, 'white', rect2)

    if pg.Rect.colliderect(rect1, rect2):
        rect1_color = 'green'
    else:
        rect1_color = 'white'


    for events in pg.event.get():
        if events.type == pg.QUIT:
            running = False

    pg.display.flip()

    
pg.quit()