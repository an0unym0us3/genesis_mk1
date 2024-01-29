import pygame
import sys

pygame.init()

#Music for title screen
pygame.mixer.music.load('./Media/music/TitleMusic.mp3')
pygame.mixer.music.play(-1)

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

# Set up the font with Courier for the Start, Credit and Exit button
font_size=36
startfont = pygame.font.Font(pygame.font.match_font('courier'), font_size)
exitfont = pygame.font.Font(pygame.font.match_font('courier'), font_size)
creditsfont = pygame.font.Font(pygame.font.match_font('courier'),font_size)
startfont_size=font_size
exitfont_size=font_size
creditsfont_size=font_size
start_text = "-Start-"

# Set up the rectangle for the Exit button
exit_button = pygame.Rect(0, 0, 280, 100)
exit_button.topleft = (original_x, original_y + 125)  # Placed way below the Start button
exit_color = (0, 255, 0)  # black color for Exit button
exit_size_increased = False

# Set up the font with Courier for the Exit button
exit_text = "-Exit-"

# Set up the rectangle for the Credit button
credits_button = pygame.Rect(0, 0, 280, 100)
credits_button.topleft = (original_x, original_y + 250)  # Placed way below the Start button
credits_color = (0, 255, 0)  # black color for Exit button
credits_size_increased = False

credits_text = "-Credits-"

# Set up the rectangle and font for the title
title_button = pygame.Rect(0, 0, 200, 50)
title_button.topleft = (original_x + 40, original_y - 100)
title_color = (0, 0, 0)  # black background
title_font_size = 60
title_font = pygame.font.Font(pygame.font.match_font('courier'), title_font_size)
title_text = "FALSHSTORM"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if start_button.collidepoint(event.pos):
                    print("Start button clicked!")
                    # You can add functionality for the Start button here
                    pygame.quit()
                    import collisionA
                    sys.exit()
                elif exit_button.collidepoint(event.pos):
                    print("Exit button clicked!")
                    running = False  # Exit the program
                elif credits_button.collidepoint(event.pos):
                    credits_running=True
                    while credits_running:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                credits_running = False

                        screen.fill("black")

                        #render credits text
                        credtext='''TEAM GENESIS_MK1: ADIT MANAV RAYHAAN MURSHID NEIL'''
                        credits_text_surface=startfont.render(credtext, True, (255,255,255))

                        #getting the rectangle
                        cred_rect=credits_text_surface.get_rect()

                        cred_rect.center=(1280//2,720//2)

                        screen.blit(credits_text_surface,cred_rect)

                        pygame.display.flip()

                        clock.tick(60)
                        

    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Check for Start button interaction
    if start_button.collidepoint(mouse_x, mouse_y):
        start_color = hover_color
        if not start_size_increased:
            # Increase the size and adjust the position for the expansion
            start_button.inflate_ip(25, 50)
            start_button.topleft = (original_x - 12, original_y - 25)
            startfont_size += 10  # Increase font size by 10
            startfont = pygame.font.Font(pygame.font.match_font('courier'), startfont_size)
            start_size_increased = True
    else:
        start_color = original_color
        if start_size_increased:
            # Reset the size and position to the original state
            start_button = pygame.Rect(0, 0, 280, 100)
            start_button.topleft = (original_x, original_y)
            startfont_size = 36  # Reset to original font size
            startfont = pygame.font.Font(pygame.font.match_font('courier'), startfont_size)
            start_size_increased = False

    # Check for Exit button interaction
    if exit_button.collidepoint(mouse_x, mouse_y):
        exit_color = hover_color
        if not exit_size_increased:
            # Increase the size and adjust the position for the expansion
            exit_button.inflate_ip(25, 50)
            exitfont_size+=10
            exitfont = pygame.font.Font(pygame.font.match_font('courier'), exitfont_size)
            exit_button.topleft = (original_x - 12, original_y + 100)
            exit_size_increased = True
    else:
        exit_color = (0, 255, 0)  # Reset color to green for the Exit button
        if exit_size_increased:
            # Reset the size and position to the original state
            exit_button = pygame.Rect(0, 0, 280, 100)
            exit_button.topleft = (original_x, original_y + 125)
            exitfont_size=36
            exitfont = pygame.font.Font(pygame.font.match_font('courier'), exitfont_size)
            exit_size_increased = False

    if credits_button.collidepoint(mouse_x, mouse_y):
        credits_color = hover_color
        if not credits_size_increased:
            # Increase the size and adjust the position for the expansion
            credits_button.inflate_ip(25, 50)
            credits_button.topleft = (original_x - 12, original_y + 225)
            creditsfont_size += 10  # Increase font size by 10
            creditsfont = pygame.font.Font(pygame.font.match_font('courier'), creditsfont_size)
            credits_size_increased = True
    else:
        credits_color = (0, 255, 0)  # Reset color to green for the Exit button
        if credits_size_increased:
            # Reset the size and position to the original state
            credits_button = pygame.Rect(0, 0, 280, 100)
            credits_button.topleft = (original_x, original_y + 250)
            creditsfont_size = 36
            creditsfont = pygame.font.Font(pygame.font.match_font('courier'), creditsfont_size)
            credits_size_increased = False


    screen.fill("black")

    # Draw the title as a separate object with a cyan background
    pygame.draw.rect(screen, title_color, title_button)
    title_surface = title_font.render(title_text, True, (0, 255, 0))
    title_rect = title_surface.get_rect(center=(title_button.x + title_button.width // 2, title_button.y + title_button.height // 2))
    screen.blit(title_surface, title_rect)

    # Draw the Start button
    pygame.draw.rect(screen, start_color, start_button)
    start_text_surface = startfont.render(start_text, True, (255, 255, 255))
    start_text_rect = start_text_surface.get_rect(center=(start_button.x + start_button.width // 2, start_button.y + start_button.height // 2))
    screen.blit(start_text_surface, start_text_rect)

    # Draw the Exit button
    pygame.draw.rect(screen, (0,0,0), exit_button)
    exit_text_surface = exitfont.render(exit_text, True, (255, 255, 255))
    exit_text_rect = exit_text_surface.get_rect(center=(exit_button.x + exit_button.width // 2, exit_button.y + exit_button.height // 2))
    screen.blit(exit_text_surface, exit_text_rect)

    # Draw the Credits button
    pygame.draw.rect(screen, (0,0,0), credits_button)
    credits_text_surface = creditsfont.render(credits_text, True, (255, 255, 255))
    credits_text_rect = credits_text_surface.get_rect(center=(credits_button.x + credits_button.width // 2, credits_button.y + credits_button.height // 2))
    screen.blit(credits_text_surface, credits_text_rect)

    pygame.display.flip()
    clock.tick(60)


pygame.quit()

