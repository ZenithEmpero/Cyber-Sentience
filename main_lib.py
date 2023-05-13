from map_data import *
from settings import *
from dev_win import *
from pathfinding.core.grid import *
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from threading import Thread
import pygame as pg, math as m, random as r
import sys

pg.mixer.init()

class Minimap:
    def __init__(self, game) -> None:
        self.game = game
        self.window = game.window
        self.enemy = Enemy(self)
        self.player = Player(self)
        self.grahics = Graphics(self)
        self.vertical_collision = []
        self.horizontal_collision = []

        x = 0
        for i in rect_walls:
            if x % 2 == 0:
                self.vertical_collision.append(i)
            else:
                self.horizontal_collision.append(i)
            x += 1
        self.SCB = SCB

    def draw(self):
    
        #self.draw_line_wall()
        
        self.player.draw()
        #self.enemy.draw()
        self.player.turn()


    def draw_line_wall(self):
        try:
            for a in line_walls:
                for i in a:
                    pg.draw.aaline(self.window, wall_color, (i[0], i[1]), (i[2], i[3]))
        except:
            print('MINIMAP ERROR')

        for a in rect_walls:
            pg.draw.rect(self.window, rect_collision_color, a)


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
            pass'''

class Player:
    
    def __init__(self, minimap):
        self.walls = []
        self.minimap = minimap
        self.game = self.minimap.game
        self.window = self.game.window
        self.enemy = self.minimap.enemy
        self.alive = True
        self.player_pos = [35, 20]
        self.angle = 0
        
        self.vertical_angle = pg.display.get_window_size()[1] / 2
        self.middle_point = 0
        self.point_len = 0
        self.points = []

        for i in line_walls:
            for a in i:
                self.walls.append(a)


    def draw(self):
        win = self.window
        self.draw_ray()

        self.player_rect_collision = pg.Rect(self.player_pos[0] - 10, self.player_pos[1] - 10, 20, 20)
        pg.draw.rect(self.window, rect_collision_color, self.player_rect_collision)

        self.player_circle = pg.draw.circle(win, 'white', self.player_pos, 10)
        self.movement()

        self.check_intersection()

    def draw_ray(self):
        win = self.window
        pos = self.player_pos
        ang = self.angle
        x = pos[0] + (m.cos(m.radians(ang)) * ray_length)
        y = pos[1] + (m.sin(m.radians(ang)) * ray_length)
        pg.draw.aaline(win, ray_color, pos, (x, y))

        self.cast_multiple_rays()

    def turn(self):
        if self.game.window_selected:
            mouse_rel = self.game.mouse_rel
            mouse_pos = self.game.mousepos
            win_size = pg.display.get_window_size()
            if mouse_rel[0] != 0:
                self.angle += (mouse_rel[0] * mouse_sensitivity)
            if mouse_rel[1] != 0:
                if self.vertical_angle < (win_size[1] * .8):
                    if mouse_rel[1] > 0:
                        pass
                    else:
                        self.vertical_angle -= ((mouse_rel[1] * 10) * mouse_sensitivity)   

                if self.vertical_angle > (win_size[1] * .2):
                    if mouse_rel[1] < 0:
                        pass
                    else:
                        self.vertical_angle -= ((mouse_rel[1] * 10) * mouse_sensitivity) 
            
            if (mouse_pos[0] > (WIDTH - 200)) or (mouse_pos[0] < 200) or (mouse_pos[1] > (HEIGHT - 200)) or (mouse_pos[1] < 200):
                pg.mouse.set_pos(WIDTH/2, HEIGHT/2)

            #pg.mouse.set_pos(WIDTH/2, HEIGHT/2)

    def movement(self):
        speed = (player_speed / 30) * self.game.delta_time
        sin_a = m.sin(m.radians(self.angle))
        cos_a = m.cos(m.radians(self.angle))
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        dx, dy = 0, 0

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        
        self.player_pos[0] += dx
        self.player_pos[1] += dy

        self.collision_checker(dx, dy)

    def collision_checker(self, dx, dy):
        for i in self.game.minimap.vertical_collision:
            if pg.Rect.colliderect(self.player_rect_collision, i):
                self.player_pos[0] -= dx
                if self.player_pos[0] > i[0]:
                    self.player_pos[0] += .1
                elif self.player_pos[0] < i[0]:
                    self.player_pos[0] -= .1

        for i in self.game.minimap.horizontal_collision:
            if pg.Rect.colliderect(self.player_rect_collision, i):
                self.player_pos[1] -= dy
                if self.player_pos[1] > i[1]:
                    self.player_pos[1] += .1
                elif self.player_pos[1] < i[1]:
                    self.player_pos[1] -= .1
    def min_and_max(self, a, b, c):
        x = max(a, min(b, (c - self.enemy.distance_to_player) * (b / c)))
        return x

    def cast_multiple_rays(self):
        self.multiple_rays_pos = []
        pf = player_fov + self.min_and_max(0, 45, 170)
        cone_angle = pf * (m.pi / 180)
        for i in range(num_rays):
            angle = m.radians(self.angle) + (i - num_rays / 2) * cone_angle / num_rays
            direction = [m.cos(angle), m.sin(angle)]
            end_point = (self.player_pos[0] + direction[0] * fov_length, self.player_pos[1] + direction[1] * fov_length)
            self.multiple_rays_pos.append(end_point)

    def check_intersection(self):
        self.points = []
        enemy_box_intersection_points = []
        for a in self.multiple_rays_pos:
            
 

            self.intersection_points = []
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

                self.t_num = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4))
                self.u_num = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2))
                self.den = ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
                if self.den == 0:
                    return
                self.t = (self.t_num / self.den)    
                self.u = self.u_num / self.den
                self.point_of_intersection = (x1 + self.t * (x2 - x1)), (y1 + self.t * (y2 - y1)) 
                if (0 < self.t) and (self.t < 1) and (1 > self.u > 0):
                    self.intersection_points.append(self.point_of_intersection)
                    
                    num_of_intersections += 1



            if len(self.intersection_points) > 0:
                z = self.check_nearest_point()
                self.points.append(z)
            else:
                #pg.draw.aaline(self.window, ray_color, self.player_pos, a)
                self.points.append(a)

        
        for a in self.points:
            x = self.enemy.line1, self.enemy.line2
            
            for i in x:
                x1 = i[0][0]
                y1 = i[0][1]
                x2 = i[1][0]
                y2 = i[1][1]
                x3 = self.player_pos[0]
                y3 = self.player_pos[1]
                x4 = a[0]
                y4 = a[1]

                self.t_num = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4))
                self.u_num = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2))
                self.den = ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
                if self.den == 0:
                    return
                self.t = (self.t_num / self.den)    
                self.u = self.u_num / self.den
                self.point_of_intersection = (x1 + self.t * (x2 - x1)), (y1 + self.t * (y2 - y1)) 
                if (0 < self.t < 1) and (0 < self.u < 1):
                    enemy_box_intersection_points.append(a)
                    pg.draw.aaline(self.window, 'green', self.player_pos, self.point_of_intersection)

        try:
            self.point_len = m.ceil(len(enemy_box_intersection_points)/2)
            self.middle_point = enemy_box_intersection_points[self.point_len]
        except:
            pass
            #print(len(enemy_box_intersection_points)/2)

            

            

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
                point_dis[pyth] = (x2, y2)
            point_dis = sorted(point_dis.items())
            x = point_dis[0][1]
            #pg.draw.aaline(self.window, ray_color, self.player_pos, x)
            #self.points[x] = None
            return x
        
class Graphics:
    def __init__(self, minimap):
        self.wall_texture = pg.image.load('textures/wall.jpg')
        self.window = minimap.window
        self.player = minimap.player
        self.enemy = minimap.enemy
        self.win_size = pg.display.get_window_size()

        self.A_texture = pg.image.load('textures/A.png')
        self.A_texture_size = self.A_texture.get_width(), self.A_texture.get_height()
        
        #self.chase_image = pg.image.load('textures/chase_image.jpg').convert_alpha()
        self.chase_rect = pg.Rect(0, 0, self.win_size[0], self.win_size[1])
        self.transparent_surface = pg.Surface((self.win_size[0], self.win_size[1]), pg.SRCALPHA)

        #AUDIO
        
        
        self.heartbeat_audio = pg.mixer.Sound('audio/heart_beat.mp3')
        self.heartbeat_audio.set_volume(0)
        self.heartbeat_audio.play(loops=-1)
        
        self.tv_static_audio = pg.mixer.Sound('audio/tv_static.wav')
        self.tv_static_audio.set_volume(0)
        self.tv_static_audio.play(loops=-1)

        self.ambience = pg.mixer.Sound('audio/ambience.wav')
        self.ambience.set_volume(.3)
        self.ambience.play(loops=-1)

        self.footsteps = pg.mixer.Sound('audio/footsteps.wav')
        self.footsteps.set_volume(1)
        self.footsteps.play(loops=-1)

    def render_walls(self):
        self.vertical_angle = self.player.vertical_angle
        va = 300#self.vertical_angle
        winsize = self.win_size
        x = 4
        coord = None
        for i in self.player.points:
            x1 = self.player.player_pos[0]
            y1 = self.player.player_pos[1]
            x2 = i[0]
            y2 = i[1]

            dif = (x2 - x1, y2 - y1)
            angle = (m.degrees(m.atan2(dif[1], dif[0]))) - self.player.angle
            pyth = m.sqrt(dif[0]**2 + dif[1]**2)
            dis = pyth * m.cos(m.radians(angle))
            a = ((30 * winsize[1]) / (dis)) #/ 10
            #a = (50000 / pyth) / 10
            color = [181, 181, 181]
            c1 = []
            for b in color:
                c1.append(b * (1 - (pyth / fov_length)))

            #try:
            g = self.min_and_max(0, 20, 200)
            g = int(g)
            ds = r.randint(0, g)
            pg.draw.line(self.window, c1, (x, va + a + ds), (x, va - a - ds), 5)

            #except:
                #pass

            if self.player.point_len != 0:
                #print(self.player.middle_point, '==', i)
                #print(self.player.points)
                if self.player.middle_point == i:
                    #pg.draw.circle(self.window, 'red', (x, va), 100)
                    coord = (x, va)
                    
            x += 4.44
        try:
            self.enemy_sprite_size_calculator()
            self.window.blit(self.A_texture_scaled, (coord[0] - self.A_texture_dimension_half[0], coord[1] - (self.A_texture_dimension_half[1] - (self.a))))
        
        except:
            pass
            #print('Error render_walls()')


    def enemy_sprite_size_calculator(self):
        self.a = ((2.3 * self.win_size[1]) / (self.enemy.distance_to_player))
        if self.a > 90:
            self.a = 90
        self.A_texture_scaled = pg.transform.scale(self.A_texture, (self.A_texture_size[0] * self.a, self.A_texture_size[1] * self.a))
        self.A_texture_dimension = self.A_texture_scaled.get_rect().size
        self.A_texture_dimension_half = ((self.A_texture_dimension[0] / 2), (self.A_texture_dimension[1] / 2))

    def draw_chase_texture(self):
        
        self.b = max(0, min(90, (170 - self.enemy.distance_to_player) * (90 / 170))) * 2
        if self.b > 90:
            self.b = 90
        #self.chase_rect_clone = self.chase_rect.copy()
        #self.chase_rect_scaled = pg.transform.scale(self.chase_image_clone, (self.chase_image.get_width() * 25, self.chase_image.get_height() * 19))
        #pg.draw.rect(self.window, (255, 0, 0, self.b), self.chase_rect_clone, pg.BLEND_RGBA_MULT)
        #self.chase_rect_clone.fill((255, 255, 255, self.b), None, pg.BLEND_RGBA_MULT)
       # self.window.blit(self.chase_rect_clone, (0, 0))    
        self.transparent_surface.fill((255, 0, 0, self.b))
        self.window.blit(self.transparent_surface, (0, 0))

        f = 1
        self.c = self.min_and_max(0, f, 250)
        self.d = self.min_and_max(0, 0.25, 150)
        #elf.c = max(0, min(f, (170 - self.enemy.distance_to_player) * (f / 170)))
        #print(self.d)
        if self.c > f:
            self.c = f
        self.heartbeat_audio.set_volume(self.c)
        self.tv_static_audio.set_volume(self.d)  

    def min_and_max(self, a, b, c):
        x = max(a, min(b, (c - self.enemy.distance_to_player) * (b / c)))
        return x

'''
            item = self.player.points[i]
            if item == 'Enemy':
                pg.draw.circle(self.window, 'red', (x, va), 100)

'''

    #def render_ceiling


class Enemy:
    def __init__(self, minimap) -> None:
        self.entity = 0
        self.minimap = minimap
        self.game = minimap.game
        self.window = minimap.window
        self.coordinate = (800, 600)
        self.line1 = (0, 0), (0, 0)
        self.line2 = (0, 0), (0, 0)
        self.distance_to_player = 0
        self.last_node = (0, 0)
        self.path_gen(35, 24, 35, 24)

        
    def draw(self):
        self.draw_render_box()
        self.movement()
        self.distance_to_player_checker()

    def draw_render_box(self):
        self.render_box = [(self.coordinate[0] - 10, self.coordinate[1] - 10), (self.coordinate[0] + 10, self.coordinate[1] + 10)]
        self.line1 = (self.render_box[0][0], self.coordinate[1]), (self.render_box[1][0], self.coordinate[1])
        self.line2 = (self.coordinate[0], self.render_box[0][1]), (self.coordinate[0], self.render_box[1][1])
        pg.draw.line(self.window, 'white', (self.render_box[0][0], self.coordinate[1]), (self.render_box[1][0], self.coordinate[1]))
        pg.draw.line(self.window, 'white', (self.coordinate[0], self.render_box[0][1]), (self.coordinate[0], self.render_box[1][1]))

    def movement(self):
        if len(self.pos_nodes) > 0:
            self.speed = (enemy_speed/30) * self.game.delta_time
            
            #for i in self.pos_nodes:
            self.at_des = False
            self.target_node = self.pos_nodes[0]
            targ_coor = self.target_node
                #while True:
            epos = self.coordinate
            x = epos[0]
            y = epos[1]
            '''
            if targ_coor[0] < epos[0]:
                x = epos[0] - self.speed
            elif targ_coor[0] > epos[0]:
                x = epos[0] + self.speed

            if targ_coor[1] < epos[1]:
                y = epos[1] - self.speed
            elif targ_coor[1] > epos[1]:
                y = epos[1] + self.speed'''
            
            dx = targ_coor[0] - epos[0]
            dy = targ_coor[1] - epos[1]

            angle = m.atan2(dy, dx)

            x += m.cos(angle) * self.speed
            y += m.sin(angle) * self.speed
            
            self.coordinate = (x, y)
            
            if self.check_if_des():
                self.pos_nodes.pop(0)

        else:
            self.path_finished()

    def check_if_des(self):
        if abs(self.coordinate[0] - self.target_node[0]) < 3 and abs(self.coordinate[1] - self.target_node[1]) < 3:
            #self.pos_nodes.pop(0)
            return True
        else: 
            return False

    def path_gen(self, x1, y1, x2, y2):
        grid = Grid(matrix= matrix) 

        start = grid.node(x1, y1)
        end = grid.node(x2, y2)
        self.last_node = (x2, y2)

        finder = AStarFinder(diagonal_movement= DiagonalMovement.always)

        self.path, runs = finder.find_path(start, end, grid)

        self.pos_node()

    def path_finished(self):
        while True:
            if self.random_node_picker():
                break
        self.path_gen(self.last_node[0], self.last_node[1], self.matrix_x, self.matrix_y)

    def random_node_picker(self):
        self.matrix_x = r.randint(0, column_lenght - 1)
        self.matrix_y = r.randint(0, row_length - 1)
        if matrix[self.matrix_y][self.matrix_x] == 1:
            return True
        else:
            return False

    def pos_node(self):
        self.pos_nodes = []
        for i in self.path:
            self.pos_nodes.append(((i[0] * x_dif) + additional_grid_value, (i[1] * y_dif) + additional_grid_value))
        #self.pos_nodes.pop(0)
    
    def distance_to_player_checker(self):
        self.player_pos = self.minimap.player.player_pos
        x = round(self.player_pos[0] - self.coordinate[0], 2)
        y = round(self.player_pos[1] - self.coordinate[1], 2)
        self.distance_to_player = round(m.sqrt(x**2 + y**2), 2) # HYPOTENUSE FORMULA