import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 300
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_COLOR = (0, 128, 255)
BUTTON_TEXT_COLOR = (255, 255, 255)
FPS = 60

# Create the main window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Button Example")

# Create font
font = pygame.font.Font(None, 36)

# Function to open the second window
def open_second_window():
    second_window = pygame.display.set_mode((300, 200))
    pygame.display.set_caption("Second Window")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

# Main game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                open_second_window()

    # Draw the button
    button_rect = pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT))
    button_text = font.render("Open Second Window", True, BUTTON_TEXT_COLOR)
    screen.blit(button_text, (WIDTH // 2 - button_text.get_width() // 2, HEIGHT // 2 - button_text.get_height() // 2))

    pygame.display.flip()
    clock.tick(FPS)
