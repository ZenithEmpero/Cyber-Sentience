import pygame
from pygame.math import Vector2

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up the line and circle
line_start = Vector2(100, 100)
line_end = Vector2(500, 100)
line_velocity = Vector2(5, 0)
line_color = (255, 255, 255)
line_width = 5
circle_pos = Vector2(320, 240)
circle_radius = 50
circle_velocity = Vector2(0, 5)
circle_color = (255, 0, 0)

# Set up the clock
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the line and circle
    line_start += line_velocity
    line_end += line_velocity
    circle_pos += circle_velocity

    # Check for collisions
    line_vec = line_end - line_start
    line_len = line_vec.length()
    line_norm = line_vec.normalize()
    circle_vec = circle_pos - line_start
    dot_product = circle_vec.dot(line_norm)
    closest_point = line_start + line_norm * dot_product
    dist = closest_point.distance_to(circle_pos)
    if dist <= circle_radius and 0 <= dot_product <= line_len:
        circle_velocity = -circle_velocity

    # Check for screen bounds
    if line_start.x < 0 or line_end.x > screen_width:
        line_velocity.x = -line_velocity.x
    if circle_pos.x - circle_radius < 0 or circle_pos.x + circle_radius > screen_width:
        circle_velocity.x = -circle_velocity.x
    if line_start.y < 0 or line_end.y > screen_height:
        line_velocity.y = -line_velocity.y
    if circle_pos.y - circle_radius < 0 or circle_pos.y + circle_radius > screen_height:
        circle_velocity.y = -circle_velocity.y

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the line and circle
    pygame.draw.line(screen, line_color, line_start, line_end, line_width)
    pygame.draw.circle(screen, circle_color, circle_pos, circle_radius)

    # Update the screen
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Clean up Pygame
pygame.quit()
