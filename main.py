import pygame as pg
import tkinter as tk
import sys
from threading import Thread
from settings import *
#from main_lib import *
from menu import *

class Main:
    def __init__(self) -> None:
        pg.init()
        #pg.mouse.set_visible(False)
        self.clock = pg.time.Clock()
        self.window_size = (WIDTH, HEIGHT)
        self.window_selected = False

        #self.new_game(self.window_size)
        #self.second_window()
        self.window = pg.display.set_mode(self.window_size, flags=pg.RESIZABLE)
        pg.display.set_caption('CYBER SENTIENCE 2203')

        
        self.body = None
        self.image = pg.image.load('textures/sample_png.png')
        width = self.image.get_rect().width
        height = self.image.get_rect().height
        self.image = pg.transform.scale(self.image, (width/10, height/10))

        self.menu = Menu(self)
        self.all_events = pg.event.get()
        self.running = True
        self.game_is_running = False

    def update(self):
        self.delta_time = self.clock.tick(FPS)

        self.mousepos = pg.mouse.get_pos()
        self.mouse_rel = pg.mouse.get_rel()
        pg.display.set_caption(f'CYBER SENTIENCE 2203 FPS: [{int(self.clock.get_fps())}]       x: [{self.mousepos[0]}]  y: [{self.mousepos[1]}] {self.mouse_rel}')
        
        self.draw()
        pg.display.flip()
        
    def check_events(self, game):
        self.all_events = pg.event.get()
        for events in self.all_events:
            if events.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if game:
                if events.type == pg.KEYDOWN:
                    if events.key == pg.K_ESCAPE:
                        self.window_selected = False
                        pg.mouse.set_visible(True)
                        self.game_is_running = False
                
                if events.type == pg.MOUSEBUTTONDOWN:
                    if self.mousepos[0] < WIDTH and self.mousepos[0] > 0 and self.mousepos[1] < HEIGHT and self.mousepos[1] > 0:
                        self.window_selected = True
                        pg.mouse.set_visible(False)
                        self.game_is_running = True

    def draw(self):
        if self.game_is_running:
            if not self.menu.running:
                self.window.fill(bg_color)        
                self.body.draw()
                self.body.graphics.render_walls()
                self.body.draw_line_wall()
                #self.body.draw_nodes()

                self.body.enemy.draw()

                self.body.graphics.draw_chase_texture()

                self.body.powercell.update()
                self.body.powersystem.update()
                self.window.blit(self.image, (200, 150))
                self.body.ui.update()

    def run(self):
        
        while self.running:
            if self.menu.running:
                self.menu.update()
                self.check_events(False)
            else:
                self.check_events(True)
                self.update()

if __name__ == '__main__':
    game = Main()
    game.run()
    pg.quit()