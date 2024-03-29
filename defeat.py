import pygame
import sys

# Initializing
pygame.init()

# Set up screen
screen_width = 1280
screen_height = 720

# Set up colors with transparency
white = (255, 255, 255)
black = (0, 0, 0, 128)
green = (0, 255, 0)

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Defeat Screen")

# Load font
font = pygame.font.Font(None, 100)

# Load background image
background_image = pygame.image.load("Media/images/Defeat.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

def draw_defeat_screen():
    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Render text
    text = font.render("Defeat!", True, white)
    text_rect = text.get_rect(center=(screen_width // 2, (screen_height // 2)-100))

    # Draw text on the screen
    screen.blit(text, text_rect)

    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    draw_defeat_screen()
