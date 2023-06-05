from prescaling import *
from map_data import *
from settings import *
from pathfinding.core.grid import *
from pathfinding.finder.a_star import AStarFinder
import pygame as pg, math as m, random as r

class Body:
    def __init__(self, game) -> None:
        pg.mixer.init(buffer=1024)
        self.game = game
        self.win_size = (WIDTH, HEIGHT)
        self.window = game.window
        self.enemy = Enemy(self)
        self.powercell = PowerCell(self)
        self.powersystem = PowerSystem(self)
        self.portal = Portal(self)
        self.player = Player(self)
        self.graphics = Graphics(self)
        self.ui = UI(self)
        self.vertical_collision = vertical_collision
        self.horizontal_collision = horizontal_collision
        

        self.SCB = SCB

    def draw(self):
        self.player.draw()
        self.player.turn()
        self.check_if_win()


    def draw_line_wall(self):
        try:
            for a in line_walls:
                for i in a:
                    pg.draw.aaline(self.window, wall_color, (i[0], i[1]), (i[2], i[3]))
        except:
            print('body ERROR')

        for a in rect_walls:
            pg.draw.rect(self.window, rect_collision_color, a)
        for a in doors:
            pg.draw.aaline(self.window, 'brown', (a[0], a[1]), (a[2], a[3]))


    def draw_nodes(self):
        try:
            for i in self.enemy.pos_nodes:
                pg.draw.circle(self.window, 'yellow', i, 5)
        except:
            pass
        '''try:
            for i in nodes:
                pg.draw.circle(self.window, 'yellow', i, 5)
        except:
            pass
'''
    def check_if_win(self):
        if self.player.escaped:
            self.game.menu.running = True
            pg.mixer.quit()
class UI:
    def __init__(self, body) -> None:
        self.body = body
        self.game = body.game
        self.player = body.player
        self.window = body.window
        self.ws = body.win_size
        self.player.ui = self
        self.powersystem = body.powersystem
        self.portal = body.portal

        self.minimap_img = pg.image.load('textures/minimap.png')
        x = .8
        self.minimap_img = pg.transform.scale(self.minimap_img, (self.minimap_img.get_width()*x, self.minimap_img.get_height()*x))

        self.jumpscare_img = pg.image.load('textures/A_jumpscare.png')
        x = 5
        self.jumpscare_img = pg.transform.scale(self.jumpscare_img, (self.jumpscare_img.get_width() * x, self.jumpscare_img.get_height() * x))
        #self.jumpscare_img_pos = r.randint(self.ws[0]*.2, self.ws[0]*.8) - self.jumpscare_img.get_width()/2, r.randint(-self.ws[1]*.083, self.ws[1]*.03)

        self.sign1_img = pg.image.load('textures/sign1.png')
        x = .5
        self.sign1_img = pg.transform.scale(self.sign1_img, (self.sign1_img.get_width() * x, self.sign1_img.get_height() * x))
        
        self.powercell_img = pg.image.load('textures/powercell.png')
        x = 1
        self.powercell_img = pg.transform.scale(self.powercell_img, (self.powercell_img.get_width() * x, self.powercell_img.get_height() * x))
        
        self.m_font = 'fonts/m.ttf'
        self.l_font = 'fonts/l.otf'

        # POWERCELL TEXT
        powercell_text = 'You can only carry one powercell at a time.'
        pt_font = pg.font.Font(self.m_font, 25)
        self.pt = pt_font.render(powercell_text, False, 'white')
        self.pt_activate = False

        # OBJECTIVE TEXT
        self.obj_font = pg.font.Font(self.m_font, 19)

        # DIRECTION TEXT
        self.dir_font = pg.font.Font(self.l_font, 50)
        # Flag

    def update(self):
        #self.ws = self.body.win_size
        self.draw()
    
    def draw(self):
        self.jumpscare()

        if self.player.alive:
            self.sprint_bar()
            self.sign1_update()
            self.powercell_update()
            self.objectives_texts()
            self.direction()
            self.display_minimap()
            if self.pt_activate:
                self.powercell_text()

    def jumpscare(self):
       if not self.body.player.alive:
            self.window.blit(self.jumpscare_img, (self.jumpscare_img_pos))
       else:
        a = int(self.ws[0]*.2)
        b = int(self.ws[0]*.8)
        c = int(-self.ws[1]*.083)
        d = int(self.ws[1]*.03)
        self.jumpscare_img_pos = r.randint(a, b) - self.jumpscare_img.get_width()/2, r.randint(c, d)
 

    def sprint_bar(self):
        #pg.draw.line(self.window, 'white', (20, 195), (20, 405), 13)
        stamina = self.player.stamina
        percentage = (stamina/100)*100
        if percentage <= 50:
            # Transition from green to yellow
            red = 255
            green = int(percentage * 5.1)  # Increase red component from 0 to 255
        else:
            # Transition from yellow to red
            red = int((1 - (percentage - 50) / 50) * 255)  # Decrease green component from 255 to 0
            green = 255
        pg.draw.line(self.window, (red, green, 0), (20, 400 - (stamina * 2)), (20, 400), 20)

    def sign1_update(self):
        self.sign1_img_pos = (self.ws[0]/2 - self.sign1_img.get_width()/2, self.ws[1]/2 - self.sign1_img.get_height()/2)
        if self.player.able_to_input_power:
            self.window.blit(self.sign1_img, self.sign1_img_pos)

    def powercell_update(self):
        if self.player.carrying_powercell:
            if self.player.look_behind == 0:
                self.window.blit(self.powercell_img, (self.ws[0]*.625, self.ws[1]*.5))

    def powercell_text(self):
        self.window.blit(self.pt, (self.ws[0]/2 - self.pt.get_width()/2, self.ws[1]*.85 - self.pt.get_height()/2))

    def objectives_texts(self):
        self.objectives_text('Objectives: ', 0, 'white')
        color = 'white'
        if self.portal.activated:
            self.objectives_text('- Escape through the portal', 56, 'white')
            color = 'green'
        self.objectives_text(f'- Recharge the power system {self.powersystem.power}/3', 28, color)

    def objectives_text(self, text, ypos, color):
        self.ot = self.obj_font.render(text, False, color)
        self.window.blit(self.ot, (self.ws[0]*.02, self.ws[1]*.04 - self.ot.get_height()/2 + ypos))

    def direction(self):
        text = self.dir_font.render(self.player.direction, False, 'white')
        self.window.blit(text, (self.ws[0]*.5 - text.get_width()/2, self.ws[1]*.04))

    def display_minimap(self):
        if self.player.show_minimap:
            self.window.blit(self.minimap_img, (self.ws[0]*.5 - self.minimap_img.get_width()/2, self.ws[1]*.5 - self.minimap_img.get_height()/2))

class Player:
    
    def __init__(self, body):
        self.walls = {}
        self.body = body
        self.game = self.body.game
        self.window = self.game.window
        self.ws = body.win_size
        self.enemy = self.body.enemy
        self.powercell = body.powercell
        self.powersystem = body.powersystem
        self.portal = body.portal
        self.ui = None
        self.alive = True
        self.stamina = 100
        self.running = False
        self.player_pos = [35, 20]
        self.angle = 90
        self.direction = ''
        self.escaped = False
        self.show_minimap = False
        
        self.vertical_angle = pg.display.get_window_size()[1] / 2
        self.middle_point = 0
        self.point_len = 0
        self.middle_point2 = 0
        self.point_len2 = 0
        self.middle_point3 = 0
        self.point_len3 = 0
        self.middle_point4 = 0
        self.point_len4 = 0
        self.points = []
        self.seen_by_enemy = False
        self.player_sees_enemy = False
        self.game_over = False
        self.return_to_menu_delay = 0
        self.speed = player_speed
        self.added_fov = 0
        self.carrying_powercell = False
        self.inside_ps_range = False
        self.sees_ps = False
        self.able_to_input_power = False
        self.look_behind = 0
    
        

        for i in line_walls:
            for a in i:
                self.walls[a] = 'w'
        for i in doors:
            self.walls[i] = 'b'


    def draw(self):
        #self.ws = self.body.win_size
        self.draw_ray()

        self.player_rect_collision = pg.Rect(self.player_pos[0] - 10, self.player_pos[1] - 10, 20, 20)
        #pg.draw.rect(self.window, rect_collision_color, self.player_rect_collision)

        #self.player_circle = pg.draw.circle(win, 'white', self.player_pos, 10)
        if self.alive:
            self.controls()

        self.check_intersection()

        self.enemy_vision()
        self.check_if_able_to_input_power()
        self.check_click_event()
        self.return_to_menu()
        self.direction_update()

    def draw_ray(self):
        win = self.window
        pos = self.player_pos
        ang = self.angle
        x = pos[0] + (m.cos(m.radians(ang)) * ray_length)
        y = pos[1] + (m.sin(m.radians(ang)) * ray_length)
        #pg.draw.aaline(win, ray_color, pos, (x, y))

        self.cast_multiple_rays()

    def turn(self):
        if not self.body.game.menu.running:
            if self.alive:
                if self.game.window_selected:
                    mouse_rel = self.game.mouse_rel
                    mouse_pos = self.game.mousepos
                    if mouse_rel[0] != 0:
                        self.angle += (mouse_rel[0] * mouse_sensitivity)
                    if mouse_rel[1] != 0:
                        if self.vertical_angle < (self.ws[1] * .8):
                            if mouse_rel[1] > 0:
                                pass
                            else:
                                self.vertical_angle -= ((mouse_rel[1] * 10) * mouse_sensitivity)   

                        if self.vertical_angle > (self.ws[1] * .2):
                            if mouse_rel[1] < 0:
                                pass
                            else:
                                self.vertical_angle -= ((mouse_rel[1] * 10) * mouse_sensitivity) 
                    
                    if (mouse_pos[0] > (self.ws[0] - 200)) or (mouse_pos[0] < 200) or (mouse_pos[1] > (self.ws[1] - 200)) or (mouse_pos[1] < 200):
                        pg.mouse.set_pos(self.ws[0]/2, self.ws[1]/2)

                    #pg.mouse.set_pos(WIDTH/2, HEIGHT/2)

    def controls(self):
        keys = pg.key.get_pressed()

        self.speed = (player_speed / 30) * self.game.delta_time

        if keys[pg.K_LSHIFT]:
            if self.stamina > 0:
                if self.running:
                    self.speed += 1.4
                    self.stamina -= .015 * self.game.delta_time
                else:
                    self.stamina += .0005 * self.game.delta_time

                    if self.stamina > 100:
                        self.stamina = 100
 
        else:
            self.stamina += .005 * self.game.delta_time

            if self.stamina > 100:
                self.stamina = 100
                    
        sin_a = m.sin(m.radians(self.angle))
        cos_a = m.cos(m.radians(self.angle))
        speed_sin = self.speed * sin_a
        speed_cos = self.speed * cos_a
        dx, dy = 0, 0

        self.running = False
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
            self.running = True
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
            self.running = True
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
            self.running = True
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos
            self.running = True
        if keys[pg.K_SPACE]:
            self.look_behind = 180
        else:
            self.look_behind = 0
        if keys[pg.K_TAB]:
            self.show_minimap = True
        else:
            self.show_minimap = False
        

        self.collision_checker(dx, dy)
        self.player_pos[0] += dx
        self.player_pos[1] += dy
                


    def collision_checker(self, dx, dy):
        for i in self.game.body.vertical_collision:
            if pg.Rect.colliderect(self.player_rect_collision, i):
                if self.player_pos[0] > i[0]:
                    if dx < 0:
                        self.player_pos[0] -= dx
                else:
                    if dx > 0:
                        self.player_pos[0] -= dx
                        
        for i in self.game.body.horizontal_collision:
            if pg.Rect.colliderect(self.player_rect_collision, i):
                if self.player_pos[1] > i[1]:
                    if dy < 0:
                        self.player_pos[1] -= dy
                else:
                    if dy > 0:
                        self.player_pos[1] -= dy

        if self.player_rect_collision.collidepoint(self.enemy.enemy_coordinate):
            if not self.game_over:
                self.fgame_over()

        if self.player_rect_collision.collidepoint(self.portal.pos):
            if self.portal.activated:
                self.fwin()

        self.ui.pt_activate = False
        if self.player_rect_collision.collidepoint(self.powercell.pos):
            if not self.carrying_powercell:
                self.carrying_powercell = True
                self.powercell.change_location()
            else:
                self.ui.pt_activate = True

        if self.player_rect_collision.colliderect(self.powersystem.rect):
            if not self.inside_ps_range:
                self.inside_ps_range = True
        else:
            self.inside_ps_range = False
    
    def min_and_max(self, a, b, c):
        x = max(a, min(b, (c - self.enemy.distance_to_player) * (b / c)))
        return x

    def cast_multiple_rays(self):
        self.multiple_rays_pos = []
        if self.alive:
            pf = player_fov + self.min_and_max(0, 45, 170) + self.added_fov
        else:
            pf = player_fov
        cone_angle = pf * (m.pi / 180)
        for i in range(num_rays):
            angle = m.radians(self.angle + self.look_behind) + (i - num_rays / 2) * cone_angle / num_rays
            direction = [m.cos(angle), m.sin(angle)]
            end_point = (self.player_pos[0] + direction[0] * fov_length, self.player_pos[1] + direction[1] * fov_length)
            self.multiple_rays_pos.append(end_point)

    def check_intersection(self):
        self.points = {}
        enemy_box_intersection_points = []
        
        for a in self.multiple_rays_pos:
            
 

            self.intersection_points = {}
            num_of_intersections = 0
            for i in self.walls:
                x1 = i[0]
                y1 = i[1]
                x2 = i[2]
                y2 = i[3]
                x3 = self.player_pos[0]
                y3 = self.player_pos[1]
                x4 = a[0]
                y4 = a[1]

                t_num = self.intersection_formula('t', x1, y1, x2, y2, x3, y3, x4, y4)
                u_num = self.intersection_formula('u', x1, y1, x2, y2, x3, y3, x4, y4)
                den = self.intersection_formula('d', x1, y1, x2, y2, x3, y3, x4, y4)
                if den == 0:
                    return
                self.t = (t_num/ den)    
                self.u = u_num / den
                self.point_of_intersection = (x1 + self.t * (x2 - x1)), (y1 + self.t * (y2 - y1)) 
                if (0 < self.t) and (self.t < 1) and (1 > self.u > 0):
                    self.intersection_points[self.point_of_intersection] = self.walls[i]
                    
                    num_of_intersections += 1

            if len(self.intersection_points) > 0:
                z = self.check_nearest_point()
                x = z[0]
                y = z[1]
                self.points[x] = y
            else:
                #pg.draw.aaline(self.window, ray_color, self.player_pos, a)
                self.points[a] = None

        powercell_cross_intersection = []
        powersystem_cross_intersection = []
        portal_cross_intersection = []
        for a in self.points:
            self.powercell_cross = self.powercell.line1, self.powercell.line2
            for i in self.powercell_cross:
                x1 = i[0][0]
                y1 = i[0][1]
                x2 = i[1][0]
                y2 = i[1][1]
                x4 = a[0]
                y4 = a[1]

                t_num = self.intersection_formula('t', x1, y1, x2, y2, x3, y3, x4, y4)
                u_num = self.intersection_formula('u', x1, y1, x2, y2, x3, y3, x4, y4)
                den = self.intersection_formula('d', x1, y1, x2, y2, x3, y3, x4, y4)
                if den == 0:
                    return
                self.t = (t_num/ den)    
                self.u = u_num / den
                self.point_of_intersection = (x1 + self.t * (x2 - x1)), (y1 + self.t * (y2 - y1)) 
                if (0 < self.t < 1) and (0 < self.u < 1):
                    powercell_cross_intersection.append(a)
                    #pg.draw.aaline(self.window, 'green', self.player_pos, self.point_of_intersection)


            self.enemy_render_box = self.enemy.line1, self.enemy.line2
            
            # ENEMY
            for i in self.enemy_render_box:
                x1 = i[0][0]
                y1 = i[0][1]
                x2 = i[1][0]
                y2 = i[1][1]

                t_num = self.intersection_formula('t', x1, y1, x2, y2, x3, y3, x4, y4)
                u_num = self.intersection_formula('u', x1, y1, x2, y2, x3, y3, x4, y4)
                den = self.intersection_formula('d', x1, y1, x2, y2, x3, y3, x4, y4)
                if den == 0:
                    return
                self.t = (t_num/ den)    
                self.u = u_num / den
                self.point_of_intersection = (x1 + self.t * (x2 - x1)), (y1 + self.t * (y2 - y1)) 
                if (0 < self.t < 1) and (0 < self.u < 1):
                    enemy_box_intersection_points.append(a)
                    #pg.draw.aaline(self.window, 'green', self.player_pos, self.point_of_intersection)

            self.powersystem_cross = self.powersystem.line1, self.powersystem.line2
            
            for i in self.powersystem_cross:
                x1 = i[0][0]
                y1 = i[0][1]
                x2 = i[1][0]
                y2 = i[1][1]

                t_num = self.intersection_formula('t', x1, y1, x2, y2, x3, y3, x4, y4)
                u_num = self.intersection_formula('u', x1, y1, x2, y2, x3, y3, x4, y4)
                den = self.intersection_formula('d', x1, y1, x2, y2, x3, y3, x4, y4)
                if den == 0:
                    return
                self.t = (t_num/ den)    
                self.u = u_num / den
                self.point_of_intersection = (x1 + self.t * (x2 - x1)), (y1 + self.t * (y2 - y1)) 
                if (0 < self.t < 1) and (0 < self.u < 1):
                    powersystem_cross_intersection.append(a)
                    #pg.draw.aaline(self.window, 'green', self.player_pos, self.point_of_intersection)

            self.portal_cross = self.portal.line1, self.portal.line2
            for i in self.portal_cross:
                x1 = i[0][0]
                y1 = i[0][1]
                x2 = i[1][0]
                y2 = i[1][1]

                t_num = self.intersection_formula('t', x1, y1, x2, y2, x3, y3, x4, y4)
                u_num = self.intersection_formula('u', x1, y1, x2, y2, x3, y3, x4, y4)
                den = self.intersection_formula('d', x1, y1, x2, y2, x3, y3, x4, y4)
                if den == 0:
                    return
                self.t = (t_num/ den)    
                self.u = u_num / den
                self.point_of_intersection = (x1 + self.t * (x2 - x1)), (y1 + self.t * (y2 - y1)) 
                if (0 < self.t < 1) and (0 < self.u < 1):
                    portal_cross_intersection.append(a)
                    #pg.draw.aaline(self.window, 'green', self.player_pos, self.point_of_intersection)



        try:
            self.point_len = m.ceil(len(enemy_box_intersection_points)/2)
            if self.point_len > 0:
                if not self.player_sees_enemy:
                    self.player_sees_enemy = True
            else:
                if self.player_sees_enemy:
                    self.player_sees_enemy = False
            self.middle_point = enemy_box_intersection_points[self.point_len]
        except:
            pass

        self.point_len2 = len(powercell_cross_intersection)//2
        if self.point_len2 != 0:
            self.middle_point2 = powercell_cross_intersection[self.point_len2]
            self.powercell.calculate_distance_to_player()

        self.point_len3 = len(powersystem_cross_intersection)//2
        if self.point_len3 != 0:
            self.middle_point3 = powersystem_cross_intersection[self.point_len3]
            self.powersystem.calculate_distance_to_player()
            self.sees_ps = True
        else:
            self.sees_ps = False

        self.point_len4 = len(portal_cross_intersection)//2
        if self.point_len4 != 0:
            self.middle_point4 = portal_cross_intersection[self.point_len4]
            self.portal.calculate_distance_to_player()


        self.enemy_ray_intersection_points = []
        for i in self.walls:
            x1 = i[0]
            y1 = i[1]
            x2 = i[2]
            y2 = i[3]
            x4 = self.enemy_end_pos[0]
            y4 = self.enemy_end_pos[1]

            t_num = self.intersection_formula('t', x1, y1, x2, y2, x3, y3, x4, y4)
            u_num = self.intersection_formula('u', x1, y1, x2, y2, x3, y3, x4, y4)
            den = self.intersection_formula('d', x1, y1, x2, y2, x3, y3, x4, y4)
            if den == 0:
                return
            t = t_num / den   
            u = u_num / den
            point_of_intersection = (x1 + t * (x2 - x1)), (y1 + t * (y2 - y1)) 

            if self.check_intersection_conditions(t, u):
                self.enemy_ray_intersection_points.append(point_of_intersection)

                point_dis = {}
                for i in self.enemy_ray_intersection_points:
                    x1 = self.player_pos[0]
                    y1 = self.player_pos[1]
                    x2 = i[0]
                    y2 = i[1]
        
                    dif = (x1 - x2, y1 - y2)
                    pyth = m.sqrt((dif[0] ** 2 + dif[1] ** 2))
                    point_dis[pyth] = (x2, y2)
                point_dis = sorted(point_dis.items())
                self.enemy_ray_point = point_dis[0][1]


        # ENEMY DETECTION
        i = self.enemy_render_box[0]
        x1 = i[0][0]
        y1 = i[0][1]
        x2 = i[1][0]
        y2 = i[1][1]
        x4 = self.enemy_ray_point[0]
        y4 = self.enemy_ray_point[1]

        t_num = self.intersection_formula('t', x1, y1, x2, y2, x3, y3, x4, y4)
        u_num = self.intersection_formula('u', x1, y1, x2, y2, x3, y3, x4, y4)
        den = self.intersection_formula('d', x1, y1, x2, y2, x3, y3, x4, y4)
        if den == 0:
            return
        t = t_num / den
        u = u_num / den

        if self.check_intersection_conditions(t, u):
            if not self.seen_by_enemy:
                self.seen_by_enemy = True
        else:
            if self.seen_by_enemy:
                self.seen_by_enemy = False

    def intersection_formula(self, type, x1, y1, x2, y2, x3, y3, x4, y4):
        if type == 't':
            return ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4))
        elif type == 'u':
            return ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2))
        elif type == 'd':
            return ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))

    def check_intersection_conditions(self, t, u):
        if (0 < t) and (t < 1) and (1 > u > 0):
            return True
        else:
            return False

    def check_nearest_point(self):
        point_dis = {}
        if len(self.intersection_points) > 0:
            for i in self.intersection_points:
                x1 = self.player_pos[0]
                y1 = self.player_pos[1]
                x2 = i[0]
                y2 = i[1]

                dif = (abs(x1 - x2), abs(y1 - y2))
                pyth = m.sqrt((dif[0])**2 + (dif[1]**2))
                point_dis[pyth] = (x2, y2, self.intersection_points[i])
            point_dis = sorted(point_dis.items())
            x = point_dis[0][1][0], point_dis[0][1][1]
            color = point_dis[0][1][2]
            #pg.draw.aaline(self.window, ray_color, self.player_pos, x)
            #self.points[x] = None
            return [x, color]
        
    def enemy_vision(self):
        for i in range(num_rays):
            # Calculate the angle between player and enemy
            self.enemy_pos = self.enemy.enemy_coordinate[0], self.enemy.enemy_coordinate[1]
            self.enemy_angle = m.atan2(self.enemy_pos[1] - self.player_pos[1], self.enemy_pos[0] - self.player_pos[0])
            #angle = m.radians(angle)

            self.enemy_end_x = self.player_pos[0] + enemy_ray_length * m.cos(self.enemy_angle)
            self.enemy_end_y = self.player_pos[1] + enemy_ray_length * m.sin(self.enemy_angle)
            self.enemy_end_pos = self.enemy_end_x, self.enemy_end_y

            try:
                pass
                #pg.draw.aaline(self.window, 'blue', self.player_pos, self.enemy_ray_point)
            except:
                pass

    def check_if_able_to_input_power(self):
        if self.inside_ps_range:
            if self.carrying_powercell:
                if self.sees_ps:
                    self.able_to_input_power = True
                else:
                    self.able_to_input_power = False
            else:
                self.able_to_input_power = False
        else:
            self.able_to_input_power = False

    def check_click_event(self):
        for events in self.game.all_events:
            if events.type == pg.MOUSEBUTTONUP:
                if self.able_to_input_power:
                    self.powersystem.power += 1
                    self.carrying_powercell = False

    def fgame_over(self):
        self.alive = False
        self.game_over = True
        self.angle = m.degrees(self.enemy_angle)
        self.body.graphics.jumpscare.play()

    def fwin(self):
        self.escaped = True

    def return_to_menu(self):
        if not self.alive:
            if self.return_to_menu_delay < 25:
                self.return_to_menu_delay += .01 * self.game.delta_time
            else:
                self.game.menu.running = True
                pg.mouse.set_visible(True)

    def direction_update(self):
        angle = m.radians(self.angle)
        dx = m.cos(angle)
        dy = m.sin(angle)
        mag = m.sqrt(dx*dx + dy*dy)
        direction = ''
        if mag >0:
            dx /= mag
            dy /= mag
        if dx > 0.5:
            if dy > 0.5:
                direction = "SE"
            elif dy < -0.5:
                direction = "NE"
            else:
                direction = "E"
        elif dx < -0.5:
            if dy > 0.5:
                direction = "SW"
            elif dy < -0.5:
                direction = "NW"
            else:
                direction = "W"
        else:
            if dy > 0.5:
                direction = "S"
            elif dy < -0.5:
                direction = "N"
        self.direction = direction

class Graphics:
    def __init__(self, body):
        self.wall_texture = pg.image.load('textures/wall.jpg')
        self.window = body.window
        self.game = body.game
        self.ws = body.win_size
        self.player = body.player
        self.body = body
        self.enemy = body.enemy
        self.powersystem = body.powersystem
        self.powercell = body.powercell
        self.portal = body.portal
        self.fog = 1
        self.or_fog = self.fog
        self.a = 0
        self.pc = 1

        self.A_texture = pg.image.load('textures/A.v2.png')
        self.A_texture_size = self.A_texture.get_width(), self.A_texture.get_height()
        
        #self.chase_image = pg.image.load('textures/chase_image.jpg').convert_alpha()
        #self.chase_rect = pg.Rect(0, 0, self.ws[0], self.ws[1])
        self.transparent_surface = pg.Surface((self.ws[0], self.ws[1]), pg.SRCALPHA)

        # POWER CELL
        self.powercell_img = pg.image.load('textures/powercell.png')
        x = .4
        self.powercell_img = pg.transform.scale(self.powercell_img, (self.powercell_img.get_width() * x, self.powercell_img.get_height() * x))
        self.pc_wave = 0

        # POWER SYSTEM
        self.powersystem_img0 = pg.image.load('textures/ps_0.png')
        self.powersystem_img1 = pg.image.load('textures/ps_1.png')
        self.powersystem_img2 = pg.image.load('textures/ps_2.png')
        self.powersystem_img3 = pg.image.load('textures/ps_3.png')

        # PORTAL
        self.portal_img = pg.image.load('textures/portal.png')

        #AUDIO
        self.heartbeat_audio = pg.mixer.Sound('audio/heart_beat.mp3')
        self.tv_static_audio = pg.mixer.Sound('audio/tv_static.wav')
        self.ambience = pg.mixer.Sound('audio/ambience.wav')
        self.jumpscare = pg.mixer.Sound('audio/jumpscare.wav')
        self.jumpscare.set_volume(.3)

        self.heartbeat_audio.set_volume(0)
        self.heartbeat_audio.play(loops=-1)
        
        self.tv_static_audio.set_volume(0)
        self.tv_static_audio.play(loops=-1)

        self.ambience.set_volume(.3)
        self.ambience.play(loops=-1)

        # Flags
        self.fog_increased = False
        self.fog_delay = 0


    def render_walls(self):
        #self.ws = self.body.win_size
        self.vertical_angle = self.player.vertical_angle
        va = self.ws[1]/2#self.vertical_angle
        x = 4
        coord = None
        coord2 = None
        coord3 = None
        coord4 = None
        
        for i in self.player.points:
            wall_color = self.player.points[i]
            x1 = self.player.player_pos[0]
            y1 = self.player.player_pos[1]
            x2 = i[0]
            y2 = i[1]

            dif = (x2 - x1, y2 - y1)
            angle =  (self.player.angle) - (m.degrees(m.atan2(dif[1], dif[0])))
            pyth = m.sqrt(dif[0]**2 + dif[1]**2)
            dis = pyth * m.cos(m.radians(angle))
            try:
                a = ((30 * self.ws[1]) / (dis)) #/ 10
            except:
                pass
            #a = (50000 / pyth) / 10

            if wall_color == 'w':
                color = [181, 181, 181]
            elif wall_color == 'b':
                color = [171, 88, 0]
            else:
                color = [0, 0, 0]
            c1 = []

            for b in color:
                c1.append(b * (self.fog - (pyth / fov_length)))

            if not self.player.alive:
                if self.fog_delay < 100:
                    self.fog_delay += .0008 * self.body.game.delta_time
                else:
                    if self.fog > 0:
                        self.fog -= .00001 * self.body.game.delta_time

            #try:
            g = self.min_and_max(0, 20, 200)
            g = int(g)
            if self.player.alive:
                ds = r.randint(0, g)
            else:
                ds = 0

            try:
                pg.draw.line(self.window, c1, (x, va + a + ds), (x, va - a - ds), m.ceil(self.ws[0]/num_rays) + 1)
            except:
                pass

            #except:
                #pass

            if self.player.point_len != 0:
                if self.player.middle_point == i:
                    #pg.draw.circle(self.window, 'red', (x, va), 100)
                    coord = (x, va)

            if self.player.point_len2 != 0:
                if self.player.middle_point2 == i:

                    coord2 = (x, va)

            if self.player.point_len3 != 0:
                if self.player.middle_point3 == i:
                    coord3 = (x, va)

            if self.player.point_len4 != 0:
                if self.player.middle_point4 == i:
                    coord4 = (x, va)
                    
            x += (self.ws[0]/num_rays)
        
            
        if self.player.player_sees_enemy:
            self.enemy_sprite_size_calculator()


        if self.player.alive:
            sprites = {}
            sprites[self.enemy.distance_to_player] = 'e'
            sprites[self.powersystem.distance_to_player] = 's'
            sprites[self.powercell.distance_to_player] = 'c'
            sprites[self.portal.distance_to_player] = 'p'
            sprites = dict(sorted(sprites.items(), reverse=True))
            for i in sprites:
                if sprites[i] == 'e':

                    if coord != None:
                        self.window.blit(self.A_texture_scaled, (coord[0] - self.A_texture_dimension_half[0], coord[1] - (self.A_texture_dimension_half[1] - (self.a))))
                elif sprites[i] == 'c':
                    self.pc_wave += (.005) * self.body.game.delta_time
                    wave = m.sin(self.pc_wave) * 15
                    self.pc_sprite_size_calculator()
                    if coord2 != None:
                        self.window.blit(self.powercell_img, (coord2[0] - self.powercell_img.get_width() / 2, coord2[1] - ((self.powercell_img.get_height() / 2) + wave - (self.pc * 7))))
                elif sprites[i] == 's':
                    self.ps_sprite_size_calculator()
                    if coord3 != None:
                        self.window.blit(self.powersystem_img_used, (coord3[0] - self.powersystem_img_used.get_width() / 2, coord3[1] - ((self.powersystem_img_used.get_height() / 2))))
                elif sprites[i] == 'p':
                    self.portal_sprite_size_calculator()
                    if coord4 != None:
                        if self.portal.activated:
                            self.window.blit(self.portal_img, (coord4[0] - self.portal_img.get_width()/2, coord4[1] - self.portal_img.get_height()/2))



    def enemy_sprite_size_calculator(self):
        
        self.a = ((.3 * self.ws[1]) / (self.enemy.distance_to_player))
        x = 5
        if self.a > x:
            self.a = x
        self.A_texture_scaled = pg.transform.scale(self.A_texture, (self.A_texture_size[0] * self.a, self.A_texture_size[1] * self.a))
        self.A_texture_dimension = self.A_texture_scaled.get_rect().size
        self.A_texture_dimension_half = ((self.A_texture_dimension[0] / 2), (self.A_texture_dimension[1] / 2))

    def ps_sprite_size_calculator(self):
        self.ps = ((self.ws[1]) / self.powersystem.distance_to_player)
        if self.ps > 25:
            self.ps = 25
        if int(self.ps) > 0:
            if self.powersystem.power == 0:
                self.powersystem_img_used = scaled_img_ps0[int(self.ps)]
            elif self.powersystem.power == 1:
                self.powersystem_img_used = scaled_img_ps1[int(self.ps)]
            elif self.powersystem.power == 2:
                self.powersystem_img_used = scaled_img_ps2[int(self.ps)]
            elif self.powersystem.power == 3:
                self.powersystem_img_used = scaled_img_ps3[int(self.ps)]
        else:
            self.powersystem_img0 = scaled_img_ps2[2]

    def pc_sprite_size_calculator(self):
        self.pc = ((self.ws[1]) / self.powercell.distance_to_player)
        if self.pc > 15:
            self.pc = 15
        if int(self.pc) > 0:
            self.powercell_img = scaled_img_powercell[int(self.pc)]
        else:
            self.powercell_img = scaled_img_powercell[2]

    def portal_sprite_size_calculator(self):
        self.p = ((self.ws[1]) / self.portal.distance_to_player)
        if self.p > 20:
            self.p = 20
        if int(self.p) > 0:
            self.portal_img = scaled_img_portal[int(self.p)]
        else:
            self.portal_img = scaled_img_portal[2]



    def draw_chase_texture(self):
        if self.player.alive:
            self.b = max(0, min(90, (170 - self.enemy.distance_to_player) * (90 / 170))) * 2
            if self.b > 90:
                self.b = 90
            #self.chase_rect_clone = self.chase_rect.copy()
            #self.chase_rect_scaled = pg.transform.scale(self.chase_image_clone, (self.chase_image.get_width() * 25, self.chase_image.get_height() * 19))
            #pg.draw.rect(self.window, (255, 0, 0, self.b), self.chase_rect_clone, pg.BLEND_RGBA_MULT)
            #self.chase_rect_clone.fill((255, 255, 255, self.b), None, pg.BLEND_RGBA_MULT)
        # self.window.blit(self.chase_rect_clone, (0, 0))    
            self.transparent_surface = pg.Surface((self.ws[0], self.ws[1]), pg.SRCALPHA)
            self.transparent_surface.fill((255, 0, 0, self.b))
            self.window.blit(self.transparent_surface, (0, 0))

            f = 1
            self.c = self.min_and_max(0, f, 250)
            self.d = self.min_and_max(0, 0.25, 150)
            #elf.c = max(0, min(f, (170 - self.enemy.distance_to_player) * (f / 170)))
            #print(self.d)
            if self.c > f:
                self.c = f
            if pg.mixer.get_init():
                self.heartbeat_audio.set_volume(self.c)
                self.tv_static_audio.set_volume(self.d) 
        else:
            if pg.mixer.get_init():
                self.heartbeat_audio.set_volume(0)
                self.tv_static_audio.set_volume(0) 
                self.ambience.set_volume(0)

    def min_and_max(self, a, b, c):
        x = max(a, min(b, (c - self.enemy.distance_to_player) * (b / c)))
        return x
class Enemy:
    def __init__(self, body) -> None:
        self.entity = 0
        self.body = body
        self.game = body.game
        self.window = body.window
        self.enemy_coordinate = (800, 600)
        self.line1 = (0, 0), (0, 0)
        self.line2 = (0, 0), (0, 0)
        self.distance_to_player = 0
        self.last_node = (0, 0)
        #self.path_gen(35, 24, 35, 24)
        self.pos_nodes = []
        self.speed = (enemy_speed/30)
        self.chase_speed = self.speed * 2
        self.speed_using = self.speed

        # FLAGS
        self.go_to_seen_pos = False

    def draw(self):
        if self.body.player.alive:
            self.check_if_see_player()
            self.draw_render_box()
            self.distance_to_player_checker()
            self.movement()

    def draw_render_box(self):
        self.render_box = [(self.enemy_coordinate[0] - 10, self.enemy_coordinate[1] - 10), (self.enemy_coordinate[0] + 10, self.enemy_coordinate[1] + 10)]
        self.line1 = (self.render_box[0][0], self.enemy_coordinate[1]), (self.render_box[1][0], self.enemy_coordinate[1])
        self.line2 = (self.enemy_coordinate[0], self.render_box[0][1]), (self.enemy_coordinate[0], self.render_box[1][1])
        #pg.draw.line(self.window, 'white', (self.render_box[0][0], self.enemy_coordinate[1]), (self.render_box[1][0], self.enemy_coordinate[1]))
        #pg.draw.line(self.window, 'white', (self.enemy_coordinate[0], self.render_box[0][1]), (self.enemy_coordinate[0], self.render_box[1][1]))

    def movement(self):
        if len(self.pos_nodes) > 0:
            speed = self.speed_using * self.game.delta_time

            if not self.go_to_seen_pos:
                self.target_node = self.pos_nodes[0]
                if self.check_if_des():
                    self.pos_nodes.pop(0)
                speed = self.speed * self.game.delta_time
            else:
                
                if self.see_player:
                    self.pos_nodes = self.player_pos[0], self.player_pos[1]
                    self.target_node = self.pos_nodes[0], self.pos_nodes[1]
                self.check_if_des()
                speed = self.chase_speed * self.game.delta_time

            targ_coor = self.target_node
            epos = self.enemy_coordinate[0], self.enemy_coordinate[1]
            x = epos[0]
            y = epos[1]

            dx = targ_coor[0] - epos[0]
            dy = targ_coor[1] - epos[1]

            angle = m.atan2(dy, dx)

            x += m.cos(angle) * speed
            y += m.sin(angle) * speed
            
            self.enemy_coordinate = (x, y)
            

        else:
            self.create_path_2()

    def check_if_des(self):
        condition = abs(self.enemy_coordinate[0] - self.target_node[0]) < 3 and abs(self.enemy_coordinate[1] - self.target_node[1]) < 3
        if condition:
            if not self.go_to_seen_pos:
                
                return True
            else:
                self.go_to_seen_pos = False
                self.create_path_2()
                return True
        else: 
            return False

    def path_gen(self, x1, y1, x2, y2):
        grid = Grid(matrix= matrix) 

        start = grid.node(x1, y1)
        end = grid.node(x2, y2)
        self.last_node = (x2, y2)

        finder = AStarFinder() #diagonal_movement= DiagonalMovement.always

        self.path, runs = finder.find_path(start, end, grid)

        self.pos_node()

    def create_path(self):
        while True:
            if self.random_node_picker():
                break
                
        self.path_gen(self.last_node[0], self.last_node[1], self.matrix_x, self.matrix_y)

    def create_path_2(self):
        while True:
            if self.random_node_picker():
                break
        self.random_start_node_picker()

        self.path_gen(self.pyths[0][1][0], self.pyths[0][1][1], self.matrix_x, self.matrix_y)


    def random_node_picker(self):
        self.matrix_x = r.randint(0, column_lenght - 1)
        self.matrix_y = r.randint(0, row_length - 1)
        if matrix[self.matrix_y][self.matrix_x] == 1:
            return True
        else:
            return False
        
    def random_start_node_picker(self):
        self.pyths = {}
        for i in nodes:
            diff = (self.enemy_coordinate[0] - nodes[i][0]), (self.enemy_coordinate[1] - nodes[i][1])
            pyth = m.sqrt(diff[0] ** 2 + diff[1] ** 2)
            self.pyths[pyth] = (i[0], i[1])
        self.pyths = sorted(self.pyths.items())

    def pos_node(self):
        self.pos_nodes = []
        for i in self.path:
            self.pos_nodes.append(((i[0] * x_dif) + additional_grid_value, (i[1] * y_dif) + additional_grid_value))
        #self.pos_nodes.pop(0)
    
    def distance_to_player_checker(self):
        self.player_pos = self.body.player.player_pos
        x = round(self.player_pos[0] - self.enemy_coordinate[0], 2)
        y = round(self.player_pos[1] - self.enemy_coordinate[1], 2)
        self.distance_to_player = round(m.sqrt(x**2 + y**2), 2) # HYPOTENUSE FORMULA


    def check_if_see_player(self):
        self.see_player =  self.body.player.seen_by_enemy
        if self.see_player:
            self.go_to_seen_pos = True

class PowerCell:
    def __init__(self, body) -> None:
        self.body = body
        self.window = body.window
        self.powersystem = None
        self.powered = False
        self.pos = (630, 140)
        self.cross_size = 3
        self.cross = ((0, 0), (0, 0), (0, 0), (0, 0))
        self.line1 = (0, 0), (0, 0)
        self.line2 = (0, 0),  (0, 0)
        self.distance_to_player = 1

        self.locations = ((r.randint(20, 560), r.randint(380, 580)), (r.randint(310, 560), r.randint(20, 360)), (r.randint(555, 780), r.randint(20, 580)))
        self.pos = self.locations[1]

    def update(self):
        self.draw_on_map()
        self.update_cross()

    def draw_on_map(self):
        pg.draw.aaline(self.window, 'white', self.cross[0], self.cross[1])
        pg.draw.aaline(self.window, 'white', self.cross[2], self.cross[3])

    def update_cross(self):
        self.line1 = (abs(self.cross_size - self.pos[0]), self.pos[1]), (self.cross_size + self.pos[0], self.pos[1])
        self.line2 = (self.pos[0], abs(self.cross_size - self.pos[1])), (self.pos[0], self.cross_size + self.pos[1])
        self.cross = self.line1[0], self.line1[1], self.line2[0], self.line2[1]

    def calculate_distance_to_player(self):
        player_pos = self.body.player.player_pos
        sub = player_pos[0] - self.pos[0], player_pos[1] - self.pos[1]
        pyth = m.sqrt(sub[0] ** 2 + sub[1] ** 2)
        self.distance_to_player = pyth

    def change_location(self):
        if self.powersystem.power < 2:
            self.pos = self.locations[self.powersystem.power - 1]
        else:
            self.pos = (170, 48)

class PowerSystem:
    def __init__(self, body) -> None:
        self.body = body
        self.window = body.window
        self.powercell = body.powercell
        self.power = 0
        self.pos = (185, 270)
        self.cross_size = 3
        self.cross = ((0, 0), (0, 0), (0, 0), (0, 0))
        self.line1 = (0, 0), (0, 0)
        self.line2 = (0, 0),  (0, 0)
        self.distance_to_player = 1
        
        x = 65
        y = 65
        self.rect = (self.pos[0] - x/2, self.pos[1] - y/2, x, y)

        self.powercell.powersystem = self

    def update(self):
        #self.draw_on_map()
        self.update_cross()

    def draw_on_map(self):
        pg.draw.aaline(self.window, 'white', self.cross[0], self.cross[1])
        pg.draw.aaline(self.window, 'white', self.cross[2], self.cross[3])

    def update_cross(self):
        self.line1 = (abs(self.cross_size - self.pos[0]), self.pos[1]), (self.cross_size + self.pos[0], self.pos[1])
        self.line2 = (self.pos[0], abs(self.cross_size - self.pos[1])), (self.pos[0], self.cross_size + self.pos[1])
        self.cross = self.line1[0], self.line1[1], self.line2[0], self.line2[1]

    def calculate_distance_to_player(self):
        player_pos = self.body.player.player_pos
        sub = player_pos[0] - self.pos[0], player_pos[1] - self.pos[1]
        pyth = m.sqrt(sub[0] ** 2 + sub[1] ** 2)
        self.distance_to_player = pyth

class Portal:
    def __init__(self, body) -> None:
        self.body = body
        self.window = body.window
        self.powersystem = body.powersystem
        self.pos = (765, 580)
        self.cross_size = 3
        self.cross = ((0, 0), (0, 0), (0, 0), (0, 0))
        self.line1 = (0, 0), (0, 0)
        self.line2 = (0, 0),  (0, 0)
        self.distance_to_player = 1

        self.activated = False

    def update(self):
        self.draw_on_map()
        self.update_cross()
        self.check_if_activated()

    def draw_on_map(self):
        pg.draw.aaline(self.window, 'white', self.cross[0], self.cross[1])
        pg.draw.aaline(self.window, 'white', self.cross[2], self.cross[3])

    def update_cross(self):
        self.line1 = (abs(self.cross_size - self.pos[0]), self.pos[1]), (self.cross_size + self.pos[0], self.pos[1])
        self.line2 = (self.pos[0], abs(self.cross_size - self.pos[1])), (self.pos[0], self.cross_size + self.pos[1])
        self.cross = self.line1[0], self.line1[1], self.line2[0], self.line2[1]

    def calculate_distance_to_player(self):
        player_pos = self.body.player.player_pos
        sub = player_pos[0] - self.pos[0], player_pos[1] - self.pos[1]
        pyth = m.sqrt(sub[0] ** 2 + sub[1] ** 2)
        self.distance_to_player = pyth

    def check_if_activated(self):
        if self.powersystem.power >= 3:
            self.activated = True