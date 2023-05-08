import math as m

# DEV WINDOW
second_window = False
sw_size = ('250x250+50+50')
wall_color = 'white'
SCB = False   # SHOW COLLISION BOX

# GAME SETTINGS
minimap = True
WIDTH, HEIGHT = (800, 600)
FPS = 60
bg_color = 'black'

# PLAYER SETTINGS
player_speed = 1.3 #1
mouse_sensitivity= .1
ray_length = 500

num_rays = 180
player_fov = 40 #45
cone_angle = player_fov * (m.pi / 180)
fov_length = 500

# MINIMAP SETTINGS
ray_color = 'green'
rect_collision_color = (93, 232, 244)

# GRAPHICS SETTINGS
WALL_SIZE = 40