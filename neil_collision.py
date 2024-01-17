import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Collision Detector")

# Set up colors
white = (255, 255, 255)
red = (255, 0, 0)

# Set up rectangles
rect1 = pygame.Rect(100, 100, 50, 50)
rect2 = pygame.Rect(200, 200, 50, 50)

# Set up clock
clock = pygame.time.Clock()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Save the previous position of rect1
    prev_rect1_pos = rect1.topleft

    # Move rectangles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rect1.x -= 20
    if keys[pygame.K_RIGHT]:
        rect1.x += 20
    if keys[pygame.K_UP]:
        rect1.y -= 20
    if keys[pygame.K_DOWN]:
        rect1.y += 20

    # Check for collisions
    if rect1.colliderect(rect2):
        # Handle collision by setting the position back to the previous position
        rect1.topleft = prev_rect1_pos

    # Clear the screen
    screen.fill(white)

    # Draw rectangles
    pygame.draw.rect(screen, red, rect1)
    pygame.draw.rect(screen, red, rect2)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

