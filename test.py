import pygame as pg
pg.init()

window = pg.display.set_mode((800, 600))
running = True
while running:
    window.fill('black')
    pg.draw.rect(window, 'white', (400, 300, 100, 100))

    for events in pg.event.get():
        if events.type == pg.QUIT:
            running = False
    pg.display.flip()

pg.quit()