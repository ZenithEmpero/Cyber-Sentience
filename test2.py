import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Center position of the window
center_x = screen_width // 2
center_y = screen_height // 2
pygame.mouse.set_visible(True)  # Hide the system cursor
pygame.mouse.set_pos(center_x, center_y)  # Set the initial cursor position

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the relative mouse movement
    mouse_delta_x, mouse_delta_y = pygame.mouse.get_rel()

    # Update the camera or player view based on the mouse movement
    # ...

    # Center the cursor position
    pygame.mouse.set_pos(center_x, center_y)

    # Rest of your game logic and drawing code here

    pygame.display.flip()

# Quit Pygame
pygame.quit()
