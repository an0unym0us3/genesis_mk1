import pygame
import sys

pygame.init()

# Set the title of the display window
pygame.display.set_caption("My Pygame Window")

screen = pygame.display.set_mode((1280, 720))

clock = pygame.time.Clock()

running = True

# Calculate the initial position for the center of the screen
original_x = (1280 - 280) // 2
original_y = (720 - 100) // 2

# Set up the rectangle for the Start button
start_button = pygame.Rect(0, 0, 280, 100)
start_button.topleft = (original_x, original_y)
original_color = (0, 0, 0)
hover_color = (0, 0, 0)
start_size_increased = False

# Set up the font with Courier for the Start button
font_size = 36
font = pygame.font.Font(pygame.font.match_font('courier'), font_size)
start_text = "Start"

# Set up the rectangle for the Exit button
exit_button = pygame.Rect(0, 0, 280, 100)
exit_button.topleft = (original_x, original_y + 200)  # Placed way below the Start button
exit_color = (0, 0, 0)  # black color for Exit button
exit_size_increased = False

# Set up the font with Courier for the Exit button
exit_text = "Exit"

# Set up the rectangle and font for the title
title_button = pygame.Rect(0, 0, 200, 50)
title_button.topleft = (original_x + 40, original_y - 100)
title_color = (0, 0, 0)  # black background
title_font_size = 24
title_font = pygame.font.Font(pygame.font.match_font('courier'), title_font_size)
title_text = "GENESIS MK_1"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if start_button.collidepoint(event.pos):
                    print("Start button clicked!")
                    # You can add functionality for the Start button here
                elif exit_button.collidepoint(event.pos):
                    print("Exit button clicked!")
                    running = False  # Exit the program

    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Check for Start button interaction
    if start_button.collidepoint(mouse_x, mouse_y):
        start_color = hover_color
        if not start_size_increased:
            # Increase the size and adjust the position for the expansion
            start_button.inflate_ip(25, 50)
            start_button.topleft = (original_x - 12, original_y - 25)
            font_size += 10  # Increase font size by 10
            font = pygame.font.Font(pygame.font.match_font('courier'), font_size)
            start_size_increased = True
    else:
        start_color = original_color
        if start_size_increased:
            # Reset the size and position to the original state
            start_button = pygame.Rect(0, 0, 280, 100)
            start_button.topleft = (original_x, original_y)
            font_size = 36  # Reset to original font size
            font = pygame.font.Font(pygame.font.match_font('courier'), font_size)
            start_size_increased = False

    # Check for Exit button interaction
    if exit_button.collidepoint(mouse_x, mouse_y):
        exit_color = hover_color
        if not exit_size_increased:
            # Increase the size and adjust the position for the expansion
            exit_button.inflate_ip(25, 50)
            font_size+=10
            font = pygame.font.Font(pygame.font.match_font('courier'), font_size)
            exit_button.topleft = (original_x - 12, original_y + 150 - 25)
            exit_size_increased = True
    else:
        exit_color = (0, 255, 0)  # Reset color to green for the Exit button
        if exit_size_increased:
            # Reset the size and position to the original state
            exit_button = pygame.Rect(0, 0, 280, 100)
            exit_button.topleft = (original_x, original_y + 150)
            font_size=36
            font = pygame.font.Font(pygame.font.match_font('courier'), font_size)
            exit_size_increased = False

    screen.fill("black")

    # Draw the title as a separate object with a cyan background
    pygame.draw.rect(screen, title_color, title_button)
    title_surface = title_font.render(title_text, True, (0, 255, 0))
    title_rect = title_surface.get_rect(center=(title_button.x + title_button.width // 2, title_button.y + title_button.height // 2))
    screen.blit(title_surface, title_rect)

    # Draw the Start button
    pygame.draw.rect(screen, start_color, start_button)
    start_text_surface = font.render(start_text, True, (255, 255, 255))
    start_text_rect = start_text_surface.get_rect(center=(start_button.x + start_button.width // 2, start_button.y + start_button.height // 2))
    screen.blit(start_text_surface, start_text_rect)

    # Draw the Exit button
    pygame.draw.rect(screen, (0,0,0), exit_button)
    exit_text_surface = font.render(exit_text, True, (255, 255, 255))
    exit_text_rect = exit_text_surface.get_rect(center=(exit_button.x + exit_button.width // 2, exit_button.y + exit_button.height // 2))
    screen.blit(exit_text_surface, exit_text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
