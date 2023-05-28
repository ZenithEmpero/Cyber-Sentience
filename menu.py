import pygame as pg
import random as r
from settings import *
from main_lib import *

class Menu:
    def __init__(self, main) -> None:
        self.main = main
        self.window = self.main.window
        self.robot_image = pg.image.load('textures/menu.png')
        x = 4
        self.robot_image = pg.transform.scale(self.robot_image, (self.robot_image.get_width() * x, self.robot_image.get_height() * x))
        self.robot_image.set_alpha(50)

        # Fonts
        self.av_font = 'fonts/av.ttf'
        self.tvd_font = 'fonts/tvd.ttf'

        # Title Text
        color = 100,100,100
        pos = (WIDTH/2, HEIGHT*.1)
        font_size = 75
        text = 'Cyber Sentience 2203'
        self.title_text = Text(self, text, self.av_font, font_size, color, pos, static= True, cs=True, clickable=False)


        # Start Text
        color = 200,200,200
        pos = (WIDTH/2, HEIGHT*.4)
        font_size = 40
        text = 'Start'
        self.start_text = Text(self, text, self.tvd_font, font_size, color, pos, False, True, clickable=True)
        
        # Settings Text
        pos = (WIDTH/2, HEIGHT*.55)
        text = 'Settings'
        self.settings_text = Text(self, text, self.tvd_font, font_size, color, pos, False, True, clickable=True)

        # Exit Text
        pos = (WIDTH/2, HEIGHT*.7)
        text = 'Exit'
        self.exit_text = Text(self, text, self.tvd_font, font_size, color, pos, True, True, clickable=True)
        


        # Flags
        self.running = True

    def update(self):
        self.display()
        self.button_event_checker()

    def display(self):
        self.window.fill((15, 15, 15))
        self.window.blit(self.robot_image, (WIDTH/2 - (self.robot_image.get_width() / 2), 0))

        self.title_text.update()
        self.start_text.update()
        self.settings_text.update()
        self.exit_text.update()

        pg.display.flip()

    def button_event_checker(self):
        self.start_flag_checker()
        self.exit_flag_checker()

    def start_flag_checker(self):
        if self.start_text.clicked:
            self.running = False
            self.main.game_is_running = True
            self.main.body = Body(self.main)
            self.start_text.clicked = False

    def exit_flag_checker(self):
        if self.exit_text.clicked:
            self.running = False
            self.main.running = False


class Text:
    def __init__(self, menu, text, font, fontsize, color, pos, static, cs, clickable) -> None:
        self.menu = menu
        self.window = menu.window
        self.text_data = text
        self.color = color
        self.color_deduction = 50
        self.font = pg.font.Font(font, fontsize)
        self.text = self.font.render(text, False, color)
        self.text_rect = self.text.get_rect()
        self.pos = pos[0] - (self.text.get_width() // 2), pos[1]
        self.text_rect.x = self.pos[0]
        self.text_rect.y = self.pos[1]
        self.static = static
        self.color_static = cs
        self.clickable = clickable
        self.in_rect = False
        self.clicked = False

    def update(self):
        #pg.draw.rect(self.window, 'green', self.text_rect)
        self.display()
        if self.clickable:
            self.cursor_in_text()
        

    def display(self):
        pos = self.pos[0], self.pos[1]
        if self.static:
            if r.randint(0, 80) == 50:
                pos = self.pos[0] + r.randint(-50, 50), self.pos[1]
                if r.randint(0, 4) == 3:
                    pos = pos[0], pos[1] + r.randint(-20, 20)

        color = self.color
        self.text = self.font.render(self.text_data, False, color)
        if self.color_static:
            if r.randint(0, 10) == 4:
                color = r.randint(self.color[0] - self.color_deduction, self.color[0])
                color = (color, color, color)
                self.text = self.font.render(self.text_data, False, color)
                
        self.window.blit(self.text, pos)

    def cursor_in_text(self):
        mouse_pos = pg.mouse.get_pos()
        
        if self.text_rect.collidepoint(mouse_pos):
            if not self.in_rect:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
                self.in_rect = True
            self.check_click_event()
        else:
            if self.in_rect:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
                self.in_rect = False
        
    def check_click_event(self):
        for event in self.menu.main.all_events:
            if event.type == pg.MOUSEBUTTONUP:
                print(f'Clicked {self.text_data} Button')
                self.clicked = True
        