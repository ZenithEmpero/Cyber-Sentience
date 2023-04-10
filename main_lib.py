from map_data import *
from settings import *
from dev_win import *
import pygame as pg, math as m

class Minimap:
    def __init__(self, game) -> None:
        self.window = game.window
        self.player = Player(game)
        self.grahics = Graphics(self)

        self.SCB = SCB

    def draw(self):
        self.draw_line_wall()
        self.player.draw()
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


class Player:
    def __init__(self, game):
        self.walls = []
        self.game = game
        self.window = game.window
        self.alive = True
        self.player_pos = [35, 20]
        self.angle = 0

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
            if mouse_rel != (0, 0):
                self.angle += (mouse_rel[0] * mouse_sensitivity)
            
            if (mouse_pos[0] > (WIDTH - 200)) or (mouse_pos[0] < 200) or (mouse_pos[1] > (HEIGHT - 200)) or (mouse_pos[1] < 200):
                pg.mouse.set_pos(WIDTH/2, HEIGHT/2)

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
        if pg.Rect.colliderect(self.player_rect_collision, wall1):
            self.player_pos[0] -= dx
            if self.player_pos[0] > wall2[0]:
                self.player_pos[0] += .06
            elif self.player_pos[0] < wall2[0]:
                self.player_pos[0] -= .06
        if pg.Rect.colliderect(self.player_rect_collision, wall2):
            self.player_pos[1] -= dy
            if self.player_pos[1] > wall2[1]:
                self.player_pos[1] += .06
            elif self.player_pos[1] < wall2[1]:
                self.player_pos[1] -= .06


    def cast_multiple_rays(self):
        self.multiple_rays_pos = []
        for i in range(num_rays):
            angle = m.radians(self.angle) + (i - num_rays / 2) * cone_angle / num_rays
            direction = [m.cos(angle), m.sin(angle)]
            end_point = (self.player_pos[0] + direction[0] * fov_length, self.player_pos[1] + direction[1] * fov_length)
            self.multiple_rays_pos.append(end_point)

    def check_intersection(self):
        self.points = []
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
                self.check_nearest_point()
            else:
                #pg.draw.aaline(self.window, ray_color, self.player_pos, a)
                self.points.append(a)

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
            self.points.append(x)
            return
        
class Graphics:
    def __init__(self, minimap):
        self.window = minimap.window
        self.player = minimap.player
        self.win_size = pg.display.get_window_size()

    def render(self):
        winsize = self.win_size
        x = 4
        for i in self.player.points:
            x1 = self.player.player_pos[0]
            y1 = self.player.player_pos[1]
            x2 = i[0]
            y2 = i[1]

            dif = (x2 - x1, y2 - y1)
            angle = (m.degrees(m.atan2(dif[1], dif[0]))) - self.player.angle
            pyth = m.sqrt(dif[0]**2 + dif[1]**2)
            dis = pyth * m.cos(m.radians(angle))
            a = (25 * winsize[1]) / (dis)
            color = [255 * (1 - ((pyth) / (fov_length)))] * 3
            pg.draw.line(self.window, color, (x, winsize[1]/2 + a), (x, winsize[1]/2 - a), 5)

            x += 4.44

