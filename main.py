import pygame as pg
import tkinter as tk
from settings import *
from pan_lib import *

class Main:
    def __init__(self) -> None:
        pg.init()
        self.clock = pg.time.Clock()
        self.window_size = (WIDTH, HEIGHT)

        self.new_game(self.window_size)
        self.second_window()

        self.minimap = Minimap(self.window)

    def new_game(self, ws):
        self.window = pg.display.set_mode(ws)

    def second_window(self):
        if second_window:
            sw = tk.Tk() # SECOND WINDOW
            sw.geometry(sw_size)
            sw.mainloop()

    def update(self):
        self.draw()
        self.delta_time = self.clock.tick(FPS)
        mousepos = pg.mouse.get_pos()
        pg.display.set_caption(f'FPS: [{int(self.clock.get_fps())}]       x: [{mousepos[0]}]  y: [{mousepos[1]}]')
        pg.display.update()
        

    def check_events(self):
        for events in pg.event.get():
            if events.type == pg.QUIT:
                pg.quit()

    def draw(self):
        self.window.fill(bg_color)
        self.minimap.draw()

    def run(self):
        while True:
            self.check_events()
            self.update()

if __name__ == '__main__':
    game = Main()
    game.run()