from prescaling import *
from map_data import *
from settings import *
from pathfinding.core.grid import *
from pathfinding.finder.a_star import AStarFinder
import pygame as pg, math as m, random as r


pg.mixer.init(buffer=1024)

class Body:
    def __init__(self, game) -> None:
        self.game = game
        self.window = game.window
        self.enemy = Enemy(self)
        self.powercell = PowerCell(self)
        self.powersystem = PowerSystem(self)
        self.player = Player(self)
        self.graphics = Graphics(self)
        self.ui = UI(self)
        self.vertical_collision = vertical_collision
        self.horizontal_collision = horizontal_collision

        self.SCB = SCB
        print(self.horizontal_collision, self.vertical_collision)

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
class UI:
    def __init__(self, body) -> None:
        self.body = body
        self.game = body.game
        self.window = body.window

        self.jumpscare_img = pg.image.load('textures/A_jumpscare.png')
        x = 5
        self.jumpscare_img = pg.transform.scale(self.jumpscare_img, (self.jumpscare_img.get_width() * x, self.jumpscare_img.get_height() * x))
        self.pos = r.randint(160, 640) - self.jumpscare_img.get_width()/2, r.randint(-50, 20)


        # Flag

    def update(self):
        self.draw()

    def draw(self):
        self.jumpscare()
        self.sprint_bar()

    def jumpscare(self):
        if not self.body.player.alive:
            self.window.blit(self.jumpscare_img, (self.pos))

    def sprint_bar(self):
        pg.draw.line(self.window, 'green', (20, 200), (20, 400), 4)


class Player:
    
    def __init__(self, body):
        self.walls = {}
        self.body = body
        self.game = self.body.game
        self.window = self.game.window
        self.enemy = self.body.enemy
        self.powercell = body.powercell
        self.powersystem = body.powersystem
        self.alive = True
        self.stamina = 100
        self.player_pos = [35, 20]
        self.angle = 90
        
        self.vertical_angle = pg.display.get_window_size()[1] / 2
        self.middle_point = 0
        self.point_len = 0
        self.middle_point2 = 0
        self.point_len2 = 0
        self.middle_point3 = 0
        self.point_len3 = 0
        self.points = []
        self.seen_by_enemy = False
        self.player_sees_enemy = False
        self.game_over = False
        self.return_to_menu_delay = 0
        self.speed = player_speed

        for i in line_walls:
            for a in i:
                self.walls[a] = 'w'
        for i in doors:
            self.walls[i] = 'b'


    def draw(self):
        self.draw_ray()

        self.player_rect_collision = pg.Rect(self.player_pos[0] - 10, self.player_pos[1] - 10, 20, 20)
        #pg.draw.rect(self.window, rect_collision_color, self.player_rect_collision)

        #self.player_circle = pg.draw.circle(win, 'white', self.player_pos, 10)
        if self.alive:
            self.movement()

        self.check_intersection()

        self.enemy_vision()
        self.return_to_menu()

    def draw_ray(self):
        win = self.window
        pos = self.player_pos
        ang = self.angle
        x = pos[0] + (m.cos(m.radians(ang)) * ray_length)
        y = pos[1] + (m.sin(m.radians(ang)) * ray_length)
        pg.draw.aaline(win, ray_color, pos, (x, y))

        self.cast_multiple_rays()

    def turn(self):
        if self.alive:
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
        self.speed = (player_speed / 30) * self.game.delta_time
        sin_a = m.sin(m.radians(self.angle))
        cos_a = m.cos(m.radians(self.angle))
        speed_sin = self.speed * sin_a
        speed_cos = self.speed * cos_a
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

        if self.player_rect_collision.collidepoint(self.powercell.pos):
            print('Touch Powercell')
    
    def min_and_max(self, a, b, c):
        x = max(a, min(b, (c - self.enemy.distance_to_player) * (b / c)))
        return x

    def cast_multiple_rays(self):
        self.multiple_rays_pos = []
        if self.alive:
            pf = player_fov + self.min_and_max(0, 45, 170)
        else:
            pf = player_fov
        cone_angle = pf * (m.pi / 180)
        for i in range(num_rays):
            angle = m.radians(self.angle) + (i - num_rays / 2) * cone_angle / num_rays
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
                    pg.draw.aaline(self.window, 'green', self.player_pos, self.point_of_intersection)


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
                    pg.draw.aaline(self.window, 'green', self.player_pos, self.point_of_intersection)

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
                    pg.draw.aaline(self.window, 'green', self.player_pos, self.point_of_intersection)


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

        #print(powersystem_cross_intersection)
        self.point_len3 = len(powersystem_cross_intersection)//2
        if self.point_len3 != 0:
            self.middle_point3 = powersystem_cross_intersection[self.point_len3]
            self.powersystem.calculate_distance_to_player()


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
                pg.draw.aaline(self.window, 'blue', self.player_pos, self.enemy_ray_point)
            except:
                pass

    def fgame_over(self):
        self.alive = False
        self.game_over = True
        self.angle = m.degrees(self.enemy_angle)
        self.body.graphics.jumpscare.play()

    def return_to_menu(self):
        if not self.alive:
            if self.return_to_menu_delay < 25:
                self.return_to_menu_delay += .01 * self.game.delta_time
            else:
                self.game.menu.running = True
                pg.mouse.set_visible(True)
class Graphics:
    def __init__(self, body):
        self.wall_texture = pg.image.load('textures/wall.jpg')
        self.window = body.window
        self.player = body.player
        self.body = body
        self.enemy = body.enemy
        self.powersystem = body.powersystem
        self.powercell = body.powercell
        self.win_size = pg.display.get_window_size()
        self.fog = 1
        self.or_fog = self.fog
        self.a = 0

        self.A_texture = pg.image.load('textures/A.v2.png')
        self.A_texture_size = self.A_texture.get_width(), self.A_texture.get_height()
        
        #self.chase_image = pg.image.load('textures/chase_image.jpg').convert_alpha()
        self.chase_rect = pg.Rect(0, 0, self.win_size[0], self.win_size[1])
        self.transparent_surface = pg.Surface((self.win_size[0], self.win_size[1]), pg.SRCALPHA)

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

        #AUDIO
        self.heartbeat_audio = pg.mixer.Sound('audio/heart_beat.mp3')
        self.tv_static_audio = pg.mixer.Sound('audio/tv_static.wav')
        self.ambience = pg.mixer.Sound('audio/ambience.wav')
        self.jumpscare = pg.mixer.Sound('audio/jumpscare.wav')
        self.jumpscare.set_volume(.7)

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
        self.vertical_angle = self.player.vertical_angle
        va = 300#self.vertical_angle
        winsize = self.win_size
        x = 4
        coord = None
        coord2 = None
        coord3 = None
        
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
                a = ((30 * winsize[1]) / (dis)) #/ 10
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
                pg.draw.line(self.window, c1, (x, va + a + ds), (x, va - a - ds), 5)
            except:
                pass

            #except:
                #pass

            if self.player.point_len != 0:
                #print(self.player.middle_point, '==', i)
                #print(self.player.points)
                if self.player.middle_point == i:
                    #pg.draw.circle(self.window, 'red', (x, va), 100)
                    coord = (x, va)

            if self.player.point_len2 != 0:
                if self.player.middle_point2 == i:

                    coord2 = (x, va)

            if self.player.point_len3 != 0:
                if self.player.middle_point3 == i:
                    coord3 = (x, va)

            #else:
                #print(self.player.point_len)
                    
            x += 4.44
        
            
        if self.player.player_sees_enemy:
            self.enemy_sprite_size_calculator()
        if coord != None:
            if self.player.alive:
                self.window.blit(self.A_texture_scaled, (coord[0] - self.A_texture_dimension_half[0], coord[1] - (self.A_texture_dimension_half[1] - (self.a))))
        
        
        self.pc_wave += .005 * self.body.game.delta_time
        wave = m.sin(self.pc_wave) * 15
        self.pc_sprite_size_calculator()
        if coord2 != None:
            self.window.blit(self.powercell_img, (coord2[0] - self.powercell_img.get_width() / 2, coord2[1] - ((self.powercell_img.get_height() / 2) + wave - (self.pc * 5))))

        self.ps_sprite_size_calculator()
        if coord3 != None:
            self.window.blit(self.powersystem_img0, (coord3[0] - self.powersystem_img0.get_width() / 2, coord3[1] - ((self.powersystem_img0.get_height() / 2))))



    def enemy_sprite_size_calculator(self):
        
        self.a = ((.3 * self.win_size[1]) / (self.enemy.distance_to_player))
        x = 5
        if self.a > x:
            self.a = x
        self.A_texture_scaled = pg.transform.scale(self.A_texture, (self.A_texture_size[0] * self.a, self.A_texture_size[1] * self.a))
        self.A_texture_dimension = self.A_texture_scaled.get_rect().size
        self.A_texture_dimension_half = ((self.A_texture_dimension[0] / 2), (self.A_texture_dimension[1] / 2))

    def ps_sprite_size_calculator(self):
        self.ps = ((self.win_size[1]) / self.powersystem.distance_to_player)
        if self.ps > 25:
            self.ps = 25
        if int(self.ps) > 0:
            self.powersystem_img0 = scaled_img[int(self.ps)]
        else:
            self.powersystem_img0 = scaled_img[2]

    def pc_sprite_size_calculator(self):
        self.pc = ((self.win_size[1]) / self.powercell.distance_to_player)
        if self.pc > 10:
            self.pc = 10
        if int(self.pc) > 0:
            self.powercell_img = scaled_img_powercell[int(self.pc)]
        else:
            self.powercell_img = scaled_img_powercell[2]

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
        else:
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
        pg.draw.line(self.window, 'white', (self.render_box[0][0], self.enemy_coordinate[1]), (self.render_box[1][0], self.enemy_coordinate[1]))
        pg.draw.line(self.window, 'white', (self.enemy_coordinate[0], self.render_box[0][1]), (self.enemy_coordinate[0], self.render_box[1][1]))

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
        print('create path 1')
        while True:
            if self.random_node_picker():
                break
                
        self.path_gen(self.last_node[0], self.last_node[1], self.matrix_x, self.matrix_y)

    def create_path_2(self):
        print('create path 2')
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
        print(len(self.pyths))
        self.pyths = sorted(self.pyths.items())
        print(f'Pyths Length: [{len(self.pyths)}]')

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
        #print(self.distance_to_player)

    def check_if_see_player(self):
        self.see_player =  self.body.player.seen_by_enemy
        if self.see_player:
            self.go_to_seen_pos = True

class PowerCell:
    def __init__(self, body) -> None:
        self.body = body
        self.window = body.window
        self.powered = False
        self.pos = (185, 300)
        self.cross_size = 8
        self.cross = ((0, 0), (0, 0), (0, 0), (0, 0))
        self.line1 = (0, 0), (0, 0)
        self.line2 = (0, 0),  (0, 0)
        self.distance_to_player = 1


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

class PowerSystem:
    def __init__(self, body) -> None:
        self.body = body
        self.window = body.window
        self.power = 0
        self.pos = (185, 270)
        self.cross_size = 8
        self.cross = ((0, 0), (0, 0), (0, 0), (0, 0))
        self.line1 = (0, 0), (0, 0)
        self.line2 = (0, 0),  (0, 0)
        self.distance_to_player = 1

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
