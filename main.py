import pygame as pg
import tkinter as tk
import sys
from threading import Thread
from settings import *
from main_lib import *
from dev_win import *

class Main:
    def __init__(self) -> None:
        pg.init()
        #pg.mouse.set_visible(False)
        self.clock = pg.time.Clock()
        self.window_size = (WIDTH, HEIGHT)
        self.window_selected = False

        #self.new_game(self.window_size)
        #self.second_window()
        Thread(target= self.new_game(self.window_size)).start()
        Thread(target= sec_win).start()

        self.minimap = Minimap(self)

    def new_game(self, ws):
        self.window = pg.display.set_mode(ws, flags=pg.RESIZABLE)

    def update(self):
        self.delta_time = self.clock.tick(FPS)
        self.mousepos = pg.mouse.get_pos()
        self.mouse_rel = pg.mouse.get_rel()
        pg.display.set_caption(f'FPS: [{int(self.clock.get_fps())}]       x: [{self.mousepos[0]}]  y: [{self.mousepos[1]}] {self.mouse_rel}')
        
        self.draw()
        pg.display.flip()
        

    def check_events(self):
        for events in pg.event.get():
            if events.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if events.type == pg.KEYDOWN:
                if events.key == pg.K_ESCAPE:
                    self.window_selected = False
                    pg.mouse.set_visible(True)
            if events.type == pg.MOUSEBUTTONDOWN:
                if self.mousepos[0] < WIDTH and self.mousepos[0] > 0 and self.mousepos[1] < HEIGHT and self.mousepos[1] > 0:
                    self.window_selected = True
                    pg.mouse.set_visible(False)

    def draw(self):
        self.window.fill(bg_color)        
        self.minimap.draw()
        self.minimap.grahics.render()

    def run(self):
        while True:
            self.check_events()
            self.update()

if __name__ == '__main__':
    game = Main()
    game.run()